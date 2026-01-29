import OpenAI from "openai";
import * as fs from "fs";
import * as path from "path";

const openai = new OpenAI();

export async function suggestNames(filePath: string): Promise<string> {
  const content = fs.readFileSync(filePath, "utf-8");
  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: `You review code for naming quality. For each poorly named variable, function, class, or parameter:
- Show the current name
- Suggest a better name
- Explain why it's better (one line)
Focus on clarity, intent, and conventions. Skip names that are already good. If everything is well-named, say so.`
      },
      { role: "user", content: `File: ${path.basename(filePath)}\n\n${content}` }
    ],
    temperature: 0.4,
  });
  return response.choices[0].message.content || "";
}
