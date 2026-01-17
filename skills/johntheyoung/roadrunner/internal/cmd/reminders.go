package cmd

import (
	"context"
	"os"
	"strings"
	"time"

	"github.com/johntheyoung/roadrunner/internal/beeperapi"
	"github.com/johntheyoung/roadrunner/internal/config"
	"github.com/johntheyoung/roadrunner/internal/errfmt"
	"github.com/johntheyoung/roadrunner/internal/outfmt"
	"github.com/johntheyoung/roadrunner/internal/ui"
)

// RemindersCmd is the parent command for reminder subcommands.
type RemindersCmd struct {
	Set   RemindersSetCmd   `cmd:"" help:"Set a reminder for a chat"`
	Clear RemindersClearCmd `cmd:"" help:"Clear a reminder from a chat"`
}

// RemindersSetCmd sets a reminder for a chat.
type RemindersSetCmd struct {
	ChatID                   string `arg:"" name:"chatID" help:"Chat ID to set reminder for"`
	At                       string `arg:"" help:"When to remind (RFC3339 or relative like '1h', '30m', '2h30m')"`
	DismissOnIncomingMessage bool   `help:"Cancel reminder if someone messages" name:"dismiss-on-message"`
}

// Run executes the reminders set command.
func (c *RemindersSetCmd) Run(ctx context.Context, flags *RootFlags) error {
	u := ui.FromContext(ctx)
	chatID := normalizeChatID(c.ChatID)

	// Parse the time
	remindAt, err := parseTime(c.At)
	if err != nil {
		return errfmt.UsageError("invalid time %q: %v", c.At, err)
	}

	// Don't allow reminders in the past
	if remindAt.Before(time.Now()) {
		return errfmt.UsageError("reminder time must be in the future")
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

	if err := client.Reminders().Set(ctx, chatID, beeperapi.SetParams{
		RemindAt:                 remindAt,
		DismissOnIncomingMessage: c.DismissOnIncomingMessage,
	}); err != nil {
		return err
	}

	// JSON output
	if outfmt.IsJSON(ctx) {
		result := map[string]any{
			"chat_id":   chatID,
			"remind_at": remindAt.Format(time.RFC3339),
		}
		return outfmt.WriteJSON(os.Stdout, result)
	}

	// Plain output
	if outfmt.IsPlain(ctx) {
		u.Out().Printf("%s\t%s", chatID, remindAt.Format(time.RFC3339))
		return nil
	}

	// Human-readable output
	u.Out().Success("Reminder set")
	u.Out().Printf("Chat ID: %s", chatID)
	u.Out().Printf("Time:    %s", remindAt.Format("Jan 2 15:04"))

	return nil
}

// RemindersClearCmd clears a reminder from a chat.
type RemindersClearCmd struct {
	ChatID string `arg:"" name:"chatID" help:"Chat ID to clear reminder from"`
}

// Run executes the reminders clear command.
func (c *RemindersClearCmd) Run(ctx context.Context, flags *RootFlags) error {
	u := ui.FromContext(ctx)
	chatID := normalizeChatID(c.ChatID)

	if err := confirmDestructive(flags, "clear reminder for "+chatID); err != nil {
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

	if err := client.Reminders().Clear(ctx, chatID); err != nil {
		return err
	}

	// JSON output
	if outfmt.IsJSON(ctx) {
		result := map[string]any{
			"chat_id": chatID,
			"cleared": true,
		}
		return outfmt.WriteJSON(os.Stdout, result)
	}

	// Plain output
	if outfmt.IsPlain(ctx) {
		u.Out().Printf("%s\tcleared", chatID)
		return nil
	}

	// Human-readable output
	u.Out().Success("Reminder cleared")

	return nil
}

// parseTime parses a time string as either RFC3339 or a duration from now.
func parseTime(s string) (time.Time, error) {
	s = strings.TrimSpace(s)

	// Try RFC3339 first
	if t, err := time.Parse(time.RFC3339, s); err == nil {
		return t, nil
	}
	if t, err := time.Parse(time.RFC3339Nano, s); err == nil {
		return t, nil
	}

	// Try RFC3339 without timezone (interpret as local time)
	loc := time.Local
	if t, err := time.ParseInLocation("2006-01-02T15:04:05.999999999", s, loc); err == nil {
		return t, nil
	}
	if t, err := time.ParseInLocation("2006-01-02T15:04:05", s, loc); err == nil {
		return t, nil
	}
	if t, err := time.ParseInLocation("2006-01-02T15:04", s, loc); err == nil {
		return t, nil
	}

	// Try date only (local midnight)
	if t, err := time.ParseInLocation("2006-01-02", s, loc); err == nil {
		return t, nil
	}

	// Try as a duration from now
	d, err := time.ParseDuration(s)
	if err != nil {
		return time.Time{}, err
	}

	return time.Now().Add(d), nil
}
