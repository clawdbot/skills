#!/usr/bin/env python3
"""
Demo script showing how to use the SilverBullet MCP server programmatically.

This demonstrates direct usage of the server functions without MCP transport.
"""

import asyncio
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import (
    list_files,
    read_page,
    write_page,
    search_pages,
    ping_server,
    get_server_config,
    append_to_page,
    delete_page,
)


async def main():
    """Run demo of SilverBullet MCP tools."""
    base_url = os.environ.get("SILVERBULLET_URL", "http://localhost:3000")
    print(f"Using SilverBullet at: {base_url}\n")

    # 1. Check server status
    print("=" * 50)
    print("1. Checking server status...")
    print("=" * 50)
    result = await ping_server(base_url)
    print(result)
    print()

    # 2. Get server config
    print("=" * 50)
    print("2. Getting server configuration...")
    print("=" * 50)
    result = await get_server_config(base_url)
    print(result)
    print()

    # 3. List all files
    print("=" * 50)
    print("3. Listing all files...")
    print("=" * 50)
    result = await list_files(base_url)
    print(result[:500] + "..." if len(result) > 500 else result)
    print()

    # 4. Read index page
    print("=" * 50)
    print("4. Reading index.md...")
    print("=" * 50)
    result = await read_page("index.md", base_url)
    print(result[:500] + "..." if len(result) > 500 else result)
    print()

    # 5. Search for pages
    print("=" * 50)
    print("5. Searching for pages with 'index'...")
    print("=" * 50)
    result = await search_pages("index", base_url)
    print(result)
    print()

    # 6. Create a test page
    print("=" * 50)
    print("6. Creating test page...")
    print("=" * 50)
    test_content = """# MCP Test Page

This page was created by the SilverBullet MCP server demo.

## Features Tested

- [x] Server connectivity
- [x] File listing
- [x] Page reading
- [x] Page creation

---
*Generated automatically*
"""
    result = await write_page("mcp-test.md", test_content, base_url)
    print(result)
    print()

    # 7. Read it back
    print("=" * 50)
    print("7. Reading test page back...")
    print("=" * 50)
    result = await read_page("mcp-test.md", base_url)
    print(result)
    print()

    # 8. Append to the test page
    print("=" * 50)
    print("8. Appending to test page...")
    print("=" * 50)
    result = await append_to_page("mcp-test.md", "## Appendix\n\nThis was appended!", base_url)
    print(result)
    print()

    # 9. Clean up - delete test page
    print("=" * 50)
    print("9. Cleaning up - deleting test page...")
    print("=" * 50)
    result = await delete_page("mcp-test.md", base_url)
    print(result)
    print()

    print("=" * 50)
    print("Demo complete!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
