package cmd

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"text/tabwriter"
	"time"

	"github.com/johntheyoung/roadrunner/internal/beeperapi"
	"github.com/johntheyoung/roadrunner/internal/config"
	"github.com/johntheyoung/roadrunner/internal/errfmt"
	"github.com/johntheyoung/roadrunner/internal/outfmt"
	"github.com/johntheyoung/roadrunner/internal/ui"
)

// MessagesCmd is the parent command for message subcommands.
type MessagesCmd struct {
	List   MessagesListCmd   `cmd:"" help:"List messages in a chat"`
	Search MessagesSearchCmd `cmd:"" help:"Search messages"`
	Send   MessagesSendCmd   `cmd:"" help:"Send a message to a chat"`
	Tail   MessagesTailCmd   `cmd:"" help:"Follow messages in a chat"`
}

// MessagesListCmd lists messages in a chat.
type MessagesListCmd struct {
	ChatID      string   `arg:"" name:"chatID" help:"Chat ID to list messages from"`
	Cursor      string   `help:"Pagination cursor (use sortKey from previous results)"`
	Direction   string   `help:"Pagination direction: before|after" enum:"before,after," default:"before"`
	Fields      []string `help:"Comma-separated list of fields for --plain output" name:"fields" sep:","`
	FailIfEmpty bool     `help:"Exit with code 1 if no results" name:"fail-if-empty"`
}

// Run executes the messages list command.
func (c *MessagesListCmd) Run(ctx context.Context, flags *RootFlags) error {
	u := ui.FromContext(ctx)
	chatID := normalizeChatID(c.ChatID)

	token, _, err := config.GetToken()
	if err != nil {
		return err
	}

	timeout := time.Duration(flags.Timeout) * time.Second
	client, err := beeperapi.NewClient(token, flags.BaseURL, timeout)
	if err != nil {
		return err
	}

	resp, err := client.Messages().List(ctx, chatID, beeperapi.MessageListParams{
		Cursor:    c.Cursor,
		Direction: c.Direction,
	})
	if err != nil {
		return err
	}

	if err := failIfEmpty(c.FailIfEmpty, len(resp.Items), "messages"); err != nil {
		return err
	}

	// JSON output
	if outfmt.IsJSON(ctx) {
		return outfmt.WriteJSON(os.Stdout, resp)
	}

	// Plain output (TSV)
	if outfmt.IsPlain(ctx) {
		fields, err := resolveFields(c.Fields, []string{"id", "sender_name", "timestamp", "text", "chat_id", "sort_key"})
		if err != nil {
			return err
		}
		for _, item := range resp.Items {
			writePlainFields(u, fields, map[string]string{
				"id":          item.ID,
				"chat_id":     item.ChatID,
				"sender_name": item.SenderName,
				"timestamp":   item.Timestamp,
				"text":        ui.Truncate(item.Text, 50),
				"sort_key":    item.SortKey,
			})
		}
		return nil
	}

	// Human-readable output
	if len(resp.Items) == 0 {
		u.Out().Warn("No messages found")
		return nil
	}

	u.Out().Printf("Messages (%d):\n", len(resp.Items))
	for _, item := range resp.Items {
		ts := ""
		if item.Timestamp != "" {
			if t, err := time.Parse(time.RFC3339, item.Timestamp); err == nil {
				ts = t.Format("Jan 2 15:04")
			}
		}
		text := ui.Truncate(item.Text, 60)
		u.Out().Printf("  [%s] %s: %s", ts, item.SenderName, text)
	}

	if resp.HasMore && resp.NextCursor != "" {
		u.Out().Dim(fmt.Sprintf("\nMore messages available. Use --cursor=%q", resp.NextCursor))
	}

	return nil
}

// MessagesSearchCmd searches for messages.
type MessagesSearchCmd struct {
	Query              string   `arg:"" optional:"" help:"Search query (literal word match)"`
	AccountIDs         []string `help:"Filter by account IDs" name:"account-ids"`
	ChatIDs            []string `help:"Filter by chat IDs" name:"chat-id"`
	ChatType           string   `help:"Filter by chat type: single|group" name:"chat-type" enum:"single,group," default:""`
	Sender             string   `help:"Filter by sender: me|others|<user-id>" name:"sender"`
	MediaTypes         []string `help:"Filter by media types: any|image|video|link|file" name:"media-types"`
	DateAfter          string   `help:"Only include messages after time (RFC3339 or duration)" name:"date-after"`
	DateBefore         string   `help:"Only include messages before time (RFC3339 or duration)" name:"date-before"`
	IncludeMuted       *bool    `help:"Include muted chats (default true)" name:"include-muted"`
	ExcludeLowPriority *bool    `help:"Exclude low priority messages (default true)" name:"exclude-low-priority"`
	Cursor             string   `help:"Pagination cursor"`
	Direction          string   `help:"Pagination direction: before|after" enum:"before,after," default:""`
	Limit              int      `help:"Max results (1-20)" default:"20"`
	Fields             []string `help:"Comma-separated list of fields for --plain output" name:"fields" sep:","`
	FailIfEmpty        bool     `help:"Exit with code 1 if no results" name:"fail-if-empty"`
}

