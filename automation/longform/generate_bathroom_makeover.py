#!/usr/bin/env python3
"""
Generate Bathroom Makeover Long-Form Video for Golden Home Project.
Target: 5-7 min, 15+ affiliate links, transformation format.
Pipeline: Pollinations.ai frames → edge-tts voiceover → ffmpeg composition
"""
import json
import os
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path

OUTPUT_DIR = Path("/tmp/bathroom_makeover")
FRAMES_DIR = OUTPUT_DIR / "frames"
AUDIO_DIR = OUTPUT_DIR / "audio"

for d in [OUTPUT_DIR, FRAMES_DIR, AUDIO_DIR]:
    d.mkdir(parents=True, exist_ok=True)

AMAZON_TAG = "goldenhomep06-20"

# ── PRODUCTS (15 total) ──
PRODUCTS = [
    {"name": "Bamboo Over-Toilet Storage Shelf", "price": "$32.99", "asin": "B08CZHVQJ4"},
    {"name": "Bathroom Accessories Set (4-piece)", "price": "$21.99", "asin": "B08S8FMWWP"},
    {"name": "Rust-Proof Corner Shower Shelf", "price": "$22.99", "asin": "B08XZV1H87"},
    {"name": "Under-Sink Organizer with Adjustable Shelf", "price": "$19.99", "asin": "B08CW3M5P4"},
    {"name": "Bathroom Storage Bins 3-pack", "price": "$14.99", "asin": "B07D8CTHXF"},
    {"name": "Ceramic Soap Dispenser Set", "price": "$19.99", "asin": "B08S8FMWWP"},
    {"name": "Bamboo Bath Mat", "price": "$29.99", "asin": "B07WLXJ8TB"},
    {"name": "LED Vanity Mirror (rechargeable)", "price": "$24.99", "asin": "B09G9FKWG3"},
    {"name": "Waffle Weave Shower Curtain", "price": "$16.99", "asin": "B07XVFBXWF"},
    {"name": "Adhesive Towel Hooks 6-pack", "price": "$12.99", "asin": "B07Y9BKMYF"},
    {"name": "Countertop Tray Organizer (marble look)", "price": "$14.99", "asin": "B09JQRJ8C4"},
    {"name": "Glass Apothecary Jars 3-pack", "price": "$18.99", "asin": "B08BHBPQHZ"},
    {"name": "Bamboo Toothbrush Holder", "price": "$9.99", "asin": "B07ZBQSV97"},
    {"name": "Shower Caddy Tension Pole", "price": "$26.99", "asin": "B08BNHBK9N"},
    {"name": "Eucalyptus Shower Bundle (artificial)", "price": "$8.99", "asin": "B09NQTD6G8"},
]

TOTAL_COST = "$297"

