package cmd

import "testing"

func TestResolveFields(t *testing.T) {
	t.Parallel()

	allowed := []string{"id", "name", "status"}

	t.Run("default", func(t *testing.T) {
		t.Parallel()
		got, err := resolveFields(nil, allowed)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		if len(got) != len(allowed) {
			t.Fatalf("got %d fields, want %d", len(got), len(allowed))
		}
	})

	t.Run("custom_valid", func(t *testing.T) {
		t.Parallel()
		got, err := resolveFields([]string{"status", "id"}, allowed)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		if got[0] != "status" || got[1] != "id" {
			t.Fatalf("unexpected order: %v", got)
		}
	})

	t.Run("invalid_field", func(t *testing.T) {
		t.Parallel()
		if _, err := resolveFields([]string{"nope"}, allowed); err == nil {
			t.Fatal("expected error, got nil")
		}
	})
}
