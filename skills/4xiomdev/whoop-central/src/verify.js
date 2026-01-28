/**
 * WHOOP Skill Verification
 *
 * - Checks that the token works against the WHOOP API
 * - Optionally forces a refresh (useful to confirm refresh_token works)
 */

import fs from 'fs';
import path from 'path';
import { getAccessToken, refreshAccessToken } from './auth.js';

const DATA_DIR = process.env.WHOOP_DATA_DIR || path.join(process.env.HOME, '.clawdbot', 'whoop');
const TOKEN_PATH = process.env.WHOOP_TOKEN_PATH || path.join(DATA_DIR, 'token.json');
const WHOOP_API = 'https://api.prod.whoop.com/developer/v2';

async function verify(opts = {}) {
  if (!fs.existsSync(TOKEN_PATH)) {
    throw new Error(`Missing token file: ${TOKEN_PATH}`);
  }

  if (opts.refresh) {
    await refreshAccessToken();
  }

  const accessToken = await getAccessToken();
  const r = await fetch(`${WHOOP_API}/user/profile/basic`, {
    headers: { Authorization: `Bearer ${accessToken}` }
  });

  const text = await r.text();
  if (!r.ok) {
    throw new Error(`WHOOP API verify failed ${r.status}: ${text}`);
  }

  const profile = JSON.parse(text);
  const token = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));

  return {
    ok: true,
    profile,
    token_meta: {
      obtained_at: token.obtained_at,
      expires_in: token.expires_in,
      scope: token.scope,
      redirect_uri: token.redirect_uri
    }
  };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const isJson = process.argv.includes('--json');
  const forceRefresh = process.argv.includes('--refresh');

  try {
    const result = await verify({ json: isJson, refresh: forceRefresh });
    if (isJson) {
      process.stdout.write(JSON.stringify(result));
    } else {
      console.log('✅ WHOOP verify OK');
      console.log(`   User: ${result.profile.first_name} ${result.profile.last_name} (${result.profile.email})`);
      console.log(`   Scopes: ${result.token_meta.scope}`);
    }
  } catch (err) {
    console.error(`❌ ${err.message}`);
    process.exit(1);
  }
}

