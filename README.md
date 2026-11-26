# thelocalsuedi.
Static site in two languages: `/en/` and `/sv/`. The start page `index.html` sends visitors to the right one. Rebuild everything with `python3 build.py`. Publish with GitHub Pages (Settings > Pages > main / root).

## Before you publish
1. `build.py`: set `SITE_URL` to your real address, run `python3 build.py` (fills canonical links, sitemap, share previews, 404 links).
2. Privacy page (`build.py`, search "PO box"): replace the placeholder with a PO box or c/o address. Swedish law expects name, address and email on a business site; you don't have to give your home address. Ask Skatteverket if your freelance work needs registering.
3. Fonts: put `InstrumentSerif-Regular.woff2`, `InstrumentSerif-Italic.woff2` and `InterTight-Variable.woff2` in `assets/fonts/` (they load from your own site, nothing goes to Google).
4. Add `assets/images/og/og-image.jpg` (1200x630), the picture shown when the link is shared.
5. Search Console: add the site and submit `sitemap.xml`. Put the site link in your Instagram, YouTube and TikTok bios.

## Your Google Drive photos (do this to get all pictures onto the site)
1. On Drive, right-click the folder "Hemsida bilder." > Download. Unzip it into `assets/originals/` (so you have `assets/originals/Work/...` and `assets/originals/Personal projects/...`).
2. `pip install pillow`, then `python3 tools/import_photos.py`, then `python3 build.py`.
3. The folder names decide the gallery. File names are never shown or used as labels (the "cowgirls" files become normal street portraits). Överstyr is stored under Work/portraits, so it stays in Work > Portraits as a series (it is not a personal project). Sub-folders (like "Rosehills - blessed insanity") keep a series together. The script prints a note for anything it could not place.
4. Camera and lens come from each photo's EXIF. No EXIF = no gear shown. You can add gear/year/about per picture in `INFO` in build.py.
5. Originals stay untouched in `assets/originals/` (keep them out of GitHub if they are large; add that folder to `.gitignore`).

## Film posters (first frame of each video)
Put your video files in `assets/originals/video/` named after the film (rehnstroms, uf-gavleborg, bike-festival, lake-jump, redbull, redbull-bts, blessed-insanity, electric-feelgood, fjarilshuset, slotboythim; .mp4 or .mov), then `python3 tools/make_posters.py` (needs ffmpeg). It saves the first frame as `assets/images/video/<name>.jpg`. Videos load from YouTube/Instagram only after Play is pressed. Descriptions, roles, places and links are in `FILMS_` in build.py. Rehnströms uses the YouTube link you gave earlier (arH-8EXF31E); change it there if it is a different film.

## Fast-loading pictures
1. Put your full-size originals in `assets/originals/` using the same sub-path as the list below (e.g. `assets/originals/work/events/events-01.jpg`).
2. `pip install pillow`, then `python3 tools/optimize.py`. It writes the web sizes into `assets/images/` (JPG and WebP at 1000 and 2000 px) and removes location data (EXIF) from the pictures.
3. `python3 build.py` again. Pages use the small WebP files automatically where they exist; frames already reserve their space, so nothing jumps while loading.

## Lightbox
Click a picture to open it large. Arrows, arrow keys, swipe to browse; Esc, the cross or a click outside closes. It shows Date, Gear and About.

## Info on every picture and film
Defaults: gear is `GEAR` in build.py. To set real info, add the file to `INFO` in build.py (key = file path from the lists below), then run `python3 build.py`.

## Availability line
`AVAILABLE` in build.py (one text per language). Empty text hides the line.

## Statistics
Off by default. GoatCounter's hosted free plan is for non-commercial use; paid assignments are probably commercial, so check their terms or choose another tool. If you use it, set `GOATCOUNTER` in build.py; the privacy page updates itself.

## Add a project
Add one line to `PROJECTS` in build.py, run it, then add pictures at the listed paths.

## Images (assets/images/)
- `og/og-image.jpg`
- `work/portraits/portraits-001.jpg`
- `work/events/events-001.jpg`
- `work/live-music/live-music-001.jpg`
- `work/commercial/commercial-001.jpg`
- `projects/life-on-film/life-on-film-001.jpg`
- `projects/street-portraits/street-portraits-001.jpg`
- `projects/street-photography/street-photography-001.jpg`
- `projects/documentary/documentary-001.jpg`
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

