#!/usr/bin/env node
/**
 * Task Breakdown Workflow
 * 
 * Uses Agent Zero to break complex tasks into steps,
 * then tracks them in a notebook system.
 * 
 * Usage:
 *   node task_breakdown.js "Build a REST API for user authentication"
 */

const fs = require('fs');
const path = require('path');
const A0Client = require('./lib/a0_api');
const config = require('./lib/config');

const HELP = `
Task Breakdown Workflow

Usage:
  node task_breakdown.js "Your complex task description"

This will:
  1. Send the task to Agent Zero for breakdown
  2. Parse the returned steps
  3. Create a project file in notebook/tasks/projects/

Environment:
  NOTEBOOK_PATH - Path to notebook directory
`;

async function breakdownTask(client, taskDescription) {
    const prompt = `You are a senior technical project manager. Break down the following task into clear, actionable steps. 

Task: "${taskDescription}"

Return ONLY a numbered list of steps in this exact format:
1. [Step title]: [Brief description]
2. [Step title]: [Brief description]
...

Keep each step atomic and completable in under 2 hours. Include any prerequisites or dependencies. Do not include any preamble or explanation - just the numbered list.`;

    return await client.sendMessage(prompt, { new: true });
}

function parseSteps(breakdownText) {
    const lines = breakdownText.split('\n').filter(line => line.trim());
    const steps = [];
    
    for (const line of lines) {
        // Try format: "1. Step title: Description"
        const match = line.match(/^\d+\.\s*(.+?):\s*(.+)$/);
        if (match) {
            steps.push({
                title: match[1].trim(),
                description: match[2].trim()
            });
            continue;
        }
        
        // Try simpler format: "1. Do something"
        const simpleMatch = line.match(/^\d+\.\s*(.+)$/);
        if (simpleMatch) {
            steps.push({
                title: simpleMatch[1].trim(),
                description: ''
            });
        }
    }
    
    return steps;
}

function createProjectFile(taskTitle, steps, notebookPath) {
    const slug = taskTitle.toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-|-$/g, '')
        .slice(0, 50);
    
    const date = new Date().toISOString().split('T')[0];
    const filename = `${date}-${slug}.md`;
    const projectsDir = path.join(notebookPath, 'tasks', 'projects');
    const filepath = path.join(projectsDir, filename);
    
    // Ensure projects directory exists
    if (!fs.existsSync(projectsDir)) {
        fs.mkdirSync(projectsDir, { recursive: true });
    }
    
    let content = `# ${taskTitle}

**Created:** ${date}
**Status:** In Progress
**Breakdown by:** Agent Zero

---

## Steps

`;

    steps.forEach((step, index) => {
        content += `### ${index + 1}. ${step.title}
- [ ] **Status:** todo
${step.description ? `- **Details:** ${step.description}\n` : ''}- **Notes:** 

`;
    });

    content += `---

## Progress Log

| Date | Step | Action | Notes |
|------|------|--------|-------|
| ${date} | - | Created | Task broken down into ${steps.length} steps |

---

## Completion Checklist
- [ ] All steps completed
- [ ] Tested/verified
- [ ] Documented
- [ ] Archived
`;

    fs.writeFileSync(filepath, content);
    return filepath;
}

async function main() {
    const task = process.argv.slice(2).join(' ');
    
    if (!task || task === '--help' || task === 'help') {
        console.log(HELP);
        return;
    }

    console.log(`📋 Breaking down task: "${task}"\n`);
    console.log('🤖 Asking Agent Zero for step breakdown...\n');

    const client = new A0Client();

    try {
        const breakdown = await breakdownTask(client, task);
        console.log('📝 Agent Zero response:\n');
        console.log(breakdown);
        console.log('\n');

        const steps = parseSteps(breakdown);
        
        if (steps.length === 0) {
            console.log('⚠️  Could not parse steps from response. Raw response saved.');
            const filepath = createProjectFile(task, [{ 
                title: 'Review breakdown', 
                description: breakdown 
            }], config.notebook.path);
            console.log(`📁 Created: ${filepath}`);
            return;
        }

        console.log(`✅ Parsed ${steps.length} steps\n`);

        const filepath = createProjectFile(task, steps, config.notebook.path);
        console.log(`📁 Project file created: ${filepath}`);
        console.log('\nSteps:');
        steps.forEach((step, i) => {
            console.log(`  ${i + 1}. ${step.title}`);
        });

    } catch (error) {
        console.error(`❌ Error: ${error.message}`);
        process.exit(1);
    }
}

main();
