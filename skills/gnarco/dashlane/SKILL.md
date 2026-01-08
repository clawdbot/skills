---
name: dashlane
description: Access passwords, secure notes, secrets and OTP codes from Dashlane vault.
homepage: https://cli.dashlane.com
metadata: {"clawdbot":{"emoji":"🔐","requires":{"bins":["dcli"]}}}
---

# Dashlane CLI

Access your Dashlane vault from the command line. Read-only access to passwords, secure notes, secrets and OTP codes.

## Installation

```bash
brew install dashlane/tap/dashlane-cli
```

## Authentication

First sync to trigger authentication:
```bash
dcli sync
```

**Steps:**
1. Enter your Dashlane email
2. **⚠️ IMPORTANT: Open the URL shown in your browser** (device registration)
3. Enter the code received by email
4. Enter your Master Password

Check current account:
```bash
dcli accounts whoami
```

## Get a Password

```bash
# Search by URL or title (copies password to clipboard by default)
dcli p mywebsite
dcli password mywebsite

# Get specific field
dcli p mywebsite -f login      # Username/login
dcli p mywebsite -f email      # Email
dcli p mywebsite -f otp        # TOTP 2FA code
dcli p mywebsite -f password   # Password (default)

# Output formats
dcli p mywebsite -o clipboard  # Copy to clipboard (default)
dcli p mywebsite -o console    # Print to stdout
dcli p mywebsite -o json       # Full JSON output (all matches)

# Search by specific fields
dcli p url=example.com
dcli p title=MyBank
dcli p id=xxxxxx               # By vault ID
dcli p url=site1 title=site2   # Multiple filters (OR)
```

## Get a Secure Note

```bash
dcli note [filters]
dcli n [filters]               # Shorthand

# Filter by title (default)
dcli n my-note
dcli n title=api-keys

# Output formats: text (default), json
dcli n my-note -o json
```

## Get a Secret

Dashlane secrets are a dedicated content type for sensitive data.

```bash
dcli secret [filters]

# Filter by title (default)
dcli secret api_keys
dcli secret title=api_keys -o json
```

## Other Commands

```bash
# Sync vault manually (auto-sync every hour by default)
dcli sync

# Lock the vault (requires master password to unlock)
dcli lock

# Logout completely
dcli logout

# Backup vault to current directory
dcli backup
dcli backup --directory /path/to/backup
```

## Configuration

```bash
# Save master password in OS keychain (default: true)
dcli configure save-master-password true

# Disable auto-sync
dcli configure disable-auto-sync true

# Enable biometrics unlock (macOS only)
dcli configure user-presence --method biometrics

# Disable user presence check
dcli configure user-presence --method none
```

## Persistence by Platform

### macOS
Master password is stored in the **Keychain** by default. Survives reboots.
```bash
dcli configure save-master-password true
```

### Linux (server/headless)
No native keychain. Options:
1. **Environment variable** (less secure, but simple):
   ```bash
   export DASHLANE_MASTER_PASSWORD="..."
   ```
2. **Local encrypted file**: `save-master-password true` stores in `~/.local/share/dcli/`
3. **External secret manager** (Vault, AWS Secrets, etc.) to inject the variable

### Docker / CI
Use the `DASHLANE_MASTER_PASSWORD` environment variable passed to the container.
```bash
docker run -e DASHLANE_MASTER_PASSWORD="..." myimage
```

### SSO / Passwordless
Not supported by dcli yet — requires a classic master password.

## Advanced: Inject Secrets

```bash
# Inject secrets into environment variables
dcli exec -- mycommand

# Inject into templated files
dcli inject < template.txt > output.txt

# Read secret by path
dcli read "dl://vault/secret-id"
```

## Examples

### Get OTP for 2FA
```bash
dcli p github -f otp
# Returns: 123456 (25s remaining)
```

### SSH Keys from Vault
Store private key in a secure note, then:
```bash
dcli n SSH_KEY | ssh-add -
```

### Scripting
```bash
# Get password for a script
PASSWORD=$(dcli p myservice -o console)

# Get JSON and parse with jq
dcli p myservice -o json | jq -r '.[0].password'
```

## Troubleshooting

- **Locked?** Run `dcli sync` to unlock
- **SSO users:** Need Chrome installed + visual interface
- **Password-less:** Not supported yet
- **Debug mode:** `dcli --debug <command>`

Docs: https://cli.dashlane.com
