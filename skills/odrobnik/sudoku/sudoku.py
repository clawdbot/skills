#!/usr/bin/env python3
"""skills/sudoku/sudoku.py

Sudoku skill CLI.

Key design (per Oliver preference):
- **Puzzles are stored as individual JSON files** under the workspace `sudoku/puzzles/` folder.
- **Images are generated from JSON on demand** (no persistent state.json / history.jsonl).
- “Latest puzzle” = newest JSON in `sudoku/puzzles/`.

Data source: https://www.sudokuonline.io (pages embed a `preloadedPuzzles` array).

Commands:
  - list
  - get <preset> [--index N|--id ID|--seed S] [--render] [--json]
  - puzzle [--latest|--file PATH|--id ID] [--json]
  - reveal [--latest|--file PATH|--id ID] [--full|--box ...|--cell r c] [--image] [--json]

Notes:
- Only **Classic 9×9** puzzles produce a reliable SudokuPad share link.
- Reveal images render **givens in black** and **filled-in values in blue**.
"""

from __future__ import annotations

import argparse
import ast
import json
import math
import os
import random
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
from PIL import Image

# Import the existing render + link utilities.
REPO_ROOT = Path.cwd()
# sys.path.insert(0, str(REPO_ROOT))

from sudoku_fetcher import (  # type: ignore
    RENDER_CELL_SIZE,
    RENDER_INSET,
    decode_puzzle,
    generate_native_link,
    generate_scl_link,
    generate_fpuzzles_link,
    get_block_dims,
    render_sudoku,
)

from sudoku_print_render import render_sudoku_a4_pdf  # type: ignore


# Storage (workspace-local)
PUZZLES_DIR = REPO_ROOT / "sudoku" / "puzzles"
RENDERS_DIR = REPO_ROOT / "sudoku" / "renders"


@dataclass(frozen=True)
class Preset:
    key: str
    desc: str
    url: str
    letters: bool = False


