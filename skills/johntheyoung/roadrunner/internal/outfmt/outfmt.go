package outfmt

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
)

// Mode represents the output mode.
type Mode struct {
	JSON  bool
	Plain bool
}

// ParseError is returned for invalid flag combinations.
type ParseError struct {
	Msg string
}

func (e *ParseError) Error() string { return e.Msg }

// FromFlags creates a Mode from flag values.
// Returns error if both JSON and Plain are set.
func FromFlags(jsonOut bool, plainOut bool) (Mode, error) {
	if jsonOut && plainOut {
		return Mode{}, &ParseError{Msg: "cannot use both --json and --plain"}
	}

	return Mode{JSON: jsonOut, Plain: plainOut}, nil
}

type ctxKey struct{}

// WithMode attaches the output mode to a context.
func WithMode(ctx context.Context, mode Mode) context.Context {
	return context.WithValue(ctx, ctxKey{}, mode)
}

// FromContext retrieves the output mode from context.
func FromContext(ctx context.Context) Mode {
	if v := ctx.Value(ctxKey{}); v != nil {
		if m, ok := v.(Mode); ok {
			return m
		}
	}

	return Mode{}
}

// IsJSON returns true if JSON output mode is enabled.
func IsJSON(ctx context.Context) bool {
	return FromContext(ctx).JSON
}

// IsPlain returns true if plain output mode is enabled.
func IsPlain(ctx context.Context) bool {
	return FromContext(ctx).Plain
}

// IsHuman returns true if human-readable output (default) is enabled.
func IsHuman(ctx context.Context) bool {
	m := FromContext(ctx)
	return !m.JSON && !m.Plain
}

// WriteJSON writes v as indented JSON to w.
func WriteJSON(w io.Writer, v any) error {
	enc := json.NewEncoder(w)
	enc.SetEscapeHTML(false)
	enc.SetIndent("", "  ")

	if err := enc.Encode(v); err != nil {
		return fmt.Errorf("encode json: %w", err)
	}

	return nil
}
