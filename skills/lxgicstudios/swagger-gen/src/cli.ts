#!/usr/bin/env node

import { Command } from "commander";
import ora from "ora";
import * as fs from "fs";
import * as path from "path";
import { generateSwagger } from "./index";

const program = new Command();

program
  .name("ai-swagger")
  .description("Generate OpenAPI spec from Express routes")
  .version("1.0.0")
  .argument("<path>", "Routes directory or file")
  .option("-o, --output <path>", "Output file path", "openapi.yaml")
  .action(async (routePath: string, options: { output: string }) => {
    const spinner = ora("Generating OpenAPI spec...").start();
    try {
      const result = await generateSwagger(routePath);
      spinner.succeed("OpenAPI spec generated!");

      fs.writeFileSync(path.resolve(options.output), result, "utf-8");
      console.log(`  Written to ${options.output}`);
    } catch (err: any) {
      spinner.fail(`Error: ${err.message}`);
      process.exit(1);
    }
  });

program.parse();
