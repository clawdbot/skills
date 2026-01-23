#!/usr/bin/env python3
"""
Oura Data Management CLI

Manage local data storage, export, and cleanup.

Usage:
    python oura_data.py info                          # Show storage info
    python oura_data.py export --output backup.json   # Export all data
    python oura_data.py export-events --output events.csv --format csv
    python oura_data.py clear-cache --confirm         # Clear cache
    python oura_data.py clear-all --confirm           # Clear all data
    python oura_data.py cleanup --days 90             # Delete cache older than 90 days
"""

import argparse
import json
import sys
from pathlib import Path
from data_manager import OuraDataManager, format_size


def main():
    parser = argparse.ArgumentParser(description="Oura Data Management")
    parser.add_argument("command", choices=[
        "info", "export", "export-events", 
        "clear-cache", "clear-events", "clear-all",
        "cleanup"
    ], help="Data management command")
    
    # Common args
    parser.add_argument("--data-dir", type=Path, help="Data directory (default: ~/.oura-analytics)")
    parser.add_argument("--confirm", action="store_true", help="Confirm destructive operations")
    
    # Export args
    parser.add_argument("--output", type=Path, help="Output file path")
    parser.add_argument("--format", choices=["json", "csv", "tar.gz"], default="json", help="Export format")
    
    # Clear cache args
    parser.add_argument("--endpoint", choices=["sleep", "daily_readiness", "daily_activity"], 
                       help="Specific endpoint to clear")
    
    # Cleanup args
    parser.add_argument("--days", type=int, default=90, help="Delete cache older than N days")
    
    args = parser.parse_args()
    
    # Initialize data manager
    manager = OuraDataManager(args.data_dir)
    
    try:
        if args.command == "info":
            info = manager.get_storage_info()
            
            print(f"Data directory: {info['data_dir']}")
            print(f"Total size: {format_size(info['total_size_bytes'])}\n")
            
            print("Cache:")
            print(f"  Size: {format_size(info['cache']['size_bytes'])}")
            print(f"  Files: {info['cache']['file_count']}")
            for endpoint, data in info['cache']['endpoints'].items():
                print(f"  {endpoint}:")
                print(f"    Files: {data['file_count']}")
                print(f"    Size: {format_size(data['size_bytes'])}")
                print(f"    Date range: {data['oldest_date']} to {data['newest_date']}")
            
            print(f"\nEvents:")
            print(f"  Exists: {info['events']['exists']}")
            if info['events']['exists']:
                print(f"  Size: {format_size(info['events']['size_bytes'])}")
                print(f"  Count: {info['events']['count']}")
            
            print(f"\nConfig:")
            print(f"  Exists: {info['config']['exists']}")
            if info['config']['exists']:
                print(f"  Size: {format_size(info['config']['size_bytes'])}")
            
            print(f"\nAlert state:")
            print(f"  Exists: {info['alert_state']['exists']}")
            if info['alert_state']['exists']:
                print(f"  Size: {format_size(info['alert_state']['size_bytes'])}")
        
        elif args.command == "export":
            if not args.output:
                print("ERROR: --output required for export", file=sys.stderr)
                sys.exit(1)
            manager.export_data(args.output, format=args.format)
        
        elif args.command == "export-events":
            if not args.output:
                print("ERROR: --output required for export-events", file=sys.stderr)
                sys.exit(1)
            manager.export_events(args.output, format=args.format)
        
        elif args.command == "clear-cache":
            manager.clear_cache(endpoint=args.endpoint, confirm=args.confirm)
        
        elif args.command == "clear-events":
            manager.clear_events(confirm=args.confirm)
        
        elif args.command == "clear-all":
            manager.clear_all(confirm=args.confirm)
        
        elif args.command == "cleanup":
            manager.cleanup_old_cache(days=args.days)
    
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
