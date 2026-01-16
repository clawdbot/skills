package cmd

import (
	"context"
	"os"
	"text/tabwriter"
	"time"

	"github.com/johntheyoung/roadrunner/internal/beeperapi"
	"github.com/johntheyoung/roadrunner/internal/config"
	"github.com/johntheyoung/roadrunner/internal/outfmt"
	"github.com/johntheyoung/roadrunner/internal/ui"
)

// AccountsCmd is the parent command for account subcommands.
type AccountsCmd struct {
	List AccountsListCmd `cmd:"" help:"List connected messaging accounts"`
}

// AccountsListCmd lists all connected accounts.
type AccountsListCmd struct{}

// AccountsListResponse is the JSON output structure.
type AccountsListResponse struct {
	Accounts []beeperapi.Account `json:"accounts"`
}

// Run executes the accounts list command.
func (c *AccountsListCmd) Run(ctx context.Context, flags *RootFlags) error {
	u := ui.FromContext(ctx)

	// Get token
	token, _, err := config.GetToken()
	if err != nil {
		return err
	}

	// Create client
	timeout := time.Duration(flags.Timeout) * time.Second
	client, err := beeperapi.NewClient(token, flags.BaseURL, timeout)
	if err != nil {
		return err
	}

	// Fetch accounts
	accounts, err := client.Accounts().List(ctx)
	if err != nil {
		return err
	}

	// JSON output
	if outfmt.IsJSON(ctx) {
		return outfmt.WriteJSON(os.Stdout, AccountsListResponse{
			Accounts: accounts,
		})
	}

	// Plain output (TSV)
	if outfmt.IsPlain(ctx) {
		for _, a := range accounts {
			u.Out().Printf("%s\t%s\t%s", a.ID, a.Network, a.DisplayName)
		}
		return nil
	}

	// Human-readable output
	if len(accounts) == 0 {
		u.Out().Warn("No accounts connected")
		return nil
	}

	w := tabwriter.NewWriter(os.Stdout, 0, 0, 2, ' ', 0)
	u.Out().Printf("Connected accounts (%d):\n", len(accounts))
	for _, a := range accounts {
		_, _ = w.Write([]byte("  " + a.Network + "\t" + a.DisplayName + "\t" + a.ID + "\n"))
	}
	w.Flush()

	return nil
}
