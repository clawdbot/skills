"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateLogger = generateLogger;
const openai_1 = __importDefault(require("openai"));
const openai = new openai_1.default();
async function generateLogger(library, env = "node") {
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
