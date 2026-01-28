import OpenAI from "openai";
import * as fs from "fs";
import * as path from "path";

const openai = new OpenAI();

export async function generateNextConfig(dir: string): Promise<string> {
  let context = "";
  const pkgPath = path.join(dir, "package.json");
  if (fs.existsSync(pkgPath)) {
    context = fs.readFileSync(pkgPath, "utf-8");
  }
  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      { role: "system", content: `You generate next.config.js (or next.config.mjs) files with best practices. Include: image optimization config, security headers, redirects/rewrites patterns, webpack customizations, bundle analyzer setup, and performance optimizations. Add helpful comments. Output valid JavaScript.` },
      { role: "user", content: `Generate a Next.js config with best practices. ${context ? "Project context:\n" + context : ""}` }
    ],
    temperature: 0.4,
  });
  return response.choices[0].message.content || "";
}
