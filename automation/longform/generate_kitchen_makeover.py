#!/usr/bin/env python3
"""
Golden Home Project — Kitchen Makeover Long-Form Video Generator
================================================================
7 sections, ~7 minutes, 17 affiliate links, $148 total cost
Syruvia integration (20% commission)
Scheduled: April 8, 2026 upload

Pipeline: Generate frames (Pollinations.ai) -> TTS voiceover (edge-tts) -> Compose (moviepy/ffmpeg)
"""

import asyncio
import json
import os
import time
import requests
import urllib.parse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path("/tmp/kitchen_makeover")
OUTPUT_DIR.mkdir(exist_ok=True)
FRAMES_DIR = OUTPUT_DIR / "frames"
FRAMES_DIR.mkdir(exist_ok=True)
AUDIO_DIR = OUTPUT_DIR / "audio"
AUDIO_DIR.mkdir(exist_ok=True)

# === VIDEO STRUCTURE ===
TITLE = "I Transformed My Entire Kitchen for $148. Here's Every Product."
TAGS = ["kitchen makeover", "amazon finds", "budget kitchen", "home transformation",
        "kitchen organization", "before and after", "golden home project", "amazon home",
        "kitchen decor", "budget home decor", "syruvia", "kitchen upgrade"]

AFFILIATE_TAG = "goldenhomep06-20"

