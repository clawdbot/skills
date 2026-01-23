#!/usr/bin/env python3
"""Tests for OuraClient API wrapper."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import json

# Add scripts directory to path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from oura_api import OuraClient


def make_mock_response(data, status=200):
    """Create a mock urllib response object."""
    mock_resp = MagicMock()
    mock_resp.status = status
    mock_resp.read.return_value = json.dumps({"data": data}).encode("utf-8")
    # Fix context manager protocol: __enter__ must return the mock itself
    mock_resp.__enter__.return_value = mock_resp
    return mock_resp


def make_mock_error(status=401):
    """Create a mock urllib error."""
    mock_resp = MagicMock()
    mock_resp.code = status
    mock_resp.reason = "Unauthorized"
    mock_resp.__enter__ = lambda self: self
    mock_resp.__exit__ = lambda self, *args: None
    return mock_resp


class TestOuraClient:
    """Test OuraClient initialization and API methods."""

    def test_client_init_with_token(self):
        """Test client initialization with explicit token."""
        client = OuraClient(token="test_token_123")
        assert client.token == "test_token_123"
        assert "Bearer test_token_123" in client.headers["Authorization"]

    def test_client_init_from_env(self, monkeypatch):
        """Test client initialization from OURA_API_TOKEN env var."""
        monkeypatch.setenv("OURA_API_TOKEN", "env_token_456")
        client = OuraClient()
        assert client.token == "env_token_456"

    def test_client_init_missing_token(self):
        """Test that missing token raises ValueError."""
        import os
        # Backup and clear env var
        original = os.environ.get("OURA_API_TOKEN")
        os.environ.pop("OURA_API_TOKEN", None)
        try:
            with pytest.raises(ValueError, match="OURA_API_TOKEN not set"):
                OuraClient()
        finally:
            if original:
                os.environ["OURA_API_TOKEN"] = original

    @patch("urllib.request.urlopen")
    def test_request_url_construction(self, mock_urlopen):
        """Test that _request constructs URL correctly."""
        mock_urlopen.return_value = make_mock_response([{"day": "2026-01-15", "score": 80}])

        client = OuraClient(token="test")
        result = client._request("sleep", "2026-01-01", "2026-01-15")

        assert len(result) == 1
        assert result[0]["day"] == "2026-01-15"
        # Check that the URL was called with correct params
        call_args = mock_urlopen.call_args
        request_url = call_args[0][0].full_url if hasattr(call_args[0][0], 'full_url') else str(call_args[0][0])
        assert "start_date=2026-01-01" in request_url
        assert "end_date=2026-01-15" in request_url

    @patch("urllib.request.urlopen")
    def test_get_sleep_no_dates(self, mock_urlopen):
        """Test get_sleep returns all data when no dates specified."""
        mock_urlopen.return_value = make_mock_response([{"day": "2026-01-10"}, {"day": "2026-01-11"}])

        client = OuraClient(token="test")
        result = client.get_sleep()

        assert len(result) == 2
        # Check no date params in URL
        call_args = mock_urlopen.call_args
        request_url = call_args[0][0].full_url if hasattr(call_args[0][0], 'full_url') else str(call_args[0][0])
        assert "start_date" not in request_url

    @patch("urllib.request.urlopen")
    def test_get_readiness(self, mock_urlopen):
        """Test get_readiness method."""
        mock_urlopen.return_value = make_mock_response([{"day": "2026-01-15", "score": 75}])

        client = OuraClient(token="test")
        result = client.get_readiness("2026-01-01", "2026-01-15")

        assert len(result) == 1
        assert result[0]["score"] == 75

    @patch("urllib.request.urlopen")
    def test_get_activity(self, mock_urlopen):
        """Test get_activity method."""
        mock_urlopen.return_value = make_mock_response([{"day": "2026-01-15", "score": 65}])

        client = OuraClient(token="test")
        result = client.get_activity("2026-01-01", "2026-01-15")

        assert len(result) == 1
        assert result[0]["score"] == 65

    @patch("urllib.request.urlopen")
    def test_error_handling(self, mock_urlopen):
        """Test that HTTP errors are raised."""
        from urllib.error import HTTPError
        mock_urlopen.side_effect = HTTPError(
            "https://api.ouraring.com/v2/usercollection/sleep",
            401, "Unauthorized", {}, None
        )

        client = OuraClient(token="test")
        with pytest.raises(Exception):
            client.get_sleep("2026-01-01", "2026-01-15")
