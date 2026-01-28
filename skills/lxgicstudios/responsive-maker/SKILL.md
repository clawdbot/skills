---
name: responsive-maker
description: Make components responsive with proper breakpoints. Use when your components look terrible on mobile.
---

# Responsive Maker

Your component looks great on desktop. Then someone opens it on their phone and it's a mess. This tool takes your components and adds proper responsive breakpoints. It handles the media queries, flexbox adjustments, and font scaling so your UI works on every screen size.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-responsive src/components/Hero.tsx
```

## What It Does

- Analyzes your component structure and adds responsive breakpoints
- Converts fixed layouts to flexible ones that adapt to screen size
- Adds mobile-first media queries or Tailwind responsive prefixes
- Handles typography scaling, spacing adjustments, and layout reflows
- Preserves your existing styles while adding responsive layers

## Usage Examples

```bash
npx ai-responsive src/components/Hero.tsx
npx ai-responsive src/components/
npx ai-responsive "src/**/*.tsx"
```

## Best Practices

- **Design mobile first** - Start with the smallest screen and add complexity for larger ones
- **Test on real devices** - Emulators miss things. Check on an actual phone.
- **Don't hide content on mobile** - Restructure it instead. Users on phones deserve the same info.

## When to Use This

- Your desktop-only components need to work on mobile
- You're retrofitting responsive design onto an existing project
- A client reported the site looks broken on their phone

## Part of the LXGIC Dev Toolkit

This is one of 110+ free developer tools built by LXGIC Studios. No paywalls, no sign-ups, no API keys on free tiers. Just tools that work.

**Find more:**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- Website: https://lxgic.dev

## Requirements

No install needed. Just run with npx. Node.js 18+ recommended.

## How It Works

Reads your component code, analyzes the layout structure, and generates responsive CSS or Tailwind classes. AI determines the optimal breakpoints and layout adjustments for each screen size.

## License

MIT. Free forever. Use it however you want.