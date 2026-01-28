#!/usr/bin/env node
"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const commander_1 = require("commander");
const ora_1 = __importDefault(require("ora"));
const index_1 = require("./index");
const fs_1 = require("fs");
const program = new commander_1.Command();
program
    .name("ai-diagram")
    .description("Generate Mermaid diagrams from your codebase")
    .version("1.0.0")
    .argument("<dir>", "Source directory to analyze")
    .option("-t, --type <type>", "Diagram type: flowchart, class, sequence, er, state", "flowchart")
    .option("-o, --output <path>", "Output file", "diagram.mmd")
    .action(async (dir, options) => {
    const spinner = (0, ora_1.default)("Scanning codebase...").start();
    try {
        const files = (0, index_1.collectFiles)(dir);
        if (files.length === 0)
            throw new Error("No source files found");
        spinner.text = `Generating ${options.type} diagram from ${files.length} files...`;
        const diagram = await (0, index_1.generateDiagram)(files, options.type);
        (0, fs_1.writeFileSync)(options.output, diagram);
        spinner.succeed(`Diagram written to ${options.output}`);
        console.log("\n" + diagram);
    }
    catch (err) {
        spinner.fail(`Error: ${err.message}`);
        process.exit(1);
    }
});
program.parse();
