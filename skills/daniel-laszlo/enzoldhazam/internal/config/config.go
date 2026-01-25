package config

import (
	"os"

	"github.com/zalando/go-keyring"
)

const (
	serviceName = "enzoldhazam"
	userKey     = "username"
	passKey     = "password"
	serialKey   = "serial"
)

// Credentials holds the authentication data
type Credentials struct {
	Username string
	Password string
	Serial   string
}

// Save stores credentials in the macOS Keychain
func Save(creds Credentials) error {
	if err := keyring.Set(serviceName, userKey, creds.Username); err != nil {
		return err
	}
	if err := keyring.Set(serviceName, passKey, creds.Password); err != nil {
		return err
	}
	if creds.Serial != "" {
		if err := keyring.Set(serviceName, serialKey, creds.Serial); err != nil {
			return err
		}
	}
	return nil
}

// Load retrieves credentials from the macOS Keychain or environment variables
func Load() (*Credentials, error) {
	// First check environment variables
	envUser := os.Getenv("ENZOLDHAZAM_USER")
	envPass := os.Getenv("ENZOLDHAZAM_PASS")
	envSerial := os.Getenv("ENZOLDHAZAM_SERIAL")

	if envUser != "" && envPass != "" {
		return &Credentials{
			Username: envUser,
			Password: envPass,
			Serial:   envSerial,
		}, nil
	}

	// Fall back to keychain
	username, err := keyring.Get(serviceName, userKey)
	if err != nil {
		return nil, err
	}

	password, err := keyring.Get(serviceName, passKey)
	if err != nil {
		return nil, err
	}

	serial, _ := keyring.Get(serviceName, serialKey) // Serial is optional

	return &Credentials{
		Username: username,
		Password: password,
		Serial:   serial,
	}, nil
}

// Clear removes all stored credentials from the Keychain
func Clear() error {
	// Attempt to delete all keys, ignore errors for missing keys
	_ = keyring.Delete(serviceName, userKey)
	_ = keyring.Delete(serviceName, passKey)
	_ = keyring.Delete(serviceName, serialKey)
	return nil
}

// HasCredentials checks if credentials are available
func HasCredentials() bool {
	// Check environment first
	if os.Getenv("ENZOLDHAZAM_USER") != "" && os.Getenv("ENZOLDHAZAM_PASS") != "" {
		return true
	}

	// Check keychain
	_, err := keyring.Get(serviceName, userKey)
	return err == nil
}
