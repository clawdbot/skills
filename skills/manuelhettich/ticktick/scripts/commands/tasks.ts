import { api, PRIORITY_REVERSE, type Task } from "../api";

interface TaskWithProject extends Task {
  projectName?: string;
}

interface TasksOptions {
  list?: string;
  status?: "pending" | "completed";
  json?: boolean;
}

function formatDueDate(dateStr: string): string {
  const date = new Date(dateStr);
  const now = new Date();
  const tomorrow = new Date(now);
  tomorrow.setDate(tomorrow.getDate() + 1);

  // Check if it's today or tomorrow
  if (date.toDateString() === now.toDateString()) {
    return "today";
  }
  if (date.toDateString() === tomorrow.toDateString()) {
    return "tomorrow";
  }

  // Format as "Jan 7" style
  return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

function formatTask(task: TaskWithProject, showProject = false): string {
  const status = task.status === 2 ? "✓" : "○";
  const priorityIndicator =
    task.priority === 5
      ? "!!!"
      : task.priority === 3
        ? "!!"
        : task.priority === 1
          ? "!"
          : "";
  const dueStr = task.dueDate ? ` - due ${formatDueDate(task.dueDate)}` : "";
  const projectStr = showProject && task.projectName ? ` (${task.projectName})` : "";
  const shortId = task.id.slice(0, 8);

  return `${status} [${shortId}] ${priorityIndicator}${task.title}${projectStr}${dueStr}`;
}

export async function tasksCommand(options: TasksOptions): Promise<void> {
  try {
    const projects = await api.listProjects();
    const projectMap = new Map(projects.map((p) => [p.id, p.name]));

    let searchProjects = projects;
    if (options.list) {
      const project = await api.findProjectByName(options.list);
      if (!project) {
        console.error(`Project not found: ${options.list}`);
        process.exit(1);
      }
      searchProjects = [project];
    }

    const tasksWithProjects: TaskWithProject[] = [];
    for (const project of searchProjects) {
      try {
        const data = await api.getProjectData(project.id);
        if (data.tasks) {
          for (const task of data.tasks) {
            tasksWithProjects.push({
              ...task,
              projectName: projectMap.get(task.projectId) || task.projectId,
            });
          }
        }
      } catch {
        continue;
      }
    }

    // Filter by status if specified
    let filteredTasks = tasksWithProjects;
    if (options.status === "pending") {
      filteredTasks = tasksWithProjects.filter((t) => t.status !== 2);
    } else if (options.status === "completed") {
      filteredTasks = tasksWithProjects.filter((t) => t.status === 2);
    }

    if (options.json) {
      console.log(JSON.stringify(filteredTasks, null, 2));
      return;
    }

    if (filteredTasks.length === 0) {
      console.log("No tasks found.");
      return;
    }

    console.log(`\nTasks (${filteredTasks.length}):\n`);
    for (const task of filteredTasks) {
      console.log(formatTask(task, !options.list));
    }
  } catch (error) {
    console.error(
      `Error: ${error instanceof Error ? error.message : String(error)}`
    );
    process.exit(1);
  }
}