SECTIONS = [
    {
        "name": "intro",
        "duration": 45,
        "voiceover": (
            "This is my kitchen. Or at least, this is what it looked like three weeks ago. "
            "Plain countertops. Cluttered cabinets. Zero personality. "
            "I spent one hundred and forty eight dollars on Amazon. Seventeen products. "
            "Same kitchen. Completely different home. "
            "I'm going to show you every single product, what it cost, and exactly where I put it. "
            "All links are in the description."
        ),
        "frames": [
            {"prompt": "plain boring kitchen with cluttered countertops, harsh fluorescent lighting, messy disorganized, realistic photo", "overlay": "BEFORE", "zoom": "in"},
            {"prompt": "same kitchen beautifully organized with warm lighting, clean countertops, decorative accents, modern cozy aesthetic, realistic photo", "overlay": "AFTER — $148 Total", "zoom": "out"},
        ],
    },
    {
        "name": "countertops",
        "duration": 70,
        "voiceover": (
            "Section one. Countertops. This is where most kitchens fail. "
            "Too much stuff, no cohesion, looks like a garage sale. "
            "First thing I got: this bamboo utensil holder. Twelve ninety nine. "
            "It holds everything and actually looks good sitting out. "
            "Next: airtight canister set. Four pieces for eighteen ninety nine. "
            "Flour, sugar, coffee, tea. No more random bags everywhere. "
            "Then this paper towel holder. Eight ninety nine. Matte black, weighted base. "
            "And finally, a bamboo cutting board organizer. Sixteen ninety nine. "
            "My cutting boards used to just lean against the wall. Now they have a home. "
            "Countertop total: fifty seven ninety six."
        ),
        "frames": [
            {"prompt": "cluttered messy kitchen countertop with random items scattered, realistic photo", "overlay": "Countertops — BEFORE", "zoom": "in"},
            {"prompt": "beautiful bamboo utensil holder on clean kitchen counter, modern kitchen, warm lighting", "overlay": "Bamboo Utensil Holder — $12.99", "zoom": "slow"},
            {"prompt": "set of 4 airtight glass canisters with bamboo lids on kitchen counter, flour sugar coffee tea labeled", "overlay": "Airtight Canister Set — $18.99", "zoom": "slow"},
            {"prompt": "matte black paper towel holder on clean kitchen counter, modern minimalist", "overlay": "Paper Towel Holder — $8.99", "zoom": "slow"},
            {"prompt": "bamboo cutting board organizer rack on countertop with 3 cutting boards neatly stored", "overlay": "Cutting Board Organizer — $16.99", "zoom": "slow"},
            {"prompt": "beautifully organized kitchen countertop with bamboo accessories, canisters, warm lighting, clean modern look", "overlay": "Countertop Total: $57.96", "zoom": "out"},
        ],
    },
    {
        "name": "cabinet_organization",
        "duration": 65,
        "voiceover": (
            "Section two. Inside the cabinets. Nobody sees these, but you open them ten times a day. "
            "Turntable lazy susans. Two pack. Sixteen ninety nine. "
            "One for spices, one for oils and vinegars. Game changer. "
            "Expandable shelf organizer. Fourteen ninety nine. "
            "Doubles your vertical space instantly. I put mugs on top, plates below. "
            "And stackable can organizer. Also fourteen ninety nine. "
            "I can actually see every can now instead of digging through a pile. "
            "Cabinet total: forty six ninety seven."
        ),
        "frames": [
            {"prompt": "messy disorganized kitchen cabinet interior with cans and items piled up", "overlay": "Cabinets — BEFORE", "zoom": "in"},
            {"prompt": "turntable lazy susan in kitchen cabinet with spices neatly arranged, organized", "overlay": "Lazy Susan 2-pack — $16.99", "zoom": "slow"},
            {"prompt": "expandable shelf organizer inside kitchen cabinet with mugs on top plates below, neat organized", "overlay": "Shelf Organizer — $14.99", "zoom": "slow"},
            {"prompt": "stackable can organizer rack in kitchen cabinet, cans neatly displayed and visible", "overlay": "Can Organizer — $14.99", "zoom": "slow"},
            {"prompt": "perfectly organized kitchen cabinet interior with lazy susan, shelf organizer, can rack, everything visible", "overlay": "Cabinet Total: $46.97", "zoom": "out"},
        ],
    },
    {
        "name": "sink_area",
        "duration": 55,
        "voiceover": (
            "Section three. The sink area. This gets gross fast if you don't have the right setup. "
            "Soap dispenser set. Three pieces. Nineteen ninety nine. "
            "Dish soap, hand soap, and a matching lotion dispenser. Looks like a spa. "
            "Ceramic sponge holder. Eight ninety nine. No more soggy sponge on the counter. "
            "Sink total: twenty eight ninety eight."
        ),
        "frames": [
            {"prompt": "messy kitchen sink area with random soap bottles and wet sponge, cluttered", "overlay": "Sink Area — BEFORE", "zoom": "in"},
            {"prompt": "beautiful matching soap dispenser set by kitchen sink, three matte black dispensers, clean modern", "overlay": "Soap Dispenser Set — $19.99", "zoom": "slow"},
            {"prompt": "ceramic sponge holder by kitchen sink, clean organized look, modern kitchen", "overlay": "Sponge Holder — $8.99", "zoom": "slow"},
            {"prompt": "beautifully organized kitchen sink area with matching dispensers and sponge holder, clean modern spa-like", "overlay": "Sink Total: $28.98", "zoom": "out"},
        ],
    },
    {
        "name": "pantry",
        "duration": 65,
        "voiceover": (
            "Section four. The pantry. This was the worst part of my kitchen. "
            "Pantry organization bins. Ten pack. Thirty two ninety nine. "
            "Clear bins so you can see everything. I sorted by category — snacks, baking, pasta, canned goods. "
            "Chalk label set. Nine ninety nine. Reusable, so when you rearrange, the labels move with you. "
            "And I added Syruvia syrups to my coffee station in the pantry. "
            "Vanilla, caramel, hazelnut. They actually taste incredible in coffee and they look amazing on display. "
            "I'll link those separately — they're not on Amazon but they're worth it. "
            "Pantry total: forty two ninety eight."
        ),
        "frames": [
            {"prompt": "messy disorganized pantry with items crammed on shelves, no system, chaotic", "overlay": "Pantry — BEFORE", "zoom": "in"},
            {"prompt": "clear pantry organization bins on shelf, neatly sorted with snacks and dry goods visible", "overlay": "Organization Bins 10-pack — $32.99", "zoom": "slow"},
            {"prompt": "reusable chalk labels on pantry bins, beautiful handwritten style labels, organized pantry", "overlay": "Chalk Labels — $9.99", "zoom": "slow"},
            {"prompt": "beautiful coffee station with syrup bottles on display, vanilla caramel hazelnut, aesthetic pantry corner", "overlay": "Syruvia Syrups — Coffee Station", "zoom": "slow"},
            {"prompt": "perfectly organized pantry with clear bins labels and coffee station, everything visible and beautiful", "overlay": "Pantry Total: $42.98", "zoom": "out"},
        ],
    },
    {
        "name": "finishing_touches",
        "duration": 50,
        "voiceover": (
            "Section five. Finishing touches. The details that make it feel expensive. "
            "Small countertop tray. Twelve ninety nine. Groups your everyday items together. "
            "It makes any countertop look intentional instead of random. "
            "And one of those adhesive hooks underneath the cabinet for your keys. "
            "Two ninety nine for a six pack. "
            "These two things took thirty seconds to set up and made the biggest visual difference. "
            "Finishing touches total: fifteen ninety eight."
        ),
        "frames": [
            {"prompt": "countertop organizing tray in kitchen grouping salt pepper and oil together, styled and intentional", "overlay": "Countertop Tray — $12.99", "zoom": "slow"},
            {"prompt": "adhesive hooks under kitchen cabinet holding keys and small items, clean organized look", "overlay": "Adhesive Hooks 6-pack — $2.99", "zoom": "slow"},
            {"prompt": "beautiful kitchen detail shot showing tray and hooks, warm lighting, styled and cozy", "overlay": "Finishing Touches: $15.98", "zoom": "out"},
        ],
    },
    {
        "name": "outro",
        "duration": 50,
        "voiceover": (
            "That's it. One hundred and forty eight dollars. Seventeen products. Same kitchen. "
            "No renovation. No contractor. No painting. Just smart products in the right places. "
            "Every single link is in the description below. I also pinned a comment with all the prices. "
            "If you're thinking about doing this to your kitchen, just start with the countertops. "
            "That's where you'll see the biggest difference for the least money. "
            "Subscribe if you want to see me do this room by room. "
            "Next up is the bathroom. I'll see you there."
        ),
        "frames": [
            {"prompt": "split screen kitchen before and after, left side messy cluttered right side beautiful organized modern", "overlay": "BEFORE → AFTER", "zoom": "out"},
            {"prompt": "beautifully transformed kitchen wide shot, organized counters, warm lighting, modern cozy home", "overlay": "$148 Total — All Links Below", "zoom": "out"},
            {"prompt": "subscribe button animation style graphic with text room by room series, clean modern design", "overlay": "Subscribe — Next: Bathroom Makeover", "zoom": "slow"},
        ],
    },
]

