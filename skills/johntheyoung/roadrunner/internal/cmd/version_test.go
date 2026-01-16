package cmd

import "testing"

func TestVersionStringVariants(t *testing.T) {
	origVersion, origCommit, origDate := Version, Commit, Date
	t.Cleanup(func() {
		Version = origVersion
		Commit = origCommit
		Date = origDate
	})

	cases := []struct {
		name    string
		version string
		commit  string
		date    string
		want    string
	}{
		{name: "default", version: "", commit: "", date: "", want: "dev"},
		{name: "version-only", version: "1.2.3", commit: "", date: "", want: "1.2.3"},
		{name: "version-commit", version: "1.2.3", commit: "abc", date: "", want: "1.2.3 (abc)"},
		{name: "version-date", version: "1.2.3", commit: "", date: "2025-01-01", want: "1.2.3 (2025-01-01)"},
		{name: "version-commit-date", version: "1.2.3", commit: "abc", date: "2025-01-01", want: "1.2.3 (abc 2025-01-01)"},
		{name: "trimmed", version: " 1.2.3 ", commit: " abc ", date: " 2025-01-01 ", want: "1.2.3 (abc 2025-01-01)"},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			Version = tc.version
			Commit = tc.commit
			Date = tc.date
			if got := VersionString(); got != tc.want {
				t.Fatalf("VersionString() = %q, want %q", got, tc.want)
			}
		})
	}
}
