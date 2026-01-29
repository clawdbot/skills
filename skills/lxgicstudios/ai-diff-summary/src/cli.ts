#!/usr/bin/env node

import { Command } from "commander";
import ora from "ora";
import { getDiff, summarizeDiff } from "./index";

const program = new Command();

program
  .name("ai-diff-summary")
  .description("Generate human-readable summaries of git diffs")
  .version("1.0.0")
  .argument("[ref]", "Git ref to diff against (e.g. HEAD~3, main, abc123)")
  .action(async (ref) => {
    const spinner = ora("Reading git diff...").start();
    try {
      const diff = getDiff(ref);
      if (!diff.trim()) {
        spinner.warn("No changes found in diff.");
        process.exit(0);
      }
      spinner.text = "Summarizing with AI...";
      const summary = await summarizeDiff(diff);
      spinner.stop();
      console.log("\n" + summary + "\n");
    } catch (err: any) {
      spinner.fail(err.message);
      process.exit(1);
    }
  });

program.parse();
