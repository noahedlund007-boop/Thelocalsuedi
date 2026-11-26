#!/usr/bin/env python3
import os, sys, json, zipfile, hashlib, subprocess, re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)

REPORT = []
ERRORS = []
CHANGES = []

def log(msg):
    print(msg, flush=True)
    REPORT.append(msg)

def run(cmd):
    p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if p.returncode:
        ERRORS.append(f"{' '.join(cmd)}: {p.stderr[-1500:]}")
    return p

def sha(data):
    return hashlib.sha256(data).hexdigest()

def image_file(p):
    return p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}

def main():
    log("=== THELOCALSUEDI AUTOMATIC UPDATE ===")

    # 1. Inspect core files
    for f in ["build.py", "data/photos.json", "assets/css/style.css",
              "assets/js/main.js"]:
        if not Path(f).exists():
            ERRORS.append(f"Saknad kärnfil: {f}")

    if ERRORS:
        raise RuntimeError("\n".join(ERRORS))

    # 2. Load gallery data and archive
    photos_path = Path("data/photos.json")
    photos = json.loads(photos_path.read_text(encoding="utf-8"))
    galleries = photos.get("galleries", {})

    archives = list(Path("incoming").glob("*.zip"))
    if not archives:
        raise RuntimeError("ZIP-arkivet saknas i incoming/")

    archive = archives[0]
    log(f"ZIP: {archive}")

    with zipfile.ZipFile(archive) as z:
        archive_entries = z.infolist()
        archive_images = defaultdict(list)
        for entry in archive_entries:
            if not entry.is_dir() and image_file(Path(entry.filename)):
                parts = Path(entry.filename).parts
                if len(parts) >= 3:
                    category = "/".join(parts[1:-1])
                    archive_images[category].append(entry)

        log(f"Originalbilder i ZIP: {sum(map(len, archive_images.values()))}")

        # 3. Match images to existing IDs safely.
        # Existing image paths are preserved. Exact hash matches are preferred.
        hash_to_ids = defaultdict(list)
        id_to_item = {}
        for category, items in galleries.items():
            for item in items:
                image_id = item.get("id")
                if image_id:
                    id_to_item[image_id] = item
                    for ext in (".jpg", ".jpeg", ".png", ".webp"):
                        candidate = Path("assets/images") / (image_id + ext)
                        if candidate.exists():
                            hash_to_ids[sha(candidate.read_bytes())].append(image_id)

        # Also use original images where available.
        original_root = Path("assets/originals")
        original_hashes = {}
        for p in original_root.rglob("*"):
            if p.is_file() and image_file(p):
                try:
                    original_hashes[sha(p.read_bytes())] = p
                except OSError:
                    pass

        reordered = 0
        unmatched = []
        for category, entries in archive_images.items():
            # Convert archive category path to photos.json category key.
            key = category.lower().replace("personal projects/", "projects/")
            key = key.replace("work/", "work/")
            if key not in galleries:
                unmatched.append(f"Okänd kategori: {category}")
                continue

            items = galleries[key]
            by_hash = {}
            for item in items:
                image_id = item.get("id")
                if not image_id:
                    continue
                for ext in (".jpg", ".jpeg", ".png", ".webp"):
                    p = Path("assets/images") / (image_id + ext)
                    if p.exists():
                        by_hash[sha(p.read_bytes())] = item
                        break

            ordered = []
            used = set()
            for entry in entries:
                try:
                    digest = sha(z.read(entry))
                except Exception:
                    continue
                item = by_hash.get(digest)
                if item and item["id"] not in used:
                    ordered.append(item)
                    used.add(item["id"])

            # Only apply a complete, unambiguous match.
            if len(ordered) == len(items) and len(used) == len(items):
                galleries[key] = ordered
                reordered += 1
                log(f"ZIP-ordning verifierad: {key} ({len(ordered)} bilder)")
            else:
                log(f"Behåller befintlig ordning: {key} — "
                    f"{len(ordered)}/{len(items)} exakta matchningar")
                unmatched.append(key)

    # 4. Portrait collection: preserve the current 48-image selection.
    portraits = galleries.get("work/portraits", [])
    log(f"Porträtt i nuvarande data: {len(portraits)}")
    if len(portraits) != 48:
        ERRORS.append("Porträttgalleriet innehåller inte exakt 48 bilder. "
                      "Ingen automatisk gissning görs.")

    # 5. Remove per-image information buttons from generated gallery markup.
    build_path = Path("build.py")
    source = build_path.read_text(encoding="utf-8")

    # Remove the video info call only; do not alter About/Gear content.
    source_new = re.sub(
        r'\s*info\(path,\s*"t",\s*"film"\)',
        '',
        source
    )
    if source_new != source:
        build_path.write_text(source_new, encoding="utf-8")
        CHANGES.append("Tog bort videokortens informationsknapp")
        source = source_new

    # Remove info-card markup only from photo figures, keeping lightbox functional.
    # Avoid broad destructive replacements; inspect current generated helper.
    if "def pim(" in source:
        start = source.index("def pim(")
        end = source.find("\ndef ", start + 5)
        if end < 0:
            end = len(source)
        block = source[start:end]
        if "info(" in block or "info-btn" in block:
            log("OBS: pim() innehåller informationsmarkup som kräver riktad kodändring.")
        else:
            log("Bildkortens pim()-funktion saknar informationsknappar.")

    # 6. Masonry layout: replace justified rows with CSS columns.
    css_path = Path("assets/css/style.css")
    css = css_path.read_text(encoding="utf-8")
    build_source = source

    if ".irow" in css and ".flow" in css:
        # Change only the gallery layout primitives.
        css_new = re.sub(
            r'\.irow\s*\{[^}]*\}',
            '.irow{display:block;columns:3;column-gap:12px}',
            css,
            count=1
        )
        css_new = re.sub(
            r'\.irow\s+\.f\s*\{[^}]*\}',
            '.irow .f{display:inline-block;width:100%;margin:0 0 12px;break-inside:avoid}',
            css_new,
            count=1
        )
        if css_new != css:
            css_path.write_text(css_new, encoding="utf-8")
            CHANGES.append("Aktiverade masonry-kolumner i gallerier")
            css = css_new
        else:
            log("Masonry CSS kunde inte säkert identifieras; CSS lämnas orörd.")
    else:
        log("Masonry ej ändrad: befintliga CSS-selektorer kunde inte verifieras.")

    # 7. Remove obsolete info-card JavaScript behavior if no info markup remains.
    js_path = Path("assets/js/main.js")
    js = js_path.read_text(encoding="utf-8")
    if ".info" not in build_source and ".info" not in js:
        log("Inga informationskomponenter hittades.")
    else:
        log("Behåller lightboxens kompatibilitet med eventuell äldre info-data.")

    # 8. Save gallery data only if verified ordering changed.
    if reordered:
        photos_path.write_text(
            json.dumps(photos, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8"
        )
        CHANGES.append(f"Uppdaterade ZIP-ordning i {reordered} gallerier")

    # 9. Video poster inventory; never fabricate thumbnails.
    video_dir = Path("assets/images/video")
    video_dir.mkdir(parents=True, exist_ok=True)
    film_ids = re.findall(r'"id"\s*:\s*"([^"]+)"', source)
    existing_posters = list(video_dir.glob("*.jpg"))
    log(f"Videominiatyrer: {len(existing_posters)} befintliga")
    if not existing_posters:
        log("Videominiatyrer saknas. Inga falska miniatyrer skapas.")

    # 10. Build both language versions.
    log("Bygger webbplatsen...")
    result = run([sys.executable, "build.py"])
    if result.stdout:
        log(result.stdout[-3000:])
    if result.returncode:
        raise RuntimeError("Webbplatsbygget misslyckades.")

    # 11. Verify outputs.
    required = ["site/index.html", "site/sv/index.html",
                "site/assets/css/style.css", "site/assets/js/main.js"]
    missing = [f for f in required if not Path(f).exists()]
    if missing:
        ERRORS.append("Saknade byggfiler: " + ", ".join(missing))

    # Check JSON validity and gallery totals.
    check = json.loads(photos_path.read_text(encoding="utf-8"))
    total = sum(len(v) for v in check["galleries"].values())
    log(f"Bildposter i data: {total}")

    # 12. Report
    log("\n=== ÄNDRINGAR ===")
    for x in CHANGES:
        log("- " + x)
    if not CHANGES:
        log("- Inga säkra kod-/ordningsändringar behövdes.")

    log("\n=== KVARSTÅENDE AUTOMATISKA KONTROLLER ===")
    for x in unmatched:
        log("- " + x)
    if not unmatched:
        log("- Inga omatchade kategorier.")

    if ERRORS:
        log("\n=== FEL ===")
        for e in ERRORS:
            log("- " + e)
        raise RuntimeError("Uppdateringen är inte helt verifierad.")

    log("\nKLART: webbplatsen har byggts och kontrollerats.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\nUPPDATERINGEN AVBRÖTS:", e, file=sys.stderr)
        sys.exit(1)
