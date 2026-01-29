import OpenAI from "openai";
import * as fs from "fs";
import * as path from "path";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export function scanProject(dir: string): string[] {
  const markers = [
    "package.json", "requirements.txt", "Gemfile", "go.mod", "Cargo.toml",
    "pom.xml", "build.gradle", "Dockerfile", ".env", "prisma/schema.prisma",
    "next.config.js", "next.config.mjs", "nuxt.config.ts", "vite.config.ts",
    "manage.py", "app.py", "main.go", "main.rs",
  ];
  const found: string[] = [];
  for (const m of markers) {
    if (fs.existsSync(path.join(dir, m))) found.push(m);
  }
  return found;
}

export async function generateCompose(files: string[], extra?: string): Promise<string> {
  const res = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: "You are a DevOps expert. Generate a production-ready docker-compose.yml based on the project files detected. Include proper networking, volumes, health checks, and environment variables. Return ONLY the YAML, no explanation.",
      },
      {
        role: "user",
        content: `Project files found: ${files.join(", ")}${extra ? `\nAdditional requirements: ${extra}` : ""}\n\nGenerate docker-compose.yml`,
      },
    ],
    temperature: 0.3,
  });
  return res.choices[0].message.content || "";
}
