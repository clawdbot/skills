import OpenAI from "openai";
import { glob } from "glob";
import * as fs from "fs";
import * as path from "path";

const CONFIG_FILES = [
  "package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
  "Cargo.toml", "go.mod", "go.sum", "pyproject.toml", "setup.py",
  "requirements.txt", "Gemfile", "build.gradle", "pom.xml",
  "tsconfig.json", "next.config.js", "next.config.mjs", "nuxt.config.ts",
  "vite.config.ts", "webpack.config.js", "Makefile",
  ".env.example", "docker-compose.yml",
  "mix.exs", "Pipfile", "poetry.lock", "composer.json",
];

export async function scanProject(dir: string): Promise<{ files: string[]; contents: Record<string, string> }> {
  const found: string[] = [];
  const contents: Record<string, string> = {};

  for (const f of CONFIG_FILES) {
    const full = path.join(dir, f);
    if (fs.existsSync(full)) {
      found.push(f);
      const stat = fs.statSync(full);
      if (stat.size < 5000) {
        contents[f] = fs.readFileSync(full, "utf-8");
      }
    }
  }

  const srcFiles = await glob("**/*.{ts,js,py,go,rs,rb,java}", {
    cwd: dir, ignore: ["node_modules/**", "dist/**", ".next/**", "target/**"],
    nodir: true,
  });
  found.push(...srcFiles.slice(0, 20).map(f => `src:${f}`));

  return { files: found, contents };
}

export async function generateDockerfile(projectInfo: { files: string[]; contents: Record<string, string> }, optimize: boolean): Promise<string> {
  if (!process.env.OPENAI_API_KEY) {
    throw new Error("Missing OPENAI_API_KEY environment variable. Set it with: export OPENAI_API_KEY=sk-...");
  }

  const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

  const prompt = optimize
    ? "Generate an optimized multi-stage Dockerfile with minimal final image size. Use alpine base images where possible. Separate build and runtime stages. Include .dockerignore suggestions as comments at the top."
    : "Generate a clean, well-commented Dockerfile for this project.";

  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: `You are a Docker expert. ${prompt} Output ONLY the Dockerfile contents. No markdown code fences.`
      },
      {
        role: "user",
        content: `Project files: ${projectInfo.files.join(", ")}\n\nKey file contents:\n${Object.entries(projectInfo.contents).map(([k, v]) => `--- ${k} ---\n${v}`).join("\n\n")}`
      }
    ],
    temperature: 0.3,
  });

  return response.choices[0]?.message?.content?.trim() || "";
}
