package beeperapi

import (
	"context"
	"fmt"

	beeperdesktopapi "github.com/beeper/desktop-api-go"
)

// AssetsService handles asset operations.
type AssetsService struct {
	client *Client
}

// Download retrieves a local file URL for an asset.
func (s *AssetsService) Download(ctx context.Context, url string) (string, error) {
	ctx, cancel := s.client.contextWithTimeout(ctx)
	defer cancel()

	resp, err := s.client.SDK.Assets.Download(ctx, beeperdesktopapi.AssetDownloadParams{
		URL: url,
	})
	if err != nil {
		return "", err
	}
	if resp.Error != "" {
		return "", fmt.Errorf("download failed: %s", resp.Error)
	}
	if resp.SrcURL == "" {
		return "", fmt.Errorf("empty src_url in response")
	}
	return resp.SrcURL, nil
}
