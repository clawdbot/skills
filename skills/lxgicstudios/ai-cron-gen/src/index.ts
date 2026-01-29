import OpenAI from "openai";

const openai = new OpenAI();

export interface CronResult {
  expression: string;
  explanation: string;
  next_runs: string[];
}

export async function generateCron(description: string): Promise<CronResult> {
  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: `Convert natural language to cron expressions. Return JSON with: expression (the cron string), explanation (human-readable confirmation), next_runs (array of 3 example run times as strings). Return ONLY valid JSON.`
      },
      { role: "user", content: description }
    ],
    temperature: 0.2,
    response_format: { type: "json_object" },
  });
  return JSON.parse(response.choices[0].message.content || "{}");
}
