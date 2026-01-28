/**
 * Get WHOOP Sleep Data (v2 API)
 */

import { getAccessToken } from './auth.js';

const WHOOP_API = 'https://api.prod.whoop.com/developer/v2';

function formatDuration(ms) {
  const hours = Math.floor(ms / 3600000);
  const mins = Math.floor((ms % 3600000) / 60000);
  return `${hours}h ${mins}m`;
}

function parseSince(s) {
  const m = String(s || '').trim().match(/^(\d+)([dh])$/i);
  if (!m) return null;
  const n = Number(m[1]);
  const unit = m[2].toLowerCase();
  const ms = unit === 'd' ? n * 86400_000 : n * 3600_000;
  return new Date(Date.now() - ms).toISOString();
}

async function getSleep(limit = 3, opts = {}) {
  const accessToken = await getAccessToken();

  const params = new URLSearchParams({ limit: String(limit) });
  if (opts.start) params.set('start', opts.start);
  if (opts.end) params.set('end', opts.end);

  const response = await fetch(`${WHOOP_API}/activity/sleep?${params}`, {
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
    console.log('😴 WHOOP Sleep');
    console.log('─'.repeat(40));

    records.forEach((rec) => {
      const score = rec.score;
      const stages = score.stage_summary;
      const date = new Date(rec.start).toLocaleDateString();
      const isNap = rec.nap ? ' (nap)' : '';

      console.log(`\n[${date}]${isNap}`);
      console.log(`  Time in Bed: ${formatDuration(stages.total_in_bed_time_milli)}`);
      console.log(`  Time Asleep: ${formatDuration(stages.total_in_bed_time_milli - stages.total_awake_time_milli)}`);
      console.log(`  REM: ${formatDuration(stages.total_rem_sleep_time_milli)}`);
      console.log(`  Deep: ${formatDuration(stages.total_slow_wave_sleep_time_milli)}`);
      console.log(`  Light: ${formatDuration(stages.total_light_sleep_time_milli)}`);
      console.log(`  Efficiency: ${score.sleep_efficiency_percentage?.toFixed(1)}%`);
      console.log(`  Performance: ${score.sleep_performance_percentage}%`);
      console.log(`  Respiratory: ${score.respiratory_rate?.toFixed(1)} rpm`);
    });

    return records;
  } else {
    console.log('No sleep data found');
    return [];
  }
}

export { getSleep };

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

    const records = await getSleep(limit, { json: isJson, jsonl: isJsonl, start: computedStart, end: end || null });
    if (isJson) process.stdout.write(JSON.stringify(records));
    if (isJsonl) {
      for (const rec of records) process.stdout.write(JSON.stringify(rec) + '\n');
    }
  } catch (err) {
    console.error(`❌ ${err.message}`);
    process.exit(1);
  }
}
