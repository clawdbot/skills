# Regex Gen

Generate regex patterns from plain English descriptions. Because nobody actually remembers regex syntax.

## Quick Start

```bash
npx ai-regex "match email addresses"
```

## What It Does

- Converts plain English to working regex
- Explains what each part of the pattern does
- Provides test cases for validation
- Supports common patterns out of the box
- Works for any programming language

## Usage

```bash
# Generate regex from description
npx ai-regex "match phone numbers with optional country code"

# Get regex for URLs
npx ai-regex "validate URLs including localhost"

# Match dates
npx ai-regex "match dates in YYYY-MM-DD format"
```

## Example Output

```
Pattern: ^[\w.-]+@[\w.-]+\.\w{2,}$
Explanation:
  ^ - Start of string
  [\w.-]+ - One or more word chars, dots, or hyphens
  @ - Literal @ symbol
  ...
Test cases: ✓ test@example.com ✓ user.name@domain.co.uk
```

## Part of the LXGIC Dev Toolkit

One of 110+ free developer tools from LXGIC Studios. No paywalls, no sign-ups.

**Find more:**
- GitHub: https://github.com/lxgic-studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- Website: https://lxgicstudios.com

## License

MIT. Free forever.
