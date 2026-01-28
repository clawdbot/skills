---
name: license-gen
description: Pick and generate the right license for your project. Use when licensing open source.
---

# License Generator

Picking a license shouldn't require a law degree. This tool explains each license in plain English and generates the LICENSE file for you.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-license
```

## What It Does

- Interactive license selection with explanations
- Generates complete LICENSE files
- Explains what each license actually means
- Covers MIT, Apache, GPL, BSD, and more

## Usage Examples

```bash
# Interactive mode
npx ai-license

# Quick MIT license
npx ai-license --type mit --name "Jane Doe"

# Explain a license before choosing
npx ai-license --explain apache-2.0
```

## Best Practices

- **MIT for simplicity** - do whatever you want, just keep the copyright
- **Apache for patents** - includes patent protection
- **GPL for copyleft** - derivatives must also be open source
- **Check dependencies** - some licenses are incompatible

## When to Use This

- Starting an open source project
- Not sure which license fits your needs
- Want to understand license implications
- Need to generate LICENSE file quickly

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
npx ai-license --help
```

## How It Works

Walks you through questions about how you want your code to be used, then recommends appropriate licenses. Uses GPT-4o-mini to explain license terms in plain English and generate the full LICENSE file.

## License

MIT. Free forever. Use it however you want.
