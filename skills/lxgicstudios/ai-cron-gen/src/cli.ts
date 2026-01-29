#!/usr/bin/env node

import { Command } from "commander";
import ora from "ora";
import { generateCron } from "./index";

const program = new Command();

program
  .name("ai-cron-gen")
  .description("Convert natural language to cron expressions")
  .version("1.0.0")
  .argument("<description>", "When you want it to run")
  .action(async (description: string) => {
    const spinner = ora("Generating cron expression...").start();
    try {
      const result = await generateCron(description);
      spinner.succeed("Done!");
      console.log(`\n  Cron: ${result.expression}`);
      console.log(`  Meaning: ${result.explanation}`);
      console.log(`\n  Next runs:`);
      result.next_runs.forEach(r => console.log(`    - ${r}`));
    } catch (err: any) {
      spinner.fail(`Error: ${err.message}`);
      process.exit(1);
    }
  });

program.parse();
