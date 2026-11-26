#!/usr/bin/env python3
"""Imports the photos from the Google Drive folder you unzipped into assets/originals/.

  python3 tools/import_photos.py     then     python3 build.py

ORDER (nothing is sorted by sharpness, contrast or "quality"):
- The folder decides the gallery (Work/portraits, Personal projects/street-portraits, ...). File names are never shown on the site.
- Inside a gallery, pictures stay grouped by series (the file-name prefix, e.g. "cowgirls-streetportrait") and follow the NUMBER at the
  end of each file name (-01, -02 ...), which is the only order information in the Drive export. "name-1-2" comes right after "name-1".
- The order of the series inside a gallery is alphabetical unless you write your own in data/order.json, for example:
  {"work/events": ["swecupdownhill-downhill-bikepark-jarvso-2025", "jarvsobikefestival-jarvso"]}   (series not listed come last)
- The result is written to data/photos.json. That file is the single source of truth: build.py shows pictures in exactly that order.
Originals are never changed or deleted. Pictures are written without camera/location data."""
import os, re, json, unicodedata
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageOps
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, DST, OUT, ORD = (os.path.join(HERE, p) for p in ("assets/originals", "assets/images", "data/photos.json", "data/order.json"))
MAP = {"commercial": "work/commercial", "events": "work/events", "live-music": "work/live-music", "portraits": "work/portraits",
       "street-photography": "projects/street-photography", "street-portraits": "projects/street-portraits", "gatupor": "projects/street-portraits",
       "life-on-film": "projects/life-on-film", "documentary": "projects/documentary"}
SIZES = (1600, 960, 480)
def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower().strip()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")
def parse(fname):
    stem = os.path.splitext(fname)[0]; m = re.match(r"^(.*?)((?:-\d+)+)$", stem)
    return (slug(m.group(1)), tuple(int(x) for x in m.group(2).split("-")[1:])) if m else (slug(stem), ())
def convert(job):
    path, pid = job; im = ImageOps.exif_transpose(Image.open(path)).convert("RGB"); os.makedirs(os.path.join(DST, os.path.dirname(pid)), exist_ok=True)
    for sz in SIZES:
        c = im.copy(); c.thumbnail((sz, sz), Image.LANCZOS); c.save(os.path.join(DST, f"{pid}-{sz}.webp"), "WEBP", quality=76, method=5)
    return pid, im.width, im.height
if __name__ == "__main__":
    found, notes = {}, []
    for dp, _, files in os.walk(SRC):
        parts = os.path.relpath(dp, SRC).split(os.sep) if dp != SRC else []
        hit = [i for i, p in enumerate(parts) if slug(p) in MAP]
        for f in files:
            if not f.lower().endswith((".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp")): continue
            if not hit: notes.append(f"NOT PLACED (no known folder in path): {os.path.join(*parts, f) if parts else f}"); continue
            key = MAP[slug(parts[hit[-1]])]; s, num = parse(f); found.setdefault(key, []).append((s, num, f, os.path.join(dp, f)))
    custom = json.load(open(ORD, encoding="utf-8")) if os.path.exists(ORD) else {}
    jobs, plan = [], {}
    for key, items in sorted(found.items()):
        want = custom.get(key, []); sr = lambda s: (want.index(s) if s in want else len(want), s)
        items.sort(key=lambda x: (sr(x[0]), x[1], x[2].lower()))
        plan[key] = []
        for n, (s, num, f, p) in enumerate(items, 1):
            pid = f"{key}/{key.split('/')[-1]}-{n:03d}"; jobs.append((p, pid)); plan[key].append({"id": pid, "series": s, "src": os.path.relpath(p, SRC)})
    with ProcessPoolExecutor() as ex: dims = {pid: (w, h) for pid, w, h in ex.map(convert, [j for j in jobs], chunksize=4)}
    for key, items in plan.items():
        for it in items: it["w"], it["h"] = dims[it["id"]]
        print(f"{key}: {len(items)} pictures in {len({i['series'] for i in items})} series")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({"galleries": plan}, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for n in sorted(set(notes)): print("NOTE:", n)
    print("done. Now run: python3 build.py")
