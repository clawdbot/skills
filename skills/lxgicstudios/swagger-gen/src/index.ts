import OpenAI from "openai";
import * as fs from "fs";
import * as path from "path";

const openai = new OpenAI();

export async function generateSwagger(dirPath: string): Promise<string> {
  const absDir = path.resolve(dirPath);
  const stat = fs.statSync(absDir);
  let routeCode = "";

  if (stat.isDirectory()) {
    const files = fs.readdirSync(absDir).filter(f => /\.(ts|js|mjs)$/.test(f));
    for (const file of files) {
      const content = fs.readFileSync(path.join(absDir, file), "utf-8");
      routeCode += `\n// === ${file} ===\n${content}\n`;
    }
  } else {
    routeCode = fs.readFileSync(absDir, "utf-8");
  }

  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: `You generate OpenAPI 3.0 specifications from Express/Node.js route code.
Rules:
- Detect all routes (GET, POST, PUT, DELETE, PATCH)
- Infer request/response schemas from the code
- Add proper descriptions, parameters, and response codes
- Include authentication if detected (Bearer, API key, etc.)
- Output valid YAML OpenAPI 3.0 spec
- Return ONLY the YAML, no explanations`
      },
      { role: "user", content: routeCode }
    ],
    temperature: 0.2,
  });

  const result = response.choices[0].message.content?.trim() || "";
  return result.replace(/^```[\w]*\n?/, "").replace(/\n?```$/, "");
}
