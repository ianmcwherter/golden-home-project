#!/usr/bin/env python3
"""
Compose Kitchen Makeover video from pre-generated frames + audio using ffmpeg.
Bypasses moviepy PIL compatibility issue.
"""
import json
import os
import subprocess
from pathlib import Path

OUTPUT_DIR = Path("/tmp/kitchen_makeover")
FRAMES_DIR = OUTPUT_DIR / "frames"
AUDIO_DIR = OUTPUT_DIR / "audio"

SECTIONS = [
    {"name": "intro", "frames": 2},
    {"name": "countertops", "frames": 6},
    {"name": "cabinet_organization", "frames": 5},
    {"name": "sink_area", "frames": 4},
    {"name": "pantry", "frames": 5},
    {"name": "finishing_touches", "frames": 3},
    {"name": "outro", "frames": 3},
]

def get_audio_duration(audio_path):
    """Get audio duration using ffprobe"""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(audio_path)],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())

def compose():
    print("=== COMPOSING KITCHEN MAKEOVER VIDEO ===\n")

    section_videos = []

    for i, section in enumerate(SECTIONS):
        section_name = section["name"]
        audio_path = AUDIO_DIR / f"section_{i:02d}_{section_name}.mp3"

        if not audio_path.exists():
            print(f"  SKIP section {i}: missing audio {audio_path}")
            continue

        audio_duration = get_audio_duration(audio_path)
        num_frames = section["frames"]
        frame_duration = audio_duration / num_frames

        print(f"  Section {i+1}/{len(SECTIONS)}: {section_name} ({audio_duration:.1f}s, {num_frames} frames, {frame_duration:.1f}s each)")

        # Build concat input for this section's frames
        concat_file = OUTPUT_DIR / f"concat_{i:02d}.txt"
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
            # Repeat last frame (ffmpeg concat demuxer quirk)
            f.write(f"file '{frame_path}'\n")

        # Create section video — clean slideshow synced to audio
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
            print(f"    ✗ Failed to create {section_video.name}")

    if not section_videos:
        print("\nERROR: No section videos created")
        return None

    # Concatenate all sections
    print(f"\n  Concatenating {len(section_videos)} sections...")
    final_concat = OUTPUT_DIR / "final_concat.txt"
    with open(final_concat, "w") as f:
        for sv in section_videos:
            f.write(f"file '{sv}'\n")

    final_output = OUTPUT_DIR / "kitchen_makeover_final.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(final_concat),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        str(final_output)
    ], capture_output=True, text=True)

    if final_output.exists():
        size_mb = final_output.stat().st_size / 1024 / 1024
        # Get duration
        dur = get_audio_duration(final_output)
        print(f"\n{'='*60}")
        print(f"✓ FINAL VIDEO: {final_output}")
        print(f"  Duration: {dur:.1f}s ({dur/60:.1f}min)")
        print(f"  Size: {size_mb:.1f}MB")
        print(f"{'='*60}")
        return final_output
    else:
        print("\nERROR: Final concatenation failed")
        return None

if __name__ == "__main__":
    compose()
