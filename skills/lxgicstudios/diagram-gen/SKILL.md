---
name: diagram-gen
description: Generate Mermaid diagrams from your codebase. Use when you need architecture visualizations.
---

# Diagram Generator

Architecture diagrams are always out of date because nobody maintains them. This tool reads your code and generates accurate Mermaid diagrams automatically.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-diagram ./src/
```

## What It Does

- Generates Mermaid diagrams from your code
- Supports flowcharts, class diagrams, sequence diagrams
- Creates ER diagrams from database schemas
- Outputs markdown-compatible Mermaid syntax

## Usage Examples

```bash
# Generate flowchart
npx ai-diagram ./src/

# Class diagram
npx ai-diagram ./src/ --type class -o architecture.mmd

# Sequence diagram of function calls
npx ai-diagram ./src/ --type sequence

# Entity relationship diagram
npx ai-diagram ./src/ --type er
```

## Best Practices

- **Pick the right diagram type** - use class for OOP, flow for processes
- **Focus on key modules** - don't diagram everything
- **Keep them updated** - run periodically as code changes
- **Add to docs** - Mermaid renders in GitHub markdown

## When to Use This

- Onboarding new team members
- Documentation that's always out of date
- Understanding unfamiliar codebases
- Architecture reviews and planning

## Part of the LXGIC Dev Toolkit

This is one of 110+ free developer tools built by LXGIC Studios. No paywalls, no sign-ups, no API keys on free tiers. Just tools that work.

**Find more:**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- Website: https://lxgicstudios.com

## Requirements

No install needed. Just run with npx. Node.js 18+ recommended. Needs OPENAI_API_KEY environment variable.

```bash
npx ai-diagram --help
```

## How It Works

Reads your source files to understand the structure, relationships, and data flow. Then generates Mermaid syntax that renders as diagrams in markdown editors, GitHub, and documentation tools.

## License

MIT. Free forever. Use it however you want.