# ── VIDEO SECTIONS ──
SECTIONS = [
    {
        "name": "intro",
        "voiceover": "My bathroom looked like every other rental bathroom in America. Builder-grade mirror. Plastic soap dispenser from the dollar store. Towels thrown over the shower rod. Same bathroom. Two hundred ninety seven dollars. No renovation. Here's every single product I used.",
        "frames": [
            "A dull beige rental bathroom with cheap fixtures, cluttered counter, mismatched towels on the shower rod, harsh overhead lighting, realistic photo",
            "The same bathroom transformed into a spa-like retreat with bamboo accents, coordinated white towels, eucalyptus hanging from the showerhead, warm lighting, clean and organized, realistic photo",
        ],
    },
    {
        "name": "shower_area",
        "voiceover": "Let's start with the shower. This rust-proof corner shelf replaced that disgusting suction cup caddy that kept falling. Twenty two ninety nine. I also added this tension pole shower caddy for twenty six ninety nine. It holds everything — shampoo, conditioner, body wash — and it doesn't move. The waffle weave shower curtain was sixteen ninety nine and instantly made the whole bathroom look more expensive. And this eucalyptus bundle? Eight ninety nine. It's artificial, so it lasts forever, and your bathroom smells like a spa every time you shower.",
        "frames": [
            "A clean modern shower with a rust-proof stainless steel corner shelf holding neatly arranged bottles, tiled wall, realistic photo",
            "A tension pole shower caddy in a white shower with three tiers holding bottles, chrome finish, clean and organized, realistic photo",
            "A white waffle weave shower curtain in a bathroom, elegant hotel-like appearance, soft natural light, realistic photo",
            "A bundle of eucalyptus leaves hanging from a chrome showerhead, spa-like bathroom atmosphere, steam and greenery, realistic photo",
            "Wide shot of the complete transformed shower area with corner shelf, tension caddy, waffle curtain, and eucalyptus, cohesive spa look, realistic photo",
        ],
    },
    {
        "name": "vanity_counter",
        "voiceover": "The vanity was the biggest mess. Everything just piled up on the counter. First, this marble-look tray organizer for fourteen ninety nine. It corrals everything into one spot. The ceramic soap dispenser set replaced the plastic bottles — nineteen ninety nine for a set that looks like it came from a boutique hotel. I added a bamboo toothbrush holder for nine ninety nine. And these glass apothecary jars? Eighteen ninety nine for a three pack. Cotton balls, Q-tips, bath salts. Everything visible but contained. The LED vanity mirror was twenty four ninety nine. Rechargeable, perfect lighting for getting ready.",
        "frames": [
            "A messy bathroom vanity counter with scattered products, toothpaste, various bottles, unorganized, realistic photo",
            "A marble-look tray organizer on a bathroom counter with neatly arranged items, soap dispenser, candle, minimalist style, realistic photo",
            "A matching ceramic soap dispenser set on a clean white bathroom counter, hotel-quality appearance, realistic photo",
            "Three glass apothecary jars on a bathroom counter filled with cotton balls, Q-tips, and bath salts, organized and decorative, realistic photo",
            "A rechargeable LED vanity mirror on a bathroom counter with soft warm lighting, elegant setup, realistic photo",
            "Wide shot of the fully organized vanity counter with tray, dispensers, jars, and mirror, spa-like and clean, realistic photo",
        ],
    },
    {
        "name": "storage_organization",
        "voiceover": "Storage was the real problem. There was nowhere to put anything. This bamboo over-toilet shelf was thirty two ninety nine and it tripled my storage space instantly. Three tiers. I put towels on top, baskets in the middle, and decorative items on the bottom shelf. The under-sink organizer was nineteen ninety nine. Adjustable shelf that works around the pipes. And these storage bins? Fourteen ninety nine for a three pack. They slide out like drawers now.",
        "frames": [
            "A bamboo three-tier over-toilet storage shelf with rolled white towels on top, woven baskets in middle, and a small plant on bottom, clean bathroom, realistic photo",
            "An under-sink cabinet opened to show a two-tier adjustable organizer working around plumbing pipes, bathroom products neatly stored, realistic photo",
            "White storage bins arranged as pull-out drawers under a bathroom sink, organized cleaning supplies and toiletries, realistic photo",
            "Wide shot showing the bathroom with over-toilet shelf, organized under-sink storage visible, coordinated storage solutions, realistic photo",
        ],
    },
    {
        "name": "finishing_touches",
        "voiceover": "The finishing touches are what made this feel like a completely different room. A bamboo bath mat replaced the old fabric one — twenty nine ninety nine. It dries faster, looks cleaner, and lasts longer. Adhesive towel hooks — twelve ninety nine for a six pack. No drilling, no damage. I put them behind the door, next to the shower, everywhere I needed a towel. And the bathroom accessories set for twenty one ninety nine tied everything together. Matching trash can, toilet brush, and cup holder. Same finish. Same style.",
        "frames": [
            "A bamboo bath mat on a white tile bathroom floor next to a bathtub, natural wood look, clean minimalist bathroom, realistic photo",
            "Adhesive chrome towel hooks on a bathroom wall with neatly folded white towels hanging, no drill installation, realistic photo",
            "A matching bathroom accessories set including a small trash can, toilet brush holder, and cup on a bathroom counter, coordinated matte black finish, realistic photo",
        ],
    },
    {
        "name": "outro",
        "voiceover": "Same bathroom. Two hundred ninety seven dollars. No plumber. No contractor. No landlord permission needed. Every single product is linked in the description and pinned in the comments. If you're starting from scratch, start with the over-toilet shelf and the shower curtain. Those two things alone will change the whole feel. Subscribe for the next room — the living room is coming. And trust me, that transformation is even bigger.",
        "frames": [
            "A stunning side-by-side comparison of a rental bathroom before and after transformation, left side cluttered and dull, right side spa-like and organized, dramatic improvement, realistic photo",
            "A beautiful fully transformed spa-like bathroom with bamboo accents, white towels, eucalyptus on shower, organized vanity, warm lighting, magazine-worthy, realistic photo",
            "Golden Home Project text logo on a clean white background with a subtle home icon, subscribe button overlay, professional branding, realistic photo",
        ],
    },
]

