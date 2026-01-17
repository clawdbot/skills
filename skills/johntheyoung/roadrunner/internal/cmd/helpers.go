package cmd

import (
	"context"
	"time"

	"github.com/johntheyoung/roadrunner/internal/beeperapi"
)

// ValidateTokenResult holds the result of token validation.
type ValidateTokenResult struct {
	Valid   bool   `json:"valid"`
	Error   string `json:"error,omitempty"`
	Account string `json:"account,omitempty"` // First account ID if available
}

// ValidateToken checks if the token is valid by making a read-only API call.
// Returns account info if successful.
func ValidateToken(ctx context.Context, token, baseURL string, timeoutSec int) ValidateTokenResult {
	timeout := time.Duration(timeoutSec) * time.Second

	client, err := beeperapi.NewClient(token, baseURL, timeout)
	if err != nil {
		return ValidateTokenResult{
			Valid: false,
			Error: err.Error(),
		}
	}

	accounts, err := client.Accounts().List(ctx)
	if err != nil {
		// Check if it's an auth error
		if beeperapi.IsUnauthorized(err) {
			return ValidateTokenResult{
				Valid: false,
				Error: "unauthorized - token is invalid or expired",
			}
		}
		return ValidateTokenResult{
			Valid: false,
			Error: beeperapi.FormatError(err),
		}
	}

	result := ValidateTokenResult{Valid: true}
	if len(accounts) > 0 {
		result.Account = accounts[0].ID
	}

	return result
}
