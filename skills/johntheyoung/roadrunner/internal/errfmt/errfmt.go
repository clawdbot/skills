package errfmt

import (
	"errors"
	"fmt"
	"strings"

	"github.com/alecthomas/kong"

	"github.com/johntheyoung/roadrunner/internal/beeperapi"
	"github.com/johntheyoung/roadrunner/internal/config"
	"github.com/johntheyoung/roadrunner/internal/outfmt"
	"github.com/johntheyoung/roadrunner/internal/ui"
)

// Format converts an error to a user-friendly message.
func Format(err error) string {
	if err == nil {
		return ""
	}

	// Handle Kong parse errors
	var parseErr *kong.ParseError
	if errors.As(err, &parseErr) {
		return formatParseError(parseErr)
	}

	// Handle outfmt parse errors (--json/--plain conflict)
	var outfmtErr *outfmt.ParseError
	if errors.As(err, &outfmtErr) {
		return outfmtErr.Msg + "\nRun with --help to see usage"
	}

	// Handle UI parse errors (--color)
	var uiErr *ui.ParseError
	if errors.As(err, &uiErr) {
		return uiErr.Msg + "\nRun with --help to see usage"
	}

	// Handle no token error
	if errors.Is(err, config.ErrNoToken) {
		return "No API token configured.\n\nSet your token:\n  rr auth set <token>\n\nOr use environment variable:\n  export BEEPER_TOKEN=<token>"
	}

	// Handle API errors
	if beeperapi.IsAPIError(err) {
		return beeperapi.FormatError(err)
	}

	return err.Error()
}

// formatParseError enhances Kong parse errors with helpful hints.
func formatParseError(err *kong.ParseError) string {
	msg := err.Error()

	// If Kong already provided a suggestion, use it as-is
	if strings.Contains(msg, "did you mean") {
		return msg
	}

	// For unknown flag errors without suggestions, add a help hint
	if strings.HasPrefix(msg, "unknown flag") {
		return msg + "\nRun with --help to see available flags"
	}

	// For missing required flags
	if strings.Contains(msg, "missing") || strings.Contains(msg, "required") {
		return msg + "\nRun with --help to see usage"
	}

	return msg
}

// ExitError wraps an error with an exit code.
type ExitError struct {
	Err  error
	Code int
}

func (e *ExitError) Error() string {
	if e.Err == nil {
		return ""
	}
	return e.Err.Error()
}

func (e *ExitError) Unwrap() error {
	return e.Err
}

// Exit codes
const (
	ExitSuccess    = 0
	ExitFailure    = 1
	ExitUsageError = 2
)

// WithCode wraps an error with an exit code.
func WithCode(err error, code int) *ExitError {
	return &ExitError{Err: err, Code: code}
}

// UsageError creates an error with exit code 2.
func UsageError(format string, args ...any) *ExitError {
	return &ExitError{
		Err:  fmt.Errorf(format, args...),
		Code: ExitUsageError,
	}
}
