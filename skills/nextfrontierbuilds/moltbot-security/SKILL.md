---
name: moltbot-security
description: Security hardening guide for Moltbot/Clawdbot. Lock down your gateway, fix file permissions, set up auth, configure firewalls. Based on real vulnerability research.
version: 1.0.0
author: NextFrontierBuilds
keywords: moltbot, clawdbot, security, hardening, gateway, firewall, tailscale, ssh, authentication, ai-agent
---

# Moltbot Security Guide

Your Moltbot gateway was designed for local use. When exposed to the internet without proper security, attackers can access your API keys, private messages, and full system access.

**Based on:** Real vulnerability research that found 1,673+ exposed Clawdbot/Moltbot gateways on Shodan.

---

## TL;DR - The 5 Essentials

1. **Bind to loopback** — Never expose gateway to public internet
2. **Set auth token** — Require authentication for all requests
3. **Fix file permissions** — Only you should read config files
4. **Update Node.js** — Use v22.12.0+ to avoid known vulnerabilities
5. **Use Tailscale** — Secure remote access without public exposure

---

## What Gets Exposed (The Real Risk)

When your gateway is publicly accessible:
- Complete conversation histories (Telegram, WhatsApp, Signal, iMessage)
- API keys for Claude, OpenAI, and other providers
- OAuth tokens and bot credentials
- Full shell access to host machine

**Prompt injection attack example:** An attacker sends you an email with hidden instructions. Your AI reads it, extracts your recent emails, and forwards summaries to the attacker. No hacking required.

---

## Quick Security Audit

Run this to check your current security posture:

```bash
clawdbot security audit --deep
```

Auto-fix issues:

```bash
clawdbot security audit --deep --fix
```

---

## Step 1: Bind Gateway to Loopback Only

**What this does:** Prevents the gateway from accepting connections from other machines.

Check your `~/.clawdbot/clawdbot.json`:

```json
{
  "gateway": {
    "bind": "loopback"
  }
}
```

**Options:**
- `loopback` — Only accessible from localhost (most secure)
- `lan` — Accessible from local network only
- `auto` — Binds to all interfaces (dangerous if exposed)

---

## Step 2: Set Up Authentication

**Option A: Token Authentication (Recommended)**

Generate a secure token:

```bash
openssl rand -hex 32
```

Add to your config:

```json
{
  "gateway": {
    "auth": {
      "mode": "token",
      "token": "your-64-char-hex-token-here"
    }
  }
}
```

Or set via environment:

```bash
export CLAWDBOT_GATEWAY_TOKEN="your-secure-random-token-here"
```

**Option B: Password Authentication**

```json
{
  "gateway": {
    "auth": {
      "mode": "password"
    }
  }
}
```

Then:

```bash
export CLAWDBOT_GATEWAY_PASSWORD="your-secure-password-here"
```

---

## Step 3: Lock Down File Permissions

**What this does:** Ensures only you can read sensitive config files.

```bash
chmod 700 ~/.clawdbot
chmod 600 ~/.clawdbot/clawdbot.json
chmod 700 ~/.clawdbot/credentials
```

**Permission meanings:**
- `700` = Only owner can access folder
- `600` = Only owner can read/write file

Or let Clawdbot fix it:

```bash
clawdbot security audit --fix
```

---

## Step 4: Disable Network Broadcasting

**What this does:** Stops Clawdbot from announcing itself via mDNS/Bonjour.

Add to your shell config (`~/.zshrc` or `~/.bashrc`):

```bash
export CLAWDBOT_DISABLE_BONJOUR=1
```

Reload:

```bash
source ~/.zshrc
```

---

## Step 5: Update Node.js

Older Node.js versions have security vulnerabilities. You need **v22.12.0+**.

Check version:

```bash
node --version
```

**Mac (Homebrew):**
```bash
brew update && brew upgrade node
```

**Ubuntu/Debian:**
```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Windows:** Download from [nodejs.org](https://nodejs.org/)

---

## Step 6: Set Up Tailscale (Remote Access)

**What this does:** Creates encrypted tunnel between your devices. Access Clawdbot from anywhere without public exposure.

**Install Tailscale:**

```bash
# Linux
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# Mac
brew install tailscale
```

**Configure Clawdbot for Tailscale:**

```json
{
  "gateway": {
    "bind": "loopback",
    "tailscale": {
      "mode": "serve"
    }
  }
}
```

Now access via your Tailscale network only.

---

## Step 7: Firewall Setup (UFW)

**For cloud servers (AWS, DigitalOcean, Hetzner, etc.)**

**Install UFW:**
```bash
sudo apt update && sudo apt install ufw -y
```

**Set defaults:**
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

**Allow SSH (don't skip!):**
```bash
sudo ufw allow ssh
```

**Allow Tailscale (if using):**
```bash
sudo ufw allow in on tailscale0
```

**Enable:**
```bash
sudo ufw enable
```

**Verify:**
```bash
sudo ufw status verbose
```

⚠️ **Never do this:**
```bash
# DON'T - exposes your gateway publicly
sudo ufw allow 18789
```

---

## Step 8: SSH Hardening

**Disable password auth (use SSH keys):**

```bash
sudo nano /etc/ssh/sshd_config
```

Change:
```
PasswordAuthentication no
PermitRootLogin no
```

Restart:
```bash
sudo systemctl restart sshd
```

---

## Security Checklist

Before deploying:

- [ ] Gateway bound to `loopback` or `lan`
- [ ] Auth token or password set
- [ ] File permissions locked (600/700)
- [ ] mDNS/Bonjour disabled
- [ ] Node.js v22.12.0+
- [ ] Tailscale configured (if remote)
- [ ] Firewall blocking port 18789
- [ ] SSH password auth disabled

---

## Config Template (Secure Defaults)

```json
{
  "gateway": {
    "port": 18789,
    "bind": "loopback",
    "auth": {
      "mode": "token",
      "token": "YOUR_64_CHAR_HEX_TOKEN"
    },
    "tailscale": {
      "mode": "serve"
    }
  }
}
```

---

## Credits

Based on security research by [@NickSpisak_](https://x.com/NickSpisak_) who found 1,673+ exposed gateways on Shodan.

Original article: https://x.com/nickspisak_/status/2016195582180700592

---

## Installation

```bash
clawdhub install NextFrontierBuilds/moltbot-security
```

Built by [@NextXFrontier](https://x.com/NextXFrontier)
