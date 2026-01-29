---
name: obsidian-plugin
description: Create and develop Obsidian plugins from scratch. Use when building a new Obsidian plugin, scaffolding from the sample-plugin-plus template, or developing plugin features. Covers project setup, manifest configuration, TypeScript development, settings UI, commands, ribbons, modals, and Obsidian API patterns.
---

# Obsidian Plugin Development

Build production-ready Obsidian plugins using the [obsidian-sample-plugin-plus](https://github.com/davidvkimball/obsidian-sample-plugin-plus) template.

## Quick Start: New Plugin

### 1. Create from Template

```bash
# Clone the template (or use GitHub's "Use this template" button)
gh repo create my-plugin --template davidvkimball/obsidian-sample-plugin-plus --public --clone
cd my-plugin

# Or clone directly
git clone https://github.com/davidvkimball/obsidian-sample-plugin-plus.git my-plugin
cd my-plugin
rm -rf .git && git init
```

### 2. Configure Plugin Identity

Update these files with your plugin's info:

**manifest.json:**
```json
{
  "id": "my-plugin",
  "name": "My Plugin",
  "version": "0.0.1",
  "minAppVersion": "1.5.0",
  "description": "What your plugin does",
  "author": "Your Name",
  "authorUrl": "https://yoursite.com",
  "isDesktopOnly": false
}
```

**package.json:** Update `name`, `description`, `author`, `license`.

**README.md:** Replace template content with your plugin's documentation.

### 3. Initialize Development Environment

```bash
pnpm install
pnpm obsidian-dev-skills          # Initialize AI skills
./scripts/setup-ref-links.sh      # Unix
# or: scripts\setup-ref-links.bat  # Windows
```

### 4. Clean Boilerplate

In `src/main.ts`:
- Remove sample ribbon icon, status bar, commands, modal, and DOM event
- Keep the settings tab if needed, or remove it
- Rename `MyPlugin` class to your plugin name

Delete `styles.css` if your plugin doesn't need custom styles.

## Development Workflow

### Build & Test

```bash
pnpm dev      # Watch mode — rebuilds on changes
pnpm build    # Production build
pnpm lint     # Check for issues
pnpm lint:fix # Auto-fix issues
pnpm test     # Run unit tests
```

### Install in Obsidian

Copy build output to your vault:
```bash
# Unix
cp main.js manifest.json styles.css ~/.obsidian/plugins/my-plugin/

# Or create a symlink for development
ln -s $(pwd) ~/.obsidian/plugins/my-plugin
```

Enable the plugin in Obsidian Settings → Community Plugins.

Use [Hot Reload](https://github.com/pjeby/hot-reload) plugin for automatic reloading during development.

## Plugin Architecture

### Entry Point (`src/main.ts`)

```typescript
import { Plugin } from 'obsidian';

export default class MyPlugin extends Plugin {
  settings: MyPluginSettings;

  async onload() {
    await this.loadSettings();
    // Register commands, ribbons, events, views
  }

  onunload() {
    // Cleanup: remove event listeners, views, DOM elements
  }

  async loadSettings() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
  }

  async saveSettings() {
    await this.saveData(this.settings);
  }
}
```

### Settings Pattern

See [references/settings.md](references/settings.md) for the complete settings UI pattern.

### Common Patterns

See [references/patterns.md](references/patterns.md) for:
- Commands (simple, editor, check callbacks)
- Ribbon icons
- Modals
- Events and lifecycle
- File operations
- Editor manipulation

## Constraints

- **No auto-git**: Never run `git commit` or `git push` without explicit approval
- **No eslint-disable**: Fix lint issues properly, don't suppress them
- **No `any` types**: Use proper TypeScript types
- **Sentence case**: UI text uses sentence case (ESLint may false-positive on this — ignore if so)

## Release Checklist

1. Update version in `manifest.json` and `package.json`
2. Update `versions.json` with `"version": "minAppVersion"`
3. Run `pnpm build` — zero errors
4. Run `pnpm lint` — zero issues
5. Create GitHub release with tag matching version (no `v` prefix)
6. Upload: `main.js`, `manifest.json`, `styles.css` (if used)

## References

- [Settings UI](references/settings.md) — Complete settings tab implementation
- [Common Patterns](references/patterns.md) — Commands, modals, events, file operations
- [Obsidian API Docs](https://docs.obsidian.md) — Official documentation
