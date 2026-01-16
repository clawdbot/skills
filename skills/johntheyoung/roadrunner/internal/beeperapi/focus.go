package beeperapi

import (
	"context"

	beeperdesktopapi "github.com/beeper/desktop-api-go"
)

// FocusParams configures focus requests.
type FocusParams struct {
	ChatID              string
	MessageID           string
	DraftText           string
	DraftAttachmentPath string
}

// FocusResult is the response from focusing the app.
type FocusResult struct {
	Success bool `json:"success"`
}

// Focus brings Beeper Desktop to the foreground, optionally navigating to a chat.
func (c *Client) Focus(ctx context.Context, params FocusParams) (FocusResult, error) {
	ctx, cancel := c.contextWithTimeout(ctx)
	defer cancel()

	sdkParams := beeperdesktopapi.FocusParams{}
	if params.ChatID != "" {
		sdkParams.ChatID = beeperdesktopapi.String(params.ChatID)
	}
	if params.MessageID != "" {
		sdkParams.MessageID = beeperdesktopapi.String(params.MessageID)
	}
	if params.DraftText != "" {
		sdkParams.DraftText = beeperdesktopapi.String(params.DraftText)
	}
	if params.DraftAttachmentPath != "" {
		sdkParams.DraftAttachmentPath = beeperdesktopapi.String(params.DraftAttachmentPath)
	}

	resp, err := c.SDK.Focus(ctx, sdkParams)
	if err != nil {
		return FocusResult{}, err
	}

	return FocusResult{
		Success: resp.Success,
	}, nil
}
