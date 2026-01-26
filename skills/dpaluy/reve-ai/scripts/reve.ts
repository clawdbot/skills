#!/usr/bin/env bun
/**
 * Reve AI Image Generation CLI
 * https://api.reve.com/console/docs
 */

import { parseArgs } from "util";
import { readFileSync, writeFileSync } from "fs";

const API_BASE = "https://api.reve.com";
const VALID_ASPECTS = ["16:9", "9:16", "3:2", "2:3", "4:3", "3:4", "1:1"];

function getApiKey(): string {
  const key = process.env.REVE_API_KEY || process.env.REVE_AI_API_KEY;
  if (!key) {
    console.error("Error: REVE_API_KEY or REVE_AI_API_KEY environment variable not set");
    process.exit(1);
  }
  return key;
}

async function apiRequest(endpoint: string, body: Record<string, unknown>): Promise<any> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${getApiKey()}`,
      "Content-Type": "application/json",
      "Accept": "application/json",
    },
    body: JSON.stringify(body),
  });

  const data = await response.json();

  if (!response.ok) {
    const msg = data.message || data.error || `HTTP ${response.status}`;
    console.error(`API Error: ${msg}`);
    if (response.status === 429 && response.headers.get("retry-after")) {
      console.error(`Retry after: ${response.headers.get("retry-after")} seconds`);
    }
    process.exit(1);
  }

  return data;
}

function loadImageBase64(path: string): string {
  try {
    const buffer = readFileSync(path);
    return buffer.toString("base64");
  } catch (e) {
    console.error(`Error: Cannot read file: ${path}`);
    process.exit(1);
  }
}

function saveImage(base64: string, outputPath: string): void {
  const buffer = Buffer.from(base64, "base64");
  writeFileSync(outputPath, buffer);
}

function printResult(result: any, outputPath: string): void {
  console.log(JSON.stringify({
    output: outputPath,
    version: result.version,
    credits_used: result.credits_used,
    credits_remaining: result.credits_remaining,
    content_violation: result.content_violation || false,
  }, null, 2));
}

async function createImage(args: string[]): Promise<void> {
  const { values, positionals } = parseArgs({
    args,
    options: {
      output: { type: "string", short: "o", default: "output.png" },
      aspect: { type: "string", default: undefined },
      version: { type: "string", default: undefined },
      help: { type: "boolean", short: "h", default: false },
    },
    allowPositionals: true,
  });

  if (values.help) {
    console.log(`Usage: reve.ts create PROMPT [options]
Options:
  -o, --output FILE    Output file path (default: output.png)
  --aspect RATIO       Aspect ratio: ${VALID_ASPECTS.join(", ")}
  --version VER        Model version (default: latest)`);
    return;
  }

  const prompt = positionals.join(" ");
  if (!prompt) {
    console.error("Error: Prompt required");
    process.exit(1);
  }

  const body: Record<string, unknown> = { prompt };
  if (values.aspect) {
    if (!VALID_ASPECTS.includes(values.aspect)) {
      console.error(`Error: Invalid aspect ratio. Valid: ${VALID_ASPECTS.join(", ")}`);
      process.exit(1);
    }
    body.aspect_ratio = values.aspect;
  }
  if (values.version) body.version = values.version;

  const result = await apiRequest("/v1/image/create", body);
  saveImage(result.image, values.output!);
  printResult(result, values.output!);
}

async function editImage(args: string[]): Promise<void> {
  const { values, positionals } = parseArgs({
    args,
    options: {
      input: { type: "string", short: "i" },
      output: { type: "string", short: "o", default: "output.png" },
      aspect: { type: "string", default: undefined },
      version: { type: "string", default: undefined },
      help: { type: "boolean", short: "h", default: false },
    },
    allowPositionals: true,
  });

  if (values.help) {
    console.log(`Usage: reve.ts edit INSTRUCTION [options]
Options:
  -i, --input FILE     Input image to edit (required)
  -o, --output FILE    Output file path (default: output.png)
  --aspect RATIO       Output aspect ratio
  --version VER        Model version (latest, latest-fast, reve-edit@20250915, reve-edit-fast@20251030)`);
    return;
  }

  if (!values.input) {
    console.error("Error: Input image required (-i FILE)");
    process.exit(1);
  }

  const instruction = positionals.join(" ");
  if (!instruction) {
    console.error("Error: Edit instruction required");
    process.exit(1);
  }

  const body: Record<string, unknown> = {
    edit_instruction: instruction,
    reference_image: loadImageBase64(values.input),
  };
  if (values.aspect) body.aspect_ratio = values.aspect;
  if (values.version) body.version = values.version;

  const result = await apiRequest("/v1/image/edit", body);
  saveImage(result.image, values.output!);
  printResult(result, values.output!);
}

async function remixImages(args: string[]): Promise<void> {
  const { values, positionals } = parseArgs({
    args,
    options: {
      input: { type: "string", short: "i", multiple: true, default: [] },
      output: { type: "string", short: "o", default: "output.png" },
      aspect: { type: "string", default: undefined },
      version: { type: "string", default: undefined },
      help: { type: "boolean", short: "h", default: false },
    },
    allowPositionals: true,
  });

  if (values.help) {
    console.log(`Usage: reve.ts remix PROMPT [options]
Options:
  -i, --input FILE     Reference image (can specify multiple, up to 6)
  -o, --output FILE    Output file path (default: output.png)
  --aspect RATIO       Output aspect ratio
  --version VER        Model version (latest, latest-fast, reve-remix@20250915, reve-remix-fast@20251030)

Use <img>N</img> in prompt to reference images by index (0-based)`);
    return;
  }

  const inputs = values.input as string[];
  if (inputs.length === 0) {
    console.error("Error: At least one reference image required (-i FILE)");
    process.exit(1);
  }
  if (inputs.length > 6) {
    console.error("Error: Maximum 6 reference images allowed");
    process.exit(1);
  }

  const prompt = positionals.join(" ");
  if (!prompt) {
    console.error("Error: Prompt required");
    process.exit(1);
  }

  const body: Record<string, unknown> = {
    prompt,
    reference_images: inputs.map(loadImageBase64),
  };
  if (values.aspect) body.aspect_ratio = values.aspect;
  if (values.version) body.version = values.version;

  const result = await apiRequest("/v1/image/remix", body);
  saveImage(result.image, values.output!);
  printResult(result, values.output!);
}

function printHelp(): void {
  console.log(`Reve AI Image Generation CLI

Usage: reve.ts COMMAND [options]

Commands:
  create PROMPT     Generate image from text prompt
  edit INSTRUCTION  Edit existing image with instructions
  remix PROMPT      Combine reference images with prompt

Use 'reve.ts COMMAND --help' for command-specific options.

Environment:
  REVE_API_KEY or REVE_AI_API_KEY must be set.`);
}

// Main
const [command, ...rest] = process.argv.slice(2);

switch (command) {
  case "create":
    await createImage(rest);
    break;
  case "edit":
    await editImage(rest);
    break;
  case "remix":
    await remixImages(rest);
    break;
  case "-h":
  case "--help":
  case undefined:
    printHelp();
    break;
  default:
    console.error(`Unknown command: ${command}`);
    console.error("Use --help for usage information");
    process.exit(1);
}
