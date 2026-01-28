/**
 * WHOOP OAuth2 Authentication
 *
 * Two modes:
 * 1. Browser auth (default) - Opens browser, runs local callback server
 * 2. Manual mode (--manual) - Paste authorization code manually
 */

import { createServer as createHttpServer } from 'http';
import { createServer as createHttpsServer } from 'https';
import { URL } from 'url';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import readline from 'readline';
import { execFileSync } from 'child_process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA_DIR = process.env.WHOOP_DATA_DIR || path.join(process.env.HOME, '.clawdbot', 'whoop');
const LEGACY_CREDENTIALS_PATH = path.join(__dirname, '..', 'credentials.json');
const LEGACY_TOKEN_PATH = path.join(__dirname, '..', 'token.json');
const LEGACY_TLS_KEY_PATH = path.join(__dirname, '..', 'tls.key');
const LEGACY_TLS_CERT_PATH = path.join(__dirname, '..', 'tls.crt');

const CREDENTIALS_PATH = process.env.WHOOP_CREDENTIALS_PATH || path.join(DATA_DIR, 'credentials.json');
const TOKEN_PATH = process.env.WHOOP_TOKEN_PATH || path.join(DATA_DIR, 'token.json');

const WHOOP_AUTH_URL = 'https://api.prod.whoop.com/oauth/oauth2/auth';
const WHOOP_TOKEN_URL = 'https://api.prod.whoop.com/oauth/oauth2/token';
const DEFAULT_REDIRECT_URI = 'http://localhost:3000/callback';
const REDIRECT_URI = process.env.WHOOP_REDIRECT_URI || DEFAULT_REDIRECT_URI;
const REDIRECT_URL = new URL(REDIRECT_URI);
const CALLBACK_PATHNAME = REDIRECT_URL.pathname || '/callback';
// If you're using a public redirect URI (e.g. ngrok), WHOOP will redirect the browser to that domain
// and you must tunnel it back to this local port.
const LISTEN_PORT = Number(process.env.WHOOP_LISTEN_PORT || 3000);
const NON_BROWSER_UA = 'MyApp/1.0 (+whoop-oauth-bootstrap)';

const DEFAULT_SCOPES = [
  'offline',
  'read:recovery',
  'read:sleep',
  'read:workout',
  'read:cycles',
  'read:profile'
];
// Helpful for debugging account/app restrictions (e.g. try just "read:profile").
const SCOPES = process.env.WHOOP_SCOPES
  ? process.env.WHOOP_SCOPES.split(/[\s,]+/).map(s => s.trim()).filter(Boolean)
  : DEFAULT_SCOPES;

function openInBrowser(url) {
  try {
    if (process.platform === 'darwin') {
      execFileSync('open', [url], { stdio: 'ignore' });
      return;
    }
    if (process.platform === 'win32') {
      execFileSync('cmd', ['/c', 'start', '', url], { stdio: 'ignore' });
      return;
    }
    execFileSync('xdg-open', [url], { stdio: 'ignore' });
  } catch {
    // Fall back to printing the URL; manual mode is always available.
    console.log(`Open this URL in your browser: ${url}`);
  }
}

function ensureDataDir() {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
}

function migrateLegacyFile(srcPath, dstPath) {
  if (!fs.existsSync(srcPath) || fs.existsSync(dstPath)) return false;
  ensureDataDir();
  try {
    fs.renameSync(srcPath, dstPath);
    return true;
  } catch {
    // Fallback for cross-device renames (or permission issues).
    fs.copyFileSync(srcPath, dstPath);
    fs.unlinkSync(srcPath);
    return true;
  }
}

function migrateLegacyAuthFiles() {
  // Keep secrets/tokens out of the skill folder so the skill can be safely published.
  const moved = [];
  if (migrateLegacyFile(LEGACY_CREDENTIALS_PATH, CREDENTIALS_PATH)) moved.push('credentials.json');
  if (migrateLegacyFile(LEGACY_TOKEN_PATH, TOKEN_PATH)) moved.push('token.json');
  // TLS certs are regeneratable; migrate if present to avoid packaging them.
  const tlsKey = process.env.WHOOP_TLS_KEY_PATH || path.join(DATA_DIR, 'tls.key');
  const tlsCert = process.env.WHOOP_TLS_CERT_PATH || path.join(DATA_DIR, 'tls.crt');
  if (migrateLegacyFile(LEGACY_TLS_KEY_PATH, tlsKey)) moved.push('tls.key');
  if (migrateLegacyFile(LEGACY_TLS_CERT_PATH, tlsCert)) moved.push('tls.crt');
  if (moved.length) {
    console.log(`ℹ️  Migrated legacy WHOOP auth files to ${DATA_DIR}: ${moved.join(', ')}`);
  }
}

