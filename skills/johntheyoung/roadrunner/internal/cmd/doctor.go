package cmd

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"time"

	"github.com/johntheyoung/roadrunner/internal/config"
	"github.com/johntheyoung/roadrunner/internal/errfmt"
	"github.com/johntheyoung/roadrunner/internal/outfmt"
	"github.com/johntheyoung/roadrunner/internal/ui"
)

// DoctorCmd validates configuration and connectivity.
type DoctorCmd struct{}

// DoctorResult holds the results of all checks.
type DoctorResult struct {
	ConfigPath   string   `json:"config_path"`
	ConfigExists bool     `json:"config_exists"`
	TokenSource  string   `json:"token_source"`
	HasToken     bool     `json:"has_token"`
	APIReachable bool     `json:"api_reachable"`
	APIURL       string   `json:"api_url"`
	TokenValid   bool     `json:"token_valid"`
	AccountID    string   `json:"account_id,omitempty"`
	AllPassed    bool     `json:"all_passed"`
	Errors       []string `json:"errors,omitempty"`
}

// Run executes the doctor command.
func (c *DoctorCmd) Run(ctx context.Context, flags *RootFlags) error {
	u := ui.FromContext(ctx)

	result := DoctorResult{
		APIURL: flags.BaseURL,
		Errors: []string{},
	}

	// Check 1: Config path
	configPath, err := config.FilePath()
	if err != nil {
		result.Errors = append(result.Errors, fmt.Sprintf("config path: %v", err))
	} else {
		result.ConfigPath = configPath
		if _, err := os.Stat(configPath); err == nil {
			result.ConfigExists = true
		}
	}

	// Check 2: Token source
	token, source, err := config.GetToken()
	if err == nil && token != "" {
		result.HasToken = true
		result.TokenSource = source.String()
	} else {
		result.TokenSource = "none"
		result.Errors = append(result.Errors, "no token configured")
	}

	// Check 3: API reachable (read-only health check)
	apiErr := checkAPIReachable(flags.BaseURL, flags.Timeout)
	if apiErr == nil {
		result.APIReachable = true
	} else {
		result.Errors = append(result.Errors, fmt.Sprintf("api: %v", apiErr))
	}

	// Check 4: Token valid (only if we have a token and API is reachable)
	if result.HasToken && result.APIReachable {
		validation := ValidateToken(ctx, token, flags.BaseURL, flags.Timeout)
		result.TokenValid = validation.Valid
		result.AccountID = validation.Account
		if !validation.Valid {
			result.Errors = append(result.Errors, fmt.Sprintf("auth: %s", validation.Error))
		}
	}

	// Determine overall pass/fail
	result.AllPassed = result.ConfigPath != "" && result.HasToken && result.APIReachable && result.TokenValid

	// Output
	if outfmt.IsJSON(ctx) {
		return outfmt.WriteJSON(os.Stdout, result)
	}

	// Human-readable output
	printCheck(u, "Config", result.ConfigPath, result.ConfigExists, "found", "not found")
	printCheck(u, "Token", result.TokenSource, result.HasToken, "", "missing")
	printCheck(u, "API", result.APIURL, result.APIReachable, "reachable", "unreachable")

	// Auth check (only show if we attempted it)
	if result.HasToken && result.APIReachable {
		authValue := "valid"
		if result.AccountID != "" {
			authValue = "valid (account: " + result.AccountID + ")"
		}
		printCheck(u, "Auth", authValue, result.TokenValid, "", "invalid")
	}

	u.Out().Println("")

	if result.AllPassed {
		u.Out().Success("All checks passed.")
		return nil
	}

	u.Out().Error("Some checks failed.")
	for _, e := range result.Errors {
		u.Out().Dim("  - " + e)
	}

	return errfmt.WithCode(fmt.Errorf("doctor checks failed"), errfmt.ExitFailure)
}

func printCheck(u *ui.UI, name, value string, ok bool, okSuffix, failSuffix string) {
	status := "✓"
	suffix := okSuffix
	if !ok {
		status = "✗"
		suffix = failSuffix
	}

	line := fmt.Sprintf("%s %-8s %s", status, name+":", value)
	if suffix != "" {
		line += " (" + suffix + ")"
	}

	if ok {
		u.Out().Success(line)
	} else {
		u.Out().Error(line)
	}
}

func checkAPIReachable(baseURL string, timeoutSec int) error {
	timeout := time.Duration(timeoutSec) * time.Second

	client := &http.Client{Timeout: timeout}

	// Try a simple GET to the base URL or a health endpoint
	// Using /v1/accounts as a read-only endpoint
	resp, err := client.Get(baseURL + "/v1/accounts")
	if err != nil {
		return fmt.Errorf("cannot connect to %s: %w", baseURL, err)
	}
	defer func() {
		_ = resp.Body.Close()
	}()

	// Any response (even 401) means API is reachable
	// We're just checking connectivity, not auth
	if resp.StatusCode >= 500 {
		return fmt.Errorf("server error: %d", resp.StatusCode)
	}

	return nil
}
