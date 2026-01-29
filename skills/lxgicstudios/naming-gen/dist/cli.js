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
    .name("ai-naming")
    .description("Suggest better variable and function names")
    .version("1.0.0")
    .argument("<file>", "Code file to analyze")
    .action(async (file) => {
    const spinner = (0, ora_1.default)("Analyzing names...").start();
    try {
        const suggestions = await (0, index_1.suggestNames)(file);
        spinner.succeed("Naming suggestions:\n");
        console.log(suggestions);
    }
    catch (err) {
        spinner.fail(`Error: ${err.message}`);
        process.exit(1);
    }
});
program.parse();
