#!/usr/bin/env python3
"""
Golden Home Project — GitHub Actions Daily Poster
===================================================
Runs in GitHub Actions (cloud) at noon ET daily.
Reads pre-generated videos from the repo, posts to YouTube + IG.

No Claude API needed. Uses YouTube Data API v3 + Meta Graph API.

Usage:
  python3 github_daily_poster.py \\
    --yt-token /tmp/yt_token.json \\
    --meta-token /tmp/meta_tokens.json \\
    --associate-tag goldenhomep06-20
"""

import argparse
import json
import os
import sys
import time
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── Paths (relative to repo root in GitHub Actions checkout)
REPO_ROOT  = Path(__file__).parent.parent
VIDEOS_DIR = REPO_ROOT / "videos" / "transformation"
LOGS_DIR   = Path(__file__).parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Content calendar (April 2026)
APRIL_CALENDAR = [
    {"date": "2026-04-01", "title": "I Transformed My Cluttered Kitchen Counter For $47",
     "products": [{"asin": "B08BHBPQHZ", "name": "Airtight Canister Set (4-piece)", "price": "$18.99"},
                  {"asin": "B07WGWFCTS", "name": "Bamboo Utensil Holder", "price": "$12.99"},
                  {"asin": "B08CHWX4S1", "name": "Paper Towel Holder Stand", "price": "$8.99"},
                  {"asin": "B09NQTD6G8", "name": "Bamboo Cutting Board Organizer", "price": "$16.99"}]},
    {"date": "2026-04-02", "title": "I Used the Wrong Pantry Organizers for 3 Years",
     "products": [{"asin": "B07NQVHKX7", "name": "Pantry Organization Bins (10-pack)", "price": "$32.99"},
                  {"asin": "B08BNHBK9N", "name": "Stackable Can Organizer", "price": "$14.99"},
                  {"asin": "B07J5N6HWJ", "name": "Chalk Label Set (reusable)", "price": "$9.99"},
                  {"asin": "B09K3MQVXL", "name": "Turntable Lazy Susan (2-pack)", "price": "$16.99"}]},
    {"date": "2026-04-04", "title": "My Kitchen Looks Like a Magazine Now — $34 Total", "ig": True,
     "products": [{"asin": "B08S8FMWWP", "name": "Minimalist Soap Dispenser Set (3-piece)", "price": "$19.99"},
                  {"asin": "B07ZBQSV97", "name": "Ceramic Sponge Holder", "price": "$8.99"},
                  {"asin": "B09JQRJ8C4", "name": "Small Countertop Tray Organizer", "price": "$12.99"}]},
    {"date": "2026-04-05", "title": "Room by Room Ep 1: The Cabinet Nobody Looks In",
     "products": [{"asin": "B08B3NWK45", "name": "Bamboo Drawer Organizer (expandable)", "price": "$21.99"},
                  {"asin": "B07D8CTHXF", "name": "Small Bins 2-pack", "price": "$11.99"},
                  {"asin": "B01N3LTFQO", "name": "DYMO Label Maker", "price": "$24.99"}]},
    {"date": "2026-04-07", "title": "I Finally Made My Bedroom Feel Like a Hotel",
     "products": [{"asin": "B07XVFBXWF", "name": "Linen Duvet Cover Set (Queen)", "price": "$54.99"},
                  {"asin": "B08JFV6MXQ", "name": "Throw Pillow Covers 4-pack", "price": "$19.99"},
                  {"asin": "B08KGWF5ZM", "name": "Bedside Tray Organizer", "price": "$16.99"}]},
    {"date": "2026-04-09", "title": "I Tested $25 vs $120 Air Purifiers. Here's the Truth.",
     "products": [{"asin": "B07VXKXR8H", "name": "LEVOIT Air Purifier (small room)", "price": "$24.99"},
                  {"asin": "B083PGLT37", "name": "LEVOIT Core 300 Air Purifier", "price": "$99.99"}]},
    {"date": "2026-04-11", "title": "My Nightstand Was a Disaster. $28 Fixed It.", "ig": True,
     "products": [{"asin": "B09G9FKWG3", "name": "Bedside Charging Station (3-port)", "price": "$19.99"},
                  {"asin": "B07WH4KBQB", "name": "Bamboo Bedside Tray", "price": "$14.99"}]},
    {"date": "2026-04-12", "title": "Room by Room Ep 2: The Junk Drawer Doesn't Have to Exist",
     "products": [{"asin": "B08B3NWK45", "name": "Interlocking Drawer Organizer Set", "price": "$18.99"},
                  {"asin": "B07Y9BKMYF", "name": "Cable Management Box", "price": "$19.99"}]},
    {"date": "2026-04-14", "title": "My Bathroom Went From Rental to Spa for $52",
     "products": [{"asin": "B08CZHVQJ4", "name": "Bamboo Over-Toilet Storage Shelf", "price": "$32.99"},
                  {"asin": "B08S8FMWWP", "name": "Bathroom Accessories Set (4-piece)", "price": "$21.99"}]},
    {"date": "2026-04-16", "title": "The Shower Caddy I Wasted $40 On (And What I Use Now)",
     "products": [{"asin": "B08XZV1H87", "name": "Rust-Proof Corner Shower Shelf (adhesive)", "price": "$22.99"}]},
    {"date": "2026-04-18", "title": "I Made My Living Room Look Twice as Expensive for $67", "ig": True,
     "products": [{"asin": "B09NXGKK3V", "name": "Waffle Knit Throw Blanket", "price": "$24.99"},
                  {"asin": "B08JFV6MXQ", "name": "Velvet Throw Pillow Covers (2-pack)", "price": "$18.99"},
                  {"asin": "B08RNX6Y8D", "name": "Faux Olive Tree with Ceramic Pot", "price": "$28.99"}]},
    {"date": "2026-04-19", "title": "Room by Room Ep 3: My Bathroom Cabinet Is Now Usable",
     "products": [{"asin": "B08CW3M5P4", "name": "Under-Sink Organizer with Adjustable Shelf", "price": "$19.99"},
                  {"asin": "B07D8CTHXF", "name": "Bathroom Storage Bins 3-pack", "price": "$14.99"}]},
    {"date": "2026-04-21", "title": "I Optimized My Morning Routine With 3 Amazon Products",
     "products": [{"asin": "B09N8P9H9K", "name": "Wall-Mounted Key and Phone Holder", "price": "$14.99"},
                  {"asin": "B07NNR4LX4", "name": "Handheld Electric Milk Frother", "price": "$8.99"},
                  {"asin": "B09JQRJ8C4", "name": "Entryway Catch-All Tray Organizer", "price": "$16.99"}]},
    {"date": "2026-04-23", "title": "I Tried Every Desk Organizer Style. This One Won.",
     "products": [{"asin": "B07WLGDRQ5", "name": "Bamboo Modular Desk Organizer Set", "price": "$34.99"}]},
    {"date": "2026-04-25", "title": "My Desk Setup Went From Chaos to Clean in 30 Minutes", "ig": True,
     "products": [{"asin": "B07Y9BKMYF", "name": "Cable Management Box (large)", "price": "$19.99"},
                  {"asin": "B09FBQR8XL", "name": "Monitor Stand with Storage Drawer", "price": "$39.99"},
                  {"asin": "B08F4YK8B7", "name": "Desktop Catch-All Organizer Tray", "price": "$14.99"}]},
    {"date": "2026-04-26", "title": "Room by Room Ep 4: The Bedroom Closet That Finally Makes Sense",
     "products": [{"asin": "B07FFXVDXG", "name": "Velvet Non-Slip Hangers (50-pack)", "price": "$19.99"},
                  {"asin": "B07X5JQPZM", "name": "Closet Shelf Dividers (6-pack)", "price": "$14.99"},
                  {"asin": "B08DC11C79", "name": "Hanging Closet Accessory Organizer", "price": "$16.99"}]},
]

