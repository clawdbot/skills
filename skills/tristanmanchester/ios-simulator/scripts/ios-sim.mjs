#!/usr/bin/env node
/**
 * ios-sim.mjs — token-efficient iOS Simulator automation for AI agents
 *
 * - Uses `xcrun simctl` for simulator/app management
 * - Uses `idb` for accessibility tree + input synthesis (optional)
 *
 * No third-party dependencies. Node >= 18 recommended.
 */

import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";

const STATE_FILE_DEFAULT = process.env.IOS_SIM_STATE_FILE || path.join(process.cwd(), ".ios-sim-state.json");

function nowIsoCompact() {
  return new Date().toISOString().replace(/[:.]/g, "-");
}

function isMacOS() {
  return process.platform === "darwin";
}

function exitWithError(message, extra = {}) {
  const payload = { ok: false, error: message, ...extra };
  // Always JSON on stderr for easy parsing
  process.stderr.write(JSON.stringify(payload) + "\n");
  process.exit(1);
}

function parseArgv(argv) {
  /** supports:
   * - --k v
   * - --k=v
   * - boolean flags
   * - terminator: --
   */
  const out = { _: [], flags: {}, passthrough: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--") {
      out.passthrough = argv.slice(i + 1);
      break;
    }
    if (a.startsWith("--")) {
      const eq = a.indexOf("=");
      if (eq !== -1) {
        const k = a.slice(2, eq);
        const v = a.slice(eq + 1);
        out.flags[k] = v === "" ? true : v;
      } else {
        const k = a.slice(2);
        const next = argv[i + 1];
        if (next !== undefined && !next.startsWith("--")) {
          out.flags[k] = next;
          i++;
        } else {
          out.flags[k] = true;
        }
      }
    } else {
      out._.push(a);
    }
  }
  return out;
}

function toBool(v, defaultValue = false) {
  if (v === undefined) return defaultValue;
  if (v === true) return true;
  if (v === false) return false;
  const s = String(v).toLowerCase().trim();
  if (["1", "true", "yes", "y", "on"].includes(s)) return true;
  if (["0", "false", "no", "n", "off"].includes(s)) return false;
  return defaultValue;
}

function toNumber(v, defaultValue = undefined) {
  if (v === undefined) return defaultValue;
  const n = Number(v);
  return Number.isFinite(n) ? n : defaultValue;
}

function emit(result, { pretty = false, text = false } = {}) {
  if (text && Array.isArray(result?.summary)) {
    process.stdout.write(result.summary.join("\n") + "\n");
    return;
  }
  process.stdout.write(JSON.stringify(result, null, pretty ? 2 : 0) + "\n");
}

function loadState(stateFile) {
  try {
    const raw = fs.readFileSync(stateFile, "utf8");
    const obj = JSON.parse(raw);
    return typeof obj === "object" && obj ? obj : {};
  } catch {
    return {};
  }
}

function saveState(stateFile, state) {
  fs.writeFileSync(stateFile, JSON.stringify(state, null, 2) + "\n", "utf8");
}

function normalise(s) {
  return String(s ?? "").toLowerCase().replace(/\s+/g, " ").trim();
}

function looksLikeUuid(s) {
  return /^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$/.test(String(s));
}

function looksLikeBundleId(s) {
  return /^[A-Za-z0-9.-]+$/.test(String(s)) && String(s).includes(".");
}

function whichSync(bin) {
  const envPath = process.env.PATH || "";
  const parts = envPath.split(path.delimiter);
  for (const p of parts) {
    const full = path.join(p, bin);
    try {
      fs.accessSync(full, fs.constants.X_OK);
      return full;
    } catch {}
  }
  return null;
}

async function run(cmd, args, {
  stdin = null,
  timeoutMs = 0,
  cwd = process.cwd(),
  env = process.env,
  allowNonZero = false,
} = {}) {
  return await new Promise((resolve, reject) => {
    const child = spawn(cmd, args, {
      stdio: ["pipe", "pipe", "pipe"],
      cwd,
      env,
      shell: false,
    });

    let stdout = "";
    let stderr = "";

    const killTimer = timeoutMs > 0 ? setTimeout(() => {
      child.kill("SIGKILL");
    }, timeoutMs) : null;

    child.stdout.on("data", (d) => { stdout += d.toString("utf8"); });
    child.stderr.on("data", (d) => { stderr += d.toString("utf8"); });

    child.on("error", (err) => {
      if (killTimer) clearTimeout(killTimer);
      reject(err);
    });

    child.on("close", (code, signal) => {
      if (killTimer) clearTimeout(killTimer);
      const ok = code === 0;
      if (!ok && !allowNonZero) {
        const error = new Error(`Command failed: ${cmd} ${args.join(" ")} (exit ${code}${signal ? `, signal ${signal}` : ""})`);
        error.stdout = stdout;
        error.stderr = stderr;
        error.code = code;
        error.signal = signal;
        reject(error);
        return;
      }
      resolve({ code, signal, stdout, stderr });
    });

    if (stdin !== null) {
      child.stdin.write(stdin);
    }
    child.stdin.end();
  });
}

async function runJson(cmd, args, opts = {}) {
  const { stdout, stderr } = await run(cmd, args, opts);
  try {
    const trimmed = stdout.trim();
    const parsed = trimmed ? JSON.parse(trimmed) : null;
    return { json: parsed, stdout, stderr };
  } catch (e) {
    const err = new Error(`Expected JSON from: ${cmd} ${args.join(" ")}`);
    err.cause = e;
    err.stdout = stdout;
    err.stderr = stderr;
    throw err;
  }
}

