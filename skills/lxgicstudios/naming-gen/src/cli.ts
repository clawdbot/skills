#!/usr/bin/env node

import { Command } from "commander";
import ora from "ora";
import { suggestNames } from "./index";

const program = new Command();

program
  .name("ai-naming")
  .description("Suggest better variable and function names")
  .version("1.0.0")
  .argument("<file>", "Code file to analyze")
  .action(async (file: string) => {
    const spinner = ora("Analyzing names...").start();
    try {
      const suggestions = await suggestNames(file);
      spinner.succeed("Naming suggestions:\n");
      console.log(suggestions);
    } catch (err: any) {
      spinner.fail(`Error: ${err.message}`);
      process.exit(1);
    }
  });

program.parse();
