# ai-license

Picking a license shouldn't require a law degree. This tool explains each license in plain English and generates the LICENSE file for you.

## Install

```bash
npm install -g ai-license
```

## Usage

```bash
# Interactive mode - it'll ask you questions
npx ai-license

# Skip the questions, just give me MIT
npx ai-license --type mit --name "Jane Doe"

# See what a license actually means before committing
npx ai-license --explain apache-2.0
```

## Supported Licenses

MIT, Apache 2.0, GPL 3.0, BSD 2-Clause, BSD 3-Clause, ISC, MPL 2.0, LGPL 3.0, AGPL 3.0, Unlicense, and more. If you're not sure which one to pick, just run it without flags and it'll walk you through it.

## Requirements

Set your `OPENAI_API_KEY` environment variable.

```bash
export OPENAI_API_KEY=sk-...
```

## License

MIT
