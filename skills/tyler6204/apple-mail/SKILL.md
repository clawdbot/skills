---
name: apple-mail
description: Apple Mail.app integration for macOS. Read inbox, search emails (fast SQLite or AppleScript), send emails, reply, and manage messages. Use when asked to check email, find emails, send emails, or interact with Mail.app.
metadata: {"clawdbot":{"emoji":"📧","os":["darwin"],"requires":{"bins":["sqlite3"]}}}
---

# Apple Mail

Interact with Mail.app on macOS via AppleScript + optional fast SQLite search.

## Requirements
- Mail.app configured with account(s)
- Automation permission for terminal to control Mail.app

## Commands

Run scripts from skill directory: `cd {baseDir}`

### List Recent Emails
```bash
scripts/mail-list.sh [mailbox] [account] [limit]
# Examples:
scripts/mail-list.sh                           # List 10 recent from INBOX (all accounts)
scripts/mail-list.sh INBOX Google 20           # List 20 from Google INBOX
scripts/mail-list.sh "[Gmail]/Spam" Google 10  # Gmail special folders need [Gmail]/ prefix
```
⚠️ **Empty mailboxes (0 messages) may hang indefinitely** - avoid listing folders like Starred if they might be empty.

### Search Emails (AppleScript - Recommended)
```bash
scripts/mail-search.sh "query" [mailbox] [limit]
# Safe to use while Mail.app is running
# Examples:
scripts/mail-search.sh "invoice" INBOX 20
scripts/mail-search.sh "amazon.com"
```

### Read Email by ID
```bash
scripts/mail-read.sh <message-id>
# Returns full email content including body
```

### Send Email
```bash
scripts/mail-send.sh "to@email.com" "Subject" "Body" [from-account] [attachment]
# Examples:
scripts/mail-send.sh "friend@gmail.com" "Hey" "What's up?"
scripts/mail-send.sh "work@co.com" "Report" "See attached." "" "/path/file.pdf"
```

### Reply to Email
```bash
scripts/mail-reply.sh <message-id> "Reply body" [reply-all]
# reply-all: true/false (default: false)
```

### List Accounts
```bash
scripts/mail-accounts.sh
```

### List Mailboxes
```bash
scripts/mail-mailboxes.sh [account]
```

---

## ⚠️ Fast Search (SQLite - REQUIRES MAIL QUIT)

> **DATABASE CORRUPTION WARNING**: The fast search script directly queries Mail's SQLite database. 
> Using it while Mail.app is running **can corrupt Mail's Envelope Index** due to WAL locking conflicts.
> **Always fully quit Mail.app before using this command** (Cmd+Q, not just closing windows).

```bash
# ONLY use when Mail.app is QUIT - script will refuse to run if Mail is open
scripts/mail-fast-search.sh "query" [limit]
# ~50ms search vs minutes with AppleScript
```

### Why this matters
- Mail.app uses SQLite with Write-Ahead Logging (WAL mode)
- Concurrent reads from external processes can cause locking conflicts
- Database corruption may result in lost emails, broken search, or Mail refusing to open
- Recovery requires rebuilding the mail index or restoring from backup

### When to use
- **Use mail-search.sh** (AppleScript): Always safe, works while Mail is running
- **Use mail-fast-search.sh** (SQLite): Only when you need speed AND Mail is quit

---

## Performance Notes

| Method | Time | Safe while Mail running? |
|--------|------|--------------------------|
| AppleScript (mail-search.sh) | Minutes | ✅ Yes - always safe |
| SQLite (mail-fast-search.sh) | ~50ms | ⛔ NO - quit Mail first |

## Output Format

List and search commands return pipe-delimited rows:
```
ID | ReadStatus | Date | Sender | Subject
```
- **ID**: Internal message ID (use with mail-read.sh)
- **ReadStatus**: `●` = unread, blank = read
- **Date**: Full timestamp in local format
- **Sender**: Name + email
- **Subject**: Email subject line

Example:
```
1405 |   | Tuesday, January 13, 2026 at 21:18:03 | Mail Delivery <mailer@google.com> | Delivery Status
1977 | ● | Tuesday, January 13, 2026 at 20:18:50 | Tinder <tinder@mail.tinder.com> | New match!
```

## Notes
- Message IDs are internal Mail.app IDs returned by list/search commands
- Confirm recipient and content before sending
- Fast search is metadata only - use mail-read.sh to get full body

