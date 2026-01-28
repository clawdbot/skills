# ai-logger

Set up structured logging in seconds. Generates production-ready config for pino, winston, or bunyan with request tracking, log rotation, and pretty dev output.

## Install

```bash
npm install -g ai-logger
```

## Usage

```bash
npx ai-logger pino
# Generates pino structured logging setup

npx ai-logger winston -o lib/logger.ts
# Winston config saved to file

npx ai-logger bunyan -e edge
# Edge runtime compatible
```

## Setup

```bash
export OPENAI_API_KEY=sk-...
```

## Options

- `-e, --env <environment>` - node, browser, edge (default: node)
- `-o, --output <path>` - Save to file

## License

MIT
