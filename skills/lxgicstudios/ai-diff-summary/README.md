# ai-diff-summary

Get a human-readable summary of your git changes. No more squinting at raw diffs.

## Install

```bash
npm install -g ai-diff-summary
```

## Usage

```bash
npx ai-diff-summary           # summarize uncommitted changes
npx ai-diff-summary HEAD~3    # summarize last 3 commits
npx ai-diff-summary main      # summarize changes vs main
```

## Setup

```bash
export OPENAI_API_KEY=sk-...
```

## License

MIT
