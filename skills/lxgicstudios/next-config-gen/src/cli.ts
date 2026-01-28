#!/usr/bin/env node
import { Command } from "commander";
import ora from "ora";
import * as fs from "fs";
import * as path from "path";
import { generateNextConfig } from "./index";

const program = new Command();
program
  .name("ai-next-config")
  .description("Generate Next.js config with best practices")
  .version("1.0.0")
  .argument("[dir]", "Project directory", ".")
  .option("-o, --output <file>", "Output file", "next.config.mjs")
  .action(async (dir: string, options: { output: string }) => {
    const spinner = ora("Generating Next.js config...").start();
    try {
      const config = await generateNextConfig(path.resolve(dir));
      fs.writeFileSync(options.output, config);
      spinner.succeed(`Next.js config written to ${options.output}`);
    } catch (err: any) {
      spinner.fail(`Error: ${err.message}`);
      process.exit(1);
    }
  });
program.parse();
