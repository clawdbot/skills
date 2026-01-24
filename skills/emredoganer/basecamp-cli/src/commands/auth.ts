import { Command } from 'commander';
import chalk from 'chalk';
import Table from 'cli-table3';
import { startOAuthFlow, logout, getAuthorization } from '../lib/auth.js';
import {
  isAuthenticated,
  setClientConfig,
  setCurrentAccountId,
  getCurrentAccountId,
  getTokens
} from '../lib/config.js';

export function createAuthCommands(): Command {
  const auth = new Command('auth')
    .description('Manage authentication');

  auth
    .command('login')
    .description('Login to Basecamp via OAuth')
    .action(async () => {
      try {
        if (isAuthenticated()) {
          console.log(chalk.yellow('Already authenticated. Use "basecamp auth logout" to logout first.'));
          return;
        }

        console.log(chalk.blue('Starting OAuth flow...'));
        await startOAuthFlow();
        console.log(chalk.green('✓ Successfully authenticated!'));

        // Fetch and display accounts
        const authorization = await getAuthorization();
        console.log(chalk.dim(`\nLogged in as: ${authorization.identity.first_name} ${authorization.identity.last_name}`));

        if (authorization.accounts.length > 0) {
          console.log(chalk.dim('\nAvailable accounts:'));
          authorization.accounts
            .filter(a => a.product === 'bc3')
            .forEach(a => {
              console.log(chalk.dim(`  ${a.id}: ${a.name}`));
            });

          // Auto-select first Basecamp 3 account
          const bc3Account = authorization.accounts.find(a => a.product === 'bc3');
          if (bc3Account) {
            setCurrentAccountId(bc3Account.id);
            console.log(chalk.green(`\n✓ Auto-selected account: ${bc3Account.name} (${bc3Account.id})`));
          }
        }
      } catch (error) {
        console.error(chalk.red('Login failed:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  auth
    .command('logout')
    .description('Logout from Basecamp')
    .action(() => {
      logout();
      console.log(chalk.green('✓ Successfully logged out'));
    });

  auth
    .command('status')
    .description('Show authentication status')
    .action(async () => {
      if (!isAuthenticated()) {
        console.log(chalk.yellow('Not authenticated. Run "basecamp auth login" to login.'));
        return;
      }

      try {
        const authorization = await getAuthorization();
        const tokens = getTokens();
        const currentAccountId = getCurrentAccountId();

        console.log(chalk.green('✓ Authenticated'));
        console.log(chalk.dim(`User: ${authorization.identity.first_name} ${authorization.identity.last_name}`));
        console.log(chalk.dim(`Email: ${authorization.identity.email_address}`));
        console.log(chalk.dim(`Current Account ID: ${currentAccountId || 'Not set'}`));

        if (tokens?.expires_at) {
          const expiresIn = Math.round((tokens.expires_at - Date.now()) / 1000 / 60);
          console.log(chalk.dim(`Token expires in: ${expiresIn} minutes`));
        }
      } catch (error) {
        console.error(chalk.red('Failed to get status:'), error instanceof Error ? error.message : error);
      }
    });

  auth
    .command('configure')
    .description('Configure OAuth client settings (client ID and redirect URI only)')
    .requiredOption('--client-id <id>', 'OAuth Client ID')
    .option('--redirect-uri <uri>', 'OAuth Redirect URI', 'http://localhost:9292/callback')
    .action((options) => {
      setClientConfig(options.clientId, options.redirectUri);
      console.log(chalk.green('✓ OAuth client configuration saved'));
      console.log(chalk.yellow('\nIMPORTANT: For security, the client secret is NOT stored in the config file.'));
      console.log(chalk.yellow('You must set it via environment variable before running "basecamp auth login":'));
      console.log(chalk.cyan('\n  export BASECAMP_CLIENT_SECRET="your-client-secret"\n'));
      console.log(chalk.dim('Add this to your shell profile (~/.bashrc, ~/.zshrc, etc.) for persistence.'));
    });

  return auth;
}

export function createAccountsCommand(): Command {
  const accounts = new Command('accounts')
    .description('List available Basecamp accounts')
    .action(async () => {
      if (!isAuthenticated()) {
        console.log(chalk.yellow('Not authenticated. Run "basecamp auth login" to login.'));
        return;
      }

      try {
        const authorization = await getAuthorization();
        const currentAccountId = getCurrentAccountId();
        const bc3Accounts = authorization.accounts.filter(a => a.product === 'bc3');

        if (bc3Accounts.length === 0) {
          console.log(chalk.yellow('No Basecamp 3 accounts found.'));
          return;
        }

        const table = new Table({
          head: ['ID', 'Name', 'Current'],
          colWidths: [15, 40, 10]
        });

        bc3Accounts.forEach(account => {
          table.push([
            account.id,
            account.name,
            account.id === currentAccountId ? chalk.green('✓') : ''
          ]);
        });

        console.log(table.toString());
      } catch (error) {
        console.error(chalk.red('Failed to list accounts:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  return accounts;
}

export function createAccountCommand(): Command {
  const account = new Command('account')
    .description('Manage current account');

  account
    .command('set <id>')
    .description('Set current Basecamp account')
    .action(async (id: string) => {
      try {
        const accountId = parseInt(id, 10);
        if (isNaN(accountId)) {
          console.error(chalk.red('Invalid account ID'));
          process.exit(1);
        }

        const authorization = await getAuthorization();
        const account = authorization.accounts.find(a => a.id === accountId);

        if (!account) {
          console.error(chalk.red(`Account ${accountId} not found`));
          process.exit(1);
        }

        if (account.product !== 'bc3') {
          console.error(chalk.red('This account is not a Basecamp 3 account'));
          process.exit(1);
        }

        setCurrentAccountId(accountId);
        console.log(chalk.green(`✓ Switched to account: ${account.name} (${accountId})`));
      } catch (error) {
        console.error(chalk.red('Failed to set account:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  account
    .command('current')
    .description('Show current account')
    .action(async () => {
      const currentAccountId = getCurrentAccountId();
      if (!currentAccountId) {
        console.log(chalk.yellow('No account selected. Run "basecamp account set <id>" to select one.'));
        return;
      }

      try {
        const authorization = await getAuthorization();
        const account = authorization.accounts.find(a => a.id === currentAccountId);

        if (account) {
          console.log(`Current account: ${account.name} (${account.id})`);
        } else {
          console.log(`Current account ID: ${currentAccountId}`);
        }
      } catch (error) {
        console.log(`Current account ID: ${currentAccountId}`);
      }
    });

  return account;
}
