import OpenAI from "openai";

const openai = new OpenAI();

export async function generateLogger(library: string, env: string = "node"): Promise<string> {
  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: `You generate production-ready structured logging configurations.
Include:
- Logger setup with proper log levels
- Request ID / correlation ID support
- Pretty printing in development, JSON in production
- Log rotation config
- Error serialization
- HTTP request logging middleware
- Child logger pattern for modules
- Environment: ${env}
- Library: ${library}
Return ONLY the code, no explanations.`
      },
      { role: "user", content: `Generate complete structured logging setup using ${library}` }
    ],
    temperature: 0.3,
  });

  const result = response.choices[0].message.content?.trim() || "";
  return result.replace(/^```[\w]*\n?/, "").replace(/\n?```$/, "");
}