function ensureLocalTlsCert() {
  // If the redirect is https://localhost:PORT/..., we need an HTTPS callback server.
  // Use a self-signed cert by default; browsers will warn but you can proceed for localhost.
  const keyPath = process.env.WHOOP_TLS_KEY_PATH || path.join(DATA_DIR, 'tls.key');
  const certPath = process.env.WHOOP_TLS_CERT_PATH || path.join(DATA_DIR, 'tls.crt');

  if (fs.existsSync(keyPath) && fs.existsSync(certPath)) {
    return { key: fs.readFileSync(keyPath), cert: fs.readFileSync(certPath) };
  }

  try {
    ensureDataDir();
    console.log('🔐 Generating a local self-signed TLS cert for https://localhost callback...');
    execFileSync('openssl', [
      'req',
      '-x509',
      '-newkey',
      'rsa:2048',
      '-nodes',
      '-keyout',
      keyPath,
      '-out',
      certPath,
      '-days',
      '365',
      '-subj',
      '/CN=localhost'
    ], { stdio: 'ignore' });
    return { key: fs.readFileSync(keyPath), cert: fs.readFileSync(certPath) };
  } catch (e) {
    throw new Error(
      `Failed to generate TLS cert via openssl. Either install openssl or set WHOOP_TLS_KEY_PATH/WHOOP_TLS_CERT_PATH. Details: ${e?.message || e}`
    );
  }
}

async function resolveWhoopBrowserLoginUrl(authUrl) {
  // WHOOP currently returns a 401 NotAuthorizedException for browser UAs on api.prod.whoop.com.
  // Work around this by resolving the login_challenge server-side with a non-browser UA, then
  // opening the final id.whoop.com URL in the user's real browser.
  try {
    const r1 = await fetch(authUrl, {
      method: 'GET',
      redirect: 'manual',
      headers: { 'User-Agent': NON_BROWSER_UA }
    });

    const loc1 = r1.headers.get('location');
    if (!loc1) return null;

    const r2 = await fetch(loc1, {
      method: 'GET',
      redirect: 'manual',
      headers: { 'User-Agent': NON_BROWSER_UA }
    });

    const loc2 = r2.headers.get('location');
    if (!loc2) return null;

    // Expect: https://id.whoop.com/?login_challenge=...
    return loc2;
  } catch {
    return null;
  }
}

async function preflightAuthUrl(authUrl) {
  // Detect common hard-fail conditions (most importantly redirect_uri mismatch) with a non-browser UA.
  try {
    const r = await fetch(authUrl, {
      method: 'GET',
      redirect: 'manual',
      headers: { 'User-Agent': NON_BROWSER_UA }
    });

    const loc = r.headers.get('location');
    if (!loc) return { ok: false, reason: 'no_location' };

    if (loc.includes('/oauth/oauth2/fallbacks/error')) {
      const u = new URL(loc);
      return {
        ok: false,
        reason: 'oauth_error',
        error: u.searchParams.get('error'),
        description: u.searchParams.get('error_description'),
        hint: u.searchParams.get('error_hint')
      };
    }

    return { ok: true };
  } catch (e) {
    return { ok: false, reason: 'fetch_failed', error: String(e?.message || e) };
  }
}