async function simctlListFull() {
  const { json } = await runJson("xcrun", ["simctl", "list", "--json"]);
  return json;
}

function flattenDevices(listJson) {
  // listJson.devices: { [runtimeId]: [{name, udid, state, isAvailable, availabilityError?...}, ...] }
  const runtimes = Array.isArray(listJson?.runtimes) ? listJson.runtimes : [];
  const runtimeById = new Map();
  for (const r of runtimes) {
    if (r?.identifier) runtimeById.set(r.identifier, r);
  }

  const out = [];
  const devicesObj = listJson?.devices || {};
  for (const [runtimeId, devs] of Object.entries(devicesObj)) {
    const runtime = runtimeById.get(runtimeId) || {};
    for (const d of (Array.isArray(devs) ? devs : [])) {
      out.push({
        runtimeId,
        runtimeName: runtime?.name || runtimeId,
        runtimeVersion: runtime?.version || "",
        runtimeAvailable: runtime?.isAvailable !== false,
        name: d?.name,
        udid: d?.udid,
        state: d?.state,
        isAvailable: d?.isAvailable !== false,
        availabilityError: d?.availabilityError || null,
      });
    }
  }
  return out;
}

function parseVersion(v) {
  const parts = String(v || "").split(".").map((x) => Number(x));
  if (!parts.length || parts.some((n) => !Number.isFinite(n))) return [-1];
  return parts;
}

function cmpVersions(a, b) {
  const pa = parseVersion(a);
  const pb = parseVersion(b);
  const n = Math.max(pa.length, pb.length);
  for (let i = 0; i < n; i++) {
    const da = pa[i] ?? 0;
    const db = pb[i] ?? 0;
    if (da !== db) return da - db;
  }
  return 0;
}

function pickBestDevice(devices, { nameSubstr = null, runtimeSubstr = null } = {}) {
  let xs = devices.filter((d) => d?.udid && looksLikeUuid(d.udid));
  xs = xs.filter((d) => d.isAvailable);

  if (nameSubstr) {
    const q = normalise(nameSubstr);
    xs = xs.filter((d) => normalise(d.name).includes(q));
  }
  if (runtimeSubstr) {
    const q = normalise(runtimeSubstr);
    xs = xs.filter((d) =>
      normalise(d.runtimeName).includes(q) || normalise(d.runtimeId).includes(q)
    );
  }

  // Prefer booted, then newer runtime version, then name
  xs.sort((a, b) => {
    const aBoot = a.state === "Booted" ? 1 : 0;
    const bBoot = b.state === "Booted" ? 1 : 0;
    if (aBoot !== bBoot) return bBoot - aBoot;

    const vcmp = cmpVersions(a.runtimeVersion, b.runtimeVersion);
    if (vcmp !== 0) return -vcmp; // descending

    return String(a.name).localeCompare(String(b.name));
  });

  return xs[0] || null;
}

async function resolveUdid({ udid, stateFile }) {
  if (udid) {
    if (!looksLikeUuid(udid)) exitWithError(`Invalid --udid (expected UUID)`, { udid });
    return udid;
  }

  const state = loadState(stateFile);
  if (state?.udid && looksLikeUuid(state.udid)) return state.udid;

  // Fallback: if exactly one booted device, use it.
  const listJson = await simctlListFull();
  const devices = flattenDevices(listJson);
  const booted = devices.filter((d) => d.state === "Booted" && d.isAvailable);
  if (booted.length === 1) return booted[0].udid;

  // Else pick "best" available iPhone device.
  const best = pickBestDevice(devices, { nameSubstr: "iPhone", runtimeSubstr: "iOS" }) || pickBestDevice(devices);
  if (best) return best.udid;

  exitWithError("Could not resolve a simulator UDID. Use `select` or pass --udid.", { stateFile });
}

async function cmdHealth({ pretty, text }) {
  const checks = [];

  const xcrunPath = whichSync("xcrun");
  checks.push({ name: "xcrun", ok: !!xcrunPath, path: xcrunPath });

  if (!isMacOS()) {
    emit({
      ok: false,
      summary: [
        "Not running on macOS.",
        "Run this skill on a macOS gateway/node with Xcode tools installed.",
      ],
      checks,
    }, { pretty, text });
    process.exit(2);
  }

  if (!xcrunPath) {
    emit({
      ok: false,
      summary: [
        "xcrun not found in PATH.",
        "Install Xcode Command Line Tools or full Xcode.",
      ],
      checks,
    }, { pretty, text });
    process.exit(2);
  }

  // Check simctl discoverable
  try {
    const { stdout } = await run("xcrun", ["--find", "simctl"]);
    checks.push({ name: "simctl", ok: true, path: stdout.trim() });
  } catch (e) {
    checks.push({ name: "simctl", ok: false, error: String(e?.stderr || e?.message || e) });
  }

  // List devices
  try {
    const listJson = await simctlListFull();
    const devices = flattenDevices(listJson);
    const booted = devices.filter((d) => d.state === "Booted" && d.isAvailable);
    checks.push({ name: "simctl list", ok: true, deviceCount: devices.length, bootedCount: booted.length });
  } catch (e) {
    checks.push({ name: "simctl list", ok: false, error: String(e?.stderr || e?.message || e) });
  }

  // idb optional
  const idbPath = whichSync("idb");
  checks.push({ name: "idb", ok: !!idbPath, path: idbPath, optional: true });

  const ok = checks.every((c) => c.ok || c.optional);

  const summary = [];
  summary.push(ok ? "Environment OK (idb optional)." : "Environment check failed.");
  for (const c of checks) {
    summary.push(`${c.ok ? "✓" : c.optional ? "·" : "✗"} ${c.name}${c.path ? ` (${c.path})` : ""}`);
  }
  if (!idbPath) summary.push("Install idb for UI automation: brew install idb-companion; pip install fb-idb");

  emit({ ok, checks, summary }, { pretty, text });
  process.exit(ok ? 0 : 2);
}

