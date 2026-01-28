#!/usr/bin/env python3
"""Compile fetched essays into EPUB with cover."""

import argparse
import json
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Compile essays to EPUB")
    parser.add_argument("--input", required=True, help="Input directory with essays/")
    parser.add_argument("--output", required=True, help="Output EPUB path")
    parser.add_argument("--cover", help="Cover image path (required!)")
    parser.add_argument("--title", help="Book title")
    parser.add_argument("--author", help="Author name")
    args = parser.parse_args()
    
    input_dir = Path(args.input)
    essays_dir = input_dir / "essays"
    
    if not essays_dir.exists():
        print(f"Error: essays directory not found at {essays_dir}")
        return 1
    
    # Load manifest for metadata
    manifest_path = input_dir / "manifest.json"
    if manifest_path.exists():
        with open(manifest_path) as f:
            manifest = json.load(f)
        site = manifest.get("site", "unknown")
    else:
        site = "unknown"
        manifest = {}
    
    # Determine title and author
    title = args.title or f"Essays from {site.title()}"
    author = args.author or site.title()
    
    # Get all markdown files sorted
    essay_files = sorted(essays_dir.glob("*.md"))
    print(f"Found {len(essay_files)} essays")
    
    if not essay_files:
        print("Error: No essays found")
        return 1
    
    # Combine into single markdown
    combined_path = input_dir / "combined.md"
    with open(combined_path, "w") as out:
        # YAML frontmatter
        out.write("---\n")
        out.write(f"title: {title}\n")
        out.write(f"author: {author}\n")
        out.write("lang: en\n")
        out.write("---\n\n")
        
        for i, essay_file in enumerate(essay_files):
            content = essay_file.read_text()
            if i > 0:
                out.write("\n\n---\n\n")  # Page break
            out.write(content)
            out.write("\n")
    
    print(f"Combined essays written to {combined_path}")
    
    # Build pandoc command
    cmd = [
        "pandoc",
        str(combined_path),
        "-o", args.output,
        "--toc",
        "--toc-depth=2",
        f"--metadata=title:{title}",
        f"--metadata=author:{author}",
    ]
    
    if args.cover:
        cover_path = Path(args.cover)
        if not cover_path.exists():
            print(f"Warning: Cover not found at {cover_path}")
            print("⚠️  Proceeding without cover - consider generating one!")
        else:
            cmd.append(f"--epub-cover-image={args.cover}")
            print(f"Using cover: {args.cover}")
    else:
        print("⚠️  No cover specified! Use --cover to add one.")
    
    print(f"Running pandoc...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"pandoc error: {result.stderr}")
        return 1
    
    output_path = Path(args.output)
    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"\n✅ EPUB created: {args.output} ({size_mb:.2f} MB)")
    print(f"   Title: {title}")
    print(f"   Author: {author}")
    print(f"   Essays: {len(essay_files)}")
    
    return 0


if __name__ == "__main__":
    exit(main())
