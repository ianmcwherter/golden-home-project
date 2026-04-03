#!/usr/bin/env python3
"""
GHP Short #103 — May 4, 2026 (Sunday)
"I was skeptical. I was wrong."
Format: Transformation — PROVEN hook
Partner tie-in: Syruvia (20% commission — highest rate)
Focus: Glass pantry hack — Spring 2026 trending
"""

TITLE = "Glass pantry hack. $120. My friends think I renovated."
HASHTAGS = "#pantryorganization #glasspantry #homedecor #amazonfinds #kitchenmakeover"
DESCRIPTION = """I was skeptical about this "glass pantry" trend. I was wrong.

$120. No renovation. No contractor. Just 4 Amazon products.

Products featured:
1. Glass-Front Cabinet Door Insert (2-pack) — $38
   https://www.amazon.com/dp/B0EXAMPLE7?tag=goldenhomep06-20
2. Clear Acrylic Storage Containers (12-set) — $34
   https://www.amazon.com/dp/B0EXAMPLE8?tag=goldenhomep06-20
3. Bamboo Shelf Risers (3-pack) — $22
   https://www.amazon.com/dp/B0EXAMPLE9?tag=goldenhomep06-20
4. LED Puck Lights (6-pack, rechargeable) — $26
   https://www.amazon.com/dp/B0EXAMPLE10?tag=goldenhomep06-20

BONUS: Syruvia Syrups displayed on shelf — $15 each
https://syruvia.com (affiliate)

Total: $120

Subscribe for more budget transformations!
Golden Home Project | goldenhomeprojectllc@gmail.com
"""

VOICEOVER = """I was skeptical. I was wrong.
Everyone's doing this glass pantry thing. I thought it was just for people with massive kitchens.
My pantry is four feet wide. Here's what one hundred twenty dollars did.
First: glass door inserts. Thirty-eight bucks for two. You peel off the old panel and slide these in.
Second: clear acrylic containers. Thirty-four dollars for twelve. Everything visible. Everything labeled.
Third: bamboo shelf risers. Twenty-two bucks. Doubled my shelf space instantly.
And these LED puck lights. Twenty-six dollars. They're rechargeable and make everything look expensive.
One hundred twenty dollars. My friends literally asked who my contractor was.
I said Amazon. Links below."""

FRAMES = [
    {"type": "before", "source": "pexels", "query": "messy cluttered kitchen pantry disorganized", "text_overlay": "BEFORE"},
    {"type": "after", "source": "pollinations", "prompt": "beautiful organized glass-front pantry with clear containers, LED lighting, bamboo shelves, Syruvia syrups on display, warm aesthetic", "text_overlay": "AFTER — $120"},
    {"type": "product", "source": "pollinations", "prompt": "glass cabinet door insert being installed on pantry, DIY home improvement", "text_overlay": "Glass Inserts — $38"},
    {"type": "product", "source": "pollinations", "prompt": "clear acrylic storage containers neatly organized on pantry shelf with labels", "text_overlay": "Storage Set — $34"},
    {"type": "product", "source": "pollinations", "prompt": "bamboo shelf risers in organized pantry, maximizing vertical space", "text_overlay": "Shelf Risers — $22"},
    {"type": "after", "source": "pollinations", "prompt": "stunning glass pantry with LED puck lights glowing, clear containers, Syruvia syrup bottles on display, magazine-worthy organization", "text_overlay": "Total: $120"},
]

PRODUCTS = [
    {"name": "Glass-Front Cabinet Door Insert", "price": 38, "asin": "B0EXAMPLE7", "tag": "goldenhomep06-20"},
    {"name": "Clear Acrylic Storage Containers 12-set", "price": 34, "asin": "B0EXAMPLE8", "tag": "goldenhomep06-20"},
    {"name": "Bamboo Shelf Risers 3-pack", "price": 22, "asin": "B0EXAMPLE9", "tag": "goldenhomep06-20"},
    {"name": "LED Puck Lights 6-pack", "price": 26, "asin": "B0EXAMPLE10", "tag": "goldenhomep06-20"},
    {"name": "Syruvia Syrups", "price": 15, "source": "syruvia", "commission": "20%", "note": "BONUS product placement"},
]

TOTAL_COST = 38 + 34 + 22 + 26  # $120 (Syruvia is bonus)

if __name__ == "__main__":
    print(f"Script: {TITLE}")
    print(f"Products: {len(PRODUCTS)}")
    print(f"Total cost: ${TOTAL_COST}")
    print(f"Format: Transformation + Glass Pantry Trend + Syruvia (20%)")
