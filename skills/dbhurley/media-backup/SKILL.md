---
name: media-backup
description: Archive Clawdbot conversation media (photos, videos) to a local folder. Works with any sync service (Dropbox, iCloud, Google Drive, OneDrive).
metadata: {"clawdbot":{"env":["MEDIA_BACKUP_DEST"]}}
---

# Media Backup

Simple backup of Clawdbot inbound media to a local folder. No APIs, no OAuth - just file copy.

Works with any cloud sync service since it's just copying to a local folder.

## Setup

Set your destination folder:
```bash
export MEDIA_BACKUP_DEST="$HOME/Dropbox/Clawdbot/media"
# or
export MEDIA_BACKUP_DEST="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Clawdbot/media"  # iCloud
# or  
export MEDIA_BACKUP_DEST="$HOME/Google Drive/Clawdbot/media"
```

Or add to clawdbot config:
```json
{
  "skills": {
    "entries": {
      "media-backup": {
        "env": {
          "MEDIA_BACKUP_DEST": "/path/to/your/folder"
        }
      }
    }
  }
}
```

## Usage

```bash
# Run backup
uv run skills/media-backup/scripts/backup.py

# Dry run (preview only)
uv run skills/media-backup/scripts/backup.py --dry-run

# Custom source/destination
uv run skills/media-backup/scripts/backup.py --source ~/.clawdbot/media/inbound --dest ~/Backups/media

# Check status
uv run skills/media-backup/scripts/backup.py status
```

## How It Works

1. Scans `~/.clawdbot/media/inbound/` for media files
2. Organizes by date: `YYYY-MM-DD/filename.jpg`
3. Tracks archived files by content hash (no duplicates)
4. Your cloud service syncs the folder automatically

## Cron Setup

Run hourly backup:
```
0 * * * * cd ~/clawd && uv run skills/media-backup/scripts/backup.py >> /tmp/media-backup.log 2>&1
```

Or via Clawdbot cron job with task:
```
Run media backup: uv run skills/media-backup/scripts/backup.py
If files archived, reply: 📸 Archived [N] media files
If none, reply: HEARTBEAT_OK
```

## Supported Formats

jpg, jpeg, png, gif, webp, heic, mp4, mov, m4v, webm
