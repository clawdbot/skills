# ai-secret-scan

Scan your codebase for leaked secrets, API keys, and credentials. Pattern matching plus AI analysis.

## Install

```bash
npm install -g ai-secret-scan
```

## Usage

```bash
npx ai-secret-scan
# Scans current directory

npx ai-secret-scan ./src
# Scans specific directory

npx ai-secret-scan --no-ai
# Pattern matching only, no AI
```

## Setup

```bash
export OPENAI_API_KEY=sk-...
```

## License

MIT
