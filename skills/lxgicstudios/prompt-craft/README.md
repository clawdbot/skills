# ai-prompt-craft

Transform basic prompts into elite structured prompts using Anthropic's 10-step framework.

Based on [Anthropic's official prompt engineering guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) for Claude.

## The 10-Step Framework

1. **Task Context** - Define the role and main task
2. **Tone Context** - Set communication style
3. **Background Data** - Reference documents and context
4. **Detailed Task Description** - Constraints and guidelines
5. **Examples** - Provide desired output examples
6. **Conversation History** - Reference past context
7. **Immediate Task** - The specific action (use verbs!)
8. **Deep Thinking** - Trigger reasoning mode
9. **Output Formatting** - Specify output structure
10. **Prefilled Response** - Start the response

## Installation

```bash
npm install -g ai-prompt-craft
```

## Usage

### Transform a Basic Prompt

```bash
ai-prompt-craft transform "Write a function to sort an array"
```

Output:
```
Write a function to sort an array

Think carefully before responding.
```

### Build a Structured Prompt

```bash
ai-prompt-craft build \
  --role "expert Python developer" \
  --task "Help write clean, efficient code" \
  --tone technical \
  --format code \
  --thinking systematic \
  --action "Create a binary search function with proper error handling"
```

Output:
```
You are expert Python developer. Help write clean, efficient code

Respond in a technical, detailed tone. Use precise terminology.

<TASK>
Create a binary search function with proper error handling
</TASK>

<THINKING>
Work through this systematically and methodically.
</THINKING>

<OUTPUT>
Format your response as code with comments.
</OUTPUT>
```

### Generate Templates

```bash
ai-prompt-craft template --use-case coding
ai-prompt-craft template --use-case research
ai-prompt-craft template --use-case brainstorm
```

Available templates: `coding`, `writing`, `analysis`, `research`, `brainstorm`, `review`, `explain`

### Analyze Existing Prompts

```bash
ai-prompt-craft analyze "You are an expert. Help me write code."
```

Output:
```
Prompt Analysis
===============
Coverage Score: 30%
Components Found: 3/10

Recommendation: Consider enhancing this prompt with more structure

Component Checklist:
  ✓ Role/Persona
  ✗ Tone Context
  ✗ Background Data
  ✗ Instructions/Rules
  ✗ Examples
  ✗ Conversation History
  ✓ Immediate Task
  ✗ Thinking Trigger
  ✗ Output Format
  ✗ Prefilled Response
```

### Validate Prompts

```bash
ai-prompt-craft validate "Write something"
```

### List Available Presets

```bash
ai-prompt-craft list tones      # professional, casual, technical, warm, etc.
ai-prompt-craft list formats    # bullets, numbered, markdown, json, etc.
ai-prompt-craft list thinking   # standard, deep, analytical, critical, etc.
ai-prompt-craft list verbs      # recommended action verbs
ai-prompt-craft list templates  # available use case templates
ai-prompt-craft list all        # show everything
```

## Piping Support

```bash
echo "Explain quantum computing" | ai-prompt-craft transform --tone academic
cat prompt.txt | ai-prompt-craft analyze
```

## Programmatic Usage

```javascript
const { buildPrompt, transformPrompt, generateTemplate, analyzePrompt } = require('ai-prompt-craft');

// Build a structured prompt
const prompt = buildPrompt({
  role: 'expert data scientist',
  task: 'Analyze datasets and provide insights',
  tone: 'professional',
  context: 'Sales data from Q4 2024',
  instructions: 'Focus on trends and anomalies',
  rules: ['Be specific', 'Include visualizations recommendations'],
  action: 'Analyze the provided CSV data',
  thinking: 'analytical',
  format: 'markdown'
});

// Transform a basic prompt
const enhanced = transformPrompt('Write a blog post about AI', {
  tone: 'casual',
  format: 'markdown',
  thinking: 'creative'
});

// Generate a template
const template = generateTemplate('coding');

// Analyze a prompt
const analysis = analyzePrompt('You are a helpful assistant.');
console.log(analysis.coverage); // 10
```

## Available Presets

### Tones
- `professional` - Formal, precise
- `casual` - Friendly, conversational
- `technical` - Detailed, terminology-focused
- `warm` - Supportive, encouraging
- `concise` - Brief, direct
- `academic` - Scholarly, citation-focused
- `creative` - Imaginative, outside the box

### Output Formats
- `bullets` - Bullet points
- `numbered` - Numbered list
- `markdown` - Full Markdown with headers
- `json` - Valid JSON
- `table` - Table format
- `prose` - Flowing paragraphs
- `code` - Code with comments
- `stepByStep` - Step-by-step instructions

### Thinking Modes
- `standard` - Basic reasoning
- `deep` - Step-by-step reasoning
- `analytical` - Multi-angle analysis
- `critical` - Issue identification
- `creative` - Unconventional solutions
- `systematic` - Methodical approach

## License

MIT

## Credits

Based on Anthropic's prompt engineering research and best practices.
