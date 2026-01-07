import { api, type CreateProjectInput, type UpdateProjectInput } from "../api";

interface ListCreateOptions {
  color?: string;
  json?: boolean;
}

interface ListUpdateOptions {
  update: boolean;
  name?: string;
  color?: string;
  json?: boolean;
}

function normalizeColor(color: string): string {
  // TickTick expects colors in hex format
  if (color.startsWith("#")) {
    return color;
  }
  return `#${color}`;
}

export async function listCreateCommand(
  name: string,
  options: ListCreateOptions
): Promise<void> {
  try {
    const input: CreateProjectInput = { name };

    if (options.color) {
      input.color = normalizeColor(options.color);
    }

    const project = await api.createProject(input);

    if (options.json) {
      console.log(JSON.stringify(project, null, 2));
      return;
    }

    console.log(`✓ Project created: "${project.name}"`);
    console.log(`  ID: ${project.id}`);
    if (project.color) {
      console.log(`  Color: ${project.color}`);
    }
  } catch (error) {
    console.error(
      `Error: ${error instanceof Error ? error.message : String(error)}`
    );
    process.exit(1);
  }
}

export async function listUpdateCommand(
  nameOrId: string,
  options: ListUpdateOptions
): Promise<void> {
  try {
    // Find the project
    const project = await api.findProjectByName(nameOrId);
    if (!project) {
      console.error(`Project not found: ${nameOrId}`);
      process.exit(1);
    }

    const input: UpdateProjectInput = { id: project.id };

    if (options.name) {
      input.name = options.name;
    }

    if (options.color) {
      input.color = normalizeColor(options.color);
    }

    const updated = await api.updateProject(input);

    if (options.json) {
      console.log(JSON.stringify(updated, null, 2));
      return;
    }

    console.log(`✓ Project updated: "${updated.name}"`);
    console.log(`  ID: ${updated.id}`);
    if (updated.color) {
      console.log(`  Color: ${updated.color}`);
    }
  } catch (error) {
    console.error(
      `Error: ${error instanceof Error ? error.message : String(error)}`
    );
    process.exit(1);
  }
}