// MessagesTailCmd follows messages in a chat via polling.
type MessagesTailCmd struct {
	ChatID    string        `arg:"" name:"chatID" help:"Chat ID to follow"`
	Cursor    string        `help:"Start cursor (sortKey)"`
	Interval  time.Duration `help:"Polling interval" default:"2s"`
	StopAfter time.Duration `help:"Stop after duration (0=forever)" name:"stop-after" default:"0s"`
}

// Run executes the messages search command.
func (c *MessagesSearchCmd) Run(ctx context.Context, flags *RootFlags) error {
	u := ui.FromContext(ctx)

	if c.Limit < 1 || c.Limit > 20 {
		return errfmt.UsageError("invalid --limit %d (expected 1-20)", c.Limit)
	}
	allowedMedia := map[string]struct{}{
		"any":   {},
		"image": {},
		"video": {},
		"link":  {},
		"file":  {},
	}
	for _, media := range c.MediaTypes {
		if _, ok := allowedMedia[media]; !ok {
			return errfmt.UsageError("invalid --media-types %q (expected any|image|video|link|file)", media)
		}
	}

	var dateAfter *time.Time
	if c.DateAfter != "" {
		t, err := parseTime(c.DateAfter)
		if err != nil {
			return errfmt.UsageError("invalid --date-after %q (expected RFC3339 or duration)", c.DateAfter)
		}
		dateAfter = &t
	}

	var dateBefore *time.Time
	if c.DateBefore != "" {
		t, err := parseTime(c.DateBefore)
		if err != nil {
			return errfmt.UsageError("invalid --date-before %q (expected RFC3339 or duration)", c.DateBefore)
		}
		dateBefore = &t
	}

	token, _, err := config.GetToken()
	if err != nil {
		return err
	}

	timeout := time.Duration(flags.Timeout) * time.Second
	client, err := beeperapi.NewClient(token, flags.BaseURL, timeout)
	if err != nil {
		return err
	}

	resp, err := client.Messages().Search(ctx, beeperapi.MessageSearchParams{
		Query:              c.Query,
		AccountIDs:         c.AccountIDs,
		ChatIDs:            normalizeChatIDs(c.ChatIDs),
		ChatType:           c.ChatType,
		Sender:             c.Sender,
		MediaTypes:         c.MediaTypes,
		DateAfter:          dateAfter,
		DateBefore:         dateBefore,
		IncludeMuted:       c.IncludeMuted,
		ExcludeLowPriority: c.ExcludeLowPriority,
		Cursor:             c.Cursor,
		Direction:          c.Direction,
		Limit:              c.Limit,
	})
	if err != nil {
		return err
	}

	if err := failIfEmpty(c.FailIfEmpty, len(resp.Items), "messages"); err != nil {
		return err
	}

	// JSON output
	if outfmt.IsJSON(ctx) {
		return outfmt.WriteJSON(os.Stdout, resp)
	}

	// Plain output (TSV)
	if outfmt.IsPlain(ctx) {
		fields, err := resolveFields(c.Fields, []string{"id", "chat_id", "sender_name", "text", "timestamp", "sort_key"})
		if err != nil {
			return err
		}
		for _, item := range resp.Items {
			writePlainFields(u, fields, map[string]string{
				"id":          item.ID,
				"chat_id":     item.ChatID,
				"sender_name": item.SenderName,
				"timestamp":   item.Timestamp,
				"text":        ui.Truncate(item.Text, 50),
				"sort_key":    item.SortKey,
			})
		}
		return nil
	}

	// Human-readable output
	if len(resp.Items) == 0 {
		u.Out().Warn("No messages found")
		u.Out().Dim("Note: Search uses literal word match, not semantic search.")
		return nil
	}

	w := tabwriter.NewWriter(os.Stdout, 0, 0, 2, ' ', 0)
	u.Out().Printf("Found %d messages:\n", len(resp.Items))
	for _, item := range resp.Items {
		ts := ""
		if item.Timestamp != "" {
			if t, err := time.Parse(time.RFC3339, item.Timestamp); err == nil {
				ts = t.Format("Jan 2")
			}
		}
		text := ui.Truncate(item.Text, 50)
		if _, err := fmt.Fprintf(w, "  [%s]\t%s:\t%s\n", ts, item.SenderName, text); err != nil {
			return err
		}
	}
	if err := w.Flush(); err != nil {
		return err
	}

	if resp.HasMore && resp.OldestCursor != "" {
		u.Out().Dim(fmt.Sprintf("\nMore results available. Use --cursor=%q --direction=before", resp.OldestCursor))
	}

	return nil
}

