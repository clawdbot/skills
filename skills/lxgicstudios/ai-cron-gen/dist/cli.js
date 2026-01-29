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
    .name("ai-cron-gen")
    .description("Convert natural language to cron expressions")
    .version("1.0.0")
    .argument("<description>", "When you want it to run")
    .action(async (description) => {
    const spinner = (0, ora_1.default)("Generating cron expression...").start();
    try {
        const result = await (0, index_1.generateCron)(description);
        spinner.succeed("Done!");
        console.log(`\n  Cron: ${result.expression}`);
        console.log(`  Meaning: ${result.explanation}`);
        console.log(`\n  Next runs:`);
        result.next_runs.forEach(r => console.log(`    - ${r}`));
    }
    catch (err) {
        spinner.fail(`Error: ${err.message}`);
        process.exit(1);
    }
});
program.parse();
