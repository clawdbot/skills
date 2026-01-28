#!/usr/bin/env node

import { Command } from "commander";
import ora from "ora";
import { scanDirectory, aiAnalyze } from "./index";

const program = new Command();

program
  .name("ai-secret-scan")
  .description("Scan for leaked secrets and API keys")
  .version("1.0.0")
  .argument("[directory]", "Directory to scan", ".")
  .option("--no-ai", "Skip AI analysis, just pattern match")
  .action(async (directory: string, options: { ai: boolean }) => {
    const spinner = ora("Scanning for secrets...").start();
    try {
      const findings = await scanDirectory(directory);
      if (findings.length === 0) {
        spinner.succeed("No secrets found. You're clean!");
        return;
      }
      spinner.warn(`Found ${findings.length} potential secret(s)`);
      findings.forEach(f => {
        console.log(`\n  ⚠ ${f.type} in ${f.file}:${f.line}`);
        console.log(`    ${f.snippet}`);
      });
      if (options.ai) {
        const aiSpinner = ora("AI analyzing findings...").start();
        const analysis = await aiAnalyze(findings);
        aiSpinner.succeed("AI Analysis:");
        console.log(`\n${analysis}`);
      }
    } catch (err: any) {
      spinner.fail(`Error: ${err.message}`);
      process.exit(1);
    }
  });

program.parse();
