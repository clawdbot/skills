#!/usr/bin/env node
/**
 * AssemblyAI helper CLI for Clawdbot.
 *
 * No external deps.
 * Uses AssemblyAI REST API:
 *  - POST /v2/upload
 *  - POST /v2/transcript
 *  - GET  /v2/transcript/:id
 *  - GET  /v2/transcript/:id/paragraphs
 *  - GET  /v2/transcript/:id/sentences
 *  - GET  /v2/transcript/:id/:subtitle_format  (srt|vtt)
 */

import fs from 'node:fs';
import fsp from 'node:fs/promises';
import path from 'node:path';

const DEFAULT_BASE_URL = 'https://api.assemblyai.com';

if (typeof fetch !== 'function') {
  console.error('This script requires Node.js 18+ (built-in fetch).');
  process.exit(2);
}

function printUsageAndExit(code = 0) {
  const msg = `AssemblyAI helper CLI

Usage:
  assemblyai.mjs transcribe <path-or-url> [options]
  assemblyai.mjs get <transcript_id>
  assemblyai.mjs wait <transcript_id> [options]
  assemblyai.mjs paragraphs <transcript_id> [options]
  assemblyai.mjs sentences <transcript_id> [options]
  assemblyai.mjs subtitles <transcript_id> <srt|vtt> [options]

Options:
  --base-url <url>           Override API base URL (default: ${DEFAULT_BASE_URL})
  --api-key <key>            Override API key (default: env ASSEMBLYAI_API_KEY)
  --config <json|@file>      Extra JSON fields merged into POST /v2/transcript body
  --wait / --no-wait         Wait for completion (default: --wait)
  --poll-ms <ms>             Poll interval in ms while waiting (default: 3000)
  --timeout-ms <ms>          Timeout in ms while waiting (default: 1800000)
  --export <kind>            For 'transcribe': text|json|paragraphs|sentences|srt|vtt (default: text)
  --chars-per-caption <n>    For subtitles export (SRT/VTT) max chars per caption
  --format <kind>            Output format (get/wait: json|text|id; paragraphs/sentences: text|json)
  --out <path|->            Write final output to file instead of stdout (default: '-')
  --quiet                    Reduce stderr logging

Env vars:
  ASSEMBLYAI_API_KEY         AssemblyAI API key
  ASSEMBLYAI_BASE_URL        Alternative to --base-url
`;
  console.error(msg);
  process.exit(code);
}

function parseArgs(argv) {
  const flags = {};
  const positionals = [];

  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];

    if (a === '-h' || a === '--help') {
      flags.help = true;
      continue;
    }

    if (!a.startsWith('--')) {
      positionals.push(a);
      continue;
    }

    // --key=value
    const eq = a.indexOf('=');
    if (eq !== -1) {
      const key = a.slice(2, eq);
      const value = a.slice(eq + 1);
      flags[key] = value;
      continue;
    }

    const key = a.slice(2);
    if (key.startsWith('no-')) {
      flags[key.slice(3)] = false;
      continue;
    }

    const next = argv[i + 1];
    if (next === undefined || next.startsWith('--')) {
      flags[key] = true;
      continue;
    }

    flags[key] = next;
    i += 1;
  }

  return { flags, positionals };
}

function isHttpUrl(s) {
  return /^https?:\/\//i.test(s);
}

function getHomeDir() {
  return process.env.HOME || process.env.USERPROFILE || '';
}

function expandHome(p) {
  if (typeof p !== 'string') return p;
  const home = getHomeDir();
  if (!home) return p;
  if (p === '~') return home;
  if (p.startsWith('~/')) return path.join(home, p.slice(2));
  return p;
}

