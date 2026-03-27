#!/usr/bin/env python3
"""
Golden Home Project — Batch Poster
Reads the post tracker, finds the next unpublished post,
and posts it to Instagram and Facebook.
"""

import os
import re
import sys
import subprocess
import logging
from pathlib import Path
from datetime import datetime

CONTENT_DIR = Path("/Users/ianmcwherter/Desktop/Golden Home Project Content files")
TRACKER_FILE = CONTENT_DIR / "golden-home-project" / "GHP_OPERATIONS_HUB.md"
FALLBACK_TRACKER = CONTENT_DIR / "GHP_POST_TRACKER.md"
AUTOMATION_DIR = Path(__file__).parent

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ghp_batch_poster")


def find_next_post():
    """Find the next post number that needs publishing."""
    # Check for post files that exist but haven't been published
    for i in range(9, 30):  # Start from 009
        post_num = f"{i:03d}"
        image = CONTENT_DIR / f"GHP_Post_{post_num}.jpg"
        caption = CONTENT_DIR / f"GHP_Post_{post_num}_Caption.txt"
        if image.exists() and caption.exists():
            logger.info(f"Found ready post: {post_num}")
            return post_num, str(image), str(caption)
    return None, None, None


def post_to_instagram(image_path, caption_path):
    """Call the Instagram posting script."""
    script = AUTOMATION_DIR / "post_to_instagram.py"
    cmd = [sys.executable, str(script), "--image", image_path, "--caption", caption_path]
    logger.info(f"Posting to Instagram: {cmd}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode == 0:
        logger.info(f"Instagram: {result.stdout.strip()}")
        return True
    else:
        logger.error(f"Instagram failed: {result.stderr.strip()}")
        return False


def post_to_facebook(image_path, caption_path):
    """Call the Facebook posting script."""
    script = AUTOMATION_DIR / "post_to_facebook.py"
    cmd = [sys.executable, str(script), "--image", image_path, "--caption", caption_path]
    logger.info(f"Posting to Facebook: {cmd}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode == 0:
        logger.info(f"Facebook: {result.stdout.strip()}")
        return True
    else:
        logger.error(f"Facebook failed: {result.stderr.strip()}")
        return False


def main():
    logger.info("=" * 50)
    logger.info(f"Batch poster started at {datetime.now().isoformat()}")

    # Check credentials
    if not os.environ.get("GHP_IG_USERNAME"):
        logger.warning("GHP_IG_USERNAME not set — skipping Instagram")
    if not os.environ.get("GHP_FB_EMAIL"):
        logger.warning("GHP_FB_EMAIL not set — skipping Facebook")

    post_num, image, caption = find_next_post()
    if not post_num:
        logger.info("No posts ready to publish. Exiting.")
        return

    logger.info(f"Publishing Post {post_num}: {image}")

    ig_success = False
    fb_success = False

    if os.environ.get("GHP_IG_USERNAME"):
        ig_success = post_to_instagram(image, caption)

    if os.environ.get("GHP_FB_EMAIL"):
        fb_success = post_to_facebook(image, caption)

    # Summary
    logger.info(f"Results — Instagram: {'✅' if ig_success else '❌'} | Facebook: {'✅' if fb_success else '❌'}")

    if ig_success or fb_success:
        # Move posted files to archive
        archive_dir = CONTENT_DIR / "posted"
        archive_dir.mkdir(exist_ok=True)
        # Don't move, just log — agent will update tracker
        logger.info(f"Post {post_num} published. Update tracker manually or via agent.")


if __name__ == "__main__":
    main()
