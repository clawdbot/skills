# Troubleshooting

## `xcrun: error: unable to find utility "simctl", not a developer tool or in PATH`
- Ensure Xcode / Command Line Tools are installed.
- Ensure the correct developer dir is selected:
  - `xcode-select -p` to view
  - `sudo xcode-select -s /Applications/Xcode.app` (or your Xcode path)
- Run first-launch component install:
  - `xcodebuild -runFirstLaunch`

## No simulators listed / missing runtimes
- Open Xcode → Settings/Preferences → Platforms (or Components) and install an iOS Simulator runtime.
- Then re-run:
  - `node {baseDir}/scripts/ios-sim.mjs list --full`

## `idb` not found
This skill can still do `simctl` operations, but UI automation requires `idb`.

Install:
```bash
brew tap facebook/fb
brew install idb-companion
python3 -m pip install --upgrade fb-idb
```

## `idb` can’t see the simulator / empty output
- Make sure the simulator is booted:
  - `node {baseDir}/scripts/ios-sim.mjs boot --wait`
- Try running `idb` directly:
  - `idb ui describe-all --udid <UDID>`
- If you have multiple simulators booted, always pass `--udid`.

## UI element not found via `ui tap --query ...`
- The accessibility label might differ from visible text.
- Use:
  - `node {baseDir}/scripts/ios-sim.mjs ui summary --limit 50`
  - or `node {baseDir}/scripts/ios-sim.mjs ui tree` and search the JSON for `AXLabel` / `title`.
- If there are multiple matches, narrow the query (e.g. “Log in” vs “Log”).

## ClawdBot gateway not on macOS
You must run commands on a macOS environment (gateway or node) where Xcode tools exist.

Use ClawdBot’s node execution so the command runs on the macOS node.
