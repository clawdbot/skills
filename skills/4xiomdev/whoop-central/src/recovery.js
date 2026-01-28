/**
 * Get WHOOP Recovery Data (v2 API)
 */

import { getAccessToken } from './auth.js';

const WHOOP_API = 'https://api.prod.whoop.com/developer/v2';

function parseSince(s) {
  const m = String(s || '').trim().match(/^(\d+)([dh])$/i);
  if (!m) return null;
  const n = Number(m[1]);
  const unit = m[2].toLowerCase();
  const ms = unit === 'd' ? n * 86400_000 : n * 3600_000;
  return new Date(Date.now() - ms).toISOString();
}

async function getRecovery(limit = 3, opts = {}) {
  const accessToken = await getAccessToken();

  const params = new URLSearchParams({ limit: String(limit) });
  if (opts.start) params.set('start', opts.start);
  if (opts.end) params.set('end', opts.end);

  const response = await fetch(`${WHOOP_API}/recovery?${params}`, {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`API error ${response.status}: ${text}`);
  }

  const data = await response.json();
  const records = data.records || [];

  if (opts.json || opts.jsonl) {
    return records;
  }

  if (records.length > 0) {
    console.log('💚 WHOOP Recovery');
    console.log('─'.repeat(40));

    records.forEach((rec) => {
      const score = rec.score;
      const date = new Date(rec.created_at).toLocaleDateString();
      console.log(`\n[${date}]`);
      console.log(`  Recovery: ${score.recovery_score}%`);
      console.log(`  HRV: ${score.hrv_rmssd_milli?.toFixed(1)} ms`);
      console.log(`  Resting HR: ${score.resting_heart_rate} bpm`);
      console.log(`  SpO2: ${score.spo2_percentage?.toFixed(1)}%`);
      console.log(`  Skin Temp: ${score.skin_temp_celsius?.toFixed(1)}°C`);
    });

    return records;
  } else {
    console.log('No recovery data found');
    return [];
  }
}

export { getRecovery };

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  const isJson = process.argv.includes('--json');
  const isJsonl = process.argv.includes('--jsonl');
  const limitIdx = process.argv.findIndex(a => a === '--limit');
  const limit = limitIdx !== -1 ? Number(process.argv[limitIdx + 1]) : 3;

  try {
    const startIdx = process.argv.findIndex(a => a === '--start');
    const endIdx = process.argv.findIndex(a => a === '--end');
    const daysIdx = process.argv.findIndex(a => a === '--days');
    const sinceIdx = process.argv.findIndex(a => a === '--since');

    const start = startIdx !== -1 ? String(process.argv[startIdx + 1] || '').trim() : null;
    const end = endIdx !== -1 ? String(process.argv[endIdx + 1] || '').trim() : null;
    const days = daysIdx !== -1 ? Number(process.argv[daysIdx + 1]) : null;
    const since = sinceIdx !== -1 ? String(process.argv[sinceIdx + 1] || '').trim() : null;

    const computedStart = start || (Number.isFinite(days) ? new Date(Date.now() - days * 86400_000).toISOString() : null) || parseSince(since);

    const records = await getRecovery(limit, { json: isJson, jsonl: isJsonl, start: computedStart, end: end || null });
    if (isJson) process.stdout.write(JSON.stringify(records));
    if (isJsonl) {
      for (const rec of records) process.stdout.write(JSON.stringify(rec) + '\n');
    }
  } catch (err) {
    console.error(`❌ ${err.message}`);
    process.exit(1);
  }
}
