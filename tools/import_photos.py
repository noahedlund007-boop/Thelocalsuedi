#!/usr/bin/env python3
"""Imports the photos you downloaded from Google Drive.

1. Download the Drive folder "Hemsida bilder." (right-click > Download), unzip it into assets/originals/
   so you get assets/originals/Work/... and assets/originals/Personal projects/...
2. pip install pillow
3. python3 tools/import_photos.py     then     python3 build.py

What it does (originals are never changed or deleted):
- Decides the gallery from the FOLDER names. File names are never used as titles or labels
  (so the 'cowgirls' file names in the street-portrait folder do not create any category).
- Makes web sizes (WebP 480/1000/2000 px + a JPG) in assets/images/, without location data.
- Reads camera and lens from the photo's EXIF where it exists. No EXIF = no gear shown (nothing is guessed).
- Orders each gallery: the strongest-looking picture first, similar series kept together, portrait/landscape
  alternated where possible, the weakest-looking pictures last. Nothing is thrown away.
- Writes data/photos.json, which build.py reads."""
import os, re, json, unicodedata
from PIL import Image, ImageOps, ImageFilter, ImageStat
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, DST, OUT = os.path.join(HERE, "assets/originals"), os.path.join(HERE, "assets/images"), os.path.join(HERE, "data/photos.json")
MAP = {"commercial": "work/commercial", "events": "work/events", "live-music": "work/live-music", "portraits": "work/portraits",
       "street-photography": "projects/street-photography", "street-portraits": "projects/street-portraits", "gatupor": "projects/street-portraits",
       "life-on-film": "projects/life-on-film", "documentary": "projects/documentary"}
def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower().strip()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")
nat = lambda s: [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", s.lower())]
def gear(im):
    try:
        ex = im.getexif(); model = (ex.get(0x0110) or "").strip(); make = (ex.get(0x010F) or "").strip()
        lens = (ex.get_ifd(0x8769).get(0xA434) or "").strip()
    except Exception: return ""
    cam = model if (not make or make.split()[0].lower() in model.lower()) else f"{make} {model}"
    return " + ".join(x for x in (cam.strip(), lens) if x)
def score(im):
    g = im.convert("L"); g.thumbnail((256, 256)); return ImageStat.Stat(g.filter(ImageFilter.FIND_EDGES)).stddev[0] + ImageStat.Stat(g).stddev[0] * .5
def alternate(items):
    rest, out = list(items), []
    while rest:
        pick = rest[0]
        if len(out) >= 2 and all((o["w"] > o["h"]) == (pick["w"] > pick["h"]) for o in out[-2:]):
            pick = next((r for r in rest if (r["w"] > r["h"]) != (pick["w"] > pick["h"])), pick)
        rest.remove(pick); out.append(pick)
    return out
found = {}; notes = []
for dp, _, files in os.walk(SRC):
    parts = os.path.relpath(dp, SRC).split(os.sep) if dp != SRC else []
    hit = [i for i, p in enumerate(parts) if slug(p) in MAP]
    for f in sorted(files, key=nat):
        if not f.lower().endswith((".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp")): continue
        if not hit: notes.append(f"NOT PLACED (no known folder name in path): {os.path.join(*parts, f) if parts else f}"); continue
        i = hit[-1]; key = MAP[slug(parts[i])]; series = slug(parts[i + 1]) if len(parts) > i + 1 else ""
        if "cowgirl" in f.lower(): notes.append(f"'cowgirl' file name treated as ordinary street portrait, label ignored: {f}") if key == "projects/street-portraits" else notes.append(f"'cowgirl' file name outside street-portraits: {f}")
        found.setdefault(key, {}).setdefault(series, []).append(os.path.join(dp, f))
galleries = {}
for key, ser in sorted(found.items()):
    items = []
    for sname, paths in sorted(ser.items()):
        for n, p in enumerate(paths, 1):
            im = ImageOps.exif_transpose(Image.open(p)); g = gear(Image.open(p)); im = im.convert("RGB")
            pid = f"{key}/{sname or key.split('/')[-1]}-{n:03d}"; os.makedirs(os.path.join(DST, os.path.dirname(pid)), exist_ok=True)
            for sz in (2000, 1000, 480):
                c = im.copy(); c.thumbnail((sz, sz), Image.LANCZOS); c.save(os.path.join(DST, f"{pid}-{sz}.webp"), "WEBP", quality=80, method=6)
            c = im.copy(); c.thumbnail((1600, 1600), Image.LANCZOS); c.save(os.path.join(DST, f"{pid}.jpg"), "JPEG", quality=82, optimize=True, progressive=True)
            it = {"id": pid, "w": im.width, "h": im.height, "s": round(score(im), 2), "series": sname}
            if g: it["gear"] = g
            items.append(it)
    best = max(items, key=lambda x: x["s"]); cut = sorted(x["s"] for x in items)[int(len(items) * .15)]
    weak = [x for x in items if x["s"] < cut and x is not best]; main = [x for x in items if x not in weak and x is not best]
    blocks = {}
    for x in main: blocks.setdefault(x["series"], []).append(x)
    ordered = [best] + [y for b in blocks.values() for y in alternate(b)] + weak
    galleries[key] = [{k: v for k, v in x.items() if k not in ("s", "series")} for x in ordered]
    print(f"{key}: {len(items)} pictures, {sum(1 for x in items if 'gear' in x)} with camera info")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump({"galleries": galleries}, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
for n in sorted(set(notes)): print("NOTE:", n)
print("done. Now run: python3 build.py")
