# Security & Privacy

## Data Storage

**Local Storage Only:**
- All Oura data is stored locally in `~/.oura-analytics/cache/`
- No data is sent to third-party services
- Cache files are stored as JSON: `cache/{endpoint}/{date}.json`

**What's Cached:**
- Sleep, readiness, and activity data per day
- Sync state tracking (last sync timestamps)
- No personally identifiable information beyond what Oura provides

**Cache Location:**
```
~/.oura-analytics/
├── cache/
│   ├── sleep/2026-01-20.json
│   ├── daily_readiness/2026-01-20.json
│   └── daily_activity/2026-01-20.json
└── sync_state.json
```

## API Token Security

**Token Storage:**
- Your Oura API token must be set via environment variable: `OURA_API_TOKEN`
- **NEVER** commit tokens to git
- **NEVER** log tokens or include them in output
- Store in `~/.bashrc`, `~/.zshrc`, or secure credential manager

**Get Your Token:**
1. Visit: https://cloud.ouraring.com/personal-access-token
2. Generate a Personal Access Token
3. Set environment variable:
   ```bash
   export OURA_API_TOKEN="your_token_here"
   ```

**Token Rotation:**
To rotate your token:
1. Generate new token at https://cloud.ouraring.com/personal-access-token
2. Update `OURA_API_TOKEN` environment variable
3. Restart any running scripts/cron jobs
4. Revoke old token in Oura Cloud dashboard

**Token Permissions:**
- Read-only access to your Oura data
- No write or delete permissions
- Token can be revoked at any time from Oura Cloud

## What's Never Logged

**The skill NEVER logs:**
- Your Oura API token
- Raw API responses (unless explicitly debugging)
- Personally identifiable information
- Location data or GPS coordinates

**Safe to Log:**
- Aggregated metrics (sleep scores, averages)
- Date ranges and timestamps
- Cache hit/miss statistics
- Error messages (sanitized)

## Data Retention

**Cache Retention:**
- Cached data persists indefinitely until manually cleared
- Clear cache: `python scripts/oura_api.py cache --clear`
- Clear specific endpoint: `python scripts/oura_api.py cache --clear --endpoint sleep`

**No Automatic Deletion:**
- Cache files are never automatically deleted
- You control when and what data is removed

## Privacy Best Practices

**For Clawdbot Integration:**
1. Store `OURA_API_TOKEN` in `~/.clawdbot/.env` (git-ignored)
2. Use `--format brief` or `--format alert` to minimize data in logs
3. Use `--format silent` for cron jobs (exit code only, no output)
4. Never share cache files publicly (contains your health data)

**For Manual Use:**
1. Set token in shell profile (`~/.bashrc` or `~/.zshrc`)
2. Use `--no-cache` flag for sensitive queries (no local storage)
3. Clear cache periodically if concerned about disk usage
4. Review cache files before sharing terminal output

## Reporting Security Issues

If you discover a security vulnerability:
1. **DO NOT** open a public GitHub issue
2. Email: martin@shapescale.com with "Oura Analytics Security" subject
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

## Compliance

**GDPR Compliance:**
- You own your data (local storage only)
- You control data retention (manual cache clearing)
- No data sharing with third parties
- Right to deletion (clear cache anytime)

**HIPAA Note:**
- This skill is NOT HIPAA-compliant
- Do not use for medical decision-making
- Consult healthcare professionals for health concerns