async function cmdList({ full, pretty, text }) {
  const listJson = await simctlListFull();
  const devices = flattenDevices(listJson);
  const booted = devices.filter((d) => d.state === "Booted" && d.isAvailable);
  const available = devices.filter((d) => d.isAvailable);

  const summary = [
    `Available devices: ${available.length}`,
    `Booted devices: ${booted.length}`,
  ];
  if (booted.length) {
    for (const d of booted.slice(0, 5)) {
      summary.push(`- ${d.name} (${d.runtimeName}) ${d.udid}`);
    }
    if (booted.length > 5) summary.push(`… +${booted.length - 5} more`);
  }

  if (full) {
    emit({ ok: true, list: listJson }, { pretty, text });
  } else {
    emit({
      ok: true,
      devices: booted.map((d) => ({ name: d.name, udid: d.udid, runtime: d.runtimeName, state: d.state })),
      counts: { available: available.length, booted: booted.length },
      summary,
    }, { pretty, text });
  }
}

async function cmdSelect({ name, runtime, boot, wait, stateFile, pretty, text }) {
  const listJson = await simctlListFull();
  const devices = flattenDevices(listJson);
  const picked = pickBestDevice(devices, { nameSubstr: name, runtimeSubstr: runtime });

  if (!picked) {
    exitWithError("No simulator matched selection.", { name, runtime });
  }

  const state = loadState(stateFile);
  state.udid = picked.udid;
  state.name = picked.name;
  state.runtime = picked.runtimeName;
  state.updatedAt = new Date().toISOString();
  saveState(stateFile, state);

  const summary = [
    `Selected: ${picked.name} (${picked.runtimeName})`,
    `UDID: ${picked.udid}`,
    `State file: ${stateFile}`,
  ];

  if (toBool(boot, false)) {
    const res = await cmdBoot({ udid: picked.udid, wait: toBool(wait, true), pretty, text, stateFile, _internalCall: true });
    summary.push("Boot: " + (res.ok ? "ok" : "failed"));
  }

  emit({
    ok: true,
    selected: { name: picked.name, udid: picked.udid, runtime: picked.runtimeName, state: picked.state },
    stateFile,
    summary,
  }, { pretty, text });
}

async function waitForBooted(udid, timeoutMs = 120000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    const listJson = await simctlListFull();
    const devices = flattenDevices(listJson);
    const d = devices.find((x) => x.udid === udid);
    if (d && d.state === "Booted") return { ok: true, state: d.state };
    await new Promise((r) => setTimeout(r, 1000));
  }
  return { ok: false, error: "timeout waiting for Booted" };
}

async function cmdBoot({ udid, wait, timeout, stateFile, pretty, text, _internalCall = false }) {
  const resolvedUdid = await resolveUdid({ udid, stateFile });
  const allowNonZero = true; // boot on already booted sometimes returns non-zero

  let bootCmd = { ok: true, stdout: "", stderr: "" };
  try {
    bootCmd = await run("xcrun", ["simctl", "boot", resolvedUdid], { allowNonZero });
  } catch (e) {
    bootCmd = { ok: false, stdout: e?.stdout || "", stderr: e?.stderr || "", error: e?.message || String(e) };
  }

  let waited = { ok: true };
  if (toBool(wait, true)) {
    const timeoutMs = Math.max(1000, (toNumber(timeout, 120) ?? 120) * 1000);
    waited = await waitForBooted(resolvedUdid, timeoutMs);
  }

  const ok = bootCmd.ok !== false && waited.ok;

  const summary = [
    `Boot: ${ok ? "ok" : "failed"}`,
    `UDID: ${resolvedUdid}`,
    ...(waited.ok ? ["State: Booted"] : [`Wait: ${waited.error || "failed"}`]),
  ];

  const result = { ok, udid: resolvedUdid, boot: bootCmd, wait: waited, summary };
  if (!_internalCall) emit(result, { pretty, text });
  return result;
}

async function cmdShutdown({ udid, all, stateFile, pretty, text }) {
  if (toBool(all, false)) {
    await run("xcrun", ["simctl", "shutdown", "all"], { allowNonZero: true });
    emit({ ok: true, summary: ["Shutdown: all"] }, { pretty, text });
    return;
  }
  const resolvedUdid = await resolveUdid({ udid, stateFile });
  await run("xcrun", ["simctl", "shutdown", resolvedUdid], { allowNonZero: true });
  emit({ ok: true, udid: resolvedUdid, summary: [`Shutdown: ${resolvedUdid}`] }, { pretty, text });
}

async function cmdErase({ udid, all, yes, stateFile, pretty, text }) {
  if (!toBool(yes, false)) exitWithError("Refusing to erase without --yes", { dangerous: true });
  if (toBool(all, false)) {
    await run("xcrun", ["simctl", "erase", "all"], { allowNonZero: true });
    emit({ ok: true, summary: ["Erase: all"] }, { pretty, text });
    return;
  }
  const resolvedUdid = await resolveUdid({ udid, stateFile });
  await run("xcrun", ["simctl", "erase", resolvedUdid], { allowNonZero: true });
  emit({ ok: true, udid: resolvedUdid, summary: [`Erase: ${resolvedUdid}`] }, { pretty, text });
}

