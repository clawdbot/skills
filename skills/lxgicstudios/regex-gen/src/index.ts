import OpenAI from "openai";

const openai = new OpenAI();

export interface RegexResult {
  pattern: string;
  flags: string;
  explanation: string;
  examples: string[];
}

export async function generateRegex(description: string): Promise<RegexResult> {
  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: `You generate regex patterns from descriptions. Return JSON with: pattern (the regex without delimiters), flags (like "gi"), explanation (one line), examples (array of 3 matching strings). Return ONLY valid JSON.`
      },
      { role: "user", content: description }
    ],
    temperature: 0.3,
    response_format: { type: "json_object" },
  });
  return JSON.parse(response.choices[0].message.content || "{}");
}
