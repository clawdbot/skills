import OpenAI from "openai";
import * as fs from "fs";
import * as path from "path";

const openai = new OpenAI();

export async function generate(filePath: string): Promise<string> {
  let content: string;
  const resolved = path.resolve(filePath);

  if (fs.statSync(resolved).isDirectory()) {
    const files = fs.readdirSync(resolved).filter(f => /\.(ts|js|prisma)$/.test(f));
    content = files.map(f => {
      const fp = path.join(resolved, f);
      return `// File: ${f}\n${fs.readFileSync(fp, "utf-8")}`;
    }).join("\n\n");
  } else {
    content = fs.readFileSync(resolved, "utf-8");
  }

  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      { role: "system", content: `You are a validation schema expert. Read the TypeScript types/interfaces provided and generate both Zod and Yup validation schemas. Include: all fields with proper types, optional fields, enums, nested objects, arrays, string constraints (email, url, min/max length), number constraints. Output both Zod and Yup versions clearly separated.` },
      { role: "user", content: `File: ${path.basename(filePath)}\n\n${content}` }
    ],
    temperature: 0.3,
  });
  return response.choices[0].message.content || "";
}
