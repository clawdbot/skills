---
name: alexa-cli
description: Control Amazon Alexa devices and smart home via the `alexacli` CLI. Use when a user asks to speak/announce on Echo devices, control lights/thermostats/locks, send voice commands, or query Alexa.
homepage: https://github.com/buddyh/alexa-cli
metadata: {"clawdbot":{"emoji":"🔊","requires":{"bins":["alexacli"]},"install":[{"id":"brew","kind":"brew","formula":"buddyh/tap/alexacli","bins":["alexacli"],"label":"Install alexacli (brew)"},{"id":"go","kind":"go","module":"github.com/buddyh/alexa-cli/cmd/alexa@latest","bins":["alexacli"],"label":"Install alexa-cli (go)"}]}}
---

# Alexa CLI

Use `alexacli` to control Amazon Echo devices and smart home via the unofficial Alexa API.

## Devices

```bash
alexacli devices
alexacli devices --json
```

## Text-to-Speech

```bash
# Speak on a specific device
alexacli speak "Hello world" -d "Kitchen Echo"

# Announce to ALL devices
alexacli speak "Dinner is ready!" --announce

# Device name matching is flexible
alexacli speak "Build complete" -d Kitchen
```

## Voice Commands (Smart Home Control)

Send any command as if you spoke it to Alexa:

```bash
# Lights
alexacli command "turn off the living room lights" -d Kitchen
alexacli command "dim the bedroom lights to 50 percent" -d Bedroom

# Thermostat
alexacli command "set thermostat to 72 degrees" -d Bedroom

# Locks
alexacli command "lock the front door" -d Kitchen

# Music
alexacli command "play jazz music" -d "Living Room"

# Timers
alexacli command "set a timer for 10 minutes" -d Kitchen
```

The `-d` flag specifies which Echo processes the command.

## Ask (Get Response Back)

Send a command and capture Alexa's text response:

```bash
alexacli ask "what's the thermostat set to" -d Kitchen
# Output: The thermostat is set to 68 degrees.

alexacli ask "what's on my calendar today" -d Kitchen --json
```

Useful for querying device state or getting Alexa-specific info.

## History

```bash
alexacli history
alexacli history --limit 5 --json
```

## Command Reference

| Command | Description |
|---------|-------------|
| `alexacli devices` | List all Echo devices |
| `alexacli speak <text> -d <device>` | Text-to-speech on device |
| `alexacli speak <text> --announce` | Announce to all devices |
| `alexacli command <text> -d <device>` | Voice command (smart home, music, etc.) |
| `alexacli ask <text> -d <device>` | Send command, get response back |
| `alexacli history` | View recent voice activity |
| `alexacli auth` | Configure authentication |

## Notes

- Uses Amazon's unofficial API (same as Alexa app)
- Refresh token valid ~14 days, re-run `alexacli auth` if expired
- Device names support partial, case-insensitive matching
- For AI/agentic use, `alexacli command` with natural language is preferred
