import { api } from "../api";

interface CompleteOptions {
  list?: string;
  json?: boolean;
}

// Check if string looks like a task ID (24-char hex)
function isTaskId(str: string): boolean {
  return /^[a-f0-9]{24}$/i.test(str);
}

export async function completeCommand(
  taskNameOrId: string,
  options: CompleteOptions
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

    await api.completeTask(projectId, task.id);

    if (options.json) {
      console.log(
        JSON.stringify(
          {
            success: true,
            task: {
              id: task.id,
              title: task.title,
              projectId: projectId,
              status: "completed",
            },
          },
          null,
          2
        )
      );
      return;
    }

    console.log(`✓ Completed: "${task.title}"`);
  } catch (error) {
    console.error(
      `Error: ${error instanceof Error ? error.message : String(error)}`
    );
    process.exit(1);
  }
}
