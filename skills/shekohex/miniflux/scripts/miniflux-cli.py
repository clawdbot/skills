#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# dependencies = ["miniflux>=1.1.4"]
# ///

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional

import miniflux

VERSION = "1.0.0"

XDG_DATA_HOME = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
CONFIG_PATH = Path(XDG_DATA_HOME) / "miniflux" / "config.json"


def load_config() -> dict:
    config = {}
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            config = json.load(f)
    return config


def save_config(base_url: str, api_key: str):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump({"base_url": base_url, "api_key": api_key}, f, indent=2)


def create_client(args) -> miniflux.Client:
    config = load_config()
    base_url = args.url or os.environ.get("MINIFLUX_URL") or config.get("base_url")
    api_key = args.api_key or os.environ.get("MINIFLUX_API_KEY") or config.get("api_key")

    if not base_url:
        print("Error: Miniflux URL not configured.", file=sys.stderr)
        print("Set MINIFLUX_URL environment variable or use --url", file=sys.stderr)
        print(f"Config file: {CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)

    if not api_key:
        print("Error: Miniflux API key not configured.", file=sys.stderr)
        print("Set MINIFLUX_API_KEY environment variable or use --api-key", file=sys.stderr)
        print(f"Config file: {CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)

    if args.url or args.api_key:
        save_config(base_url, api_key)

    return miniflux.Client(base_url, api_key=api_key)


def strip_html(html: str) -> str:
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<[^>]+>", "", html)
    html = re.sub(r"\s+", " ", html)
    return html.strip()


def format_timestamp(ts: str) -> str:
    if not ts:
        return ""
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return ts


def truncate_content(content: str, limit: Optional[int], offset: int = 0, total_len: Optional[int] = None) -> str:
    if offset > 0:
        content = content[offset:]
    if limit and len(content) > limit:
        content = content[:limit]
        total = total_len or len(content)
        content = f"{content}\n\n[...truncated, total: {total} chars]"
    return content


def count_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", strip_html(text)))


def cmd_list(args):
    client = create_client(args)
    kwargs = {}
    if getattr(args, 'status', None):
        kwargs["status"] = args.status
    if getattr(args, 'feed', None):
        kwargs["feed_id"] = int(args.feed)
    if getattr(args, 'category', None):
        kwargs["category_id"] = int(args.category)
    if getattr(args, 'starred', None):
        kwargs["starred"] = True
    if getattr(args, 'search', None):
        kwargs["search"] = args.search
    if getattr(args, 'limit', None):
        kwargs["limit"] = int(args.limit)

    try:
        result = client.get_entries(**kwargs)
        entries = result.get("entries", [])

        if not entries:
            print("No articles found.", file=sys.stderr)
            sys.exit(0)

        if getattr(args, 'json', False):
            print(json.dumps(entries, indent=2))
        elif getattr(args, 'plain', False):
            for e in entries:
                print(f"{e['id']}\t{e.get('feed', {}).get('title', 'Unknown')}\t{e['title']}\t{e.get('url', '')}")
        else:
            for e in entries:
                feed_title = e.get("feed", {}).get("title", "Unknown")
                published = format_timestamp(e.get("published_at"))
                status = e.get("status", "unread")
                star = "*" if e.get("starred") else " "

                if getattr(args, 'brief', False):
                    print(f"{star} [{feed_title}] {e['title']}")
                elif getattr(args, 'summary', False):
                    content = strip_html(e.get("content", ""))
                    excerpt = content[:200] + "..." if len(content) > 200 else content
                    print(f"{star} [{feed_title}] {e['title']}")
                    print(f"  Published: {published}")
                    print(f"  {excerpt}")
                    print()
                else:
                    content = strip_html(e.get("content", ""))
                    content_limit = getattr(args, 'content_limit', None)
                    offset = getattr(args, 'offset', 0)
                    content = truncate_content(content, content_limit, offset)
                    print(f"{star} [{feed_title}] {e['title']}")
                    print(f"  Published: {published}")
                    print(f"  URL: {e.get('url', '')}")
                    print(f"  Status: {status}")
                    print()
                    print(content)
                    print()

    except miniflux.AccessUnauthorized:
        print("Error: Invalid API credentials.", file=sys.stderr)
        print("Check MINIFLUX_API_KEY environment variable or --api-key", file=sys.stderr)
        sys.exit(1)
    except miniflux.ClientError as e:
        print(f"Error: {e.get_error_reason()}", file=sys.stderr)
        sys.exit(1)


def cmd_get(args):
    client = create_client(args)

    try:
        entry = client.get_entry(args.entry_id)

        if args.json:
            print(json.dumps(entry, indent=2))
        elif args.plain:
            print(f"{entry['id']}\t{entry.get('feed', {}).get('title', 'Unknown')}\t{entry['title']}\t{entry.get('url', '')}")
        else:
            content_html = entry.get("content", "")
            content = strip_html(content_html)
            total_len = len(content)

            if args.limit or args.offset:
                content = truncate_content(content, args.limit, args.offset or 0, total_len)

            feed_title = entry.get("feed", {}).get("title", "Unknown")
            published = format_timestamp(entry.get("published_at"))
            author = entry.get("author", "")
            reading_time = entry.get("reading_time", 0)

            print(f"[{feed_title}] {entry['title']}")
            if author:
                print(f"  Author: {author}")
            print(f"  Published: {published}")
            print(f"  Reading time: {reading_time} min")
            print(f"  URL: {entry.get('url', '')}")
            print(f"  Status: {entry.get('status', 'unread')}")
            if args.limit or args.offset:
                print(f"  Content length: {total_len} chars")
            print()
            print(content)

    except miniflux.ResourceNotFound:
        print(f"Error: Article {args.entry_id} not found.", file=sys.stderr)
        print(f"Use '{os.path.basename(sys.argv[0])} list' to browse available articles.", file=sys.stderr)
        sys.exit(1)
    except miniflux.AccessUnauthorized:
        print("Error: Invalid API credentials.", file=sys.stderr)
        print("Check MINIFLUX_API_KEY environment variable or --api-key", file=sys.stderr)
        sys.exit(1)
    except miniflux.ClientError as e:
        print(f"Error: {e.get_error_reason()}", file=sys.stderr)
        sys.exit(1)


def cmd_mark_read(args):
    client = create_client(args)

    try:
        client.update_entries(args.entry_ids, "read")
        for eid in args.entry_ids:
            print(f"Marked article {eid} as read")
    except miniflux.AccessUnauthorized:
        print("Error: Invalid API credentials.", file=sys.stderr)
        sys.exit(1)
    except miniflux.ClientError as e:
        print(f"Error: {e.get_error_reason()}", file=sys.stderr)
        sys.exit(1)


def cmd_mark_unread(args):
    client = create_client(args)

    try:
        client.update_entries(args.entry_ids, "unread")
        for eid in args.entry_ids:
            print(f"Marked article {eid} as unread")
    except miniflux.AccessUnauthorized:
        print("Error: Invalid API credentials.", file=sys.stderr)
        sys.exit(1)
    except miniflux.ClientError as e:
        print(f"Error: {e.get_error_reason()}", file=sys.stderr)
        sys.exit(1)


def cmd_feeds(args):
    client = create_client(args)

    try:
        feeds = client.get_feeds()

        if args.json:
            print(json.dumps(feeds, indent=2))
        else:
            for f in feeds:
                category = f.get("category", {}).get("title", "Uncategorized")
                print(f"[{category}] {f['title']}")
                print(f"  URL: {f.get('feed_url', '')}")
                print(f"  Site: {f.get('site_url', '')}")
                print()

    except miniflux.ClientError as e:
        print(f"Error: {e.get_error_reason()}", file=sys.stderr)
        sys.exit(1)


def cmd_categories(args):
    client = create_client(args)

    try:
        categories = client.get_categories()

        if args.json:
            print(json.dumps(categories, indent=2))
        else:
            for c in categories:
                print(f"{c['id']}: {c['title']}")

    except miniflux.ClientError as e:
        print(f"Error: {e.get_error_reason()}", file=sys.stderr)
        sys.exit(1)


def cmd_stats(args):
    client = create_client(args)

    try:
        if args.entry_id:
            entry = client.get_entry(args.entry_id)
            content = strip_html(entry.get("content", ""))
            words = count_words(content)
            chars = len(content)
            reading_time = entry.get("reading_time", 0)
            print(f"Article {args.entry_id} statistics:")
            print(f"  Words: {words}")
            print(f"  Characters: {chars}")
            print(f"  Estimated reading time: {reading_time} min")
        else:
            counters = client.get_feed_counters()
            print("Unread counts per feed:")
            for feed_id, count in counters.get("unreads", {}).items():
                print(f"  Feed {feed_id}: {count} unread")

    except miniflux.ResourceNotFound:
        print(f"Error: Article {args.entry_id} not found.", file=sys.stderr)
        sys.exit(1)
    except miniflux.ClientError as e:
        print(f"Error: {e.get_error_reason()}", file=sys.stderr)
        sys.exit(1)


def cmd_refresh(args):
    client = create_client(args)

    try:
        if args.all:
            client.refresh_all_feeds()
            print("Refreshed all feeds")
        elif args.feed:
            client.refresh_feed(int(args.feed))
            print(f"Refreshed feed {args.feed}")
        else:
            print("Error: Specify --all or --feed=ID", file=sys.stderr)
            sys.exit(1)
    except miniflux.ClientError as e:
        print(f"Error: {e.get_error_reason()}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Miniflux feed reader CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List unread articles
  miniflux-cli.py list --status=unread

  # Get article details
  miniflux-cli.py get 123

  # List with brief output
  miniflux-cli.py list --brief

  # Mark articles as read
  miniflux-cli.py mark-read 123 456

  # Show article statistics
  miniflux-cli.py stats --entry-id=123

Configuration:
  Precedence: Flags → Environment variables → Config file
  Environment: MINIFLUX_URL, MINIFLUX_API_KEY
  Config file: ~/.local/share/miniflux/config.json

For more help on a subcommand:
  miniflux-cli.py <subcommand> --help
        """
    )

    parser.add_argument("-v", "--version", action="version", version=f"miniflux-cli.py {VERSION}")
    parser.add_argument("-q", "--quiet", action="store_true", help="suppress non-error output")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug output")
    parser.add_argument("--no-color", action="store_true", help="disable colored output")
    parser.add_argument("--url", help="Miniflux server URL")
    parser.add_argument("--api-key", help="Miniflux API key")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list command
    list_parser = subparsers.add_parser("list", help="List articles", formatter_class=argparse.RawDescriptionHelpFormatter,
                                        epilog="""
Examples:
  miniflux-cli.py list --status=unread --brief
  miniflux-cli.py list --feed=42 --summary
  miniflux-cli.py list --search="python" --limit=10
                                        """)
    list_parser.add_argument("--status", choices=["read", "unread", "removed"], help="filter by status")
    list_parser.add_argument("--feed", help="filter by feed ID")
    list_parser.add_argument("--category", help="filter by category ID")
    list_parser.add_argument("--starred", action="store_true", help="show only starred")
    list_parser.add_argument("--search", help="search query")
    list_parser.add_argument("--limit", help="max number of entries")
    list_parser.add_argument("--offset", type=int, default=0, help="skip first N chars in content")
    list_parser.add_argument("--content-limit", type=int, help="max characters per article")
    list_parser.add_argument("-b", "--brief", action="store_true", help="brief output (titles only)")
    list_parser.add_argument("-s", "--summary", action="store_true", help="summary output (titles + excerpt)")
    list_parser.add_argument("-f", "--full", action="store_true", help="full article content (default)")
    list_parser.add_argument("--json", action="store_true", help="output as JSON")
    list_parser.add_argument("--plain", action="store_true", help="plain text output (one per line)")

    # get command
    get_parser = subparsers.add_parser("get", help="Get single article by ID", formatter_class=argparse.RawDescriptionHelpFormatter,
                                       epilog="""
Examples:
  miniflux-cli.py get 123
  miniflux-cli.py get 123 --limit=2000
  miniflux-cli.py get 123 --offset=1000 --limit=1000
                                       """)
    get_parser.add_argument("entry_id", help="article ID")
    get_parser.add_argument("--limit", type=int, help="max characters to return")
    get_parser.add_argument("--offset", type=int, default=0, help="skip first N chars")
    get_parser.add_argument("-f", "--full", action="store_true", help="full article content (default)")
    get_parser.add_argument("--json", action="store_true", help="output as JSON")
    get_parser.add_argument("--plain", action="store_true", help="plain text output")

    # mark-read command
    mr_parser = subparsers.add_parser("mark-read", help="Mark article(s) as read", formatter_class=argparse.RawDescriptionHelpFormatter,
                                      epilog="""
Examples:
  miniflux-cli.py mark-read 123
  miniflux-cli.py mark-read 123 456 789
                                      """)
    mr_parser.add_argument("entry_ids", nargs="+", type=int, help="article ID(s) to mark as read")

    # mark-unread command
    mu_parser = subparsers.add_parser("mark-unread", help="Mark article(s) as unread", formatter_class=argparse.RawDescriptionHelpFormatter,
                                      epilog="""
Examples:
  miniflux-cli.py mark-unread 123
  miniflux-cli.py mark-unread 123 456
                                      """)
    mu_parser.add_argument("entry_ids", nargs="+", type=int, help="article ID(s) to mark as unread")

    # feeds command
    feeds_parser = subparsers.add_parser("feeds", help="List all feeds", formatter_class=argparse.RawDescriptionHelpFormatter,
                                         epilog="""
Examples:
  miniflux-cli.py feeds
  miniflux-cli.py feeds --json
                                         """)
    feeds_parser.add_argument("--json", action="store_true", help="output as JSON")

    # categories command
    cat_parser = subparsers.add_parser("categories", help="List all categories", formatter_class=argparse.RawDescriptionHelpFormatter,
                                       epilog="""
Examples:
  miniflux-cli.py categories
                                       """)
    cat_parser.add_argument("--json", action="store_true", help="output as JSON")

    # stats command
    stats_parser = subparsers.add_parser("stats", help="Show statistics", formatter_class=argparse.RawDescriptionHelpFormatter,
                                         epilog="""
Examples:
  miniflux-cli.py stats --entry-id=123
  miniflux-cli.py stats
                                         """)
    stats_parser.add_argument("--entry-id", type=int, help="show stats for specific article")

    # refresh command
    refresh_parser = subparsers.add_parser("refresh", help="Refresh feeds", formatter_class=argparse.RawDescriptionHelpFormatter,
                                           epilog="""
Examples:
  miniflux-cli.py refresh --all
  miniflux-cli.py refresh --feed=42
                                           """)
    refresh_parser.add_argument("--all", action="store_true", help="refresh all feeds")
    refresh_parser.add_argument("--feed", help="refresh specific feed by ID")

    # search command (alias for list --search)
    search_parser = subparsers.add_parser("search", help="Search articles", formatter_class=argparse.RawDescriptionHelpFormatter,
                                          epilog="""
Examples:
  miniflux-cli.py search "python"
  miniflux-cli.py search "ai" --status=unread --brief
                                          """)
    search_parser.add_argument("query", help="search query")
    search_parser.add_argument("--status", choices=["read", "unread", "removed"], help="filter by status")
    search_parser.add_argument("--feed", help="filter by feed ID")
    search_parser.add_argument("--limit", help="max number of entries")
    search_parser.add_argument("-b", "--brief", action="store_true", help="brief output (titles only)")
    search_parser.add_argument("-s", "--summary", action="store_true", help="summary output")
    search_parser.add_argument("--json", action="store_true", help="output as JSON")
    search_parser.add_argument("--plain", action="store_true", help="plain text output")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "search":
        args.search = args.query
        args.command = "list"

    commands = {
        "list": cmd_list,
        "get": cmd_get,
        "mark-read": cmd_mark_read,
        "mark-unread": cmd_mark_unread,
        "feeds": cmd_feeds,
        "categories": cmd_categories,
        "stats": cmd_stats,
        "refresh": cmd_refresh,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
