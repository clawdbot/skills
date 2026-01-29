#!/usr/bin/env node

import { Command } from "commander";
import ora from "ora";
import * as fs from "fs";
import * as path from "path";
import { scanProject, generateDockerfile } from "./index";

const program = new Command();

program
  .name("ai-dockerfile")
  .description("Scans your project and generates an optimized Dockerfile")
  .version("1.0.0")
  .option("-p, --preview", "Preview without writing")
  .option("-o, --output <path>", "Output path", "Dockerfile")
  .option("-d, --dir <path>", "Project directory", ".")
  .option("--optimize", "Generate optimized multi-stage build")
  .action(async (opts) => {
    const spinner = ora("Scanning project...").start();

    try {
      const dir = path.resolve(opts.dir);
      const info = await scanProject(dir);

      if (info.files.length === 0) {
        spinner.warn("No project files found. Are you in the right directory?");
        process.exit(1);
      }

      spinner.text = `Found ${info.files.length} files. Generating Dockerfile...`;

      const dockerfile = await generateDockerfile(info, !!opts.optimize);

      if (opts.preview) {
        spinner.stop();
        console.log("\n--- Generated Dockerfile ---\n");
        console.log(dockerfile);
        console.log("\n----------------------------\n");
      } else {
        const outPath = path.resolve(opts.output);
        fs.writeFileSync(outPath, dockerfile + "\n");
        spinner.succeed(`Dockerfile written to ${outPath}`);
      }
    } catch (err: any) {
      spinner.fail(err.message);
      process.exit(1);
    }
  });

program.parse();
