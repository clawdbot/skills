#!/usr/bin/env node
"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const commander_1 = require("commander");
const ora_1 = __importDefault(require("ora"));
const index_1 = require("./index");
const program = new commander_1.Command();
program
    .name("ai-secret-scan")
    .description("Scan for leaked secrets and API keys")
    .version("1.0.0")
    .argument("[directory]", "Directory to scan", ".")
    .option("--no-ai", "Skip AI analysis, just pattern match")
    .action(async (directory, options) => {
    const spinner = (0, ora_1.default)("Scanning for secrets...").start();
    try {
        const findings = await (0, index_1.scanDirectory)(directory);
        if (findings.length === 0) {
            spinner.succeed("No secrets found. You're clean!");
            return;
        }
        spinner.warn(`Found ${findings.length} potential secret(s)`);
        findings.forEach(f => {
            console.log(`\n  ⚠ ${f.type} in ${f.file}:${f.line}`);
            console.log(`    ${f.snippet}`);
        });
        if (options.ai) {
            const aiSpinner = (0, ora_1.default)("AI analyzing findings...").start();
            const analysis = await (0, index_1.aiAnalyze)(findings);
            aiSpinner.succeed("AI Analysis:");
            console.log(`\n${analysis}`);
        }
    }
    catch (err) {
        spinner.fail(`Error: ${err.message}`);
        process.exit(1);
    }
});
program.parse();
