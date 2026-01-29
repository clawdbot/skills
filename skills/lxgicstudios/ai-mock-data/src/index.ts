import OpenAI from "openai";
import * as fs from "fs";
import * as path from "path";

export interface MockDataOptions {
  description: string;
  count?: number;
  format?: "json" | "csv" | "sql";
  schema?: string;
}

function tryReadFile(input: string): string | null {
  const resolved = path.resolve(process.cwd(), input);
  if (fs.existsSync(resolved)) {
    return fs.readFileSync(resolved, "utf-8");
  }
  return null;
}

export async function generateMockData(options: MockDataOptions): Promise<string> {
  const count = options.count || 10;
  const format = options.format || "json";

  let schemaInfo = "";
  if (options.schema) {
    const fileContent = tryReadFile(options.schema);
    if (fileContent) {
      schemaInfo = `\n\nSchema/type definition:\n${fileContent}`;
    } else {
      schemaInfo = `\n\nSchema: ${options.schema}`;
    }
  }

  const openai = new OpenAI();

  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: `You generate realistic mock data. Output exactly ${count} records in ${format} format. Make the data look real, not obviously fake. Use realistic names, emails, dates, etc. Vary the data. Don't use "John Doe" or "test@example.com". Output ONLY the data, no explanation or markdown code fences.`,
      },
      {
        role: "user",
        content: `Generate mock data for: ${options.description}${schemaInfo}`,
      },
    ],
    temperature: 0.8,
  });

  return response.choices[0]?.message?.content || "No data generated";
}
