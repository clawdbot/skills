package beeperapi

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"strings"

	beeperdesktopapi "github.com/beeper/desktop-api-go"
)

// findJSONBody extracts the JSON body from a full HTTP response dump.
// DumpResponse(true) returns headers followed by body, separated by \r\n\r\n.
func findJSONBody(resp []byte) []byte {
	// Look for the body separator
	sep := []byte("\r\n\r\n")
	idx := bytes.Index(resp, sep)
	if idx == -1 {
		// Try with just \n\n as fallback
		sep = []byte("\n\n")
		idx = bytes.Index(resp, sep)
	}
	if idx == -1 {
		// No separator found, try parsing the whole thing as JSON
		if len(resp) > 0 && resp[0] == '{' {
			return resp
		}
		return nil
	}
	body := resp[idx+len(sep):]
	if len(body) == 0 {
		return nil
	}
	return body
}

// FormatError converts SDK errors to user-friendly messages.
func FormatError(err error) string {
	if err == nil {
		return ""
	}

	var apiErr *beeperdesktopapi.Error
	if errors.As(err, &apiErr) {
		return formatAPIError(apiErr)
	}

	return err.Error()
}

// IsAPIError returns true if the error is an API error from the SDK.
func IsAPIError(err error) bool {
	var apiErr *beeperdesktopapi.Error
	return errors.As(err, &apiErr)
}

func formatAPIError(err *beeperdesktopapi.Error) string {
	// Try to extract message from response body
	// DumpResponse(true) includes the body, (false) only includes headers
	respBody := err.DumpResponse(true)

	// The response body is after the headers, separated by \r\n\r\n
	// Try to find and parse the JSON body
	if bodyStart := findJSONBody(respBody); bodyStart != nil {
		var body map[string]any
		if jsonErr := json.Unmarshal(bodyStart, &body); jsonErr == nil {
			if msg, ok := body["message"].(string); ok && msg != "" {
				return fmt.Sprintf("API error (%d): %s", err.StatusCode, msg)
			}
			if errMsg, ok := body["error"].(string); ok && errMsg != "" {
				return fmt.Sprintf("API error (%d): %s", err.StatusCode, errMsg)
			}
		}
	}

	// Fallback to raw JSON if available
	if raw := strings.TrimSpace(err.RawJSON()); raw != "" {
		var body map[string]any
		if jsonErr := json.Unmarshal([]byte(raw), &body); jsonErr == nil {
			if msg, ok := body["message"].(string); ok && msg != "" {
				return fmt.Sprintf("API error (%d): %s", err.StatusCode, msg)
			}
			if errMsg, ok := body["error"].(string); ok && errMsg != "" {
				return fmt.Sprintf("API error (%d): %s", err.StatusCode, errMsg)
			}
		}
	}

	// Fallback to status code
	switch err.StatusCode {
	case 401:
		return "API error (401): Unauthorized - check your token"
	case 403:
		return "API error (403): Forbidden - insufficient permissions"
	case 404:
		return "API error (404): Not found"
	case 429:
		return "API error (429): Rate limited - try again later"
	default:
		return fmt.Sprintf("API error (%d)", err.StatusCode)
	}
}

// IsNotFound returns true if the error is a 404.
func IsNotFound(err error) bool {
	var apiErr *beeperdesktopapi.Error
	if errors.As(err, &apiErr) {
		return apiErr.StatusCode == 404
	}
	return false
}

// IsUnauthorized returns true if the error is a 401.
func IsUnauthorized(err error) bool {
	var apiErr *beeperdesktopapi.Error
	if errors.As(err, &apiErr) {
		return apiErr.StatusCode == 401
	}
	return false
}
