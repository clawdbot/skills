package cmd

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestResolveTextInput(t *testing.T) {
	t.Run("text_arg", func(t *testing.T) {
		got, err := resolveTextInput("hello", "", false, true, "message text", "--text-file", "--stdin")
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		if got != "hello" {
			t.Fatalf("got %q, want %q", got, "hello")
		}
	})

	t.Run("file_path", func(t *testing.T) {
		dir := t.TempDir()
		path := filepath.Join(dir, "msg.txt")
		if err := os.WriteFile(path, []byte("from file"), 0600); err != nil {
			t.Fatalf("write file: %v", err)
		}
		got, err := resolveTextInput("", path, false, true, "message text", "--text-file", "--stdin")
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		if got != "from file" {
			t.Fatalf("got %q, want %q", got, "from file")
		}
	})

	t.Run("stdin", func(t *testing.T) {
		withStdin(t, "from stdin", func() {
			got, err := resolveTextInput("", "", true, true, "message text", "--text-file", "--stdin")
			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}
			if got != "from stdin" {
				t.Fatalf("got %q, want %q", got, "from stdin")
			}
		})
	})

	t.Run("stdin_dash", func(t *testing.T) {
		withStdin(t, "dash stdin", func() {
			got, err := resolveTextInput("", "-", false, true, "message text", "--text-file", "--stdin")
			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}
			if got != "dash stdin" {
				t.Fatalf("got %q, want %q", got, "dash stdin")
			}
		})
	})

	t.Run("multiple_sources", func(t *testing.T) {
		_, err := resolveTextInput("hello", "file.txt", false, true, "message text", "--text-file", "--stdin")
		if err == nil {
			t.Fatal("expected error, got nil")
		}
		if !strings.Contains(err.Error(), "use only one") {
			t.Fatalf("unexpected error: %v", err)
		}
	})
}
