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
exports.scanProject = scanProject;
exports.generateCompose = generateCompose;
const openai_1 = __importDefault(require("openai"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const openai = new openai_1.default({ apiKey: process.env.OPENAI_API_KEY });
function scanProject(dir) {
    const markers = [
        "package.json", "requirements.txt", "Gemfile", "go.mod", "Cargo.toml",
        "pom.xml", "build.gradle", "Dockerfile", ".env", "prisma/schema.prisma",
        "next.config.js", "next.config.mjs", "nuxt.config.ts", "vite.config.ts",
        "manage.py", "app.py", "main.go", "main.rs",
    ];
    const found = [];
    for (const m of markers) {
        if (fs.existsSync(path.join(dir, m)))
            found.push(m);
    }
    return found;
}
async function generateCompose(files, extra) {
    const res = await openai.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [
            {
                role: "system",
                content: "You are a DevOps expert. Generate a production-ready docker-compose.yml based on the project files detected. Include proper networking, volumes, health checks, and environment variables. Return ONLY the YAML, no explanation.",
            },
            {
                role: "user",
                content: `Project files found: ${files.join(", ")}${extra ? `\nAdditional requirements: ${extra}` : ""}\n\nGenerate docker-compose.yml`,
            },
        ],
        temperature: 0.3,
    });
    return res.choices[0].message.content || "";
}
