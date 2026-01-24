import { Command } from 'commander';
import chalk from 'chalk';
import Table from 'cli-table3';
import { listMessages, getMessage, createMessage } from '../lib/api.js';
import { isAuthenticated } from '../lib/config.js';

export function createMessagesCommands(): Command {
  const messages = new Command('messages')
    .description('Manage messages');

  messages
    .command('list')
    .description('List messages in a project')
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
        const messageList = await listMessages(projectId);

        if (options.json) {
          console.log(JSON.stringify(messageList, null, 2));
          return;
        }

        if (messageList.length === 0) {
          console.log(chalk.yellow('No messages found.'));
          return;
        }

        const table = new Table({
          head: ['ID', 'Subject', 'Author', 'Date', 'Comments'],
          colWidths: [12, 35, 20, 12, 10],
          wordWrap: true
        });

        messageList.forEach(msg => {
          table.push([
            msg.id,
            msg.subject.substring(0, 32) + (msg.subject.length > 32 ? '...' : ''),
            msg.creator?.name || '-',
            new Date(msg.created_at).toLocaleDateString(),
            msg.comments_count
          ]);
        });

        console.log(table.toString());
        console.log(chalk.dim(`\nTotal: ${messageList.length} messages`));
      } catch (error) {
        console.error(chalk.red('Failed to list messages:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  messages
    .command('get <id>')
    .description('Get message details')
    .requiredOption('-p, --project <id>', 'Project ID')
    .option('--json', 'Output as JSON')
    .action(async (id: string, options) => {
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
        const messageId = parseInt(id, 10);
        if (isNaN(messageId)) {
          console.error(chalk.red('Invalid message ID: must be a number'));
          process.exit(1);
        }
        const message = await getMessage(projectId, messageId);

        if (options.json) {
          console.log(JSON.stringify(message, null, 2));
          return;
        }

        console.log(chalk.bold(message.subject));
        console.log(chalk.dim(`ID: ${message.id}`));
        console.log(chalk.dim(`Author: ${message.creator?.name || '-'}`));
        console.log(chalk.dim(`Created: ${new Date(message.created_at).toLocaleString()}`));
        console.log(chalk.dim(`Comments: ${message.comments_count}`));
        console.log(chalk.dim(`URL: ${message.app_url}`));
        console.log(chalk.dim('\nContent:'));
        console.log(message.content || '-');
      } catch (error) {
        console.error(chalk.red('Failed to get message:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  messages
    .command('create')
    .description('Create a message')
    .requiredOption('-p, --project <id>', 'Project ID')
    .requiredOption('-s, --subject <subject>', 'Message subject')
    .option('-c, --content <content>', 'Message content (HTML)')
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
        const message = await createMessage(projectId, options.subject, options.content);

        if (options.json) {
          console.log(JSON.stringify(message, null, 2));
          return;
        }

        console.log(chalk.green('✓ Message created'));
        console.log(chalk.dim(`ID: ${message.id}`));
        console.log(chalk.dim(`Subject: ${message.subject}`));
        console.log(chalk.dim(`URL: ${message.app_url}`));
      } catch (error) {
        console.error(chalk.red('Failed to create message:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  return messages;
}
