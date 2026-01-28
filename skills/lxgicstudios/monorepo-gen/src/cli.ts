#!/usr/bin/env node
import { Command } from "commander";
import ora from "ora";
import * as path from "path";
import { generateMonorepo, writeFiles } from "./index";

const program = new Command();
program
  .name("ai-monorepo")
  .description("Set up a Turborepo monorepo structure")
  .version("1.0.0")
  .argument("[dir]", "Target directory", ".")
  .action(async (dir: string) => {
    const spinner = ora("Generating monorepo structure...").start();
    try {
      const result = await generateMonorepo(path.resolve(dir));
      const files = writeFiles(path.resolve(dir), result);
      spinner.succeed(`Monorepo created with ${files.length} files:`);
      files.forEach(f => console.log(`  - ${f}`));
    } catch (err: any) {
      spinner.fail(`Error: ${err.message}`);
      process.exit(1);
    }
  });
program.parse();
