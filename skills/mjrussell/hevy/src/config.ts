/**
 * Configuration management for Hevy CLI
 * 
 * API key is read from HEVY_API_KEY environment variable.
 * No file-based config needed - keeps things simple and secure.
 */

export interface HevyConfig {
  apiKey: string;
}

const ENV_VAR_NAME = "HEVY_API_KEY";

/**
 * Get API key from environment variable
 */
export function getApiKey(): string | null {
  return process.env[ENV_VAR_NAME] ?? null;
}

/**
 * Check if API key is configured
 */
export function isConfigured(): boolean {
  const key = getApiKey();
  return key !== null && key.length > 0;
}

/**
 * Require API key or exit with helpful message
 */
export function requireApiKey(): string {
  const key = getApiKey();
  if (!key) {
    console.error(`Error: ${ENV_VAR_NAME} environment variable not set.`);
    console.error("");
    console.error("To get your API key:");
    console.error("  1. Go to https://hevy.com/settings?developer");
    console.error("  2. Generate an API key (requires Hevy Pro)");
    console.error("");
    console.error("Then set the environment variable:");
    console.error(`  export ${ENV_VAR_NAME}="your-api-key-here"`);
    console.error("");
    console.error("Or add it to your shell profile (~/.zshrc, ~/.bashrc, etc.)");
    process.exit(1);
  }
  return key;
}

/**
 * Get config object (for API client)
 */
export function getConfig(): HevyConfig {
  return {
    apiKey: requireApiKey(),
  };
}