function normaliseBaseUrl(raw) {
  return String(raw || '').replace(/\/+$/, '');
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function readConfigArg(configArg) {
  if (!configArg) return {};

  if (typeof configArg !== 'string') {
    throw new Error('--config must be a JSON string or @path/to/file.json');
  }

  if (configArg.startsWith('@')) {
    const p = configArg.slice(1);
    const raw = await fsp.readFile(p, 'utf8');
    return JSON.parse(raw);
  }

  return JSON.parse(configArg);
}

async function request(baseUrl, apiKey, relOrAbsUrl, { method = 'GET', headers = {}, body } = {}) {
  const url = isHttpUrl(relOrAbsUrl) ? relOrAbsUrl : `${baseUrl}${relOrAbsUrl.startsWith('/') ? '' : '/'}${relOrAbsUrl}`;

  const res = await fetch(url, {
    method,
    headers: {
      Authorization: apiKey,
      ...headers,
    },
    body,
    // Required in Node when using a streaming request body
    ...(body && typeof body === 'object' && typeof body.pipe === 'function' ? { duplex: 'half' } : {}),
  });

  if (res.ok) return res;

  // Include response text to make debugging easier.
  const errText = await res.text().catch(() => '');
  const prefix = `HTTP ${res.status} ${res.statusText}`;
  throw new Error(errText ? `${prefix}: ${errText}` : prefix);
}

async function requestJson(baseUrl, apiKey, relOrAbsUrl, opts = {}) {
  const res = await request(baseUrl, apiKey, relOrAbsUrl, opts);
  return res.json();
}

async function requestText(baseUrl, apiKey, relOrAbsUrl, opts = {}) {
  const res = await request(baseUrl, apiKey, relOrAbsUrl, opts);
  return res.text();
}

async function uploadFile({ baseUrl, apiKey, filePath, quiet }) {
  const abs = path.resolve(expandHome(filePath));
  const stat = await fsp.stat(abs);

  if (!quiet) console.error(`[assemblyai] Uploading ${abs} (${stat.size} bytes) ...`);

  const stream = fs.createReadStream(abs);
  const json = await requestJson(baseUrl, apiKey, '/v2/upload', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/octet-stream',
      'Content-Length': String(stat.size),
    },
    body: stream,
  });

  if (!json?.upload_url) {
    throw new Error('Upload succeeded but response did not include upload_url');
  }

  if (!quiet) console.error(`[assemblyai] Uploaded. upload_url=${json.upload_url}`);

  return json.upload_url;
}

