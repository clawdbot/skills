import OpenAI from "openai";
import * as fs from "fs";
import { glob } from "glob";

const openai = new OpenAI();

export async function scanRoutes(dir: string): Promise<string[]> {
  const files = await glob("**/*.{js,ts,jsx,tsx}", {
    cwd: dir, absolute: true, ignore: ["**/node_modules/**", "**/dist/**", "**/.git/**"]
  });
  const contents: string[] = [];
  for (const f of files) {
    try {
      const content = fs.readFileSync(f, "utf-8");
      if (content.length > 0 && content.length < 50000) {
        contents.push(`// File: ${f}\n${content}`);
      }
    } catch {}
  }
  return contents;
}

export async function generateRBAC(routeCode: string[]): Promise<string> {
  const combined = routeCode.join("\n\n").substring(0, 60000);
  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      { role: "system", content: "You are a security architect. Analyze the route/endpoint code and generate a complete RBAC (Role-Based Access Control) configuration. Define roles (admin, user, moderator, etc.), permissions per route, and output a ready-to-use JSON config plus middleware code. Be concise and practical." },
      { role: "user", content: combined }
    ],
    temperature: 0.3,
  });
  return response.choices[0].message.content || "Could not generate RBAC config.";
}
