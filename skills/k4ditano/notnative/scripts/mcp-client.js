#!/usr/bin/env node

const WebSocket = require('ws');

const WS_URL = 'ws://127.0.0.1:8788';

let ws = null;
let idCounter = 1;
const pendingRequests = new Map();

function sendRequest(method, params = {}) {
  return new Promise((resolve, reject) => {
    const id = idCounter++;

    pendingRequests.set(id, { resolve, reject });

    ws.send(JSON.stringify({
      jsonrpc: '2.0',
      id,
      method,
      params
    }));

    // 10 second timeout
    setTimeout(() => {
      if (pendingRequests.has(id)) {
        pendingRequests.delete(id);
        reject(new Error(`Request timeout: ${method}`));
      }
    }, 10000);
  });
}

async function initialize() {
  const result = await sendRequest('initialize', {
    protocolVersion: '2024-11-05',
    capabilities: {},
    clientInfo: {
      name: 'clawdbot-skill',
      version: '1.0.0'
    }
  });
  return result;
}

async function listTools() {
  const result = await sendRequest('tools/list', {});
  return result.tools;
}

async function callTool(name, args = {}) {
  const result = await sendRequest('tools/call', {
    name,
    arguments: args
  });
  return result;
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command) {
    console.error('Usage: mcp-client.js <command> [args...]');
    console.error('');
    console.error('Commands:');
    console.error('  list                    - List all available tools');
    console.error('  call <tool> <args>     - Call a tool with JSON args');
    console.error('  search <query>         - Search notes by query');
    console.error('  semantic <query>       - Semantic search by meaning');
    console.error('  read <name>            - Read a note by name');
    console.error('  active                 - Get currently active note');
    console.error('  create <content>       - Create a new note');
    console.error('  insert <args>          - Insert content into note');
    console.error('  append <content>       - Append content to note');
    console.error('  update <name> <content> - Update a note');
    console.error('  list-folders           - List all folders');
    console.error('  list-notes [folder]    - List notes (optional folder filter)');
    console.error('  list-tags              - List all tags');
    console.error('  tasks                  - List pending tasks');
    console.error('  events                 - Get upcoming calendar events');
    console.error('  stats                  - Get workspace statistics');
    console.error('  docs <query>           - Get app documentation');
    console.error('  run-python <code>      - Execute Python code');
    process.exit(1);
  }

  ws = new WebSocket(WS_URL);

  ws.on('open', async () => {
    try {
      await initialize();

      switch (command) {
        case 'list':
          const tools = await listTools();
          console.log(JSON.stringify(tools, null, 2));
          break;

        case 'call': {
          const toolName = args[1];
          const toolArgs = args[2] ? JSON.parse(args[2]) : {};
          const result = await callTool(toolName, toolArgs);
          console.log(JSON.stringify(result, null, 2));
          break;
        }

        case 'search': {
          const query = args[1];
          const limit = args[2] ? parseInt(args[2]) : undefined;
          const result = await callTool('search_notes', { query, limit });
          console.log(JSON.stringify(result, null, 2));
          break;
        }

        case 'semantic': {
          const query = args[1];
          const limit = args[2] ? parseInt(args[2]) : undefined;
          const result = await callTool('semantic_search', { query, limit });
          console.log(JSON.stringify(result, null, 2));
          break;
        }

        case 'read': {
          const name = args[1];
          const result = await callTool('read_note', { name });
          console.log(JSON.stringify(result, null, 2));
          break;
        }

        case 'active': {
          const result = await callTool('get_active_note', {});
          console.log(JSON.stringify(result, null, 2));
          break;
        }

        case 'create': {
          const content = args[1];
          const name = args[2];
          const folder = args[3];
          const result = await callTool('create_note', { content, name, folder });
          console.log(JSON.stringify(result, null, 2));
          break;
        }

        case 'insert': {
          const toolArgs = JSON.parse(args[1]);
          const result = await callTool('insert_into_note', toolArgs);
          console.log(JSON.stringify(result, null, 2));
          break;
        }

        case 'append': {
          const content = args[1];
          const name = args[2];
          const result = await callTool('append_to_note', { content, name });
          console.log(JSON.stringify(result, null, 2));
          break;
        }

        case 'update': {
          const name = args[1];
          const content = args[2];
          const result = await callTool('update_note', { name, content });
          console.log(JSON.stringify(result, null, 2));
          break;
        }

        case 'list-folders': {
          const result = await callTool('list_folders', {});
          console.log(JSON.stringify(result, null, 2));
          break;
        }

        case 'list-notes': {
          const folder = args[1];
          const limit = args[2] ? parseInt(args[2]) : undefined;
          const result = await callTool('list_notes', { folder, limit });
          console.log(JSON.stringify(result, null, 2));
          break;
        }

        case 'list-tags': {
          const result = await callTool('list_tags', {});
          console.log(JSON.stringify(result, null, 2));
          break;
        }

        case 'tasks': {
          const result = await callTool('list_tasks', {});
          console.log(JSON.stringify(result, null, 2));
          break;
        }

        case 'events': {
          const result = await callTool('get_upcoming_events', {});
          console.log(JSON.stringify(result, null, 2));
          break;
        }

        case 'stats': {
          const result = await callTool('get_workspace_stats', {});
          console.log(JSON.stringify(result, null, 2));
          break;
        }

        case 'docs': {
          const query = args[1];
          const result = await callTool('get_app_documentation', { query });
          console.log(JSON.stringify(result, null, 2));
          break;
        }

        case 'run-python': {
          const code = args[1];
          const result = await callTool('run_python', { code });
          console.log(JSON.stringify(result, null, 2));
          break;
        }

        default:
          console.error(`Unknown command: ${command}`);
          process.exit(1);
      }

      ws.close();
      setTimeout(() => process.exit(0), 100);
    } catch (err) {
      console.error('Error:', err.message);
      ws.close();
      process.exit(1);
    }
  });

  ws.on('message', (data) => {
    const msg = JSON.parse(data.toString());

    if (msg.method === 'endpoint') {
      // Ignore endpoint messages
      return;
    }

    if (pendingRequests.has(msg.id)) {
      const { resolve, reject } = pendingRequests.get(msg.id);
      pendingRequests.delete(msg.id);

      if (msg.error) {
        reject(new Error(msg.error.message || JSON.stringify(msg.error)));
      } else {
        resolve(msg.result);
      }
    }
  });

  ws.on('error', (err) => {
    console.error('WebSocket error:', err.message);
    process.exit(1);
  });

  setTimeout(() => {
    console.error('Connection timeout');
    ws.close();
    process.exit(1);
  }, 10000);
}

if (require.main === module) {
  main();
}
