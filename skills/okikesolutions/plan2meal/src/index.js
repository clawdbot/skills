/**
 * Plan2Meal ClawdHub Skill - Main Entry Point
 * 
 * Handles incoming messages and routes them to appropriate command handlers.
 */

const ConvexClient = require('./convex');
const GitHubOAuth = require('./github-oauth');
const Plan2MealCommands = require('./commands');
const { isValidUrl, generateState } = require('./utils');

// Skill configuration
let config = {
  convexUrl: process.env.CONVEX_URL || 'https://gallant-bass-875.convex.cloud',
  githubClientId: process.env.GITHUB_CLIENT_ID || '',
  githubClientSecret: process.env.GITHUB_CLIENT_SECRET || '',
  clawdbotUrl: process.env.CLAWDBOT_URL || 'http://localhost:3000'
};

// Initialize clients
let oauth = null;
let commands = null;

// Session storage (in production, use proper session storage)
const sessionStore = new Map();

/**
 * Initialize the skill with configuration
 */
function initialize(customConfig = {}) {
  config = { ...config, ...customConfig };

  if (config.githubClientId && config.githubClientSecret) {
    oauth = new GitHubOAuth(
      config.githubClientId,
      config.githubClientSecret,
      config.clawdbotUrl
    );
  }

  return {
    name: 'plan2meal',
    version: '1.0.0',
    commands: getCommandPatterns()
  };
}

/**
 * Get command patterns for skill registration
 */
function getCommandPatterns() {
  return [
    { pattern: /^plan2meal\s+add\s+(.+)$/i, description: 'Add recipe from URL' },
    { pattern: /^plan2meal\s+list$/i, description: 'List your recipes' },
    { pattern: /^plan2meal\s+search\s+(.+)$/i, description: 'Search recipes' },
    { pattern: /^plan2meal\s+show\s+(.+)$/i, description: 'Show recipe details' },
    { pattern: /^plan2meal\s+delete\s+(.+)$/i, description: 'Delete a recipe' },
    { pattern: /^plan2meal\s+lists$/i, description: 'List grocery lists' },
    { pattern: /^plan2meal\s+list-show\s+(.+)$/i, description: 'Show grocery list' },
    { pattern: /^plan2meal\s+list-create\s+(.+)$/i, description: 'Create grocery list' },
    { pattern: /^plan2meal\s+list-add\s+(\S+)\s+(\S+)$/i, description: 'Add recipe to list' },
    { pattern: /^plan2meal\s+help$/i, description: 'Show help' }
  ];
}

/**
 * Get or create Convex client for a user
 */
function getConvexClient(githubToken) {
  return new ConvexClient(config.convexUrl, githubToken);
}

/**
 * Get or create command handler
 */
function getCommands(githubToken) {
  const convex = getConvexClient(githubToken);
  return new Plan2MealCommands(convex, oauth, config);
}

/**
 * Handle incoming message
 */
async function handleMessage(message, context = {}) {
  const { sessionId, userId } = context;
  
  // Get or create session
  let session = sessionStore.get(sessionId) || {};
  const githubToken = session.githubToken;
  
  // Parse command
  const text = message.trim();
  
  // Handle OAuth callback
  if (text.startsWith('/oauth/callback') || text.includes('code=')) {
    return handleOAuthCallback(text, sessionId);
  }
  
  // Check if authenticated
  if (!githubToken) {
    return initiateAuth(sessionId);
  }

  // Route command
  return routeCommand(text, githubToken);
}

/**
 * Route command to appropriate handler
 */
