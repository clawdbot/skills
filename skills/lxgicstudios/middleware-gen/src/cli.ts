#!/usr/bin/env node

import { Command } from "commander";
import ora from "ora";
import * as fs from "fs";
import { generateMiddleware } from "./index";

const program = new Command();

program
  .name("ai-middleware")
  .description("Generate Express middleware from plain English")
  .version("1.0.0")
  .argument("<description>", "Describe the middleware you need")
  .option("-t, --typescript", "Generate TypeScript", false)
  .option("-o, --output <file>", "Write to file")
  .action(async (description, opts) => {
    const spinner = ora("Generating middleware...").start();
    try {
      const code = await generateMiddleware(description, opts);
      spinner.stop();
      if (opts.output) {
        fs.writeFileSync(opts.output, code);
        console.log(`Middleware written to ${opts.output}`);
      } else {
        console.log("\n" + code + "\n");
      }
    } catch (err: any) {
      spinner.fail(err.message);
      process.exit(1);
    }
  });

program.parse();
