#!/usr/bin/env node

import { Command } from "commander";
import ora from "ora";
import { scanRoutes, generateRBAC } from "./index";

const program = new Command();

program
  .name("ai-permission")
  .description("Generate RBAC permission configs from your routes")
  .version("1.0.0")
  .argument("[directory]", "Routes directory to scan", ".")
  .action(async (directory: string) => {
    const spinner = ora("Scanning routes...").start();
    try {
      const routeCode = await scanRoutes(directory);
      if (routeCode.length === 0) {
        spinner.warn("No route files found.");
        return;
      }
      spinner.text = `Generating RBAC config from ${routeCode.length} file(s)...`;
      const rbac = await generateRBAC(routeCode);
      spinner.succeed("RBAC Config Generated:");
      console.log(`\n${rbac}`);
    } catch (err: any) {
      spinner.fail(`Error: ${err.message}`);
      process.exit(1);
    }
  });

program.parse();
