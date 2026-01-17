package cmd

import "testing"

func TestNormalizeChatID(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name string
		in   string
		want string
	}{
		{name: "empty", in: "", want: ""},
		{name: "no_escape", in: "!abc123:beeper.local", want: "!abc123:beeper.local"},
		{name: "single_escape", in: "\\!abc123:beeper.local", want: "!abc123:beeper.local"},
		{name: "double_escape", in: "\\\\!abc123:beeper.local", want: "!abc123:beeper.local"},
		{name: "other_prefix", in: "\\not-a-chat", want: "\\not-a-chat"},
	}

	for _, tt := range tests {
		tt := tt
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			if got := normalizeChatID(tt.in); got != tt.want {
				t.Fatalf("normalizeChatID(%q) = %q, want %q", tt.in, got, tt.want)
			}
		})
	}
}
