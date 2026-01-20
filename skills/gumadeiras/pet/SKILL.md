---
name: pet
description: Simple command-line snippet manager. Use it to save and reuse complex commands.
metadata: {"clawdbot":{"emoji":"🐘","requires":{"bins":["pet"]}}}
---

# pet (Simple Command-Line Snippet Manager)

Pet acts as a CLI snippet manager. It helps you save complex commands and reuse them.

## Usage

### Create a new snippet
```bash
pet new
```
This opens an editor. Enter the command and a description.
Format:
```toml
[[snippets]]
  command = "echo 'hello'"
  description = "say hello"
  output = ""
```

### Search and List snippets
```bash
pet search
```

### Execute a snippet directly
```bash
pet exec
```

### Sync with Gist (Optional)
If configured in `~/.config/pet/config.toml`, you can sync snippets to a GitHub Gist:
```bash
pet sync
```

## Storage
Snippets are stored in `~/.config/pet/snippet.toml`.
