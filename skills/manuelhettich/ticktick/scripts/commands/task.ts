import { api, PRIORITY_MAP, type CreateTaskInput, type UpdateTaskInput } from "../api";

interface TaskCreateOptions {
  list: string;
  content?: string;
  priority?: string;
  due?: string;
  tag?: string[];
  json?: boolean;
}

interface TaskUpdateOptions {
  update: boolean;
  list?: string;
  content?: string;
  priority?: string;
  due?: string;
  tag?: string[];
  json?: boolean;
}

// Check if string looks like a task ID (24-char hex)
function isTaskId(str: string): boolean {
  return /^[a-f0-9]{24}$/i.test(str);
}

function parseDueDate(dueStr: string): string {
  // Handle relative dates
  // TickTick expects full ISO datetime like "2026-01-07T23:00:00.000+0000"
  const now = new Date();
  const lowerDue = dueStr.toLowerCase();

  // Helper to format as end-of-day ISO string (TickTick needs +0000 not Z)
  const toEndOfDay = (d: Date): string => {
    d.setHours(23, 59, 59, 0);
    return d.toISOString().replace("Z", "+0000");
  };

  if (lowerDue === "today") {
    return toEndOfDay(now);
  }
  if (lowerDue === "tomorrow") {
    now.setDate(now.getDate() + 1);
    return toEndOfDay(now);
  }
  if (lowerDue.match(/^in (\d+) days?$/i)) {
    const match = lowerDue.match(/^in (\d+) days?$/i);
    if (match) {
      now.setDate(now.getDate() + parseInt(match[1], 10));
      return toEndOfDay(now);
    }
  }
  if (lowerDue.match(/^next (monday|tuesday|wednesday|thursday|friday|saturday|sunday)$/i)) {
    const match = lowerDue.match(/^next (monday|tuesday|wednesday|thursday|friday|saturday|sunday)$/i);
    if (match) {
      const days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
      const targetDay = days.indexOf(match[1].toLowerCase());
      const currentDay = now.getDay();
      let daysUntil = targetDay - currentDay;
      if (daysUntil <= 0) daysUntil += 7;
      now.setDate(now.getDate() + daysUntil);
      return toEndOfDay(now);
    }
  }

  // Try parsing as ISO date
  const parsed = new Date(dueStr);
  if (!isNaN(parsed.getTime())) {
    return parsed.toISOString().replace("Z", "+0000");
  }

  throw new Error(`Invalid date format: ${dueStr}. Try 'today', 'tomorrow', 'in 3 days', or ISO date.`);
}

export async function taskCreateCommand(
  title: string,
  options: TaskCreateOptions
): Promise<void> {
  try {
    // Find the project
    const project = await api.findProjectByName(options.list);
    if (!project) {
      console.error(`Project not found: ${options.list}`);
      process.exit(1);
    }

    const input: CreateTaskInput = {
      title,
      projectId: project.id,
    };

    if (options.content) {
      input.content = options.content;
    }

    if (options.priority) {
      const priority = PRIORITY_MAP[options.priority.toLowerCase()];
      if (priority === undefined) {
        console.error(
          `Invalid priority: ${options.priority}. Use none, low, medium, or high.`
        );
        process.exit(1);
      }
      input.priority = priority;
    }

    if (options.due) {
      input.dueDate = parseDueDate(options.due);
    }

    if (options.tag && options.tag.length > 0) {
      input.tags = options.tag;
    }

    const task = await api.createTask(input);

    if (options.json) {
      console.log(JSON.stringify(task, null, 2));
      return;
    }

    console.log(`✓ Task created: "${task.title}"`);
    console.log(`  ID: ${task.id}`);
    console.log(`  Project: ${project.name}`);
    if (task.dueDate) {
      console.log(`  Due: ${new Date(task.dueDate).toLocaleDateString()}`);
    }
  } catch (error) {
    console.error(
      `Error: ${error instanceof Error ? error.message : String(error)}`
    );
    process.exit(1);
  }
}

export async function taskUpdateCommand(
  taskNameOrId: string,
  options: TaskUpdateOptions
): Promise<void> {
  try {
    let found: { task: { id: string; title: string }; projectId: string } | undefined;

    // If it looks like an ID and no --list specified, use findTaskById
    if (isTaskId(taskNameOrId) && !options.list) {
      found = await api.findTaskById(taskNameOrId);
    } else {
      // Search by title (with optional project filter)
      found = await api.findTaskByTitle(taskNameOrId, options.list);
    }

    if (!found) {
      console.error(`Task not found: ${taskNameOrId}`);
      process.exit(1);
    }

    const { task, projectId } = found;

    const input: UpdateTaskInput = {
      id: task.id,
      projectId: projectId,
    };

    // Only include fields that are explicitly set
    if (options.content !== undefined) {
      input.content = options.content;
    }

    if (options.priority) {
      const priority = PRIORITY_MAP[options.priority.toLowerCase()];
      if (priority === undefined) {
        console.error(
          `Invalid priority: ${options.priority}. Use none, low, medium, or high.`
        );
        process.exit(1);
      }
      input.priority = priority;
    }

    if (options.due) {
      input.dueDate = parseDueDate(options.due);
    }

    if (options.tag && options.tag.length > 0) {
      input.tags = options.tag;
    }

    const updated = await api.updateTask(input);

    if (options.json) {
      console.log(JSON.stringify(updated, null, 2));
      return;
    }

    console.log(`✓ Task updated: "${updated.title}"`);
    console.log(`  ID: ${updated.id}`);
  } catch (error) {
    console.error(
      `Error: ${error instanceof Error ? error.message : String(error)}`
    );
    process.exit(1);
  }
}
