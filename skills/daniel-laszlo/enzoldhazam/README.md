# enzoldhazam

CLI tool for controlling thermostats via [enzoldhazam.hu](https://www.enzoldhazam.hu) (NGBS iCON Smart Home system).

## Installation

```bash
# Clone the repository
git clone https://github.com/daniel-laszlo/enzoldhazam.git
cd enzoldhazam

# Build
go build -o enzoldhazam ./cmd/enzoldhazam

# Optional: move to PATH
mv enzoldhazam /usr/local/bin/
```

## Usage

### Authentication

Login and save credentials to macOS Keychain:

```bash
enzoldhazam login
```

Or use environment variables:

```bash
export ENZOLDHAZAM_USER="your-email@example.com"
export ENZOLDHAZAM_PASS="your-password"
```

### Commands

```bash
# Show all rooms with current/target temperatures
enzoldhazam status

# Get specific room details
enzoldhazam get <room-name>
enzoldhazam get <thermostat-id>

# Set target temperature
enzoldhazam set <room-name> <temperature>

# Clear stored credentials
enzoldhazam logout
```

### JSON Output

All data commands support `--json` flag for automation:

```bash
enzoldhazam status --json
enzoldhazam get <room-name> --json
```

## Example Output

```
$ enzoldhazam status
Device: My Device (123456789012)
Status: Online | Water: 38.2°C | External: 5.0°C

Living Room     22.5°C (target: 21.5°C) RH: 31%
Office          21.6°C (target: 21.5°C) RH: 30%
Bedroom         21.8°C (target: 21.5°C) RH: 26%
```

## Requirements

- Go 1.21+
- macOS (for Keychain credential storage)
- An enzoldhazam.hu account with registered NGBS iCON device(s)

## License

MIT
