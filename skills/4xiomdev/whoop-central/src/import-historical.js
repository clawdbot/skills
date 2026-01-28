#!/usr/bin/env node
/**
 * Import all historical WHOOP data to health-doctor logs
 * Fetches: recovery, sleep, strain, workouts
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { randomUUID } from 'crypto';
import { getAccessToken } from './auth.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const HEALTH_DIR = path.join(process.env.HOME, 'clawd', 'health', 'logs', 'whoop');
const WHOOP_API = 'https://api.prod.whoop.com/developer/v2';
const PAGE_LIMIT = 25; // WHOOP docs cap v2 collections at 25

// Helper to fetch with token
async function fetchWhoop(endpoint) {
  const accessToken = await getAccessToken();
  const response = await fetch(`${WHOOP_API}${endpoint}`, {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  });
  
  const text = await response.text();
  if (!response.ok) {
    throw new Error(`API error ${response.status}: ${text}`);
  }

  try {
    return JSON.parse(text);
  } catch {
    throw new Error(`API returned non-JSON for ${endpoint}: ${text.slice(0, 200)}`);
  }
}

// Log entry to JSONL
const existingIdsByFile = new Map(); // logFile -> Set(whoop_id)

function loadExistingIds(logFile) {
  if (existingIdsByFile.has(logFile)) return existingIdsByFile.get(logFile);
  const ids = new Set();
  if (fs.existsSync(logFile)) {
    const lines = fs.readFileSync(logFile, 'utf8').split('\n');
    for (const line of lines) {
      if (!line) continue;
      try {
        const entry = JSON.parse(line);
        const whoopId = entry?.meta?.whoop_id;
        if (whoopId) ids.add(String(whoopId));
      } catch {
        // Ignore malformed lines.
      }
    }
  }
  existingIdsByFile.set(logFile, ids);
  return ids;
}

function logEntry(category, data, timestamp, whoopId) {
  const date = new Date(timestamp);
  const month = date.toISOString().slice(0, 7); // YYYY-MM
  const logDir = path.join(HEALTH_DIR, category);
  
  // Create directory if needed
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
  }
  
  const logFile = path.join(logDir, `${month}.jsonl`);
  const ids = loadExistingIds(logFile);
  const whoopIdStr = whoopId != null ? String(whoopId) : null;
  if (whoopIdStr && ids.has(whoopIdStr)) return null;
  
  const entry = {
    id: randomUUID(),
    ts: timestamp,
    type: category,
    source: 'whoop',
    data: data,
    meta: { imported_at: new Date().toISOString(), whoop_id: whoopIdStr }
  };
  
  fs.appendFileSync(logFile, JSON.stringify(entry) + '\n');
  if (whoopIdStr) ids.add(whoopIdStr);
  return entry;
}

// Fetch and import recovery data
async function importRecovery() {
  console.log('📊 Fetching recovery data...');
  let imported = 0;
  let nextToken = null;
  
  do {
    const endpoint = `/recovery?limit=${PAGE_LIMIT}${nextToken ? `&nextToken=${encodeURIComponent(nextToken)}` : ''}`;
    const data = await fetchWhoop(endpoint);
    
    if (data.records && data.records.length > 0) {
      for (const rec of data.records) {
        const score = rec.score || {};
        const entry = logEntry('recovery', {
          cycle_id: rec.cycle_id,
          sleep_id: rec.sleep_id,
          score_state: rec.score_state,
          recovery_score: score.recovery_score,
          hrv_rmssd_milli: score.hrv_rmssd_milli,
          resting_heart_rate: score.resting_heart_rate,
          spo2_percentage: score.spo2_percentage,
          skin_temp_celsius: score.skin_temp_celsius
        }, rec.created_at, rec.cycle_id);
        if (entry) imported++;
      }
    }
    
    nextToken = data.next_token || data.nextToken;
  } while (nextToken);
  
  console.log(`  ✅ Imported ${imported} recovery records`);
  return imported;
}

// Fetch and import sleep data
async function importSleep() {
  console.log('😴 Fetching sleep data...');
  let imported = 0;
  let nextToken = null;
  
  do {
    const endpoint = `/activity/sleep?limit=${PAGE_LIMIT}${nextToken ? `&nextToken=${encodeURIComponent(nextToken)}` : ''}`;
    const data = await fetchWhoop(endpoint);
    
    if (data.records && data.records.length > 0) {
      for (const sleep of data.records) {
        const score = sleep.score || {};
        const stages = score.stage_summary || {};
        const entry = logEntry('sleep', {
          id: sleep.id,
          nap: sleep.nap,
          score_state: sleep.score_state,
          start: sleep.start,
          end: sleep.end,
          sleep_performance_percentage: score.sleep_performance_percentage,
          sleep_efficiency_percentage: score.sleep_efficiency_percentage,
          sleep_consistency_percentage: score.sleep_consistency_percentage,
          respiratory_rate: score.respiratory_rate,
          total_in_bed_time_milli: stages.total_in_bed_time_milli,
          total_awake_time_milli: stages.total_awake_time_milli,
          total_rem_sleep_time_milli: stages.total_rem_sleep_time_milli,
          total_slow_wave_sleep_time_milli: stages.total_slow_wave_sleep_time_milli,
          total_light_sleep_time_milli: stages.total_light_sleep_time_milli,
          disturbance_count: stages.disturbance_count,
          stage_summary: stages
        }, sleep.start, sleep.id);
        if (entry) imported++;
      }
    }
    
    nextToken = data.next_token || data.nextToken;
  } while (nextToken);
  
  console.log(`  ✅ Imported ${imported} sleep records`);
  return imported;
}

// Fetch and import cycle (strain) data
async function importStrain() {
  console.log('💪 Fetching strain/cycle data...');
  let imported = 0;
  let nextToken = null;
  
  do {
    const endpoint = `/cycle?limit=${PAGE_LIMIT}${nextToken ? `&nextToken=${encodeURIComponent(nextToken)}` : ''}`;
    const data = await fetchWhoop(endpoint);
    
    if (data.records && data.records.length > 0) {
      for (const cycle of data.records) {
        const score = cycle.score || {};
        const entry = logEntry('strain', {
          id: cycle.id,
          score_state: cycle.score_state,
          strain: score.strain,
          kilojoule: score.kilojoule,
          average_heart_rate: score.average_heart_rate,
          max_heart_rate: score.max_heart_rate,
          start: cycle.start,
          end: cycle.end
        }, cycle.start, cycle.id);
        if (entry) imported++;
      }
    }
    
    nextToken = data.next_token || data.nextToken;
  } while (nextToken);
  
  console.log(`  ✅ Imported ${imported} strain records`);
  return imported;
}

// Fetch and import workout data
async function importWorkouts() {
  console.log('🏋️ Fetching workout data...');
  let imported = 0;
  let nextToken = null;
  
  do {
    const endpoint = `/activity/workout?limit=${PAGE_LIMIT}${nextToken ? `&nextToken=${encodeURIComponent(nextToken)}` : ''}`;
    const data = await fetchWhoop(endpoint);
    
    if (data.records && data.records.length > 0) {
      for (const workout of data.records) {
        const score = workout.score || {};
        const entry = logEntry('workouts', {
          id: workout.id,
          sport_name: workout.sport_name,
          sport_id: workout.sport_id,
          score_state: workout.score_state,
          strain: score.strain,
          kilojoule: score.kilojoule,
          average_heart_rate: score.average_heart_rate,
          max_heart_rate: score.max_heart_rate,
          percent_recorded: score.percent_recorded,
          distance_meter: score.distance_meter,
          altitude_gain_meter: score.altitude_gain_meter,
          altitude_change_meter: score.altitude_change_meter,
          zone_durations: score.zone_durations,
          duration_minutes: Math.round((new Date(workout.end) - new Date(workout.start)) / 60000),
          start: workout.start,
          end: workout.end
        }, workout.start, workout.id);
        if (entry) imported++;
      }
    }
    
    nextToken = data.next_token || data.nextToken;
  } while (nextToken);
  
  console.log(`  ✅ Imported ${imported} workout records`);
  return imported;
}

// Main import
async function main() {
  console.log('🔄 Starting WHOOP historical import...\n');
  
  try {
    const stats = {
      recovery: await importRecovery(),
      sleep: await importSleep(),
      strain: await importStrain(),
      workouts: await importWorkouts()
    };
    
    console.log('\n📈 Import complete!');
    console.log('─'.repeat(40));
    console.log(`  Recovery: ${stats.recovery} records`);
    console.log(`  Sleep: ${stats.sleep} records`);
    console.log(`  Strain: ${stats.strain} records`);
    console.log(`  Workouts: ${stats.workouts} records`);
    console.log(`  Total: ${Object.values(stats).reduce((a, b) => a + b, 0)} records`);
    console.log(`\n💾 Data saved to: ${HEALTH_DIR}`);
  } catch (error) {
    console.error('❌ Import failed:', error.message);
    process.exit(1);
  }
}

main();
