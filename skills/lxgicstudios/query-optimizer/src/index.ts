import OpenAI from "openai";
import * as fs from "fs";
import { glob } from "glob";

const openai = new OpenAI();

export async function scanQueryFiles(dir: string): Promise<string[]> {
  const files = await glob("**/*.{js,ts,sql,prisma}", {
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

export async function optimizeQueries(codeChunks: string[]): Promise<string> {
  const combined = codeChunks.join("\n\n").substring(0, 60000);
  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      { role: "system", content: "You are a database performance expert. Analyze SQL queries and Prisma/ORM code for performance issues: N+1 queries, missing indexes, unnecessary joins, unoptimized WHERE clauses, missing pagination. Provide optimized versions with explanations. Be concise." },
      { role: "user", content: combined }
    ],
    temperature: 0.3,
  });
  return response.choices[0].message.content || "No optimization suggestions.";
}
