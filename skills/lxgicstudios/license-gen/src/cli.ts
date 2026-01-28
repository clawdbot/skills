#!/usr/bin/env node

import { Command } from "commander";
import ora from "ora";
import inquirer from "inquirer";
import * as fs from "fs";
import * as path from "path";
import { explainLicense, generateLicense, LICENSE_TYPES } from "./index";

const program = new Command();

program
  .name("ai-license")
  .description("Interactive license picker that explains licenses in plain English")
  .version("1.0.0")
  .option("-t, --type <license>", "License type (e.g. mit, apache-2.0)")
  .option("-n, --name <name>", "Copyright holder name")
  .option("-o, --output <path>", "Output path", "LICENSE")
  .option("-e, --explain <license>", "Explain a license without generating it")
  .action(async (opts) => {
    try {
      if (opts.explain) {
        const spinner = ora("Looking up that license...").start();
        const explanation = await explainLicense(opts.explain);
        spinner.stop();
        console.log(`\n${explanation}\n`);
        return;
      }

      let licenseType = opts.type;
      let name = opts.name;

      if (!licenseType || !name) {
        const answers = await inquirer.prompt([
          ...(!licenseType ? [{
            type: "list" as const,
            name: "licenseType",
            message: "Pick a license:",
            choices: LICENSE_TYPES,
          }] : []),
          ...(!name ? [{
            type: "input" as const,
            name: "name",
            message: "Copyright holder name:",
            validate: (input: string) => input.length > 0 || "Name can't be empty",
          }] : []),
        ]);

        licenseType = licenseType || answers.licenseType;
        name = name || answers.name;
      }

      const spinner = ora("Generating license...").start();

      const explanation = await explainLicense(licenseType);
      spinner.stop();
      console.log(`\nHere's what ${licenseType} means:\n${explanation}\n`);

      const { proceed } = await inquirer.prompt([{
        type: "confirm",
        name: "proceed",
        message: "Want to generate this license?",
        default: true,
      }]);

      if (!proceed) {
        console.log("No worries. Run again when you're ready.");
        return;
      }

      spinner.start("Writing LICENSE file...");
      const licenseText = await generateLicense(licenseType, name);
      const outPath = path.resolve(opts.output);
      fs.writeFileSync(outPath, licenseText + "\n");
      spinner.succeed(`LICENSE written to ${outPath}`);
    } catch (err: any) {
      console.error(`\nError: ${err.message}`);
      process.exit(1);
    }
  });

program.parse();