PRESETS: Dict[str, Preset] = {
    # Kids
    "kids4n": Preset(
        key="kids4n",
        desc="Kids 4x4",
        url="https://www.sudokuonline.io/kids/numbers-4-4",
        letters=False,
    ),
    "kids4l": Preset(
        key="kids4l",
        desc="Kids 4x4 with Letters",
        url="https://www.sudokuonline.io/kids/letters-4-4",
        letters=True,
    ),
    "kids6": Preset(
        key="kids6",
        desc="Kids 6x6",
        url="https://www.sudokuonline.io/kids/numbers-6-6",
        letters=False,
    ),
    "kids6l": Preset(
        key="kids6l",
        desc="Kids 6x6 with Letters",
        url="https://www.sudokuonline.io/kids/letters-6-6",
        letters=True,
    ),

    # Classic 9x9
    "easy9": Preset(
        key="easy9",
        desc="Classic 9x9 (Easy)",
        url="https://www.sudokuonline.io/easy",
        letters=False,
    ),
    "medium9": Preset(
        key="medium9",
        desc="Classic 9x9 (Medium)",
        url="https://www.sudokuonline.io/medium",
        letters=False,
    ),
    "hard9": Preset(
        key="hard9",
        desc="Classic 9x9 (Hard)",
        url="https://www.sudokuonline.io/hard",
        letters=False,
    ),
    "evil9": Preset(
        key="evil9",
        desc="Classic 9x9 (Evil)",
        url="https://www.sudokuonline.io/evil",
        letters=False,
    ),
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%SZ")


def ensure_dirs() -> None:
    PUZZLES_DIR.mkdir(parents=True, exist_ok=True)
    RENDERS_DIR.mkdir(parents=True, exist_ok=True)


def parse_preloaded_puzzles(html: str) -> List[Dict[str, Any]]:
    m = re.search(r"const preloadedPuzzles = \[(.*?)\];", html, re.DOTALL)
    if not m:
        raise ValueError("Could not find preloadedPuzzles in HTML")

    blob = m.group(1)
    puzzles: List[Dict[str, Any]] = []

    # Entries are JS-ish object literals.
    for pm in re.finditer(r"\{[^}]+\}", blob):
        s = pm.group(0)
        s = re.sub(r"\btrue\b", "True", s)
        s = re.sub(r"\bfalse\b", "False", s)
        s = re.sub(r"\bnull\b", "None", s)
        try:
            obj = ast.literal_eval(s)
            if isinstance(obj, dict) and "id" in obj and "data" in obj:
                puzzles.append(obj)
        except Exception:
            continue

    return puzzles


def fetch_puzzles(url: str) -> List[Dict[str, Any]]:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return parse_preloaded_puzzles(r.text)


def pick_puzzle(
    puzzles: List[Dict[str, Any]],
    *,
    index: Optional[int] = None,
    puzzle_id: Optional[str] = None,
    seed: Optional[str] = None,
) -> Tuple[Dict[str, Any], int]:
    if not puzzles:
        raise ValueError("No puzzles found")

    if puzzle_id is not None:
        for i, p in enumerate(puzzles):
            if str(p.get("id")) == puzzle_id:
                return p, i
        raise ValueError(f"Puzzle id not found: {puzzle_id}")

    if index is not None:
        # 1-based index by default (friendlier). Allow 0 as explicit first element.
        i = 0 if index == 0 else (index - 1)
        if i < 0 or i >= len(puzzles):
            raise ValueError(f"index out of range: {index} (have {len(puzzles)} puzzles)")
        return puzzles[i], i

    rng = random.Random(seed)
    i = rng.randrange(len(puzzles))
    return puzzles[i], i


def format_cell_value(val: int, letters_mode: bool) -> str:
    if val == 0:
        return ""
    if letters_mode:
        return chr(ord("A") + val - 1)
    return str(val)


def puzzle_json_filename(stamp: str, preset_key: str, size: int, puzzle_id: str) -> str:
    short = puzzle_id.split("-")[0]
    return f"{stamp}_{preset_key}_{size}x{size}_{short}.json"


def write_puzzle_json(doc: Dict[str, Any]) -> Path:
    ensure_dirs()
    stamp = doc.get("created_utc") or utc_stamp()
    preset_key = doc.get("preset", {}).get("key", "preset")
    size = int(doc.get("size", 0) or 0)
    puzzle_id = str(doc.get("picked", {}).get("id", "unknown"))
    path = PUZZLES_DIR / puzzle_json_filename(str(stamp), str(preset_key), size, puzzle_id)
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def list_puzzle_jsons() -> List[Path]:
    ensure_dirs()
    return sorted(PUZZLES_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime)


def latest_puzzle_json() -> Path:
    files = list_puzzle_jsons()
    if not files:
        raise FileNotFoundError(f"No puzzles stored yet in {PUZZLES_DIR}")
    return files[-1]


def find_puzzle_json_by_short_id(short_id: str) -> Path:
    """Fast-path lookup by the short ID used in filenames (first UUID segment)."""
    ensure_dirs()
    matches = sorted(PUZZLES_DIR.glob(f"*_{short_id}.json"), key=lambda p: p.stat().st_mtime)
    if not matches:
        raise FileNotFoundError(f"No stored puzzle JSON found for short id={short_id}")
    return matches[-1]


def find_puzzle_json_by_id(puzzle_id: str) -> Path:
    """Find a stored puzzle by UUID.

    Accepts either:
    - full UUID (e.g. 324306f5-034d-4089-8723-56a8087fde14)
    - short ID (first segment, e.g. 324306f5) which is embedded in the filename

    Fast path: try filename match first; fallback: scan JSON contents.
    """

    sid = puzzle_id.split("-")[0]

    # Fast path: try filename glob using short-id suffix.
    candidates = sorted(PUZZLES_DIR.glob(f"*_{sid}.json"), key=lambda p: p.stat().st_mtime)
    if candidates:
        # If user gave only short id, just return latest match.
        if "-" not in puzzle_id:
            return candidates[-1]

        # If user gave full UUID, verify candidate content before returning.
        for p in reversed(candidates):
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
                if str(d.get("picked", {}).get("id")) == puzzle_id:
                    return p
            except Exception:
                continue

    # Slow path: scan all stored docs.
    files = list_puzzle_jsons()
    for p in reversed(files):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            if str(d.get("picked", {}).get("id")) == puzzle_id:
                return p
        except Exception:
            continue

    raise FileNotFoundError(f"No stored puzzle JSON found for id={puzzle_id}")


def load_puzzle_doc(*, file: Optional[str] = None, puzzle_id: Optional[str] = None, latest: bool = False) -> Tuple[Dict[str, Any], Path]:
    if sum(1 for x in (file is not None, puzzle_id is not None, latest) if x) > 1:
        raise SystemExit("Use only one of --file / --id / --latest")

    if file is not None:
        p = Path(file).expanduser()
        if not p.exists():
            raise FileNotFoundError(p)
    elif puzzle_id is not None:
        p = find_puzzle_json_by_id(puzzle_id)
    else:
        p = latest_puzzle_json()

    doc = json.loads(p.read_text(encoding="utf-8"))
    return doc, p


def render_paths(doc: Dict[str, Any], *, kind: str, ext: str = "png") -> Path:
    ensure_dirs()
    stamp = utc_stamp()
    preset_key = doc.get("preset", {}).get("key", "preset")
    size = int(doc.get("size", 0) or 0)
    puzzle_id_short = str(doc.get("picked", {}).get("id", "unknown")).split("-")[0]
    return RENDERS_DIR / f"{stamp}_{preset_key}_{size}x{size}_{puzzle_id_short}_{kind}.{ext}"


def _print_header(doc: Dict[str, Any]) -> Tuple[str, List[str]]:
    puzzle_id = str(doc.get("picked", {}).get("id", "unknown"))
    short_id = puzzle_id.split("-")[0]

    preset_key = str(doc.get("preset", {}).get("key", ""))
    size = int(doc.get("size", 0) or 0)
    letters_mode = bool(doc.get("preset", {}).get("letters", False))

    # Title conventions
    # - Kids: "Kids 6x6" (and optionally add Letters when needed)
    # - Classic: "Easy Classic" / "Medium Classic" / ...
    if preset_key.startswith("kids"):
        title = f"Kids {size}x{size}"
        if letters_mode:
            title += " Letters"
    else:
        difficulty = preset_key.replace("9", "").capitalize() or "Easy"
        title = f"{difficulty} Classic"

    right_lines = [short_id]
    return title, right_lines


def render_puzzle_image(doc: Dict[str, Any], *, printable: bool = False) -> Path:
    kind = "puzzle_print" if printable else "puzzle"
    out = render_paths(doc, kind=kind, ext="png")
    clues = doc["clues"]
    size = int(doc["size"])
    letters_mode = bool(doc.get("preset", {}).get("letters", False))

    if printable:
        title, right_lines = _print_header(doc)
        render_sudoku(
            clues,
            size,
            str(out),
            title=title,
            extra_lines=None,
            extra_lines_right=right_lines,
            letters_mode=letters_mode,
        )
    else:
        render_sudoku(clues, size, str(out), title=None, extra_lines=None, extra_lines_right=None, letters_mode=letters_mode)

    return out


def render_puzzle_pdf(doc: Dict[str, Any], *, printable: bool = True, dpi: int = 300) -> Path:
    kind = "puzzle_print" if printable else "puzzle"
    out = render_paths(doc, kind=kind, ext="pdf")
    clues = doc["clues"]
    size = int(doc["size"])
    letters_mode = bool(doc.get("preset", {}).get("letters", False))
    bw, bh = get_block_dims(size)

    title_left = None
    right_lines: List[str] = []
    if printable:
        title_left, right_lines = _print_header(doc)

    render_sudoku_a4_pdf(
        grid=clues,
        size=size,
        out_pdf=out,
        bw=bw,
        bh=bh,
        title_left=title_left,
        right_lines=right_lines,
        original_clues=None,
        letters_mode=letters_mode,
        dpi=dpi,
    )
    return out


def render_reveal_image(doc: Dict[str, Any], *, printable: bool = False) -> Path:
    """Render a styled solution image: givens black, filled-in values blue."""
    kind = "reveal_print" if printable else "reveal"
    out = render_paths(doc, kind=kind, ext="png")
    clues = doc["clues"]
    solution = doc["solution"]
    size = int(doc["size"])
    letters_mode = bool(doc.get("preset", {}).get("letters", False))

    if printable:
        title, right_lines = _print_header(doc)
        title = f"Solution: {title}"
        render_sudoku(
            solution,
            size,
            str(out),
            title=title,
            extra_lines=None,
            extra_lines_right=right_lines,
            original_clues=clues,
            letters_mode=letters_mode,
        )
    else:
        render_sudoku(solution, size, str(out), title=None, extra_lines=None, extra_lines_right=None, original_clues=clues, letters_mode=letters_mode)

    return out


def render_reveal_pdf(doc: Dict[str, Any], *, printable: bool = True, dpi: int = 300) -> Path:
    kind = "reveal_print" if printable else "reveal"
    out = render_paths(doc, kind=kind, ext="pdf")
    clues = doc["clues"]
    solution = doc["solution"]
    size = int(doc["size"])
    letters_mode = bool(doc.get("preset", {}).get("letters", False))
    bw, bh = get_block_dims(size)

    title_left = None
    right_lines: List[str] = []
    if printable:
        t, right_lines = _print_header(doc)
        title_left = f"Solution: {t}"

    render_sudoku_a4_pdf(
        grid=solution,
        size=size,
        out_pdf=out,
        bw=bw,
        bh=bh,
        title_left=title_left,
        right_lines=right_lines,
        original_clues=clues,
        letters_mode=letters_mode,
        dpi=dpi,
    )
    return out


def crop_box_image(
    image_path: Path,
    *,
    size: int,
    box_r: int,
    box_c: int,
    out_path: Path,
    margin: int = RENDER_INSET,
    cell_size: int = RENDER_CELL_SIZE,
) -> Path:
    bw, bh = get_block_dims(size)

    br0 = box_r - 1
    bc0 = box_c - 1

    left = margin
    top = margin

    x0 = left + (bc0 * bw) * cell_size
    y0 = top + (br0 * bh) * cell_size
    x1 = x0 + (bw * cell_size)
    y1 = y0 + (bh * cell_size)

    pad = 6

    img = Image.open(image_path)
    crop = img.crop((max(0, x0 - pad), max(0, y0 - pad), min(img.width, x1 + pad), min(img.height, y1 + pad)))
    crop.save(out_path)
    return out_path


def crop_cell_image(
    image_path: Path,
    *,
    r: int,
    c: int,
    out_path: Path,
    margin: int = RENDER_INSET,
    cell_size: int = RENDER_CELL_SIZE,
) -> Path:
    rr0 = r - 1
    cc0 = c - 1

    left = margin
    top = margin

    x0 = left + cc0 * cell_size
    y0 = top + rr0 * cell_size
    x1 = x0 + cell_size
    y1 = y0 + cell_size

    pad = 6

    img = Image.open(image_path)
    crop = img.crop((max(0, x0 - pad), max(0, y0 - pad), min(img.width, x1 + pad), min(img.height, y1 + pad)))
    crop.save(out_path)
    return out_path


def cmd_list(args: argparse.Namespace) -> int:
    items = []
    for key in sorted(PRESETS.keys()):
        p = PRESETS[key]
        items.append({"preset": p.key, "desc": p.desc, "letters": p.letters, "url": p.url})

    if args.json:
        print(json.dumps({"presets": items}, ensure_ascii=False))
    else:
        for it in items:
            print(f"- {it['preset']}: {it['desc']}\n  {it['url']}")

    return 0


def cmd_get(args: argparse.Namespace) -> int:
    if args.preset not in PRESETS:
        raise SystemExit(f"Unknown preset '{args.preset}'. Run: sudoku.py list")

    selector_count = sum(1 for x in (args.index is not None, args.id is not None, args.seed is not None) if x)
    if selector_count > 1:
        raise SystemExit("Use only one of --index / --id / --seed")

    preset = PRESETS[args.preset]

    puzzles = fetch_puzzles(preset.url)
    puzzle, picked_idx = pick_puzzle(puzzles, index=args.index, puzzle_id=args.id, seed=args.seed)

    size, clues, solution = decode_puzzle(puzzle["data"])

    stamp = utc_stamp()
    puzzle_id = str(puzzle["id"])

    # Share link: classic 9x9 only.
    share_kind = "none"
    share_link = None
    if size == 9:
        short_id = puzzle_id.split("-")[0]
        # Oliver preference: embedded SudokuPad metadata title format
        # "Easy Classic [ID]"
        difficulty = preset.key.replace("9", "").capitalize()  # easy/medium/hard/evil
        share_title = f"{difficulty} Classic [{short_id}]"

        # Use SudokuPad /puzzle/ links (required for SudokuPad app).
        # The payload is generated URL-safe so chat systems don't break it.
        share_link = generate_native_link(clues, size, title=share_title)
        if isinstance(share_link, str) and share_link.startswith("http"):
            share_kind = "native"
        else:
            share_kind = "none"
            share_link = None

    doc: Dict[str, Any] = {
        "version": 2,
        "created_utc": stamp,
        "preset": {"key": preset.key, "desc": preset.desc, "url": preset.url, "letters": preset.letters},
        "picked": {"id": puzzle_id, "index": picked_idx, "total": len(puzzles)},
        "size": size,
        "block": {"bw": get_block_dims(size)[0], "bh": get_block_dims(size)[1]},
        "clues": clues,
        "solution": solution,
        "share": {"kind": share_kind, "link": share_link},
    }

    json_path = write_puzzle_json(doc)

    payload: Dict[str, Any] = {
        "preset": preset.key,
        "desc": preset.desc,
        "puzzle_id": puzzle_id,
        "picked_index": picked_idx,
        "puzzle_count": len(puzzles),
        "size": size,
        "letters_mode": preset.letters,
        "puzzle_json": str(json_path),
        "share_kind": share_kind,
        "share_link": share_link,
    }

    if args.render:
        payload["puzzle_image"] = str(render_puzzle_image(doc, printable=False))

    if args.json:
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(f"Stored: {json_path}")
        if payload.get("puzzle_image"):
            print(f"Puzzle image: {payload['puzzle_image']}")
        if share_kind != "none":
            print(f"Share link ({share_kind}): {share_link}")

    return 0


def cmd_render(args: argparse.Namespace) -> int:
    doc, json_path = load_puzzle_doc(file=args.file, puzzle_id=args.id, latest=args.latest)

    if args.pdf:
        # PDF is primarily for printing; we include the small header by default.
        out_path = render_puzzle_pdf(doc, printable=True)
        out = {"puzzle_json": str(json_path), "puzzle_pdf": str(out_path)}
    else:
        img = render_puzzle_image(doc, printable=args.printable)
        out = {"puzzle_json": str(json_path), "puzzle_image": str(img)}

    if args.json:
        print(json.dumps(out, ensure_ascii=False))
    else:
        print(str(list(out.values())[-1]))
    return 0


def cmd_share(args: argparse.Namespace) -> int:
    doc, json_path = load_puzzle_doc(file=args.file, puzzle_id=args.id, latest=args.latest)
    
    clues = doc["clues"]
    size = int(doc["size"])
    puzzle_id = str(doc.get("picked", {}).get("id", "unknown"))
    short_id = puzzle_id.split("-")[0]
    
    preset_key = str(doc.get("preset", {}).get("key", ""))
    difficulty = preset_key.replace("9", "").capitalize() or "Easy"
    
    title = f"{difficulty} Classic [{short_id}]"
    
    link = None
    if args.type == "scl":
        link = generate_scl_link(clues, size, title=title)
    elif args.type == "fpuzzle":
        link = generate_fpuzzles_link(clues, size, title=title)
    else: # sudokupad
        if size == 9:
            link = generate_native_link(clues, size, title=title)
        else:
            link = generate_native_link(clues, size, title=title)
            if not link.startswith("http"):
                 link = generate_scl_link(clues, size, title=title)

    out = {"puzzle_json": str(json_path), "share_link": link, "type": args.type}
    
    if args.json:
        print(json.dumps(out, ensure_ascii=False))
    else:
        print(link)
    return 0


def cmd_reveal(args: argparse.Namespace) -> int:
    doc, json_path = load_puzzle_doc(file=args.file, puzzle_id=args.id, latest=args.latest)

    size = int(doc["size"])
    letters_mode = bool(doc.get("preset", {}).get("letters", False))

    # If nothing selected, default to full reveal image.
    want_full = bool(args.full) or (args.box is None and args.cell is None)

    if args.pdf and want_full:
        pdf = render_reveal_pdf(doc, printable=True)
        out = {"puzzle_json": str(json_path), "solution_pdf": str(pdf)}
        if args.json:
            print(json.dumps(out, ensure_ascii=False))
        else:
            print(str(pdf))
        return 0

    reveal_img = render_reveal_image(doc, printable=args.printable)

    if want_full:
        out = {"puzzle_json": str(json_path), "solution_image": str(reveal_img)}
        if args.json:
            print(json.dumps(out, ensure_ascii=False))
        else:
            print(str(reveal_img))
        return 0

    if args.box is not None:
        bw, bh = get_block_dims(size)
        boxes_per_row = size // bw
        boxes_per_col = size // bh
        total_boxes = boxes_per_row * boxes_per_col

        vals = args.box
        if len(vals) == 1:
            idx = vals[0]
            if not (1 <= idx <= total_boxes):
                raise ValueError(f"box index out of range: {idx} (1..{total_boxes})")
            box_r = (idx - 1) // boxes_per_row + 1
            box_c = (idx - 1) % boxes_per_row + 1
        elif len(vals) == 2:
            box_r, box_c = vals
            if not (1 <= box_r <= boxes_per_col and 1 <= box_c <= boxes_per_row):
                raise ValueError(
                    f"box row/col out of range: ({box_r},{box_c}); rows 1..{boxes_per_col}, cols 1..{boxes_per_row}"
                )
            idx = (box_r - 1) * boxes_per_row + box_c
        else:
            raise ValueError("--box expects either 1 value (index) or 2 values (row col)")

        out_path = render_paths(doc, kind=f"box_{idx}_r{box_r}_c{box_c}")
        crop_box_image(reveal_img, size=size, box_r=box_r, box_c=box_c, out_path=out_path)

        out = {"puzzle_json": str(json_path), "box": {"index": idx, "r": box_r, "c": box_c}, "image": str(out_path)}
        if args.json:
            print(json.dumps(out, ensure_ascii=False))
        else:
            print(str(out_path))
        return 0

    if args.cell is not None:
        r, c = args.cell
        if not (1 <= r <= size and 1 <= c <= size):
            raise ValueError(f"cell out of range: ({r},{c}) for size {size}")

        val = int(doc["solution"][r - 1][c - 1])
        text = format_cell_value(val, letters_mode)

        cell_img_path: Optional[Path] = None
        if args.image:
            cell_img_path = render_paths(doc, kind=f"cell_r{r}_c{c}")
            crop_cell_image(reveal_img, r=r, c=c, out_path=cell_img_path)

        if args.json:
            out: Dict[str, Any] = {"puzzle_json": str(json_path), "cell": {"r": r, "c": c}, "value": val, "text": text}
            if cell_img_path:
                out["image"] = str(cell_img_path)
            print(json.dumps(out, ensure_ascii=False))
        else:
            # requirement: output just the digit/letter
            print(text)
            if cell_img_path:
                print(str(cell_img_path))
        return 0

    raise SystemExit("Nothing to reveal")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="sudoku.py")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="List available presets")
    p_list.add_argument("--text", dest="json", action="store_false", help="Output text instead of JSON")
    p_list.set_defaults(json=True)
    p_list.set_defaults(func=cmd_list)

    p_get = sub.add_parser("get", help="Fetch a puzzle from a preset and store as JSON")
    p_get.add_argument("preset", help="Preset name (see: list)")
    p_get.add_argument("--index", type=int, help="Select puzzle by index (1-based; 0 allowed for first)")
    p_get.add_argument("--id", help="Select puzzle by UUID (full UUID from source)")
    p_get.add_argument("--seed", help="Deterministic random selection (string)")
    p_get.add_argument("--render", action="store_true", help="Also render the puzzle image now")
    p_get.add_argument("--text", dest="json", action="store_false", help="Output text instead of JSON")
    p_get.set_defaults(json=True)
    p_get.set_defaults(func=cmd_get)

    p_ren = sub.add_parser("render", help="Render puzzle image from stored JSON")
    g = p_ren.add_mutually_exclusive_group(required=False)
    g.add_argument("--latest", action="store_true", help="Use latest stored puzzle (default)")
    g.add_argument("--file", help="Path to a stored puzzle JSON")
    g.add_argument("--id", help="Puzzle ID (full UUID or short 8-char ID from filename)")
    p_ren.add_argument("--printable", action="store_true", help="Include small header (difficulty + short ID) for printout")
    p_ren.add_argument("--pdf", action="store_true", help="Render as A4 PDF (recommended for printing)")
    p_ren.add_argument("--text", dest="json", action="store_false", help="Output text instead of JSON")
    p_ren.set_defaults(json=True)
    p_ren.set_defaults(func=cmd_render)

    p_share = sub.add_parser("share", help="Generate share link")
    g_share = p_share.add_mutually_exclusive_group(required=False)
    g_share.add_argument("--latest", action="store_true", help="Use latest stored puzzle (default)")
    g_share.add_argument("--file", help="Path to a stored puzzle JSON")
    g_share.add_argument("--id", help="Puzzle ID (full UUID or short 8-char ID from filename)")
    p_share.add_argument("--type", choices=["sudokupad", "fpuzzle", "scl"], default="sudokupad", help="Link type")
    p_share.add_argument("--text", dest="json", action="store_false", help="Output text instead of JSON")
    p_share.set_defaults(json=True)
    p_share.set_defaults(func=cmd_share)

    p_rev = sub.add_parser("reveal", help="Reveal solution from stored JSON (full/box/cell)")
    g2 = p_rev.add_mutually_exclusive_group(required=False)
    g2.add_argument("--latest", action="store_true", help="Use latest stored puzzle (default)")
    g2.add_argument("--file", help="Path to a stored puzzle JSON")
    g2.add_argument("--id", help="Puzzle ID (full UUID or short 8-char ID from filename)")
    p_rev.add_argument("--printable", action="store_true", help="Include small header (difficulty + short ID) for printout")
    p_rev.add_argument("--pdf", action="store_true", help="Render as A4 PDF (recommended for printing)")

    sel = p_rev.add_mutually_exclusive_group(required=False)
    sel.add_argument("--full", action="store_true", help="Full solution image (default)")
    sel.add_argument("--box", type=int, nargs="+", help="Reveal a single box: '--box <idx>' or '--box <row> <col>' (1-based)")
    sel.add_argument("--cell", type=int, nargs=2, metavar=("ROW", "COL"), help="Reveal a single cell value: '--cell <row> <col>' (1-based)")

    p_rev.add_argument("--image", action="store_true", help="With --cell: also write a tiny 1-cell image")
    p_rev.add_argument("--text", dest="json", action="store_false", help="Output text instead of JSON")
    p_rev.set_defaults(json=True)
    p_rev.set_defaults(func=cmd_reveal)

    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
