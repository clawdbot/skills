---
name: docker-writer
description: Scan your project and generate an optimized Dockerfile. Use when you need to containerize fast.
---

# Docker Writer

Writing Dockerfiles isn't hard, but writing good ones is. Multi-stage builds, proper layer caching, small image sizes. Most people copy-paste from Stack Overflow and call it done. This tool scans your project, figures out what runtime and dependencies you're using, and generates a properly optimized Dockerfile. It handles the boring parts so you can focus on shipping.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-dockerfile
```

## What It Does

- Scans your project directory to detect language, framework, and dependencies
- Generates a Dockerfile with proper base images and build steps
- Supports optimized multi-stage builds with the --optimize flag
- Preview mode lets you review before writing any files
- Works with Node.js, Python, Go, and other common project types

## Usage Examples

```bash
# Generate Dockerfile for current project
npx ai-dockerfile

# Preview without writing to disk
npx ai-dockerfile --preview

# Generate optimized multi-stage build
npx ai-dockerfile --optimize

# Specify project directory and output path
npx ai-dockerfile --dir ./my-app --output docker/Dockerfile
```

## Best Practices

- **Always preview first** - Run with --preview before writing. Check that the base image, build steps, and exposed ports make sense for your project.
- **Use --optimize for production** - Multi-stage builds produce smaller images. The default is fine for development, but use --optimize when you're deploying.
- **Check your .dockerignore** - The tool generates the Dockerfile, but you still need a .dockerignore to keep node_modules and other junk out of the build context.
- **Test the build** - Run docker build after generating. The output is good but edge cases in your project setup might need manual tweaks.

## When to Use This

- You're containerizing a project for the first time
- You want a multi-stage build but don't remember the syntax
- Quick prototyping where you need a working container fast
- Onboarding a project to Docker that's never been containerized

## How It Works

The tool scans your project directory for package.json, requirements.txt, go.mod, and other dependency files. It identifies your tech stack and sends that info to an AI model that generates a Dockerfile tailored to your project. With --optimize, it creates multi-stage builds that separate build and runtime stages.

## Requirements

No install needed. Just run with npx. Node.js 18+ recommended.

```bash
npx ai-dockerfile --help
```

## Part of the LXGIC Dev Toolkit

This is one of 110+ free developer tools built by LXGIC Studios. No paywalls, no sign-ups, no API keys on free tiers. Just tools that work.

**Find more:**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- Website: https://lxgic.dev

## License

MIT. Free forever. Use it however you want.