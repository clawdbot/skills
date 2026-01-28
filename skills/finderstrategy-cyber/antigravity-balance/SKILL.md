---
name: antigravity-balance
description: Check Google Antigravity AI model quota/token balance. Use when a user asks about their Antigravity usage, remaining tokens, model limits, quota status, or rate limits. Works by detecting the local Antigravity language server process and querying its API.
---

# Antigravity Balance

Check your Antigravity AI model quota and token balance.

## Quick Start

```bash
# Check quota (auto-detects local Antigravity process)
node scripts/agquota.js

# JSON output for parsing
node scripts/agquota.js --json

# Verbose output (debugging)
node scripts/agquota.js -v
```

## How It Works

1. **Process Detection**: Finds the running `language_server_macos_arm` (or platform equivalent) process
2. **Extracts Connection Info**: Parses `--extension_server_port` and `--csrf_token` from process args
3. **Port Discovery**: Scans nearby ports to find the HTTPS API endpoint (typically extensionPort + 1)
4. **Queries Local API**: Hits `https://127.0.0.1:{port}/exa.language_server_pb.LanguageServerService/GetUserStatus`
5. **Displays Quota**: Shows remaining percentage, reset time, and model info

## Output Format

Default output shows:
- User name, email, and tier
- Model name and remaining quota percentage
- Visual progress bar (color-coded: green >50%, yellow >20%, red ≤20%)
- Reset countdown (e.g., "4h 32m")

JSON output (`--json`) returns structured data:
```json
{
  "user": { "name": "...", "email": "...", "tier": "..." },
  "models": [
    { "label": "Claude Sonnet 4.5", "remainingPercent": 80, "resetTime": "..." }
  ],
  "timestamp": "2026-01-28T01:00:00.000Z"
}
```

## Requirements

- Node.js (uses built-in `https` module)
- Antigravity (or Windsurf) must be running

## Troubleshooting

If the script fails:
1. Ensure Antigravity/Windsurf is running
2. Check if the language server process exists: `ps aux | grep language_server`
3. The process must have `--app_data_dir antigravity` in its args (distinguishes from other Codeium forks)

## Platform-Specific Process Names

| Platform | Process Name |
|----------|--------------|
| macOS (ARM) | `language_server_macos_arm` |
| macOS (Intel) | `language_server_macos` |
| Linux | `language_server_linux` |
| Windows | `language_server_windows_x64.exe` |