PAGES_BASE = "https://ianmcwherter.github.io/golden-home-project/videos/transformation"


def amazon(asin, tag):
    return f"https://www.amazon.com/dp/{asin}?tag={tag}"


def today_str():
    return datetime.now().strftime("%Y-%m-%d")


def refresh_yt_token(token_path):
    with open(token_path) as f:
        t = json.load(f)
    required = {"token_uri", "client_id", "client_secret", "refresh_token"}
    missing = required - t.keys()
    if missing:
        raise RuntimeError(f"YT token JSON missing keys: {missing}")
    resp = requests.post(t["token_uri"], data={
        "client_id": t["client_id"], "client_secret": t["client_secret"],
        "refresh_token": t["refresh_token"], "grant_type": "refresh_token",
    }, timeout=30)
    result = resp.json()
    if "access_token" in result:
        t["token"] = result["access_token"]
        t["expiry"] = (datetime.now(timezone.utc) + timedelta(seconds=result.get("expires_in", 3600))).isoformat()
        with open(token_path, "w") as f:
            json.dump(t, f, indent=2)
        return t
    raise RuntimeError(f"Token refresh failed: {result}")


def build_description(title, products, tag):
    lines = [title, "", "🔥 SHOP THESE PRODUCTS:"]
    for i, p in enumerate(products):
        lines.append(f"#{i+1} {p['name']} — {p['price']}")
        lines.append(f"   ➡️ {amazon(p['asin'], tag)}")
    lines += [
        "", "Everything is linked above. Ships fast from Amazon.",
        "🏠 More home finds: goldenhomeproject.com",
        "👉 Follow: @goldenhomeproject",
        "", "⚠️ As an Amazon Associate I earn from qualifying purchases.",
        "", "#amazonfinds #homedecor #homeorganization #roomtransformation #shorts",
    ]
    return "\n".join(lines)


