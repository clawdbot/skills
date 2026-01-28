import OpenAI from "openai";
import { readFileSync, writeFileSync, readdirSync, statSync } from "fs";
import { join, extname } from "path";

const openai = new OpenAI();

export function collectFiles(dir: string, maxFiles = 30): string[] {
  const files: string[] = [];
  const walk = (d: string) => {
    if (files.length >= maxFiles) return;
    for (const entry of readdirSync(d)) {
      if (entry.startsWith(".") || entry === "node_modules" || entry === "dist") continue;
      const full = join(d, entry);
      if (statSync(full).isDirectory()) walk(full);
      else if ([".ts", ".js", ".tsx", ".jsx", ".py", ".go", ".rs"].includes(extname(full))) {
        files.push(full);
      }
    }
  };
  walk(dir);
  return files;
}

export async function generateDiagram(files: string[], type: string): Promise<string> {
  const summary = files.map(f => {
    const content = readFileSync(f, "utf-8").slice(0, 500);
    return `// ${f}\n${content}`;
  }).join("\n\n").slice(0, 12000);

  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      { role: "system", content: `You generate Mermaid diagrams from code. Diagram type: ${type}.
Types: flowchart (default), class, sequence, er, state.
Analyze the code structure, relationships, and data flow.
Return ONLY the Mermaid diagram code, no markdown fences.` },
      { role: "user", content: summary }
    ],
    temperature: 0.3,
  });

  return response.choices[0].message.content?.trim() || "";
}
