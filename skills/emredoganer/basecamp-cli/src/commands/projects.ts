import { Command } from 'commander';
import chalk from 'chalk';
import Table from 'cli-table3';
import { listProjects, getProject, createProject, archiveProject } from '../lib/api.js';
import { isAuthenticated } from '../lib/config.js';

export function createProjectsCommands(): Command {
  const projects = new Command('projects')
    .description('Manage Basecamp projects');

  projects
    .command('list')
    .description('List all projects')
    .option('--json', 'Output as JSON')
    .action(async (options) => {
      if (!isAuthenticated()) {
        console.log(chalk.yellow('Not authenticated. Run "basecamp auth login" to login.'));
        return;
      }

      try {
        const projectList = await listProjects();

        if (options.json) {
          console.log(JSON.stringify(projectList, null, 2));
          return;
        }

        if (projectList.length === 0) {
          console.log(chalk.yellow('No projects found.'));
          return;
        }

        const table = new Table({
          head: ['ID', 'Name', 'Status', 'Description'],
          colWidths: [12, 30, 12, 40],
          wordWrap: true
        });

        projectList.forEach(project => {
          table.push([
            project.id,
            project.name,
            project.status,
            project.description?.substring(0, 37) + (project.description?.length > 37 ? '...' : '') || '-'
          ]);
        });

        console.log(table.toString());
        console.log(chalk.dim(`\nTotal: ${projectList.length} projects`));
      } catch (error) {
        console.error(chalk.red('Failed to list projects:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  projects
    .command('get <id>')
    .description('Get project details')
    .option('--json', 'Output as JSON')
    .action(async (id: string, options) => {
      if (!isAuthenticated()) {
        console.log(chalk.yellow('Not authenticated. Run "basecamp auth login" to login.'));
        return;
      }

      try {
        const projectId = parseInt(id, 10);
        if (isNaN(projectId)) {
          console.error(chalk.red('Invalid ID: must be a number'));
          process.exit(1);
        }
        const project = await getProject(projectId);

        if (options.json) {
          console.log(JSON.stringify(project, null, 2));
          return;
        }

        console.log(chalk.bold(project.name));
        console.log(chalk.dim(`ID: ${project.id}`));
        console.log(chalk.dim(`Status: ${project.status}`));
        console.log(chalk.dim(`Purpose: ${project.purpose || '-'}`));
        console.log(chalk.dim(`Description: ${project.description || '-'}`));
        console.log(chalk.dim(`Created: ${new Date(project.created_at).toLocaleDateString()}`));
        console.log(chalk.dim(`URL: ${project.app_url}`));

        console.log(chalk.dim('\nEnabled tools:'));
        project.dock
          .filter(d => d.enabled)
          .forEach(d => {
            console.log(chalk.dim(`  - ${d.title} (${d.name})`));
          });
      } catch (error) {
        console.error(chalk.red('Failed to get project:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  projects
    .command('create')
    .description('Create a new project')
    .requiredOption('-n, --name <name>', 'Project name')
    .option('-d, --description <description>', 'Project description')
    .option('--json', 'Output as JSON')
    .action(async (options) => {
      if (!isAuthenticated()) {
        console.log(chalk.yellow('Not authenticated. Run "basecamp auth login" to login.'));
        return;
      }

      try {
        const project = await createProject(options.name, options.description);

        if (options.json) {
          console.log(JSON.stringify(project, null, 2));
          return;
        }

        console.log(chalk.green('✓ Project created'));
        console.log(chalk.dim(`ID: ${project.id}`));
        console.log(chalk.dim(`Name: ${project.name}`));
        console.log(chalk.dim(`URL: ${project.app_url}`));
      } catch (error) {
        console.error(chalk.red('Failed to create project:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  projects
    .command('archive <id>')
    .description('Archive a project')
    .action(async (id: string) => {
      if (!isAuthenticated()) {
        console.log(chalk.yellow('Not authenticated. Run "basecamp auth login" to login.'));
        return;
      }

      try {
        const projectId = parseInt(id, 10);
        if (isNaN(projectId)) {
          console.error(chalk.red('Invalid ID: must be a number'));
          process.exit(1);
        }
        await archiveProject(projectId);
        console.log(chalk.green(`✓ Project ${projectId} archived`));
      } catch (error) {
        console.error(chalk.red('Failed to archive project:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  return projects;
}