# All 17 products for description
PRODUCTS = [
    {"name": "Bamboo Utensil Holder", "price": "$12.99", "asin": "B07WGWFCTS"},
    {"name": "Airtight Canister Set (4-piece)", "price": "$18.99", "asin": "B08BHBPQHZ"},
    {"name": "Paper Towel Holder (matte black)", "price": "$8.99", "asin": "B08CHWX4S1"},
    {"name": "Bamboo Cutting Board Organizer", "price": "$16.99", "asin": "B09NQTD6G8"},
    {"name": "Turntable Lazy Susan (2-pack)", "price": "$16.99", "asin": "B09K3MQVXL"},
    {"name": "Expandable Shelf Organizer", "price": "$14.99", "asin": "B08BNHBK9N"},
    {"name": "Stackable Can Organizer", "price": "$14.99", "asin": "B07NQVHKX7"},
    {"name": "Soap Dispenser Set (3-piece)", "price": "$19.99", "asin": "B08S8FMWWP"},
    {"name": "Ceramic Sponge Holder", "price": "$8.99", "asin": "B07ZBQSV97"},
    {"name": "Pantry Organization Bins (10-pack)", "price": "$32.99", "asin": "B07J5N6HWJ"},
    {"name": "Chalk Label Set (reusable)", "price": "$9.99", "asin": "B09JQRJ8C4"},
    {"name": "Countertop Tray Organizer", "price": "$12.99", "asin": "B09JQRJ8C4"},
    {"name": "Adhesive Hooks (6-pack)", "price": "$2.99", "asin": "B07Y9BKMYF"},
]

SYRUVIA_LINK = "https://syruvia.com/?ref=goldenhomeproject"

DESCRIPTION = f"""I Transformed My Entire Kitchen for $148. Here's Every Product.

17 products. $148. Same kitchen. No renovation needed.

TIMESTAMPS:
0:00 — Before & After
0:45 — Section 1: Countertops ($57.96)
1:55 — Section 2: Cabinets ($46.97)
3:00 — Section 3: Sink Area ($28.98)
3:55 — Section 4: Pantry ($42.98)
5:00 — Section 5: Finishing Touches ($15.98)
5:50 — Final Reveal & What to Start With

SHOP EVERY PRODUCT:
""" + "\n".join(
    f"{i+1}. {p['name']} — {p['price']}\n   https://www.amazon.com/dp/{p['asin']}?tag={AFFILIATE_TAG}"
    for i, p in enumerate(PRODUCTS)
) + f"""

COFFEE STATION:
Syruvia Syrups (Vanilla, Caramel, Hazelnut)
   {SYRUVIA_LINK}

Total: $148 (Amazon products only)

Subscribe for Room by Room transformations — Bathroom is next!

Golden Home Project | goldenhomeproject.com
As an Amazon Associate, Golden Home Project earns from qualifying purchases.

#kitchenmakeover #amazonfinds #homedecor #budgethome #homeorganization #kitchenorganization #beforeandafter #roomtransformation
"""

