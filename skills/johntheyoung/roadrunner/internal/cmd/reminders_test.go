package cmd

import (
	"errors"
	"testing"
	"time"

	"github.com/johntheyoung/roadrunner/internal/errfmt"
)

func TestParseTimeVariants(t *testing.T) {
	cases := []struct {
		name string
		in   string
		want time.Time
	}{
		{
			name: "rfc3339",
			in:   "2025-01-02T15:04:05Z",
			want: time.Date(2025, 1, 2, 15, 4, 5, 0, time.UTC),
		},
		{
			name: "local-no-tz",
			in:   "2025-01-02T15:04",
			want: time.Date(2025, 1, 2, 15, 4, 0, 0, time.Local),
		},
		{
			name: "date-only",
			in:   "2025-01-02",
			want: time.Date(2025, 1, 2, 0, 0, 0, 0, time.Local),
		},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			got, err := parseTime(tc.in)
			if err != nil {
				t.Fatalf("parseTime(%q) error: %v", tc.in, err)
			}
			if !got.Equal(tc.want) {
				t.Fatalf("parseTime(%q) = %v, want %v", tc.in, got, tc.want)
			}
		})
	}
}

func TestParseTimeDuration(t *testing.T) {
	start := time.Now()
	got, err := parseTime("1h")
	if err != nil {
		t.Fatalf("parseTime(duration) error: %v", err)
	}
	diff := got.Sub(start)
	if diff < 59*time.Minute || diff > 61*time.Minute {
		t.Fatalf("parseTime(duration) delta = %v, want ~1h", diff)
	}
}

func TestParseTimeInvalid(t *testing.T) {
	if _, err := parseTime("not-a-time"); err == nil {
		t.Fatal("parseTime(invalid) expected error")
	}
}

func TestConfirmDestructiveNonInteractive(t *testing.T) {
	err := confirmDestructive(&RootFlags{NoInput: true}, "archive chat")
	if err == nil {
		t.Fatal("confirmDestructive expected error")
	}
	var exitErr *errfmt.ExitError
	if !errors.As(err, &exitErr) {
		t.Fatalf("confirmDestructive error = %T, want *errfmt.ExitError", err)
	}
	if exitErr.Code != errfmt.ExitUsageError {
		t.Fatalf("confirmDestructive code = %d, want %d", exitErr.Code, errfmt.ExitUsageError)
	}
}

func TestConfirmDestructiveForce(t *testing.T) {
	if err := confirmDestructive(&RootFlags{Force: true}, "archive chat"); err != nil {
		t.Fatalf("confirmDestructive(force) error: %v", err)
	}
}
