#!/usr/bin/env python3
"""Send EPUB to Kindle via Mail.app."""

import argparse
import subprocess
from pathlib import Path

DEFAULT_KINDLE_EMAIL = "simonpilkington74_8oVjpj@kindle.com"


def send_via_mail_app(file_path: str, kindle_email: str, subject: str) -> bool:
    """Send file to Kindle using Mail.app AppleScript."""
    
    applescript = f'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"{subject}", visible:false}}
        tell newMessage
            make new to recipient at end of to recipients with properties {{address:"{kindle_email}"}}
            set content to "Sent from blog-to-kindle skill."
            make new attachment with properties {{file name:"{file_path}"}} at after the last paragraph
        end tell
        send newMessage
    end tell
    '''
    
    result = subprocess.run(
        ["osascript", "-e", applescript],
        capture_output=True,
        text=True
    )
    
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Send EPUB to Kindle")
    parser.add_argument("--file", required=True, help="EPUB file to send")
    parser.add_argument("--kindle-email", default=DEFAULT_KINDLE_EMAIL, help="Kindle email address")
    parser.add_argument("--subject", help="Email subject (default: filename)")
    args = parser.parse_args()
    
    file_path = Path(args.file).resolve()
    
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return 1
    
    if not file_path.suffix.lower() in [".epub", ".mobi", ".pdf"]:
        print(f"Warning: {file_path.suffix} may not be supported by Kindle")
    
    # Check file size
    size_mb = file_path.stat().st_size / (1024 * 1024)
    if size_mb > 50:
        print(f"Error: File too large ({size_mb:.1f} MB). Kindle limit is 50MB.")
        return 1
    
    subject = args.subject or file_path.stem.replace("_", " ").replace("-", " ").title()
    
    print(f"Sending to Kindle...")
    print(f"  File: {file_path}")
    print(f"  Size: {size_mb:.2f} MB")
    print(f"  To: {args.kindle_email}")
    print(f"  Subject: {subject}")
    
    success = send_via_mail_app(str(file_path), args.kindle_email, subject)
    
    if success:
        print(f"\n✅ Sent to Kindle!")
        print(f"   Should arrive in a few minutes.")
        return 0
    else:
        print(f"\n❌ Failed to send. Check Mail.app.")
        return 1


if __name__ == "__main__":
    exit(main())
