# ai-middleware

Generate Express middleware from plain English descriptions. Rate limiting, auth, logging, whatever you need.

## Install

```bash
npm install -g ai-middleware
```

## Usage

```bash
npx ai-middleware "rate limit 100 req/min per IP"
npx ai-middleware "JWT auth with role-based access" -t
npx ai-middleware "request logging with response time" -o logger.ts -t
```

## Options

- `-t, --typescript` - Generate TypeScript
- `-o, --output <file>` - Write to file

## Setup

```bash
export OPENAI_API_KEY=sk-...
```

## License

MIT
