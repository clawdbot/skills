---
name: notnative
description: Use Notnative MCP server (ws://127.0.0.1:8788) for note management, search, calendar, tasks, Python execution, and canvas operations. Connects to a local Notnative app instance via WebSocket. Use when you need to search or read notes from Notnative vault, create/update/append content to notes, manage calendar events and tasks, execute Python code for calculations/charts/data analysis, work with canvas diagrams, or access any Notnative app feature via MCP tools.
---

# Notnative

Interact with a local Notnative app instance through its MCP WebSocket server. The Notnative app must be running on port 8788.

## Quick Start

The skill provides a CLI client at `scripts/mcp-client.js` that handles MCP protocol communication.

### Common Commands

```bash
# Search notes by query
node scripts/mcp-client.js search "recipe chicken"
node scripts/mcp-client.js search "project notnative" --limit 10

# Semantic search (by meaning)
node scripts/mcp-client.js semantic "healthy breakfast ideas"

# Read a specific note
node scripts/mcp-client.js read "Recetas/Pollo al limón"

# Get currently active/open note
node scripts/mcp-client.js active

# Create a new note
node scripts/mcp-client.js create "# New Note\n\nContent here" "Note Name" "Personal"

# Append content to note (uses active note if no name specified)
node scripts/mcp-client.js append "\n- New item" "My List"

# Update a note (OVERWRITES entire content)
node scripts/mcp-client.js update "My Note" "# Updated content"

# List notes (optional folder filter)
node scripts/mcp-client.js list-notes "Personal"
node scripts/mcp-client.js list-notes

# List folders
node scripts/mcp-client.js list-folders

# List tags
node scripts/mcp-client.js list-tags

# List tasks
node scripts/mcp-client.js tasks

# Get upcoming calendar events
node scripts/mcp-client.js events

# Get workspace statistics
node scripts/mcp-client.js stats

# Get app documentation
node scripts/mcp-client.js docs "vim commands"

# Execute Python code
node scripts/mcp-client.js run-python "print('Hello, World!')"
```

### Advanced Usage: Direct Tool Calls

Call any MCP tool directly using `call` command with JSON args:

```bash
# Insert content into specific location
node scripts/mcp-client.js call insert_into_note '{"name":"My Note","insertAtLine":10,"content":"New paragraph here"}'

# Create a calendar event
node scripts/mcp-client.js call create_calendar_event '{"title":"Meeting","startTime":"2026-01-26T10:00:00","duration":60}'

# Add a task
node scripts/mcp-client.js call create_task '{"text":"Call John tomorrow","dueDate":"2026-01-26"}'

# Web search
node scripts/mcp-client.js call web_search '{"query":"best JavaScript frameworks 2026"}'

# Browse a webpage
node scripts/mcp-client.js call web_browse '{"url":"https://example.com"}'
```

### List All Available Tools

```bash
node scripts/mcp-client.js list
```

This shows all 86 available MCP tools with their input schemas.

## Key Features

### Note Management

- **Search**: Full-text search (`search_notes`) and semantic search (`semantic_search`)
- **Read**: Get note content by name or active note (`read_note`, `get_active_note`)
- **Create**: Create new notes (`create_note`, `create_daily_note`)
- **Edit**: Insert into note (`insert_into_note`), append (`append_to_note`), or full update (`update_note`)
- **Organize**: Rename, move, delete notes (`rename_note`, `move_note`, `delete_note`)
- **History**: Get and restore note versions (`get_note_history`, `restore_note_from_history`)

### Calendar & Tasks

- **Events**: Create, list, update, delete calendar events (`create_calendar_event`, `list_calendar_events`, `get_upcoming_events`)
- **Tasks**: Create, list, complete tasks (`create_task`, `list_tasks`, `complete_task`)
- **Integration**: Convert tasks to events, find free time (`convert_task_to_event`, `find_free_time`)

### Python Execution

Run Python code with libraries: matplotlib, pandas, numpy, pillow, openpyxl, xlsxwriter

```bash
node scripts/mcp-client.js run-python "import matplotlib.pyplot as plt; plt.plot([1,2,3],[1,4,9]); plt.savefig('plot.png')"
```

Use this for calculations, data analysis, charts, and Excel files with formatting.

### Canvas Operations

Work with canvas diagrams: `canvas_get_state`, `canvas_add_node`, `canvas_connect_nodes`, `canvas_auto_layout`, `canvas_to_mermaid`, etc.

### Tags & Folders

- **Tags**: Create, list, add/remove from notes (`create_tag`, `list_tags`, `add_tag_to_note`)
- **Folders**: Create, list, rename, move folders (`create_folder`, `list_folders`, `rename_folder`)

### Analysis & Search

- **Analysis**: Analyze note structure, get backlinks, find similar notes (`analyze_note_structure`, `get_backlinks`, `find_similar_notes`)
- **Search**: Semantic search, web search, web browse (`semantic_search`, `web_search`, `web_browse`)
- **YouTube**: Get video transcripts (`get_youtube_transcript`)

## Server Requirements

The Notnative MCP server must be running on `ws://127.0.0.1:8788`. Ensure:

1. Notnative app is running
2. MCP server is enabled
3. WebSocket is accessible on port 8788

## Error Handling

- **Connection timeout**: Check if Notnative app is running
- **Request timeout**: Tool execution exceeded 10 seconds
- **Tool not found**: Verify tool name using `list` command

## Script Details

The `scripts/mcp-client.js` script:

1. Connects to WebSocket server
2. Initializes MCP session
3. Sends JSON-RPC requests
4. Returns structured JSON output

All commands return JSON formatted output for easy parsing.
