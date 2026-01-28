---
name: readme-writer
description: Generate polished README.md files from your codebase. Use when you need docs fast.
---

# README Writer

Writing a good README is one of those things everyone puts off. You know it matters, but staring at a blank file after finishing your code is painful. This tool reads your project and writes a real README with badges, install steps, usage examples, and API docs. Just point it at a directory and you're done.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-readme
```

## What It Does

- Scans your project directory and reads package.json, source files, and existing docs
- Generates a full README with badges, installation instructions, and usage examples
- Includes API documentation pulled from your actual code
- Writes directly to README.md or any output file you specify
- Works with any Node.js project out of the box

## Usage Examples

```bash
# Generate README for current directory
npx ai-readme

# Generate for a specific project
npx ai-readme ./my-project

# Write to a custom file
npx ai-readme --output DOCS.md
```

## Best Practices

- **Run it early** - Don't wait until your project is done. Generate a README while the code is fresh in your mind, then tweak it.
- **Review the output** - It's good but it's not psychic. Check that examples actually work and descriptions match what your code does.
- **Commit the result** - Treat the generated README like real code. Version it, update it when things change.
- **Use it on existing projects** - Got an old repo with no docs? This is the fastest way to fix that.

## When to Use This

- You just finished a project and need docs before publishing to npm
- You inherited a repo with zero documentation
- You want a starting point that's better than a blank file
- Open source projects that need a professional first impression

## How It Works

The tool walks your project directory and picks up signals from package.json, source files, and any existing documentation. It sends that context to an AI model that understands code structure and generates markdown formatted as a proper README. Output goes straight to a file.

## Requirements

No install needed. Just run with npx. Node.js 18+ recommended.

```bash
npx ai-readme --help
```

## Part of the LXGIC Dev Toolkit

This is one of 110+ free developer tools built by LXGIC Studios. No paywalls, no sign-ups, no API keys on free tiers. Just tools that work.

**Find more:**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- Website: https://lxgic.dev

## License

MIT. Free forever. Use it however you want.