# ai-type-gen

Paste in a JSON file, get back clean TypeScript interfaces. No more manually typing out types from API responses.

## Install

```bash
npm install -g ai-type-gen
```

## Usage

```bash
npx ai-type-gen response.json --name UserResponse
```

This reads your JSON, figures out the structure, and spits out proper TypeScript interfaces with nested types, optional fields, and JSDoc comments where they make sense.

```bash
# Save to a file
npx ai-type-gen data.json --name Product --output types/product.ts
```

## Setup

```bash
export OPENAI_API_KEY=sk-...
```

## Options

- `-n, --name <name>` - Name for the root interface (default: ApiResponse)
- `-o, --output <file>` - Write to a file instead of stdout

## Why?

Because copying a JSON response and manually writing interfaces is tedious. This does it in seconds and handles the edge cases you'd probably miss, like nullable fields and nested objects.

## License

MIT
