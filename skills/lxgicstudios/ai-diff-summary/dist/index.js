"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getDiff = getDiff;
exports.summarizeDiff = summarizeDiff;
const openai_1 = __importDefault(require("openai"));
const child_process_1 = require("child_process");
const openai = new openai_1.default({ apiKey: process.env.OPENAI_API_KEY });
function getDiff(ref) {
    const cmd = ref ? `git diff ${ref}` : "git diff HEAD";
    try {
        return (0, child_process_1.execSync)(cmd, { encoding: "utf-8", maxBuffer: 1024 * 1024 * 5 });
    }
    catch (err) {
        throw new Error(`Failed to get diff: ${err.message}`);
    }
}
async function summarizeDiff(diff) {
    const res = await openai.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [
            {
                role: "system",
                content: "You are a senior developer. Summarize the given git diff in clear, human-readable bullet points. Group changes by file or feature. Mention what was added, removed, or modified. Keep it concise but thorough.",
            },
            {
                role: "user",
                content: `Summarize this git diff:\n\n${diff.slice(0, 12000)}`,
            },
        ],
        temperature: 0.3,
    });
    return res.choices[0].message.content || "No summary generated.";
}