async function cmdDelete({ udid, yes, stateFile, pretty, text }) {
  if (!toBool(yes, false)) exitWithError("Refusing to delete without --yes", { dangerous: true });
  const resolvedUdid = await resolveUdid({ udid, stateFile });
  await run("xcrun", ["simctl", "delete", resolvedUdid], { allowNonZero: true });
  emit({ ok: true, udid: resolvedUdid, summary: [`Delete: ${resolvedUdid}`] }, { pretty, text });
}

async function cmdCreate({ name, deviceType, runtime, stateFile, pretty, text }) {
  if (!name || typeof name !== "string") exitWithError("Missing --name");
  if (!deviceType || typeof deviceType !== "string") exitWithError("Missing --device-type");
  if (!runtime || typeof runtime !== "string") exitWithError("Missing --runtime");

  const listJson = await simctlListFull();
  const devicetypes = Array.isArray(listJson?.devicetypes) ? listJson.devicetypes : [];
  const runtimes = Array.isArray(listJson?.runtimes) ? listJson.runtimes : [];

  const dtQ = normalise(deviceType);
  const rtQ = normalise(runtime);

  const dtMatches = devicetypes
    .filter((d) => d?.identifier && d?.name)
    .filter((d) => normalise(d.name).includes(dtQ) || normalise(d.identifier).includes(dtQ));

  if (!dtMatches.length) exitWithError("No device type matched --device-type", { deviceType });

  // Prefer exact-ish match and common iPhone types
  dtMatches.sort((a, b) => String(a.name).localeCompare(String(b.name)));
  const dt = dtMatches[0];

  const rtMatches = runtimes
    .filter((r) => r?.identifier && r?.name && r?.isAvailable !== false)
    .filter((r) => normalise(r.name).includes(rtQ) || normalise(r.identifier).includes(rtQ));

  if (!rtMatches.length) exitWithError("No runtime matched --runtime", { runtime });

  rtMatches.sort((a, b) => -cmpVersions(a.version, b.version));
  const rt = rtMatches[0];

  const { stdout } = await run("xcrun", ["simctl", "create", name, dt.identifier, rt.identifier]);
  const createdUdid = stdout.trim();

  const state = loadState(stateFile);
  state.udid = createdUdid;
  state.name = name;
  state.runtime = rt.name;
  state.updatedAt = new Date().toISOString();
  saveState(stateFile, state);

  emit({
    ok: true,
    created: { udid: createdUdid, name, deviceType: dt.name, runtime: rt.name },
    stateFile,
    summary: [`Created: ${name}`, `UDID: ${createdUdid}`],
  }, { pretty, text });
}

async function cmdScreenshot({ udid, out, stateFile, pretty, text }) {
  if (!out || typeof out !== "string") exitWithError("Missing --out <file.png>");
  const resolvedUdid = await resolveUdid({ udid, stateFile });
  const outPath = path.resolve(out);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });

  await run("xcrun", ["simctl", "io", resolvedUdid, "screenshot", outPath]);
  emit({ ok: true, udid: resolvedUdid, out: outPath, summary: [`Screenshot: ${outPath}`] }, { pretty, text });
}

async function cmdRecordVideo({ udid, out, stateFile }) {
  if (!out || typeof out !== "string") exitWithError("Missing --out <file.mp4>");
  const resolvedUdid = await resolveUdid({ udid, stateFile });
  const outPath = path.resolve(out);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });

  // This is intentionally a foreground process. Stop with Ctrl+C.
  const child = spawn("xcrun", ["simctl", "io", resolvedUdid, "recordVideo", outPath], {
    stdio: "inherit",
    shell: false,
  });
  child.on("exit", (code) => process.exit(code ?? 0));
}

async function cmdOpenUrl({ udid, url, stateFile, pretty, text }) {
  if (!url || typeof url !== "string") exitWithError("Missing --url");
  const resolvedUdid = await resolveUdid({ udid, stateFile });
  await run("xcrun", ["simctl", "openurl", resolvedUdid, url]);
  emit({ ok: true, udid: resolvedUdid, url, summary: [`Open URL: ${url}`] }, { pretty, text });
}

async function cmdClipboardGet({ udid, stateFile, pretty, text }) {
  const resolvedUdid = await resolveUdid({ udid, stateFile });
  const { stdout } = await run("xcrun", ["simctl", "pbpaste", resolvedUdid], { allowNonZero: true });
  emit({ ok: true, udid: resolvedUdid, text: stdout, summary: ["Clipboard read"] }, { pretty, text });
}

async function cmdClipboardSet({ udid, text: clipText, stateFile, pretty, text }) {
  if (clipText === undefined) exitWithError("Missing --text");
  const resolvedUdid = await resolveUdid({ udid, stateFile });
  await run("xcrun", ["simctl", "pbcopy", resolvedUdid], { stdin: String(clipText) });
  emit({ ok: true, udid: resolvedUdid, summary: ["Clipboard set"] }, { pretty, text });
}

async function cmdAppInstall({ udid, app, stateFile, pretty, text }) {
  if (!app || typeof app !== "string") exitWithError("Missing --app <path/to/App.app>");
  const resolvedUdid = await resolveUdid({ udid, stateFile });
  const appPath = path.resolve(app);
  if (!fs.existsSync(appPath)) exitWithError("App path does not exist", { app: appPath });

  await run("xcrun", ["simctl", "install", resolvedUdid, appPath]);
  emit({ ok: true, udid: resolvedUdid, app: appPath, summary: [`Installed: ${path.basename(appPath)}`] }, { pretty, text });
}

