# ai-auth-check

[![npm version](https://img.shields.io/npm/v/ai-auth-check.svg)](https://www.npmjs.com/package/ai-auth-check)
[![npm downloads](https://img.shields.io/npm/dm/ai-auth-check.svg)](https://www.npmjs.com/package/ai-auth-check)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI-powered auth auditor. Find session management flaws, weak JWT configs, and OAuth vulnerabilities in your code.

Audit your auth implementation for security flaws.

## Install

```bash
npm install -g ai-auth-check
```

## Usage

```bash
npx ai-auth-check ./src/auth/
npx ai-auth-check ./lib/middleware/ -o security-report.md
```

## Setup

```bash
export OPENAI_API_KEY=sk-...
```
