"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateRegex = generateRegex;
const openai_1 = __importDefault(require("openai"));
const openai = new openai_1.default();
async function generateRegex(description) {
    const response = await openai.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [
            {
                role: "system",
                content: `You generate regex patterns from descriptions. Return JSON with: pattern (the regex without delimiters), flags (like "gi"), explanation (one line), examples (array of 3 matching strings). Return ONLY valid JSON.`
            },
            { role: "user", content: description }
        ],
        temperature: 0.3,
        response_format: { type: "json_object" },
    });
    return JSON.parse(response.choices[0].message.content || "{}");
}
