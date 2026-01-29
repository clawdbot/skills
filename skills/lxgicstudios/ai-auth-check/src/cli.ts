#!/usr/bin/env node
import { Command } from "commander";
import ora from "ora";
import * as fs from "fs";
import * as path from "path";
import { auditAuth } from "./index";

const program = new Command();
program
  .name("ai-auth-check")
  .description("Audit auth implementation for security flaws")
  .version("1.0.0")
  .argument("<dir>", "Directory containing auth code")
  .option("-o, --output <file>", "Output file", "auth-audit.md")
  .action(async (dir: string, options: { output: string }) => {
    const spinner = ora("Auditing auth implementation...").start();
    try {
      const audit = await auditAuth(path.resolve(dir));
      fs.writeFileSync(options.output, audit);
      spinner.succeed(`Audit written to ${options.output}`);
      console.log("\n" + audit);
    } catch (err: any) {
      spinner.fail(`Error: ${err.message}`);
      process.exit(1);
    }
  });
program.parse();
