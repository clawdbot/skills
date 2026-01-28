"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.collectFiles = collectFiles;
exports.generateDiagram = generateDiagram;
const openai_1 = __importDefault(require("openai"));
const fs_1 = require("fs");
const path_1 = require("path");
const openai = new openai_1.default();
function collectFiles(dir, maxFiles = 30) {
    const files = [];
    const walk = (d) => {
        if (files.length >= maxFiles)
            return;
        for (const entry of (0, fs_1.readdirSync)(d)) {
            if (entry.startsWith(".") || entry === "node_modules" || entry === "dist")
                continue;
            const full = (0, path_1.join)(d, entry);
            if ((0, fs_1.statSync)(full).isDirectory())
                walk(full);
            else if ([".ts", ".js", ".tsx", ".jsx", ".py", ".go", ".rs"].includes((0, path_1.extname)(full))) {
                files.push(full);
            }
        }
    };
    walk(dir);
    return files;
}
async function generateDiagram(files, type) {
    const summary = files.map(f => {
        const content = (0, fs_1.readFileSync)(f, "utf-8").slice(0, 500);
        return `// ${f}\n${content}`;
    }).join("\n\n").slice(0, 12000);
    const response = await openai.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [
            { role: "system", content: `You generate Mermaid diagrams from code. Diagram type: ${type}.
Types: flowchart (default), class, sequence, er, state.
Analyze the code structure, relationships, and data flow.
Return ONLY the Mermaid diagram code, no markdown fences.` },
            { role: "user", content: summary }
        ],
        temperature: 0.3,
    });
    return response.choices[0].message.content?.trim() || "";
}
