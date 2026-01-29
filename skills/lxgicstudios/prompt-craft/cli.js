#!/usr/bin/env node

/**
 * ai-prompt-craft CLI
 * Transform basic prompts into elite structured prompts using Anthropic's 10-step framework
 */

const {
  buildPrompt,
  transformPrompt,
  generateTemplate,
  validatePrompt,
  analyzePrompt,
  TONE_PRESETS,
  OUTPUT_FORMATS,
  THINKING_TRIGGERS,
  ACTION_VERBS
} = require('./index.js');

const args = process.argv.slice(2);

function showHelp() {
  console.log(`
ai-prompt-craft - Transform basic prompts into elite structured prompts

Based on Anthropic's 10-step prompting framework for Claude.

USAGE:
  ai-prompt-craft <command> [options]
  prompt-craft <command> [options]

COMMANDS:
  build         Build a structured prompt from components
  transform     Transform a basic prompt into structured format
  template      Generate a prompt template for a use case
  analyze       Analyze an existing prompt's structure
  validate      Validate a prompt and get suggestions
  list          List available presets (tones, formats, etc.)

BUILD OPTIONS:
  --role        Set the AI's role/persona
  --task        Set the main task description
  --tone        Set tone (professional, casual, technical, warm, concise, academic, creative)
  --context     Add background context/data
  --instructions Add detailed instructions
  --rules       Add rules (comma-separated)
  --examples    Add examples (comma-separated or JSON array)
  --history     Add conversation history reference
  --action      Set the immediate action/task
  --thinking    Set thinking mode (standard, deep, analytical, critical, creative, systematic)
  --format      Set output format (bullets, numbered, markdown, json, table, prose, code, stepByStep)
  --prefill     Add prefilled response start

TEMPLATE OPTIONS:
  --use-case    Use case (coding, writing, analysis, research, brainstorm, review, explain)

EXAMPLES:
  # Transform a basic prompt
  ai-prompt-craft transform "Write a function to sort an array"

  # Build a structured prompt
  ai-prompt-craft build --role "expert Python developer" --task "Write clean code" \\
    --tone technical --format code --thinking systematic \\
    --action "Create a binary search function"

  # Generate a template
  ai-prompt-craft template --use-case coding

  # Analyze a prompt
  ai-prompt-craft analyze "You are an expert. Help me write code."

  # Validate a prompt
  ai-prompt-craft validate "Write something"

  # List available presets
  ai-prompt-craft list tones
  ai-prompt-craft list formats
  ai-prompt-craft list thinking
  ai-prompt-craft list verbs
  ai-prompt-craft list templates

PIPING:
  echo "Explain quantum computing" | ai-prompt-craft transform --tone academic
  cat prompt.txt | ai-prompt-craft analyze
`);
}

function parseArgs(args) {
  const options = {};
  let command = null;
  let positional = [];
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--help' || arg === '-h') {
      showHelp();
      process.exit(0);
    }
    
    if (arg.startsWith('--')) {
      const key = arg.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
      const value = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true;
      
      if (key === 'rules' || key === 'examples') {
        try {
          options[key] = JSON.parse(value);
        } catch {
          options[key] = value.split(',').map(s => s.trim());
        }
      } else {
        options[key] = value;
      }
    } else if (!command) {
      command = arg;
    } else {
      positional.push(arg);
    }
  }
  
  return { command, options, positional };
}

async function readStdin() {
  if (process.stdin.isTTY) return null;
  
  return new Promise((resolve) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('readable', () => {
      let chunk;
      while ((chunk = process.stdin.read()) !== null) {
        data += chunk;
      }
    });
    process.stdin.on('end', () => {
      resolve(data.trim());
    });
    setTimeout(() => resolve(data.trim() || null), 100);
  });
}

