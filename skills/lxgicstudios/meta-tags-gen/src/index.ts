import OpenAI from "openai";
import * as cheerio from "cheerio";
import * as fs from "fs";
import * as https from "https";
import * as http from "http";

const openai = new OpenAI();

interface MetaAudit {
  existing: Record<string, string>;
  missing: string[];
  generated: string;
}

function fetchUrl(url: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const client = url.startsWith("https") ? https : http;
    client.get(url, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => resolve(data));
      res.on("error", reject);
    }).on("error", reject);
  });
}

export function auditExistingMeta(html: string): { existing: Record<string, string>; missing: string[] } {
  const $ = cheerio.load(html);
  const existing: Record<string, string> = {};

  const title = $("title").text();
  if (title) existing["title"] = title;

  $("meta").each((_, el) => {
    const name = $(el).attr("name") || $(el).attr("property") || "";
    const content = $(el).attr("content") || "";
    if (name && content) existing[name] = content;
  });

  const required = [
    "title", "description",
    "og:title", "og:description", "og:image", "og:url", "og:type",
    "twitter:card", "twitter:title", "twitter:description", "twitter:image",
  ];

  const missing = required.filter((tag) => !existing[tag]);
  return { existing, missing };
}

export async function generateMetaTags(html: string, url?: string): Promise<MetaAudit> {
  const { existing, missing } = auditExistingMeta(html);

  if (missing.length === 0) {
    return { existing, missing: [], generated: "<!-- All essential meta tags are present! -->" };
  }

  const $ = cheerio.load(html);
  const bodyText = $("body").text().slice(0, 2000);
  const pageTitle = $("title").text() || $("h1").first().text() || "";

  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: `You generate HTML meta tags for SEO. Rules:
- Only generate tags that are MISSING (listed below)
- Use the page content to write accurate, compelling descriptions
- Keep meta description under 160 chars
- OG image should use a placeholder URL like https://example.com/og-image.png
- Return ONLY valid HTML meta tags, one per line, no markdown fences`
      },
      {
        role: "user",
        content: `URL: ${url || "unknown"}
Page title: ${pageTitle}
Missing tags: ${missing.join(", ")}
Existing tags: ${JSON.stringify(existing)}

Page content preview:
${bodyText}`
      }
    ],
    temperature: 0.3,
  });

  return {
    existing,
    missing,
    generated: response.choices[0].message.content?.trim() || "",
  };
}

export async function generateFromUrl(url: string): Promise<MetaAudit> {
  const html = await fetchUrl(url);
  return generateMetaTags(html, url);
}

export async function generateFromFile(filePath: string): Promise<MetaAudit> {
  const html = fs.readFileSync(filePath, "utf-8");
  return generateMetaTags(html);
}
