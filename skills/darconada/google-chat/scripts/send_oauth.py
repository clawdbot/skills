#!/usr/bin/env python3
"""
Send a message to Google Chat via OAuth 2.0.
Usage: 
  # Send to a space by name
  python3 send_oauth.py --credentials creds.json --token token.json --space "Space Name" "Message"
  
  # Send DM to user email
  python3 send_oauth.py --credentials creds.json --token token.json --dm user@domain.com "Message"
  
  # Send to space by ID
  python3 send_oauth.py --credentials creds.json --token token.json --space-id "spaces/AAAA..." "Message"
"""

import sys
import json
import argparse
from typing import Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os


SCOPES = [
    'https://www.googleapis.com/auth/chat.messages',
    'https://www.googleapis.com/auth/chat.spaces',
    'https://www.googleapis.com/auth/chat.memberships.readonly'
]


def get_credentials(credentials_path: str, token_path: str) -> Credentials:
    """Get or refresh OAuth credentials."""
    creds = None
    
    # Load existing token if available
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # Refresh or create new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            print("\n🔐 Authentication required!", file=sys.stderr)
            print("Opening browser for authentication...\n", file=sys.stderr)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return creds


def find_space_by_name(service, space_name: str) -> Optional[str]:
    """Find a space ID by its display name."""
    try:
        result = service.spaces().list(pageSize=100).execute()
        spaces = result.get('spaces', [])
        
        for space in spaces:
            if space.get('displayName', '').lower() == space_name.lower():
                return space['name']
        
        return None
    except HttpError as e:
        print(f"Error listing spaces: {e}", file=sys.stderr)
        return None


def create_dm_space(service, user_email: str) -> Optional[str]:
    """Create or get a DM space with a user."""
    try:
        # List existing spaces to find DM
        result = service.spaces().list(pageSize=100).execute()
        spaces = result.get('spaces', [])
        
        # Look for existing DM with this user
        for space in spaces:
            if space.get('type') == 'DIRECT_MESSAGE' or space.get('spaceType') == 'DIRECT_MESSAGE':
                # Check if this DM includes the target user
                # For DMs, we can try to send and see if it works
                # This is a limitation - we can't easily find existing DMs by email
                pass
        
        # For now, we need the space ID directly for DMs
        # OAuth API doesn't easily support creating DMs by email
        print(f"Error: Cannot create DM to {user_email} directly.", file=sys.stderr)
        print(f"To send DMs via OAuth, you need the space ID.", file=sys.stderr)
        print(f"List available spaces with: --list-spaces", file=sys.stderr)
        return None
    except HttpError as e:
        print(f"Error: {e}", file=sys.stderr)
        return None


def send_message(service, space_id: str, message: str, add_emoji: bool = True) -> dict:
    """Send a message to a space."""
    try:
        # Add robot emoji prefix
        if add_emoji:
            message = f"🤖 {message}"
        
        body = {'text': message}
        result = service.spaces().messages().create(
            parent=space_id,
            body=body
        ).execute()
        return {"success": True, "response": result}
    except HttpError as e:
        return {"success": False, "error": str(e)}


def list_spaces(service):
    """List all available spaces."""
    try:
        result = service.spaces().list(pageSize=100).execute()
        spaces = result.get('spaces', [])
        
        print("\n=== Available Spaces ===\n")
        for space in spaces:
            space_type = space.get('spaceType', space.get('type', 'UNKNOWN'))
            space_id = space['name']
            
            # For DMs, try to get member info
            if space_type == 'DIRECT_MESSAGE':
                try:
                    members_result = service.spaces().members().list(parent=space_id).execute()
                    members = members_result.get('memberships', [])
                    member_names = []
                    for member in members:
                        member_info = member.get('member', {})
                        display_name = member_info.get('displayName', 'Unknown')
                        member_names.append(display_name)
                    
                    name = f"DM: {', '.join(member_names)}"
                except:
                    name = space.get('displayName', 'DM (unknown participants)')
            else:
                name = space.get('displayName', space.get('name', 'Unnamed'))
            
            print(f"• {name}")
            print(f"  Type: {space_type}")
            print(f"  ID: {space_id}\n")
        
        return True
    except HttpError as e:
        print(f"Error listing spaces: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description='Send Google Chat messages via OAuth')
    parser.add_argument('--credentials', required=True, help='Path to OAuth credentials JSON')
    parser.add_argument('--token', required=True, help='Path to token file (will be created if missing)')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--space', help='Space display name')
    group.add_argument('--space-id', help='Space ID (spaces/...)')
    group.add_argument('--dm', help='User email for direct message')
    group.add_argument('--list-spaces', action='store_true', help='List all available spaces')
    
    parser.add_argument('message', nargs='?', help='Message to send')
    parser.add_argument('--no-emoji', action='store_true', help='Skip robot emoji prefix')
    
    args = parser.parse_args()
    
    # Get credentials
    creds = get_credentials(args.credentials, args.token)
    service = build('chat', 'v1', credentials=creds)
    
    # Handle list-spaces command
    if args.list_spaces:
        if list_spaces(service):
            sys.exit(0)
        else:
            sys.exit(1)
    
    # Validate message is provided for send operations
    if not args.message:
        print("Error: message is required when sending", file=sys.stderr)
        sys.exit(1)
    
    # Determine space ID
    space_id = None
    if args.space_id:
        space_id = args.space_id
    elif args.space:
        space_id = find_space_by_name(service, args.space)
        if not space_id:
            print(f"Error: Space '{args.space}' not found", file=sys.stderr)
            sys.exit(1)
    elif args.dm:
        space_id = create_dm_space(service, args.dm)
        if not space_id:
            print(f"Error: Could not create DM with {args.dm}", file=sys.stderr)
            sys.exit(1)
    
    # Send message
    result = send_message(service, space_id, args.message, add_emoji=not args.no_emoji)
    
    if result["success"]:
        print(json.dumps(result["response"], indent=2))
    else:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
