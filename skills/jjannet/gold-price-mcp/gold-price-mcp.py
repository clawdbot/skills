#!/usr/bin/env python3.10
"""
MCP Service: Thai Gold Price
"""

import asyncio
import json
import sys
from typing import List

import httpx
import mcp.types as types
import mcp.server.stdio
from mcp.server import Server

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------

API_URL = "https://api.chnwt.dev/thai-gold-api/latest"
HTTP_TIMEOUT = 10.0

# -------------------------------------------------------------------
# MCP Server
# -------------------------------------------------------------------

server = Server("thai-gold-price-mcp")


# -------------------------------------------------------------------
# MCP: list_tools
# -------------------------------------------------------------------

@server.list_tools()
async def list_tools() -> List[types.Tool]:
    return [
        types.Tool(
            name="get_thai_gold_price",
            description=(
                "Fetch the latest Thai gold prices including "
                "gold bar and gold ornament prices with last update time."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        )
    ]


# -------------------------------------------------------------------
# MCP: call_tool
# -------------------------------------------------------------------

@server.call_tool()
async def call_tool(
    name: str,
    arguments: dict | None,
) -> List[types.TextContent]:

    if name != "get_thai_gold_price":
        raise ValueError(f"Unsupported tool: {name}")

    return await fetch_thai_gold_price()


# -------------------------------------------------------------------
# Business Logic
# -------------------------------------------------------------------

async def fetch_thai_gold_price() -> List[types.TextContent]:
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            response = await client.get(API_URL)
            response.raise_for_status()
            payload = response.json()

        if payload.get("status") != "success":
            return _error("Upstream API returned non-success status")

        data = payload.get("response")
        if not isinstance(data, dict):
            return _error("Invalid response format from upstream API")

        return [
            types.TextContent(
                type="text",
                text=json.dumps(data, ensure_ascii=False, indent=2),
            )
        ]

    except httpx.TimeoutException:
        return _error("Timeout while calling gold price API")

    except httpx.HTTPError as exc:
        return _error(f"HTTP error: {str(exc)}")

    except Exception as exc:
        return _error(f"Unexpected error: {str(exc)}")


def _error(message: str) -> List[types.TextContent]:
    return [
        types.TextContent(
            type="text",
            text=json.dumps(
                {"error": message},
                ensure_ascii=False,
                indent=2,
            ),
        )
    ]


# -------------------------------------------------------------------
# Entrypoint
# -------------------------------------------------------------------

async def main() -> None:
    async with mcp.server.stdio.stdio_server() as (read, write):
        await server.run(
            read,
            write,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        print(f"Fatal error: {exc}", file=sys.stderr)
        sys.exit(1)