async function submitTranscript({ baseUrl, apiKey, audioUrl, config, quiet }) {
  const body = {
    audio_url: audioUrl,
    ...(config || {}),
  };

  if (!quiet) console.error('[assemblyai] Submitting transcript job ...');

  const json = await requestJson(baseUrl, apiKey, '/v2/transcript', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  if (!json?.id) {
    throw new Error('Transcript submission succeeded but response did not include id');
  }

  if (!quiet) console.error(`[assemblyai] Submitted. id=${json.id} status=${json.status}`);

  return json;
}

async function getTranscript({ baseUrl, apiKey, id }) {
  return requestJson(baseUrl, apiKey, `/v2/transcript/${encodeURIComponent(id)}`);
}

async function waitForTranscript({ baseUrl, apiKey, id, pollMs, timeoutMs, quiet }) {
  const start = Date.now();
  while (true) {
    const t = await getTranscript({ baseUrl, apiKey, id });

    if (t?.status === 'completed') return t;
    if (t?.status === 'error') {
      const msg = t?.error ? String(t.error) : 'Unknown AssemblyAI error';
      throw new Error(`Transcription failed (id=${id}): ${msg}`);
    }

    const elapsed = Date.now() - start;
    if (elapsed > timeoutMs) {
      throw new Error(`Timed out waiting for transcript (id=${id}) after ${elapsed}ms`);
    }

    if (!quiet) console.error(`[assemblyai] Waiting... status=${t?.status ?? 'unknown'} elapsed=${elapsed}ms`);
    await delay(pollMs);
  }
}

async function getParagraphs({ baseUrl, apiKey, id }) {
  return requestJson(baseUrl, apiKey, `/v2/transcript/${encodeURIComponent(id)}/paragraphs`);
}

async function getSentences({ baseUrl, apiKey, id }) {
  return requestJson(baseUrl, apiKey, `/v2/transcript/${encodeURIComponent(id)}/sentences`);
}

async function getSubtitles({ baseUrl, apiKey, id, subtitleFormat, charsPerCaption }) {
  const qp = charsPerCaption ? `?chars_per_caption=${encodeURIComponent(String(charsPerCaption))}` : '';
  const raw = await requestText(
    baseUrl,
    apiKey,
    `/v2/transcript/${encodeURIComponent(id)}/${encodeURIComponent(subtitleFormat)}${qp}`,
  );

  // The API reference examples show a JSON string, but some clients return plain text.
  // If it looks like a JSON string, decode it.
  const trimmed = raw.trim();
  if (trimmed.startsWith('"') && trimmed.endsWith('"')) {
    try {
      return JSON.parse(trimmed);
    } catch {
      // Fall through
    }
  }

  return raw;
}

async function writeOutput({ outPath, content }) {
  if (!outPath || outPath === '-') {
    process.stdout.write(content);
    if (!content.endsWith('\n')) process.stdout.write('\n');
    return;
  }

  await fsp.mkdir(path.dirname(outPath), { recursive: true });
  await fsp.writeFile(outPath, content, 'utf8');
}

function toTextFromParagraphs(paragraphsJson) {
  const paras = Array.isArray(paragraphsJson?.paragraphs) ? paragraphsJson.paragraphs : [];
  return paras.map((p) => String(p?.text ?? '')).filter(Boolean).join('\n\n');
}

function toTextFromSentences(sentencesJson) {
  const sents = Array.isArray(sentencesJson?.sentences) ? sentencesJson.sentences : [];
  return sents.map((s) => String(s?.text ?? '')).filter(Boolean).join('\n');
}

async function main() {
  const { flags, positionals } = parseArgs(process.argv.slice(2));
  if (flags.help || positionals.length === 0) printUsageAndExit(0);

  const command = positionals[0];
  const quiet = Boolean(flags.quiet);

  const baseUrl = normaliseBaseUrl(flags['base-url'] ?? process.env.ASSEMBLYAI_BASE_URL ?? DEFAULT_BASE_URL);
  const apiKey = String(flags['api-key'] ?? process.env.ASSEMBLYAI_API_KEY ?? '');
  if (!apiKey) {
    console.error('Missing API key. Set ASSEMBLYAI_API_KEY or pass --api-key.');
    process.exit(2);
  }

  const pollMs = Number(flags['poll-ms'] ?? 3000);
  const timeoutMs = Number(flags['timeout-ms'] ?? 1_800_000);
  const outPath = expandHome(String(flags.out ?? '-'));


  if (command === 'transcribe') {
    const audio = positionals[1];
    if (!audio) {
      console.error('transcribe requires <path-or-url>');
      printUsageAndExit(2);
    }

    const wait = flags.wait === false ? false : true;
    const exportKind = String(flags.export ?? 'text');

    const config = await readConfigArg(flags.config).catch((err) => {
      console.error(`Failed to parse --config: ${err?.message ?? err}`);
      process.exit(2);
    });

    const audioUrl = isHttpUrl(audio)
      ? audio
      : await uploadFile({ baseUrl, apiKey, filePath: expandHome(audio), quiet });

    const submitted = await submitTranscript({ baseUrl, apiKey, audioUrl, config, quiet });

    if (!wait) {
      const minimal = {
        id: submitted.id,
        status: submitted.status,
        audio_url: submitted.audio_url,
      };
      await writeOutput({ outPath, content: JSON.stringify(minimal, null, 2) + '\n' });
      return;
    }

    const done = await waitForTranscript({ baseUrl, apiKey, id: submitted.id, pollMs, timeoutMs, quiet });

    if (exportKind === 'json') {
      await writeOutput({ outPath, content: JSON.stringify(done, null, 2) + '\n' });
      return;
    }

    if (exportKind === 'paragraphs') {
      const paragraphs = await getParagraphs({ baseUrl, apiKey, id: done.id });
      const text = String(flags.format ?? 'text') === 'json'
        ? JSON.stringify(paragraphs, null, 2) + '\n'
        : toTextFromParagraphs(paragraphs) + '\n';
      await writeOutput({ outPath, content: text });
      return;
    }

    if (exportKind === 'sentences') {
      const sentences = await getSentences({ baseUrl, apiKey, id: done.id });
      const text = String(flags.format ?? 'text') === 'json'
        ? JSON.stringify(sentences, null, 2) + '\n'
        : toTextFromSentences(sentences) + '\n';
      await writeOutput({ outPath, content: text });
      return;
    }

    if (exportKind === 'srt' || exportKind === 'vtt') {
      const charsPerCaption = flags['chars-per-caption'] ? Number(flags['chars-per-caption']) : undefined;
      const subs = await getSubtitles({ baseUrl, apiKey, id: done.id, subtitleFormat: exportKind, charsPerCaption });
      await writeOutput({ outPath, content: String(subs) });
      return;
    }

    // Default: text
    await writeOutput({ outPath, content: String(done.text ?? '') });
    return;
  }

  if (command === 'get') {
    const id = positionals[1];
    if (!id) {
      console.error('get requires <transcript_id>');
      printUsageAndExit(2);
    }

    const wait = flags.wait === true;
    const format = String(flags.format ?? 'json');

    const transcript = wait
      ? await waitForTranscript({ baseUrl, apiKey, id, pollMs, timeoutMs, quiet })
      : await getTranscript({ baseUrl, apiKey, id });

    if (format === 'id') {
      await writeOutput({ outPath, content: String(transcript?.id ?? id) });
      return;
    }

    if (format === 'text') {
      await writeOutput({ outPath, content: String(transcript?.text ?? '') });
      return;
    }

    await writeOutput({ outPath, content: JSON.stringify(transcript, null, 2) + '\n' });
    return;
  }

  if (command === 'wait') {
    const id = positionals[1];
    if (!id) {
      console.error('wait requires <transcript_id>');
      printUsageAndExit(2);
    }

    const format = String(flags.format ?? 'json');
    const done = await waitForTranscript({ baseUrl, apiKey, id, pollMs, timeoutMs, quiet });

    if (format === 'id') {
      await writeOutput({ outPath, content: String(done?.id ?? id) });
      return;
    }

    if (format === 'text') {
      await writeOutput({ outPath, content: String(done?.text ?? '') });
      return;
    }

    await writeOutput({ outPath, content: JSON.stringify(done, null, 2) + '\n' });
    return;
  }

  if (command === 'paragraphs') {
    const id = positionals[1];
    if (!id) {
      console.error('paragraphs requires <transcript_id>');
      printUsageAndExit(2);
    }

    const format = String(flags.format ?? 'text');
    const json = await getParagraphs({ baseUrl, apiKey, id });

    if (format === 'json') {
      await writeOutput({ outPath, content: JSON.stringify(json, null, 2) + '\n' });
      return;
    }

    await writeOutput({ outPath, content: toTextFromParagraphs(json) + '\n' });
    return;
  }

  if (command === 'sentences') {
    const id = positionals[1];
    if (!id) {
      console.error('sentences requires <transcript_id>');
      printUsageAndExit(2);
    }

    const format = String(flags.format ?? 'text');
    const json = await getSentences({ baseUrl, apiKey, id });

    if (format === 'json') {
      await writeOutput({ outPath, content: JSON.stringify(json, null, 2) + '\n' });
      return;
    }

    await writeOutput({ outPath, content: toTextFromSentences(json) + '\n' });
    return;
  }

  if (command === 'subtitles') {
    const id = positionals[1];
    const subtitleFormat = positionals[2];

    if (!id || !subtitleFormat) {
      console.error('subtitles requires <transcript_id> <srt|vtt>');
      printUsageAndExit(2);
    }

    const charsPerCaption = flags['chars-per-caption'] ? Number(flags['chars-per-caption']) : undefined;
    const subs = await getSubtitles({ baseUrl, apiKey, id, subtitleFormat, charsPerCaption });
    await writeOutput({ outPath, content: String(subs) });
    return;
  }

  console.error(`Unknown command: ${command}`);
  printUsageAndExit(2);
}

main().catch((err) => {
  console.error(err?.stack ?? err);
  process.exit(1);
});
