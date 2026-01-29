# ai-mock-data

[![npm version](https://img.shields.io/npm/v/ai-mock-data.svg)](https://www.npmjs.com/package/ai-mock-data)
[![npm downloads](https://img.shields.io/npm/dm/ai-mock-data.svg)](https://www.npmjs.com/package/ai-mock-data)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI-powered mock data generator. Create realistic test fixtures without writing faker configs.

Need test data that doesn't look like garbage? Describe what you want and get back realistic mock data. Way better than writing faker.js configs by hand.

## Install

```bash
npm install -g ai-mock-data
```

## Usage

```bash
# Simple description
npx ai-mock-data "users with name, email, age" --count 50

# Get CSV instead
npx ai-mock-data "product catalog with prices" --count 100 --format csv

# SQL inserts
npx ai-mock-data "blog posts with authors" --format sql --count 20

# From a schema file
npx ai-mock-data "users" --schema types/User.ts --count 50

# Save to file
npx ai-mock-data "orders" --count 200 -o mock-orders.json
```

## Setup

```bash
export OPENAI_API_KEY=your-key-here
```

## Options

- `-c, --count <number>` - How many records (default 10)
- `-f, --format <fmt>` - json, csv, or sql (default json)
- `-s, --schema <file>` - TS type or JSON schema file to match
- `-o, --output <file>` - Write to a file

## License

MIT
