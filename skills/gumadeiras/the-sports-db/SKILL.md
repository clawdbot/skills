---
name: the-sports-db
description: Access sports data via TheSportsDB (teams, events, scores).
metadata: {"clawdbot":{"emoji":"🏟️","requires":{"env":["THE_SPORTS_DB_KEY"]}}}
---

# TheSportsDB

Free sports database.

## Configuration
Ensure `THE_SPORTS_DB_KEY` is set in `~/.clawdbot/.env`. (Default test key is often `123` or `3`).

## Usage

### Search Team
```bash
curl -s "https://www.thesportsdb.com/api/v1/json/$THE_SPORTS_DB_KEY/searchteams.php?t=Palmeiras"
```

### Last Events (Scores)
Get last 5 events for a team ID:
```bash
curl -s "https://www.thesportsdb.com/api/v1/json/$THE_SPORTS_DB_KEY/eventslast.php?id=134465"
```

### Next Events (Fixtures)
Get next 5 events for a team ID:
```bash
curl -s "https://www.thesportsdb.com/api/v1/json/$THE_SPORTS_DB_KEY/eventsnext.php?id=134465"
```

**Note:** Rate limit is 30 requests/minute.
