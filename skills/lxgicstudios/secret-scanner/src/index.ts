import OpenAI from "openai";
import * as fs from "fs";
import { glob } from "glob";
import * as path from "path";

const openai = new OpenAI();

export interface SecretFinding {
  file: string;
  line: number;
  type: string;
  severity: string;
  snippet: string;
}

const PATTERNS = [
  { name: "AWS Key", regex: /AKIA[0-9A-Z]{16}/ },
  { name: "Generic Secret", regex: /(api[_-]?key|secret|token|password|credential)\s*[:=]\s*['"][^'"]{8,}['"]/gi },
  { name: "Private Key", regex: /-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----/ },
  { name: "GitHub Token", regex: /gh[pousr]_[A-Za-z0-9_]{36,}/ },
  { name: "Slack Token", regex: /xox[baprs]-[0-9a-zA-Z-]+/ },
  { name: "JWT", regex: /eyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+/ },
];

export async function scanFile(filePath: string): Promise<SecretFinding[]> {
  const content = fs.readFileSync(filePath, "utf-8");
  const lines = content.split("\n");
  const findings: SecretFinding[] = [];

  lines.forEach((line, i) => {
    for (const p of PATTERNS) {
      if (p.regex.test(line)) {
        findings.push({ file: filePath, line: i + 1, type: p.name, severity: "high", snippet: line.trim().substring(0, 100) });
      }
      p.regex.lastIndex = 0;
    }
  });

  return findings;
}

export async function scanDirectory(dir: string): Promise<SecretFinding[]> {
  const files = await glob("**/*.{js,ts,jsx,tsx,py,rb,go,java,env,json,yml,yaml,toml,cfg,conf,ini}", {
    cwd: dir, absolute: true, ignore: ["**/node_modules/**", "**/dist/**", "**/.git/**"]
  });
  const all: SecretFinding[] = [];
  for (const f of files) {
    try {
      const findings = await scanFile(f);
      all.push(...findings);
    } catch {}
  }
  return all;
}

export async function aiAnalyze(findings: SecretFinding[]): Promise<string> {
  if (findings.length === 0) return "No secrets found. Your code looks clean!";
  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      { role: "system", content: "You analyze potential secret leaks in code. For each finding, confirm if it's a real leak or false positive, rate severity, and suggest a fix. Be concise." },
      { role: "user", content: JSON.stringify(findings) }
    ],
    temperature: 0.2,
  });
  return response.choices[0].message.content || "";
}
