# Claude OAuth Token Refresher

Automatically refreshes your Claude tokens before they expire. No more authentication failures.

**The problem:** Claude tokens expire every 8 hours, interrupting your workflow with authentication errors.

**This tool:** Monitors and refreshes your tokens automatically so you never see auth failures again.

---

## 🔑 Prerequisites

Before installing this skill, you need:

### Step 1: Install Claude Code CLI

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

### Step 2: Run Claude and Log In

```bash
claude
```

Follow the login prompts. **This creates the Keychain item** that stores your tokens.

### Step 3: Install Clawdbot (if you haven't)

```bash
npm install -g clawdbot
clawdbot gateway start
```

---

## 📋 Requirements

- macOS with Keychain
- Claude Code CLI (installed and authenticated above)
- `jq` (`brew install jq`)
- Clawdbot (for scheduling)

---

## ⚡ What It Does

**Your tokens stay fresh automatically.**

The tool:
- Checks your Claude token every few hours
- Refreshes it 30 minutes before expiry
- Updates both Keychain and Clawdbot config
- Runs silently in the background

Zero manual intervention needed.

---

## 🚀 Installation

**After completing prerequisites above:**

```bash
clawdhub install claude-oauth-refresher
```

### First-Time Setup

**Run the refresher to get your model running on Claude subscription:**

```bash
cd ~/clawd/skills/claude-oauth-refresher
./refresh-token.sh
```

**Expected output:**
```
✅ Token still valid (475 minutes remaining)
```

**That's it!** The script auto-discovers your keychain setup and automates token refresh.

### What Happens

The installation:
- Finds your tokens in Keychain automatically
- Validates token structure
- Sets up automatic refresh schedule
- Logs all operations to `~/clawd/logs/`

---

## 🔧 How It Works

**Result:** Your tokens stay fresh without you thinking about it.

**The process:**

1. **Reads** your current token from macOS Keychain
2. **Checks** expiry time (refreshes 30 min before expiry)
3. **Calls** Anthropic OAuth API with your refresh token
4. **Updates** both Keychain and Clawdbot config automatically

**Smart fallback:** If your account name isn't "claude", it tries common alternatives: "Claude Code", "default", "oauth", "anthropic"

**Example (force refresh):**

```bash
./refresh-token.sh --force
```

Output:
```
[17:48:16] ✓ Received new tokens
[17:48:16] New expiry: 2026-01-24 01:48:16 (8 hours)
[17:48:16] ✓ Auth file updated
[17:48:16] ✓ Keychain updated
✅ Token refreshed successfully!
```

---
---

# 📚 Additional Information

**Everything below is optional.** The skill works out-of-the-box for most users.

This section contains:
- Advanced configuration options
- Implementation details for developers
- Troubleshooting for edge cases

**You don't need to read this for initial installation.**

---

<details>
<summary><b>Configuration Options</b> (optional customization)</summary>

<br>

Create `claude-oauth-refresh-config.json` if you need to customize:

```json
{
  "refresh_buffer_minutes": 30,
  "keychain_service": "Claude Code-credentials",
  "keychain_account": "claude",
  "auth_file": "~/.clawdbot/agents/main/agent/auth-profiles.json"
}
```

Most users don't need this - the defaults work fine.

</details>

<details>
<summary><b>Setting Up Another Device</b></summary>

<br>

The script has automatic fallback.

Usually you just:
1. Copy the skill folder
2. Run `./refresh-token.sh`
3. It finds your tokens automatically

**If your setup is unusual:**

Check which keychain account has your tokens:
```bash
security find-generic-password -l "Claude Code-credentials"
```

Look for the entry with `"acct"<blob>="your-account-name"`

Then create a config file with your account name.

</details>

<details>
<summary><b>How Detection Works</b> (implementation details)</summary>

<br>

The script:
1. Tries your configured account name first
2. If that fails or has incomplete data, tries common names
3. Validates each entry has `refreshToken` and `expiresAt`
4. Uses the first complete entry found

**Data structure expected:**
```json
{
  "claudeAiOauth": {
    "accessToken": "sk-ant-oat01-...",
    "refreshToken": "sk-ant-ort01-...",
    "expiresAt": 1769190496000,
    "scopes": [...],
    "subscriptionType": "max",
    "rateLimitTier": "default_claude_max_20x"
  }
}
```

</details>

<details>
<summary><b>Troubleshooting</b></summary>

<br>

### "No refreshToken in keychain"

Your keychain account name is different.

The script should auto-discover it.

If not:
```bash
security find-generic-password -l "Claude Code-credentials"
```

Check which account has the tokens.

### "Failed to retrieve from Keychain"

Possible causes:
- Keychain is locked
- Entry doesn't exist

Run:
```bash
security find-generic-password -s "Claude Code-credentials" -l
```

### Token refresh fails

Check:
- Internet connection
- Refresh token hasn't been revoked
- Re-authenticate with Claude if needed

</details>

<details>
<summary><b>For Developers</b> (architecture)</summary>

<br>

### Data Flow

```
Keychain (claudeAiOauth JSON)
    ↓ read refreshToken, expiresAt
OAuth API (POST with refresh_token)
    ↓ returns new accessToken, refreshToken, expires_in
Update Keychain (complete JSON)
    ↓
Update auth-profiles.json (just accessToken)
```

### Automatic Scheduling

After refresh, creates a Clawdbot cron job:
```bash
Next refresh = (new_expiry - buffer_minutes)
```

### Portability Features

- Tries multiple common account names
- Validates data structure before using
- Helpful errors with diagnostic commands
- Works without config file using sensible defaults

</details>

---

## License

MIT
