# ai-docs

[![npm version](https://img.shields.io/npm/v/@lxgicstudios/ai-docs.svg)](https://www.npmjs.com/package/@lxgicstudios/ai-docs)
[![npm downloads](https://img.shields.io/npm/dm/@lxgicstudios/ai-docs.svg)](https://www.npmjs.com/package/@lxgicstudios/ai-docs)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI-powered JSDoc/TSDoc generator. Automatically document your exported functions, classes, and interfaces.

Adds JSDoc or TSDoc comments to your code. Point it at files or a directory and it'll document your exported functions, classes, and interfaces without touching any logic.

## Install

```bash
npm install -g ai-docs
```

## Setup

```bash
export OPENAI_API_KEY=sk-your-key-here
```

## Usage

```bash
# Preview docs for a directory (prints to stdout)
npx ai-docs src/ --style jsdoc

# TSDoc style
npx ai-docs src/ --style tsdoc

# Actually write the changes back to the files
npx ai-docs src/ --style jsdoc --write

# Single file
npx ai-docs src/utils.ts --style jsdoc

# Glob patterns work too
npx ai-docs "src/**/*.ts" --style tsdoc
```

## What it does

Reads each file, sends it to OpenAI, gets back the same file with doc comments added to all the exported stuff. It won't change your code. It just adds comments above functions, classes, interfaces, and types.

## Tips

- Run without `--write` first to preview what it'll do
- It skips files over 20KB (they'd blow the context window anyway)
- Automatically ignores node_modules and dist folders
