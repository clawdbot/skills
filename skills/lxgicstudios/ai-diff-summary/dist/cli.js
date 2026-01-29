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
    .name("ai-diff-summary")
    .description("Generate human-readable summaries of git diffs")
    .version("1.0.0")
    .argument("[ref]", "Git ref to diff against (e.g. HEAD~3, main, abc123)")
    .action(async (ref) => {
    const spinner = (0, ora_1.default)("Reading git diff...").start();
    try {
        const diff = (0, index_1.getDiff)(ref);
        if (!diff.trim()) {
            spinner.warn("No changes found in diff.");
            process.exit(0);
        }
        spinner.text = "Summarizing with AI...";
        const summary = await (0, index_1.summarizeDiff)(diff);
        spinner.stop();
        console.log("\n" + summary + "\n");
    }
    catch (err) {
        spinner.fail(err.message);
        process.exit(1);
    }
});
program.parse();
