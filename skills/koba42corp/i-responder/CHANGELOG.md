# Recent Changes - v1.1.0

## What's New

### 🔑 Keyword Triggers
Only respond when messages contain specific words (e.g., "help", "urgent", "emergency")
- Add: `/autorespond_add_keyword +15551234567 help`
- Remove: `/autorespond_remove_keyword +15551234567 help`
- Clear: `/autorespond_clear_keywords +15551234567`
- Case-insensitive matching

### ⏰ Time Windows
Restrict auto-responses to specific hours (e.g., only respond 9 AM - 10 PM)
- Set: `/autorespond_set_time_window +15551234567 09:00 22:00`
- Clear: `/autorespond_clear_time_windows +15551234567`
- Multiple windows per contact supported

### 📊 Statistics Tracking
Track response activity per contact
- Total responses (all-time)
- Daily count (resets at midnight)
- Average per day
- View: `/autorespond_stats` or `/autorespond_stats +15551234567`

### 🚦 Daily Reply Cap
Limit max replies per day per contact (prevents spam)
- Set: `/autorespond_set_daily_cap +15551234567 10`
- Set to 0 for unlimited
- Automatically resets at midnight

## Bug Fixes

- Fixed race condition that could cause duplicate responses
- Added processing locks to prevent multiple simultaneous replies
- Auto-cleanup of stale locks on watcher restart

## Documentation

- Enhanced README.md with professional markdown formatting
- Added shields/badges and better visual structure
- Improved command reference tables
- Added troubleshooting section
