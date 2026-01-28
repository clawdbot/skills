# Moltbot Security Guide

Security hardening for Moltbot/Clawdbot. Lock down your gateway, fix file permissions, set up authentication, configure firewalls.

**Based on real vulnerability research** that found 1,673+ exposed Clawdbot/Moltbot gateways on Shodan.

## Install

**ClawdHub:**
```bash
clawdhub install NextFrontierBuilds/moltbot-security
```

**npm:**
```bash
npm install moltbot-security
```

## The 5 Essentials

1. **Bind to loopback** — Never expose gateway publicly
2. **Set auth token** — Require authentication
3. **Fix file permissions** — Only you read configs
4. **Update Node.js** — v22.12.0+ required
5. **Use Tailscale** — Secure remote access

## Quick Audit

```bash
clawdbot security audit --deep --fix
```

## What Gets Exposed

Without proper security:
- Conversation histories (Telegram, WhatsApp, Signal)
- API keys (Claude, OpenAI)
- OAuth tokens and credentials
- Full shell access

## Secure Config Template

```json
{
  "gateway": {
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

## Credits

Based on research by [@NickSpisak_](https://x.com/NickSpisak_)

---

Built by [@NextXFrontier](https://x.com/NextXFrontier)
