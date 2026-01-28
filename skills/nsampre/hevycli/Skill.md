# Hevy CLI Skill

## Description

Access and analyze Hevy fitness tracking data including workouts, routines, and exercise templates via the command line.

## When to Use

Use this skill when the user asks to:
- View their workout history or recent workouts
- Get details about a specific workout
- Check their total workout count
- List or view their workout routines
- Browse exercise templates
- Export workout data as JSON
- Analyze their fitness progress over time

## Prerequisites

- User must have `hevycli` installed (`go install github.com/nsampre/hevycli@latest`)
- User must have configured their Hevy API key (`hevycli config set-api-key <key>`)
- User must have a Hevy Pro subscription

## Available Commands

### Configuration
```bash
# Set API key
hevycli config set-api-key <api-key-uuid>

# View current config
hevycli config show
```

### Workouts
```bash
# List recent workouts
hevycli workouts list [--page N] [--page-size N] [--format json|table]

# Get detailed workout information (accepts full UUID or 8-char short ID)
hevycli workouts get <workout-id>

# Get total workout count
hevycli workouts count
```

### Routines
```bash
# List routines
hevycli routines list [--page N] [--page-size N] [--format json|table]

# Get routine details (accepts full UUID or 8-char short ID)
hevycli routines get <routine-id>
```

### Exercises
```bash
# List exercise templates
hevycli exercises list [--page N] [--page-size N] [--format json|table]

# Get exercise template details
hevycli exercises get <template-id>
```

## Global Flags

- `--format` - Output format: `table` (default) or `json`
- `--debug` - Enable debug output for API requests

## Usage Examples

### Example 1: View Recent Workout History
```bash
hevycli workouts list --page-size 5
```

### Example 2: Get Detailed Workout with Sets and Reps
```bash
# Using short ID (first 8 characters)
hevycli workouts get f75e9c13

# Or using full UUID
hevycli workouts get f75e9c13-32d7-407d-9715-011f5d5698fa
```

### Example 3: Export Data for Analysis
```bash
# Export all workouts as JSON
hevycli workouts list --format json > workouts.json

# Export routines
hevycli routines list --format json > routines.json
```

### Example 4: Check Progress
```bash
# View total workouts completed
hevycli workouts count

# List exercise templates to find specific exercise IDs
hevycli exercises list
```

## Tips for Claude

1. **Use JSON format for analysis**: When helping users analyze their data, use `--format json` to get structured data that can be parsed and analyzed.

2. **Short IDs are supported**: Users can copy short IDs from `workouts list` output and use them directly in `workouts get` commands.

3. **Pagination**: API max page size is 10. Use pagination (`--page N`) to access older workouts.

4. **Error handling**: If a command fails:
   - Check if API key is configured (`hevycli config show`)
   - Verify the user has Hevy Pro subscription
   - Check if the ID exists or is valid

5. **Data insights**: After retrieving workout data, you can:
   - Calculate training volume (weight × reps × sets)
   - Track progression over time
   - Identify patterns in workout frequency
   - Suggest rest day intervals

## Example Interaction

**User**: "Show me my last 3 workouts"

**Claude**:
```bash
hevycli workouts list --page-size 3
```

**User**: "Get details on the first workout"

**Claude**:
```bash
# Using the short ID from the list output
hevycli workouts get f75e9c13
```

**User**: "How many total workouts have I completed?"

**Claude**:
```bash
hevycli workouts count
```

## Notes

- The tool reads data only - it does not create or modify workouts
- All timestamps are in ISO 8601 format
- Weights are always displayed in kilograms
- Distances are in meters, durations in seconds
- Table output handles emoji in workout titles (may have minor alignment issues depending on terminal)
