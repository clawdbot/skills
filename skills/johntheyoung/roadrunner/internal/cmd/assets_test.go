package cmd

import (
	"os"
	"path/filepath"
	"testing"
)

func TestAssetsDownloadDestination(t *testing.T) {
	temp := t.TempDir()
	dirPath := filepath.Join(temp, "outdir")
	if err := os.MkdirAll(dirPath, 0755); err != nil {
		t.Fatalf("mkdir: %v", err)
	}
	cases := []struct {
		name    string
		srcURL  string
		dest    string
		want    string
		wantErr bool
	}{
		{
			name:   "file-url-to-dir",
			srcURL: "file:///tmp/beeper/hello.png",
			dest:   dirPath,
			want:   filepath.Join(dirPath, "hello.png"),
		},
		{
			name:   "file-url-to-file",
			srcURL: "file:///tmp/beeper/hello.png",
			dest:   filepath.Join(temp, "out.png"),
			want:   filepath.Join(temp, "out.png"),
		},
		{
			name:   "path-to-dir",
			srcURL: "/tmp/beeper/hello.png",
			dest:   dirPath,
			want:   filepath.Join(dirPath, "hello.png"),
		},
		{
			name:   "path-to-file",
			srcURL: "/tmp/beeper/hello.png",
			dest:   filepath.Join(temp, "out.png"),
			want:   filepath.Join(temp, "out.png"),
		},
		{
			name:    "bad-url",
			srcURL:  "file://",
			dest:    temp,
			wantErr: true,
		},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			got, err := assetsDownloadDestination(tc.srcURL, tc.dest)
			if tc.wantErr {
				if err == nil {
					t.Fatal("expected error")
				}
				return
			}
			if err != nil {
				t.Fatalf("assetsDownloadDestination error: %v", err)
			}
			if got != tc.want {
				t.Fatalf("assetsDownloadDestination = %q, want %q", got, tc.want)
			}
		})
	}
}

func TestAssetLocalPath(t *testing.T) {
	got, err := assetLocalPath("file:///tmp/beeper/hello%20world.png")
	if err != nil {
		t.Fatalf("assetLocalPath error: %v", err)
	}
	want := filepath.FromSlash("/tmp/beeper/hello world.png")
	if got != want {
		t.Fatalf("assetLocalPath = %q, want %q", got, want)
	}
}
