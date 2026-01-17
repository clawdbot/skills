package config

import (
	"os"
	"path/filepath"
)

const appName = "beeper"

// Dir returns the configuration directory path.
// Uses XDG_CONFIG_HOME if set, otherwise ~/.config/beeper
func Dir() (string, error) {
	if xdg := os.Getenv("XDG_CONFIG_HOME"); xdg != "" {
		return filepath.Join(xdg, appName), nil
	}

	home, err := os.UserHomeDir()
	if err != nil {
		return "", err
	}

	return filepath.Join(home, ".config", appName), nil
}

// FilePath returns the full path to the config file.
func FilePath() (string, error) {
	dir, err := Dir()
	if err != nil {
		return "", err
	}

	return filepath.Join(dir, "config.json"), nil
}
