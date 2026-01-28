/**
 * WHOOP "Today" Snapshot (prompt-friendly)
 *
 * Includes: recovery, sleep, strain (cycle), last workout.
 */

import { getAccessToken } from './auth.js';

const WHOOP_API = 'https://api.prod.whoop.com/developer/v2';

function fmtMins(mins) {
  const h = Math.floor(mins / 60);
  const m = mins % 60;
  return h > 0 ? `${h}h ${m}m` : `${m}m`;
}

function durationMinutes(start, end) {
  if (!start || !end) return null;
  const ms = new Date(end) - new Date(start);
  if (!Number.isFinite(ms) || ms < 0) return null;
  return Math.round(ms / 60000);
}

async function getToday(opts = {}) {
  const accessToken = await getAccessToken();
  const headers = { Authorization: `Bearer ${accessToken}` };

  const [recoveryRes, sleepRes, cycleRes, workoutRes] = await Promise.all([
    fetch(`${WHOOP_API}/recovery?limit=1`, { headers }),
    fetch(`${WHOOP_API}/activity/sleep?limit=1`, { headers }),
    fetch(`${WHOOP_API}/cycle?limit=1`, { headers }),
    fetch(`${WHOOP_API}/activity/workout?limit=1`, { headers })
  ]);

  for (const [name, res] of [
    ['recovery', recoveryRes],
    ['sleep', sleepRes],
    ['cycle', cycleRes],
    ['workout', workoutRes]
  ]) {
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`API error ${res.status} (${name}): ${text}`);
    }
  }

  const recovery = (await recoveryRes.json()).records?.[0] ?? null;
  const sleep = (await sleepRes.json()).records?.[0] ?? null;
  const cycle = (await cycleRes.json()).records?.[0] ?? null;
  const workout = (await workoutRes.json()).records?.[0] ?? null;

  const out = { recovery, sleep, cycle, workout };
  if (opts.json) return out;

  const lines = [];
  if (recovery?.score) {
    lines.push(`Recovery: ${recovery.score.recovery_score}% (HRV ${recovery.score.hrv_rmssd_milli?.toFixed(1)} ms, RHR ${recovery.score.resting_heart_rate} bpm)`);
  }
  if (sleep?.score?.stage_summary) {
    const st = sleep.score.stage_summary;
    const asleepMin = Math.round(((st.total_in_bed_time_milli || 0) - (st.total_awake_time_milli || 0)) / 60000);
    lines.push(`Sleep: ${fmtMins(asleepMin)} (Perf ${sleep.score.sleep_performance_percentage}%, Eff ${sleep.score.sleep_efficiency_percentage?.toFixed(1)}%)`);
  }
  if (cycle?.score) {
    lines.push(`Strain: ${cycle.score.strain?.toFixed(1)} (AvgHR ${cycle.score.average_heart_rate} / MaxHR ${cycle.score.max_heart_rate})`);
  }
  if (workout) {
    const mins = durationMinutes(workout.start, workout.end);
    const wStrain = workout.score?.strain;
    const name = workout.sport_name || `sport_id:${workout.sport_id ?? 'unknown'}`;
    lines.push(`Last workout: ${name} (${mins != null ? fmtMins(mins) : 'duration N/A'}, Strain ${wStrain != null ? wStrain.toFixed(1) : 'N/A'})`);
  }

  console.log(lines.join('\n'));
  return out;
}

export { getToday };

if (import.meta.url === `file://${process.argv[1]}`) {
  const isJson = process.argv.includes('--json');
  try {
    const result = await getToday({ json: isJson });
    if (isJson) process.stdout.write(JSON.stringify(result));
  } catch (err) {
    console.error(`❌ ${err.message}`);
    process.exit(1);
  }
}