function loadCredentials() {
  migrateLegacyAuthFiles();
  if (!fs.existsSync(CREDENTIALS_PATH)) {
    console.error('❌ credentials.json not found!\n');
    console.log('Setup instructions:');
    console.log('1. Go to: https://developer.whoop.com/');
    console.log('2. Create an App (or edit existing)');
    console.log('3. Add this EXACT Redirect URI:');
    console.log(`   ${REDIRECT_URI}`);
    console.log('4. Copy Client ID and Client Secret');
    console.log('5. Create credentials.json at:');
    console.log(`   ${CREDENTIALS_PATH}`);
    console.log('   Contents: {"client_id": "...", "client_secret": "..."}');
    console.log('\n   (You can override with WHOOP_DATA_DIR or WHOOP_CREDENTIALS_PATH.)');
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
}

function buildAuthUrl(client_id, state) {
  return `${WHOOP_AUTH_URL}?` + new URLSearchParams({
    client_id,
    redirect_uri: REDIRECT_URI,
    response_type: 'code',
    scope: SCOPES.join(' '),
    state
  });
}

async function exchangeCodeForToken(code, client_id, client_secret) {
  console.log('\n🔄 Exchanging code for token...');

  const response = await fetch(WHOOP_TOKEN_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      client_id,
      client_secret,
      redirect_uri: REDIRECT_URI
    })
  });

  const tokens = await response.json();

  if (tokens.error) {
    console.error('\n❌ Token exchange failed!');
    console.error(`   Error: ${tokens.error}`);
    if (tokens.error_hint) {
      console.error(`   Hint: ${tokens.error_hint}`);
    }

    if (tokens.error_hint?.includes('redirect_uri')) {
      console.log('\n⚠️  REDIRECT URI MISMATCH');
      console.log('   Make sure your WHOOP app has this EXACT redirect URI:');
      console.log(`   ${REDIRECT_URI}`);
      console.log('\n   To fix:');
      console.log('   1. Go to https://developer.whoop.com/');
      console.log('   2. Select your app');
      console.log('   3. Edit Redirect URIs');
      console.log(`   4. Add: ${REDIRECT_URI}`);
      console.log('   5. Save and try again');
    }

    // Save error for debugging
    tokens.obtained_at = Date.now();
    ensureDataDir();
    fs.writeFileSync(TOKEN_PATH, JSON.stringify(tokens, null, 2));
    return null;
  }

  if (tokens.access_token) {
    tokens.obtained_at = Date.now();
    // Persist the redirect_uri used to obtain this token set. WHOOP's token endpoint may
    // validate redirect_uri on refresh as well.
    tokens.redirect_uri = REDIRECT_URI;
    ensureDataDir();
    fs.writeFileSync(TOKEN_PATH, JSON.stringify(tokens, null, 2));
    console.log('✅ WHOOP authenticated!');
    console.log(`   Token saved to: ${TOKEN_PATH}`);
    return tokens;
  }

  console.error('❌ Unexpected response:', tokens);
  return null;
}

async function manualAuth() {
  const { client_id, client_secret } = loadCredentials();
  const state = Math.random().toString(36).substring(2, 10);

  const authUrl = buildAuthUrl(client_id, state);
  const preflight = await preflightAuthUrl(authUrl);
  if (!preflight.ok) {
    console.error('\n❌ WHOOP authorization preflight failed.');
    if (preflight.reason === 'oauth_error') {
      console.error(`   Error: ${preflight.error}`);
      if (preflight.description) console.error(`   Description: ${preflight.description}`);
      if (preflight.hint) console.error(`   Hint: ${preflight.hint}`);
    } else {
      console.error(`   Reason: ${preflight.reason}`);
      if (preflight.error) console.error(`   Details: ${preflight.error}`);
    }
    console.error('\nMost common fix: update your WHOOP app Redirect URIs to match EXACTLY:');
    console.error(`   ${REDIRECT_URI}\n`);
    process.exit(1);
  }

  const startUrl = await resolveWhoopBrowserLoginUrl(authUrl);

  console.log('🔐 WHOOP Manual Authentication\n');
  console.log('Step 1: Open this URL in your browser:\n');
  console.log(startUrl ?? authUrl);
  if (startUrl) {
    console.log('\n   (Resolved via non-browser bootstrap to avoid WHOOP blocking browser UAs on api.prod.whoop.com)');
  }
  console.log('\n---');
  console.log('\nStep 2: After authorizing, you\'ll be redirected to a URL like:');
  console.log(`   ${REDIRECT_URI}?code=XXXXX&state=${state}`);
  console.log('\nStep 3: Copy the "code" value from that URL');
  console.log('   (It may show an error page - that\'s OK, just copy from the address bar)\n');

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  const answer = await new Promise(resolve => {
    rl.question('Paste the code here: ', resolve);
  });
  rl.close();

  const code = answer.trim();
  if (!code) {
    console.error('❌ No code provided');
    process.exit(1);
  }

  const tokens = await exchangeCodeForToken(code, client_id, client_secret);
  if (tokens) {
    console.log('\n✅ Success! You can now use the WHOOP commands.');
  }
  process.exit(tokens ? 0 : 1);
}

