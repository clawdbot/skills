"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.scanFile = scanFile;
exports.scanDirectory = scanDirectory;
exports.aiAnalyze = aiAnalyze;
const openai_1 = __importDefault(require("openai"));
const fs = __importStar(require("fs"));
const glob_1 = require("glob");
const openai = new openai_1.default();
const PATTERNS = [
    { name: "AWS Key", regex: /AKIA[0-9A-Z]{16}/ },
    { name: "Generic Secret", regex: /(api[_-]?key|secret|token|password|credential)\s*[:=]\s*['"][^'"]{8,}['"]/gi },
    { name: "Private Key", regex: /-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----/ },
    { name: "GitHub Token", regex: /gh[pousr]_[A-Za-z0-9_]{36,}/ },
    { name: "Slack Token", regex: /xox[baprs]-[0-9a-zA-Z-]+/ },
    { name: "JWT", regex: /eyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+/ },
];
async function scanFile(filePath) {
    const content = fs.readFileSync(filePath, "utf-8");
    const lines = content.split("\n");
    const findings = [];
    lines.forEach((line, i) => {
        for (const p of PATTERNS) {
            if (p.regex.test(line)) {
                findings.push({ file: filePath, line: i + 1, type: p.name, severity: "high", snippet: line.trim().substring(0, 100) });
            }
            p.regex.lastIndex = 0;
        }
    });
    return findings;
}
async function scanDirectory(dir) {
    const files = await (0, glob_1.glob)("**/*.{js,ts,jsx,tsx,py,rb,go,java,env,json,yml,yaml,toml,cfg,conf,ini}", {
        cwd: dir, absolute: true, ignore: ["**/node_modules/**", "**/dist/**", "**/.git/**"]
    });
    const all = [];
    for (const f of files) {
        try {
            const findings = await scanFile(f);
            all.push(...findings);
        }
        catch { }
    }
    return all;
}
async function aiAnalyze(findings) {
    if (findings.length === 0)
        return "No secrets found. Your code looks clean!";
    const response = await openai.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [
            { role: "system", content: "You analyze potential secret leaks in code. For each finding, confirm if it's a real leak or false positive, rate severity, and suggest a fix. Be concise." },
            { role: "user", content: JSON.stringify(findings) }
        ],
        temperature: 0.2,
    });
    return response.choices[0].message.content || "";
}
