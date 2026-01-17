package cmd

import (
	"context"
	"fmt"
	"io"
	"net/url"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/johntheyoung/roadrunner/internal/beeperapi"
	"github.com/johntheyoung/roadrunner/internal/config"
	"github.com/johntheyoung/roadrunner/internal/errfmt"
	"github.com/johntheyoung/roadrunner/internal/outfmt"
	"github.com/johntheyoung/roadrunner/internal/ui"
)

// AssetsCmd is the parent command for asset subcommands.
type AssetsCmd struct {
	Download AssetsDownloadCmd `cmd:"" help:"Download an asset by mxc:// URL"`
}

// AssetsDownloadCmd downloads an asset from a Matrix URL.
type AssetsDownloadCmd struct {
	URL  string `arg:"" name:"url" help:"Matrix content URL (mxc:// or localmxc://)"`
	Dest string `help:"Destination file or directory (optional)" name:"dest"`
}

// Run executes the assets download command.
func (c *AssetsDownloadCmd) Run(ctx context.Context, flags *RootFlags) error {
	u := ui.FromContext(ctx)

	if c.URL == "" {
		return errfmt.UsageError("asset URL is required")
	}

	token, _, err := config.GetToken()
	if err != nil {
		return err
	}

	timeout := time.Duration(flags.Timeout) * time.Second
	client, err := beeperapi.NewClient(token, flags.BaseURL, timeout)
	if err != nil {
		return err
	}

	srcURL, err := client.Assets().Download(ctx, c.URL)
	if err != nil {
		return err
	}

	destPath := ""
	if c.Dest != "" {
		destPath, err = assetsDownloadDestination(srcURL, c.Dest)
		if err != nil {
			return errfmt.UsageError("invalid --dest: %s", err.Error())
		}
		if err := copyAsset(srcURL, destPath); err != nil {
			return err
		}
	}

	// JSON output
	if outfmt.IsJSON(ctx) {
		return outfmt.WriteJSON(os.Stdout, map[string]any{
			"src_url": srcURL,
			"dest":    destPath,
			"copied":  destPath != "",
		})
	}

	// Plain output
	if outfmt.IsPlain(ctx) {
		if destPath != "" {
			u.Out().Printf("%s", destPath)
		} else {
			u.Out().Printf("%s", srcURL)
		}
		return nil
	}

	// Human-readable output
	if destPath != "" {
		u.Out().Successf("Saved to %s", destPath)
	} else {
		u.Out().Successf("Downloaded to %s", srcURL)
	}

	return nil
}

func assetsDownloadDestination(srcURL string, dest string) (string, error) {
	path, err := assetLocalPath(srcURL)
	if err != nil {
		return "", err
	}
	base := filepath.Base(path)
	if base == "." || base == string(filepath.Separator) {
		return "", fmt.Errorf("invalid source filename")
	}
	info, err := os.Stat(dest)
	if err == nil && info.IsDir() {
		return filepath.Join(dest, base), nil
	}
	if err != nil && os.IsNotExist(err) {
		if strings.HasSuffix(dest, string(filepath.Separator)) {
			return filepath.Join(dest, base), nil
		}
	}
	return dest, nil
}

func assetLocalPath(srcURL string) (string, error) {
	if strings.HasPrefix(srcURL, "file://") {
		parsed, err := url.Parse(srcURL)
		if err != nil {
			return "", err
		}
		if parsed.Path == "" {
			return "", fmt.Errorf("empty file URL path")
		}
		path, err := url.PathUnescape(parsed.Path)
		if err != nil {
			return "", err
		}
		return filepath.FromSlash(path), nil
	}
	return srcURL, nil
}

func copyAsset(srcURL string, dest string) error {
	path, err := assetLocalPath(srcURL)
	if err != nil {
		return err
	}
	in, err := os.Open(path)
	if err != nil {
		return fmt.Errorf("open %s: %w", path, err)
	}
	defer func() {
		_ = in.Close()
	}()

	if err := os.MkdirAll(filepath.Dir(dest), 0755); err != nil {
		return fmt.Errorf("create dir: %w", err)
	}

	out, err := os.Create(dest)
	if err != nil {
		return fmt.Errorf("create %s: %w", dest, err)
	}
	defer func() {
		_ = out.Close()
	}()

	if _, err := io.Copy(out, in); err != nil {
		return fmt.Errorf("copy asset: %w", err)
	}

	return nil
}
