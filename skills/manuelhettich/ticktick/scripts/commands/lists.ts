import { api, type Project } from "../api";

interface ListsOptions {
  json?: boolean;
}

function formatProject(project: Project): string {
  const color = project.color ? ` (${project.color})` : "";
  const closed = project.closed ? " [closed]" : "";
  return `• ${project.name}${color}${closed}\n  id: ${project.id}`;
}

export async function listsCommand(options: ListsOptions): Promise<void> {
  try {
    const projects = await api.listProjects();

    if (options.json) {
      console.log(JSON.stringify(projects, null, 2));
      return;
    }

    if (projects.length === 0) {
      console.log("No projects found.");
      return;
    }

    console.log(`\nProjects (${projects.length}):\n`);
    for (const project of projects) {
      console.log(formatProject(project));
      console.log();
    }
  } catch (error) {
    console.error(
      `Error: ${error instanceof Error ? error.message : String(error)}`
    );
    process.exit(1);
  }
}
