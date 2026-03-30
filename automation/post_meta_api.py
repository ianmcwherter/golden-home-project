#!/usr/bin/env python3
"""
Golden Home Project — Meta Graph API Poster
Posts to Facebook Page and Instagram using the official Graph API.
Requires: Facebook App ID, App Secret, and Page Access Token.

First run: Call with --setup to get your Page Access Token via browser OAuth.
After setup: Posts directly via API (no browser needed).
"""

import os
import sys
import json
import time
import logging
import requests
import webbrowser
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# --- Config ---
CONFIG_FILE = Path(__file__).parent / "logs" / "meta_config.json"
TOKEN_FILE = Path(__file__).parent / "logs" / "meta_tokens.json"
LOG_FILE = Path(__file__).parent / "logs" / "posting_log.json"
GRAPH_API = "https://graph.facebook.com/v21.0"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ghp_meta_api")


def load_config():
    if not CONFIG_FILE.exists():
        logger.error(f"Config not found: {CONFIG_FILE}")
        sys.exit(1)
    return json.loads(CONFIG_FILE.read_text())


def load_tokens():
    if TOKEN_FILE.exists():
        return json.loads(TOKEN_FILE.read_text())
    return {}


def save_tokens(tokens):
    TOKEN_FILE.write_text(json.dumps(tokens, indent=2))


# --- OAuth Setup ---
class OAuthHandler(BaseHTTPRequestHandler):
    """Captures the OAuth redirect code."""
    code = None
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        if "code" in query:
            OAuthHandler.code = query["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authorization successful! You can close this tab.")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Authorization failed.")
    def log_message(self, format, *args):
        pass  # Suppress HTTP logs


def setup_tokens():
    """Interactive setup to get Page Access Token and IG Business Account ID."""
    config = load_config()
    app_id = config["app_id"]
    app_secret = config["app_secret"]
    page_id = config["page_id"]

    # Step 1: Get user access token via OAuth
    permissions = "pages_show_list,pages_read_engagement,pages_manage_posts,instagram_basic,instagram_content_publish,business_management"
    auth_url = (
        f"https://www.facebook.com/v21.0/dialog/oauth?"
        f"client_id={app_id}&redirect_uri=http://localhost:8080/"
        f"&scope={permissions}&response_type=code"
    )

    logger.info("Opening browser for Facebook authorization...")
    webbrowser.open(auth_url)

    # Start local server to capture redirect
    server = HTTPServer(("localhost", 8080), OAuthHandler)
    server.handle_request()
    code = OAuthHandler.code

    if not code:
        logger.error("Failed to get authorization code")
        sys.exit(1)

    # Step 2: Exchange code for short-lived user token
    logger.info("Exchanging code for access token...")
    resp = requests.get(f"{GRAPH_API}/oauth/access_token", params={
        "client_id": app_id,
        "client_secret": app_secret,
        "redirect_uri": "http://localhost:8080/",
        "code": code,
    }).json()

    if "access_token" not in resp:
        logger.error(f"Token exchange failed: {resp}")
        sys.exit(1)

    short_token = resp["access_token"]

    # Step 3: Exchange for long-lived user token (60 days)
    logger.info("Getting long-lived token...")
    resp = requests.get(f"{GRAPH_API}/oauth/access_token", params={
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_token,
    }).json()

    long_lived_user_token = resp.get("access_token", short_token)

    # Step 4: Get Page Access Token (never expires)
    logger.info("Getting Page access token...")
    resp = requests.get(f"{GRAPH_API}/{page_id}", params={
        "fields": "access_token,name",
        "access_token": long_lived_user_token,
    }).json()

    page_token = resp.get("access_token")
    page_name = resp.get("name", "Unknown")
    logger.info(f"Page: {page_name}")

    # Step 5: Get Instagram Business Account ID
    logger.info("Getting Instagram Business Account ID...")
    resp = requests.get(f"{GRAPH_API}/{page_id}", params={
        "fields": "instagram_business_account",
        "access_token": page_token,
    }).json()

    ig_account_id = resp.get("instagram_business_account", {}).get("id")
    if ig_account_id:
        logger.info(f"Instagram Business Account ID: {ig_account_id}")
    else:
        logger.warning("No Instagram Business Account linked to this page")

    # Save tokens
    tokens = {
        "page_access_token": page_token,
        "ig_business_account_id": ig_account_id,
        "page_name": page_name,
        "created": datetime.now().isoformat(),
    }
    save_tokens(tokens)
    logger.info("Tokens saved! Setup complete.")
    return tokens