def build_pin_comment(products, tag):
    lines = ["📌 SHOP ALL PRODUCTS — Amazon links:\n"]
    symbols = "①②③④⑤"
    for i, p in enumerate(products[:5]):
        lines.append(f"{symbols[i]} {p['name']} — {p['price']}")
        lines.append(f"   🛒 {amazon(p['asin'], tag)}")
    lines += ["", "🏠 goldenhomeproject.com",
              "⚠️ Amazon Associate — qualifying purchases earn commission."]
    return "\n".join(lines)


def post_yt_short(video_path, title, description, pin_comment, yt_token):
    token = yt_token.get("token") or yt_token.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    metadata = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": ["amazonfinds", "homedecor", "homeorganization", "roomtransformation", "shorts"],
            "categoryId": "26",
        },
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
    }
    init = requests.post(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        headers={**headers, "Content-Type": "application/json", "X-Upload-Content-Type": "video/mp4"},
        json=metadata, timeout=30,
    )
    if init.status_code != 200:
        print(f"  [YT] Init failed: {init.status_code} {init.text[:200]}")
        return None

    upload_url = init.headers["Location"]
    file_size = os.path.getsize(video_path)
    with open(video_path, "rb") as f:
        upload = requests.put(
            upload_url, data=f,
            headers={**headers, "Content-Type": "video/mp4", "Content-Length": str(file_size)},
            timeout=300,
        )

    result = upload.json()
    if "id" not in result:
        print(f"  [YT] Upload failed: {result}")
        return None

    video_id = result["id"]
    print(f"  [YT] ✓ https://youtube.com/shorts/{video_id}")

    time.sleep(8)
    cr = requests.post(
        "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet",
        headers={**headers, "Content-Type": "application/json"},
        json={"snippet": {"videoId": video_id,
                          "topLevelComment": {"snippet": {"textOriginal": pin_comment}}}},
        timeout=30,
    )
    if "id" in cr.json():
        print(f"  [YT Comment] ✓ Affiliate links pinned")
    return video_id


