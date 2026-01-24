import { Command } from 'commander';
import chalk from 'chalk';
import Table from 'cli-table3';
import { listPeople, getPerson, getMe } from '../lib/api.js';
import { isAuthenticated } from '../lib/config.js';

export function createPeopleCommands(): Command {
  const people = new Command('people')
    .description('Manage people');

  people
    .command('list')
    .description('List people')
    .option('-p, --project <id>', 'Project ID (optional, lists all if omitted)')
    .option('--json', 'Output as JSON')
    .action(async (options) => {
      if (!isAuthenticated()) {
        console.log(chalk.yellow('Not authenticated. Run "basecamp auth login" to login.'));
        return;
      }

      try {
        let projectId: number | undefined = undefined;
        if (options.project) {
          projectId = parseInt(options.project, 10);
          if (isNaN(projectId)) {
            console.error(chalk.red('Invalid project ID: must be a number'));
            process.exit(1);
          }
        }
        const peopleList = await listPeople(projectId);

        if (options.json) {
          console.log(JSON.stringify(peopleList, null, 2));
          return;
        }

        if (peopleList.length === 0) {
          console.log(chalk.yellow('No people found.'));
          return;
        }

        const table = new Table({
          head: ['ID', 'Name', 'Email', 'Title', 'Role'],
          colWidths: [12, 25, 30, 20, 12],
          wordWrap: true
        });

        peopleList.forEach(person => {
          let role = '';
          if (person.owner) role = 'Owner';
          else if (person.admin) role = 'Admin';
          else if (person.client) role = 'Client';
          else role = 'Member';

          table.push([
            person.id,
            person.name,
            person.email_address,
            person.title || '-',
            role
          ]);
        });

        console.log(table.toString());
        console.log(chalk.dim(`\nTotal: ${peopleList.length} people`));
      } catch (error) {
        console.error(chalk.red('Failed to list people:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  people
    .command('get <id>')
    .description('Get person details')
    .option('--json', 'Output as JSON')
    .action(async (id: string, options) => {
      if (!isAuthenticated()) {
        console.log(chalk.yellow('Not authenticated. Run "basecamp auth login" to login.'));
        return;
      }

      try {
        const personId = parseInt(id, 10);
        if (isNaN(personId)) {
          console.error(chalk.red('Invalid ID: must be a number'));
          process.exit(1);
        }
        const person = await getPerson(personId);

        if (options.json) {
          console.log(JSON.stringify(person, null, 2));
          return;
        }

        console.log(chalk.bold(person.name));
        console.log(chalk.dim(`ID: ${person.id}`));
        console.log(chalk.dim(`Email: ${person.email_address}`));
        console.log(chalk.dim(`Title: ${person.title || '-'}`));
        console.log(chalk.dim(`Bio: ${person.bio || '-'}`));
        console.log(chalk.dim(`Location: ${person.location || '-'}`));
        console.log(chalk.dim(`Time Zone: ${person.time_zone}`));
        console.log(chalk.dim(`Company: ${person.company?.name || '-'}`));

        let role = '';
        if (person.owner) role = 'Owner';
        else if (person.admin) role = 'Admin';
        else if (person.client) role = 'Client';
        else role = 'Member';
        console.log(chalk.dim(`Role: ${role}`));
      } catch (error) {
        console.error(chalk.red('Failed to get person:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  return people;
}

export function createMeCommand(): Command {
  const me = new Command('me')
    .description('Get your profile')
    .option('--json', 'Output as JSON')
    .action(async (options) => {
      if (!isAuthenticated()) {
        console.log(chalk.yellow('Not authenticated. Run "basecamp auth login" to login.'));
        return;
      }

      try {
        const person = await getMe();

        if (options.json) {
          console.log(JSON.stringify(person, null, 2));
          return;
        }

        console.log(chalk.bold(person.name));
        console.log(chalk.dim(`ID: ${person.id}`));
        console.log(chalk.dim(`Email: ${person.email_address}`));
        console.log(chalk.dim(`Title: ${person.title || '-'}`));
        console.log(chalk.dim(`Bio: ${person.bio || '-'}`));
        console.log(chalk.dim(`Location: ${person.location || '-'}`));
        console.log(chalk.dim(`Time Zone: ${person.time_zone}`));
        console.log(chalk.dim(`Company: ${person.company?.name || '-'}`));
      } catch (error) {
        console.error(chalk.red('Failed to get profile:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  return me;
}