# ── DESCRIPTION ──
DESCRIPTION = f"""I Transformed My Entire Bathroom for $297. Here's Every Product.

15 products. $297. Same bathroom. No renovation needed.

TIMESTAMPS:
0:00 — Before & After
0:40 — Section 1: Shower Area ($75.96)
2:00 — Section 2: Vanity Counter ($87.95)
3:30 — Section 3: Storage & Organization ($67.97)
4:30 — Section 4: Finishing Touches ($64.97)
5:30 — Final Reveal & Where to Start

SHOP EVERY PRODUCT:
""" + "\n".join(
    f"{i+1}. {p['name']} — {p['price']}\n   https://www.amazon.com/dp/{p['asin']}?tag={AMAZON_TAG}"
    for i, p in enumerate(PRODUCTS)
) + f"""

Total: $297 (all Amazon products)

Subscribe for Room by Room transformations — Living Room is next!

🏠 Golden Home Project | goldenhomeproject.com
As an Amazon Associate, Golden Home Project earns from qualifying purchases.

#bathroommakeover #amazonfinds #homedecor #budgethome #homeorganization #bathroomorganization #beforeandafter #roomtransformation #rentalfriendly #spabathroom
"""

PIN_COMMENT = "🛒 SHOP EVERY PRODUCT (affiliate links):\n\n" + "\n".join(
    f"{i+1}. {p['name']} — {p['price']} → https://www.amazon.com/dp/{p['asin']}?tag={AMAZON_TAG}"
    for i, p in enumerate(PRODUCTS)
) + "\n\nTotal: $297 for a complete bathroom transformation!\nSubscribe for the Living Room Makeover — coming next! 🏠"


def generate_frame(prompt, filename):
    """Generate image via Pollinations.ai"""
    if filename.exists() and filename.stat().st_size > 5000:
        print(f"    [cached] {filename.name}")
        return True
    import requests as req
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1920&height=1080&nologo=true"
    try:
        r = req.get(url, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            print(f"    ✗ {filename.name}: HTTP {r.status_code}")
            return False
        with open(filename, "wb") as f:
            f.write(r.content)
        size = filename.stat().st_size
        if size < 5000:
            print(f"    [too small: {size}B] {filename.name}")
            filename.unlink()
            return False
        print(f"    ✓ {filename.name} ({size//1024}KB)")
        return True
    except Exception as e:
        print(f"    ✗ {filename.name}: {e}")
        return False


def generate_voiceover(text, filename):
    """Generate voiceover via edge-tts"""
    if filename.exists():
        print(f"    [cached] {filename.name}")
        return True
    try:
        subprocess.run([
            "python3", "-m", "edge_tts",
            "--voice", "en-US-GuyNeural",
            "--text", text,
            "--write-media", str(filename),
        ], capture_output=True, text=True, check=True)
        print(f"    ✓ {filename.name}")
        return True
    except Exception as e:
        print(f"    ✗ {filename.name}: {e}")
        return False


def get_audio_duration(path):
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


def compose_video():
    """Compose final video from frames + audio using ffmpeg"""
    print("\n=== COMPOSING VIDEO ===\n")
    section_videos = []

    for i, section in enumerate(SECTIONS):
        section_name = section["name"]
        audio_path = AUDIO_DIR / f"section_{i:02d}_{section_name}.mp3"

        if not audio_path.exists():
            print(f"  SKIP section {i}: missing audio")
            continue

        audio_duration = get_audio_duration(audio_path)
        num_frames = len(section["frames"])
        frame_duration = audio_duration / num_frames

        print(f"  Section {i+1}/{len(SECTIONS)}: {section_name} ({audio_duration:.1f}s, {num_frames} frames, {frame_duration:.1f}s each)")

        concat_file = OUTPUT_DIR / f"concat_{i:02d}.txt"
        last_frame = None
        with open(concat_file, "w") as f:
            for j in range(num_frames):
                frame_path = FRAMES_DIR / f"section_{i:02d}_frame_{j:02d}.jpg"
                if not frame_path.exists():
                    frame_path = FRAMES_DIR / f"section_{i:02d}_frame_{j:02d}.png"
                if not frame_path.exists():
                    print(f"    MISSING: frame {j}")
                    continue
                f.write(f"file '{frame_path}'\n")
                f.write(f"duration {frame_duration}\n")
                last_frame = frame_path
            if last_frame:
                f.write(f"file '{last_frame}'\n")

        section_video = OUTPUT_DIR / f"section_{i:02d}.mp4"
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", str(concat_file),
            "-i", str(audio_path),
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
            "-c:v", "libx264", "-preset", "medium", "-crf", "23",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            str(section_video)
        ], capture_output=True, text=True)

        if section_video.exists() and section_video.stat().st_size > 1000:
            section_videos.append(section_video)
            print(f"    ✓ {section_video.name} ({section_video.stat().st_size // 1024}KB)")
        else:
            print(f"    ✗ Failed: {section_video.name}")

    if not section_videos:
        print("\nERROR: No section videos")
        return None

    # Concatenate all sections
    print(f"\n  Concatenating {len(section_videos)} sections...")
    final_concat = OUTPUT_DIR / "final_concat.txt"
    with open(final_concat, "w") as f:
        for sv in section_videos:
            f.write(f"file '{sv}'\n")

    raw_output = OUTPUT_DIR / "bathroom_makeover_raw.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(final_concat),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        str(raw_output)
    ], capture_output=True, text=True)

    # Re-encode at 24fps for YouTube
    final_output = OUTPUT_DIR / "bathroom_makeover_final.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(raw_output),
        "-vf", "fps=24",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        str(final_output)
    ], capture_output=True, text=True)

    if final_output.exists():
        size_mb = final_output.stat().st_size / 1024 / 1024
        dur = get_audio_duration(final_output)
        print(f"\n{'='*60}")
        print(f"✓ FINAL VIDEO: {final_output}")
        print(f"  Duration: {dur:.1f}s ({dur/60:.1f}min)")
        print(f"  Size: {size_mb:.1f}MB")
        print(f"{'='*60}")
        return final_output
    else:
        print("\nERROR: Final encoding failed")
        return None


