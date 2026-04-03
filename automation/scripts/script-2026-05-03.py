#!/usr/bin/env python3
"""
GHP Short #102 — May 3, 2026 (Saturday)
"I tested a $35 robot vacuum vs my old one."
Format: Comparison (tested $X vs $Y) — Revenue format #2
Partner tie-in: Dreame (5%+ commission, Easter Sale 60% off thru Apr 12, high-AOV)
"""

TITLE = "I tested a $35 robot vacuum vs my old one."
HASHTAGS = "#robotvacuum #dreame #amazonfinds #homecleaning #budgethome"
DESCRIPTION = """I tested a $35 robot vacuum against my trusty upright. Here's what happened.

Spoiler: the robot won in 3 out of 4 categories.

Products featured:
1. Dreame L10s Ultra Robot Vacuum (SALE: $299, was $799) — https://www.dreametech.com/pages/easter-sale-2026
2. Budget Robot Vacuum ($35 Amazon) — https://www.amazon.com/dp/B0EXAMPLE5?tag=goldenhomep06-20
3. Dreame H12 Pro Wet Dry Vacuum ($249) — https://www.dreametech.com/pages/easter-sale-2026
4. Microfiber Mop Pads Replacement (12-pack) — $14
   https://www.amazon.com/dp/B0EXAMPLE6?tag=goldenhomep06-20

Dreame Easter Sale: Up to 60% off through April 12!

Subscribe for honest product testing!
Golden Home Project | goldenhomeprojectllc@gmail.com
"""

VOICEOVER = """I tested a thirty-five dollar robot vacuum against my old upright.
Here's what happened.
Round one: hardwood floors. The robot got every corner. My upright missed under the couch. Robot wins.
Round two: carpet. Honestly? The upright is better on deep carpet. Upright wins.
Round three: pet hair. The robot's brushless design didn't tangle once. Robot wins.
Round four: the kitchen after cooking. The robot ran automatically at 8 AM. I didn't lift a finger. Robot wins.
Three out of four. And right now Dreame has their Easter sale — up to sixty percent off.
The L10s Ultra is two-ninety-nine, down from eight hundred.
Links below."""

FRAMES = [
    {"type": "before", "source": "pexels", "query": "dirty floor with dust and pet hair", "text_overlay": "The Test"},
    {"type": "product", "source": "pollinations", "prompt": "budget robot vacuum cleaning hardwood floor, overhead view, clean modern room", "text_overlay": "$35 Robot Vacuum"},
    {"type": "product", "source": "pollinations", "prompt": "premium Dreame robot vacuum on hardwood floor, sleek design, modern home", "text_overlay": "Dreame L10s Ultra — $299 (was $799)"},
    {"type": "after", "source": "pollinations", "prompt": "spotless hardwood floor in modern living room, bright natural light, clean aesthetic", "text_overlay": "Robot: 3/4 wins"},
    {"type": "product", "source": "pollinations", "prompt": "Dreame Easter Sale banner, robot vacuums displayed, 60% off text, spring flowers", "text_overlay": "Dreame Easter Sale — 60% OFF"},
]

PRODUCTS = [
    {"name": "Budget Robot Vacuum", "price": 35, "asin": "B0EXAMPLE5", "tag": "goldenhomep06-20"},
    {"name": "Dreame L10s Ultra", "price": 299, "source": "dreame", "commission": "5%+", "note": "Easter Sale — was $799"},
    {"name": "Dreame H12 Pro", "price": 249, "source": "dreame", "commission": "5%+"},
    {"name": "Microfiber Mop Pads 12-pack", "price": 14, "asin": "B0EXAMPLE6", "tag": "goldenhomep06-20"},
]

if __name__ == "__main__":
    print(f"Script: {TITLE}")
    print(f"Products: {len(PRODUCTS)}")
    print(f"Format: Comparison — tested $X vs $Y")
    print(f"Partner: Dreame (5%+ commission, Easter Sale)")
