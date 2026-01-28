#!/usr/bin/env node

import { Command } from "commander";
import ora from "ora";
import { scanQueryFiles, optimizeQueries } from "./index";

const program = new Command();

program
  .name("ai-query-optimize")
  .description("Optimize SQL and Prisma queries using AI")
  .version("1.0.0")
  .argument("[directory]", "Directory with query files", ".")
  .action(async (directory: string) => {
    const spinner = ora("Scanning query files...").start();
    try {
      const codeChunks = await scanQueryFiles(directory);
      if (codeChunks.length === 0) {
        spinner.warn("No query files found.");
        return;
      }
      spinner.text = `Optimizing ${codeChunks.length} file(s)...`;
      const analysis = await optimizeQueries(codeChunks);
      spinner.succeed("Query Optimization Complete:");
      console.log(`\n${analysis}`);
    } catch (err: any) {
      spinner.fail(`Error: ${err.message}`);
      process.exit(1);
    }
  });

program.parse();
