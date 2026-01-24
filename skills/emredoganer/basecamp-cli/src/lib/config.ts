import Conf from 'conf';
import crypto from 'crypto';
import os from 'os';
import type { BasecampConfig, BasecampTokens } from '../types/index.js';

// =============================================================================
// Encryption utilities for secure token storage
// =============================================================================

/**
 * Generate a machine-specific encryption key
 * This provides better security than plain text while not requiring external dependencies
 * Note: For maximum security, consider using system keychain (macOS Keychain, Windows Credential Manager)
 */
function getEncryptionKey(): Buffer {
  const machineId = `${os.hostname()}-${os.userInfo().username}-basecamp-cli-tokens`;
  return crypto.createHash('sha256').update(machineId).digest();
}

/**
 * Encrypt a string using AES-256-CBC
 * @param text Plain text to encrypt
 * @returns Encrypted string in format "iv:encryptedData"
 */
function encrypt(text: string): string {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-cbc', getEncryptionKey(), iv);
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  return iv.toString('hex') + ':' + encrypted;
}

/**
 * Decrypt a string that was encrypted with encrypt()
 * @param text Encrypted string in format "iv:encryptedData"
 * @returns Decrypted plain text
 */
function decrypt(text: string): string {
  try {
    const [ivHex, encrypted] = text.split(':');
    if (!ivHex || !encrypted) {
      throw new Error('Invalid encrypted format');
    }
    const iv = Buffer.from(ivHex, 'hex');
    const decipher = crypto.createDecipheriv('aes-256-cbc', getEncryptionKey(), iv);
    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
  } catch {
    // If decryption fails, the data might be in plain text (legacy)
    // Return as-is to allow migration
    return text;
  }
}

/**
 * Check if a string appears to be encrypted (has iv:data format)
 */
function isEncrypted(text: string): boolean {
  if (!text) return false;
  const parts = text.split(':');
  // Encrypted format: 32 char hex IV + ':' + encrypted data
  return parts.length === 2 && parts[0].length === 32 && /^[0-9a-f]+$/i.test(parts[0]);
}

// =============================================================================
// Configuration store
// =============================================================================

const config = new Conf<BasecampConfig>({
  projectName: 'basecamp-cli',
  schema: {
    tokens: {
      type: 'object',
      properties: {
        access_token: { type: 'string' },
        refresh_token: { type: 'string' },
        expires_at: { type: 'number' }
      }
    },
    currentAccountId: { type: 'number' },
    clientId: { type: 'string' },
    redirectUri: { type: 'string' }
    // Note: clientSecret is intentionally NOT stored in config for security.
    // It must be provided via BASECAMP_CLIENT_SECRET environment variable.
  }
});

// =============================================================================
// Token management with encryption
// =============================================================================

export function getTokens(): BasecampTokens | undefined {
  const storedTokens = config.get('tokens');
  if (!storedTokens) return undefined;

  // Ensure required fields exist
  if (!storedTokens.access_token || !storedTokens.refresh_token) {
    return undefined;
  }

  // Decrypt tokens if they are encrypted
  const access_token = isEncrypted(storedTokens.access_token)
    ? decrypt(storedTokens.access_token)
    : storedTokens.access_token; // Legacy plain text support

  const refresh_token = isEncrypted(storedTokens.refresh_token)
    ? decrypt(storedTokens.refresh_token)
    : storedTokens.refresh_token; // Legacy plain text support

  return {
    access_token,
    refresh_token,
    expires_at: storedTokens.expires_at
  };
}

export function setTokens(tokens: BasecampTokens): void {
  // Encrypt sensitive token values before storing
  const encryptedTokens = {
    access_token: tokens.access_token ? encrypt(tokens.access_token) : undefined,
    refresh_token: tokens.refresh_token ? encrypt(tokens.refresh_token) : undefined,
    expires_at: tokens.expires_at
  };
  config.set('tokens', encryptedTokens);
}

export function clearTokens(): void {
  config.delete('tokens');
}

// =============================================================================
// Account management
// =============================================================================

export function getCurrentAccountId(): number | undefined {
  return config.get('currentAccountId');
}

export function setCurrentAccountId(accountId: number): void {
  config.set('currentAccountId', accountId);
}

// =============================================================================
// Client credentials
// =============================================================================

/**
 * Get OAuth client credentials.
 *
 * SECURITY NOTE: Client secret is ONLY read from the BASECAMP_CLIENT_SECRET
 * environment variable and is never stored in the config file.
 *
 * Client ID and redirect URI can be stored in config as they are not sensitive.
 */
export function getClientCredentials(): { clientId?: string; clientSecret?: string; redirectUri?: string } {
  const clientSecret = process.env.BASECAMP_CLIENT_SECRET;

  if (!clientSecret) {
    throw new Error(
      'BASECAMP_CLIENT_SECRET environment variable is not set.\n\n' +
      'For security, the client secret must be provided via environment variable.\n' +
      'Set it using:\n' +
      '  export BASECAMP_CLIENT_SECRET="your-client-secret"\n\n' +
      'Or add it to your shell profile (~/.bashrc, ~/.zshrc, etc.)'
    );
  }

  return {
    clientId: config.get('clientId') || process.env.BASECAMP_CLIENT_ID,
    clientSecret,
    redirectUri: config.get('redirectUri') || process.env.BASECAMP_REDIRECT_URI || 'http://localhost:9292/callback'
  };
}

/**
 * Store non-sensitive client configuration.
 *
 * SECURITY NOTE: This function intentionally does NOT accept or store
 * the client secret. The client secret must be provided via the
 * BASECAMP_CLIENT_SECRET environment variable.
 */
export function setClientConfig(clientId: string, redirectUri?: string): void {
  config.set('clientId', clientId);
  if (redirectUri) {
    config.set('redirectUri', redirectUri);
  }
}

// =============================================================================
// Utility functions
// =============================================================================

export function clearAll(): void {
  config.clear();
}

export function isAuthenticated(): boolean {
  const tokens = getTokens();
  return !!tokens?.access_token;
}

export function isTokenExpired(): boolean {
  const tokens = getTokens();
  if (!tokens?.expires_at) return true;
  return Date.now() >= tokens.expires_at - 60000; // 1 minute buffer
}

export { config };
