"""
Tests for SilverBullet MCP server.

Run with: pytest tests/
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx


# Import the server module
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import (
    get_base_url,
    list_files,
    read_page,
    write_page,
    delete_page,
    search_pages,
    ping_server,
)


class TestGetBaseUrl:
    """Tests for get_base_url helper."""

    def test_returns_provided_url(self):
        """Should return the provided URL when given."""
        result = get_base_url("http://example.com:3000")
        assert result == "http://example.com:3000"

    def test_returns_default_when_none(self):
        """Should return default URL when None provided."""
        with patch.dict(os.environ, {"SILVERBULLET_URL": "http://test:3000"}):
            # Re-import to pick up env var
            from server import DEFAULT_BASE_URL
            result = get_base_url(None)
            assert result is not None


class TestListFiles:
    """Tests for list_files tool."""

    @pytest.mark.asyncio
    async def test_list_files_success(self):
        """Should return file list on success."""
        mock_response = MagicMock()
        mock_response.text = '[{"name": "index.md"}]'
        mock_response.raise_for_status = MagicMock()

        with patch("server.make_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = mock_response
            result = await list_files("http://localhost:3000")
            assert "index.md" in result

    @pytest.mark.asyncio
    async def test_list_files_error(self):
        """Should return error message on failure."""
        with patch("server.make_request", new_callable=AsyncMock) as mock_req:
            mock_req.side_effect = Exception("Connection failed")
            result = await list_files("http://localhost:3000")
            assert "Error" in result


class TestReadPage:
    """Tests for read_page tool."""

    @pytest.mark.asyncio
    async def test_read_page_success(self):
        """Should return page content on success."""
        mock_response = MagicMock()
        mock_response.text = "# Hello World"
        mock_response.raise_for_status = MagicMock()

        with patch("server.make_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = mock_response
            result = await read_page("index.md", "http://localhost:3000")
            assert "Hello World" in result

    @pytest.mark.asyncio
    async def test_read_page_strips_leading_slash(self):
        """Should strip leading slash from path."""
        mock_response = MagicMock()
        mock_response.text = "content"
        mock_response.raise_for_status = MagicMock()

        with patch("server.make_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = mock_response
            await read_page("/index.md", "http://localhost:3000")
            # Verify the URL doesn't have double slashes
            call_args = mock_req.call_args
            assert "/.fs//index.md" not in str(call_args)


class TestWritePage:
    """Tests for write_page tool."""

    @pytest.mark.asyncio
    async def test_write_page_adds_md_extension(self):
        """Should add .md extension if missing."""
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()

        with patch("server.make_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = mock_response
            result = await write_page("test", "content", "http://localhost:3000")
            assert "test.md" in result


class TestSearchPages:
    """Tests for search_pages tool."""

    @pytest.mark.asyncio
    async def test_search_pages_filters_results(self):
        """Should filter files by query."""
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"name": "meeting-notes.md"},
            {"name": "index.md"},
            {"name": "meeting-2024.md"},
        ]
        mock_response.raise_for_status = MagicMock()

        with patch("server.make_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = mock_response
            result = await search_pages("meeting", "http://localhost:3000")
            assert "meeting-notes.md" in result
            assert "meeting-2024.md" in result
            # index.md should not be in filtered results
            import json
            data = json.loads(result)
            names = [f["name"] for f in data]
            assert "index.md" not in names


class TestPingServer:
    """Tests for ping_server tool."""

    @pytest.mark.asyncio
    async def test_ping_success(self):
        """Should return available message on 200."""
        mock_response = MagicMock()
        mock_response.status_code = 200

        with patch("server.make_request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = mock_response
            result = await ping_server("http://localhost:3000")
            assert "available" in result

    @pytest.mark.asyncio
    async def test_ping_failure(self):
        """Should return unavailable message on error."""
        with patch("server.make_request", new_callable=AsyncMock) as mock_req:
            mock_req.side_effect = Exception("Connection refused")
            result = await ping_server("http://localhost:3000")
            assert "unavailable" in result
