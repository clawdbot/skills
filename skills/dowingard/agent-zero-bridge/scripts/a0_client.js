#!/usr/bin/env node
/**
 * Agent Zero Client - For Clawdbot to call Agent Zero
 * 
 * Usage:
 *   node a0_client.js <message>
 *   node a0_client.js message <text> [--new] [--attach <path>]
 *   node a0_client.js status
 *   node a0_client.js reset
 *   node a0_client.js history
 *   node a0_client.js context [id]
 */

const A0Client = require('./lib/a0_api');
const { parseArgs } = require('./lib/cli');

const HELP = `
Agent Zero Client (Clawdbot → A0)

Usage:
  node a0_client.js <message>
  node a0_client.js message <text> [--new] [--attach <path>]
  node a0_client.js status
  node a0_client.js reset
  node a0_client.js history [--length <n>]
  node a0_client.js context [id]

Options:
  --new           Start new conversation
  --attach <path> Attach file (repeatable)
  --timeout <ms>  Request timeout
  --json          Output as JSON

Environment:
  A0_API_URL      Agent Zero URL (default: http://127.0.0.1:50001)
  A0_API_KEY      Agent Zero API key (required)
`;

async function main() {
    const parsed = parseArgs(process.argv.slice(2));
    const commands = ['message', 'reset', 'status', 'history', 'context', 'help'];
    
    // Default to message if command not recognized
    if (parsed.command && !commands.includes(parsed.command)) {
        parsed.args.unshift(parsed.command);
        parsed.command = 'message';
    }

    if (!parsed.command || parsed.command === 'help' || parsed.options.help) {
        console.log(HELP);
        return;
    }

    const client = new A0Client();

    try {
        let result;
        
        switch (parsed.command) {
            case 'message':
                const msg = parsed.args.join(' ');
                if (!msg) {
                    console.error("Error: Provide a message");
                    process.exit(1);
                }
                result = await client.sendMessage(msg, parsed.options);
                break;

            case 'reset':
                result = await client.reset(parsed.options);
                break;

            case 'status':
                result = await client.status();
                result = parsed.options.json ? result : JSON.stringify(result, null, 2);
                break;

            case 'history':
                const hist = await client.history(parsed.options);
                if (parsed.options.json) {
                    result = hist;
                } else if (hist.error) {
                    result = hist.error;
                } else {
                    result = `Context: ${hist.contextId}\nItems: ${hist.totalItems}\n\n` +
                        hist.items.map(i => `[${i.type}] ${i.heading || ''}: ${(i.content || '').slice(0, 200)}`).join('\n');
                }
                break;

            case 'context':
                if (parsed.args[0]) {
                    client.setContext(parsed.args[0]);
                    result = `Context set to: ${parsed.args[0]}`;
                } else {
                    const ctx = client.getContext();
                    result = ctx ? `Current context: ${ctx}` : "No active context";
                }
                break;

            default:
                console.error(`Unknown command: ${parsed.command}`);
                process.exit(1);
        }

        if (typeof result === 'object') {
            console.log(JSON.stringify(result, null, 2));
        } else {
            console.log(result);
        }

    } catch (error) {
        console.error(`Error: ${error.message}`);
        process.exit(1);
    }
}

main();
