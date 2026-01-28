#!/usr/bin/env node

import { Command } from "commander";
import ora from "ora";
import { generateFromUrl, generateFromFile } from "./index";

const program = new Command();

program
  .name("ai-meta-tags")
  .description("Generate missing SEO meta tags, Open Graph, and Twitter cards")
  .version("1.0.0")
  .option("-u, --url <url>", "URL to scan")
  .option("-f, --file <path>", "Local HTML file to scan")
  .action(async (options: { url?: string; file?: string }) => {
    if (!options.url && !options.file) {
      console.error("Provide either --url or --file");
      process.exit(1);
    }

    const spinner = ora("Scanning for missing meta tags...").start();
    try {
      const result = options.url
        ? await generateFromUrl(options.url)
        : await generateFromFile(options.file!);

      if (result.missing.length === 0) {
        spinner.succeed("All essential meta tags are present!");
        return;
      }

      spinner.succeed(`Found ${result.missing.length} missing tag(s)\n`);

      console.log("Missing:");
      result.missing.forEach((tag) => console.log(`  - ${tag}`));
      console.log("\nGenerated tags (copy into your <head>):\n");
      console.log(result.generated);
    } catch (err: any) {
      spinner.fail(`Error: ${err.message}`);
      process.exit(1);
    }
  });

program.parse();
