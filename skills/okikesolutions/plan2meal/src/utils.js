/**
 * Utility functions for Plan2Meal skill
 */

/**
 * Escape markdown special characters
 */
function markdownEscape(text) {
  if (!text) return '';
  const str = String(text);
  return str
    .replace(/[_*[\]()~`>#+=|{}.!-]/g, '\\$&')
    .replace(/\n/g, ' ');
}

/**
 * Format duration in minutes to human readable
 */
function formatDuration(minutes) {
  if (!minutes) return null;
  if (minutes < 60) return `${minutes} min`;
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return mins ? `${hours}h ${mins}m` : `${hours}h`;
}

/**
 * Validate URL
 */
function isValidUrl(string) {
  try {
    new URL(string);
    return true;
  } catch {
    return false;
  }
}

/**
 * Generate a random state string for OAuth
 */
function generateState() {
  return Math.random().toString(36).substring(2, 15) + 
         Math.random().toString(36).substring(2, 15);
}

/**
 * Truncate text with ellipsis
 */
function truncate(text, maxLength = 100) {
  if (!text) return '';
  const str = String(text);
  if (str.length <= maxLength) return str;
  return str.slice(0, maxLength - 3) + '...';
}

/**
 * Parse recipe ID from various formats
 */
function parseRecipeId(input) {
  // Handle URL format: https://.../recipe/123
  if (input.includes('/')) {
    const parts = input.split('/');
    return parts[parts.length - 1];
  }
  return input.trim();
}

/**
 * Sleep for specified milliseconds
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

module.exports = {
  markdownEscape,
  formatDuration,
  isValidUrl,
  generateState,
  truncate,
  parseRecipeId,
  sleep
};