#!/usr/bin/env node
import { Command } from "commander";
import ora from "ora";
import { collectFiles, generateDiagram } from "./index";
import { writeFileSync } from "fs";

const program = new Command();
program
  .name("ai-diagram")
  .description("Generate Mermaid diagrams from your codebase")
  .version("1.0.0")
  .argument("<dir>", "Source directory to analyze")
  .option("-t, --type <type>", "Diagram type: flowchart, class, sequence, er, state", "flowchart")
  .option("-o, --output <path>", "Output file", "diagram.mmd")
  .action(async (dir: string, options: { type: string; output: string }) => {
    const spinner = ora("Scanning codebase...").start();
    try {
      const files = collectFiles(dir);
      if (files.length === 0) throw new Error("No source files found");
      spinner.text = `Generating ${options.type} diagram from ${files.length} files...`;
      const diagram = await generateDiagram(files, options.type);
      writeFileSync(options.output, diagram);
      spinner.succeed(`Diagram written to ${options.output}`);
      console.log("\n" + diagram);
    } catch (err: any) {
      spinner.fail(`Error: ${err.message}`);
      process.exit(1);
    }
  });
program.parse();
