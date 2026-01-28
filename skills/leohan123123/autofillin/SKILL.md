---
name: autofillin
description: Automated web form filling and file uploading skill with Playwright browser automation. Handles login persistence, form detection, file uploads, and waits for manual confirmation before submission.
version: 1.1.0
trigger: autofillin
author: leohan123123
tags: automation, form, upload, browser, playwright, mcp
---

# AutoFillIn - Browser Form Automation Skill

**Trigger Command**: `autofillin`

An intelligent automation skill that fills web forms, uploads files/folders to correct positions, and handles complex multi-field submissions with persistent login support.

## What's New in v1.1.0

- Persistent Login: Uses Playwright with `--save-storage` to preserve login sessions
- Playwright Chromium: No more "unsafe browser" blocks from Google OAuth
- Folder Upload Support: Works with `webkitdirectory` file inputs
- Auto-retry Login: Detects login pages and prompts for one-time authentication

## Features

- Navigate to any web form URL
- Auto-fill text fields, textareas, dropdowns
- Upload files/folders to correct form positions
- Persistent login via saved browser storage
- Wait for manual confirmation before submission
- Support for multi-file uploads with position mapping

## Quick Setup

```bash
# 1. Install Playwright browsers
npx playwright install chromium

# 2. First-time login (saves session for reuse)
npx playwright open --save-storage=~/.playwright-auth.json "https://your-target-site.com"
# Login manually in the browser that opens, then close it

# 3. Future runs will auto-login using saved session
npx playwright open --load-storage=~/.playwright-auth.json "https://your-target-site.com"
```

## Browser Automation Options

### Option 1: Playwright CLI (Recommended for OAuth sites)

```bash
# First login - saves session
npx playwright open --save-storage=~/.playwright-auth.json "https://molthub.com/upload"

# Subsequent uses - loads saved session
npx playwright open --load-storage=~/.playwright-auth.json "https://molthub.com/upload"
```

Advantages:
- No "unsafe browser" blocks from Google/GitHub OAuth
- Session persistence across runs
- Works with MCP browser tools

### Option 2: Chrome Debug Mode (For non-OAuth sites)

```bash
# Start Chrome with debug port
~/clawd/skills/autofillin/scripts/start-chrome.sh "https://example.com/form"
```

Note: Chrome debug mode with custom `--user-data-dir` is blocked by Google OAuth. Use Playwright for sites requiring Google/GitHub login.

## Usage Examples

### Basic Form Filling

```
autofillin https://example.com/form
- Fill "Name" field with "John Doe"
- Fill "Email" field with "john@example.com"
- Upload resume.pdf to file input
```

### MoltHub Skill Upload (This skill was published this way!)

```
autofillin https://molthub.com/upload

Form Data:
- Slug: autofillin
- Display name: AutoFillIn - Browser Form Automation Skill
- Version: 1.1.0
- Tags: automation, browser, form, playwright, mcp
- Changelog: v1.1.0 - Added Playwright support, session persistence

Upload:
- Folder: ~/clawd/skills/autofillin/

[WAIT FOR MANUAL CONFIRMATION TO PUBLISH]
```

## Workflow

```
1. BROWSER SETUP
   - Check for saved session (~/.playwright-auth.json)
   - Launch Playwright Chromium with session
   - Or prompt for one-time login if no session exists

2. NAVIGATION & LOGIN
   - Navigate to target URL
   - Detect if login is required
   - If login needed: Fill username, prompt for password, save session

3. PAGE ANALYSIS
   - Take accessibility snapshot
   - Identify all form fields
   - Map field labels to input elements

4. AUTO-FILL PHASE
   - Fill text fields using fill() or fill_form()
   - Select dropdown options
   - Upload files/folders via upload_file()

5. CONFIRMATION PHASE
   - Display summary of filled data
   - WAIT FOR MANUAL CONFIRMATION
   - User reviews and clicks Submit/Publish
```

## MCP Tools Used

| Tool | Purpose |
|------|---------|
| take_snapshot | Get page accessibility tree |
| fill | Fill single form field |
| fill_form | Fill multiple fields at once |
| upload_file | Upload file or folder |
| browser_click | Click buttons |
| evaluate_script | Run JavaScript |
| navigate_page | Navigate to URLs |

## Credential Management

### Safe Storage (Recommended)

```bash
# Use macOS Keychain
security add-generic-password -a "github" -s "autofillin" -w "your-password"
security find-generic-password -a "github" -s "autofillin" -w
```

### Session Persistence

Sessions saved to `~/.playwright-auth.json` include cookies, localStorage, and sessionStorage.

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Unsafe browser | Google OAuth blocked | Use Playwright instead of Chrome debug |
| Login required | Session expired | Run with --save-storage |
| Element not found | Page changed | Take new snapshot |
| Upload failed | Wrong file type | Check webkitdirectory |

## Files in This Skill

```
autofillin/
├── SKILL.md              # This documentation
├── mcp-config.txt        # MCP configuration guide
└── scripts/
    ├── setup-env.sh      # Environment setup
    ├── start-chrome.sh   # Chrome debug launcher
    └── autofillin.sh     # Main orchestrator
```

## Author

- GitHub: [@leohan123123](https://github.com/leohan123123)
- MoltHub: [@leohan123123](https://molthub.com/leohan123123)

## License

MIT
