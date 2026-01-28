#!/usr/bin/env node

import { Command } from "commander";
import ora from "ora";
import * as fs from "fs";
import * as path from "path";
import { generateLogger } from "./index";

const program = new Command();

program
  .name("ai-logger")
  .description("Set up structured logging configuration")
  .version("1.0.0")
  .argument("<library>", "Logging library: pino, winston, bunyan")
  .option("-e, --env <environment>", "Environment: node, browser, edge", "node")
  .option("-o, --output <path>", "Output file path")
  .action(async (library: string, options: { env: string; output?: string }) => {
    const spinner = ora(`Generating ${library} logging config...`).start();
    try {
      const result = await generateLogger(library, options.env);
      spinner.succeed(`${library} logging config generated!`);

      if (options.output) {
        fs.writeFileSync(path.resolve(options.output), result, "utf-8");
        console.log(`  Written to ${options.output}`);
      } else {
        console.log("\n" + result);
      }
    } catch (err: any) {
      spinner.fail(`Error: ${err.message}`);
      process.exit(1);
    }
  });

program.parse();
