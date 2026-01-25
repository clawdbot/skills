package api

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"net/http/cookiejar"
	"net/url"
	"regexp"
	"strconv"
	"strings"

	"enzoldhazam/internal/models"
)

const (
	baseURL   = "https://www.enzoldhazam.hu"
	axURL     = baseURL + "/Ax"
	userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15"
)

// Client handles API communication with enzoldhazam.hu
type Client struct {
	httpClient *http.Client
	loggedIn   bool
}

// NewClient creates a new API client with cookie jar
func NewClient() (*Client, error) {
	jar, err := cookiejar.New(nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create cookie jar: %w", err)
	}

	return &Client{
		httpClient: &http.Client{Jar: jar},
	}, nil
}

// doRequest performs an HTTP request with browser-like headers
func (c *Client) doRequest(method, urlStr string, body io.Reader) (*http.Response, error) {
	req, err := http.NewRequest(method, urlStr, body)
	if err != nil {
		return nil, err
	}
	req.Header.Set("User-Agent", userAgent)
	return c.httpClient.Do(req)
}

// Login authenticates with the NGBS system
func (c *Client) Login(username, password string) error {
	// Step 1: Get login page to extract CSRF token and establish session
	resp, err := c.doRequest("GET", baseURL+"/", nil)
	if err != nil {
		return fmt.Errorf("failed to get login page: %w", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("failed to read login page: %w", err)
	}

	// Extract CSRF token from hidden input
	tokenRegex := regexp.MustCompile(`name="token"\s+value="([^"]+)"`)
	matches := tokenRegex.FindSubmatch(body)
	if len(matches) < 2 {
		return fmt.Errorf("failed to find CSRF token")
	}
	token := string(matches[1])

	// Step 2: POST login credentials with required headers
	data := url.Values{}
	data.Set("username", username)
	data.Set("password", password)
	data.Set("token", token)
	data.Set("x-email", "")

	req, err := http.NewRequest("POST", baseURL+"/", strings.NewReader(data.Encode()))
	if err != nil {
		return fmt.Errorf("failed to create login request: %w", err)
	}
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	req.Header.Set("User-Agent", userAgent)
	req.Header.Set("Origin", baseURL)
	req.Header.Set("Referer", baseURL+"/")

	loginResp, err := c.httpClient.Do(req)
	if err != nil {
		return fmt.Errorf("login request failed: %w", err)
	}
	defer loginResp.Body.Close()

	// Consume response body
	io.Copy(io.Discard, loginResp.Body)

	// Step 3: Verify login by trying to get device list
	testResp, err := c.doRequest("GET", axURL+"?action=iconList", nil)
	if err != nil {
		return fmt.Errorf("login verification failed: %w", err)
	}
	defer testResp.Body.Close()

	testBody, _ := io.ReadAll(testResp.Body)
	testBody = bytes.TrimSpace(testBody)

	// If we get an error response or HTML, login failed
	if len(testBody) > 0 && testBody[0] != '{' && testBody[0] != '[' {
		return fmt.Errorf("login failed: invalid credentials")
	}

	// Check for error in JSON response
	if bytes.Contains(testBody, []byte(`"error"`)) {
		return fmt.Errorf("login failed: %s", string(testBody))
	}

	c.loggedIn = true
	return nil
}

// GetDevices returns the list of devices associated with the account
func (c *Client) GetDevices() (*models.DeviceListResponse, error) {
	resp, err := c.doRequest("GET", axURL+"?action=iconList", nil)
	if err != nil {
		return nil, fmt.Errorf("failed to get devices: %w", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response: %w", err)
	}

	var result models.DeviceListResponse
	if err := json.Unmarshal(body, &result); err != nil {
		return nil, fmt.Errorf("failed to parse response: %w", err)
	}

	return &result, nil
}

// GetDevice returns detailed information about a specific device
func (c *Client) GetDevice(serial string) (*models.DeviceResponse, error) {
	resp, err := c.doRequest("GET", axURL+"?action=iconByID&serial="+serial, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to get device: %w", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response: %w", err)
	}

	var result models.DeviceResponse
	if err := json.Unmarshal(body, &result); err != nil {
		return nil, fmt.Errorf("failed to parse response: %w", err)
	}

	return &result, nil
}

// SetTemperature sets the target temperature for a thermostat
func (c *Client) SetTemperature(serial, thermostatID string, temperature float64) (*models.SetResponse, error) {
	// Create multipart form data
	var buf bytes.Buffer
	writer := multipart.NewWriter(&buf)

	_ = writer.WriteField("action", "setThermostat")
	_ = writer.WriteField("icon", serial)
	_ = writer.WriteField("thermostat", thermostatID)
	_ = writer.WriteField("attr", "REQ")
	_ = writer.WriteField("value", strconv.FormatFloat(temperature, 'f', 1, 64))

	writer.Close()

	req, err := http.NewRequest("POST", axURL, &buf)
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}
	req.Header.Set("Content-Type", writer.FormDataContentType())
	req.Header.Set("User-Agent", userAgent)

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to set temperature: %w", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response: %w", err)
	}

	var result models.SetResponse
	if err := json.Unmarshal(body, &result); err != nil {
		return nil, fmt.Errorf("failed to parse response: %w", err)
	}

	return &result, nil
}

// IsLoggedIn returns whether the client has successfully authenticated
func (c *Client) IsLoggedIn() bool {
	return c.loggedIn
}
