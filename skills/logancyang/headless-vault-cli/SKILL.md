---
name: headless-vault-cli
description: Read and edit Markdown notes on your personal computer via SSH tunnel. Use when the user asks to read, create, or append to notes in their vault.
homepage: https://github.com/logancyang/headless-vault-cli
metadata: {"moltbot":{"emoji":"🗄️"}}
---

# Headless Vault CLI

Access Markdown notes on your personal computer from this VPS-hosted Moltbot via SSH tunnel.

**Terminology**: "Local machine" = your personal computer (macOS or Linux) where your notes live. This skill runs on the VPS and connects to your machine via a reverse SSH tunnel.

## Available Commands

You have access to these commands ONLY. Do not attempt commands not listed here (no rename, delete, move, or edit commands exist).

| Command | Description |
|---------|-------------|
| `tree` | List vault directory structure |
| `resolve` | Find note by path or title |
| `info` | Get file metadata (lines, bytes, sha256, mtime) |
| `read` | Read note content |
| `create` | Create a NEW note (fails if file exists) |
| `append` | Append content to EXISTING note |
| `set-root` | Set vault root directory |

## How to Run Commands

All commands are executed via SSH:
```bash
ssh -4 -p ${VAULT_SSH_PORT:-2222} ${VAULT_SSH_USER}@${VAULT_SSH_HOST:-localhost} vaultctl <command> [args]
```

Always use `-4` to force IPv4 (avoids IPv6 timeout issues).

## Command Reference

### tree - List vault structure
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree --depth 2
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree --all
```
Options:
- `--depth N` - Maximum depth to traverse
- `--all` - Include all files, not just .md

### resolve - Find note by path or title
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl resolve --title "Meeting Notes"
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl resolve --path "Projects/Plan.md"
```

**For paths/titles with spaces**, use `--base64`:
```bash
# echo -n "My Meeting Notes" | base64 → TXkgTWVldGluZyBOb3Rlcw==
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl resolve --title TXkgTWVldGluZyBOb3Rlcw== --base64
```

### info - Get file metadata
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl info "Projects/Plan.md"
```
Returns JSON: `{"path": "...", "lines": N, "bytes": N, "sha256": "...", "mtime": N}`

**For paths with spaces**, use `--base64`:
```bash
# echo -n "Notes/My File.md" | base64 → Tm90ZXMvTXkgRmlsZS5tZA==
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl info Tm90ZXMvTXkgRmlsZS5tZA== --base64
```

### read - Read note content
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl read "Projects/Plan.md"
```
Returns JSON: `{"path": "...", "content": "..."}`

**For paths with spaces**, use `--base64`:
```bash
# echo -n "Notes/My File.md" | base64 → Tm90ZXMvTXkgRmlsZS5tZA==
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl read Tm90ZXMvTXkgRmlsZS5tZA== --base64
```

### create - Create a NEW note
**IMPORTANT**: Use `--base64` flag with BOTH path AND content base64 encoded. This is required for paths/content with spaces or special characters.

```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl create <base64_path> <base64_content> --base64
```

Example to create "Notes/Morning Brief.md" with content "# Hello\n\nWorld":
```bash
# Encode path: echo -n "Notes/Morning Brief.md" | base64 → Tm90ZXMvTW9ybmluZyBCcmllZi5tZA==
# Encode content: echo -n "# Hello\n\nWorld" | base64 → IyBIZWxsbwoKV29ybGQ=
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl create Tm90ZXMvTW9ybmluZyBCcmllZi5tZA== IyBIZWxsbwoKV29ybGQ= --base64
```

