import OpenAI from "openai";
import { execSync } from "child_process";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export function getDiff(ref?: string): string {
  const cmd = ref ? `git diff ${ref}` : "git diff HEAD";
  try {
    return execSync(cmd, { encoding: "utf-8", maxBuffer: 1024 * 1024 * 5 });
  } catch (err: any) {
    throw new Error(`Failed to get diff: ${err.message}`);
  }
}

export async function summarizeDiff(diff: string): Promise<string> {
  const res = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: "You are a senior developer. Summarize the given git diff in clear, human-readable bullet points. Group changes by file or feature. Mention what was added, removed, or modified. Keep it concise but thorough.",
      },
      {
        role: "user",
        content: `Summarize this git diff:\n\n${diff.slice(0, 12000)}`,
      },
    ],
    temperature: 0.3,
  });
  return res.choices[0].message.content || "No summary generated.";
}
