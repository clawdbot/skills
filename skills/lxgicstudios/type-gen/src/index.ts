import OpenAI from "openai";
import * as fs from "fs";

const openai = new OpenAI();

export async function generateTypes(jsonContent: string, name: string): Promise<string> {
  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: `You generate TypeScript interfaces from JSON data. Rules:
- Use the provided name for the root interface
- Create nested interfaces for nested objects (use PascalCase names)
- Use proper types: string, number, boolean, arrays, etc.
- Mark fields that could be null as optional with ?
- Add brief JSDoc comments for non-obvious fields
- Use readonly for id fields
- Return ONLY the TypeScript code, no explanations or markdown fences`
      },
      { role: "user", content: `Generate TypeScript interfaces for this JSON. Root interface name: ${name}\n\n${jsonContent}` }
    ],
    temperature: 0.2,
  });

  return response.choices[0].message.content?.trim() || "";
}

export async function generateTypesFromFile(filePath: string, name: string): Promise<string> {
  const content = fs.readFileSync(filePath, "utf-8");
  JSON.parse(content); // validate it's valid JSON
  return generateTypes(content, name);
}
