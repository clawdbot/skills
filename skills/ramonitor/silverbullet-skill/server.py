#!/usr/bin/env python3
"""
SilverBullet MCP Server

An MCP server that provides tools for interacting with SilverBullet
note-taking app via its REST API.
"""

import os
import logging
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr (required for stdio transport)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("silverbullet-mcp")

# Initialize FastMCP server
mcp = FastMCP("silverbullet")

# Default base URL (can be overridden via environment variable)
DEFAULT_BASE_URL = os.environ.get("SILVERBULLET_URL", "http://localhost:3000")


def get_base_url(base_url: str | None = None) -> str:
    """Get the base URL, using default if not provided."""
    return base_url or DEFAULT_BASE_URL


async def make_request(
    method: str,
    url: str,
    content: str | None = None,
    headers: dict[str, str] | None = None,
) -> httpx.Response:
    """Make an HTTP request to SilverBullet."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        request_headers = headers or {}
        if method == "PUT" and content is not None:
            request_headers["Content-Type"] = "text/markdown"

        response = await client.request(
            method=method,
            url=url,
            content=content,
            headers=request_headers,
        )
        return response


@mcp.tool()
async def list_files(base_url: str | None = None) -> str:
    """
    List all files in the SilverBullet space.

    Returns a JSON array of all files with metadata including
    name, lastModified, created, and permissions.

    Args:
        base_url: SilverBullet server URL (optional, uses SILVERBULLET_URL env var if not provided)
    """
    url = f"{get_base_url(base_url)}/.fs"

    try:
        response = await make_request("GET", url)
        response.raise_for_status()
        return response.text
    except httpx.HTTPStatusError as e:
        return f"Error: HTTP {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def read_page(path: str, base_url: str | None = None) -> str:
    """
    Read the content of a page from SilverBullet.

    Args:
        path: Path to the page (e.g., "index.md" or "journal/2024-01-15.md")
        base_url: SilverBullet server URL (optional)

    Returns:
        The markdown content of the page
    """
    # Ensure path doesn't start with /
    path = path.lstrip("/")
    url = f"{get_base_url(base_url)}/.fs/{path}"

    try:
        response = await make_request("GET", url)
        response.raise_for_status()
        return response.text
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"Error: Page '{path}' not found"
        return f"Error: HTTP {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def write_page(path: str, content: str, base_url: str | None = None) -> str:
    """
    Create or update a page in SilverBullet.

    Args:
        path: Path to the page (e.g., "notes/meeting.md")
        content: Markdown content to write
        base_url: SilverBullet server URL (optional)

    Returns:
        Success or error message
    """
    # Ensure path doesn't start with /
    path = path.lstrip("/")
    # Ensure .md extension
    if not path.endswith(".md"):
        path = f"{path}.md"

    url = f"{get_base_url(base_url)}/.fs/{path}"

    try:
        response = await make_request("PUT", url, content=content)
        response.raise_for_status()
        return f"Successfully wrote to '{path}'"
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 403:
            return f"Error: Permission denied - page '{path}' may be read-only"
        return f"Error: HTTP {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def delete_page(path: str, base_url: str | None = None) -> str:
    """
    Delete a page from SilverBullet.

    Args:
        path: Path to the page to delete (e.g., "drafts/old-note.md")
        base_url: SilverBullet server URL (optional)

    Returns:
        Success or error message
    """
    # Ensure path doesn't start with /
    path = path.lstrip("/")
    url = f"{get_base_url(base_url)}/.fs/{path}"

    try:
        response = await make_request("DELETE", url)
        response.raise_for_status()
        return f"Successfully deleted '{path}'"
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"Error: Page '{path}' not found"
        if e.response.status_code == 403:
            return f"Error: Permission denied - cannot delete '{path}'"
        return f"Error: HTTP {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def get_page_metadata(path: str, base_url: str | None = None) -> str:
    """
    Get metadata for a page without fetching its content.

    Args:
        path: Path to the page
        base_url: SilverBullet server URL (optional)

    Returns:
        JSON with lastModified, created, permission, and contentLength
    """
    import json

    # Ensure path doesn't start with /
    path = path.lstrip("/")
    url = f"{get_base_url(base_url)}/.fs/{path}"

    try:
        response = await make_request("GET", url, headers={"X-Get-Meta": "true"})
        response.raise_for_status()

        metadata = {
            "path": path,
            "lastModified": response.headers.get("X-Last-Modified"),
            "created": response.headers.get("X-Created"),
            "permission": response.headers.get("X-Permission", "ro"),
            "contentLength": response.headers.get("X-Content-Length"),
        }
        return json.dumps(metadata, indent=2)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"Error: Page '{path}' not found"
        return f"Error: HTTP {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def search_pages(query: str, base_url: str | None = None) -> str:
    """
    Search for pages by name pattern.

    Args:
        query: Search term to match against page names
        base_url: SilverBullet server URL (optional)

    Returns:
        JSON array of matching pages
    """
    import json

    url = f"{get_base_url(base_url)}/.fs"

    try:
        response = await make_request("GET", url)
        response.raise_for_status()

        files = response.json()
        query_lower = query.lower()

        # Filter files that match the query
        matches = [
            f for f in files
            if query_lower in f.get("name", "").lower()
        ]

        return json.dumps(matches, indent=2)
    except httpx.HTTPStatusError as e:
        return f"Error: HTTP {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def append_to_page(path: str, content: str, base_url: str | None = None) -> str:
    """
    Append content to an existing page.

    Args:
        path: Path to the page
        content: Content to append
        base_url: SilverBullet server URL (optional)

    Returns:
        Success or error message
    """
    # Ensure path doesn't start with /
    path = path.lstrip("/")
    # Ensure .md extension
    if not path.endswith(".md"):
        path = f"{path}.md"

    url = f"{get_base_url(base_url)}/.fs/{path}"

    try:
        # First, read existing content
        response = await make_request("GET", url)

        if response.status_code == 404:
            # Page doesn't exist, create it
            existing_content = ""
        else:
            response.raise_for_status()
            existing_content = response.text

        # Append new content
        new_content = f"{existing_content}\n\n{content}" if existing_content else content

        # Write back
        write_response = await make_request("PUT", url, content=new_content)
        write_response.raise_for_status()

        return f"Successfully appended to '{path}'"
    except httpx.HTTPStatusError as e:
        return f"Error: HTTP {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def ping_server(base_url: str | None = None) -> str:
    """
    Check if the SilverBullet server is available.

    Args:
        base_url: SilverBullet server URL (optional)

    Returns:
        Server status message
    """
    url = f"{get_base_url(base_url)}/.ping"

    try:
        response = await make_request("GET", url)
        if response.status_code == 200:
            return f"Server is available at {get_base_url(base_url)}"
        return f"Server responded with status {response.status_code}"
    except Exception as e:
        return f"Server unavailable: {str(e)}"


@mcp.tool()
async def get_server_config(base_url: str | None = None) -> str:
    """
    Get the SilverBullet server configuration.

    Args:
        base_url: SilverBullet server URL (optional)

    Returns:
        JSON with readOnly, spaceFolderPath, and indexPage
    """
    url = f"{get_base_url(base_url)}/.config"

    try:
        response = await make_request("GET", url)
        response.raise_for_status()
        return response.text
    except httpx.HTTPStatusError as e:
        return f"Error: HTTP {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    """Run the MCP server."""
    import sys

    # Check for HTTP mode
    if "--http" in sys.argv:
        # HTTP transport for daemon mode
        port = 8080
        for i, arg in enumerate(sys.argv):
            if arg == "--port" and i + 1 < len(sys.argv):
                port = int(sys.argv[i + 1])

        logger.info(f"Starting HTTP server on port {port}")
        mcp.run(transport="sse", port=port)
    else:
        # Default: stdio transport
        logger.info("Starting stdio server")
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
