import { Command } from 'commander';
import chalk from 'chalk';
import Table from 'cli-table3';
import {
  listTodoLists,
  getTodoList,
  createTodoList,
  listTodos,
  getTodo,
  createTodo,
  updateTodo,
  completeTodo,
  uncompleteTodo
} from '../lib/api.js';
import { isAuthenticated } from '../lib/config.js';

export function createTodoListsCommands(): Command {
  const todolists = new Command('todolists')
    .description('Manage to-do lists');

  todolists
    .command('list')
    .description('List to-do lists in a project')
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
        const lists = await listTodoLists(projectId);

        if (options.json) {
          console.log(JSON.stringify(lists, null, 2));
          return;
        }

        if (lists.length === 0) {
          console.log(chalk.yellow('No to-do lists found.'));
          return;
        }

        const table = new Table({
          head: ['ID', 'Name', 'Progress', 'Description'],
          colWidths: [12, 25, 15, 35],
          wordWrap: true
        });

        lists.forEach(list => {
          table.push([
            list.id,
            list.name,
            list.completed_ratio || '0/0',
            list.description?.substring(0, 32) + (list.description?.length > 32 ? '...' : '') || '-'
          ]);
        });

        console.log(table.toString());
        console.log(chalk.dim(`\nTotal: ${lists.length} lists`));
      } catch (error) {
        console.error(chalk.red('Failed to list to-do lists:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  todolists
    .command('create')
    .description('Create a to-do list')
    .requiredOption('-p, --project <id>', 'Project ID')
    .requiredOption('-n, --name <name>', 'List name')
    .option('-d, --description <description>', 'List description')
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
        const list = await createTodoList(projectId, options.name, options.description);

        if (options.json) {
          console.log(JSON.stringify(list, null, 2));
          return;
        }

        console.log(chalk.green('✓ To-do list created'));
        console.log(chalk.dim(`ID: ${list.id}`));
        console.log(chalk.dim(`Name: ${list.name}`));
      } catch (error) {
        console.error(chalk.red('Failed to create to-do list:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  return todolists;
}

export function createTodosCommands(): Command {
  const todos = new Command('todos')
    .description('Manage to-dos');

  todos
    .command('list')
    .description('List to-dos in a to-do list')
    .requiredOption('-p, --project <id>', 'Project ID')
    .requiredOption('-l, --list <id>', 'To-do list ID')
    .option('--completed', 'Show completed to-dos')
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
        const listId = parseInt(options.list, 10);
        if (isNaN(listId)) {
          console.error(chalk.red('Invalid list ID: must be a number'));
          process.exit(1);
        }
        const todoList = await listTodos(projectId, listId, options.completed);

        if (options.json) {
          console.log(JSON.stringify(todoList, null, 2));
          return;
        }

        if (todoList.length === 0) {
          console.log(chalk.yellow('No to-dos found.'));
          return;
        }

        const table = new Table({
          head: ['ID', 'Status', 'Content', 'Due', 'Assignees'],
          colWidths: [12, 10, 35, 12, 20],
          wordWrap: true
        });

        todoList.forEach(todo => {
          table.push([
            todo.id,
            todo.completed ? chalk.green('✓') : chalk.dim('○'),
            todo.content.substring(0, 32) + (todo.content.length > 32 ? '...' : ''),
            todo.due_on || '-',
            todo.assignees?.map(a => a.name).join(', ') || '-'
          ]);
        });

        console.log(table.toString());
        console.log(chalk.dim(`\nTotal: ${todoList.length} to-dos`));
      } catch (error) {
        console.error(chalk.red('Failed to list to-dos:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  todos
    .command('get <id>')
    .description('Get to-do details')
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
        const todoId = parseInt(id, 10);
        if (isNaN(todoId)) {
          console.error(chalk.red('Invalid todo ID: must be a number'));
          process.exit(1);
        }
        const todo = await getTodo(projectId, todoId);

        if (options.json) {
          console.log(JSON.stringify(todo, null, 2));
          return;
        }

        console.log(chalk.bold(todo.content));
        console.log(chalk.dim(`ID: ${todo.id}`));
        console.log(chalk.dim(`Status: ${todo.completed ? 'Completed' : 'Pending'}`));
        console.log(chalk.dim(`Description: ${todo.description || '-'}`));
        console.log(chalk.dim(`Due: ${todo.due_on || '-'}`));
        console.log(chalk.dim(`Starts: ${todo.starts_on || '-'}`));
        console.log(chalk.dim(`Assignees: ${todo.assignees?.map(a => a.name).join(', ') || '-'}`));
        console.log(chalk.dim(`Comments: ${todo.comments_count}`));
        console.log(chalk.dim(`URL: ${todo.app_url}`));
      } catch (error) {
        console.error(chalk.red('Failed to get to-do:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  todos
    .command('create')
    .description('Create a to-do')
    .requiredOption('-p, --project <id>', 'Project ID')
    .requiredOption('-l, --list <id>', 'To-do list ID')
    .requiredOption('-c, --content <content>', 'To-do content')
    .option('-d, --description <description>', 'To-do description')
    .option('--due <date>', 'Due date (YYYY-MM-DD)')
    .option('--starts <date>', 'Start date (YYYY-MM-DD)')
    .option('--assignees <ids>', 'Comma-separated assignee IDs')
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
        const listId = parseInt(options.list, 10);
        if (isNaN(listId)) {
          console.error(chalk.red('Invalid list ID: must be a number'));
          process.exit(1);
        }

        const todoOptions: {
          description?: string;
          due_on?: string;
          starts_on?: string;
          assignee_ids?: number[];
        } = {};

        if (options.description) todoOptions.description = options.description;
        if (options.due) todoOptions.due_on = options.due;
        if (options.starts) todoOptions.starts_on = options.starts;
        if (options.assignees) {
          todoOptions.assignee_ids = options.assignees.split(',').map((id: string) => parseInt(id.trim(), 10));
        }

        const todo = await createTodo(projectId, listId, options.content, todoOptions);

        if (options.json) {
          console.log(JSON.stringify(todo, null, 2));
          return;
        }

        console.log(chalk.green('✓ To-do created'));
        console.log(chalk.dim(`ID: ${todo.id}`));
        console.log(chalk.dim(`Content: ${todo.content}`));
      } catch (error) {
        console.error(chalk.red('Failed to create to-do:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  todos
    .command('update <id>')
    .description('Update a to-do')
    .requiredOption('-p, --project <id>', 'Project ID')
    .option('-c, --content <content>', 'New content')
    .option('-d, --description <description>', 'New description')
    .option('--due <date>', 'Due date (YYYY-MM-DD)')
    .option('--starts <date>', 'Start date (YYYY-MM-DD)')
    .option('--assignees <ids>', 'Comma-separated assignee IDs')
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
        const todoId = parseInt(id, 10);
        if (isNaN(todoId)) {
          console.error(chalk.red('Invalid todo ID: must be a number'));
          process.exit(1);
        }

        const updates: {
          content?: string;
          description?: string;
          due_on?: string | null;
          starts_on?: string | null;
          assignee_ids?: number[];
        } = {};

        if (options.content) updates.content = options.content;
        if (options.description) updates.description = options.description;
        if (options.due) updates.due_on = options.due;
        if (options.starts) updates.starts_on = options.starts;
        if (options.assignees) {
          updates.assignee_ids = options.assignees.split(',').map((id: string) => parseInt(id.trim(), 10));
        }

        const todo = await updateTodo(projectId, todoId, updates);

        if (options.json) {
          console.log(JSON.stringify(todo, null, 2));
          return;
        }

        console.log(chalk.green('✓ To-do updated'));
        console.log(chalk.dim(`ID: ${todo.id}`));
        console.log(chalk.dim(`Content: ${todo.content}`));
      } catch (error) {
        console.error(chalk.red('Failed to update to-do:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  todos
    .command('complete <id>')
    .description('Mark a to-do as complete')
    .requiredOption('-p, --project <id>', 'Project ID')
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
        const todoId = parseInt(id, 10);
        if (isNaN(todoId)) {
          console.error(chalk.red('Invalid todo ID: must be a number'));
          process.exit(1);
        }
        await completeTodo(projectId, todoId);
        console.log(chalk.green(`✓ To-do ${todoId} completed`));
      } catch (error) {
        console.error(chalk.red('Failed to complete to-do:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  todos
    .command('uncomplete <id>')
    .description('Mark a to-do as incomplete')
    .requiredOption('-p, --project <id>', 'Project ID')
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
        const todoId = parseInt(id, 10);
        if (isNaN(todoId)) {
          console.error(chalk.red('Invalid todo ID: must be a number'));
          process.exit(1);
        }
        await uncompleteTodo(projectId, todoId);
        console.log(chalk.green(`✓ To-do ${todoId} marked as incomplete`));
      } catch (error) {
        console.error(chalk.red('Failed to uncomplete to-do:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  return todos;
}
