#!/usr/bin/env python3
"""Upload files to catbox.moe or litterbox.catbox.moe"""

import argparse
import sys
from pathlib import Path
import requests


CATBOX_API = "https://catbox.moe/user/api.php"
LITTERBOX_API = "https://litterbox.catbox.moe/resources/internals/api.php"


def upload_to_catbox(file_path, userhash=None):
    """Upload file to catbox.moe (permanent storage)"""
    with open(file_path, "rb") as f:
        files = {"fileToUpload": f}
        data = {"reqtype": "fileupload"}
        if userhash:
            data["userhash"] = userhash

        response = requests.post(CATBOX_API, data=data, files=files)
        response.raise_for_status()
        return response.text.strip()


def upload_to_litterbox(file_path, time="24h"):
    """Upload file to litterbox.catbox.moe (temporary storage)"""
    valid_times = ["1h", "12h", "24h", "72h"]
    if time not in valid_times:
        raise ValueError(f"Invalid time. Must be one of: {', '.join(valid_times)}")

    with open(file_path, "rb") as f:
        files = {"fileToUpload": f}
        data = {"reqtype": "fileupload", "time": time}

        response = requests.post(LITTERBOX_API, data=data, files=files)
        response.raise_for_status()
        return response.text.strip()


def main():
    parser = argparse.ArgumentParser(description="Upload files to catbox.moe or litterbox.catbox.moe")
    parser.add_argument("file", help="File to upload")
    parser.add_argument("--service", choices=["catbox", "litterbox"], default="litterbox", help="Service to use (default: litterbox)")
    parser.add_argument("--time", choices=["1h", "12h", "24h", "72h"], default="24h", help="Litterbox expiration time (default: 24h)")
    parser.add_argument("--userhash", help="Catbox account hash (for catbox service)")

    args = parser.parse_args()
    file_path = Path(args.file)

    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    try:
        if args.service == "catbox":
            url = upload_to_catbox(file_path, args.userhash)
        else:
            url = upload_to_litterbox(file_path, args.time)

        print(url)
    except requests.RequestException as e:
        print(f"Upload failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
