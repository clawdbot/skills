# ai-regex

Generate regex patterns from plain English. No more regex pain.

## Install

```bash
npm install -g ai-regex
```

## Usage

```bash
npx ai-regex "email addresses"
# → /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g

npx ai-regex "US phone numbers" --json
# → Full JSON with pattern, flags, explanation, examples
```

## Setup

```bash
export OPENAI_API_KEY=sk-...
```

## License

MIT