async function cmdAppUninstall({ udid, bundleId, stateFile, pretty, text }) {
  if (!bundleId || typeof bundleId !== "string") exitWithError("Missing --bundle-id");
  if (!looksLikeBundleId(bundleId)) exitWithError("Invalid --bundle-id", { bundleId });
  const resolvedUdid = await resolveUdid({ udid, stateFile });

  await run("xcrun", ["simctl", "uninstall", resolvedUdid, bundleId], { allowNonZero: true });
  emit({ ok: true, udid: resolvedUdid, bundleId, summary: [`Uninstalled: ${bundleId}`] }, { pretty, text });
}

async function cmdAppLaunch({ udid, bundleId, passthroughArgs, stateFile, pretty, text }) {
  if (!bundleId || typeof bundleId !== "string") exitWithError("Missing --bundle-id");
  if (!looksLikeBundleId(bundleId)) exitWithError("Invalid --bundle-id", { bundleId });
  const resolvedUdid = await resolveUdid({ udid, stateFile });

  const args = ["simctl", "launch", resolvedUdid, bundleId, ...passthroughArgs];
  const { stdout, stderr, code } = await run("xcrun", args, { allowNonZero: true });
  emit({
    ok: code === 0,
    udid: resolvedUdid,
    bundleId,
    pid: stdout.trim() || null,
    stderr: stderr.trim() || null,
    summary: [`Launch: ${bundleId}`, stdout.trim() ? `PID: ${stdout.trim()}` : "No PID returned"],
  }, { pretty, text });
}

async function cmdAppTerminate({ udid, bundleId, stateFile, pretty, text }) {
  if (!bundleId || typeof bundleId !== "string") exitWithError("Missing --bundle-id");
  if (!looksLikeBundleId(bundleId)) exitWithError("Invalid --bundle-id", { bundleId });
  const resolvedUdid = await resolveUdid({ udid, stateFile });

  await run("xcrun", ["simctl", "terminate", resolvedUdid, bundleId], { allowNonZero: true });
  emit({ ok: true, udid: resolvedUdid, bundleId, summary: [`Terminate: ${bundleId}`] }, { pretty, text });
}

async function cmdAppContainer({ udid, bundleId, type, stateFile, pretty, text }) {
  if (!bundleId || typeof bundleId !== "string") exitWithError("Missing --bundle-id");
  if (!looksLikeBundleId(bundleId)) exitWithError("Invalid --bundle-id", { bundleId });

  const resolvedUdid = await resolveUdid({ udid, stateFile });
  const t = type ? String(type) : "data";
  if (!["data", "app"].includes(t)) exitWithError("Invalid --type (expected data|app)", { type });

  const { stdout } = await run("xcrun", ["simctl", "get_app_container", resolvedUdid, bundleId, t]);
  const containerPath = stdout.trim();
  emit({ ok: true, udid: resolvedUdid, bundleId, type: t, path: containerPath }, { pretty, text });
}

async function cmdPrivacy({ udid, action, bundleId, service, stateFile, pretty, text }) {
  if (!action) exitWithError("Missing privacy subcommand (grant|revoke|reset)");
  if (!bundleId || typeof bundleId !== "string") exitWithError("Missing --bundle-id");
  if (!looksLikeBundleId(bundleId)) exitWithError("Invalid --bundle-id", { bundleId });
  if (!service || typeof service !== "string") exitWithError("Missing --service <svc[,svc...]>");

  const resolvedUdid = await resolveUdid({ udid, stateFile });
  const svcs = service.split(",").map((s) => s.trim()).filter(Boolean);
  if (!svcs.length) exitWithError("No services parsed from --service", { service });

  const results = [];
  for (const svc of svcs) {
    await run("xcrun", ["simctl", "privacy", resolvedUdid, action, svc, bundleId], { allowNonZero: true });
    results.push({ service: svc, action, ok: true });
  }

  emit({ ok: true, udid: resolvedUdid, bundleId, action, services: svcs, results }, { pretty, text });
}

async function cmdPush({ udid, bundleId, payload, stateFile, pretty, text }) {
  if (!bundleId || typeof bundleId !== "string") exitWithError("Missing --bundle-id");
  if (!looksLikeBundleId(bundleId)) exitWithError("Invalid --bundle-id", { bundleId });
  if (!payload || typeof payload !== "string") exitWithError("Missing --payload <json-string>");

  const resolvedUdid = await resolveUdid({ udid, stateFile });

  // Validate JSON
  let payloadObj;
  try {
    payloadObj = JSON.parse(payload);
  } catch {
    exitWithError("--payload is not valid JSON", { payload });
  }
  if (typeof payloadObj !== "object" || payloadObj === null) exitWithError("--payload must be a JSON object", { payload });

  const tmpPath = path.join(os.tmpdir(), `sim-push-${nowIsoCompact()}.apns.json`);
  fs.writeFileSync(tmpPath, JSON.stringify(payloadObj), "utf8");

  await run("xcrun", ["simctl", "push", resolvedUdid, bundleId, tmpPath], { allowNonZero: true });

  emit({ ok: true, udid: resolvedUdid, bundleId, tmp: tmpPath, summary: ["Push sent"] }, { pretty, text });
}

async function cmdLogsShow({ udid, last, predicate, stateFile, pretty, text }) {
  const resolvedUdid = await resolveUdid({ udid, stateFile });
  const args = ["simctl", "spawn", resolvedUdid, "log", "show", "--style", "syslog", "--last", String(last || "5m")];
  if (predicate) {
    args.push("--predicate", String(predicate));
  }
  const { stdout, stderr, code } = await run("xcrun", args, { allowNonZero: true });
  emit({ ok: code === 0, udid: resolvedUdid, last: String(last || "5m"), predicate: predicate || null, stdout, stderr }, { pretty, text });
}

