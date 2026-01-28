---
name: component-gen
description: Generate React components from plain English descriptions. Use when you need UI components fast.
---

# Component Gen

Starting a new React component from scratch is tedious. You know what you want, a card with an image, title, and action buttons, but setting up the boilerplate takes longer than it should. This tool takes a plain English description and generates a complete React component. TypeScript, Tailwind, whatever you need.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-component "a pricing card with plan name, price, features list, and CTA button"
```

## What It Does

- Generates complete React components from plain English descriptions
- Optional TypeScript output with proper type annotations
- Tailwind CSS support with the --tailwind flag
- Can write directly to a file or print to stdout
- Produces clean, production-ready component code

## Usage Examples

```bash
# Generate a basic component
npx ai-component "a pricing card with plan name, price, features list, and CTA button"

# Generate with TypeScript
npx ai-component "a user profile dropdown with avatar, name, and logout" -t

# Generate with Tailwind and save to file
npx ai-component "a responsive navbar with logo, links, and mobile menu" --tailwind -o Navbar.tsx
```

## Best Practices

- **Be descriptive about layout** - The more specific you are about positioning and styling, the better the component looks
- **Use TypeScript for real projects** - The -t flag gives you proper types and interfaces
- **Pair with Tailwind** - The --tailwind flag produces much cleaner markup than inline styles
- **Iterate on the output** - Generate the base component, then tweak it. Faster than writing from scratch.

## When to Use This

- Prototyping a new feature and need a quick component skeleton
- Building a design system and want consistent starting points
- Learning React patterns by seeing how components should be structured
- Hackathons and MVPs where speed matters more than perfection

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
npx ai-component --help
```

## How It Works

The tool takes your description and sends it to an AI model that understands React patterns and component architecture. It generates a complete, functional component with proper structure, styling, and any requested features.

## License

MIT. Free forever. Use it however you want.