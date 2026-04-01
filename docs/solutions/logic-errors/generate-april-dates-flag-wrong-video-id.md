---
title: "generate_april_content.py --dates flag assigns wrong video IDs"
category: logic-errors
date: 2026-03-31
tags: [python, video-generation, content-pipeline, ffmpeg, april-calendar]
severity: critical
status: fixed
---

## Problem

When running `generate_april_content.py` with the `--dates` flag to regenerate specific videos, the output files were named incorrectly. For example:

```bash
python3 generate_april_content.py --dates 2026-04-23 2026-04-26
```

Produced `trans_001.mp4` and `trans_002.mp4` instead of the correct `trans_014.mp4` and `trans_016.mp4`. This overwrote existing correct files and produced mismatched content.

## Root Cause

The script filtered `APRIL_CALENDAR` to only the requested dates, then used `enumerate()` on the *filtered* list to calculate `video_id`:

```python
# BUG: filtered list → i starts at 0 regardless of true calendar position
shorts = [v for v in APRIL_CALENDAR if v["platform"] == "youtube_short"]
if args.dates:
    shorts = [v for v in shorts if v["date"] in args.dates]

for i, entry in enumerate(shorts):
    video_id = i + 1  # WRONG: always starts at 1
```

April 23 is position 14 in the full calendar, but in a filtered 2-item list it becomes position 1 → `trans_001.mp4`.

## Fix Applied

Preserve the full calendar for index lookups; filter only for iteration:

```python
all_shorts = [v for v in APRIL_CALENDAR if v["platform"] == "youtube_short"]
if args.dates:
    shorts = [v for v in all_shorts if v["date"] in args.dates]
else:
    shorts = all_shorts

for entry in shorts:
    # Use position in FULL calendar for correct video ID
    video_id = all_shorts.index(entry) + 1
    voice = VOICES[(video_id - 1) % len(VOICES)]
```

## Prevention

Always derive IDs from the source-of-truth list, not a filtered subset. When filtering a list for iteration but needing original indices, keep a reference to the unfiltered list.

## Real-World Impact

The bug caused `trans_001.mp4` (April 1 kitchen counter video) to be overwritten with April 23 desk organizer content. Recovery required restoring from the GitHub repo copy, which had the correct file.