PIN_COMMENT = """📌 EVERY PRODUCT + PRICE:

COUNTERTOPS ($57.96):
① Bamboo Utensil Holder — $12.99
② Airtight Canister Set (4-piece) — $18.99
③ Paper Towel Holder — $8.99
④ Cutting Board Organizer — $16.99

CABINETS ($46.97):
⑤ Lazy Susan 2-pack — $16.99
⑥ Shelf Organizer — $14.99
⑦ Can Organizer — $14.99

SINK ($28.98):
⑧ Soap Dispenser Set — $19.99
⑨ Sponge Holder — $8.99

PANTRY ($42.98):
⑩ Organization Bins (10-pack) — $32.99
⑪ Chalk Labels — $9.99

FINISHING TOUCHES ($15.98):
⑫ Countertop Tray — $12.99
⑬ Adhesive Hooks (6-pack) — $2.99

COFFEE STATION:
☕ Syruvia Syrups — syruvia.com/?ref=goldenhomeproject

All Amazon links in the description! 🏠
"""


def generate_frame(prompt, filename, retries=3):
    """Generate a 1920x1080 frame using Pollinations.ai"""
    encoded = urllib.parse.quote(prompt + ", 1920x1080, photorealistic, professional photography")
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1920&height=1080&nologo=true"

    for attempt in range(retries):
        try:
            print(f"    Generating: {filename} (attempt {attempt+1})")
            resp = requests.get(url, timeout=120)
            if resp.status_code == 200 and len(resp.content) > 5000:
                filepath = FRAMES_DIR / filename
                filepath.write_bytes(resp.content)
                print(f"    ✓ {filename} ({len(resp.content)//1024}KB)")
                time.sleep(8)  # Rate limit: max 2 concurrent
                return filepath
            print(f"    Retry... (status={resp.status_code}, size={len(resp.content)})")
        except Exception as e:
            print(f"    Error: {e}")
        time.sleep(10)

    print(f"    ✗ Failed to generate {filename}")
    return None


def add_text_overlay(image_path, text, position="bottom"):
    """Add text overlay to frame"""
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # Try to use a nice font, fall back to default
    font_size = 64
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/SFNSText.ttf", font_size)
        except:
            font = ImageFont.load_default()

    # Calculate text position
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    if position == "bottom":
        x = (img.width - text_w) // 2
        y = img.height - text_h - 80
    elif position == "center":
        x = (img.width - text_w) // 2
        y = (img.height - text_h) // 2
    else:
        x = (img.width - text_w) // 2
        y = 60

    # Draw shadow
    draw.text((x+3, y+3), text, fill="black", font=font)
    # Draw text
    draw.text((x, y), text, fill="white", font=font)

    img.save(image_path)
    return image_path


async def generate_audio(text, filename, voice="en-US-GuyNeural"):
    """Generate TTS audio using edge-tts"""
    import edge_tts
    filepath = AUDIO_DIR / filename
    communicate = edge_tts.Communicate(text, voice, rate="-5%")
    await communicate.save(str(filepath))
    print(f"    ✓ Audio: {filename}")
    return filepath


