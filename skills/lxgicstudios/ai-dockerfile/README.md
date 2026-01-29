# ai-dockerfile

[![npm version](https://img.shields.io/npm/v/ai-dockerfile.svg)](https://www.npmjs.com/package/ai-dockerfile)
[![npm downloads](https://img.shields.io/npm/dm/ai-dockerfile.svg)](https://www.npmjs.com/package/ai-dockerfile)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI-powered Dockerfile generator. Scans your project and creates optimized multi-stage builds.

Writing Dockerfiles is tedious. This tool scans your project and generates an optimized multi-stage Dockerfile that actually makes sense.

## Install

```bash
npm install -g ai-dockerfile
```

## Usage

```bash
# Generate a Dockerfile
npx ai-dockerfile

# Generate an optimized multi-stage build
npx ai-dockerfile --optimize

# Preview without writing
npx ai-dockerfile --preview

# Custom output path
npx ai-dockerfile --output ./docker/Dockerfile
```

## What it does

Looks at your project structure, figures out the runtime, framework, and build steps, then generates a proper multi-stage Dockerfile. It handles Node.js, Python, Go, Rust, and more.

## Requirements

Set your `OPENAI_API_KEY` environment variable.

```bash
export OPENAI_API_KEY=sk-...
```

## License

MIT
