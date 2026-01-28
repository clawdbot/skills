import OpenAI from "openai";
import * as fs from "fs";
import * as path from "path";

const openai = new OpenAI();

export async function generateMonorepo(dir: string): Promise<string> {
  let context = "";
  const pkgPath = path.join(dir, "package.json");
  if (fs.existsSync(pkgPath)) {
    context = "Existing package.json:\n" + fs.readFileSync(pkgPath, "utf-8");
  }
  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      { role: "system", content: `You generate Turborepo monorepo configurations. Output a JSON object with file paths as keys and file contents as values. Include: turbo.json, root package.json with workspaces, packages/ui/package.json, packages/config/package.json, apps/web/package.json, apps/docs/package.json, and a root tsconfig.json. Follow Turborepo best practices with proper pipeline config.` },
      { role: "user", content: `Generate a Turborepo monorepo setup. ${context}` }
    ],
    temperature: 0.4,
    response_format: { type: "json_object" },
  });
  return response.choices[0].message.content || "{}";
}

export function writeFiles(dir: string, filesJson: string): string[] {
  const files = JSON.parse(filesJson);
  const written: string[] = [];
  for (const [filePath, content] of Object.entries(files)) {
    const fullPath = path.join(dir, filePath);
    fs.mkdirSync(path.dirname(fullPath), { recursive: true });
    fs.writeFileSync(fullPath, typeof content === "string" ? content : JSON.stringify(content, null, 2));
    written.push(filePath);
  }
  return written;
}
