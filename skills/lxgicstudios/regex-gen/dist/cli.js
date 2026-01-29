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
    .name("ai-regex")
    .description("Generate regex from plain English")
    .version("1.0.0")
    .argument("<description>", "What the regex should match")
    .option("-j, --json", "Output as JSON", false)
    .action(async (description, options) => {
    const spinner = (0, ora_1.default)("Generating regex...").start();
    try {
        const result = await (0, index_1.generateRegex)(description);
        spinner.succeed("Done!");
        if (options.json) {
            console.log(JSON.stringify(result, null, 2));
        }
        else {
            console.log(`\n  Pattern: /${result.pattern}/${result.flags}`);
            console.log(`  ${result.explanation}`);
            console.log(`\n  Examples:`);
            result.examples.forEach(ex => console.log(`    ✓ ${ex}`));
        }
    }
    catch (err) {
        spinner.fail(`Error: ${err.message}`);
        process.exit(1);
    }
});
program.parse();