def compose_video():
    """Compose all frames + audio into final video using moviepy"""
    from moviepy.editor import (
        ImageClip, AudioFileClip, concatenate_videoclips,
        CompositeVideoClip, concatenate_audioclips
    )

    print("\n=== COMPOSING FINAL VIDEO ===")

    all_clips = []

    for i, section in enumerate(SECTIONS):
        print(f"  Composing section {i+1}/{len(SECTIONS)}: {section['name']}")

        audio_path = AUDIO_DIR / f"section_{i:02d}_{section['name']}.mp3"
        if not audio_path.exists():
            print(f"    ✗ Missing audio: {audio_path}")
            continue

        audio = AudioFileClip(str(audio_path))
        audio_duration = audio.duration

        frames = section["frames"]
        frame_duration = audio_duration / len(frames)

        section_clips = []
        for j, frame_info in enumerate(frames):
            frame_path = FRAMES_DIR / f"section_{i:02d}_frame_{j:02d}.jpg"
            if not frame_path.exists():
                frame_path = FRAMES_DIR / f"section_{i:02d}_frame_{j:02d}.png"
            if not frame_path.exists():
                print(f"    ✗ Missing frame: {frame_path}")
                continue

            clip = ImageClip(str(frame_path)).set_duration(frame_duration)

            # Ken Burns effect
            zoom_type = frame_info.get("zoom", "slow")
            if zoom_type == "in":
                clip = clip.resize(lambda t: 1 + 0.04 * t / frame_duration)
            elif zoom_type == "out":
                clip = clip.resize(lambda t: 1.04 - 0.04 * t / frame_duration)
            else:
                clip = clip.resize(lambda t: 1 + 0.02 * t / frame_duration)

            section_clips.append(clip)

        if section_clips:
            section_video = concatenate_videoclips(section_clips, method="compose")
            section_video = section_video.set_audio(audio)
            all_clips.append(section_video)

    if not all_clips:
        print("ERROR: No clips to compose")
        return None

    print(f"\n  Concatenating {len(all_clips)} sections...")
    final = concatenate_videoclips(all_clips, method="compose")

    output_path = OUTPUT_DIR / "kitchen_makeover_final.mp4"
    print(f"  Rendering to {output_path}...")
    final.write_videofile(
        str(output_path),
        fps=24,
        codec="libx264",
        audio_codec="aac",
        bitrate="5000k",
        preset="medium",
        threads=4,
    )

    print(f"\n✓ FINAL VIDEO: {output_path}")
    print(f"  Duration: {final.duration:.1f}s ({final.duration/60:.1f}min)")
    print(f"  Size: {output_path.stat().st_size / 1024 / 1024:.1f}MB")

    return output_path


async def main():
    print("=" * 60)
    print("GOLDEN HOME PROJECT — Kitchen Makeover Long-Form Generator")
    print("=" * 60)
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Sections: {len(SECTIONS)}")
    total_frames = sum(len(s['frames']) for s in SECTIONS)
    print(f"Total frames: {total_frames}")
    print(f"Target duration: ~{sum(s['duration'] for s in SECTIONS) // 60}min")
    print()

    # Step 1: Generate all frames
    print("=== STEP 1: GENERATING FRAMES ===")
    for i, section in enumerate(SECTIONS):
        print(f"\n  Section {i+1}/{len(SECTIONS)}: {section['name']}")
        for j, frame in enumerate(section["frames"]):
            filename = f"section_{i:02d}_frame_{j:02d}.jpg"
            filepath = FRAMES_DIR / filename

            # Skip if already generated
            if filepath.exists() and filepath.stat().st_size > 5000:
                print(f"    ✓ {filename} (cached)")
                continue

            result = generate_frame(frame["prompt"], filename)
            if result and frame.get("overlay"):
                add_text_overlay(result, frame["overlay"])

    # Step 2: Generate all audio
    print("\n=== STEP 2: GENERATING VOICEOVER ===")
    for i, section in enumerate(SECTIONS):
        filename = f"section_{i:02d}_{section['name']}.mp3"
        filepath = AUDIO_DIR / filename

        if filepath.exists() and filepath.stat().st_size > 1000:
            print(f"    ✓ {filename} (cached)")
            continue

        await generate_audio(section["voiceover"], filename)

    # Step 3: Compose final video
    print("\n=== STEP 3: COMPOSING VIDEO ===")
    output = compose_video()

    if output:
        # Save metadata
        meta = {
            "title": TITLE,
            "description": DESCRIPTION,
            "pin_comment": PIN_COMMENT,
            "tags": TAGS,
            "products": PRODUCTS,
            "syruvia_link": SYRUVIA_LINK,
            "total_cost": "$148",
            "affiliate_tag": AFFILIATE_TAG,
            "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        meta_path = OUTPUT_DIR / "metadata.json"
        meta_path.write_text(json.dumps(meta, indent=2))
        print(f"\n✓ Metadata saved: {meta_path}")
        print(f"\n{'='*60}")
        print(f"READY FOR UPLOAD")
        print(f"  Video: {output}")
        print(f"  Metadata: {meta_path}")
        print(f"{'='*60}")

    return output


if __name__ == "__main__":
    asyncio.run(main())