- Creates parent directories automatically
- Fails if file already exists (use `append` to add to existing files)
- File must have `.md` extension
- **NEVER duplicate the title as a heading inside the note content** (e.g., for "My Note.md", don't start content with "# My Note")

### append - Append to EXISTING note
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl append <base64_path> <base64_content> --base64
```

- Fails if file does not exist (use `create` for new files)

### set-root - Set vault root directory
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl set-root /path/to/vault
```

## What You CANNOT Do

These operations are NOT supported:
- **Rename** files or folders
- **Delete** files or folders
- **Move** files between folders
- **Edit** specific parts of a file (only append to end)
- **Create** folders without a file (folders are created automatically with `create`)

## Environment Variables

Auto-configured by tunnel-setup.sh:
- `VAULT_SSH_USER` - Local machine username (auto-detected)
- `VAULT_SSH_PORT` - Tunnel port (default: 2222)
- `VAULT_SSH_HOST` - Tunnel host (default: localhost)

## Tips

- Always run `vaultctl tree` first to see what notes exist
- Use `vaultctl resolve --title "..."` to find a note by name
- All output is JSON
- The local machine must be online with tunnel running
- **For paths with spaces**: Use `--base64` flag with base64-encoded path (works for `read`, `info`, `create`, `append`)

## Examples

**Important**: Always run `tree` first if you're unsure what notes exist. This prevents errors from wrong paths or duplicate names.

### Example 1: User asks to read a note (check first)
User: "Show me my project plan"

Step 1 - Check what exists:
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree
```
Output:
```json
{"tree": [{"path": "Projects", "type": "dir"}, {"path": "Projects/Plan.md", "type": "file"}]}
```

Step 2 - Now read the correct path:
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl read "Projects/Plan.md"
```
Output:
```json
{"path": "Projects/Plan.md", "content": "# Project Plan\n\n## Goals\n..."}
```

### Example 2: User asks to create a note (check first to avoid duplicates)
User: "Create a meeting notes file"

Step 1 - Check what already exists:
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree
```
Output:
```json
{"tree": [{"path": "Projects", "type": "dir"}, {"path": "Projects/Plan.md", "type": "file"}]}
```

Step 2 - No "Meeting Notes" exists, safe to create (do NOT duplicate title as heading):
```bash
# echo -n "Meeting Notes.md" | base64 → TWVldGluZyBOb3Rlcy5tZA==
# echo -n "## Agenda\n\n- Item 1\n- Item 2\n" | base64 → IyMgQWdlbmRhCgotIEl0ZW0gMQotIEl0ZW0gMgo=
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl create TWVldGluZyBOb3Rlcy5tZA== IyMgQWdlbmRhCgotIEl0ZW0gMQotIEl0ZW0gMgo= --base64
```
Output:
```json
{"status": "ok", "path": "Meeting Notes.md"}
```

### Example 3: User asks about vault contents
User: "What's in my notes?"

```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree --depth 2
```
Output:
```json
{"tree": [{"path": "Projects", "type": "dir"}, {"path": "Projects/Plan.md", "type": "file"}, {"path": "Ideas.md", "type": "file"}]}
```

Then summarize for user: "You have a Projects folder with Plan.md, and an Ideas.md file at the root."

### Example 4: Complex workflow with source and output notes
User: "According to the source note 'AI Digest Sources.md', browse the sources and output the digest to 'digest/2025-01-28-digest.md'"

Step 1 - Check what exists:
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree
```
Output:
```json
{"tree": [{"path": "AI Digest Sources.md", "type": "file"}, {"path": "digest", "type": "dir"}, {"path": "digest/2025-01-27-digest.md", "type": "file"}]}
```

Step 2 - Validate:
- Source "AI Digest Sources.md" exists ✓
- Output "digest/2025-01-28-digest.md" does NOT exist → will use `create`

(If source didn't exist: STOP and ask user "I couldn't find 'AI Digest Sources.md'. Did you mean one of these: [list alternatives]?")

(If output already existed: use `append` instead of `create`)

Step 3 - Read the source note:
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl read "AI Digest Sources.md"
```
Output:
```json
{"path": "AI Digest Sources.md", "content": "# AI Digest Sources\n\n- https://example.com/article1\n- https://example.com/article2\n"}
```

Step 4 - Browse sources and generate digest content (done by bot outside this skill)

Step 5 - Write output to vault (do NOT duplicate title as heading):
```bash
# echo -n "digest/2025-01-28-digest.md" | base64 → ZGlnZXN0LzIwMjUtMDEtMjgtZGlnZXN0Lm1k
# echo -n "## Summary\n\nKey points from today's sources...\n" | base64 → IyMgU3VtbWFyeQoKS2V5IHBvaW50cyBmcm9tIHRvZGF5J3Mgc291cmNlcy4uLgo=
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl create ZGlnZXN0LzIwMjUtMDEtMjgtZGlnZXN0Lm1k IyMgU3VtbWFyeQoKS2V5IHBvaW50cyBmcm9tIHRvZGF5J3Mgc291cmNlcy4uLgo= --base64
```

(If output already existed, use `append` instead:)
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl append ZGlnZXN0LzIwMjUtMDEtMjgtZGlnZXN0Lm1k IyMgVXBkYXRlCi4uLg== --base64
```