async function browserAuth() {
  const { client_id, client_secret } = loadCredentials();
  const state = Math.random().toString(36).substring(2, 10);

  const authUrl = buildAuthUrl(client_id, state);
  const preflight = await preflightAuthUrl(authUrl);
  if (!preflight.ok) {
    console.error('\n❌ WHOOP authorization preflight failed.');
    if (preflight.reason === 'oauth_error') {
      console.error(`   Error: ${preflight.error}`);
      if (preflight.description) console.error(`   Description: ${preflight.description}`);
      if (preflight.hint) console.error(`   Hint: ${preflight.hint}`);
    } else {
      console.error(`   Reason: ${preflight.reason}`);
      if (preflight.error) console.error(`   Details: ${preflight.error}`);
    }
    console.error('\nMost common fix: update your WHOOP app Redirect URIs to match EXACTLY:');
    console.error(`   ${REDIRECT_URI}\n`);
    return false;
  }

  console.log('🔐 WHOOP Browser Authentication\n');
  console.log('Required redirect URI (must be in WHOOP app settings):');
  console.log(`   ${REDIRECT_URI}\n`);

  return new Promise((resolve) => {
    const isLocalRedirect = (REDIRECT_URL.hostname === 'localhost' || REDIRECT_URL.hostname === '127.0.0.1');
    // Important: when using a public HTTPS redirect (trycloudflare/ngrok/etc), the local listener is still plain HTTP
    // unless you're explicitly using https://localhost. Otherwise, tunnels like `cloudflared --url http://localhost:3000`
    // would break.
    const localProtocol = (isLocalRedirect && REDIRECT_URL.protocol === 'https:') ? 'https' : 'http';
    const serverOpts = localProtocol === 'https' ? ensureLocalTlsCert() : undefined;
    const server = (localProtocol === 'https' ? createHttpsServer(serverOpts, handler) : createHttpServer(handler));

    async function handler(req, res) {
      const url = new URL(req.url, `${localProtocol}://localhost:${LISTEN_PORT}`);

      if (url.pathname === CALLBACK_PATHNAME) {
        const code = url.searchParams.get('code');
        const error = url.searchParams.get('error');
        const errorDescription = url.searchParams.get('error_description');
        const errorHint = url.searchParams.get('error_hint');
        const returnedState = url.searchParams.get('state');

        if (error) {
          res.writeHead(400, { 'Content-Type': 'text/html' });
          res.end(
            `<h1>❌ Authorization Failed</h1>` +
            `<p><b>Error:</b> ${error}</p>` +
            (errorDescription ? `<p><b>Description:</b> ${errorDescription}</p>` : '') +
            (errorHint ? `<p><b>Hint:</b> ${errorHint}</p>` : '') +
            `<p>Check the terminal for details.</p>`
          );
          console.error(`\n❌ Authorization error: ${error}`);
          if (errorDescription) console.error(`   Description: ${errorDescription}`);
          if (errorHint) console.error(`   Hint: ${errorHint}`);
          server.close();
          resolve(false);
          return;
        }

        if (returnedState !== state) {
          res.writeHead(400, { 'Content-Type': 'text/html' });
          res.end('<h1>❌ State Mismatch</h1><p>Security check failed. Please try again.</p>');
          console.error('\n❌ State mismatch - possible CSRF attack');
          server.close();
          resolve(false);
          return;
        }

        if (code) {
          const tokens = await exchangeCodeForToken(code, client_id, client_secret);

          if (tokens) {
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end('<h1>✅ WHOOP Connected!</h1><p>You can close this window.</p>');
            server.close();
            resolve(true);
          } else {
            res.writeHead(400, { 'Content-Type': 'text/html' });
            res.end('<h1>❌ Token Exchange Failed</h1><p>Check the terminal for details.</p>');
            server.close();
            resolve(false);
          }
        }
      }
    }

    server.listen(LISTEN_PORT, () => {
      console.log(`Waiting for callback on ${localProtocol}://localhost:${LISTEN_PORT}${CALLBACK_PATHNAME}...`);
      if (!isLocalRedirect) {
        console.log(`Public redirect will hit: ${REDIRECT_URI}`);
      }
      if (localProtocol === 'https') {
        console.log('Note: your browser may show a TLS warning for localhost (self-signed cert). You must proceed to continue.');
      }
      console.log('Opening browser...\n');
      (async () => {
        const startUrl = await resolveWhoopBrowserLoginUrl(authUrl);
        if (startUrl) {
          console.log('Bootstrap OK. Opening id.whoop.com login URL (avoids browser UA block on api.prod.whoop.com)...\n');
          openInBrowser(startUrl);
        } else {
          console.log('Bootstrap failed. Falling back to opening the raw authorization URL...\n');
          openInBrowser(authUrl);
        }
      })();

      console.log('💡 If the browser doesn\'t open or you\'re on a different device:');
      console.log('   Run: node src/auth.js --manual\n');
    });

    // Timeout after 5 minutes
    setTimeout(() => {
      console.log('\n⏰ Timeout - no callback received after 5 minutes');
      console.log('   Try: node src/auth.js --manual');
      server.close();
      resolve(false);
    }, 5 * 60 * 1000);
  });
}

