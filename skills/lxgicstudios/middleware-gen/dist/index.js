"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateMiddleware = generateMiddleware;
const openai_1 = __importDefault(require("openai"));
const openai = new openai_1.default({ apiKey: process.env.OPENAI_API_KEY });
async function generateMiddleware(description, options) {
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
