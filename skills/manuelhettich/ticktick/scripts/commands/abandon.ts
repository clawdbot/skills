import { api } from "../api";

interface AbandonOptions {
  list?: string;
  json?: boolean;
}

// Check if string looks like a task ID (24-char hex)
function isTaskId(str: string): boolean {
  return /^[a-f0-9]{24}$/i.test(str);
}

export async function abandonCommand(
  taskNameOrId: string,
  options: AbandonOptions
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

    // Status -1 = won't do / abandoned in TickTick
    const result = await api.updateTask({
      id: task.id,
      projectId: projectId,
      status: -1,
    });

    if (options.json) {
      console.log(JSON.stringify(result, null, 2));
      return;
    }

    console.log(`✓ Abandoned: "${task.title}"`);
  } catch (error) {
    console.error(
      `Error: ${error instanceof Error ? error.message : String(error)}`
    );
    process.exit(1);
  }
}
