# ai-diagram

Generate Mermaid diagrams from your codebase. Supports flowcharts, class diagrams, sequence diagrams, and more.

## Install

```bash
npm install -g ai-diagram
```

## Usage

```bash
npx ai-diagram ./src/
# → Generates flowchart in diagram.mmd

npx ai-diagram ./src/ --type class -o architecture.mmd
# → Class diagram

npx ai-diagram ./src/ --type sequence
# → Sequence diagram of function calls
```

## Setup

```bash
export OPENAI_API_KEY=sk-...
```

## Diagram Types

- `flowchart` - Code flow and dependencies (default)
- `class` - Class relationships and inheritance
- `sequence` - Function call sequences
- `er` - Entity relationship diagram
- `state` - State machine diagram

## License

MIT
