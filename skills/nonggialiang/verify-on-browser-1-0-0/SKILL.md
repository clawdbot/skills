---
description: Control browser via Chrome DevTools Protocol - full CDP access
---

# Browser Control Skill

Use the `browser` MCP server to control a browser with full CDP access. The core `cdp_send` tool can call ANY Chrome DevTools Protocol method.

## Available Tools

### `cdp_send` - Raw CDP Access
Call any CDP method directly:
```
cdp_send(method: "Domain.method", params: {...})
```

### `screenshot` - Capture Page
```
screenshot(format: "png"|"jpeg", fullPage: true|false)
```

### `get_url` - Current URL
```
get_url()
```

### `close_browser` - Close Browser
```
close_browser()
```

## Common CDP Operations

### Navigation
```javascript
// Navigate to URL
cdp_send(method: "Page.navigate", params: { url: "https://example.com" })

// Reload
cdp_send(method: "Page.reload")

// Go back/forward
cdp_send(method: "Page.navigateToHistoryEntry", params: { entryId: 1 })
```

### DOM Manipulation
```javascript
// Get document root
cdp_send(method: "DOM.getDocument")

// Query selector (needs nodeId from getDocument)
cdp_send(method: "DOM.querySelector", params: { nodeId: 1, selector: "h1" })

// Get outer HTML
cdp_send(method: "DOM.getOuterHTML", params: { nodeId: 5 })

// Set attribute
cdp_send(method: "DOM.setAttributeValue", params: { nodeId: 5, name: "class", value: "new-class" })
```

### JavaScript Execution
```javascript
// Evaluate expression
cdp_send(method: "Runtime.evaluate", params: { expression: "document.title" })

// Evaluate with return value
cdp_send(method: "Runtime.evaluate", params: {
  expression: "document.querySelectorAll('a').length",
  returnByValue: true
})

// Call function on object
cdp_send(method: "Runtime.callFunctionOn", params: {
  objectId: "...",
  functionDeclaration: "function() { return this.innerText; }"
})
```

### Network
```javascript
// Enable network tracking (required first)
cdp_send(method: "Network.enable")

// Set cookies
cdp_send(method: "Network.setCookie", params: {
  name: "session",
  value: "abc123",
  domain: ".example.com"
})

// Get cookies
cdp_send(method: "Network.getCookies")

// Clear cache
cdp_send(method: "Network.clearBrowserCache")

// Set extra headers
cdp_send(method: "Network.setExtraHTTPHeaders", params: {
  headers: { "X-Custom": "value" }
})

// Block URLs
cdp_send(method: "Network.setBlockedURLs", params: { urls: ["*.ads.com"] })
```

### Input Simulation
```javascript
// Click (dispatch mouse event)
cdp_send(method: "Input.dispatchMouseEvent", params: {
  type: "mousePressed",
  x: 100,
  y: 200,
  button: "left",
  clickCount: 1
})

// Type text
cdp_send(method: "Input.insertText", params: { text: "Hello world" })

// Key press
cdp_send(method: "Input.dispatchKeyEvent", params: {
  type: "keyDown",
  key: "Enter"
})
```

### Emulation
```javascript
// Set viewport
cdp_send(method: "Emulation.setDeviceMetricsOverride", params: {
  width: 375,
  height: 812,
  deviceScaleFactor: 3,
  mobile: true
})

// Set geolocation
cdp_send(method: "Emulation.setGeolocationOverride", params: {
  latitude: 37.7749,
  longitude: -122.4194,
  accuracy: 100
})

// Set timezone
cdp_send(method: "Emulation.setTimezoneOverride", params: { timezoneId: "America/New_York" })
```

### Performance & Debugging
```javascript
// Enable performance metrics
cdp_send(method: "Performance.enable")

// Get metrics
cdp_send(method: "Performance.getMetrics")

// Start profiler
cdp_send(method: "Profiler.start")

// Stop and get profile
cdp_send(method: "Profiler.stop")

// Enable debugger
cdp_send(method: "Debugger.enable")

// Set breakpoint
cdp_send(method: "Debugger.setBreakpointByUrl", params: {
  lineNumber: 10,
  url: "https://example.com/script.js"
})
```

### Storage
```javascript
// Get local storage
cdp_send(method: "DOMStorage.getDOMStorageItems", params: {
  storageId: { securityOrigin: "https://example.com", isLocalStorage: true }
})

// Clear storage
cdp_send(method: "Storage.clearDataForOrigin", params: {
  origin: "https://example.com",
  storageTypes: "all"
})
```

## CDP Protocol Reference

For complete list of all domains and methods:
https://chromedevtools.github.io/devtools-protocol/

Common domains:
- **Page** - Navigation, lifecycle, PDF generation
- **DOM** - Document structure manipulation
- **CSS** - Stylesheet manipulation
- **Runtime** - JavaScript execution
- **Network** - Request/response interception
- **Input** - Keyboard/mouse simulation
- **Emulation** - Device/viewport simulation
- **Debugger** - JavaScript debugging
- **Performance** - Performance metrics
- **Storage** - localStorage, IndexedDB, cookies
