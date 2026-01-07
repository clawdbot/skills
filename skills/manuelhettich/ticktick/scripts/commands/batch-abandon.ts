import { api, UpdateTaskInput } from "../api";

interface BatchAbandonOptions {
  json?: boolean;
}

// Check if string looks like a task ID (24-char hex)
function isTaskId(str: string): boolean {
  return /^[a-f0-9]{24}$/i.test(str);
}

export async function batchAbandonCommand(
  taskIds: string[],
  options: BatchAbandonOptions
): Promise<void> {
  if (taskIds.length === 0) {
    console.error("Error: At least one task ID is required");
    process.exit(1);
  }

  // Validate all inputs are task IDs
  const invalidIds = taskIds.filter((id) => !isTaskId(id));
  if (invalidIds.length > 0) {
    console.error(
      `Error: Invalid task ID format: ${invalidIds.join(", ")}\n` +
        "Task IDs must be 24-character hex strings."
    );
    process.exit(1);
  }

  try {
    // Look up each task to get projectId
    const updates: UpdateTaskInput[] = [];
    const notFound: string[] = [];

    for (const taskId of taskIds) {
      const found = await api.findTaskById(taskId);
      if (found) {
        updates.push({
          id: found.task.id,
          projectId: found.projectId,
          status: -1, // -1 = won't do / abandoned
        });
      } else {
        notFound.push(taskId);
      }
    }

    if (notFound.length > 0) {
      console.error(`Warning: Tasks not found: ${notFound.join(", ")}`);
    }

    if (updates.length === 0) {
      console.error("Error: No valid tasks to abandon");
      process.exit(1);
    }

    // Send batch request
    const result = await api.batchTasks({ update: updates });

    if (options.json) {
      console.log(
        JSON.stringify(
          {
            abandoned: updates.map((u) => u.id),
            notFound,
            response: result,
          },
          null,
          2
        )
      );
      return;
    }

    // Report results
    const successCount = updates.length - (result.id2error ? Object.keys(result.id2error).length : 0);
    console.log(`✓ Abandoned ${successCount} task(s)`);

    if (result.id2error && Object.keys(result.id2error).length > 0) {
      console.error("Errors:");
      for (const [id, error] of Object.entries(result.id2error)) {
        console.error(`  ${id}: ${error}`);
      }
    }

    if (notFound.length > 0) {
      console.log(`Skipped ${notFound.length} task(s) not found`);
    }
  } catch (error) {
    console.error(
      `Error: ${error instanceof Error ? error.message : String(error)}`
    );
    process.exit(1);
  }
}
