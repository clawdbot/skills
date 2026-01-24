import crypto from 'crypto';
import http from 'http';
import { URL } from 'url';
import open from 'open';
import got from 'got';
import chalk from 'chalk';
import type { BasecampTokens, BasecampAuthorization } from '../types/index.js';
import { getClientCredentials, setTokens, getTokens, clearTokens, isTokenExpired } from './config.js';

const OAUTH_BASE = 'https://launchpad.37signals.com';

// In-memory storage for OAuth flow state (only needed during the flow)
let pendingOAuthState: {
  state: string;
  codeVerifier: string;
} | null = null;

/**
 * Generate a cryptographically random string using base64url encoding
 * @param length - Number of random bytes (output will be longer due to base64 encoding)
 */
function generateRandomString(length: number): string {
  return crypto.randomBytes(length)
    .toString('base64url');
}

/**
 * Generate PKCE code verifier (43-128 characters as per RFC 7636)
 */
function generateCodeVerifier(): string {
  // 32 bytes = 43 characters in base64url encoding
  return generateRandomString(32);
}

/**
 * Generate PKCE code challenge from verifier using SHA256 (S256 method)
 * @param verifier - The code verifier to hash
 */
function generateCodeChallenge(verifier: string): string {
  return crypto
    .createHash('sha256')
    .update(verifier)
    .digest('base64url');
}

/**
 * Generate cryptographically random state for CSRF protection
 */
function generateState(): string {
  return generateRandomString(32);
}

export async function startOAuthFlow(): Promise<BasecampTokens> {
  const { clientId, clientSecret, redirectUri } = getClientCredentials();

  if (!clientId || !clientSecret) {
    throw new Error(
      'Missing OAuth credentials. Please set BASECAMP_CLIENT_ID and BASECAMP_CLIENT_SECRET environment variables,\n' +
      'or run: basecamp auth configure --client-id <id> --client-secret <secret>'
    );
  }

  // Generate PKCE values
  const codeVerifier = generateCodeVerifier();
  const codeChallenge = generateCodeChallenge(codeVerifier);

  // Generate state for CSRF protection
  const state = generateState();

  // Store state and code verifier for validation in callback
  pendingOAuthState = {
    state,
    codeVerifier
  };

  const parsedUri = new URL(redirectUri!);
  const port = parseInt(parsedUri.port) || 9292;

  return new Promise((resolve, reject) => {
    const server = http.createServer(async (req, res) => {
      const url = new URL(req.url!, `http://localhost:${port}`);

      if (url.pathname === '/callback') {
        const code = url.searchParams.get('code');
        const returnedState = url.searchParams.get('state');
        const error = url.searchParams.get('error');

        if (error) {
          res.writeHead(400, { 'Content-Type': 'text/html' });
          res.end('<html><body><h1>Authentication Failed</h1><p>You can close this window.</p></body></html>');
          server.close();
          pendingOAuthState = null;
          reject(new Error(`OAuth error: ${error}`));
          return;
        }

        // Validate state parameter for CSRF protection
        if (!returnedState || !pendingOAuthState || returnedState !== pendingOAuthState.state) {
          res.writeHead(400, { 'Content-Type': 'text/html' });
          res.end('<html><body><h1>Authentication Failed</h1><p>Invalid state parameter. Possible CSRF attack.</p></body></html>');
          server.close();
          pendingOAuthState = null;
          reject(new Error('OAuth error: State mismatch - possible CSRF attack'));
          return;
        }

        if (code) {
          try {
            const tokens = await exchangeCodeForTokens(
              code,
              clientId,
              clientSecret,
              redirectUri!,
              pendingOAuthState.codeVerifier
            );
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end('<html><body><h1>Authentication Successful!</h1><p>You can close this window and return to the CLI.</p></body></html>');
            server.close();
            pendingOAuthState = null;
            resolve(tokens);
          } catch (err) {
            res.writeHead(500, { 'Content-Type': 'text/html' });
            res.end('<html><body><h1>Token Exchange Failed</h1><p>Please try again.</p></body></html>');
            server.close();
            pendingOAuthState = null;
            reject(err);
          }
        }
      }
    });

    server.listen(port, () => {
      // Build authorization URL with PKCE and state parameters
      const authParams = new URLSearchParams({
        type: 'web_server',
        client_id: clientId,
        redirect_uri: redirectUri!,
        state: state,
        code_challenge: codeChallenge,
        code_challenge_method: 'S256'
      });
      const authUrl = `${OAUTH_BASE}/authorization/new?${authParams.toString()}`;
      console.log(chalk.blue('Opening browser for authentication...'));
      console.log(chalk.dim(`If browser doesn't open, visit: ${authUrl}`));
      open(authUrl);
    });

    server.on('error', (err) => {
      pendingOAuthState = null;
      reject(new Error(`Failed to start OAuth callback server: ${err.message}`));
    });

    // Timeout after 5 minutes
    setTimeout(() => {
      server.close();
      pendingOAuthState = null;
      reject(new Error('Authentication timed out'));
    }, 5 * 60 * 1000);
  });
}

async function exchangeCodeForTokens(
  code: string,
  clientId: string,
  clientSecret: string,
  redirectUri: string,
  codeVerifier: string
): Promise<BasecampTokens> {
  const response = await got.post(`${OAUTH_BASE}/authorization/token`, {
    searchParams: {
      type: 'web_server',
      client_id: clientId,
      client_secret: clientSecret,
      redirect_uri: redirectUri,
      code,
      code_verifier: codeVerifier
    }
  }).json<{ access_token: string; refresh_token: string; expires_in: number }>();

  const tokens: BasecampTokens = {
    access_token: response.access_token,
    refresh_token: response.refresh_token,
    expires_at: Date.now() + (response.expires_in * 1000)
  };

  setTokens(tokens);
  return tokens;
}

export async function refreshTokens(): Promise<BasecampTokens> {
  const { clientId, clientSecret, redirectUri } = getClientCredentials();
  const currentTokens = getTokens();

  if (!currentTokens?.refresh_token) {
    throw new Error('No refresh token available. Please login again.');
  }

  if (!clientId || !clientSecret) {
    throw new Error('Missing OAuth credentials');
  }

  const response = await got.post(`${OAUTH_BASE}/authorization/token`, {
    searchParams: {
      type: 'refresh',
      client_id: clientId,
      client_secret: clientSecret,
      refresh_token: currentTokens.refresh_token
    }
  }).json<{ access_token: string; expires_in: number }>();

  const tokens: BasecampTokens = {
    access_token: response.access_token,
    refresh_token: currentTokens.refresh_token,
    expires_at: Date.now() + (response.expires_in * 1000)
  };

  setTokens(tokens);
  return tokens;
}

export async function getValidAccessToken(): Promise<string> {
  const tokens = getTokens();

  if (!tokens?.access_token) {
    throw new Error('Not authenticated. Please run: basecamp auth login');
  }

  if (isTokenExpired()) {
    console.log(chalk.dim('Token expired, refreshing...'));
    const newTokens = await refreshTokens();
    return newTokens.access_token;
  }

  return tokens.access_token;
}

export async function getAuthorization(): Promise<BasecampAuthorization> {
  const accessToken = await getValidAccessToken();

  const response = await got.get(`${OAUTH_BASE}/authorization.json`, {
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'User-Agent': 'Basecamp CLI (emredoganer@github.com)'
    }
  }).json<BasecampAuthorization>();

  return response;
}

export function logout(): void {
  clearTokens();
}
