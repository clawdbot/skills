---
name: trein
description: Query Dutch Railways (NS) for train departures, trip planning, disruptions, and station search via the trein CLI.
homepage: https://github.com/joelkuijper/trein
metadata: {"clawdbot":{"emoji":"🚆","requires":{"bins":["trein"],"env":["NS_API_KEY"]},"primaryEnv":"NS_API_KEY","install":[{"id":"npm","kind":"node","package":"trein","bins":["trein"],"label":"Install trein (npm)"},{"id":"download-mac-arm","kind":"download","url":"https://github.com/joelkuijper/trein/releases/latest/download/trein-darwin-arm64","bins":["trein"],"label":"Download (macOS Apple Silicon)","os":["darwin"]},{"id":"download-mac-x64","kind":"download","url":"https://github.com/joelkuijper/trein/releases/latest/download/trein-darwin-x64","bins":["trein"],"label":"Download (macOS Intel)","os":["darwin"]},{"id":"download-linux","kind":"download","url":"https://github.com/joelkuijper/trein/releases/latest/download/trein-linux-x64","bins":["trein"],"label":"Download (Linux x64)","os":["linux"]}]}}
---

# trein - Dutch Railways CLI

A CLI for the NS (Dutch Railways) API with real-time departures, trip planning, disruptions, and station search.

## Install

npm (recommended):
```bash
npm i -g trein
```

Or download a standalone binary from [GitHub Releases](https://github.com/joelkuijper/trein/releases).

## Setup

Get an API key from https://apiportal.ns.nl/ and set it:
```bash
export NS_API_KEY="your-api-key"
```

Or create `~/.config/trein/trein.config.json`:
```json
{ "apiKey": "your-api-key" }
```

## Commands

### Departures
```bash
trein departures "Amsterdam Centraal"
trein d amsterdam
trein d amsterdam --json  # structured output
```

### Trip Planning
```bash
trein trip "Utrecht" "Den Haag Centraal"
trein t utrecht denhaag --json
```

### Disruptions
```bash
trein disruptions
trein disruptions --json
```

### Station Search
```bash
trein stations rotterdam
trein s rotterdam --json
```

### Aliases (shortcuts)
```bash
trein alias set home "Amsterdam Centraal"
trein alias set work "Rotterdam Centraal"
trein alias list
trein d home  # uses alias
```

## Tips
- Use `--json` flag for all commands to get structured output for parsing
- Station names support fuzzy matching (e.g., "adam" -> "Amsterdam Centraal")
- Aliases are stored in the config file and can be used in place of station names
