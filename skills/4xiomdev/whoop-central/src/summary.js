/**
 * WHOOP Daily Summary (v2 API)
 */

import { getAccessToken } from './auth.js';

const WHOOP_API = 'https://api.prod.whoop.com/developer/v2';

function formatDuration(ms) {
  const hours = Math.floor(ms / 3600000);
  const mins = Math.floor((ms % 3600000) / 60000);
  return `${hours}h ${mins}m`;
}

function getRecoveryEmoji(score) {
  if (score >= 67) return '💚';
  if (score >= 34) return '💛';
  return '❤️';
}

async function getSummary(opts = {}) {
  const accessToken = await getAccessToken();
  const headers = { 'Authorization': `Bearer ${accessToken}` };

  // Fetch all data in parallel
  const [recoveryRes, sleepRes, cycleRes] = await Promise.all([
    fetch(`${WHOOP_API}/recovery?limit=1`, { headers }),
    fetch(`${WHOOP_API}/activity/sleep?limit=1`, { headers }),
    fetch(`${WHOOP_API}/cycle?limit=1`, { headers })
  ]);

  for (const [name, res] of [
    ['recovery', recoveryRes],
    ['sleep', sleepRes],
    ['cycle', cycleRes]
  ]) {
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`API error ${res.status} (${name}): ${text}`);
    }
  }

  const recovery = (await recoveryRes.json()).records?.[0];
  const sleep = (await sleepRes.json()).records?.[0];
  const cycle = (await cycleRes.json()).records?.[0];

  if (opts.json) {
    return { recovery, sleep, cycle };
  }

  console.log('╔════════════════════════════════════════╗');
  console.log('║         WHOOP DAILY SUMMARY            ║');
  console.log('╚════════════════════════════════════════╝');
  console.log('');

  // Recovery
  if (recovery?.score) {
    const r = recovery.score;
    const emoji = getRecoveryEmoji(r.recovery_score);
    console.log(`${emoji} RECOVERY: ${r.recovery_score}%`);
    console.log(`   HRV: ${r.hrv_rmssd_milli?.toFixed(1)} ms`);
    console.log(`   Resting HR: ${r.resting_heart_rate} bpm`);
    console.log(`   SpO2: ${r.spo2_percentage?.toFixed(1)}%`);
    console.log('');
  }

  // Sleep
  if (sleep?.score) {
    const s = sleep.score;
    const stages = s.stage_summary;
    const totalSleep = stages.total_in_bed_time_milli - stages.total_awake_time_milli;
    console.log(`😴 SLEEP: ${formatDuration(totalSleep)}`);
    console.log(`   Performance: ${s.sleep_performance_percentage}%`);
    console.log(`   REM: ${formatDuration(stages.total_rem_sleep_time_milli)}`);
    console.log(`   Deep: ${formatDuration(stages.total_slow_wave_sleep_time_milli)}`);
    console.log(`   Efficiency: ${s.sleep_efficiency_percentage?.toFixed(1)}%`);
    console.log('');
  }

  // Strain
  if (cycle?.score) {
    const c = cycle.score;
    console.log(`🔥 STRAIN: ${c.strain?.toFixed(1)}`);
    console.log(`   Calories: ${Math.round(c.kilojoule / 4.184)} kcal`);
    console.log(`   Avg HR: ${c.average_heart_rate} bpm`);
    console.log(`   Max HR: ${c.max_heart_rate} bpm`);
  }

  console.log('');
  console.log('─'.repeat(42));

  return { recovery, sleep, cycle };
}

export { getSummary };

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  const isJson = process.argv.includes('--json');
  const isJsonl = process.argv.includes('--jsonl');

  try {
    const result = await getSummary({ json: isJson || isJsonl });
    if (isJson) process.stdout.write(JSON.stringify(result));
    if (isJsonl) process.stdout.write(JSON.stringify(result) + '\n');
  } catch (err) {
    console.error(`❌ ${err.message}`);
    process.exit(1);
  }
}
