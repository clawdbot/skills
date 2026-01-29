# x-api 🐦

A Clawdbot skill for posting to X (Twitter) using the official API.

## Why This Exists

The excellent [bird CLI](https://github.com/steipete/bird) is great for **reading** Twitter — timeline, mentions, search, etc. But **posting** through bird gets blocked by Twitter's bot detection:

```
❌ Failed to post tweet: Authorization: This request looks like it might be automated.
To protect our users from spam and other malicious activity, we can't complete this action right now.
```

Twitter's internal GraphQL API (what bird uses) aggressively blocks automated posts. The only reliable way to post is through the **official X API** with OAuth 1.0a.

## The Catch

The X API isn't free:
- **Free tier**: 1,500 posts/month, but requires credits (pay-as-you-go)
- **Basic tier**: $100/month for higher limits
- You need to create a Developer account and app at [developer.x.com](https://developer.x.com)

## Installation

Copy the skill to your Clawdbot skills directory:

```bash
cp -r x-api ~/.clawdbot/skills/
cd ~/.clawdbot/skills/x-api/scripts
npm install
```

## Setup

### 1. Get API Credentials

1. Go to https://developer.x.com/en/portal/dashboard
2. Create a Project and App
3. Set App permissions to **Read and Write**
4. Generate keys from "Keys and tokens" tab

### 2. Configure Credentials

**Option A: Environment variables**
```bash
export X_API_KEY="your-api-key"
export X_API_SECRET="your-api-secret"
export X_ACCESS_TOKEN="your-access-token"
export X_ACCESS_SECRET="your-access-token-secret"
```

**Option B: Config file** at `~/.clawdbot/secrets/x-api.json`
```json
{
  "consumerKey": "your-api-key",
  "consumerSecret": "your-api-secret",
  "accessToken": "your-access-token",
  "accessTokenSecret": "your-access-token-secret"
}
```

## Usage

```bash
node ~/.clawdbot/skills/x-api/scripts/x-post.mjs "Your tweet text here"
```

Multi-line tweets work too:
```bash
node ~/.clawdbot/skills/x-api/scripts/x-post.mjs "Line one

Line two

Line three"
```

## Recommended Setup

| Task | Tool |
|------|------|
| **Reading** (timeline, mentions, search) | [bird CLI](https://github.com/steipete/bird) — free, cookie-based |
| **Posting** | This skill — official API, paid |

## License

MIT

---

Built by [Lobster General Intelligence](https://github.com/lobstergeneralintelligence) 🦞
