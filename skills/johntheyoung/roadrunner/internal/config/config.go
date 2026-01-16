package config

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
)

// Config represents the stored configuration.
type Config struct {
	Token string `json:"token,omitempty"`
}

// ErrNoToken is returned when no token is configured.
var ErrNoToken = errors.New("no token configured")

// Load reads the config from disk.
// Returns empty config (not error) if file doesn't exist.
func Load() (*Config, error) {
	path, err := FilePath()
	if err != nil {
		return nil, fmt.Errorf("get config path: %w", err)
	}

	data, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			return &Config{}, nil
		}
		return nil, fmt.Errorf("read config: %w", err)
	}

	var cfg Config
	if err := json.Unmarshal(data, &cfg); err != nil {
		return nil, fmt.Errorf("parse config: %w", err)
	}

	return &cfg, nil
}

// Save writes the config to disk.
func Save(cfg *Config) error {
	path, err := FilePath()
	if err != nil {
		return fmt.Errorf("get config path: %w", err)
	}

	// Ensure directory exists
	dir := filepath.Dir(path)
	if err := os.MkdirAll(dir, 0700); err != nil {
		return fmt.Errorf("create config dir: %w", err)
	}

	data, err := json.MarshalIndent(cfg, "", "  ")
	if err != nil {
		return fmt.Errorf("marshal config: %w", err)
	}

	// Write with restrictive permissions (token is sensitive)
	if err := os.WriteFile(path, data, 0600); err != nil {
		return fmt.Errorf("write config: %w", err)
	}

	return nil
}

// TokenSource indicates where the token came from.
type TokenSource int

const (
	TokenSourceNone TokenSource = iota
	TokenSourceEnv
	TokenSourceEnvSDK // SDK fallback env var
	TokenSourceConfig
)

func (s TokenSource) String() string {
	switch s {
	case TokenSourceEnv:
		return "BEEPER_TOKEN env var"
	case TokenSourceEnvSDK:
		return "BEEPER_ACCESS_TOKEN env var (SDK fallback)"
	case TokenSourceConfig:
		return "config file"
	default:
		return "none"
	}
}

// GetToken returns the token and its source.
// Precedence: BEEPER_TOKEN > BEEPER_ACCESS_TOKEN > config file
func GetToken() (token string, source TokenSource, err error) {
	// Check CLI env var first
	if t := os.Getenv("BEEPER_TOKEN"); t != "" {
		return t, TokenSourceEnv, nil
	}

	// Check SDK fallback env var
	if t := os.Getenv("BEEPER_ACCESS_TOKEN"); t != "" {
		return t, TokenSourceEnvSDK, nil
	}

	// Load from config
	cfg, err := Load()
	if err != nil {
		return "", TokenSourceNone, err
	}

	if cfg.Token != "" {
		return cfg.Token, TokenSourceConfig, nil
	}

	return "", TokenSourceNone, ErrNoToken
}

// SetToken saves the token to config.
func SetToken(token string) error {
	cfg, err := Load()
	if err != nil {
		return err
	}

	cfg.Token = token
	return Save(cfg)
}

// ClearToken removes the token from config.
func ClearToken() error {
	cfg, err := Load()
	if err != nil {
		return err
	}

	cfg.Token = ""
	return Save(cfg)
}
