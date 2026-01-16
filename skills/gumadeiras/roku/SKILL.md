---
name: roku
description: CLI interface to control Roku devices via python-roku.
homepage: https://github.com/gumadeiras/roku-cli
metadata: {"clawdbot":{"emoji":"📺","requires":{"bins":["roku"]},"install":[{"id":"python","kind":"pip","package":"roku","bins":["roku"],"label":"Install roku (pip)"}]}}
---

# roku CLI

Control your Roku from the command line using python-roku.

Setup
- CLI available at: https://github.com/gumadeiras/roku-cli
- Install: `pip3 install roku`
- Find your Roku IP: `roku discover` or check Roku settings > Network
- Use `--ip 192.168.x.x` or set default in commands

You may need to change the remote control setting on the Roku:

Settings → System → Advanced System Settings → Control by Mobile Apps → Enable

Common commands
- Discover: `roku discover`
- Navigation: `roku press home|back|left|right|up|down|select`
- Text entry: `roku text "search query"`
- Apps: `roku apps` (list), `roku launch Netflix` (launch by name or ID)
- Status: `roku active` (current app), `roku info` (device info)

Key options
- `--ip 192.168.x.x` - Specify Roku IP (auto-discovers if omitted)
- `roku press --event keydown|keyup` - Key hold/release events

Examples
```bash
# Find your Roku
roku discover

# Control playback
roku press play
roku press pause
roku press forward
roku press reverse

# Navigate menus
roku press right
roku press select
roku press back
roku press home

# Enter text (e.g., in search)
roku text "netflix"

# List and launch apps
roku apps
roku launch Hulu
roku launch 12  # by app ID

# Check what's playing
roku active
```

Notes
- Auto-discovery works on local network; may need `--timeout 10` for slow networks
- App names are case-insensitive
- Use app ID (from `roku apps`) if name lookup fails
