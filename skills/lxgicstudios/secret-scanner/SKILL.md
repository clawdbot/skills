# Secret Scanner

Scan your codebase for leaked secrets, API keys, and credentials before they hit production.

## Quick Start

```bash
npx ai-secret-scan
```

## What It Does

- Scans files for hardcoded secrets and API keys
- Detects common patterns (AWS, Stripe, GitHub tokens, etc.)
- Checks .env files for sensitive data exposure
- Warns about secrets in git history
- Zero config, instant results

## Usage

```bash
# Scan current directory
npx ai-secret-scan

# Scan specific path
npx ai-secret-scan ./src
```

## When to Use

- Before pushing to a public repo
- During security audits
- Setting up CI/CD pipelines
- Onboarding new team members

## Part of the LXGIC Dev Toolkit

One of 110+ free developer tools from LXGIC Studios. No paywalls, no sign-ups.

**Find more:**
- GitHub: https://github.com/lxgic-studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- Website: https://lxgicstudios.com

## License

MIT. Free forever.
