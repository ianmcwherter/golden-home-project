#!/usr/bin/env python3
"""
Golden Home Project — YouTube Shorts Uploader
Uploads videos to YouTube using OAuth 2.0 (free, no API approval needed).
First run opens browser for one-time consent. Token is saved for future runs.
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
except ImportError:
    print("ERROR: Google API libraries not installed.")
    print("Run: pip3 install google-auth google-auth-oauthlib google-api-python-client")
    sys.exit(1)

# --- Config ---
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]
CLIENT_SECRET = Path(__file__).parent / "logs" / "yt_client_secret.json"
TOKEN_FILE = Path(__file__).parent / "logs" / "yt_token.json"
LOG_FILE = Path(__file__).parent / "logs" / "posting_log.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ghp_yt_uploader")


def get_authenticated_service():
    """Authenticate and return YouTube API service."""
    creds = None

    # Load saved token
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    # Refresh or get new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing expired token...")
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET.exists():
                logger.error(f"Client secret not found at {CLIENT_SECRET}")
                logger.error("Download from Google Cloud Console and place in automation/logs/")
                sys.exit(1)
            logger.info("Opening browser for YouTube authorization...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET), SCOPES
            )
            creds = flow.run_local_server(port=8080)

        # Save token for next time
        TOKEN_FILE.write_text(creds.to_json())
        logger.info("Token saved")

    return build("youtube", "v3", credentials=creds)


def upload_video(youtube, video_path, title, description, tags=None, category="26", privacy="public"):
    """
    Upload a video to YouTube.
    Category 26 = Howto & Style (good for home product content)
    """
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or ["amazon finds", "home products", "golden home project"],
            "categoryId": category,
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }

    # For Shorts, add #Shorts to title if not already there
    if "#Shorts" not in title and "#shorts" not in title:
        # Check if video is vertical (Shorts format)
        body["snippet"]["title"] = title

    media = MediaFileUpload(
        video_path,
        mimetype="video/mp4",
        resumable=True,
        chunksize=1024 * 1024,  # 1MB chunks
    )

    logger.info(f"Uploading: {video_path}")
    logger.info(f"Title: {title}")

    request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=media,
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            logger.info(f"Upload progress: {int(status.progress() * 100)}%")

    video_id = response["id"]
    video_url = f"https://youtube.com/watch?v={video_id}"
    logger.info(f"Upload complete! URL: {video_url}")

    return {
        "video_id": video_id,
        "url": video_url,
        "title": title,
        "timestamp": datetime.now().isoformat(),
    }


def log_result(video_path, success, details):
    """Append result to JSON log file."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "platform": "youtube",
        "file": str(video_path),
        "success": success,
        **details,
    }
    logs = []
    if LOG_FILE.exists():
        try:
            logs = json.loads(LOG_FILE.read_text())
        except json.JSONDecodeError:
            logs = []
    logs.append(log_entry)
    LOG_FILE.write_text(json.dumps(logs, indent=2))


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Upload to YouTube for Golden Home Project")
    parser.add_argument("--video", required=True, help="Path to video file (MP4)")
    parser.add_argument("--title", required=True, help="Video title")
    parser.add_argument("--description", help="Video description (or path to text file)")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--privacy", default="public", choices=["public", "private", "unlisted"])
    parser.add_argument("--shorts", action="store_true", help="Add #Shorts tag for YouTube Shorts")
    args = parser.parse_args()

    # Read description from file if path exists
    description = args.description or ""
    if description and Path(description).exists():
        description = Path(description).read_text().strip()

    # Add Shorts tag
    title = args.title
    if args.shorts and "#Shorts" not in title:
        title = f"{title} #Shorts"

    # Add affiliate link to description
    if "goldenhomeproject.com" not in description:
        description += "\n\n🏠 Shop all our picks: https://goldenhomeproject.com"
        description += "\n\nAs an Amazon Associate, Golden Home Project earns from qualifying purchases."

    tags = args.tags.split(",") if args.tags else [
        "amazon finds", "home products", "golden home project",
        "amazon must haves", "home hacks", "apartment hacks"
    ]

    try:
        youtube = get_authenticated_service()
        result = upload_video(youtube, args.video, title, description, tags, privacy=args.privacy)
        log_result(args.video, True, result)
        print(f"SUCCESS: Uploaded to YouTube — {result['url']}")
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        log_result(args.video, False, {"error": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    main()
