"""Regenerate favicon set from favicon-source.png.

Steps:
1. Load source, autocrop near-white border to tighten the icon
2. Pad to square with transparent background so nothing is distorted
3. Resize to 16 / 32 / 48 / 180 (apple-touch) / 192 / 512 PNGs
4. Build multi-resolution favicon.ico (16 + 32 + 48)

Run:  uv run python amendment-histories/_make_favicons.py
"""

from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
SRC = HERE / "favicon-source.png"

# Everything above this brightness is considered background.
# The source has a light off-white background around a mid-tone icon.
BG_BRIGHTNESS_THRESHOLD = 240


def autocrop(img: Image.Image) -> Image.Image:
    """Trim near-white / near-transparent border to the icon's bbox."""
    rgba = img.convert("RGBA")
    r, g, b, a = rgba.split()
    # Any pixel where alpha < 250 OR brightness > threshold counts as bg
    from PIL import ImageMath
    gray = Image.eval(r, lambda v: v).convert("L")
    # Simple: build a "content" mask where pixel is darker than threshold
    content_mask = gray.point(lambda p: 255 if p < BG_BRIGHTNESS_THRESHOLD else 0)
    bbox = content_mask.getbbox()
    if bbox is None:
        return rgba
    # Add a small breathing margin (2% of longest side)
    w, h = rgba.size
    margin = int(max(w, h) * 0.02)
    l, t, r_, b_ = bbox
    l = max(0, l - margin)
    t = max(0, t - margin)
    r_ = min(w, r_ + margin)
    b_ = min(h, b_ + margin)
    return rgba.crop((l, t, r_, b_))


def pad_to_square(img: Image.Image) -> Image.Image:
    """Center on a transparent square canvas."""
    w, h = img.size
    side = max(w, h)
    canvas = Image.new("RGBA", (side, side), (255, 255, 255, 0))
    canvas.paste(img, ((side - w) // 2, (side - h) // 2), img)
    return canvas


def resize(img: Image.Image, size: int) -> Image.Image:
    return img.resize((size, size), Image.Resampling.LANCZOS)


def main():
    src = Image.open(SRC)
    print(f"Source: {SRC.name}  ({src.size[0]}x{src.size[1]}, mode={src.mode})")
    cropped = autocrop(src)
    print(f"After autocrop: {cropped.size[0]}x{cropped.size[1]}")
    squared = pad_to_square(cropped)
    print(f"After square-pad: {squared.size[0]}x{squared.size[1]}")

    # Emit PNGs at each favicon size
    outputs = {
        16: HERE / "favicon-16.png",
        32: HERE / "favicon-32.png",
        48: HERE / "favicon-48.png",
        180: HERE / "apple-touch-icon.png",
        192: HERE / "favicon-192.png",
        512: HERE / "favicon-512.png",
    }
    for sz, path in outputs.items():
        out = resize(squared, sz)
        # For apple-touch, we want a solid white background (iOS convention)
        if path.name == "apple-touch-icon.png":
            bg = Image.new("RGBA", out.size, (255, 255, 255, 255))
            bg.paste(out, (0, 0), out)
            bg.convert("RGB").save(path, "PNG", optimize=True)
        else:
            out.save(path, "PNG", optimize=True)
        print(f"  {path.name:<26}  {sz}x{sz}  {path.stat().st_size:,} B")

    # Multi-resolution .ico bundling 16, 32, 48
    ico_path = HERE / "favicon.ico"
    # PIL's save with sizes=[…] embeds each size in the .ico
    squared.save(
        ico_path,
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
    )
    print(f"  {ico_path.name:<26}  16+32+48  {ico_path.stat().st_size:,} B")


if __name__ == "__main__":
    main()
