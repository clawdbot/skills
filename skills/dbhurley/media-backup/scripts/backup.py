# /// script
# requires-python = ">=3.11"
# dependencies = ["click>=8.0.0"]
# ///
"""Backup Clawdbot media to a local folder (synced by Dropbox/iCloud/etc)."""

import os
import sys
import json
import hashlib
import shutil
from pathlib import Path
from datetime import datetime

import click

# Defaults
DEFAULT_SOURCE = Path.home() / ".clawdbot" / "media" / "inbound"
DEFAULT_DEST = Path.home() / "Dropbox" / "Clawdbot" / "media"
STATE_FILE = Path.home() / ".clawdbot" / "media" / "backup-state.json"

MEDIA_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.heic',
    '.mp4', '.mov', '.m4v', '.webm'
}


def get_dest_path() -> Path:
    """Get destination from env or default."""
    env_dest = os.environ.get("MEDIA_BACKUP_DEST")
    if env_dest:
        return Path(env_dest).expanduser()
    return DEFAULT_DEST


def load_state() -> set:
    """Load set of already-archived file hashes."""
    if STATE_FILE.exists():
        try:
            return set(json.loads(STATE_FILE.read_text()))
        except:
            return set()
    return set()


def save_state(hashes: set):
    """Save archived file hashes."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(list(hashes)))


def file_hash(path: Path) -> str:
    """Get MD5 hash of file content."""
    return hashlib.md5(path.read_bytes()).hexdigest()


@click.group(invoke_without_command=True)
@click.option("--source", "-s", type=click.Path(exists=True), help="Source directory")
@click.option("--dest", "-d", type=click.Path(), help="Destination directory")
@click.option("--dry-run", is_flag=True, help="Preview only, don't copy")
@click.pass_context
def cli(ctx, source, dest, dry_run):
    """Backup Clawdbot media to a local folder."""
    if ctx.invoked_subcommand is None:
        # Default action: run backup
        run_backup(source, dest, dry_run)


def run_backup(source, dest, dry_run):
    """Run the backup."""
    source_path = Path(source) if source else DEFAULT_SOURCE
    dest_path = Path(dest) if dest else get_dest_path()
    
    if not source_path.exists():
        click.echo(f"Source not found: {source_path}", err=True)
        sys.exit(1)
    
    # Load state
    archived = load_state()
    
    # Stats
    copied = 0
    skipped = 0
    errors = 0
    
    # Process files
    for file in source_path.iterdir():
        if not file.is_file():
            continue
        
        # Check extension
        if file.suffix.lower() not in MEDIA_EXTENSIONS:
            continue
        
        # Check if already archived
        fhash = file_hash(file)
        if fhash in archived:
            skipped += 1
            continue
        
        # Get date folder from file mtime
        mtime = datetime.fromtimestamp(file.stat().st_mtime)
        date_folder = mtime.strftime("%Y-%m-%d")
        
        # Destination path
        dest_dir = dest_path / date_folder
        dest_file = dest_dir / file.name
        
        if dry_run:
            click.echo(f"Would copy: {file.name} → {dest_dir}/")
            copied += 1
            continue
        
        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, dest_file)
            archived.add(fhash)
            copied += 1
            click.echo(f"✓ {file.name} → {date_folder}/")
        except Exception as e:
            click.echo(f"✗ {file.name}: {e}", err=True)
            errors += 1
    
    # Save state
    if not dry_run and copied > 0:
        save_state(archived)
    
    # Summary
    click.echo(f"\n📸 Copied: {copied}, Skipped: {skipped}, Errors: {errors}")
    
    if dry_run:
        click.echo(f"Destination: {dest_path}")


@cli.command()
def status():
    """Show backup status."""
    source_path = DEFAULT_SOURCE
    dest_path = get_dest_path()
    archived = load_state()
    
    click.echo(f"📂 Source: {source_path}")
    click.echo(f"📁 Destination: {dest_path}")
    click.echo(f"✓ Archived: {len(archived)} files")
    
    # Count pending
    if source_path.exists():
        pending = 0
        for file in source_path.iterdir():
            if file.is_file() and file.suffix.lower() in MEDIA_EXTENSIONS:
                if file_hash(file) not in archived:
                    pending += 1
        click.echo(f"⏳ Pending: {pending} files")
    
    # Check dest exists
    if dest_path.exists():
        click.echo(f"🔗 Destination exists: ✓")
    else:
        click.echo(f"🔗 Destination exists: ✗ (will be created)")


@cli.command()
def reset():
    """Reset backup state (re-archive all files)."""
    if STATE_FILE.exists():
        STATE_FILE.unlink()
        click.echo("✓ State reset. Next backup will re-process all files.")
    else:
        click.echo("No state file found.")


if __name__ == "__main__":
    cli()
