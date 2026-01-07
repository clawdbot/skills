#!/usr/bin/env bash
# Convenience wrapper for ticktick CLI
cd "$(dirname "$0")/.." && bun run scripts/ticktick.ts "$@"
