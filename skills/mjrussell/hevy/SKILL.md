---
name: hevy
description: Query workout data from Hevy including workouts, routines, exercises, and history. Use when user asks about their workouts, gym sessions, exercise progress, or fitness routines.
homepage: https://hevy.com
metadata:
  clawdbot:
    emoji: "🏋️"
    requires:
      bins: ["hevy"]
      env: ["HEVY_API_KEY"]
---

# Hevy CLI

CLI for the Hevy workout tracking API. Query workouts, routines, exercises, and track progress.

## Setup

Requires Hevy Pro subscription for API access.

1. Get API key from https://hevy.com/settings?developer
2. Set environment variable: `export HEVY_API_KEY="your-key"`

## Commands

### Status

```bash
# Check configuration and connection
hevy status
```

### Workouts

```bash
# List recent workouts (default 5)
hevy workouts
hevy workouts --limit 10

# Fetch all workouts
hevy workouts --all

# Show detailed workout
hevy workout <workout-id>

# JSON output
hevy workouts --json
hevy workout <id> --json

# Show weights in kg (default is lbs)
hevy workouts --kg
```

### Routines

```bash
# List all routines
hevy routines

# Show detailed routine
hevy routine <routine-id>

# JSON output
hevy routines --json
```

### Exercises

```bash
# List all exercise templates
hevy exercises

# Search by name
hevy exercises --search "bench press"

# Filter by muscle group
hevy exercises --muscle chest

# Show only custom exercises
hevy exercises --custom

# JSON output
hevy exercises --json
```

### Exercise History

```bash
# Show history for specific exercise
hevy history <exercise-template-id>
hevy history <exercise-template-id> --limit 50

# JSON output
hevy history <exercise-template-id> --json
```

### Creating Routines

```bash
# Create routine from JSON (stdin)
echo '{"routine": {...}}' | hevy create-routine

# Create routine from file
hevy create-routine --file routine.json

# Create a routine folder
hevy create-folder "Push Pull Legs"

# Update existing routine
echo '{"routine": {...}}' | hevy update-routine <routine-id>

# Create custom exercise (checks for duplicates first!)
hevy create-exercise --title "My Exercise" --muscle chest --type weight_reps

# Force create even if duplicate exists
hevy create-exercise --title "My Exercise" --muscle chest --force
```

**⚠️ Duplicate Prevention:** `create-exercise` checks if an exercise with the same name already exists and will error if found. Use `--force` to create anyway (not recommended).

**Routine JSON format:**
```json
{
  "routine": {
    "title": "Push Day 💪",
    "folder_id": null,
    "notes": "Chest, shoulders, triceps",
    "exercises": [
      {
        "exercise_template_id": "79D0BB3A",
        "notes": "Focus on form",
        "rest_seconds": 90,
        "sets": [
          { "type": "warmup", "weight_kg": 20, "reps": 15 },
          { "type": "normal", "weight_kg": 60, "reps": 8 }
        ]
      }
    ]
  }
}
```

### Other

```bash
# Total workout count
hevy count

# List routine folders
hevy folders
```

## Usage Examples

**User asks "What did I do at the gym?"**
```bash
hevy workouts
```

**User asks "Show me my last chest workout"**
```bash
hevy workouts --limit 10  # Find relevant workout ID
hevy workout <id>         # Get details
```

**User asks "How am I progressing on bench press?"**
```bash
hevy exercises --search "bench press"  # Get exercise template ID
hevy history <exercise-id>              # View progression
```

**User asks "What routines do I have?"**
```bash
hevy routines
hevy routine <id>  # For details
```

**User asks "Find leg exercises"**
```bash
hevy exercises --muscle quadriceps
hevy exercises --muscle hamstrings
hevy exercises --muscle glutes
```

**User asks "Create a push day routine"**
```bash
# 1. Find exercise IDs
hevy exercises --search "bench press"
hevy exercises --search "shoulder press"
# 2. Create routine JSON with those IDs and pipe to create-routine
```

## Notes

- **Duplicate Prevention:** `create-exercise` checks for existing exercises with the same name before creating. Use `--force` to override (not recommended).
- **API Limitations:** Hevy API does NOT support deleting or editing exercise templates - only creating. Delete exercises manually in the app.
- **API Rate Limits:** Be mindful when fetching all data (--all flag)
- **Weights:** Defaults to lbs, use --kg for kilograms
- **Pagination:** Most commands auto-paginate, but limit flags help reduce API calls
- **IDs:** Workout/routine/exercise IDs are UUIDs, shown in detailed views

## API Reference

Full API docs: https://api.hevyapp.com/docs/

### Available Endpoints
- `GET /v1/workouts` - List workouts (paginated)
- `GET /v1/workouts/{id}` - Get single workout
- `GET /v1/workouts/count` - Total workout count
- `GET /v1/routines` - List routines
- `GET /v1/routines/{id}` - Get single routine
- `GET /v1/exercise_templates` - List exercises
- `GET /v1/exercise_templates/{id}` - Get single exercise
- `GET /v1/exercise_history/{id}` - Exercise history
- `GET /v1/routine_folders` - List folders

### Write Operations (supported but use carefully)
- `POST /v1/workouts` - Create workout
- `PUT /v1/workouts/{id}` - Update workout
- `POST /v1/routines` - Create routine
- `PUT /v1/routines/{id}` - Update routine
- `POST /v1/exercise_templates` - Create custom exercise
- `POST /v1/routine_folders` - Create folder

The CLI focuses on read operations. Write operations are available via the API client for programmatic use.
