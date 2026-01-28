---
name: a11y-auditor
description: Scan HTML and JSX for accessibility issues and get fix suggestions. Use when you need to catch WCAG violations before they hit production.
---

# Accessibility Auditor

Accessibility isn't optional but checking for it manually is painful. This tool scans your HTML and JSX files for WCAG violations and tells you exactly what's wrong and how to fix it. No more guessing if your alt text is right or your heading hierarchy makes sense.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-a11y src/
```

## What It Does

- Scans HTML and JSX files for WCAG 2.1 AA violations
- Catches missing alt text, broken heading hierarchy, and color contrast issues
- Generates specific fix suggestions with code examples
- Supports glob patterns so you can target specific directories
- Reports severity levels so you know what to fix first

## Usage Examples

```bash
# Scan your entire src directory
npx ai-a11y src/

# Scan specific component files
npx ai-a11y src/components/Button.tsx

# Scan all JSX files
npx ai-a11y "src/**/*.jsx"
```

## Best Practices

- **Run it before every PR** - Catch a11y issues before code review, not after
- **Start with your most visited pages** - Fix the high traffic stuff first
- **Don't ignore warnings** - Warnings today become lawsuits tomorrow
- **Pair with manual testing** - Automated checks catch about 30% of real a11y issues. Use a screen reader for the rest.

## When to Use This

- You're building a public facing web app and need WCAG compliance
- Your team doesn't have a dedicated a11y reviewer
- You inherited a codebase with zero accessibility consideration
- You want to catch obvious violations before a manual audit

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
npx ai-a11y --help
```

## How It Works

The tool reads your HTML or JSX files and extracts the DOM structure. It checks against WCAG 2.1 guidelines for common violations like missing labels, poor contrast ratios, and incorrect ARIA usage. Then it sends the issues to an AI model that generates specific, actionable fix suggestions with code.

## License

MIT. Free forever. Use it however you want.