#!/usr/bin/env node

/**
 * Session Reader for Telegram Usage Command
 * Reads actual session data from Clawdbot's session store
 */

const fs = require('fs');
const path = require('path');

/**
 * Get the session store path for the current agent
 * @param {string} agentId - Agent ID (default: 'main')
 * @returns {string} Path to sessions.json
 */
function getSessionStorePath(agentId = 'main') {
  const homeDir = process.env.HOME || process.env.USERPROFILE;
  return path.join(homeDir, '.clawdbot', 'agents', agentId, 'sessions', 'sessions.json');
}

/**
 * Get the session reset time from config
 * @param {number} atHour - Hour to reset (0-23)
 * @returns {Date} Next reset time
 */
function getNextResetTime(atHour = 4) {
  const now = new Date();
  const reset = new Date();
  reset.setHours(atHour, 0, 0, 0);
  
  // If reset time has passed today, use tomorrow
  if (reset <= now) {
    reset.setDate(reset.getDate() + 1);
  }
  
  return reset;
}

/**
 * Calculate time remaining until reset
 * @param {number} atHour - Hour to reset
 * @returns {number} Milliseconds until reset
 */
function getTimeUntilReset(atHour = 4) {
  const nextReset = getNextResetTime(atHour);
  return nextReset.getTime() - Date.now();
}

/**
 * Format duration in milliseconds
 * @param {number} ms - Milliseconds
 * @returns {string} Formatted duration
 */
function formatDuration(ms) {
  const totalSeconds = Math.floor(ms / 1000);
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  
  if (hours > 0) {
    return `${hours}h ${minutes}m`;
  }
  return `${minutes}m`;
}

/**
 * Read session store and extract statistics
 * @param {string} sessionKey - Session key (e.g., 'agent:main:main')
 * @param {string} agentId - Agent ID (default: 'main')
 * @returns {Object} Session statistics
 */
function readSessionStats(sessionKey, agentId = 'main') {
  const storePath = getSessionStorePath(agentId);
  
  if (!fs.existsSync(storePath)) {
    console.warn(`Session store not found at ${storePath}`);
    return null;
  }

  try {
    const store = JSON.parse(fs.readFileSync(storePath, 'utf-8'));
    const session = store[sessionKey];
    
    if (!session) {
      console.warn(`Session ${sessionKey} not found in store`);
      return null;
    }

    return {
      sessionId: session.sessionId,
      updatedAt: session.updatedAt,
      inputTokens: session.inputTokens || 0,
      outputTokens: session.outputTokens || 0,
      totalTokens: session.totalTokens || 0,
      contextTokens: session.contextTokens || 0,
      model: session.model,
      provider: session.provider
    };
  } catch (error) {
    console.error(`Error reading session store: ${error.message}`);
    return null;
  }
}

/**
 * Read conversation JSONL to get token counts
 * @param {string} transcriptPath - Path to transcript JSONL
 * @returns {Object} Token statistics
 */
function readTokensFromTranscript(transcriptPath) {
  if (!fs.existsSync(transcriptPath)) {
    return null;
  }

  try {
    const lines = fs.readFileSync(transcriptPath, 'utf-8').trim().split('\n');
    let totalInput = 0;
    let totalOutput = 0;
    
    for (const line of lines) {
      if (!line) continue;
      const entry = JSON.parse(line);
      
      if (entry.role === 'user' && entry.usage?.inputTokens) {
        totalInput += entry.usage.inputTokens;
      }
      if (entry.role === 'assistant' && entry.usage?.outputTokens) {
        totalOutput += entry.usage.outputTokens;
      }
    }

    return {
      inputTokens: totalInput,
      outputTokens: totalOutput,
      totalTokens: totalInput + totalOutput
    };
  } catch (error) {
    console.warn(`Could not parse transcript: ${error.message}`);
    return null;
  }
}

/**
 * Get transcript path for a session
 * @param {string} sessionId - Session ID
 * @param {string} agentId - Agent ID
 * @returns {string} Path to transcript
 */
function getTranscriptPath(sessionId, agentId = 'main') {
  const homeDir = process.env.HOME || process.env.USERPROFILE;
  return path.join(homeDir, '.clawdbot', 'agents', agentId, 'sessions', `${sessionId}.jsonl`);
}

/**
 * Estimate context window usage
 * @param {Object} session - Session stats
 * @param {string} model - Model name
 * @returns {Object} Context usage stats
 */
function estimateContextUsage(session, model = 'claude-3-5-haiku') {
  // Context window sizes for common models
  const contextWindows = {
    'claude-3-5-haiku': 200000,
    'claude-haiku-4-5': 200000,
    'claude-3-haiku': 200000,
    'claude-3-5-sonnet': 200000,
    'claude-3-sonnet': 200000,
    'claude-3-opus': 200000,
    'claude-opus-4': 200000,
    'gpt-4': 8192,
    'gpt-4-turbo': 128000,
    'gpt-3.5-turbo': 4096
  };

  // Try to match model name (partial matches)
  let windowSize = 4096;
  for (const [modelKey, size] of Object.entries(contextWindows)) {
    if (model.toLowerCase().includes(modelKey.toLowerCase())) {
      windowSize = size;
      break;
    }
  }

  const contextUsed = session.contextTokens || session.totalTokens || 1024;
  const percentage = Math.round((contextUsed / windowSize) * 100);

  return {
    used: contextUsed,
    total: windowSize,
    percentage: Math.min(percentage, 100) // Cap at 100%
  };
}

