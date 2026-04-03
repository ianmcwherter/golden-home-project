#!/usr/bin/env python3
"""
GHP Short #101 — May 1, 2026 (Thursday)
"My kitchen looked like this. Same kitchen. $67."
Format: Transformation (BEFORE -> AFTER) — PROVEN top performer
Trend tie-in: Floral kitchen accents (Spring 2026 trending)
"""

TITLE = "My kitchen looked like this. Same kitchen. $67."
HASHTAGS = "#kitchenmakeover #homedecor #amazonfinds #budgethome #floralkitchen"
DESCRIPTION = """My kitchen looked like this. Same kitchen. $67.

These 4 floral accents completely changed the vibe — and everything is from Amazon.

Products featured:
1. Floral Ceramic Canister Set (3-pc) — $24
   https://www.amazon.com/dp/B0EXAMPLE1?tag=goldenhomep06-20
2. Floral Cotton Kitchen Towels (4-pack) — $16
   https://www.amazon.com/dp/B0EXAMPLE2?tag=goldenhomep06-20
3. Floral Enamel Dutch Oven (6 qt) — $19
   https://www.amazon.com/dp/B0EXAMPLE3?tag=goldenhomep06-20
4. Floral Drawer Liner Roll — $8
   https://www.amazon.com/dp/B0EXAMPLE4?tag=goldenhomep06-20

Total: $67

Subscribe for more budget transformations!
Golden Home Project | goldenhomeprojectllc@gmail.com
"""

VOICEOVER = """My kitchen looked like this.
Plain white. Boring. Zero personality.
Same kitchen. Sixty-seven dollars.
First: these floral canisters. Twenty-four bucks. Instant countertop upgrade.
Second: matching kitchen towels. Sixteen dollars for four. Ties the whole look together.
Third: this floral Dutch oven. Nineteen dollars. Yes, really. It works AND it's decor.
And this drawer liner — eight dollars — makes every drawer feel brand new.
Sixty-seven dollars. Same kitchen. Completely different vibe.
Links in the description."""

FRAMES = [
    {"type": "before", "source": "pexels", "query": "plain white kitchen countertop boring", "text_overlay": "BEFORE"},
    {"type": "after", "source": "pollinations", "prompt": "beautiful kitchen countertop with floral ceramic canisters, matching floral towels, warm lighting, cozy aesthetic", "text_overlay": "AFTER — $67"},
    {"type": "product", "source": "pollinations", "prompt": "floral ceramic canister set on kitchen counter, 3 pieces, cottagecore aesthetic", "text_overlay": "Floral Canisters — $24"},
    {"type": "product", "source": "pollinations", "prompt": "floral cotton kitchen towels hanging on oven handle, bright kitchen", "text_overlay": "Kitchen Towels — $16"},
    {"type": "product", "source": "pollinations", "prompt": "beautiful floral enamel Dutch oven on stovetop, cottagecore kitchen", "text_overlay": "Dutch Oven — $19"},
    {"type": "after", "source": "pollinations", "prompt": "fully styled floral kitchen with canisters, towels, Dutch oven, drawer liner, warm cozy lighting", "text_overlay": "Total: $67"},
]

PRODUCTS = [
    {"name": "Floral Ceramic Canister Set", "price": 24, "asin": "B0EXAMPLE1", "tag": "goldenhomep06-20"},
    {"name": "Floral Cotton Kitchen Towels", "price": 16, "asin": "B0EXAMPLE2", "tag": "goldenhomep06-20"},
    {"name": "Floral Enamel Dutch Oven", "price": 19, "asin": "B0EXAMPLE3", "tag": "goldenhomep06-20"},
    {"name": "Floral Drawer Liner", "price": 8, "asin": "B0EXAMPLE4", "tag": "goldenhomep06-20"},
]

TOTAL_COST = sum(p["price"] for p in PRODUCTS)

if __name__ == "__main__":
    print(f"Script: {TITLE}")
    print(f"Products: {len(PRODUCTS)}")
    print(f"Total cost: ${TOTAL_COST}")
    print(f"Format: Transformation + Floral Trend")
