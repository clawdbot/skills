package cmd

import (
	"context"
	"os"
	"time"

	"github.com/johntheyoung/roadrunner/internal/beeperapi"
	"github.com/johntheyoung/roadrunner/internal/config"
	"github.com/johntheyoung/roadrunner/internal/outfmt"
	"github.com/johntheyoung/roadrunner/internal/ui"
)

// FocusCmd focuses the Beeper Desktop app.
type FocusCmd struct {
	ChatID              string `help:"Chat ID to focus (optional)" name:"chat-id"`
	MessageID           string `help:"Message ID to jump to (optional)" name:"message-id"`
	DraftText           string `help:"Pre-fill draft text (optional)" name:"draft-text"`
	DraftTextFile       string `help:"Read draft text from file ('-' for stdin)" name:"draft-text-file"`
	DraftAttachmentPath string `help:"Pre-fill draft attachment path (optional)" name:"draft-attachment"`
}

// Run executes the focus command.
func (c *FocusCmd) Run(ctx context.Context, flags *RootFlags) error {
	u := ui.FromContext(ctx)
	chatID := normalizeChatID(c.ChatID)

	draftText, err := resolveTextInput(c.DraftText, c.DraftTextFile, false, false, "draft text", "--draft-text-file", "")
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

	resp, err := client.Focus(ctx, beeperapi.FocusParams{
		ChatID:              chatID,
		MessageID:           c.MessageID,
		DraftText:           draftText,
		DraftAttachmentPath: c.DraftAttachmentPath,
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
		u.Out().Printf("%t", resp.Success)
		return nil
	}

	// Human-readable output
	if resp.Success {
		if c.ChatID != "" {
			u.Out().Success("Focused Beeper Desktop on chat")
		} else {
			u.Out().Success("Focused Beeper Desktop")
		}
	} else {
		u.Out().Warn("Focus request sent but app may not have responded")
	}

	return nil
}
