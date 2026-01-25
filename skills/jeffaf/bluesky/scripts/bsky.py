#!/usr/bin/env python3
"""Bluesky CLI - bird-like interface for Bluesky/AT Protocol"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from atproto import Client
except ImportError:
    print("Error: atproto not installed. Run: pip install atproto", file=sys.stderr)
    sys.exit(1)

CONFIG_PATH = Path.home() / ".config" / "bsky" / "config.json"

def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return {}

def save_config(config):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, indent=2))

def get_client():
    config = load_config()
    if not config.get("handle") or not config.get("app_password"):
        print("Not logged in. Run: bsky login --handle your.handle --password your-app-password", file=sys.stderr)
        sys.exit(1)
    
    client = Client()
    client.login(config["handle"], config["app_password"])
    return client

def cmd_login(args):
    config = {
        "handle": args.handle,
        "app_password": args.password
    }
    try:
        client = Client()
        client.login(args.handle, args.password)
        config["did"] = client.me.did
        save_config(config)
        print(f"Logged in as {args.handle} ({client.me.did})")
    except Exception as e:
        print(f"Login failed: {e}", file=sys.stderr)
        sys.exit(1)

def cmd_whoami(args):
    config = load_config()
    if config.get("handle"):
        client = get_client()
        print(f"Handle: {client.me.handle}")
        print(f"DID: {client.me.did}")
    else:
        print("Not logged in")

def cmd_timeline(args):
    client = get_client()
    response = client.get_timeline(limit=args.count)
    
    for item in response.feed:
        post = item.post
        author = post.author.handle
        text = post.record.text if hasattr(post.record, 'text') else ""
        created = post.record.created_at if hasattr(post.record, 'created_at') else ""
        likes = post.like_count or 0
        reposts = post.repost_count or 0
        replies = post.reply_count or 0
        
        try:
            dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
            time_str = dt.strftime("%b %d %H:%M")
        except:
            time_str = created[:16] if created else ""
        
        print(f"@{author} · {time_str}")
        print(f"  {text[:200]}")
        print(f"  ❤️ {likes}  🔁 {reposts}  💬 {replies}")
        print(f"  🔗 https://bsky.app/profile/{author}/post/{post.uri.split('/')[-1]}")
        print()

def cmd_post(args):
    client = get_client()
    response = client.send_post(text=args.text)
    uri = response.uri
    post_id = uri.split('/')[-1]
    print(f"Posted: https://bsky.app/profile/{client.me.handle}/post/{post_id}")

def cmd_profile(args):
    client = get_client()
    handle = args.handle.lstrip('@') if args.handle else client.me.handle
    
    profile = client.get_profile(handle)
    print(f"@{profile.handle}")
    print(f"  Name: {profile.display_name or '(none)'}")
    print(f"  Bio: {profile.description or '(none)'}")
    print(f"  Followers: {profile.followers_count}")
    print(f"  Following: {profile.follows_count}")
    print(f"  Posts: {profile.posts_count}")
    print(f"  DID: {profile.did}")

def cmd_search(args):
    client = get_client()
    response = client.app.bsky.feed.search_posts({"q": args.query, "limit": args.count})
    
    if not response.posts:
        print("No results found.")
        return
    
    for post in response.posts:
        author = post.author.handle
        text = post.record.text if hasattr(post.record, 'text') else ""
        likes = post.like_count or 0
        
        print(f"@{author}: {text[:150]}")
        print(f"  ❤️ {likes}  🔗 https://bsky.app/profile/{author}/post/{post.uri.split('/')[-1]}")
        print()

def cmd_notifications(args):
    client = get_client()
    response = client.app.bsky.notification.list_notifications({"limit": args.count})
    
    for notif in response.notifications:
        reason = notif.reason
        author = notif.author.handle
        time_str = notif.indexed_at[:16] if notif.indexed_at else ""
        
        icons = {
            "like": "❤️",
            "repost": "🔁",
            "follow": "👤",
            "reply": "💬",
            "mention": "📢",
            "quote": "💭"
        }
        icon = icons.get(reason, "•")
        
        if reason == "like":
            print(f"{icon} @{author} liked your post · {time_str}")
        elif reason == "repost":
            print(f"{icon} @{author} reposted · {time_str}")
        elif reason == "follow":
            print(f"{icon} @{author} followed you · {time_str}")
        elif reason == "reply":
            print(f"{icon} @{author} replied · {time_str}")
        elif reason == "mention":
            print(f"{icon} @{author} mentioned you · {time_str}")
        elif reason == "quote":
            print(f"{icon} @{author} quoted you · {time_str}")
        else:
            print(f"{icon} {reason} from @{author} · {time_str}")

def main():
    parser = argparse.ArgumentParser(description="Bluesky CLI")
    subparsers = parser.add_subparsers(dest="command")
    
    # login
    login_p = subparsers.add_parser("login", help="Login to Bluesky")
    login_p.add_argument("--handle", required=True, help="Your handle (e.g. user.bsky.social)")
    login_p.add_argument("--password", required=True, help="App password (not your main password)")
    
    # whoami
    subparsers.add_parser("whoami", help="Show current user")
    
    # timeline
    tl_p = subparsers.add_parser("timeline", aliases=["tl", "home"], help="Show home timeline")
    tl_p.add_argument("-n", "--count", type=int, default=10, help="Number of posts")
    
    # post
    post_p = subparsers.add_parser("post", aliases=["p"], help="Create a post")
    post_p.add_argument("text", help="Post text")
    
    # profile
    profile_p = subparsers.add_parser("profile", help="Show profile")
    profile_p.add_argument("handle", nargs="?", help="Handle to look up (default: self)")
    
    # search
    search_p = subparsers.add_parser("search", aliases=["s"], help="Search posts")
    search_p.add_argument("query", help="Search query")
    search_p.add_argument("-n", "--count", type=int, default=10, help="Number of results")
    
    # notifications
    notif_p = subparsers.add_parser("notifications", aliases=["notif", "n"], help="Show notifications")
    notif_p.add_argument("-n", "--count", type=int, default=20, help="Number of notifications")
    
    args = parser.parse_args()
    
    commands = {
        "login": cmd_login,
        "whoami": cmd_whoami,
        "timeline": cmd_timeline,
        "tl": cmd_timeline,
        "home": cmd_timeline,
        "post": cmd_post,
        "p": cmd_post,
        "profile": cmd_profile,
        "search": cmd_search,
        "s": cmd_search,
        "notifications": cmd_notifications,
        "notif": cmd_notifications,
        "n": cmd_notifications,
    }
    
    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
