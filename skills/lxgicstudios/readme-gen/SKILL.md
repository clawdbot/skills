---
name: readme-gen
description: Generate beautiful README.md files with badges, install instructions, and API docs. Use when starting new projects.
---

# README Gen

Your project has no README. Or worse, it has one that says "TODO: write readme". This tool generates complete README files from your codebase. Badges, installation steps, API documentation, examples. A README that makes people actually want to use your project.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-readme
```

## What It Does

- Generates a complete README from your project structure
- Adds appropriate badges (npm, license, build status)
- Creates installation instructions for your package manager
- Documents your API based on exports
- Includes usage examples from your code or tests

## Usage Examples

```bash
# Generate README for current project
npx ai-readme

# Specify output file
npx ai-readme --output README.md

# Include specific sections
npx ai-readme --sections intro,install,api,examples

# Generate for a CLI tool
npx ai-readme --type cli
```

## Best Practices

- **Run at project start** - Easier to maintain a README than to write one from scratch later
- **Customize the intro** - AI writes decent intros but your voice is better
- **Add real examples** - Generated examples are generic. Show your actual use cases.
- **Keep badges minimal** - Nobody needs 15 badges. Pick the 3-5 that matter.

## When to Use This

- Starting a new open source project
- Publishing a package to npm
- Your README is embarrassingly empty
- Restructuring a project and need fresh docs

## Part of the LXGIC Dev Toolkit

This is one of 110+ free developer tools built by LXGIC Studios. No paywalls, no sign-ups, no API keys on free tiers. Just tools that work.

**Find more:**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- Website: https://lxgic.dev

## Requirements

No install needed. Just run with npx. Node.js 18+ recommended.

```bash
npx ai-readme --help
```

## How It Works

The tool reads your package.json, analyzes your source files for exports and CLI commands, checks for existing docs or examples, then generates a structured README with all the sections a good project needs.

## License

MIT. Free forever. Use it however you want.
