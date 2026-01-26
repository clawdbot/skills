# gcal-pro

> Google Calendar skill for Clawdbot — manage your calendar through natural conversation.

**Pricing:** Free tier (read-only) | Pro $12 one-time (full access)

## Features

### Free Tier
- ✅ View today's events
- ✅ View tomorrow / this week
- ✅ Search events
- ✅ List calendars
- ✅ Find free time slots

### Pro Tier ($12)
- ✅ Everything in Free
- ✅ Create events
- ✅ Quick add (natural language)
- ✅ Update/reschedule events
- ✅ Delete events
- ✅ Morning brief (via Clawdbot cron)

## Installation

### Prerequisites
- Python 3.11+
- Google account
- Clawdbot installed

### Quick Start

1. **Install Python dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Set up Google Cloud:**
   - Follow [docs/GOOGLE_CLOUD_SETUP.md](docs/GOOGLE_CLOUD_SETUP.md)
   - Save `client_secret.json` to `~/.config/gcal-pro/`

3. **Authenticate:**
   ```powershell
   python scripts/gcal_auth.py auth
   ```

4. **Test:**
   ```powershell
   python scripts/gcal_core.py today
   ```

### One-Line Setup (after Google Cloud setup)
```powershell
.\scripts\setup.ps1
```

## Usage

### View Schedule
```bash
# Today's events
python scripts/gcal_core.py today

# Tomorrow
python scripts/gcal_core.py tomorrow

# This week
python scripts/gcal_core.py week

# Search
python scripts/gcal_core.py search -q "meeting"
```

### Create Events (Pro)
```bash
# Natural language
python scripts/gcal_core.py quick -q "Lunch with Alex Friday noon at Cafe Roma"
```

### Find Free Time
```bash
python scripts/gcal_core.py free
```

### Morning Brief
```bash
python scripts/gcal_core.py brief
```

## File Structure
```
gcal-pro/
├── SKILL.md              # Clawdbot skill definition
├── README.md             # This file
├── requirements.txt      # Python dependencies
├── PLAN.md               # Product plan & roadmap
├── scripts/
│   ├── gcal_auth.py      # OAuth authentication
│   ├── gcal_core.py      # Calendar operations
│   └── setup.ps1         # Windows setup script
├── docs/
│   └── GOOGLE_CLOUD_SETUP.md
└── references/
    └── (API docs, examples)
```

## Configuration

Config files are stored in `~/.config/gcal-pro/`:

| File | Purpose |
|------|---------|
| `client_secret.json` | OAuth app credentials (you provide) |
| `token.json` | Your access token (auto-generated) |
| `license.json` | Pro license (if purchased) |

## Clawdbot Integration

### As a Skill
Copy to your Clawdbot skills directory or reference directly.

### Morning Brief Cron
Set up in Clawdbot:
```
Schedule: 0 8 * * * (8 AM daily)
Command: python /path/to/gcal-pro/scripts/gcal_core.py brief
```

## Troubleshooting

### "client_secret.json not found"
Complete Google Cloud setup and save credentials to `~/.config/gcal-pro/`

### "Token refresh failed"
Re-authenticate: `python scripts/gcal_auth.py auth --force`

### "Access blocked: unverified app"
During testing, click "Advanced" → "Go to gcal-pro (unsafe)"

### "requires Pro tier"
Write operations need Pro license. View operations are free.

## License

Proprietary. Free tier for personal use. Pro license required for write operations.

## Support

- Issues: [GitHub Issues]
- Upgrade to Pro: [Gumroad Link]

---

Built for [Clawdbot](https://clawd.bot) by Bilal
