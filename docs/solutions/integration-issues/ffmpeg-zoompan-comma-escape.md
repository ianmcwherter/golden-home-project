---
title: "ffmpeg zoompan filter commas must be escaped with \\, inside filter expressions"
category: integration-issues
date: 2026-03-31
tags: [ffmpeg, ken-burns, zoompan, video-generation, animation]
severity: high
status: fixed
---

## Problem

Ken Burns animation (slow zoom/pan) on video frames would fail silently for product and AFTER frames, producing clips with no video stream:

```
At least one output file must be written into output file,
because at least one of its streams received no packets.
```

Only the first frame (BEFORE) would succeed; subsequent frames failed, producing reels with 1 clip instead of 5+.

## Root Cause

ffmpeg's filter graph parser uses commas as filter separators. Inside a `zoompan` expression like:

```
zoompan=z='min(zoom+0.0008,1.12)'
```

The comma inside `min(zoom+0.0008,1.12)` is interpreted as a filter separator, breaking the filter graph. ffmpeg silently skips the malformed filter.

## Fix Applied

Escape all commas inside filter expressions with `\\,` in Python string literals (which produces `\,` in the actual shell command):

```python
# WRONG — comma breaks filter graph:
zoom_expr = "min(zoom+0.0008,1.12)"

# CORRECT — comma escaped:
zoom_expr = "min(zoom+0.0008\\,1.12)"

# For zoom-out direction:
zoom_expr = "if(eq(on\\,1)\\,1.12\\,max(zoom-0.0008\\,1.0))"
```

The full zoompan filter string in `create_kenburns_clip()`:
```python
vf = (
    f"scale={W}:{H}:flags=lanczos,setsar=1,"
    f"zoompan=z='{zoom_expr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
    f":d={n_frames}:s={W}x{H}:fps={FPS}"
)
```

Note: commas between top-level filters (e.g., `scale=...,setsar=1,zoompan=...`) do NOT need escaping — only commas *inside* filter argument expressions.

## Prevention

When building ffmpeg filter graphs programmatically, always escape commas inside math expressions. Test with a simple static frame before running full batch generation.