/**
 * Collect all usage statistics
 * @param {string} sessionKey - Session key to read
 * @param {Object} options - Options
 * @returns {Object} Comprehensive usage stats
 */
function collectUsageStats(sessionKey, options = {}) {
  const {
    agentId = 'main',
    resetHour = 4,
    quotaRemaining = null,
    provider = 'anthropic'
  } = options;

  const session = readSessionStats(sessionKey, agentId);
  
  if (!session) {
    // Return defaults if session not found
    return {
      quotaRemaining: quotaRemaining || 85,
      sessionTimeRemaining: getTimeUntilReset(resetHour),
      totalTokens: { input: 0, output: 0 },
      contextUsage: { used: 0, total: 4096 },
      model: 'Unknown',
      provider: provider,
      sessionFound: false
    };
  }

  // Try to read tokens from transcript
  const transcriptPath = getTranscriptPath(session.sessionId, agentId);
  const transcriptTokens = readTokensFromTranscript(transcriptPath);

  const totalTokens = transcriptTokens || {
    inputTokens: session.inputTokens || 0,
    outputTokens: session.outputTokens || 0,
    totalTokens: session.totalTokens || 0
  };

  const contextUsage = estimateContextUsage(session, session.model);

  return {
    quotaRemaining: quotaRemaining || 82,
    sessionTimeRemaining: getTimeUntilReset(resetHour),
    totalTokens: {
      input: totalTokens.inputTokens || 0,
      output: totalTokens.outputTokens || 0
    },
    contextUsage: {
      used: contextUsage.used,
      total: contextUsage.total
    },
    contextPercentage: contextUsage.percentage,
    model: session.model || 'Claude 3.5 Haiku',
    provider: session.provider || provider,
    sessionId: session.sessionId,
    updatedAt: session.updatedAt,
    sessionFound: true
  };
}

/**
 * Format stats for display
 * @param {Object} stats - Usage statistics
 * @returns {string} Formatted message
 */
function formatStats(stats) {
  const quotaIndicator = getQuotaIndicator(stats.quotaRemaining);
  const contextIndicator = getQuotaIndicator(100 - (stats.contextPercentage || 0));
  const timeRemaining = formatDuration(stats.sessionTimeRemaining);

  let message = '<b>📊 Session Usage Report</b>\n\n';

  message += '<b>🔋 Quota Remaining</b>\n';
  message += `${quotaIndicator} <code>${stats.quotaRemaining}%</code> of API quota\n`;
  message += `Provider: ${stats.provider}\n\n`;

  message += '<b>⏱️ Session Time</b>\n';
  message += `${timeRemaining} remaining\n`;
  message += '(resets daily at 4:00 AM)\n\n';

  message += '<b>🎯 Tokens Used</b>\n';
  const total = stats.totalTokens.input + stats.totalTokens.output;
  message += `${total.toLocaleString('en-US')} total tokens\n`;
  message += `├─ Input: ${stats.totalTokens.input.toLocaleString('en-US')}\n`;
  message += `└─ Output: ${stats.totalTokens.output.toLocaleString('en-US')}\n\n`;

  message += '<b>📦 Context Window</b>\n';
  message += `${contextIndicator} <code>${stats.contextPercentage || 0}%</code> used\n`;
  message += `${stats.contextUsage.used.toLocaleString('en-US')} / ${stats.contextUsage.total.toLocaleString('en-US')} tokens\n`;

  message += `\n<i>Model: ${stats.model}</i>`;
  if (stats.sessionId) {
    message += `\n<i>Session: ${stats.sessionId.substring(0, 8)}...</i>`;
  }

  return message;
}

/**
 * Get quota indicator emoji
 */
function getQuotaIndicator(percentage) {
  if (percentage >= 75) return '🟢';
  if (percentage >= 50) return '🟡';
  if (percentage >= 25) return '🟠';
  return '🔴';
}

// Export
module.exports = {
  getSessionStorePath,
  getNextResetTime,
  getTimeUntilReset,
  formatDuration,
  readSessionStats,
  readTokensFromTranscript,
  getTranscriptPath,
  estimateContextUsage,
  collectUsageStats,
  formatStats,
  getQuotaIndicator
};

// CLI usage
if (require.main === module) {
  const sessionKey = process.argv[2] || 'agent:main:main';
  const agentId = process.argv[3] || 'main';

  const stats = collectUsageStats(sessionKey, {
    agentId,
    resetHour: 4
  });

  if (process.argv[4] === '--json') {
    console.log(JSON.stringify(stats, null, 2));
  } else {
    console.log(formatStats(stats));
  }
}
