---
name: railil
description: Search for Israel Rail train schedules using the railil CLI. Find routes between stations with fuzzy search, filter by date/time, and output in various formats (JSON, Markdown, Table).
homepage: https://github.com/lirantal/railil
metadata: {"clawdbot":{"emoji":"🚆","requires":{"bins":["railil"]},"install":[{"id":"node","kind":"node","package":"railil","bins":["railil"],"label":"Install railil (npm)"}]}}
---

# Railil CLI

A CLI tool for checking Israel Rail train schedules.

## Installation

```bash
npm install -g railil
```

## Usage

The CLI supports fuzzy matching for station names.

### Basic Search

Search for the next trains between two stations:

```bash
railil --from "Tel Aviv" --to "Haifa"
```

### Date and Time

Search for a specific date and time:

```bash
railil --from "Beer Sheva" --to "Tel Aviv" --time 08:00 --date 2023-11-01
```

### Output Formats

For machine-readable output or specific formatting, use the `--output` flag.
Supported formats: `text` (default), `json`, `table`, `markdown`.

**JSON Output (Recommended for agents):**
```bash
railil --from "Tel Aviv" --to "Haifa" --output json
```

**Markdown Output:**
```bash
railil --from "Tel Aviv" --to "Haifa" --output markdown
```

### Options

- `-f, --from <station>`: Origin station name (fuzzy match supported).
- `-t, --to <station>`: Destination station name (fuzzy match supported).
- `-d, --date <date>`: Date of travel.
- `-h, --time <time>`: Time of travel (HH:MM).
- `-l, --limit <number>`: Limit the number of results.
- `-o, --output <format>`: Output format (`json`, `text`, `table`, `markdown`).
- `--help`: Show help message.

## Examples

**Find next 3 trains from Ben Gurion Airport to Jerusalem:**
```bash
railil --from "Ben Gurion" --to "Jerusalem" --limit 3
```

**Get schedule for tomorrow morning in JSON:**
```bash
railil --from "Haifa" --to "Tel Aviv" --time 07:30 --output json
```