// Run executes the messages tail command.
func (c *MessagesTailCmd) Run(ctx context.Context, flags *RootFlags) error {
	u := ui.FromContext(ctx)
	chatID := normalizeChatID(c.ChatID)

	if c.Interval <= 0 {
		return errfmt.UsageError("invalid --interval %s (must be > 0)", c.Interval)
	}

	token, _, err := config.GetToken()
	if err != nil {
		return err
	}

	timeout := time.Duration(flags.Timeout) * time.Second
	client, err := beeperapi.NewClient(token, flags.BaseURL, timeout)
	if err != nil {
		return err
	}

	cursor := c.Cursor
	if cursor == "" {
		seed, err := client.Messages().List(ctx, chatID, beeperapi.MessageListParams{
			Direction: "before",
		})
		if err != nil {
			return err
		}
		cursor = firstSortKey(seed.Items)
	}

	deadline := time.Time{}
	if c.StopAfter > 0 {
		deadline = time.Now().Add(c.StopAfter)
	}

	ticker := time.NewTicker(c.Interval)
	defer ticker.Stop()

	encoder := json.NewEncoder(os.Stdout)
	encoder.SetEscapeHTML(false)

	for {
		if !deadline.IsZero() && time.Now().After(deadline) {
			return nil
		}

		resp, err := client.Messages().List(ctx, chatID, beeperapi.MessageListParams{
			Cursor:    cursor,
			Direction: "after",
		})
		if err != nil {
			return err
		}

		if len(resp.Items) > 0 {
			for _, item := range resp.Items {
				switch {
				case outfmt.IsJSON(ctx):
					if err := encoder.Encode(item); err != nil {
						return fmt.Errorf("encode json: %w", err)
					}
				case outfmt.IsPlain(ctx):
					u.Out().Printf("%s\t%s\t%s\t%s", item.ID, item.SenderName, item.Timestamp, ui.Truncate(item.Text, 50))
				default:
					ts := ""
					if item.Timestamp != "" {
						if t, err := time.Parse(time.RFC3339, item.Timestamp); err == nil {
							ts = t.Format("Jan 2 15:04")
						}
					}
					text := ui.Truncate(item.Text, 60)
					u.Out().Printf("[%s] %s: %s", ts, item.SenderName, text)
				}
			}

			if next := lastSortKey(resp.Items); next != "" {
				cursor = next
			}
		}

		<-ticker.C
	}
}

// MessagesSendCmd sends a message to a chat.
type MessagesSendCmd struct {
	ChatID           string `arg:"" name:"chatID" help:"Chat ID to send message to"`
	Text             string `arg:"" optional:"" help:"Message text to send"`
	ReplyToMessageID string `help:"Message ID to reply to" name:"reply-to"`
	TextFile         string `help:"Read message text from file ('-' for stdin)" name:"text-file"`
	Stdin            bool   `help:"Read message text from stdin" name:"stdin"`
}

// Run executes the messages send command.
func (c *MessagesSendCmd) Run(ctx context.Context, flags *RootFlags) error {
	u := ui.FromContext(ctx)
	chatID := normalizeChatID(c.ChatID)

	text, err := resolveTextInput(c.Text, c.TextFile, c.Stdin, true, "message text", "--text-file", "--stdin")
	if err != nil {
		return err
	}

	token, _, err := config.GetToken()
	if err != nil {
		return err
	}

	timeout := time.Duration(flags.Timeout) * time.Second
	client, err := beeperapi.NewClient(token, flags.BaseURL, timeout)
	if err != nil {
		return err
	}

	resp, err := client.Messages().Send(ctx, chatID, beeperapi.SendParams{
		Text:             text,
		ReplyToMessageID: c.ReplyToMessageID,
	})
	if err != nil {
		return err
	}

	// JSON output
	if outfmt.IsJSON(ctx) {
		return outfmt.WriteJSON(os.Stdout, resp)
	}

	// Plain output
	if outfmt.IsPlain(ctx) {
		u.Out().Printf("%s\t%s", resp.ChatID, resp.PendingMessageID)
		return nil
	}

	// Human-readable output
	u.Out().Success("Message sent")
	u.Out().Printf("Chat ID:    %s", resp.ChatID)
	u.Out().Printf("Pending ID: %s", resp.PendingMessageID)

	return nil
}

func firstSortKey(items []beeperapi.MessageItem) string {
	for _, item := range items {
		if item.SortKey != "" {
			return item.SortKey
		}
	}
	return ""
}

func lastSortKey(items []beeperapi.MessageItem) string {
	for i := len(items) - 1; i >= 0; i-- {
		if items[i].SortKey != "" {
			return items[i].SortKey
		}
	}
	return ""
}
