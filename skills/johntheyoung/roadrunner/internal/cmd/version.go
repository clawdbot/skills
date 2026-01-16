package cmd

import (
	"context"
	"fmt"
	"os"
	"strings"

	"github.com/johntheyoung/roadrunner/internal/outfmt"
	"github.com/johntheyoung/roadrunner/internal/ui"
)

// VersionCmd shows version information.
type VersionCmd struct{}

// VersionString returns a human-readable version string.
func VersionString() string {
	v := strings.TrimSpace(Version)
	if v == "" {
		v = "dev"
	}

	commit := strings.TrimSpace(Commit)
	date := strings.TrimSpace(Date)
	if commit == "" && date == "" {
		return v
	}
	if commit == "" {
		return fmt.Sprintf("%s (%s)", v, date)
	}
	if date == "" {
		return fmt.Sprintf("%s (%s)", v, commit)
	}
	return fmt.Sprintf("%s (%s %s)", v, commit, date)
}

// Run executes the version command.
func (c *VersionCmd) Run(ctx context.Context) error {
	u := ui.FromContext(ctx)

	if outfmt.IsJSON(ctx) {
		return outfmt.WriteJSON(os.Stdout, map[string]string{
			"version": strings.TrimSpace(Version),
			"commit":  strings.TrimSpace(Commit),
			"date":    strings.TrimSpace(Date),
		})
	}

	u.Out().Println(VersionString())
	return nil
}
