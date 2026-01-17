package beeperapi

import (
	"context"
	"time"

	beeperdesktopapi "github.com/beeper/desktop-api-go"
)

// RemindersService handles reminder operations.
type RemindersService struct {
	client *Client
}

// SetParams configures reminder set requests.
type SetParams struct {
	RemindAt                 time.Time
	DismissOnIncomingMessage bool
}

// Reminders returns the reminders service.
func (c *Client) Reminders() *RemindersService {
	return &RemindersService{client: c}
}

// Set creates a reminder for a chat.
func (s *RemindersService) Set(ctx context.Context, chatID string, params SetParams) error {
	ctx, cancel := s.client.contextWithTimeout(ctx)
	defer cancel()

	sdkParams := beeperdesktopapi.ChatReminderNewParams{
		Reminder: beeperdesktopapi.ChatReminderNewParamsReminder{
			RemindAtMs: float64(params.RemindAt.UnixMilli()),
		},
	}
	if params.DismissOnIncomingMessage {
		sdkParams.Reminder.DismissOnIncomingMessage = beeperdesktopapi.Bool(true)
	}

	return s.client.SDK.Chats.Reminders.New(ctx, chatID, sdkParams)
}

// Clear removes a reminder from a chat.
func (s *RemindersService) Clear(ctx context.Context, chatID string) error {
	ctx, cancel := s.client.contextWithTimeout(ctx)
	defer cancel()

	return s.client.SDK.Chats.Reminders.Delete(ctx, chatID)
}
