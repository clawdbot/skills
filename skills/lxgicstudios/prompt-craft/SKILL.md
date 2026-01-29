# ai-prompt-craft

Transform basic prompts into elite structured prompts using Anthropic's 10-step framework.

## Quick Reference

```bash
# Transform a basic prompt
ai-prompt-craft transform "Write a sorting function"

# Build with all options
ai-prompt-craft build --role "expert dev" --tone technical --format code --thinking systematic --action "Create a REST API"

# Generate a template
ai-prompt-craft template --use-case coding

# Analyze prompt structure
ai-prompt-craft analyze "Your prompt here"

# List presets
ai-prompt-craft list tones
ai-prompt-craft list formats
```

## The 10-Step Framework

1. **Task Context** - Role + main task (`--role`, `--task`)
2. **Tone Context** - Communication style (`--tone`)
3. **Background Data** - Documents/context (`--context`)
4. **Detailed Task** - Constraints/rules (`--instructions`, `--rules`)
5. **Examples** - Desired outputs (`--examples`)
6. **Conversation History** - Past context (`--history`)
7. **Immediate Task** - Specific action (`--action`)
8. **Deep Thinking** - Reasoning mode (`--thinking`)
9. **Output Format** - Structure (`--format`)
10. **Prefilled Response** - Start structure (`--prefill`)

## Presets

**Tones:** professional, casual, technical, warm, concise, academic, creative

**Formats:** bullets, numbered, markdown, json, table, prose, code, stepByStep

**Thinking:** standard, deep, analytical, critical, creative, systematic

**Templates:** coding, writing, analysis, research, brainstorm, review, explain

## Examples

### Code Review Prompt
```bash
ai-prompt-craft build \
  --role "senior code reviewer" \
  --tone professional \
  --thinking critical \
  --format markdown \
  --rules "Check for bugs,Review architecture,Suggest improvements" \
  --action "Review this pull request"
```

### Research Prompt
```bash
ai-prompt-craft build \
  --role "thorough researcher" \
  --tone academic \
  --thinking deep \
  --format markdown \
  --action "Research the history of quantum computing"
```

### Creative Writing
```bash
ai-prompt-craft template --use-case writing --tone creative --action "Write a short story about AI"
```

## Piping

```bash
echo "Explain machine learning" | ai-prompt-craft transform --tone warm --format stepByStep
cat draft.txt | ai-prompt-craft analyze
```
