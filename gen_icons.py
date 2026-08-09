"""Generates minimal line-art badge SVGs for the catalog. No external assets used."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from seed_data import PRODUCTS  # noqa: E402

OUT_DIR = os.path.join(os.path.dirname(__file__), "static", "images", "products")
os.makedirs(OUT_DIR, exist_ok=True)

ACCENTS = {
    "emerald": dict(tint="#E4EEE8", mid="#9FC1AE", ink="#1F6F54"),
    "clay":    dict(tint="#F4E4D9", mid="#DDAF93", ink="#B5643E"),
    "gold":    dict(tint="#F2E8D4", mid="#D9BE8B", ink="#9A7530"),
}

# Hand-simplified line-art glyphs, drawn on a 48x48 grid, stroke-based.
ICONS = {
    "headphones": '<path d="M10 30v-6a14 14 0 0 1 28 0v6"/><rect x="6" y="28" width="8" height="12" rx="4"/><rect x="34" y="28" width="8" height="12" rx="4"/>',
    "smartwatch": '<rect x="16" y="14" width="16" height="20" rx="4"/><path d="M20 14V8h8v6M20 34v6h8v-6"/><circle cx="24" cy="24" r="1.4" fill="currentColor" stroke="none"/>',
    "speaker": '<rect x="14" y="6" width="20" height="36" rx="6"/><circle cx="24" cy="15" r="2.6"/><circle cx="24" cy="28" r="7"/><circle cx="24" cy="28" r="2.4" fill="currentColor" stroke="none"/>',
    "camera": '<rect x="6" y="14" width="36" height="24" rx="4"/><path d="M16 14l3-5h10l3 5"/><circle cx="24" cy="26" r="8"/><circle cx="24" cy="26" r="2.8" fill="currentColor" stroke="none"/>',
    "laptop-stand": '<path d="M8 34h32"/><path d="M14 34l6-16h8l6 16"/><path d="M18 22h12"/>',
    "mouse": '<rect x="16" y="8" width="16" height="30" rx="8"/><path d="M24 8v12"/>',
    "jacket": '<path d="M14 10l-8 6 4 6 4-3v21h20V19l4 3 4-6-8-6-6 4z"/><path d="M20 10v6l4 3 4-3v-6"/>',
    "sneaker": '<path d="M6 30v6h36v-4c0-3-3-4-6-5l-8-3-6-8-8 2 2 6-6 2z"/><path d="M18 22l6 6"/>',
    "jeans": '<path d="M14 6h20l1 12-3 24h-6l-2-20-2 20h-6l-3-24z"/><path d="M14 6v10h20V6"/>',
    "sunglasses": '<circle cx="14" cy="24" r="8"/><circle cx="34" cy="24" r="8"/><path d="M22 22h4"/><path d="M6 22l-2 2M42 22l2 2"/>',
    "handbag": '<rect x="8" y="18" width="32" height="22" rx="4"/><path d="M16 18v-4a8 8 0 0 1 16 0v4"/>',
    "scarf": '<path d="M6 12c8 4 8-4 16 0s8-4 16 0"/><path d="M12 12v20l6 6M36 12v14l-6 8"/>',
    "coffee-maker": '<path d="M12 8h20l-3 26a3 3 0 0 1-3 3H18a3 3 0 0 1-3-3z"/><path d="M32 16h4a4 4 0 0 1 0 8h-4"/><path d="M8 40h28"/>',
    "lamp": '<path d="M14 14l6-8h8l6 8z"/><path d="M24 22v14"/><path d="M14 42h20"/>',
    "vase": '<path d="M18 6h12l2 8-4 6 6 10a6 6 0 0 1-6 12h-8a6 6 0 0 1-6-12l6-10-4-6z"/>',
    "cookware": '<circle cx="24" cy="22" r="14"/><path d="M10 22H4M38 22h6"/><path d="M18 22a6 6 0 0 1 12 0"/>',
    "pillow": '<path d="M8 12c4-4 28-4 32 0s4 24 0 28-28 4-32 0-4-24 0-28z"/><path d="M18 18l12 12M30 18L18 30"/>',
    "clock": '<circle cx="24" cy="24" r="16"/><path d="M24 15v9l6 4"/>',
    "book": '<path d="M8 8h14a4 4 0 0 1 4 4v28a4 4 0 0 0-4-4H8z"/><path d="M40 8H26a4 4 0 0 0-4 4v28a4 4 0 0 1 4-4h14z"/>',
    "yogamat": '<rect x="8" y="16" width="34" height="16" rx="8"/><path d="M14 16a8 8 0 0 0 0 16"/>',
    "bottle": '<path d="M20 6h8v6l4 4v24a4 4 0 0 1-4 4H20a4 4 0 0 1-4-4V16l4-4z"/><path d="M16 24h16"/>',
    "tent": '<path d="M24 8l18 30H6z"/><path d="M24 8v30"/><path d="M16 38l8-14 8 14"/>',
    "dumbbell": '<path d="M6 24h4M38 24h4"/><rect x="10" y="18" width="6" height="12" rx="2"/><rect x="32" y="18" width="6" height="12" rx="2"/><path d="M16 24h16"/>',
}


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def badge_svg(icon_key: str, accent: str) -> str:
    c = ACCENTS[accent]
    glyph = ICONS[icon_key]
    return f'''<svg viewBox="0 0 320 320" xmlns="http://www.w3.org/2000/svg" role="img">
  <rect width="320" height="320" fill="{c['tint']}"/>
  <circle cx="160" cy="160" r="118" fill="none" stroke="{c['mid']}" stroke-width="1.5"/>
  <circle cx="160" cy="160" r="104" fill="none" stroke="{c['mid']}" stroke-width="1" stroke-dasharray="2 5"/>
  <g transform="translate(88 88)" stroke="{c['ink']}" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round">
    {glyph}
  </g>
</svg>'''


def main():
    slugs = {}
    for p in PRODUCTS:
        slug = slugify(p["name"])
        slugs[p["name"]] = slug
        svg = badge_svg(p["icon_key"], p["accent"])
        with open(os.path.join(OUT_DIR, f"{slug}.svg"), "w") as f:
            f.write(svg)
    print(f"Generated {len(PRODUCTS)} product badges in {OUT_DIR}")


if __name__ == "__main__":
    main()
