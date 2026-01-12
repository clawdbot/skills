#!/usr/bin/env python3
"""
Fetch and render Sudoku puzzles from sudokuonline.io.
Supports 4x4, 6x6, and 9x9 grids, including letters mode.

Usage:
    ./sudoku_fetcher.py [url] [--letters] [--solution]
    
Examples:
    ./sudoku_fetcher.py                                       # Default (6x6)
    ./sudoku_fetcher.py https://www.sudokuonline.io/easy      # 9x9 Easy
    ./sudoku_fetcher.py https://www.sudokuonline.io/kids/letters-4-4 --letters
"""

import requests
import re
import random
import sys
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Default URL if none provided
DEFAULT_URL = "https://www.sudokuonline.io/kids/numbers-6-6"

# Repo-local helpers (avoid absolute paths; makes this portable)
REPO_ROOT = Path(__file__).resolve().parent
ENCODE_LZ_JS = REPO_ROOT / "encode_lz.js"
ENCODE_NATIVE_JS = REPO_ROOT / "encode_native.js"

def fetch_puzzles(url):
    """Fetch preloaded puzzles from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
    except Exception as e:
        print(f"Error fetching URL: {e}")
        sys.exit(1)
    
    # Extract the preloadedPuzzles array
    match = re.search(r'const preloadedPuzzles = \[(.*?)\];', html, re.DOTALL)
    if not match:
        print("Could not find preloadedPuzzles in HTML. Is this a valid sudokuonline.io page?")
        sys.exit(1)
    
    puzzles_str = match.group(1).strip()
    
    # Extract individual puzzle objects
    puzzles = []
    for puzzle_match in re.finditer(r"\{[^}]+\}", puzzles_str):
        puzzle_str = puzzle_match.group(0)
        # Convert JS object to JSON
        puzzle_str = puzzle_str.replace("'", '"').replace("false", "False").replace("true", "True")
        try:
            puzzle = eval(puzzle_str)
            puzzles.append(puzzle)
        except:
            continue
            
    return puzzles

def decode_puzzle(data):
    """
    Decode puzzle data into a grid.
    Returns: (size, clues_grid, solution_grid)
    """
    total_cells = len(data)
    size = int(math.sqrt(total_cells))
    
    if size * size != total_cells:
        raise ValueError(f"Invalid data length: {total_cells} (not a perfect square)")
        
    clues = [[0]*size for _ in range(size)]
    solution = [[0]*size for _ in range(size)]
    
    for i, val in enumerate(data):
        row, col = i // size, i % size
        if val > 100:
            digit = val - 100
            clues[row][col] = digit
            solution[row][col] = digit
        else:
            clues[row][col] = 0
            solution[row][col] = val
            
    return size, clues, solution

def get_block_dims(size):
    """Return (block_width, block_height) for a given grid size."""
    if size == 4:
        return 2, 2
    elif size == 6:
        return 3, 2  # 3 cols x 2 rows (standard for 6x6 "landscape" blocks)
    elif size == 9:
        return 3, 3
    else:
        # Fallback for weird sizes: assume sqrt
        root = int(math.sqrt(size))
        return root, size // root

def format_val(val, letters_mode):
    """Convert integer value to display string (Number or Letter)."""
    if val == 0:
        return ""
    if letters_mode:
        return chr(ord('A') + val - 1)
    return str(val)

import zlib
import base64
import json

def generate_scl_link(grid, size, title="Sudoku", author="Clawdbot"):
    """
    Generate a SudokuPad SCL link (native format).
    Pipeline: JSON -> Deflate -> Base64URL -> Strip Padding
    """
    # 1. Build SCL JSON object
    # Convert grid to "givens" string
    givens_str = ""
    for r in range(size):
        for c in range(size):
            val = grid[r][c]
            # Use dot for empty, as per standard SCL examples
            givens_str += str(val) if val != 0 else "."
            
    scl_obj = {
        "size": size,
        "givens": givens_str,
        "constraints": [], # Ensure constraints array exists
        "metadata": {
            "title": title,
            "author": author,
            "rules": "Normal Sudoku rules apply."
        }
    }

    # 2. Serialize to JSON (minimal separators)
    json_str = json.dumps(scl_obj, separators=(',', ':'))

    # 3. Compress (Raw Deflate)
    compressor = zlib.compressobj(level=9, wbits=-15)
    compressed = compressor.compress(json_str.encode('utf-8')) + compressor.flush()

    # 4. Base64 URL-safe encode
    b64 = base64.urlsafe_b64encode(compressed).decode('utf-8')

    # 5. Strip padding
    b64 = b64.rstrip("=")
    
    link = f"https://sudokupad.app/scl/{b64}"
    return link

import subprocess

def generate_puzzle_link(grid, size, title="Sudoku", author="Clawdbot"):
    """
    Generate a SudokuPad /puzzle/ link (LZString compressed).
    Uses SCL-style JSON payload but compressed with LZString.
    """
    # Build JSON (SCL style)
    givens_str = ""
    for r in range(size):
        for c in range(size):
            val = grid[r][c]
            givens_str += str(val) if val != 0 else "."
            
    scl_obj = {
        "size": size,
        "givens": givens_str,
        "metadata": {
            "title": title,
            "author": author
        }
    }
    json_str = json.dumps(scl_obj)
    
    # Compress using Node.js script (since python lzstring can be finicky)
    try:
        result = subprocess.run(
            ['node', str(ENCODE_LZ_JS), json_str],
            capture_output=True, text=True, check=True
        )
        compressed = result.stdout.strip()
        # Oliver prefers svencodes.com domain
        return f"https://sudokupad.svencodes.com/puzzle/{compressed}"
    except Exception as e:
        return f"Error generating puzzle link: {e}"

def generate_native_link(grid, size, title="Sudoku"):
    """
    Generate a *real* Sven SudokuPad `/puzzle/` share link for classic sudoku.

    Note: The `title` is embedded into the SudokuPad puzzle metadata (not the URL).

    This uses SudokuPad's compact classic codec (see `PuzzleTools.zipClassicSudoku2`):
    - Build an 81-char row-major string using digits and `0` for blanks
    - Encode to compact `p`
    - Wrap as JSON and LZString-compress (base64)

    Note: This is intended for classic 9x9 sudokus.
    """

    if size != 9:
        return "Native /puzzle/ classic format currently implemented for 9x9 only."

    puzzle81 = ''.join(str(grid[r][c]) if grid[r][c] else '0' for r in range(9) for c in range(9))

    try:
        result = subprocess.run(
            ['node', str(ENCODE_NATIVE_JS), puzzle81, title],
            capture_output=True,
            text=True,
            check=True,
        )
        payload = result.stdout.strip()
        # Payload is already URL-safe (EncodedURIComponent alphabet). Do not URL-encode.
        return f"https://sudokupad.svencodes.com/puzzle/{payload}"
    except Exception as e:
        return f"Error generating native link: {e}"

def generate_fpuzzles_link(grid, size, title="Sudoku", author="Clawdbot"):
    """
    Generate a SudokuPad link using F-Puzzles format (fallback).
    """
    # Create F-Puzzles JSON structure
    fpuzzles_obj = {
        "size": size,
        "grid": [],
        "info": {
            "title": title,
            "author": author
        }
    }

    # Populate grid
    for r in range(size):
        for c in range(size):
            val = grid[r][c]
            cell = {"col": c, "row": r}
            if val != 0:
                cell["value"] = val
                cell["given"] = True
            fpuzzles_obj["grid"].append(cell)

    # Convert to JSON string
    json_str = json.dumps(fpuzzles_obj)

    # Compress (Raw Deflate)
    compressor = zlib.compressobj(level=9, wbits=-15)
    compressed = compressor.compress(json_str.encode('utf-8')) + compressor.flush()

    # Base64 encode (standard, but SudokuPad accepts it)
    b64 = base64.b64encode(compressed).decode('utf-8')
    
    link = f"https://sudokupad.app/fpuzzles/{b64}"
    return link

# Render constants (used by both rendering and image cropping helpers)
RENDER_CELL_SIZE = 80
RENDER_OUTER_LINE_WIDTH = 4
# The grid starts at the image edge (no outer padding beyond the outer border).
RENDER_INSET = 0

# Print/PDF constants
A4_INCH_W = 8.27
A4_INCH_H = 11.69
A4_DPI_DEFAULT = 300


def render_sudoku(
    grid,
    size,
    filename="sudoku.png",
    title=None,
    extra_lines=None,
    extra_lines_right=None,
    original_clues=None,
    letters_mode=False,
):
    """Render the Sudoku grid.

    Rendering goals:
    - No outer padding outside the outermost grid lines.
    - The outer border should look like a single continuous rectangle (clean corners).

    Note: If a title or extra_lines are provided, they are rendered in an area *above* the grid.
    """

    cell_size = RENDER_CELL_SIZE
    outer_w = RENDER_OUTER_LINE_WIDTH

    # Calculate header height (supports left + right header blocks)
    left_h = 0
    if title:
        left_h += 30
    if extra_lines:
        left_h += len(extra_lines) * 20

    right_h = 0
    if extra_lines_right:
        right_h += len(extra_lines_right) * 20

    header_content_height = max(left_h, right_h)

    # Add some padding if we have a header
    header_height = header_content_height + 20 if header_content_height > 0 else 0

    board_size = cell_size * size

    # No padding outside the grid: the outer border sits at the image edge.
    # +1 because PIL coordinates are inclusive at the right/bottom edge.
    img_width = board_size + 1
    img_height = header_height + board_size + 1

    bg_color = (255, 255, 255)
    line_color = (0, 0, 0)
    text_color = (0, 0, 0)  # true black for givens/clues
    solution_color = (0, 100, 200)  # blue for filled-in (non-given) values

    img = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)

    # Load fonts
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        meta_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except Exception:
        font = ImageFont.load_default()
        title_font = font
        meta_font = font

    grid_left = RENDER_INSET
    grid_top = header_height + RENDER_INSET
    grid_right = grid_left + board_size
    grid_bottom = grid_top + board_size

    # Draw Header
    header_top = 15

    # Left block (title + optional extra lines)
    current_y = header_top
    if title:
        draw.text((grid_left, current_y), title, font=title_font, fill=(50, 50, 50))
        current_y += 30

    if extra_lines:
        for line in extra_lines:
            draw.text((grid_left, current_y), line, font=meta_font, fill=(100, 100, 100))
            current_y += 20

    # Right block (right-aligned)
    if extra_lines_right:
        ry = header_top
        for line in extra_lines_right:
            bbox = draw.textbbox((0, 0), line, font=meta_font)
            w = bbox[2] - bbox[0]
            x = grid_right - w
            draw.text((x, ry), line, font=meta_font, fill=(100, 100, 100))
            ry += 20

    # Outer border: draw as one rectangle so the corners look like a single stroke.
    draw.rectangle([grid_left, grid_top, grid_right, grid_bottom], outline=line_color, width=outer_w)

    # Get block dimensions
    bw, bh = get_block_dims(size)

    # Internal grid lines (skip outer border lines; those are handled by the rectangle above)
    for i in range(1, size):
        is_block_boundary = (i % bh == 0)
        width = 4 if is_block_boundary else 1
        y = grid_top + i * cell_size
        draw.line([(grid_left, y), (grid_right, y)], fill=line_color, width=width)

    for j in range(1, size):
        is_block_boundary = (j % bw == 0)
        width = 4 if is_block_boundary else 1
        x = grid_left + j * cell_size
        draw.line([(x, grid_top), (x, grid_bottom)], fill=line_color, width=width)

    # Draw content
    for row in range(size):
        for col in range(size):
            val = grid[row][col]
            if val != 0:
                text = format_val(val, letters_mode)

                # Center text within the cell
                x = grid_left + col * cell_size + cell_size // 2
                y = grid_top + row * cell_size + cell_size // 2

                bbox = draw.textbbox((0, 0), text, font=font)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]

                fill = text_color
                if original_clues and original_clues[row][col] == 0:
                    fill = solution_color

                draw.text((x - w / 2, y - h / 2 - 2), text, font=font, fill=fill)

    img.save(filename)
    return filename

def main():
    args = sys.argv[1:]
    url = DEFAULT_URL
    letters_mode = False
    show_solution = False
    
    # Parse simple args
    for arg in args:
        if arg == "--letters":
            letters_mode = True
        elif arg == "--solution":
            show_solution = True
        elif arg.startswith("http"):
            url = arg
            # Auto-detect letters mode from URL if not explicitly set
            if "letters" in url and "--letters" not in args:
                letters_mode = True

    print(f"Fetching from: {url}")
    puzzles = fetch_puzzles(url)
    print(f"Found {len(puzzles)} puzzles.")
    
    if not puzzles:
        print("No puzzles found.")
        return

    # Pick random puzzle
    puzzle = random.choice(puzzles)
    size, clues, solution = decode_puzzle(puzzle['data'])
    
    print(f"Selected Puzzle ID: {puzzle['id']}")
    print(f"Grid Size: {size}x{size}")
    if letters_mode:
        print("Mode: Letters")
        
    # Render
    filename = f"sudoku_{size}x{size}.png"
    render_sudoku(clues, size, filename, 
                  title=f"Sudoku {size}x{size} ({'Letters' if letters_mode else 'Numbers'})", 
                  letters_mode=letters_mode)
    print(f"Saved puzzle to {filename}")
    
    # Generate SudokuPad SCL link
    try:
        # Note: SCL handles custom sizes (like 4x4) gracefully usually
        if letters_mode:
            print("\nNote: For SudokuPad link, letters are mapped to numbers (A=1, B=2...).")
            
        link_scl = generate_scl_link(clues, size, title=f"Sudoku {size}x{size}")
        print(f"\n🔗 SudokuPad Link (SCL):\n{link_scl}")
        
        link_fp = generate_fpuzzles_link(clues, size, title=f"Sudoku {size}x{size}")
        print(f"\n🔗 SudokuPad Link (F-Puzzles Fallback):\n{link_fp}\n")
        
        short_id = str(puzzle['id']).split('-')[0]
        link_native = generate_native_link(clues, size, title=f"Sudoku {size}x{size} [{short_id}]")
        print(f"\n🔗 SudokuPad Link (Native Short Share):\n{link_native}\n")
    except Exception as e:
        print(f"Error generating link: {e}")
    
    if show_solution:
        sol_filename = f"sudoku_{size}x{size}_solution.png"
        render_sudoku(solution, size, sol_filename, 
                      title=f"Solution {size}x{size}", 
                      original_clues=clues,
                      letters_mode=letters_mode)
        print(f"Saved solution to {sol_filename}")

if __name__ == "__main__":
    main()