export async function getAccessToken() {
  migrateLegacyAuthFiles();
  if (!fs.existsSync(TOKEN_PATH)) {
    throw new Error(`Not authenticated. Run: node src/auth.js (token path: ${TOKEN_PATH})`);
  }

  const tokens = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));

  if (tokens.error) {
    throw new Error(`Auth failed: ${tokens.error}. Run: node src/auth.js`);
  }

  if (!tokens.access_token) {
    throw new Error('Invalid token. Run: node src/auth.js');
  }

  // Check if token is expired (tokens.expires_in is in seconds)
  const expiresAt = tokens.obtained_at + (tokens.expires_in * 1000);
  if (Date.now() >= expiresAt - 60000) { // Refresh 1 min before expiry
    return refreshAccessToken();
  }

  return tokens.access_token;
}

export async function refreshAccessToken() {
  migrateLegacyAuthFiles();
  if (!fs.existsSync(TOKEN_PATH)) {
    throw new Error(`Not authenticated. Missing token file: ${TOKEN_PATH}`);
  }

  const tokens = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
  if (!tokens.refresh_token) {
    throw new Error('Token has no refresh_token (did you request the "offline" scope?). Run: node src/auth.js');
  }

  console.log('🔄 Refreshing WHOOP token...');
  const { client_id, client_secret } = loadCredentials();
  const refreshRedirect = tokens.redirect_uri || REDIRECT_URI;

  const response = await fetch(WHOOP_TOKEN_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'refresh_token',
      refresh_token: tokens.refresh_token,
      client_id,
      client_secret,
      // WHOOP docs include scope in refresh requests.
      scope: 'offline',
      // In practice WHOOP may validate redirect_uri during refresh too.
      redirect_uri: refreshRedirect
    })
  });

  const newTokens = await response.json();
  if (newTokens.error) {
    throw new Error(`Token refresh failed: ${newTokens.error}. Run: node src/auth.js`);
  }

  newTokens.obtained_at = Date.now();
  // Preserve redirect_uri so future refreshes stay consistent, even if WHOOP doesn't echo it back.
  newTokens.redirect_uri = refreshRedirect;
  ensureDataDir();
  fs.writeFileSync(TOKEN_PATH, JSON.stringify(newTokens, null, 2));
  return newTokens.access_token;
}

// CLI entry point
if (import.meta.url === `file://${process.argv[1]}`) {
  const isManual = process.argv.includes('--manual') || process.argv.includes('-m');
  const isPrintUrl = process.argv.includes('--print-url');

  if (isPrintUrl) {
    const { client_id } = loadCredentials();
    const state = Math.random().toString(36).substring(2, 10);
    const authUrl = buildAuthUrl(client_id, state);
    const startUrl = await resolveWhoopBrowserLoginUrl(authUrl);
    // Print ONLY the URL for easy scripting: open "$(node src/auth.js --print-url)"
    console.log(startUrl ?? authUrl);
    process.exit(0);
  }

  if (isManual) {
    manualAuth();
  } else {
    const success = await browserAuth();
    process.exit(success ? 0 : 1);
  }
}
