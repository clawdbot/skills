"""A4 print rendering helpers for Sudoku.

Goal: create a print-friendly A4 PDF with safe margins (so printer non-printable edges
won't clip the outer border) and high DPI (so digits aren't pixelated).

Deliberately printer-agnostic.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class A4Spec:
    width_px: int
    height_px: int
    dpi: int
    margin_px: int
    header_top_px: int


def a4_spec(dpi: int = 300, margin_mm: float = 15.0, header_mm: float = 22.0) -> A4Spec:
    # A4 inches: 8.27 × 11.69
    width_px = int(round(8.27 * dpi))
    height_px = int(round(11.69 * dpi))

    mm_to_in = 1.0 / 25.4
    margin_px = int(round(margin_mm * mm_to_in * dpi))
    header_top_px = int(round(header_mm * mm_to_in * dpi))

    return A4Spec(width_px=width_px, height_px=height_px, dpi=dpi, margin_px=margin_px, header_top_px=header_top_px)


def _load_fonts(cell_size: int):
    # Digit font ~ 60% of cell
    digit_px = max(18, int(cell_size * 0.62))
    title_px = max(14, int(cell_size * 0.30))
    meta_px = max(12, int(cell_size * 0.22))

    try:
        digit = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", digit_px)
        title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", title_px)
        meta = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", meta_px)
    except Exception:
        digit = ImageFont.load_default()
        title = digit
        meta = digit

    return digit, title, meta


def render_sudoku_a4_pdf(
    *,
    grid: List[List[int]],
    size: int,
    out_pdf: Path,
    bw: int,
    bh: int,
    title_left: Optional[str] = None,
    right_lines: Optional[List[str]] = None,
    original_clues: Optional[List[List[int]]] = None,
    letters_mode: bool = False,
    dpi: int = 300,
) -> Path:
    spec = a4_spec(dpi=dpi)

    bg = (255, 255, 255)
    black = (0, 0, 0)
    gray = (100, 100, 100)
    blue = (0, 100, 200)

    img = Image.new("RGB", (spec.width_px, spec.height_px), bg)
    draw = ImageDraw.Draw(img)

    right_lines = right_lines or []

    # Consistent header block
    header_h = spec.header_top_px

    # Available area for the board (keep safe margins)
    avail_w = spec.width_px - 2 * spec.margin_px
    avail_h = spec.height_px - (spec.margin_px + header_h + spec.margin_px)

    cell_size = min(avail_w // size, avail_h // size)
    board_w = cell_size * size
    board_h = cell_size * size

    left = spec.margin_px + (avail_w - board_w) // 2
    top = spec.margin_px + header_h
    right = left + board_w
    bottom = top + board_h

    digit_font, title_font, meta_font = _load_fonts(cell_size)

    # Header left
    # Put header comfortably below the top edge so it matches typical A4 worksheet layouts.
    header_y = spec.margin_px
    if title_left:
        draw.text((spec.margin_px, header_y), title_left, font=title_font, fill=gray)

    # Header right (right-aligned)
    ry = header_y
    for line in right_lines:
        bbox = draw.textbbox((0, 0), line, font=meta_font)
        w = bbox[2] - bbox[0]
        x = spec.width_px - spec.margin_px - w
        draw.text((x, ry), line, font=meta_font, fill=gray)
        ry += int(meta_font.size * 1.35) if hasattr(meta_font, "size") else 20

    # Line widths scale with cell size
    outer_w = max(4, cell_size // 18)
    inner_w = max(2, cell_size // 55)
    block_w = max(3, cell_size // 28)

    # Outer border inside printable area
    draw.rectangle([left, top, right, bottom], outline=black, width=outer_w)

    # Internal grid lines
    for i in range(1, size):
        y = top + i * cell_size
        w = block_w if (i % bh == 0) else inner_w
        draw.line([(left, y), (right, y)], fill=black, width=w)

    for j in range(1, size):
        x = left + j * cell_size
        w = block_w if (j % bw == 0) else inner_w
        draw.line([(x, top), (x, bottom)], fill=black, width=w)

    def fmt(val: int) -> str:
        if val == 0:
            return ""
        if letters_mode:
            return chr(ord("A") + val - 1)
        return str(val)

    for r in range(size):
        for c in range(size):
            val = grid[r][c]
            if val == 0:
                continue
            text = fmt(val)

            cx = left + c * cell_size + cell_size // 2
            cy = top + r * cell_size + cell_size // 2

            bbox = draw.textbbox((0, 0), text, font=digit_font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]

            fill = black
            if original_clues is not None and original_clues[r][c] == 0:
                fill = blue

            draw.text((cx - tw / 2, cy - th / 2), text, font=digit_font, fill=fill)

    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_pdf, "PDF", resolution=float(dpi))
    return out_pdf
