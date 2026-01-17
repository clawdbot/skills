package cmd

import (
	"fmt"
	"strings"

	"github.com/johntheyoung/roadrunner/internal/errfmt"
	"github.com/johntheyoung/roadrunner/internal/ui"
)

func resolveFields(fields []string, allowed []string) ([]string, error) {
	if len(fields) == 0 {
		out := make([]string, len(allowed))
		copy(out, allowed)
		return out, nil
	}

	allowedSet := make(map[string]struct{}, len(allowed))
	for _, f := range allowed {
		allowedSet[f] = struct{}{}
	}

	out := make([]string, 0, len(fields))
	for _, raw := range fields {
		f := strings.TrimSpace(raw)
		if f == "" {
			continue
		}
		if _, ok := allowedSet[f]; !ok {
			return nil, errfmt.UsageError("invalid --fields %q (allowed: %s)", f, strings.Join(allowed, ", "))
		}
		out = append(out, f)
	}

	if len(out) == 0 {
		return nil, errfmt.UsageError("invalid --fields (no fields provided)")
	}

	return out, nil
}

func writePlainFields(u *ui.UI, fields []string, values map[string]string) {
	row := make([]string, len(fields))
	for i, f := range fields {
		row[i] = values[f]
	}
	u.Out().Println(strings.Join(row, "\t"))
}

func formatBool(value bool) string {
	return fmt.Sprintf("%t", value)
}