## Error Handling

### Common error messages
| Message | Cause |
|---------|-------|
| `⛔ ERROR: Mail.app is running` | Quit Mail.app before using mail-fast-search.sh |
| `Message not found with ID: X` | Invalid or deleted message ID - get fresh IDs from mail-list.sh |
| `No emails found matching: X` | Search query matched nothing |
| `Usage: ...` | Missing required arguments |
| `Can't get mailbox "X" (-1728)` | Mailbox doesn't exist - check mail-mailboxes.sh for exact names |
| `Can't get account "X" (-1728)` | Account doesn't exist - check mail-accounts.sh for exact names |
| `Invalid index (-1719)` | Mailbox is empty or has fewer messages than requested limit |
| `Error: Mail database not found` | Mail.app database not found or wrong location - ensure Mail.app has synced |

### Script validation
| Script | Required args | Optional args |
|--------|---------------|---------------|
| mail-read.sh | message-id | - |
| mail-reply.sh | message-id, body | reply-all (true/false) |
| mail-search.sh | query | mailbox, limit |
| mail-send.sh | to, subject, body | from-account, attachment |

### Gotchas
- **Empty mailboxes can hang** - Listing a mailbox with 0 messages (like Starred or empty folders) may hang indefinitely. Check mailbox count first if unsure.
- **Invalid mailbox = silent failure** - `mail-search.sh` returns "No emails found" for non-existent mailbox names instead of an error. Always verify mailbox names with `mail-mailboxes.sh` if search returns nothing.
- **SQLite search requires Mail quit** - mail-fast-search.sh refuses to run if Mail.app is open to prevent database corruption
- **AppleScript search is slower but safer** - mail-search.sh can take minutes on large mailboxes but is always safe
- **Message IDs expire** - IDs from old list/search results may no longer exist; always get fresh IDs
- **Non-numeric IDs fail gracefully** - scripts handle invalid ID formats without crashing
- **Empty body now rejected** - mail-send.sh requires all 3 args (to, subject, body)
- **Gmail mailboxes need prefix** - Use `[Gmail]/Spam`, `[Gmail]/Sent Mail` syntax for special Gmail folders (not just `Spam`)
- **Invalid mailbox/account errors** - AppleScript returns error (-1728) for non-existent mailboxes or accounts
- **Empty search results** - mail-fast-search.sh returns no output (not even headers) when nothing matches
- **SQL wildcards in fast-search** - `%` in query acts as SQL LIKE wildcard; avoid special chars in queries
- **macOS database variations** - Envelope Index database location and schema varies by macOS version; script auto-detects

---

## ⚠️ Gmail Mailbox Naming (Important!)

**`mail-mailboxes.sh` shows Gmail folders WITHOUT the `[Gmail]/` prefix, but you MUST use the prefix to access them!**

This is confusing but intentional - Mail.app's AppleScript interface requires the full path.

### What you see vs what you use:

| mail-mailboxes.sh shows | You must use |
|-------------------------|--------------|
| `Spam` | `[Gmail]/Spam` |
| `Sent Mail` | `[Gmail]/Sent Mail` |
| `All Mail` | `[Gmail]/All Mail` |
| `Trash` | `[Gmail]/Trash` |
| `Drafts` | `[Gmail]/Drafts` |
| `Starred` | `[Gmail]/Starred` |
| `Important` | `[Gmail]/Important` |

### Examples:
```bash
# ❌ WRONG - will error
scripts/mail-list.sh "Spam" Google 5
scripts/mail-list.sh "Sent Mail" Google 5

# ✅ CORRECT - works
scripts/mail-list.sh "[Gmail]/Spam" Google 5
scripts/mail-list.sh "[Gmail]/Sent Mail" Google 5

# Custom labels work as-is (no prefix needed)
scripts/mail-list.sh "Work" Google 5
scripts/mail-list.sh "Receipts" Google 5
```

### Other providers (Yahoo, iCloud, etc.)
Non-Gmail accounts work without special prefixes:
```bash
scripts/mail-list.sh "Junk" "Yahoo!" 5      # Works
scripts/mail-list.sh "Sent Messages" "Yahoo!" 5  # Works
```

### Search with invalid mailbox
**`mail-search.sh` silently returns "No emails found" for invalid mailbox names** instead of an error. If your search returns nothing, verify the mailbox name exists.
