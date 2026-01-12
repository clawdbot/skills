---
name: sudoku
description: Fetch Sudoku puzzles and store them as JSON in the workspace; render images on demand; reveal solutions later.
metadata:
  clawdbot:
    emoji: "🧩"
    requires:
      bins: ["python3", "node"]
---

# Sudoku

## Overview

Fetch, render, and reveal Sudoku puzzles. Use `sudoku.py` to get new puzzles from `sudokuonline.io`, generate printable PDFs or images, and reveal solutions.

## Actions

### Get a Puzzle

Fetches a new puzzle and stores it as JSON. Output is JSON by default (use `--text` for human-readable output).

**Get a Classic Easy puzzle:**
```bash
./sudoku.py get easy9
```

**Get a Kids 6x6 puzzle:**
```bash
./sudoku.py get kids6
```

### Render Puzzle

Render a puzzle as an image or PDF.

**Render latest puzzle as A4 PDF (for printing):**
```bash
./sudoku.py render --pdf
```

**Render latest puzzle as clean PNG (for viewing):**
```bash
./sudoku.py render
```

**Render a specific previous puzzle by short ID:**
```bash
./sudoku.py render --id a09f3680
```

### Reveal Solution

Reveal the solution for the latest or specific puzzle.

**Reveal full solution as printable PDF:**
```bash
./sudoku.py reveal --pdf
```

**Reveal full solution as PNG image:**
```bash
./sudoku.py reveal
```

**Reveal a single cell (row 3, column 7):**
```bash
./sudoku.py reveal --cell 3 7
```

**Reveal a specific 3x3 box (index 5):**
```bash
./sudoku.py reveal --box 5
```

### Share Link

Generate a share link for a stored puzzle.

**Generate a SudokuPad share link (default):**
```bash
./sudoku.py share
```

**Generate an SCL share link:**
```bash
./sudoku.py share --type scl
```

**Generate an fpuzzles share link:**
```bash
./sudoku.py share --type fpuzzle
```

**Telegram Formatting Tip:**
Format links as a short button-style link and hide the full URL: `[Easy Classic \[<id>\]](<url>)`.
