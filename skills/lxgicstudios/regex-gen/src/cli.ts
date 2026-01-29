#!/usr/bin/env node

import { Command } from "commander";
import ora from "ora";
import { generateRegex } from "./index";

const program = new Command();

program
  .name("ai-regex")
  .description("Generate regex from plain English")
  .version("1.0.0")
  .argument("<description>", "What the regex should match")
  .option("-j, --json", "Output as JSON", false)
  .action(async (description: string, options: { json: boolean }) => {
    const spinner = ora("Generating regex...").start();
    try {
      const result = await generateRegex(description);
      spinner.succeed("Done!");
      if (options.json) {
        console.log(JSON.stringify(result, null, 2));
      } else {
        console.log(`\n  Pattern: /${result.pattern}/${result.flags}`);
        console.log(`  ${result.explanation}`);
        console.log(`\n  Examples:`);
        result.examples.forEach(ex => console.log(`    ✓ ${ex}`));
      }
    } catch (err: any) {
      spinner.fail(`Error: ${err.message}`);
      process.exit(1);
    }
  });

program.parse();
