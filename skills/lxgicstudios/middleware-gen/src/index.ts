import OpenAI from "openai";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function generateMiddleware(description: string, options: { typescript?: boolean }): Promise<string> {
  const lang = options.typescript ? "TypeScript" : "JavaScript";

  const res = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: `You are a senior Node.js developer. Generate a complete Express middleware function in ${lang}. Include proper error handling, types, and inline comments. The middleware should be production-ready and exportable. Return ONLY the code, no explanation.`,
      },
      {
        role: "user",
        content: `Create Express middleware: ${description}`,
      },
    ],
    temperature: 0.3,
  });
  return res.choices[0].message.content || "";
}
