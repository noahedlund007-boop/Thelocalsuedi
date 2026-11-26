# thelocalsuedi.
Static site in two languages: `/en/` and `/sv/`. The start page `index.html` sends visitors to the right one. Rebuild everything with `python3 build.py`. Publish with GitHub Pages (Settings > Pages > main / root).

## Before you publish
1. `build.py`: set `SITE_URL` to your real address, run `python3 build.py` (fills canonical links, sitemap, share previews, 404 links).
2. Privacy page (`build.py`, search "PO box"): replace the placeholder with a PO box or c/o address. Swedish law expects name, address and email on a business site; you don't have to give your home address. Ask Skatteverket if your freelance work needs registering.
3. Fonts: put `InstrumentSerif-Regular.woff2`, `InstrumentSerif-Italic.woff2` and `InterTight-Variable.woff2` in `assets/fonts/` (they load from your own site, nothing goes to Google).
4. Add `assets/images/og/og-image.jpg` (1200x630), the picture shown when the link is shared.
5. Search Console: add the site and submit `sitemap.xml`. Put the site link in your Instagram, YouTube and TikTok bios.

## Photos from Google Drive
1. Download the Drive folder "Hemsida bilder." (right-click > Download), unzip it into `assets/originals/`.
2. `pip install pillow`, then `python3 tools/import_photos.py`, then `python3 build.py`.
3. The folder decides the gallery; file names are never shown. Pictures are NOT sorted by sharpness or contrast. Within a gallery they stay grouped by series (the file-name prefix) and follow the number at the end of each file name. Series are alphabetical unless you list your own order in `data/order.json` (see the top of tools/import_photos.py).
4. `data/photos.json` is the single source of truth for what is shown and in which order. Edit it by hand if you want a different order.
5. Originals stay untouched in `assets/originals/` (git-ignored). The generated web sizes go to `assets/images/`.

## Menu hover pictures
Each gallery shows a picture when you hover its name in the lists. Put your own `assets/images/<gallery>/cover.jpg` (for example `assets/images/work/portraits/cover.jpg`) to choose it. Without a file, `data/covers.json` ({"work/portraits": "work/portraits/portraits-005"}) or else the first picture is used.

## Film thumbnails
Order of choice: your own frame `assets/images/video/<id>.jpg` (ids in the list below; `python3 tools/make_posters.py` takes the first frame from videos in `assets/originals/video/`), otherwise a photo from the same event/band in your gallery (bike-festival, uf-gavleborg, blessed-insanity, electric-feelgood; change with `data/thumbs.json`), otherwise a typographic card. Nothing is invented.

## Masonry galleries and lightbox
Pictures keep their proportions and fill 2, 3 or 4 columns depending on screen width, in the order of `data/photos.json`. Click a picture to open it large; arrows, arrow keys or swipe to browse; Esc closes.

## Availability line
`AVAILABLE` in build.py (one text per language). Empty text hides the line.

## Statistics
Off by default. GoatCounter's hosted free plan is for non-commercial use; paid assignments are probably commercial, so check their terms or choose another tool. If you use it, set `GOATCOUNTER` in build.py; the privacy page updates itself.

## Add a project
Add one line to `PROJECTS` in build.py, run it, then add pictures at the listed paths.

## Images (assets/images/)
- `og/og-image.jpg`
- `work/portraits/portraits-001-960.webp`
- `work/events/events-001-960.webp`
- `work/live-music/live-music-001-960.webp`
- `work/commercial/commercial-001-960.webp`
- `projects/life-on-film/life-on-film-001-960.webp`
- `projects/street-portraits/street-portraits-001-960.webp`
- `projects/street-photography/street-photography-001-960.webp`
- `projects/documentary/documentary-001-960.webp`
- `video/uf-gavleborg.jpg`
- `video/bike-festival.jpg`
- `video/lake-jump.jpg`
- `video/redbull.jpg`
- `video/redbull-bts.jpg`
- `video/rehnstroms.jpg`
- `video/blessed-insanity.jpg`
- `video/electric-feelgood.jpg`
- `video/fjarilshuset.jpg`
- `video/slotboythim.jpg`
- `about/noah-portrait.jpg`
- `menu/menu-bg.jpg`

## Videos (assets/videos/)

