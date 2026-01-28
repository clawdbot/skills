#!/usr/bin/env python3
"""
Reddit Scraper - Read and search Reddit posts via Reddit's public JSON API (no API key needed)
"""

import argparse
import json
import sys
from datetime import datetime
import time

try:
    import requests
except ImportError:
    print("Error: Missing requests library")
    print("Install with: apt-get install python3-requests")
    sys.exit(1)


class RedditScraper:
    BASE_URL = "https://www.reddit.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Clawdbot/1.0 (Reddit Reader; +https://github.com/clawdbot)'
        })

    def get_subreddit_posts(self, subreddit, sort='top', limit=25, time_filter='day'):
        """Fetch posts from a subreddit using JSON API"""
        sort_map = {
            'hot': 'hot',
            'new': 'new',
            'top': 'top',
            'populares': 'top',
            'nuevos': 'new',
            'rising': 'rising',
        }
        
        sort_param = sort_map.get(sort, 'top')
        url = f"{self.BASE_URL}/r/{subreddit}/{sort_param}.json"
        
        params = {'limit': limit}
        if sort_param == 'top':
            params['t'] = time_filter  # hour, day, week, month, year, all
            
        return self._fetch_json(url, params)

    def search_posts(self, query, subreddit=None, limit=25, sort='relevance', time_filter='all'):
        """Search for posts using JSON API"""
        if subreddit:
            url = f"{self.BASE_URL}/r/{subreddit}/search.json"
            params = {
                'q': query,
                'restrict_sr': 'on',
                'limit': limit,
                'sort': sort,
                't': time_filter
            }
        else:
            url = f"{self.BASE_URL}/search.json"
            params = {
                'q': query,
                'limit': limit,
                'sort': sort,
                't': time_filter
            }
            
        return self._fetch_json(url, params)

    def _fetch_json(self, url, params=None):
        """Fetch and parse posts from Reddit JSON API"""
        all_posts = []

        try:
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            # Handle different response formats
            if 'data' in data and 'children' in data['data']:
                children = data['data']['children']
            else:
                return all_posts
                
            for child in children:
                if child.get('kind') == 't3':  # t3 = link/post
                    post_data = child.get('data', {})
                    post = self._parse_post(post_data)
                    if post:
                        all_posts.append(post)

        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}", file=sys.stderr)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}", file=sys.stderr)

        return all_posts

    def _parse_post(self, data):
        """Extract relevant fields from post data"""
        try:
            # Skip promoted posts
            if data.get('promoted', False):
                return None
            
            # Get selftext (no truncation)
            selftext = data.get('selftext', '') or ''
                
            # Build short URL using redd.it
            post_id = data.get('id', '')
            short_url = f"https://redd.it/{post_id}" if post_id else f"https://reddit.com{data.get('permalink', '')}"
            
            return {
                'title': data.get('title', ''),
                'author': data.get('author', '[deleted]'),
                'score': data.get('score', 0),
                'num_comments': data.get('num_comments', 0),
                'url': short_url,
                'subreddit': data.get('subreddit', ''),
                'created_utc': int(data.get('created_utc', time.time())),
                'flair': data.get('link_flair_text', ''),
                'selftext': selftext,
                'is_self': data.get('is_self', False),
                'upvote_ratio': data.get('upvote_ratio', 0),
            }
        except Exception as e:
            print(f"Error parsing post: {e}", file=sys.stderr)
            return None


def format_posts(posts, as_json=False, verbose=False):
    """Format and display posts"""
    if not posts:
        print("No posts found.")
        return

    if as_json:
        print(json.dumps(posts, indent=2))
    else:
        for i, post in enumerate(posts, 1):
            created = datetime.fromtimestamp(post.get('created_utc', 0)).strftime('%Y-%m-%d %H:%M')
            subreddit = post.get('subreddit', 'unknown')
            author = post.get('author', 'unknown')
            ratio = post.get('upvote_ratio', 0)
            flair = post.get('flair', '')
            
            # Title with flair
            title = post.get('title', 'N/A')
            if flair:
                print(f"\n{i}. [{flair}] {title}")
            else:
                print(f"\n{i}. {title}")
                
            print(f"   r/{subreddit}")
            print(f"   🔼 {post.get('score', 0)} ({int(ratio*100)}%) • 💬 {post.get('num_comments', 0)} • {created}")
            
            # Always show post URL (permalink)
            print(f"   {post.get('url', '')}")
                
            # Show selftext summary if available
            selftext = post.get('selftext', '')
            if selftext:
                preview = selftext.replace('\n', ' ').strip()
                if preview:
                    print(f"   📝 {preview}")


def main():
    parser = argparse.ArgumentParser(description='Reddit Scraper - Read and search Reddit posts (JSON API)')
    parser.add_argument('--subreddit', '-s', help='Subreddit name (without r/)')
    parser.add_argument('--search', '-q', help='Search query')
    parser.add_argument('--sort', choices=['hot', 'new', 'top', 'populares', 'nuevos', 'rising'], default='top',
                    help='Sort order (default: top)')
    parser.add_argument('--time', '-t', choices=['hour', 'day', 'week', 'month', 'year', 'all'], default='day',
                    help='Time filter for top/search (default: day)')
    parser.add_argument('--limit', '-n', type=int, default=25,
                    help='Number of posts to fetch (default: 25)')
    parser.add_argument('--json', '-j', action='store_true',
                    help='Output as JSON')
    parser.add_argument('--verbose', '-v', action='store_true',
                    help='Show post preview text')

    args = parser.parse_args()

    scraper = RedditScraper()

    if args.search:
        posts = scraper.search_posts(args.search, args.subreddit, args.limit, 
                                     sort='relevance' if args.sort == 'top' else args.sort,
                                     time_filter=args.time)
        format_posts(posts, args.json, args.verbose)
    elif args.subreddit:
        posts = scraper.get_subreddit_posts(args.subreddit, args.sort, args.limit, args.time)
        format_posts(posts, args.json, args.verbose)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
