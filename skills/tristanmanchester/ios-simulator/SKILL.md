---
name: ios-simulator
description: Automate iOS Simulator workflows (simctl + idb): create/boot/erase devices, install/launch apps, push notifications, privacy grants, screenshots, and accessibility-based UI navigation. Use when working with iOS apps, Xcode, Simulator, simctl, idb, UI automation, or iOS testing.
metadata: {"clawdbot":{"emoji":"📱","os":["darwin"],"requires":{"bins":["xcrun"]},"install":[{"brew":{"formula":"idb-companion","bins":["idb_companion"],"tap":"facebook/fb"}}]}}
---

# iOS Simulator Automation

This skill provides a **Node-only** CLI wrapper around:
- `xcrun simctl` for simulator/device/app management
- `idb` for **accessibility-tree** inspection + synthesised UI input (tap/text/button)

It is designed for **AI agents**: minimal, structured output by default, with opt-in detail.

## Important constraints

- **Must run on macOS** with Xcode Command Line Tools (or Xcode) available.
- If the ClawdBot gateway is not macOS, run these commands on a connected **macOS node** (see “Remote macOS node” below).  
- `idb` is optional, but required for UI tree / semantic tapping. (Install steps below.)

## Quick start

```bash
# 1) Sanity check
node {baseDir}/scripts/ios-sim.mjs health

# 2) List simulators (compact)
node {baseDir}/scripts/ios-sim.mjs list

# 3) Select a default simulator (writes .ios-sim-state.json in the current dir)
node {baseDir}/scripts/ios-sim.mjs select --name "iPhone" --runtime "iOS" --boot

# 4) Install + launch an .app
node {baseDir}/scripts/ios-sim.mjs app install --app path/to/MyApp.app
node {baseDir}/scripts/ios-sim.mjs app launch --bundle-id com.example.MyApp

# 5) Inspect current UI (requires idb)
node {baseDir}/scripts/ios-sim.mjs ui summary
node {baseDir}/scripts/ios-sim.mjs ui tap --query "Log in"
node {baseDir}/scripts/ios-sim.mjs ui type --text "hello world"

# 6) Screenshot
node {baseDir}/scripts/ios-sim.mjs screenshot --out artifacts/screen.png
```

## Remote macOS node

If you are not on macOS, run the same commands on the macOS node using ClawdBot’s node execution (e.g. `exec` with `host: node` / node tools). Ensure the skill folder exists on that node, or copy it there.

## Output conventions (token-efficient)

- Default output: **single-line JSON** (small summary object).
- Add `--pretty` to pretty-print JSON.
- Add `--text` for a short human-readable summary (when provided by the command).
- Commands that can be huge (`ui tree`, `list --full`) are **opt-in**.

## State / default UDID

`select` writes a state file (default: `./.ios-sim-state.json`) that stores the chosen UDID.
All commands accept `--udid <UUID>` and otherwise fall back to the state file.

Override location with:
- `IOS_SIM_STATE_FILE=/path/to/state.json`

## Dependency notes

### Xcode / simctl availability
If `xcrun` cannot find `simctl`, ensure Xcode CLI tools are selected (via Xcode settings or `xcode-select`) and run the first-launch setup:
- `xcodebuild -runFirstLaunch`

### idb (for accessibility automation)
Install `idb_companion` and the `idb` CLI:
```bash
brew tap facebook/fb
brew install idb-companion
python3 -m pip install --upgrade fb-idb
```

## Safety tiers

| Tier | Commands | Notes |
|------|----------|------|
| SAFE | `list`, `health`, `boot`, `shutdown`, `screenshot`, `ui *` | No data loss |
| CAUTION | `privacy *`, `push`, `clipboard *`, `openurl` | Alters simulator/app state |
| DANGEROUS | `erase`, `delete` | Requires `--yes` |

## Command index

All commands live under:
```bash
node {baseDir}/scripts/ios-sim.mjs <command> [subcommand] [flags]
```

### Core simulator lifecycle
- `list [--full]`
- `select --name <substr> [--runtime <substr>] [--boot]`
- `boot [--udid <uuid>] [--wait]`
- `shutdown [--udid <uuid>|--all]`
- `erase --yes [--udid <uuid>|--all]`
- `delete --yes [--udid <uuid>]`
- `create --name <name> --device-type <substr> --runtime <substr>`

### App management
- `app install --app <path/to/App.app> [--udid ...]`
- `app uninstall --bundle-id <id> [--udid ...]`
- `app launch --bundle-id <id> [--udid ...] [-- <args...>]`
- `app terminate --bundle-id <id> [--udid ...]`
- `app container --bundle-id <id> [--type data|app] [--udid ...]`

### Screenshots & video
- `screenshot --out <file.png> [--udid ...]`
- `record-video --out <file.mp4> [--udid ...]` (runs until Ctrl+C)

### Clipboard / URL
- `clipboard get [--udid ...]`
- `clipboard set --text <text> [--udid ...]`
- `openurl --url <url> [--udid ...]`

### Simulator permissions & push notifications
- `privacy grant --bundle-id <id> --service <svc[,svc...]> [--udid ...]`
- `privacy revoke --bundle-id <id> --service <svc[,svc...]> [--udid ...]`
- `privacy reset --bundle-id <id> --service <svc[,svc...]> [--udid ...]`
- `push --bundle-id <id> --payload <json-string> [--udid ...]`

### Logs
- `logs show [--last 5m] [--predicate <expr>] [--udid ...]`

### Accessibility-driven UI automation (requires idb)
- `ui summary [--limit 12]`
- `ui tree` (full UI JSON array)
- `ui find --query <text> [--limit 20]`
- `ui tap --query <text>` (find + tap best match)
- `ui tap --x <num> --y <num>` (raw coordinate tap)
- `ui type --text <text>`
- `ui button --name HOME|LOCK|SIRI|SIDE_BUTTON|APPLE_PAY`

## Troubleshooting

See: [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)