// ---- idb-backed UI automation ----

function ensureIdb() {
  const p = whichSync("idb");
  if (!p) {
    exitWithError("idb not found. Install for UI automation: `brew install idb-companion` + `python3 -m pip install fb-idb`", { missing: "idb" });
  }
  return p;
}

async function idbDescribeAll({ udid }) {
  ensureIdb();
  const resolvedUdid = udid;
  // idb ui describe-all already prints JSON array
  const { json } = await runJson("idb", ["ui", "describe-all", "--udid", resolvedUdid, "--json"], { allowNonZero: true });
  // Some idb versions print to stdout even without --json; keep tolerant.
  if (!Array.isArray(json)) {
    // If json parsing failed above, we'd have thrown. If it parsed but isn't array, we still accept.
    return Array.isArray(json) ? json : [];
  }
  return json;
}

function elementLabel(el) {
  const parts = [
    el?.AXLabel,
    el?.title,
    el?.AXValue,
    el?.role_description,
    el?.type,
  ].filter((x) => typeof x === "string" && x.trim().length);
  return parts[0] || "";
}

function isInteractive(el) {
  if (!el || el.enabled === false) return false;
  const t = normalise(el.type);
  const role = normalise(el.role_description || el.role);
  const label = elementLabel(el);
  if (!label) return false;

  const interactiveTypes = [
    "button",
    "text field",
    "secure text field",
    "search field",
    "switch",
    "slider",
    "link",
    "cell",
    "tab bar button",
    "checkbox",
    "radio button",
  ];

  const typeHints = [
    "button",
    "textfield",
    "securetextfield",
    "searchfield",
    "switch",
    "slider",
    "link",
    "cell",
    "tabbarbutton",
    "checkbox",
    "radiobutton",
  ];

  return interactiveTypes.some((x) => role.includes(x)) || typeHints.some((x) => t.includes(x));
}

function scoreMatch(query, candidate) {
  const q = normalise(query);
  const c = normalise(candidate);
  if (!q || !c) return 0;
  if (q === c) return 100;
  if (c.startsWith(q)) return 90;
  if (c.includes(q)) return 80;
  if (q.includes(c)) return 60;
  // cheap token overlap
  const qt = new Set(q.split(" ").filter(Boolean));
  const ct = new Set(c.split(" ").filter(Boolean));
  let inter = 0;
  for (const t of qt) if (ct.has(t)) inter++;
  const score = Math.round((inter / Math.max(1, qt.size)) * 50);
  return score; // 0..50
}

function centreOfFrame(frame) {
  const x = toNumber(frame?.x, null);
  const y = toNumber(frame?.y, null);
  const w = toNumber(frame?.width, null);
  const h = toNumber(frame?.height, null);
  if (x === null || y === null || w === null || h === null) return null;
  return { x: x + w / 2, y: y + h / 2 };
}

function summariseUi(elements, limit = 12) {
  const total = elements.length;
  const interactive = elements.filter(isInteractive);
  const countsByType = {};
  const top = [];

  for (const el of interactive) {
    const t = String(el?.type || el?.role_description || "unknown");
    countsByType[t] = (countsByType[t] || 0) + 1;
  }

  // pick top by type then label
  for (const el of interactive) {
    const label = elementLabel(el);
    if (!label) continue;
    top.push({ type: el.type || el.role_description || "unknown", label });
    if (top.length >= limit) break;
  }

  const summary = [
    `UI elements: ${total}`,
    `Interactive: ${interactive.length}`,
    ...top.map((x) => `- ${x.type}: ${x.label}`),
  ];

  return { total, interactiveCount: interactive.length, countsByType, top, summary };
}

async function cmdUiSummary({ udid, limit, stateFile, pretty, text }) {
  const resolvedUdid = await resolveUdid({ udid, stateFile });
  const elements = await idbDescribeAll({ udid: resolvedUdid });
  const lim = Math.max(1, Math.min(200, Number(limit || 12)));
  const s = summariseUi(elements, lim);
  emit({ ok: true, udid: resolvedUdid, ...s }, { pretty, text });
}

async function cmdUiTree({ udid, stateFile, pretty }) {
  const resolvedUdid = await resolveUdid({ udid, stateFile });
  const elements = await idbDescribeAll({ udid: resolvedUdid });
  emit({ ok: true, udid: resolvedUdid, elements }, { pretty, text: false });
}

async function cmdUiFind({ udid, query, limit, stateFile, pretty, text }) {
  if (!query || typeof query !== "string") exitWithError("Missing --query");
  const resolvedUdid = await resolveUdid({ udid, stateFile });
  const elements = await idbDescribeAll({ udid: resolvedUdid });

  const matches = [];
  for (const el of elements) {
    if (!isInteractive(el)) continue;
    const label = elementLabel(el);
    const score = Math.max(
      scoreMatch(query, label),
      scoreMatch(query, el?.AXLabel),
      scoreMatch(query, el?.title),
      scoreMatch(query, el?.AXValue),
    );
    if (score <= 0) continue;
    matches.push({
      score,
      label,
      type: el?.type || el?.role_description || "unknown",
      frame: el?.frame || null,
      centre: centreOfFrame(el?.frame) || null,
    });
  }

  matches.sort((a, b) => b.score - a.score);
  const lim = Math.max(1, Math.min(200, Number(limit || 20)));
  const trimmed = matches.slice(0, lim);

  const summary = [
    `Matches: ${matches.length}`,
    ...trimmed.slice(0, Math.min(10, trimmed.length)).map((m) => `${m.score} — ${m.type}: ${m.label}`),
  ];

  emit({ ok: true, udid: resolvedUdid, query, matches: trimmed, summary }, { pretty, text });
}