def post_ig_reel(video_index, caption, meta_tokens):
    token = meta_tokens["page_access_token"]
    ig_id = meta_tokens["ig_business_account_id"]
    video_url = f"{PAGES_BASE}/trans_{video_index:03d}.mp4"
    api = "https://graph.facebook.com/v19.0"

    resp = requests.post(f"{api}/{ig_id}/media", data={
        "media_type": "REELS", "video_url": video_url,
        "caption": caption, "access_token": token,
    }, timeout=30)
    container = resp.json()
    if "id" not in container:
        print(f"  [IG] Container failed: {container}")
        return None

    status_code = None
    for _ in range(18):
        time.sleep(10)
        s = requests.get(f"{api}/{container['id']}",
                         params={"fields": "status_code", "access_token": token},
                         timeout=15).json()
        status_code = s.get("status_code")
        if status_code == "FINISHED":
            break
        if status_code == "ERROR":
            print(f"  [IG] Container processing failed: {s}")
            return None

    if status_code != "FINISHED":
        print(f"  [IG] Container never finished (last status: {status_code})")
        return None

    pub = requests.post(f"{api}/{ig_id}/media_publish",
                        data={"creation_id": container["id"], "access_token": token},
                        timeout=30)
    result = pub.json()
    if "id" in result:
        print(f"  [IG] ✓ Reel published: {result['id']}")
        return result["id"]
    print(f"  [IG] ✗ {result}")
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--yt-token", required=True)
    parser.add_argument("--meta-token", required=True)
    parser.add_argument("--associate-tag", default="goldenhomep06-20")
    parser.add_argument("--date", default=None, help="Override date (YYYY-MM-DD)")
    args = parser.parse_args()

    today = args.date or today_str()
    is_saturday = datetime.strptime(today, "%Y-%m-%d").weekday() == 5

    print(f"\n{'='*60}")
    print(f"GHP DAILY POSTER (GitHub Actions) — {today}")
    print(f"{'='*60}")

    # Find today's entry
    entry = next((e for e in APRIL_CALENDAR if e["date"] == today), None)
    if not entry:
        print(f"  No content scheduled for {today}. Done.")
        sys.exit(0)

    # Find video index (1-based position in calendar)
    video_index = APRIL_CALENDAR.index(entry) + 1
    video_path = VIDEOS_DIR / f"trans_{video_index:03d}.mp4"

    title    = entry["title"]
    products = entry.get("products", [])
    tag      = args.associate_tag

    print(f"  Title:   {title}")
    print(f"  Video:   trans_{video_index:03d}.mp4")
    print(f"  Products: {len(products)}")

    if not video_path.exists():
        print(f"  ERROR: {video_path} not found. Commit videos to repo first.")
        sys.exit(1)

    yt_token     = refresh_yt_token(args.yt_token)
    with open(args.meta_token) as f:
        meta_tokens = json.load(f)

    description  = build_description(title, products, tag)
    pin_comment  = build_pin_comment(products, tag)
    yt_title     = f"{title} #shorts #amazonfinds #homedecor"

    print(f"\n  Uploading to YouTube...")
    yt_id = post_yt_short(str(video_path), yt_title, description, pin_comment, yt_token)

    ig_id = None
    if is_saturday and entry.get("ig"):
        print(f"\n  Posting to Instagram (Saturday)...")
        ig_caption = (
            f"{title} 🏠✨\n\n"
            + "\n".join(f"{i+1}️⃣ {p['name']} — {p['price']}" for i, p in enumerate(products))
            + "\n\nAll links in bio — goldenhomeproject.com 🔗\n\n"
            + "#amazonfinds #homedecor #homeorganization #roomtransformation"
        )
        ig_id = post_ig_reel(video_index, ig_caption, meta_tokens)

    log = {"date": today, "title": title, "youtube": yt_id, "instagram": ig_id,
           "video": f"trans_{video_index:03d}.mp4"}
    log_path = LOGS_DIR / f"gh_post_{today}.json"
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)

    print(f"\n  Log saved: {log_path}")
    print(f"  YouTube: {'✓ ' + yt_id if yt_id else '✗ failed'}")
    print(f"  Instagram: {'✓' if ig_id else 'skipped' if not is_saturday else '✗ failed'}")


if __name__ == "__main__":
    main()
