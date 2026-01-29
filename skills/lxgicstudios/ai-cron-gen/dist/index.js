"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateCron = generateCron;
const openai_1 = __importDefault(require("openai"));
const openai = new openai_1.default();
async function generateCron(description) {
    const response = await openai.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [
            {
                role: "system",
                content: `Convert natural language to cron expressions. Return JSON with: expression (the cron string), explanation (human-readable confirmation), next_runs (array of 3 example run times as strings). Return ONLY valid JSON.`
            },
            { role: "user", content: description }
        ],
        temperature: 0.2,
        response_format: { type: "json_object" },
    });
    return JSON.parse(response.choices[0].message.content || "{}");
}
