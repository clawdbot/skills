/**
 * ai-prompt-craft
 * Transform basic prompts into elite structured prompts using Anthropic's 10-step framework
 * 
 * Framework based on Anthropic's official prompt engineering guide
 */

const PROMPT_COMPONENTS = {
  taskContext: {
    name: 'Task Context',
    description: 'Define the role and main task',
    tag: null,
    required: true
  },
  toneContext: {
    name: 'Tone Context',
    description: 'Set communication style (professional, casual, warm, technical)',
    tag: null,
    required: false
  },
  backgroundData: {
    name: 'Background Data',
    description: 'Reference documents, files, or context profiles',
    tag: 'CONTEXT',
    required: false
  },
  detailedTask: {
    name: 'Detailed Task Description',
    description: 'Expand task with constraints and guidelines',
    tag: 'INSTRUCTIONS',
    required: true
  },
  examples: {
    name: 'Examples',
    description: 'Provide tangible examples of desired output',
    tag: 'EXAMPLE',
    required: false
  },
  conversationHistory: {
    name: 'Conversation History',
    description: 'Reference previous conversations or context',
    tag: 'HISTORY',
    required: false
  },
  immediateTask: {
    name: 'Immediate Task',
    description: 'The specific action to perform now (use strong verbs)',
    tag: 'TASK',
    required: true
  },
  deepThinking: {
    name: 'Deep Thinking',
    description: 'Trigger reasoning and analysis',
    tag: 'THINKING',
    required: false
  },
  outputFormat: {
    name: 'Output Formatting',
    description: 'Specify exact output format',
    tag: 'OUTPUT',
    required: false
  },
  prefilledResponse: {
    name: 'Prefilled Response',
    description: 'Start the response structure',
    tag: null,
    required: false
  }
};

const TONE_PRESETS = {
  professional: 'Respond in a professional, formal tone. Be precise and thorough.',
  casual: 'Respond in a friendly, conversational tone. Keep it approachable.',
  technical: 'Respond in a technical, detailed tone. Use precise terminology.',
  warm: 'Respond in a warm, supportive tone. Be encouraging and helpful.',
  concise: 'Respond briefly and directly. No unnecessary elaboration.',
  academic: 'Respond in an academic, scholarly tone. Cite reasoning.',
  creative: 'Respond creatively with flair. Think outside the box.'
};

const OUTPUT_FORMATS = {
  bullets: 'Format your response as bullet points.',
  numbered: 'Format your response as a numbered list.',
  markdown: 'Format your response using Markdown with headers and sections.',
  json: 'Format your response as valid JSON.',
  table: 'Format your response as a table.',
  prose: 'Format your response as flowing prose paragraphs.',
  code: 'Format your response as code with comments.',
  stepByStep: 'Format your response as step-by-step instructions.'
};

const THINKING_TRIGGERS = {
  standard: 'Think carefully before responding.',
  deep: 'Think deeply and reason through this step by step.',
  analytical: 'Analyze this from multiple angles before responding.',
  critical: 'Apply critical thinking and consider potential issues.',
  creative: 'Think creatively and explore unconventional solutions.',
  systematic: 'Work through this systematically and methodically.'
};

const ACTION_VERBS = [
  'Analyze', 'Create', 'Design', 'Develop', 'Evaluate', 'Explain',
  'Generate', 'Identify', 'Implement', 'List', 'Optimize', 'Outline',
  'Propose', 'Review', 'Summarize', 'Transform', 'Write', 'Build',
  'Compare', 'Critique', 'Debug', 'Draft', 'Extract', 'Format',
  'Improve', 'Investigate', 'Map', 'Organize', 'Plan', 'Refactor',
  'Simplify', 'Structure', 'Synthesize', 'Test', 'Validate'
];

/**
 * Build a structured prompt from components
 */
