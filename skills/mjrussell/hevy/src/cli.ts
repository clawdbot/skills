#!/usr/bin/env node

/**
 * Hevy CLI - Command line interface for Hevy workout tracking
 */

import { Command } from "commander";
import { HevyClient } from "./api.js";
import { getConfig, isConfigured } from "./config.js";
import type { Workout, Routine, ExerciseTemplate, Set } from "./types.js";

const program = new Command();

program
  .name("hevy")
  .description("CLI for Hevy workout tracking")
  .version("1.0.0");

// ============================================
// Helper Functions
// ============================================

function formatDate(isoString: string): string {
  const date = new Date(isoString);
  return date.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function formatTime(isoString: string): string {
  const date = new Date(isoString);
  return date.toLocaleTimeString("en-US", {
    hour: "numeric",
    minute: "2-digit",
  });
}

function formatDuration(startTime: string, endTime: string): string {
  const start = new Date(startTime);
  const end = new Date(endTime);
  const diffMs = end.getTime() - start.getTime();
  const diffMins = Math.round(diffMs / 60000);
  
  if (diffMins < 60) {
    return `${diffMins}min`;
  }
  const hours = Math.floor(diffMins / 60);
  const mins = diffMins % 60;
  return mins > 0 ? `${hours}h ${mins}min` : `${hours}h`;
}

function formatWeight(kg: number | null, unit: "kg" | "lbs" = "lbs"): string {
  if (kg === null) return "-";
  if (unit === "lbs") {
    return `${Math.round(kg * 2.20462)}lbs`;
  }
  return `${kg}kg`;
}

function formatSet(set: Set, unit: "kg" | "lbs" = "lbs"): string {
  const parts: string[] = [];
  
  if (set.weight_kg !== null) {
    parts.push(formatWeight(set.weight_kg, unit));
  }
  if (set.reps !== null) {
    parts.push(`${set.reps} reps`);
  }
  if (set.distance_meters !== null) {
    parts.push(`${set.distance_meters}m`);
  }
  if (set.duration_seconds !== null) {
    const mins = Math.floor(set.duration_seconds / 60);
    const secs = set.duration_seconds % 60;
    parts.push(mins > 0 ? `${mins}:${secs.toString().padStart(2, "0")}` : `${secs}s`);
  }
  if (set.rpe !== null) {
    parts.push(`RPE ${set.rpe}`);
  }
  
  const typePrefix = set.type !== "normal" ? `[${set.type}] ` : "";
  return typePrefix + (parts.length > 0 ? parts.join(" × ") : "-");
}

function printWorkoutSummary(workout: Workout, unit: "kg" | "lbs" = "lbs"): void {
  console.log(`\n📅 ${formatDate(workout.start_time)} - ${workout.title}`);
  console.log(`   ⏱️  ${formatTime(workout.start_time)} - ${formatTime(workout.end_time)} (${formatDuration(workout.start_time, workout.end_time)})`);
  
  if (workout.description) {
    console.log(`   📝 ${workout.description}`);
  }
  
  const totalSets = workout.exercises.reduce((sum, ex) => sum + ex.sets.length, 0);
  console.log(`   💪 ${workout.exercises.length} exercises, ${totalSets} sets`);
}

function printWorkoutDetail(workout: Workout, unit: "kg" | "lbs" = "lbs"): void {
  printWorkoutSummary(workout, unit);
  console.log("");
  
  for (const exercise of workout.exercises) {
    console.log(`   ${exercise.index + 1}. ${exercise.title}`);
    if (exercise.notes) {
      console.log(`      📝 ${exercise.notes}`);
    }
    for (const set of exercise.sets) {
      console.log(`      • ${formatSet(set, unit)}`);
    }
  }
}

function printRoutineSummary(routine: Routine): void {
  const totalSets = routine.exercises.reduce((sum, ex) => sum + ex.sets.length, 0);
  console.log(`• ${routine.title} (${routine.exercises.length} exercises, ${totalSets} sets)`);
}

function printRoutineDetail(routine: Routine, unit: "kg" | "lbs" = "lbs"): void {
  console.log(`\n🏋️ ${routine.title}`);
  if (routine.notes) {
    console.log(`   📝 ${routine.notes}`);
  }
  console.log(`   Created: ${formatDate(routine.created_at)}`);
  console.log("");
  
  for (const exercise of routine.exercises) {
    console.log(`   ${exercise.index + 1}. ${exercise.title}`);
    if (exercise.notes) {
      console.log(`      📝 ${exercise.notes}`);
    }
    if (exercise.rest_seconds) {
      console.log(`      ⏱️  Rest: ${exercise.rest_seconds}s`);
    }
    for (const set of exercise.sets) {
      const repRange = set.rep_range 
        ? `${set.rep_range.start}-${set.rep_range.end} reps`
        : set.reps ? `${set.reps} reps` : "";
      const weight = set.weight_kg ? formatWeight(set.weight_kg, unit) : "";
      const parts = [weight, repRange].filter(Boolean);
      console.log(`      • ${parts.join(" × ") || "-"}`);
    }
  }
}

// ============================================
// Commands
// ============================================

// Status command - check if configured
program
  .command("status")
  .description("Check API key configuration and connection")
  .action(async () => {
    if (!isConfigured()) {
      console.log("❌ Not configured - HEVY_API_KEY environment variable not set");
      console.log("");
      console.log("To get your API key:");
      console.log("  1. Go to https://hevy.com/settings?developer");
      console.log("  2. Generate an API key (requires Hevy Pro)");
      console.log("");
      console.log("Then set: export HEVY_API_KEY=\"your-key\"");
      process.exit(1);
    }

    console.log("✓ HEVY_API_KEY is set");
    
    try {
      const client = new HevyClient(getConfig());
      const count = await client.getWorkoutCount();
      console.log(`✓ Connected to Hevy API`);
      console.log(`✓ Account has ${count} workouts`);
    } catch (error) {
      console.log("❌ Failed to connect to Hevy API");
      console.error(error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

// Workouts command
program
  .command("workouts")
  .description("List recent workouts")
  .option("-n, --limit <number>", "Number of workouts to show", "5")
  .option("--all", "Fetch all workouts (may be slow)")
  .option("--json", "Output as JSON")
  .option("--kg", "Show weights in kg instead of lbs")
  .action(async (options: { limit: string; all?: boolean; json?: boolean; kg?: boolean }) => {
    const client = new HevyClient(getConfig());
    const unit = options.kg ? "kg" : "lbs";

    try {
      let workouts: Workout[];
      
      if (options.all) {
        console.log("Fetching all workouts...");
        workouts = await client.getAllWorkouts();
      } else {
        const limit = parseInt(options.limit, 10);
        workouts = await client.getRecentWorkouts(limit);
      }

      if (options.json) {
        console.log(JSON.stringify(workouts, null, 2));
        return;
      }

      if (workouts.length === 0) {
        console.log("No workouts found.");
        return;
      }

      console.log(`\n📊 ${workouts.length} workout${workouts.length !== 1 ? "s" : ""}:\n`);
      for (const workout of workouts) {
        printWorkoutSummary(workout, unit);
      }
      console.log("");
    } catch (error) {
      console.error("Error:", error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

// Workout detail command
program
  .command("workout <id>")
  .description("Show detailed workout by ID")
  .option("--json", "Output as JSON")
  .option("--kg", "Show weights in kg instead of lbs")
  .action(async (id: string, options: { json?: boolean; kg?: boolean }) => {
    const client = new HevyClient(getConfig());
    const unit = options.kg ? "kg" : "lbs";

    try {
      const workout = await client.getWorkout(id);

      if (options.json) {
        console.log(JSON.stringify(workout, null, 2));
        return;
      }

      printWorkoutDetail(workout, unit);
      console.log("");
    } catch (error) {
      console.error("Error:", error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

// Routines command
program
  .command("routines")
  .description("List all routines")
  .option("--json", "Output as JSON")
  .action(async (options: { json?: boolean }) => {
    const client = new HevyClient(getConfig());

    try {
      const routines = await client.getAllRoutines();

      if (options.json) {
        console.log(JSON.stringify(routines, null, 2));
        return;
      }

      if (routines.length === 0) {
        console.log("No routines found.");
        return;
      }

      console.log(`\n🏋️ ${routines.length} routine${routines.length !== 1 ? "s" : ""}:\n`);
      for (const routine of routines) {
        printRoutineSummary(routine);
      }
      console.log("");
    } catch (error) {
      console.error("Error:", error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

// Routine detail command
program
  .command("routine <id>")
  .description("Show detailed routine by ID")
  .option("--json", "Output as JSON")
  .option("--kg", "Show weights in kg instead of lbs")
  .action(async (id: string, options: { json?: boolean; kg?: boolean }) => {
    const client = new HevyClient(getConfig());
    const unit = options.kg ? "kg" : "lbs";

    try {
      const routine = await client.getRoutine(id);

      if (options.json) {
        console.log(JSON.stringify(routine, null, 2));
        return;
      }

      printRoutineDetail(routine, unit);
      console.log("");
    } catch (error) {
      console.error("Error:", error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

// Exercises command
program
  .command("exercises")
  .description("List exercise templates")
  .option("-s, --search <query>", "Search by name")
  .option("--custom", "Show only custom exercises")
  .option("--muscle <group>", "Filter by muscle group")
  .option("--json", "Output as JSON")
  .action(async (options: { search?: string; custom?: boolean; muscle?: string; json?: boolean }) => {
    const client = new HevyClient(getConfig());

    try {
      let templates: ExerciseTemplate[];
      
      if (options.search) {
        templates = await client.searchExerciseTemplates(options.search);
      } else {
        console.log("Fetching exercise templates...");
        templates = await client.getAllExerciseTemplates();
      }

      // Apply filters
      if (options.custom) {
        templates = templates.filter(t => t.is_custom);
      }
      if (options.muscle) {
        const muscle = options.muscle.toLowerCase();
        templates = templates.filter(t => 
          t.primary_muscle_group.toLowerCase().includes(muscle) ||
          t.secondary_muscle_groups.some(m => m.toLowerCase().includes(muscle))
        );
      }

      if (options.json) {
        console.log(JSON.stringify(templates, null, 2));
        return;
      }

      if (templates.length === 0) {
        console.log("No exercises found.");
        return;
      }

      console.log(`\n💪 ${templates.length} exercise${templates.length !== 1 ? "s" : ""}:\n`);
      for (const template of templates.slice(0, 50)) {
        const custom = template.is_custom ? " [custom]" : "";
        console.log(`• ${template.title}${custom}`);
        console.log(`  ${template.primary_muscle_group} | ${template.type} | ID: ${template.id}`);
      }
      if (templates.length > 50) {
        console.log(`\n... and ${templates.length - 50} more. Use --json for full list.`);
      }
      console.log("");
    } catch (error) {
      console.error("Error:", error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

// Exercise history command
program
  .command("history <exerciseId>")
  .description("Show history for a specific exercise")
  .option("-n, --limit <number>", "Number of entries to show", "20")
  .option("--json", "Output as JSON")
  .option("--kg", "Show weights in kg instead of lbs")
  .action(async (exerciseId: string, options: { limit: string; json?: boolean; kg?: boolean }) => {
    const client = new HevyClient(getConfig());
    const unit = options.kg ? "kg" : "lbs";
    const limit = parseInt(options.limit, 10);

    try {
      // First get the exercise name
      let exerciseName = exerciseId;
      try {
        const template = await client.getExerciseTemplate(exerciseId);
        exerciseName = template.title;
      } catch {
        // If we can't get the template, just use the ID
      }

      const history = await client.getAllExerciseHistory(exerciseId);

      if (options.json) {
        console.log(JSON.stringify(history.slice(0, limit), null, 2));
        return;
      }

      if (history.length === 0) {
        console.log(`No history found for ${exerciseName}.`);
        return;
      }

      console.log(`\n📈 History for ${exerciseName} (${Math.min(limit, history.length)} of ${history.length} entries):\n`);
      
      let currentWorkout = "";
      for (const entry of history.slice(0, limit)) {
        const workoutHeader = `${formatDate(entry.workout_start_time)} - ${entry.workout_title}`;
        if (workoutHeader !== currentWorkout) {
          currentWorkout = workoutHeader;
          console.log(`\n${workoutHeader}`);
        }
        
        const weight = entry.weight_kg !== null ? formatWeight(entry.weight_kg, unit) : "";
        const reps = entry.reps !== null ? `${entry.reps} reps` : "";
        const rpe = entry.rpe !== null ? `RPE ${entry.rpe}` : "";
        const parts = [weight, reps, rpe].filter(Boolean);
        const typePrefix = entry.set_type !== "normal" ? `[${entry.set_type}] ` : "";
        console.log(`  • ${typePrefix}${parts.join(" × ")}`);
      }
      console.log("");
    } catch (error) {
      console.error("Error:", error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

// Folders command
program
  .command("folders")
  .description("List routine folders")
  .option("--json", "Output as JSON")
  .action(async (options: { json?: boolean }) => {
    const client = new HevyClient(getConfig());

    try {
      const folders = await client.getAllRoutineFolders();

      if (options.json) {
        console.log(JSON.stringify(folders, null, 2));
        return;
      }

      if (folders.length === 0) {
        console.log("No routine folders found.");
        return;
      }

      console.log(`\n📁 ${folders.length} folder${folders.length !== 1 ? "s" : ""}:\n`);
      for (const folder of folders) {
        console.log(`• ${folder.title} (ID: ${folder.id})`);
      }
      console.log("");
    } catch (error) {
      console.error("Error:", error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

// Count command
program
  .command("count")
  .description("Show total workout count")
  .action(async () => {
    const client = new HevyClient(getConfig());

    try {
      const count = await client.getWorkoutCount();
      console.log(`Total workouts: ${count}`);
    } catch (error) {
      console.error("Error:", error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

// Create routine command
program
  .command("create-routine")
  .description("Create a new routine from JSON (reads from stdin or --file)")
  .option("-f, --file <path>", "Read routine JSON from file")
  .option("--json", "Output created routine as JSON")
  .action(async (options: { file?: string; json?: boolean }) => {
    const client = new HevyClient(getConfig());

    try {
      let input: string;
      
      if (options.file) {
        const fs = await import("node:fs");
        input = fs.readFileSync(options.file, "utf-8");
      } else {
        // Read from stdin
        const chunks: Buffer[] = [];
        for await (const chunk of process.stdin) {
          chunks.push(chunk);
        }
        input = Buffer.concat(chunks).toString("utf-8");
      }

      if (!input.trim()) {
        console.error("Error: No input provided. Pass JSON via stdin or --file");
        console.error("");
        console.error("Example JSON:");
        console.error(JSON.stringify({
          routine: {
            title: "Push Day",
            notes: "Focus on chest and triceps",
            exercises: [
              {
                exercise_template_id: "79D0BB3A",
                notes: "Warm up properly",
                rest_seconds: 90,
                sets: [
                  { type: "warmup", weight_kg: 20, reps: 15 },
                  { type: "normal", weight_kg: 60, reps: 10 },
                  { type: "normal", weight_kg: 60, reps: 10 },
                  { type: "normal", weight_kg: 60, reps: 10 }
                ]
              }
            ]
          }
        }, null, 2));
        process.exit(1);
      }

      const routineData = JSON.parse(input);
      const routine = await client.createRoutine(routineData);

      if (options.json) {
        console.log(JSON.stringify(routine, null, 2));
      } else {
        console.log(`✅ Created routine: ${routine.title}`);
        console.log(`   ID: ${routine.id}`);
        console.log(`   Exercises: ${routine.exercises.length}`);
      }
    } catch (error) {
      console.error("Error:", error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

// Create routine folder command
program
  .command("create-folder <name>")
  .description("Create a new routine folder")
  .option("--json", "Output created folder as JSON")
  .action(async (name: string, options: { json?: boolean }) => {
    const client = new HevyClient(getConfig());

    try {
      const folder = await client.createRoutineFolder({
        routine_folder: { title: name }
      });

      if (options.json) {
        console.log(JSON.stringify(folder, null, 2));
      } else {
        console.log(`✅ Created folder: ${folder.title}`);
        console.log(`   ID: ${folder.id}`);
      }
    } catch (error) {
      console.error("Error:", error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

// Update routine command
program
  .command("update-routine <id>")
  .description("Update an existing routine from JSON (reads from stdin or --file)")
  .option("-f, --file <path>", "Read routine JSON from file")
  .option("--json", "Output updated routine as JSON")
  .action(async (id: string, options: { file?: string; json?: boolean }) => {
    const client = new HevyClient(getConfig());

    try {
      let input: string;
      
      if (options.file) {
        const fs = await import("node:fs");
        input = fs.readFileSync(options.file, "utf-8");
      } else {
        const chunks: Buffer[] = [];
        for await (const chunk of process.stdin) {
          chunks.push(chunk);
        }
        input = Buffer.concat(chunks).toString("utf-8");
      }

      if (!input.trim()) {
        console.error("Error: No input provided. Pass JSON via stdin or --file");
        process.exit(1);
      }

      const routineData = JSON.parse(input);
      const routine = await client.updateRoutine(id, routineData);

      if (options.json) {
        console.log(JSON.stringify(routine, null, 2));
      } else {
        console.log(`✅ Updated routine: ${routine.title}`);
        console.log(`   ID: ${routine.id}`);
        console.log(`   Exercises: ${routine.exercises.length}`);
      }
    } catch (error) {
      console.error("Error:", error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

// Create custom exercise command
program
  .command("create-exercise")
  .description("Create a custom exercise template")
  .requiredOption("--title <name>", "Exercise name")
  .requiredOption("--muscle <group>", "Primary muscle group")
  .option("--type <type>", "Exercise type", "weight_reps")
  .option("--equipment <category>", "Equipment category", "none")
  .option("--other-muscles <groups>", "Secondary muscles (comma-separated)")
  .option("--force", "Create even if exercise with same name exists")
  .option("--json", "Output created exercise as JSON")
  .action(async (options: { 
    title: string; 
    muscle: string; 
    type: string; 
    equipment: string;
    otherMuscles?: string;
    force?: boolean;
    json?: boolean 
  }) => {
    const client = new HevyClient(getConfig());

    try {
      // Check for existing exercise with same name (unless --force)
      if (!options.force) {
        const existing = await client.searchExerciseTemplates(options.title);
        const exactMatch = existing.find(
          e => e.title.toLowerCase() === options.title.toLowerCase()
        );
        
        if (exactMatch) {
          console.error(`❌ Exercise "${exactMatch.title}" already exists!`);
          console.error(`   ID: ${exactMatch.id}`);
          console.error(`   Muscle: ${exactMatch.primary_muscle_group}`);
          console.error(`   Type: ${exactMatch.type}`);
          console.error(`   Custom: ${exactMatch.is_custom ? "yes" : "no"}`);
          console.error("");
          console.error("Use --force to create a duplicate anyway.");
          process.exit(1);
        }
      }

      const exercise = await client.createExerciseTemplate({
        exercise: {
          title: options.title,
          muscle_group: options.muscle as any,
          exercise_type: options.type as any,
          equipment_category: options.equipment as any,
          other_muscles: options.otherMuscles?.split(",").map(m => m.trim()) as any,
        }
      });

      if (options.json) {
        console.log(JSON.stringify(exercise, null, 2));
      } else {
        console.log(`✅ Created exercise: ${exercise.title}`);
        console.log(`   ID: ${exercise.id}`);
        console.log(`   Muscle: ${exercise.primary_muscle_group}`);
        console.log(`   Type: ${exercise.type}`);
      }
    } catch (error) {
      console.error("Error:", error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

program.parse();
