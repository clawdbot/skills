#!/usr/bin/env python3
"""
gcal-pro: OAuth 2.0 Authentication Module
Handles secure local token storage and credential management.
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional, Tuple

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Configuration
CONFIG_DIR = Path.home() / ".config" / "gcal-pro"
CLIENT_SECRET_FILE = CONFIG_DIR / "client_secret.json"
TOKEN_FILE = CONFIG_DIR / "token.json"
LICENSE_FILE = CONFIG_DIR / "license.json"

# Scopes - Minimal permissions per tier
SCOPES_FREE = ["https://www.googleapis.com/auth/calendar.readonly"]
SCOPES_PRO = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events"
]


def get_config_dir() -> Path:
    """Ensure config directory exists and return path."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    return CONFIG_DIR


def check_client_secret() -> bool:
    """Check if client_secret.json exists."""
    return CLIENT_SECRET_FILE.exists()


def is_pro_user() -> bool:
    """Check if user has Pro license."""
    try:
        from gcal_license import is_pro
        return is_pro()
    except ImportError:
        # Fallback to direct file check
        if not LICENSE_FILE.exists():
            return False
        try:
            with open(LICENSE_FILE, "r") as f:
                license_data = json.load(f)
                return license_data.get("tier") == "pro" and license_data.get("valid", False)
        except (json.JSONDecodeError, IOError):
            return False


def get_scopes() -> list:
    """Return appropriate scopes based on license tier."""
    return SCOPES_PRO if is_pro_user() else SCOPES_FREE


def get_credentials(force_refresh: bool = False) -> Optional[Credentials]:
    """
    Get valid credentials, refreshing or re-authenticating as needed.
    
    Args:
        force_refresh: Force re-authentication even if token exists
        
    Returns:
        Valid Credentials object or None if authentication fails
    """
    get_config_dir()
    
    if not check_client_secret():
        print(f"ERROR: client_secret.json not found at {CLIENT_SECRET_FILE}")
        print("Please complete Google Cloud setup first.")
        return None
    
    creds = None
    scopes = get_scopes()
    
    # Load existing token if available
    if TOKEN_FILE.exists() and not force_refresh:
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), scopes)
        except Exception as e:
            print(f"Warning: Could not load existing token: {e}")
            creds = None
    
    # Check if credentials need refresh or re-auth
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            _save_token(creds)
        except Exception as e:
            print(f"Token refresh failed: {e}")
            creds = None
    
    # Need new authentication
    if not creds or not creds.valid:
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_FILE), scopes
            )
            creds = flow.run_local_server(
                port=8080,
                prompt="consent",
                success_message="Authentication successful! You can close this window."
            )
            _save_token(creds)
            print("[OK] Authentication successful!")
        except Exception as e:
            print(f"Authentication failed: {e}")
            return None
    
    return creds


def _save_token(creds: Credentials) -> None:
    """Save credentials to token file."""
    with open(TOKEN_FILE, "w") as token_file:
        token_file.write(creds.to_json())
    # Secure the token file (readable only by owner on Unix)
    try:
        os.chmod(TOKEN_FILE, 0o600)
    except (OSError, AttributeError):
        pass  # Windows doesn't support chmod the same way


def get_calendar_service():
    """
    Get authenticated Google Calendar API service.
    
    Returns:
        Google Calendar API service object or None
    """
    creds = get_credentials()
    if not creds:
        return None
    
    try:
        service = build("calendar", "v3", credentials=creds)
        return service
    except Exception as e:
        print(f"Failed to build Calendar service: {e}")
        return None


def revoke_credentials() -> bool:
    """Revoke current credentials and delete local tokens."""
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
            # Attempt to revoke via Google
            import requests
            requests.post(
                "https://oauth2.googleapis.com/revoke",
                params={"token": creds.token},
                headers={"content-type": "application/x-www-form-urlencoded"}
            )
        except Exception:
            pass  # Revocation is best-effort
        
        # Delete local token
        TOKEN_FILE.unlink()
        print("[OK] Credentials revoked and local token deleted.")
        return True
    else:
        print("No credentials to revoke.")
        return False


def get_auth_status() -> dict:
    """Get current authentication status."""
    status = {
        "config_dir": str(CONFIG_DIR),
        "client_secret_exists": check_client_secret(),
        "token_exists": TOKEN_FILE.exists(),
        "is_pro": is_pro_user(),
        "authenticated": False,
        "scopes": []
    }
    
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
            status["authenticated"] = creds.valid or (creds.expired and creds.refresh_token)
            status["scopes"] = list(creds.scopes) if creds.scopes else []
        except Exception:
            pass
    
    return status


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="gcal-pro authentication")
    parser.add_argument("command", choices=["auth", "status", "revoke"],
                        help="Authentication command")
    parser.add_argument("--force", action="store_true",
                        help="Force re-authentication")
    
    args = parser.parse_args()
    
    if args.command == "auth":
        creds = get_credentials(force_refresh=args.force)
        if creds:
            print(f"[OK] Authenticated successfully")
            print(f"  Token stored at: {TOKEN_FILE}")
        else:
            sys.exit(1)
    
    elif args.command == "status":
        status = get_auth_status()
        print(f"Config directory: {status['config_dir']}")
        print(f"Client secret:    {'[OK] Found' if status['client_secret_exists'] else '[X] Missing'}")
        print(f"Token:            {'[OK] Found' if status['token_exists'] else '[X] Missing'}")
        print(f"Authenticated:    {'[OK] Yes' if status['authenticated'] else '[X] No'}")
        print(f"Tier:             {'Pro' if status['is_pro'] else 'Free'}")
        if status['scopes']:
            print(f"Scopes:           {', '.join(status['scopes'])}")
    
    elif args.command == "revoke":
        revoke_credentials()
