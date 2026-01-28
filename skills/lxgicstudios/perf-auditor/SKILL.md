---
name: perf-auditor
description: Run a Lighthouse performance audit with AI fix suggestions. Use when your site is slow and you need actionable fixes.
---

# Performance Auditor

Your site scores 43 on Lighthouse and you don't know where to start. This tool runs a performance audit and gives you specific, prioritized fixes instead of vague suggestions. It tells you exactly what's slowing things down and how to fix it.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-lighthouse https://mysite.com
```

## What It Does

- Runs a Lighthouse performance audit on any URL
- Identifies the biggest performance bottlenecks with specific metrics
- Generates AI powered fix suggestions with actual code changes
- Prioritizes fixes by impact so you tackle the big wins first
- Covers Core Web Vitals, render blocking resources, and image optimization

## Usage Examples

```bash
# Audit a production URL
npx ai-lighthouse https://mysite.com

# Audit a local dev server
npx ai-lighthouse http://localhost:3000

# Audit a specific page
npx ai-lighthouse https://mysite.com/products
```

## Best Practices

- **Test production, not dev** - Dev builds are unoptimized. Always audit the production URL for real numbers.
- **Fix the top 3 issues first** - Don't try to fix everything at once. The top 3 usually account for 80% of the problem.
- **Run before and after** - Get a baseline, make changes, then re-audit to see the improvement
- **Check mobile and desktop separately** - Mobile performance is usually worse and that's where most users are

## When to Use This

- Your Lighthouse score dropped and you need to figure out why
- A client is complaining about slow page loads
- You want to optimize before a product launch
- You need to pass Core Web Vitals thresholds for SEO

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
npx ai-lighthouse --help
```

## How It Works

The tool runs Lighthouse programmatically against your URL to collect performance metrics. It then analyzes the audit results and sends the bottleneck data to an AI model that generates specific, actionable fix suggestions. Each suggestion includes the expected impact and code changes.

## License

MIT. Free forever. Use it however you want.