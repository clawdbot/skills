import OpenAI from "openai";

const LICENSE_TYPES = [
  "MIT", "Apache-2.0", "GPL-3.0", "BSD-2-Clause", "BSD-3-Clause",
  "ISC", "MPL-2.0", "LGPL-3.0", "AGPL-3.0", "Unlicense"
];

export { LICENSE_TYPES };

export async function explainLicense(licenseType: string): Promise<string> {
  if (!process.env.OPENAI_API_KEY) {
    throw new Error("Missing OPENAI_API_KEY environment variable. Set it with: export OPENAI_API_KEY=sk-...");
  }

  const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: "Explain software licenses in plain English. Be casual, concise, and helpful. No legal jargon. Use bullet points for key points."
      },
      {
        role: "user",
        content: `Explain the ${licenseType} license in plain English. What can people do? What can't they do? Who should use it?`
      }
    ],
    temperature: 0.5,
  });

  return response.choices[0]?.message?.content?.trim() || "";
}

export async function generateLicense(licenseType: string, name: string, year?: number): Promise<string> {
  if (!process.env.OPENAI_API_KEY) {
    throw new Error("Missing OPENAI_API_KEY environment variable. Set it with: export OPENAI_API_KEY=sk-...");
  }

  const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
  const currentYear = year || new Date().getFullYear();

  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: "Generate the full text of a software license. Output ONLY the license text, nothing else. Use the exact standard text for the license type."
      },
      {
        role: "user",
        content: `Generate the full ${licenseType} license text for:\nCopyright holder: ${name}\nYear: ${currentYear}`
      }
    ],
    temperature: 0.1,
  });

  return response.choices[0]?.message?.content?.trim() || "";
}
