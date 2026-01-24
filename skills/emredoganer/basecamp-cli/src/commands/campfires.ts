import { Command } from 'commander';
import chalk from 'chalk';
import Table from 'cli-table3';
import { listCampfires, getCampfireLines, sendCampfireLine } from '../lib/api.js';
import { isAuthenticated } from '../lib/config.js';

export function createCampfiresCommands(): Command {
  const campfires = new Command('campfires')
    .description('Manage campfires (chat)');

  campfires
    .command('list')
    .description('List campfires in a project')
    .requiredOption('-p, --project <id>', 'Project ID')
    .option('--json', 'Output as JSON')
    .action(async (options) => {
      if (!isAuthenticated()) {
        console.log(chalk.yellow('Not authenticated. Run "basecamp auth login" to login.'));
        return;
      }

      try {
        const projectId = parseInt(options.project, 10);
        if (isNaN(projectId)) {
          console.error(chalk.red('Invalid project ID: must be a number'));
          process.exit(1);
        }
        const campfireList = await listCampfires(projectId);

        if (options.json) {
          console.log(JSON.stringify(campfireList, null, 2));
          return;
        }

        if (campfireList.length === 0) {
          console.log(chalk.yellow('No campfires found.'));
          return;
        }

        const table = new Table({
          head: ['ID', 'Title', 'Topic'],
          colWidths: [12, 30, 40],
          wordWrap: true
        });

        campfireList.forEach(campfire => {
          table.push([
            campfire.id,
            campfire.title || 'Campfire',
            campfire.topic || '-'
          ]);
        });

        console.log(table.toString());
      } catch (error) {
        console.error(chalk.red('Failed to list campfires:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  campfires
    .command('lines')
    .description('Get recent campfire messages')
    .requiredOption('-p, --project <id>', 'Project ID')
    .requiredOption('-c, --campfire <id>', 'Campfire ID')
    .option('-n, --limit <number>', 'Number of lines to show', '20')
    .option('--json', 'Output as JSON')
    .action(async (options) => {
      if (!isAuthenticated()) {
        console.log(chalk.yellow('Not authenticated. Run "basecamp auth login" to login.'));
        return;
      }

      try {
        const projectId = parseInt(options.project, 10);
        if (isNaN(projectId)) {
          console.error(chalk.red('Invalid project ID: must be a number'));
          process.exit(1);
        }
        const campfireId = parseInt(options.campfire, 10);
        if (isNaN(campfireId)) {
          console.error(chalk.red('Invalid campfire ID: must be a number'));
          process.exit(1);
        }
        const limit = parseInt(options.limit, 10);
        if (isNaN(limit)) {
          console.error(chalk.red('Invalid limit: must be a number'));
          process.exit(1);
        }
        const lines = await getCampfireLines(projectId, campfireId);

        if (options.json) {
          console.log(JSON.stringify(lines, null, 2));
          return;
        }

        if (lines.length === 0) {
          console.log(chalk.yellow('No messages found.'));
          return;
        }

        const displayLines = lines.slice(-limit);

        displayLines.forEach(line => {
          const time = new Date(line.created_at).toLocaleTimeString();
          const author = line.creator?.name || 'Unknown';
          console.log(chalk.dim(`[${time}]`) + ` ${chalk.blue(author)}: ${line.content}`);
        });

        console.log(chalk.dim(`\nShowing ${displayLines.length} of ${lines.length} messages`));
      } catch (error) {
        console.error(chalk.red('Failed to get campfire lines:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  campfires
    .command('send')
    .description('Send a message to a campfire')
    .requiredOption('-p, --project <id>', 'Project ID')
    .requiredOption('-c, --campfire <id>', 'Campfire ID')
    .requiredOption('-m, --message <message>', 'Message content')
    .option('--json', 'Output as JSON')
    .action(async (options) => {
      if (!isAuthenticated()) {
        console.log(chalk.yellow('Not authenticated. Run "basecamp auth login" to login.'));
        return;
      }

      try {
        const projectId = parseInt(options.project, 10);
        if (isNaN(projectId)) {
          console.error(chalk.red('Invalid project ID: must be a number'));
          process.exit(1);
        }
        const campfireId = parseInt(options.campfire, 10);
        if (isNaN(campfireId)) {
          console.error(chalk.red('Invalid campfire ID: must be a number'));
          process.exit(1);
        }
        const line = await sendCampfireLine(projectId, campfireId, options.message);

        if (options.json) {
          console.log(JSON.stringify(line, null, 2));
          return;
        }

        console.log(chalk.green('✓ Message sent'));
      } catch (error) {
        console.error(chalk.red('Failed to send message:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  return campfires;
}
