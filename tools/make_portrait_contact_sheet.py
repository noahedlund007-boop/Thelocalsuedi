import os, json, math
from PIL import Image, ImageOps, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data/photos.json")
OUTPUT = os.path.join(ROOT, "tools/contact-sheets")
os.makedirs(OUTPUT, exist_ok=True)

with open(DATA, encoding="utf-8") as f:
    data = json.load(f)

photos = data["galleries"]["work/portraits"]

cols = 4
rows = 5
per_page = cols * rows
thumb_w, thumb_h = 320, 230
cell_w, cell_h = 360, 285
margin = 30

for page_index in range(math.ceil(len(photos) / per_page)):
    batch = photos[page_index * per_page:(page_index + 1) * per_page]

    width = margin * 2 + cols * cell_w
    height = margin * 2 + rows * cell_h + 50
    sheet = Image.new("RGB", (width, height), "#222222")
    draw = ImageDraw.Draw(sheet)

    draw.text((margin, 15),
              f"WORK / PORTRAITS — PAGE {page_index + 1}",
              fill="white")

    for i, item in enumerate(batch):
        number = page_index * per_page + i + 1
        image_path = os.path.join(ROOT, "assets/images", item["id"] + ".jpg")

        if not os.path.exists(image_path):
            print("MISSING:", item["id"])
            continue

        with Image.open(image_path) as source:
            im = ImageOps.exif_transpose(source).convert("RGB")
            im.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)

        col = i % cols
        row = i // cols
        x = margin + col * cell_w
        y = margin + 45 + row * cell_h

        px = x + (thumb_w - im.width) // 2
        py = y + (thumb_h - im.height) // 2
        sheet.paste(im, (px, py))

        draw.text((x, y + 238),
                  f"#{number:03d}  {item['id']}",
                  fill="white")

    filename = os.path.join(
        OUTPUT, f"portraits-{page_index + 1:02d}.jpg"
    )
    sheet.save(filename, quality=90)

print(f"KLART: {len(photos)} porträtt")
print(f"Kontaktkartor sparade i: {OUTPUT}")