function buildPrompt(options = {}) {
  const sections = [];
  
  // 1. Task Context (Role + Task)
  if (options.role || options.task) {
    let taskContext = '';
    if (options.role) {
      taskContext += `You are ${options.role}. `;
    }
    if (options.task) {
      taskContext += options.task;
    }
    sections.push(taskContext.trim());
  }
  
  // 2. Tone Context
  if (options.tone) {
    const toneText = TONE_PRESETS[options.tone] || options.tone;
    sections.push(toneText);
  }
  
  // 3. Background Data
  if (options.context) {
    sections.push(`<CONTEXT>\n${options.context}\n</CONTEXT>`);
  }
  
  // 4. Detailed Task Description & Rules
  if (options.instructions || options.rules) {
    let instructionBlock = '<INSTRUCTIONS>\n';
    if (options.instructions) {
      instructionBlock += options.instructions + '\n';
    }
    if (options.rules && options.rules.length > 0) {
      instructionBlock += '\nRules:\n';
      options.rules.forEach((rule, i) => {
        instructionBlock += `${i + 1}. ${rule}\n`;
      });
    }
    instructionBlock += '</INSTRUCTIONS>';
    sections.push(instructionBlock);
  }
  
  // 5. Examples
  if (options.examples && options.examples.length > 0) {
    options.examples.forEach((example, i) => {
      if (typeof example === 'object') {
        sections.push(`<EXAMPLE>\nInput: ${example.input}\nOutput: ${example.output}\n</EXAMPLE>`);
      } else {
        sections.push(`<EXAMPLE>\n${example}\n</EXAMPLE>`);
      }
    });
  }
  
  // 6. Conversation History
  if (options.history) {
    sections.push(`<HISTORY>\n${options.history}\n</HISTORY>`);
  }
  
  // 7. Immediate Task (with strong verbs)
  if (options.action) {
    sections.push(`<TASK>\n${options.action}\n</TASK>`);
  }
  
  // 8. Deep Thinking
  if (options.thinking) {
    const thinkingText = THINKING_TRIGGERS[options.thinking] || options.thinking;
    if (options.thinkingTag !== false) {
      sections.push(`<THINKING>\n${thinkingText}\n</THINKING>`);
    } else {
      sections.push(thinkingText);
    }
  }
  
  // 9. Output Formatting
  if (options.format) {
    const formatText = OUTPUT_FORMATS[options.format] || options.format;
    sections.push(`<OUTPUT>\n${formatText}\n</OUTPUT>`);
  }
  
  // 10. Prefilled Response
  if (options.prefill) {
    sections.push(`\n${options.prefill}`);
  }
  
  return sections.join('\n\n');
}

/**
 * Transform a basic prompt into a structured one
 */
function transformPrompt(basicPrompt, options = {}) {
  // Extract components from basic prompt
  const enhanced = {
    task: basicPrompt,
    ...options
  };
  
  // Auto-add thinking if not specified
  if (!enhanced.thinking && options.autoThinking !== false) {
    enhanced.thinking = 'standard';
  }
  
  return buildPrompt(enhanced);
}

/**
 * Generate a prompt template for a specific use case
 */
function generateTemplate(useCase, customization = {}) {
  const templates = {
    coding: {
      role: 'an expert software engineer with deep knowledge of best practices',
      tone: 'technical',
      thinking: 'systematic',
      format: 'code',
      rules: [
        'Write clean, maintainable code',
        'Include helpful comments',
        'Follow language-specific conventions',
        'Handle edge cases'
      ]
    },
    writing: {
      role: 'a skilled writer with expertise in clear communication',
      tone: 'professional',
      thinking: 'creative',
      format: 'prose',
      rules: [
        'Use clear, concise language',
        'Maintain consistent tone',
        'Structure content logically'
      ]
    },
    analysis: {
      role: 'a data analyst with expertise in extracting insights',
      tone: 'analytical',
      thinking: 'analytical',
      format: 'bullets',
      rules: [
        'Support claims with evidence',
        'Consider multiple perspectives',
        'Identify key patterns and trends'
      ]
    },
    research: {
      role: 'a thorough researcher with attention to detail',
      tone: 'academic',
      thinking: 'deep',
      format: 'markdown',
      rules: [
        'Verify information accuracy',
        'Cite sources when available',
        'Present balanced viewpoints'
      ]
    },
    brainstorm: {
      role: 'a creative strategist skilled at generating innovative ideas',
      tone: 'creative',
      thinking: 'creative',
      format: 'bullets',
      rules: [
        'Think outside the box',
        'Quantity over initial quality',
        'Build on ideas iteratively'
      ]
    },
    review: {
      role: 'an experienced reviewer with high standards',
      tone: 'professional',
      thinking: 'critical',
      format: 'markdown',
      rules: [
        'Be constructive in feedback',
        'Highlight both strengths and areas for improvement',
        'Provide specific, actionable suggestions'
      ]
    },
    explain: {
      role: 'an expert educator who excels at making complex topics accessible',
      tone: 'warm',
      thinking: 'systematic',
      format: 'stepByStep',
      rules: [
        'Start with fundamentals',
        'Use analogies and examples',
        'Build complexity gradually'
      ]
    }
  };
  
  const template = templates[useCase] || templates.writing;
  return { ...template, ...customization };
}

