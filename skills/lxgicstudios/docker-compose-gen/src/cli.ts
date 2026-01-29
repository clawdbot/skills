#!/usr/bin/env node

import { Command } from "commander";
import ora from "ora";
import * as fs from "fs";
import { scanProject, generateCompose } from "./index";

const program = new Command();

program
  .name("ai-docker-compose")
  .description("Generate docker-compose.yml by scanning your project")
  .version("1.0.0")
  .option("-d, --dir <path>", "Project directory", ".")
  .option("-o, --output <file>", "Output file", "docker-compose.yml")
  .option("--preview", "Print to stdout instead of writing", false)
  .option("-a, --add <services>", "Additional services to include (e.g. redis,postgres)")
  .action(async (opts) => {
    const spinner = ora("Scanning project...").start();
    try {
      const files = scanProject(opts.dir);
      if (files.length === 0) {
        spinner.warn("No project files found.");
        process.exit(1);
      }
      spinner.text = `Found ${files.length} markers. Generating docker-compose.yml...`;
      const yaml = await generateCompose(files, opts.add);
      spinner.stop();
      if (opts.preview) {
        console.log("\n" + yaml + "\n");
      } else {
        fs.writeFileSync(opts.output, yaml);
        console.log(`Written to ${opts.output}`);
      }
    } catch (err: any) {
      spinner.fail(err.message);
      process.exit(1);
    }
  });

program.parse();