async function main() {
  const { command, options, positional } = parseArgs(args);
  const stdinData = await readStdin();
  
  if (!command) {
    showHelp();
    process.exit(0);
  }
  
  switch (command) {
    case 'build': {
      const prompt = buildPrompt(options);
      console.log(prompt);
      break;
    }
    
    case 'transform': {
      const basicPrompt = positional.join(' ') || stdinData;
      if (!basicPrompt) {
        console.error('Error: No prompt provided. Pass as argument or pipe via stdin.');
        process.exit(1);
      }
      const prompt = transformPrompt(basicPrompt, options);
      console.log(prompt);
      break;
    }
    
    case 'template': {
      const useCase = options.useCase || positional[0] || 'writing';
      const template = generateTemplate(useCase, options);
      
      console.log('Generated Template Configuration:');
      console.log(JSON.stringify(template, null, 2));
      console.log('\nBuilt Prompt:');
      console.log(buildPrompt({ ...template, action: options.action || '[Your task here]' }));
      break;
    }
    
    case 'analyze': {
      const prompt = positional.join(' ') || stdinData;
      if (!prompt) {
        console.error('Error: No prompt provided. Pass as argument or pipe via stdin.');
        process.exit(1);
      }
      
      const analysis = analyzePrompt(prompt);
      console.log('Prompt Analysis');
      console.log('===============');
      console.log(`Coverage Score: ${analysis.coverage}%`);
      console.log(`Components Found: ${analysis.score}/10`);
      console.log(`\nRecommendation: ${analysis.recommendation}`);
      console.log('\nComponent Checklist:');
      
      const componentNames = {
        hasRole: 'Role/Persona',
        hasTone: 'Tone Context',
        hasContext: 'Background Data',
        hasInstructions: 'Instructions/Rules',
        hasExamples: 'Examples',
        hasHistory: 'Conversation History',
        hasTask: 'Immediate Task',
        hasThinking: 'Thinking Trigger',
        hasFormat: 'Output Format',
        hasPrefill: 'Prefilled Response'
      };
      
      for (const [key, name] of Object.entries(componentNames)) {
        const status = analysis.components[key] ? '✓' : '✗';
        console.log(`  ${status} ${name}`);
      }
      break;
    }
    
    case 'validate': {
      const prompt = positional.join(' ') || stdinData;
      if (!prompt) {
        console.error('Error: No prompt provided. Pass as argument or pipe via stdin.');
        process.exit(1);
      }
      
      const validation = validatePrompt(prompt);
      console.log('Prompt Validation');
      console.log('=================');
      console.log(`Score: ${validation.score}/100`);
      console.log(`Status: ${validation.isValid ? '✓ Valid' : '✗ Issues Found'}`);
      
      if (validation.issues.length > 0) {
        console.log('\nIssues:');
        validation.issues.forEach(issue => console.log(`  ✗ ${issue}`));
      }
      
      if (validation.suggestions.length > 0) {
        console.log('\nSuggestions:');
        validation.suggestions.forEach(s => console.log(`  → ${s}`));
      }
      break;
    }
    
    case 'list': {
      const listType = positional[0] || 'all';
      
      if (listType === 'tones' || listType === 'all') {
        console.log('Available Tones:');
        for (const [key, desc] of Object.entries(TONE_PRESETS)) {
          console.log(`  ${key.padEnd(15)} ${desc}`);
        }
        console.log();
      }
      
      if (listType === 'formats' || listType === 'all') {
        console.log('Available Output Formats:');
        for (const [key, desc] of Object.entries(OUTPUT_FORMATS)) {
          console.log(`  ${key.padEnd(15)} ${desc}`);
        }
        console.log();
      }
      
      if (listType === 'thinking' || listType === 'all') {
        console.log('Available Thinking Modes:');
        for (const [key, desc] of Object.entries(THINKING_TRIGGERS)) {
          console.log(`  ${key.padEnd(15)} ${desc}`);
        }
        console.log();
      }
      
      if (listType === 'verbs' || listType === 'all') {
        console.log('Recommended Action Verbs:');
        const verbsPerRow = 6;
        for (let i = 0; i < ACTION_VERBS.length; i += verbsPerRow) {
          console.log('  ' + ACTION_VERBS.slice(i, i + verbsPerRow).join(', '));
        }
        console.log();
      }
      
      if (listType === 'templates' || listType === 'all') {
        console.log('Available Use Case Templates:');
        const templates = ['coding', 'writing', 'analysis', 'research', 'brainstorm', 'review', 'explain'];
        templates.forEach(t => console.log(`  ${t}`));
        console.log();
      }
      break;
    }
    
    default:
      console.error(`Unknown command: ${command}`);
      console.error('Run "ai-prompt-craft --help" for usage information.');
      process.exit(1);
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
