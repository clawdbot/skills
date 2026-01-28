/**
 * WHOOP Skill Setup (no network calls)
 *
 * Creates files in ~/.clawdbot/whoop/:
 * - credentials.json
 * - token.json (optional, if user pastes Postman tokens)
 */

import fs from 'fs';
import path from 'path';
import readline from 'readline';

const DATA_DIR = process.env.WHOOP_DATA_DIR || path.join(process.env.HOME, '.clawdbot', 'whoop');
const CREDENTIALS_PATH = process.env.WHOOP_CREDENTIALS_PATH || path.join(DATA_DIR, 'credentials.json');
const TOKEN_PATH = process.env.WHOOP_TOKEN_PATH || path.join(DATA_DIR, 'token.json');

function ensureDir() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
}

function rlQuestion(rl, q) {
  return new Promise(resolve => rl.question(q, resolve));
}

function nowMs() {
  return Date.now();
}

async function main() {
  ensureDir();

  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  console.log('🏋️  WHOOP Central Setup\n');
  console.log(`This will write:\n- ${CREDENTIALS_PATH}\n- ${TOKEN_PATH} (optional)\n`);

  const redirectDefault = 'https://localhost:3000/callback';
  const redirectUri = (await rlQuestion(rl, `Redirect URI [${redirectDefault}]: `)).trim() || redirectDefault;

  const clientId = (await rlQuestion(rl, 'WHOOP Client ID: ')).trim();
  const clientSecret = (await rlQuestion(rl, 'WHOOP Client Secret: ')).trim();

  if (!clientId || !clientSecret) {
    rl.close();
    console.error('\n❌ Missing client id/secret. Aborting.');
    process.exit(1);
  }

  const creds = { client_id: clientId, client_secret: clientSecret };
  fs.writeFileSync(CREDENTIALS_PATH, JSON.stringify(creds, null, 2) + '\n');
  console.log(`\n✅ Saved credentials: ${CREDENTIALS_PATH}`);

  const hasTokens = (await rlQuestion(rl, '\nDo you already have tokens (from Postman) to paste now? [y/N]: '))
    .trim()
    .toLowerCase()
    .startsWith('y');

  if (!hasTokens) {
    rl.close();
    console.log('\nNext: authenticate to generate tokens.\n');
    console.log('Option A (recommended):');
    console.log('  node src/auth.js\n');
    console.log('Option B (fallback): use Postman to obtain access_token + refresh_token, then paste into token.json.\n');
    console.log('Tip: when using Postman, make sure Client Authentication is "Send client credentials in body" (client_secret_post).\n');
    console.log(`When you have tokens, create: ${TOKEN_PATH}`);
    console.log('Then run:');
    console.log(`  WHOOP_REDIRECT_URI='${redirectUri}' node src/verify.js`);
    process.exit(0);
  }

  const accessToken = (await rlQuestion(rl, 'access_token: ')).trim();
  const refreshToken = (await rlQuestion(rl, 'refresh_token: ')).trim();
  const scopeDefault = 'offline read:profile';
  const scope = (await rlQuestion(rl, `scope [${scopeDefault}]: `)).trim() || scopeDefault;
  const expiresInRaw = (await rlQuestion(rl, 'expires_in seconds [3600]: ')).trim() || '3600';
  const expiresIn = Number(expiresInRaw);

  if (!accessToken || !refreshToken || !Number.isFinite(expiresIn)) {
    rl.close();
    console.error('\n❌ Missing/invalid token fields. Aborting.');
    process.exit(1);
  }

  const token = {
    access_token: accessToken,
    refresh_token: refreshToken,
    expires_in: expiresIn,
    scope,
    token_type: 'bearer',
    redirect_uri: redirectUri,
    obtained_at: nowMs()
  };

  fs.writeFileSync(TOKEN_PATH, JSON.stringify(token, null, 2) + '\n');
  rl.close();

  console.log(`\n✅ Saved token: ${TOKEN_PATH}`);
  console.log('\nVerify:');
  console.log(`  WHOOP_REDIRECT_URI='${redirectUri}' node src/verify.js`);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(err => {
    console.error(`❌ ${err.message}`);
    process.exit(1);
  });
}