def main():
    print("=" * 60)
    print("BATHROOM MAKEOVER LONG-FORM VIDEO GENERATOR")
    print("15 affiliate products | $297 total | Transformation format")
    print("=" * 60)

    # Step 1: Generate frames
    print("\n--- GENERATING FRAMES ---")
    total_frames = sum(len(s["frames"]) for s in SECTIONS)
    generated = 0
    for i, section in enumerate(SECTIONS):
        print(f"\n  Section {i+1}/{len(SECTIONS)}: {section['name']}")
        for j, prompt in enumerate(section["frames"]):
            filename = FRAMES_DIR / f"section_{i:02d}_frame_{j:02d}.jpg"
            if generate_frame(prompt, filename):
                generated += 1
            time.sleep(8)  # Rate limit
    print(f"\n  Frames: {generated}/{total_frames}")

    # Step 2: Generate voiceovers
    print("\n--- GENERATING VOICEOVERS ---")
    for i, section in enumerate(SECTIONS):
        print(f"\n  Section {i+1}/{len(SECTIONS)}: {section['name']}")
        filename = AUDIO_DIR / f"section_{i:02d}_{section['name']}.mp3"
        generate_voiceover(section["voiceover"], filename)

    # Step 3: Compose video
    result = compose_video()

    # Step 4: Save description
    desc_path = OUTPUT_DIR / "description.txt"
    with open(desc_path, "w") as f:
        f.write(DESCRIPTION)
    print(f"\nDescription saved to {desc_path}")

    # Step 5: Save pin comment
    comment_path = OUTPUT_DIR / "pin_comment.txt"
    with open(comment_path, "w") as f:
        f.write(PIN_COMMENT)

    if result:
        print(f"\n✓ ALL DONE! Video ready for upload.")
        print(f"  Video: {result}")
        print(f"  Description: {desc_path}")
        print(f"  Pin comment: {comment_path}")

        # Backup to Desktop
        import shutil
        desktop = Path.home() / "Desktop" / "Golden Home Project Content files"
        if desktop.exists():
            shutil.copy2(result, desktop / "Bathroom_Makeover_LongForm.mp4")
            shutil.copy2(desc_path, desktop / "Bathroom_Makeover_Description.txt")
            print(f"\n  Backed up to Desktop folder ✓")


if __name__ == "__main__":
    main()