async function routeCommand(text, githubToken) {
  const cmd = getCommands(githubToken);
  
  // plan2meal add <url>
  const addMatch = text.match(/^plan2meal\s+add\s+(.+)$/i);
  if (addMatch) {
    const url = addMatch[1].trim();
    if (!isValidUrl(url)) {
      return { text: '❌ Invalid URL. Please provide a valid recipe URL.' };
    }
    return cmd.addRecipe(githubToken, url);
  }

  // plan2meal list
  if (/^plan2meal\s+list$/i.test(text)) {
    return cmd.listRecipes(githubToken);
  }

  // plan2meal search <term>
  const searchMatch = text.match(/^plan2meal\s+search\s+(.+)$/i);
  if (searchMatch) {
    return cmd.searchRecipes(githubToken, searchMatch[1].trim());
  }

  // plan2meal show <id>
  const showMatch = text.match(/^plan2meal\s+show\s+(.+)$/i);
  if (showMatch) {
    return cmd.showRecipe(githubToken, showMatch[1].trim());
  }

  // plan2meal delete <id>
  const deleteMatch = text.match(/^plan2meal\s+delete\s+(.+)$/i);
  if (deleteMatch) {
    return cmd.deleteRecipe(githubToken, deleteMatch[1].trim());
  }

  // plan2meal lists
  if (/^plan2meal\s+lists$/i.test(text)) {
    return cmd.lists(githubToken);
  }

  // plan2meal list-show <id>
  const listShowMatch = text.match(/^plan2meal\s+list-show\s+(.+)$/i);
  if (listShowMatch) {
    return cmd.showList(githubToken, listShowMatch[1].trim());
  }

  // plan2meal list-create <name>
  const listCreateMatch = text.match(/^plan2meal\s+list-create\s+(.+)$/i);
  if (listCreateMatch) {
    return cmd.createList(githubToken, listCreateMatch[1].trim());
  }

  // plan2meal list-add <listId> <recipeId>
  const listAddMatch = text.match(/^plan2meal\s+list-add\s+(\S+)\s+(\S+)$/i);
  if (listAddMatch) {
    return cmd.addRecipeToList(githubToken, listAddMatch[1].trim(), listAddMatch[2].trim());
  }

  // plan2meal help
  if (/^plan2meal\s+help$/i.test(text)) {
    return cmd.help();
  }

  return { text: '❌ Unknown command. Type `plan2meal help` for available commands.' };
}

/**
 * Initiate GitHub OAuth flow
 */
function initiateAuth(sessionId) {
  if (!oauth) {
    return {
      text: '⚠️ GitHub OAuth is not configured. Please set GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET in your environment.'
    };
  }

  const state = generateState();
  const authUrl = oauth.getAuthUrl(state);
  
  // Store state for verification
  sessionStore.set(`oauth_state_${sessionId}`, state);
  
  return {
    text: `🔐 To use Plan2Meal, please authenticate with GitHub:\n\n[Click here to authorize](${authUrl})\n\n` +
          `Or reply with your GitHub Personal Access Token if you prefer not to use OAuth.`,
    requiresAuth: false
  };
}

/**
 * Handle OAuth callback
 */
async function handleOAuthCallback(text, sessionId) {
  if (!oauth) {
    return { text: '⚠️ GitHub OAuth is not configured.' };
  }

  // Extract code from URL
  let code;
  if (text.includes('code=')) {
    const url = new URL(text.startsWith('http') ? text : `http://localhost${text}`);
    code = url.searchParams.get('code');
  } else {
    code = text;
  }

  if (!code) {
    return { text: '❌ No authorization code found.' };
  }

  try {
    const { token, userInfo } = await oauth.handleCallback(code);
    
    // Store token in session
    sessionStore.set(sessionId, {
      githubToken: token,
      userInfo,
      createdAt: Date.now()
    });

    return {
      text: `✅ Successfully authenticated as **${userInfo.login}**!\n\n` +
            `You can now use Plan2Meal commands. Type \`plan2meal help\` to get started.`
    };
  } catch (error) {
    return { text: `❌ Authentication failed: ${error.message}` };
  }
}

/**
 * Set user token manually (for PAT-based auth)
 */
function setUserToken(sessionId, token) {
  sessionStore.set(sessionId, {
    githubToken: token,
    userInfo: null,
    createdAt: Date.now()
  });
}

/**
 * Clear session
 */
function clearSession(sessionId) {
  sessionStore.delete(sessionId);
}

/**
 * Get session info
 */
function getSession(sessionId) {
  return sessionStore.get(sessionId);
}

// Export for ClawdHub
module.exports = {
  initialize,
  handleMessage,
  setUserToken,
  clearSession,
  getSession,
  getCommandPatterns
};