/**
 * Validate prompt structure
 */
function validatePrompt(prompt) {
  const issues = [];
  const suggestions = [];
  
  // Check for role/context
  if (!prompt.includes('You are') && !prompt.includes('As a')) {
    suggestions.push('Consider adding a role/persona for Claude');
  }
  
  // Check for XML tags (structured prompting)
  const hasTags = /<[A-Z]+>/.test(prompt);
  if (!hasTags) {
    suggestions.push('Consider using XML tags to structure your prompt');
  }
  
  // Check for output format specification
  if (!prompt.toLowerCase().includes('format') && !/<OUTPUT>/.test(prompt)) {
    suggestions.push('Consider specifying the desired output format');
  }
  
  // Check for thinking triggers
  const thinkingTerms = ['think', 'reason', 'analyze', 'consider'];
  const hasThinking = thinkingTerms.some(term => prompt.toLowerCase().includes(term));
  if (!hasThinking) {
    suggestions.push('Consider adding a thinking trigger for complex tasks');
  }
  
  // Check prompt length
  if (prompt.length < 50) {
    issues.push('Prompt may be too short for complex tasks');
  }
  
  return {
    isValid: issues.length === 0,
    issues,
    suggestions,
    score: Math.max(0, 100 - (issues.length * 20) - (suggestions.length * 10))
  };
}

/**
 * Extract components from an existing prompt
 */
function analyzePrompt(prompt) {
  const components = {
    hasRole: /you are|as a|acting as/i.test(prompt),
    hasTone: Object.keys(TONE_PRESETS).some(tone => prompt.toLowerCase().includes(tone)),
    hasContext: /<CONTEXT>|context:|background:/i.test(prompt),
    hasInstructions: /<INSTRUCTIONS>|instructions:|rules:/i.test(prompt),
    hasExamples: /<EXAMPLE>|example:|for example/i.test(prompt),
    hasHistory: /<HISTORY>|previous|conversation/i.test(prompt),
    hasTask: /<TASK>|please|now/i.test(prompt),
    hasThinking: /think|reason|analyze|consider/i.test(prompt),
    hasFormat: /<OUTPUT>|format|bullet|list|json/i.test(prompt),
    hasPrefill: prompt.endsWith(':') || prompt.endsWith(':\n')
  };
  
  const score = Object.values(components).filter(Boolean).length;
  const coverage = Math.round((score / 10) * 100);
  
  return {
    components,
    score,
    coverage,
    recommendation: coverage < 50 ? 'Consider enhancing this prompt with more structure' :
                    coverage < 80 ? 'Good structure, minor improvements possible' :
                    'Well-structured prompt'
  };
}

module.exports = {
  buildPrompt,
  transformPrompt,
  generateTemplate,
  validatePrompt,
  analyzePrompt,
  PROMPT_COMPONENTS,
  TONE_PRESETS,
  OUTPUT_FORMATS,
  THINKING_TRIGGERS,
  ACTION_VERBS
};
