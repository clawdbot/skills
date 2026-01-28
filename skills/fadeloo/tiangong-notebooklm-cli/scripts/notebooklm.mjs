#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

function usage() {
  console.error("Usage: notebooklm.mjs <command> [args...]");
  console.error("Examples:");
  console.error("  notebooklm.mjs status");
  console.error("  notebooklm.mjs login");
  console.error("  notebooklm.mjs list");
  console.error("  notebooklm.mjs ask \"Summarize this notebook\" --notebook <id>");
  console.error("  notebooklm.mjs source add https://example.com --notebook <id>");
  console.error("  notebooklm.mjs artifact list --notebook <id> --json");
  process.exit(2);
}

function hasWorkspaceMarker(dir) {
  const pyproject = path.join(dir, "pyproject.toml");
  if (!fs.existsSync(pyproject)) return false;
  const content = fs.readFileSync(pyproject, "utf8");
  return content.includes("[tool.tiangong.workspace]");
}

function findRepoRoot(startDir) {
  let dir = startDir;
  while (true) {
    if (hasWorkspaceMarker(dir)) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return null;
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const envRoot = (process.env.TIANGONG_WORKSPACE_ROOT ?? "").trim();
const repoRoot = envRoot || findRepoRoot(scriptDir);

if (!repoRoot) {
  console.error("Could not locate repo root. Set TIANGONG_WORKSPACE_ROOT to the workspace path.");
  process.exit(1);
}

const result = spawnSync("uv", ["run", "tiangong-workspace", "notebooklm", ...args], {
  cwd: repoRoot,
  stdio: "inherit",
});

if (result.error) {
  console.error(`Failed to run uv: ${result.error.message}`);
  process.exit(1);
}

process.exit(result.status ?? 1);
