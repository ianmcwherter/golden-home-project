#!/usr/bin/env python3
"""
Golden Home Project — Instagram Auto-Poster
Posts images to Instagram using instagrapi (no official API needed).
Uses username/password auth with session persistence.
"""

import os
import sys
import json
import time
import random
import logging
from pathlib import Path
from datetime import datetime

try:
    from instagrapi import Client
    from instagrapi.exceptions import (
        LoginRequired, ChallengeRequired, FeedbackRequired,
        PleaseWaitFewMinutes
    )
except ImportError:
    print("ERROR: instagrapi not installed. Run: pip3 install instagrapi")
    sys.exit(1)

# --- Config ---
SESSION_FILE = Path(__file__).parent / "logs" / "ig_session.json"
LOG_FILE = Path(__file__).parent / "logs" / "posting_log.json"
MAX_RETRIES = 3
MIN_DELAY = 30
MAX_DELAY = 90

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ghp_ig_poster")


def get_credentials():
    username = os.environ.get("GHP_IG_USERNAME")
    password = os.environ.get("GHP_IG_PASSWORD")
    if not username or not password:
        logger.error("Set GHP_IG_USERNAME and GHP_IG_PASSWORD environment variables")
        sys.exit(1)
    return username, password


def human_delay():
    delay = random.uniform(MIN_DELAY, MAX_DELAY)
    logger.info(f"Waiting {delay:.0f}s (human-like delay)...")
    time.sleep(delay)


def login(cl: Client, username: str, password: str) -> Client:
    """Login with session persistence to reduce ban risk."""
    if SESSION_FILE.exists():
        try:
            cl.load_settings(SESSION_FILE)
            cl.login(username, password)
            cl.get_timeline_feed()  # Verify session works
            logger.info("Logged in via saved session")
            return cl
        except (LoginRequired, Exception) as e:
            logger.warning(f"Saved session failed ({e}), doing fresh login...")

    cl.login(username, password)
    cl.dump_settings(SESSION_FILE)
    logger.info("Fresh login successful, session saved")
    return cl


def post_photo(cl: Client, image_path: str, caption: str) -> dict:
    """Upload a photo with caption. Returns media info dict."""
    logger.info(f"Uploading: {image_path}")
    media = cl.photo_upload(
        path=image_path,
        caption=caption,
    )
    logger.info(f"Posted! Media ID: {media.id}, URL: https://instagram.com/p/{media.code}")
    return {
        "media_id": str(media.id),
        "code": media.code,
        "url": f"https://instagram.com/p/{media.code}",
        "timestamp": datetime.now().isoformat(),
    }


def log_result(image_path: str, success: bool, details: dict):
    """Append result to JSON log file."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "platform": "instagram",
        "image": str(image_path),
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
    parser = argparse.ArgumentParser(description="Post to Instagram for Golden Home Project")
    parser.add_argument("--image", required=True, help="Path to image file")
    parser.add_argument("--caption", required=True, help="Path to caption text file OR raw caption text")
    args = parser.parse_args()

    # Read caption
    caption_path = Path(args.caption)
    if caption_path.exists():
        caption = caption_path.read_text().strip()
    else:
        caption = args.caption

    username, password = get_credentials()

    cl = Client()
    cl.delay_range = [1, 3]  # Small delays between API calls

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Attempt {attempt}/{MAX_RETRIES}")
            human_delay()
            cl = login(cl, username, password)
            result = post_photo(cl, args.image, caption)
            log_result(args.image, True, result)
            print(f"SUCCESS: Posted to Instagram — {result['url']}")
            return
        except PleaseWaitFewMinutes:
            wait = random.uniform(300, 600)
            logger.warning(f"Rate limited. Waiting {wait:.0f}s...")
            time.sleep(wait)
        except FeedbackRequired as e:
            logger.error(f"Instagram feedback required (possible ban): {e}")
            log_result(args.image, False, {"error": str(e)})
            sys.exit(2)
        except ChallengeRequired as e:
            logger.error(f"Challenge required (verify identity): {e}")
            log_result(args.image, False, {"error": str(e)})
            sys.exit(3)
        except Exception as e:
            logger.error(f"Attempt {attempt} failed: {e}")
            if attempt == MAX_RETRIES:
                log_result(args.image, False, {"error": str(e)})
                sys.exit(1)
            time.sleep(random.uniform(60, 120))

    log_result(args.image, False, {"error": "Max retries exceeded"})
    sys.exit(1)


if __name__ == "__main__":
    main()
