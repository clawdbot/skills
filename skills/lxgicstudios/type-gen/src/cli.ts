#!/usr/bin/env node

import { Command } from "commander";
import ora from "ora";
import * as fs from "fs";
import { generateTypesFromFile } from "./index";

const program = new Command();

program
  .name("ai-type-gen")
  .description("Generate TypeScript interfaces from JSON files")
  .version("1.0.0")
  .argument("<file>", "Path to JSON file")
  .option("-n, --name <name>", "Root interface name", "ApiResponse")
  .option("-o, --output <file>", "Output file path (prints to stdout if omitted)")
  .action(async (file: string, options: { name: string; output?: string }) => {
    if (!fs.existsSync(file)) {
      console.error(`File not found: ${file}`);
      process.exit(1);
    }

    const spinner = ora("Generating TypeScript interfaces...").start();
    try {
      const result = await generateTypesFromFile(file, options.name);
      spinner.succeed("Types generated!");
      console.log("");

      if (options.output) {
        fs.writeFileSync(options.output, result);
        console.log(`Written to ${options.output}`);
      } else {
        console.log(result);
      }
    } catch (err: any) {
      spinner.fail(`Error: ${err.message}`);
      process.exit(1);
    }
  });

program.parse();
