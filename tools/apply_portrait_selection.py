import json, os, shutil

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_file = os.path.join(root, "data/photos.json")
backup_file = os.path.join(root, "data/photos-before-portrait-selection.json")
selection_file = os.path.join(root, "data/portrait-selection.json")

keep = set(
    list(range(1, 9))
    + [35, 37, 39, 40, 42, 43, 45, 49, 51, 55, 56, 60, 62,
       119, 122, 125, 128, 131, 133, 134, 135, 136, 143]
    + list(range(144, 159))
)

with open(data_file, encoding="utf-8") as f:
    data = json.load(f)

photos = data["galleries"]["work/portraits"]

if len(photos) != 158:
    raise SystemExit(f"STOPP: Förväntade 158 bilder, hittade {len(photos)}. Inget ändrat.")

if not os.path.exists(backup_file):
    shutil.copy2(data_file, backup_file)

selected = [p for i, p in enumerate(photos, 1) if i in keep]

with open(selection_file, "w", encoding="utf-8") as f:
    json.dump({
        "kept_numbers": sorted(keep),
        "kept_ids": [p["id"] for p in selected]
    }, f, indent=2, ensure_ascii=False)

data["galleries"]["work/portraits"] = selected

with open(data_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=1, ensure_ascii=False)

print(f"Klart: {len(selected)} porträtt behålls.")
print(f"{len(photos) - len(selected)} porträtt döljs från galleriet.")
print("Originalbilderna är orörda.")
print("Säkerhetskopia:", backup_file)
