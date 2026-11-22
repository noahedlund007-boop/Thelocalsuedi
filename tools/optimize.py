#!/usr/bin/env python3
"""Turns originals in assets/originals/ into web sizes in assets/images/ (same sub-paths).
Needs Pillow: pip install pillow.  Writes NAME.jpg (2000 px), NAME-1000.jpg, NAME-1000.webp, NAME-2000.webp.
Saving without EXIF removes camera/location metadata."""
import os
from PIL import Image, ImageOps
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, DST = os.path.join(HERE, "assets/originals"), os.path.join(HERE, "assets/images")
n = 0
for dp, _, files in os.walk(SRC):
    for f in files:
        if not f.lower().endswith((".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp")): continue
        rel = os.path.relpath(dp, SRC); stem = os.path.splitext(f)[0]
        out = os.path.join(DST, rel); os.makedirs(out, exist_ok=True)
        im = ImageOps.exif_transpose(Image.open(os.path.join(dp, f))).convert("RGB")
        for size in (2000, 1000):
            c = im.copy(); c.thumbnail((size, size), Image.LANCZOS)
            c.save(os.path.join(out, f"{stem}-{size}.webp"), "WEBP", quality=80, method=6)
            if size == 2000: c.save(os.path.join(out, f"{stem}.jpg"), "JPEG", quality=84, optimize=True, progressive=True)
            else: c.save(os.path.join(out, f"{stem}-1000.jpg"), "JPEG", quality=82, optimize=True, progressive=True)
        n += 1
print(n, "pictures optimized")