async function cmdUiTap({ udid, query, x, y, stateFile, pretty, text }) {
  const resolvedUdid = await resolveUdid({ udid, stateFile });
  ensureIdb();

  let tapPoint = null;
  let target = null;

  if (x !== undefined && y !== undefined) {
    const px = toNumber(x);
    const py = toNumber(y);
    if (px === undefined || py === undefined) exitWithError("Invalid --x/--y (expected numbers)", { x, y });
    tapPoint = { x: px, y: py };
    target = { kind: "coordinate", x: px, y: py };
  } else {
    if (!query || typeof query !== "string") exitWithError("Missing --query (or provide --x and --y)");
    const elements = await idbDescribeAll({ udid: resolvedUdid });
    let best = null;
    let bestScore = 0;

    for (const el of elements) {
      if (!isInteractive(el)) continue;
      const label = elementLabel(el);
      const score = Math.max(
        scoreMatch(query, label),
        scoreMatch(query, el?.AXLabel),
        scoreMatch(query, el?.title),
        scoreMatch(query, el?.AXValue),
      );
      if (score > bestScore) {
        const centre = centreOfFrame(el?.frame);
        if (!centre) continue;
        bestScore = score;
        best = { score, label, type: el?.type || el?.role_description || "unknown", centre };
      }
    }

    if (!best || bestScore < 50) {
      exitWithError("No sufficiently confident UI match for --query. Try `ui summary` or `ui tree`.", { query, bestScore });
    }

    tapPoint = best.centre;
    target = best;
  }

  await run("idb", ["ui", "tap", String(tapPoint.x), String(tapPoint.y), "--udid", resolvedUdid, "--json"], { allowNonZero: true });

  emit({
    ok: true,
    udid: resolvedUdid,
    tapped: target,
    summary: [`Tap: ${target.kind === "coordinate" ? `${target.x},${target.y}` : target.label}`],
  }, { pretty, text });
}

async function cmdUiType({ udid, text: inputText, stateFile, pretty, text }) {
  if (inputText === undefined) exitWithError("Missing --text");
  const resolvedUdid = await resolveUdid({ udid, stateFile });
  ensureIdb();

  await run("idb", ["text", String(inputText), "--udid", resolvedUdid, "--json"], { allowNonZero: true });
  emit({ ok: true, udid: resolvedUdid, summary: ["Typed text"] }, { pretty, text });
}

async function cmdUiButton({ udid, name, stateFile, pretty, text }) {
  if (!name || typeof name !== "string") exitWithError("Missing --name HOME|LOCK|SIRI|SIDE_BUTTON|APPLE_PAY");
  const resolvedUdid = await resolveUdid({ udid, stateFile });
  ensureIdb();

  const n = String(name).toUpperCase();
  await run("idb", ["ui", "button", n, "--udid", resolvedUdid, "--json"], { allowNonZero: true });
  emit({ ok: true, udid: resolvedUdid, button: n, summary: [`Button: ${n}`] }, { pretty, text });
}

// ---- help ----

function help() {
  const msg = `
Usage:
  node ios-sim.mjs <command> [subcommand] [flags] [-- passthrough...]

Global flags:
  --state-file <path>   (default: ./.ios-sim-state.json or IOS_SIM_STATE_FILE)
  --pretty              pretty-print JSON
  --text                output short text summary (if provided)
  --help

Commands:
  health
  list [--full]
  select --name <substr> [--runtime <substr>] [--boot] [--wait]
  boot [--udid <uuid>] [--wait] [--timeout <sec>]
  shutdown [--udid <uuid>|--all]
  erase --yes [--udid <uuid>|--all]
  delete --yes [--udid <uuid>]
  create --name <name> --device-type <substr> --runtime <substr>

  app install --app <path/to/App.app> [--udid <uuid>]
  app uninstall --bundle-id <id> [--udid <uuid>]
  app launch --bundle-id <id> [--udid <uuid>] [-- <args...>]
  app terminate --bundle-id <id> [--udid <uuid>]
  app container --bundle-id <id> [--type data|app] [--udid <uuid>]

  screenshot --out <file.png> [--udid <uuid>]
  record-video --out <file.mp4> [--udid <uuid>]
  openurl --url <url> [--udid <uuid>]
  clipboard get [--udid <uuid>]
  clipboard set --text <text> [--udid <uuid>]
  privacy grant|revoke|reset --bundle-id <id> --service <svc[,svc...]> [--udid <uuid>]
  push --bundle-id <id> --payload <json> [--udid <uuid>]
  logs show [--last 5m] [--predicate <expr>] [--udid <uuid>]

  ui summary [--limit 12] [--udid <uuid>]
  ui tree [--udid <uuid>]
  ui find --query <text> [--limit 20] [--udid <uuid>]
  ui tap --query <text> [--udid <uuid>]
  ui tap --x <num> --y <num> [--udid <uuid>]
  ui type --text <text> [--udid <uuid>]
  ui button --name HOME|LOCK|SIRI|SIDE_BUTTON|APPLE_PAY [--udid <uuid>]

Examples:
  node ios-sim.mjs health --text
  node ios-sim.mjs list
  node ios-sim.mjs select --name "iPhone 15" --runtime "iOS" --boot
  node ios-sim.mjs app install --app ./DerivedData/.../MyApp.app
  node ios-sim.mjs ui tap --query "Log in"
`.trim();
  process.stdout.write(msg + "\n");
}

