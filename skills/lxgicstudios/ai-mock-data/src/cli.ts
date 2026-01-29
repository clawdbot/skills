#!/usr/bin/env node

import { Command } from "commander";
import ora from "ora";
import * as fs from "fs";
import { generateMockData } from "./index";

const program = new Command();

program
  .name("ai-mock-data")
  .description("Generate realistic mock data from descriptions, types, or schemas")
  .version("1.0.0")
  .argument("<description>", "Describe the data you want, or pass a file path")
  .option("-c, --count <number>", "Number of records", "10")
  .option("-f, --format <fmt>", "Output format: json, csv, sql", "json")
  .option("-s, --schema <file>", "Path to a TS type or JSON schema file")
  .option("-o, --output <file>", "Write to a file")
  .action(async (description: string, options: any) => {
    const spinner = ora("Cooking up some data...").start();

    try {
      const data = await generateMockData({
        description,
        count: parseInt(options.count, 10),
        format: options.format,
        schema: options.schema,
      });

      spinner.succeed("Done!");
      console.log("\n" + data);

      if (options.output) {
        fs.writeFileSync(options.output, data, "utf-8");
        console.log(`\nWritten to ${options.output}`);
      }
    } catch (err: any) {
      spinner.fail(err.message);
      process.exit(1);
    }
  });

program.parse();
