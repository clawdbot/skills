---
name: ci-gen
description: Generate GitHub Actions CI/CD workflows from project analysis. Use when setting up automated pipelines.
---

# CI/CD Workflow Generator

Point this at any project and get a working GitHub Actions workflow. It scans your codebase, detects the stack, and generates a pipeline that actually makes sense for your setup.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-ci ./my-project
```

## What It Does

- Scans your project to detect framework, language, and dependencies
- Generates GitHub Actions workflow with proper build and test steps
- Includes caching for faster CI runs
- Sets up deployment steps based on common platforms
- Creates separate workflows for PRs vs main branch pushes

## Usage Examples

```bash
# Analyze current directory
npx ai-ci .

# Generate for a specific project
npx ai-ci ./apps/frontend

# Include deployment to Vercel
npx ai-ci . --deploy vercel
```

## Best Practices

- **Review the output** - AI generates good defaults but tweak for your exact needs
- **Start with tests only** - Get CI green first, add deployment later
- **Use secrets properly** - The workflow references secrets, make sure to add them in GitHub
- **Keep it simple** - Don't overcomplicate your first pipeline

## When to Use This

- Starting a new project and need CI fast
- Migrating from another CI system to GitHub Actions
- Learning GitHub Actions syntax through real examples
- Standardizing CI across multiple repos

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
npx ai-ci --help
```

## How It Works

The tool uses glob patterns to scan your project structure. It identifies package.json, requirements.txt, Dockerfile, and other config files to understand your stack. Then it generates a workflow YAML tailored to what it found.

## License

MIT. Free forever. Use it however you want.