async function main() {
  const argv = process.argv.slice(2);
  const parsed = parseArgv(argv);
  const flags = parsed.flags;

  const pretty = toBool(flags.pretty, false);
  const text = toBool(flags.text, false);
  const stateFile = typeof flags["state-file"] === "string" ? String(flags["state-file"]) : STATE_FILE_DEFAULT;

  const [cmd, subcmd, ...restPos] = parsed._;

  if (toBool(flags.help, false) || !cmd) {
    help();
    process.exit(0);
  }

  // Most commands require macOS+xcrun (but we still provide helpful errors).
  if (!isMacOS() && cmd !== "help") {
    // Still allow help.
    exitWithError("This tool must run on macOS (Simulator host). Use a macOS node/gateway.", { platform: process.platform });
  }
  if (!whichSync("xcrun")) {
    exitWithError("xcrun not found. Install Xcode Command Line Tools / Xcode.", {});
  }

  switch (cmd) {
    case "health":
      await cmdHealth({ pretty, text });
      return;

    case "list":
      await cmdList({ full: toBool(flags.full, false), pretty, text });
      return;

    case "select":
      await cmdSelect({
        name: flags.name,
        runtime: flags.runtime,
        boot: flags.boot,
        wait: flags.wait,
        stateFile,
        pretty,
        text,
      });
      return;

    case "boot":
      await cmdBoot({ udid: flags.udid, wait: flags.wait, timeout: flags.timeout, stateFile, pretty, text });
      return;

    case "shutdown":
      await cmdShutdown({ udid: flags.udid, all: flags.all, stateFile, pretty, text });
      return;

    case "erase":
      await cmdErase({ udid: flags.udid, all: flags.all, yes: flags.yes, stateFile, pretty, text });
      return;

    case "delete":
      await cmdDelete({ udid: flags.udid, yes: flags.yes, stateFile, pretty, text });
      return;

    case "create":
      await cmdCreate({ name: flags.name, deviceType: flags["device-type"], runtime: flags.runtime, stateFile, pretty, text });
      return;

    case "screenshot":
      await cmdScreenshot({ udid: flags.udid, out: flags.out, stateFile, pretty, text });
      return;

    case "record-video":
      await cmdRecordVideo({ udid: flags.udid, out: flags.out, stateFile });
      return;

    case "openurl":
      await cmdOpenUrl({ udid: flags.udid, url: flags.url, stateFile, pretty, text });
      return;

    case "clipboard":
      if (!subcmd) exitWithError("clipboard requires subcommand: get|set");
      if (subcmd === "get") await cmdClipboardGet({ udid: flags.udid, stateFile, pretty, text });
      else if (subcmd === "set") await cmdClipboardSet({ udid: flags.udid, text: flags.text ?? flags.value, stateFile, pretty, text });
      else exitWithError("Unknown clipboard subcommand", { subcmd });
      return;

    case "app":
      if (!subcmd) exitWithError("app requires subcommand: install|uninstall|launch|terminate|container");
      if (subcmd === "install") await cmdAppInstall({ udid: flags.udid, app: flags.app, stateFile, pretty, text });
      else if (subcmd === "uninstall") await cmdAppUninstall({ udid: flags.udid, bundleId: flags["bundle-id"], stateFile, pretty, text });
      else if (subcmd === "launch") await cmdAppLaunch({ udid: flags.udid, bundleId: flags["bundle-id"], passthroughArgs: parsed.passthrough, stateFile, pretty, text });
      else if (subcmd === "terminate") await cmdAppTerminate({ udid: flags.udid, bundleId: flags["bundle-id"], stateFile, pretty, text });
      else if (subcmd === "container") await cmdAppContainer({ udid: flags.udid, bundleId: flags["bundle-id"], type: flags.type, stateFile, pretty, text });
      else exitWithError("Unknown app subcommand", { subcmd });
      return;

    case "privacy": {
      const action = subcmd;
      await cmdPrivacy({
        udid: flags.udid,
        action,
        bundleId: flags["bundle-id"],
        service: flags.service,
        stateFile,
        pretty,
        text,
      });
      return;
    }

    case "push":
      await cmdPush({ udid: flags.udid, bundleId: flags["bundle-id"], payload: flags.payload, stateFile, pretty, text });
      return;

    case "logs":
      if (!subcmd) exitWithError("logs requires subcommand: show");
      if (subcmd === "show") await cmdLogsShow({ udid: flags.udid, last: flags.last, predicate: flags.predicate, stateFile, pretty, text });
      else exitWithError("Unknown logs subcommand", { subcmd });
      return;

    case "ui":
      if (!subcmd) exitWithError("ui requires subcommand: summary|tree|find|tap|type|button");
      if (subcmd === "summary") await cmdUiSummary({ udid: flags.udid, limit: flags.limit, stateFile, pretty, text });
      else if (subcmd === "tree") await cmdUiTree({ udid: flags.udid, stateFile, pretty });
      else if (subcmd === "find") await cmdUiFind({ udid: flags.udid, query: flags.query, limit: flags.limit, stateFile, pretty, text });
      else if (subcmd === "tap") await cmdUiTap({ udid: flags.udid, query: flags.query, x: flags.x, y: flags.y, stateFile, pretty, text });
      else if (subcmd === "type") await cmdUiType({ udid: flags.udid, text: flags.text, stateFile, pretty, text });
      else if (subcmd === "button") await cmdUiButton({ udid: flags.udid, name: flags.name, stateFile, pretty, text });
      else exitWithError("Unknown ui subcommand", { subcmd });
      return;

    default:
      exitWithError("Unknown command. Run with --help.", { cmd });
  }
}

main().catch((e) => {
  exitWithError(e?.message || String(e), { stderr: e?.stderr, stdout: e?.stdout });
});