# --- Posting Functions ---
def post_to_facebook(caption, image_path=None, image_url=None):
    """Post to Facebook Page via Graph API."""
    config = load_config()
    tokens = load_tokens()
    page_token = tokens.get("page_access_token")
    if not page_token:
        logger.error("No page token. Run with --setup first.")
        sys.exit(1)

    page_id = config["page_id"]

    if image_path and Path(image_path).exists():
        # Photo post with local file upload
        logger.info(f"Posting photo to Facebook: {image_path}")
        with open(image_path, "rb") as f:
            resp = requests.post(
                f"{GRAPH_API}/{page_id}/photos",
                data={"message": caption, "access_token": page_token},
                files={"source": f},
            ).json()
    elif image_url:
        # Photo post with URL
        resp = requests.post(
            f"{GRAPH_API}/{page_id}/photos",
            data={"message": caption, "url": image_url, "access_token": page_token},
        ).json()
    else:
        # Text-only post
        resp = requests.post(
            f"{GRAPH_API}/{page_id}/feed",
            data={"message": caption, "access_token": page_token},
        ).json()

    if "id" in resp or "post_id" in resp:
        post_id = resp.get("id") or resp.get("post_id")
        logger.info(f"Facebook post published! ID: {post_id}")
        return {"success": True, "post_id": post_id, "platform": "facebook"}
    else:
        logger.error(f"Facebook post failed: {resp}")
        return {"success": False, "error": str(resp), "platform": "facebook"}


def post_to_instagram(caption, image_url):
    """
    Post to Instagram via Graph API.
    NOTE: Instagram API requires image_url (publicly accessible URL).
    Local files must be hosted first (e.g., on goldenhomeproject.com).
    """
    tokens = load_tokens()
    page_token = tokens.get("page_access_token")
    ig_id = tokens.get("ig_business_account_id")

    if not page_token or not ig_id:
        logger.error("No tokens. Run with --setup first.")
        sys.exit(1)

    # Step 1: Create media container
    logger.info(f"Creating Instagram media container...")
    resp = requests.post(
        f"{GRAPH_API}/{ig_id}/media",
        data={
            "image_url": image_url,
            "caption": caption,
            "access_token": page_token,
        },
    ).json()

    container_id = resp.get("id")
    if not container_id:
        logger.error(f"Container creation failed: {resp}")
        return {"success": False, "error": str(resp), "platform": "instagram"}

    # Step 2: Wait for container to be ready
    logger.info("Waiting for media processing...")
    time.sleep(5)

    # Step 3: Publish
    logger.info("Publishing to Instagram...")
    resp = requests.post(
        f"{GRAPH_API}/{ig_id}/media_publish",
        data={
            "creation_id": container_id,
            "access_token": page_token,
        },
    ).json()

    if "id" in resp:
        logger.info(f"Instagram post published! ID: {resp['id']}")
        return {"success": True, "post_id": resp["id"], "platform": "instagram"}
    else:
        logger.error(f"Instagram publish failed: {resp}")
        return {"success": False, "error": str(resp), "platform": "instagram"}


def log_result(platform, image_path, success, details):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "platform": platform,
        "image": str(image_path) if image_path else None,
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
    parser = argparse.ArgumentParser(description="Post via Meta Graph API")
    parser.add_argument("--setup", action="store_true", help="Run OAuth setup to get tokens")
    parser.add_argument("--facebook", action="store_true", help="Post to Facebook")
    parser.add_argument("--instagram", action="store_true", help="Post to Instagram")
    parser.add_argument("--image", help="Local image path (Facebook) or public URL (Instagram)")
    parser.add_argument("--caption", help="Caption text or path to caption file")
    args = parser.parse_args()

    if args.setup:
        setup_tokens()
        return

    if not args.caption:
        parser.error("--caption is required")

    # Read caption
    caption_path = Path(args.caption)
    caption = caption_path.read_text().strip() if caption_path.exists() else args.caption

    if args.facebook:
        result = post_to_facebook(caption, image_path=args.image)
        log_result("facebook", args.image, result["success"], result)
        if result["success"]:
            print(f"SUCCESS: Posted to Facebook — ID: {result['post_id']}")
        else:
            print(f"FAILED: {result.get('error')}")
            sys.exit(1)

    if args.instagram:
        if not args.image or not args.image.startswith("http"):
            logger.error("Instagram requires --image as a public URL (https://...)")
            logger.info("Tip: Upload image to goldenhomeproject.com/images/ first")
            sys.exit(1)
        result = post_to_instagram(caption, image_url=args.image)
        log_result("instagram", args.image, result["success"], result)
        if result["success"]:
            print(f"SUCCESS: Posted to Instagram — ID: {result['post_id']}")
        else:
            print(f"FAILED: {result.get('error')}")
            sys.exit(1)


if __name__ == "__main__":
    main()
