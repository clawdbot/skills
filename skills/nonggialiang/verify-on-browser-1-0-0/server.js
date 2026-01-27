// Minimal CDP MCP Server - Maximum flexibility browser control
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { chromium } from "playwright";
import { z } from "zod";

const server = new McpServer({
  name: "browser-cdp",
  version: "1.0.0",
});

let browser = null;
let page = null;
let cdp = null;

async function ensureBrowser() {
  if (!browser) {
    browser = await chromium.launch({
      headless: false,
      args: ["--disable-web-security", "--allow-running-insecure-content"],
    });
    page = await browser.newPage();
    cdp = await page.context().newCDPSession(page);
  }
  return { browser, page, cdp };
}

// Core tool: Raw CDP method - call ANY Chrome DevTools Protocol method
// Reference: https://chromedevtools.github.io/devtools-protocol/
server.tool(
  "cdp_send",
  {
    method: z
      .string()
      .describe("CDP method (e.g., 'Page.navigate', 'DOM.getDocument', 'Runtime.evaluate')"),
    params: z
      .record(z.unknown())
      .optional()
      .describe("Parameters object for the CDP method"),
  },
  async ({ method, params }) => {
    const { cdp } = await ensureBrowser();
    try {
      const result = await cdp.send(method, params || {});
      return {
        content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ error: error.message }, null, 2),
          },
        ],
        isError: true,
      };
    }
  }
);

// Convenience: Take screenshot (returns base64 image)
server.tool(
  "screenshot",
  {
    format: z.enum(["png", "jpeg"]).optional().describe("Image format"),
    fullPage: z.boolean().optional().describe("Capture full scrollable page"),
  },
  async ({ format = "png", fullPage = false }) => {
    const { page } = await ensureBrowser();
    const buffer = await page.screenshot({ type: format, fullPage });
    return {
      content: [
        {
          type: "image",
          data: buffer.toString("base64"),
          mimeType: `image/${format}`,
        },
      ],
    };
  }
);

// Convenience: Get current URL
server.tool("get_url", {}, async () => {
  const { page } = await ensureBrowser();
  return { content: [{ type: "text", text: page.url() }] };
});

// Convenience: Close browser
server.tool("close_browser", {}, async () => {
  if (browser) {
    await browser.close();
    browser = null;
    page = null;
    cdp = null;
  }
  return { content: [{ type: "text", text: "Browser closed" }] };
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
