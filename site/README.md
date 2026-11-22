# thelocalsuedi.
Static site in two languages: `/en/` and `/sv/`. The start page `index.html` sends visitors to the right one. Rebuild everything with `python3 build.py`. Publish with GitHub Pages (Settings > Pages > main / root).

## Before you publish
1. `build.py`: set `SITE_URL` to your real address, run `python3 build.py` (fills canonical links, sitemap, share previews, 404 links).
2. Privacy page (`build.py`, search "PO box"): replace the placeholder with a PO box or c/o address. Swedish law expects name, address and email on a business site; you don't have to give your home address. Ask Skatteverket if your freelance work needs registering.
3. Fonts: put `InstrumentSerif-Regular.woff2`, `InstrumentSerif-Italic.woff2` and `InterTight-Variable.woff2` in `assets/fonts/` (they load from your own site, nothing goes to Google).
4. Add `assets/images/og/og-image.jpg` (1200x630), the picture shown when the link is shared.
5. Search Console: add the site and submit `sitemap.xml`. Put the site link in your Instagram, YouTube and TikTok bios.

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
- `home/intro-poster.jpg`
- `og/og-image.jpg`
- `work/events/cover.jpg`
- `work/portraits/cover.jpg`
- `work/live-music/cover.jpg`
- `work/events/events-01.jpg`
- `work/events/events-02.jpg`
- `work/events/events-03.jpg`
- `work/events/events-04.jpg`
- `work/events/events-05.jpg`
- `work/events/events-06.jpg`
- `work/events/events-07.jpg`
- `work/events/events-08.jpg`
- `work/events/events-09.jpg`
- `work/events/events-10.jpg`
- `work/events/events-11.jpg`
- `work/events/events-12.jpg`
- `work/events/events-13.jpg`
- `work/events/events-14.jpg`
- `work/portraits/portraits-01.jpg`
- `work/portraits/portraits-02.jpg`
- `work/portraits/portraits-03.jpg`
- `work/portraits/portraits-04.jpg`
- `work/portraits/portraits-05.jpg`
- `work/portraits/portraits-06.jpg`
- `work/portraits/portraits-07.jpg`
- `work/portraits/portraits-08.jpg`
- `work/portraits/portraits-09.jpg`
- `work/portraits/portraits-10.jpg`
- `work/portraits/portraits-11.jpg`
- `work/portraits/portraits-12.jpg`
- `work/portraits/portraits-13.jpg`
- `work/portraits/portraits-14.jpg`
- `work/live-music/live-music-01.jpg`
- `work/live-music/live-music-02.jpg`
- `work/live-music/live-music-03.jpg`
- `work/live-music/live-music-04.jpg`
- `work/live-music/live-music-05.jpg`
- `work/live-music/live-music-06.jpg`
- `work/live-music/live-music-07.jpg`
- `work/live-music/live-music-08.jpg`
- `work/live-music/live-music-09.jpg`
- `work/live-music/live-music-10.jpg`
- `work/live-music/live-music-11.jpg`
- `work/live-music/live-music-12.jpg`
- `work/live-music/live-music-13.jpg`
- `work/live-music/live-music-14.jpg`
- `projects/first-roll/cover.jpg`
- `projects/street-portraits/cover.jpg`
- `projects/street-photography/cover.jpg`
- `projects/overstyr/cover.jpg`
- `projects/first-roll/first-roll-01.jpg`
- `projects/first-roll/first-roll-02.jpg`
- `projects/first-roll/first-roll-03.jpg`
- `projects/first-roll/first-roll-04.jpg`
- `projects/first-roll/first-roll-05.jpg`
- `projects/first-roll/first-roll-06.jpg`
- `projects/first-roll/first-roll-07.jpg`
- `projects/first-roll/first-roll-08.jpg`
- `projects/first-roll/first-roll-09.jpg`
- `projects/first-roll/first-roll-10.jpg`
- `projects/first-roll/first-roll-11.jpg`
- `projects/first-roll/first-roll-12.jpg`
- `projects/street-portraits/street-portraits-01.jpg`
- `projects/street-portraits/street-portraits-02.jpg`
- `projects/street-portraits/street-portraits-03.jpg`
- `projects/street-portraits/street-portraits-04.jpg`
- `projects/street-portraits/street-portraits-05.jpg`
- `projects/street-portraits/street-portraits-06.jpg`
- `projects/street-portraits/street-portraits-07.jpg`
- `projects/street-portraits/street-portraits-08.jpg`
- `projects/street-portraits/street-portraits-09.jpg`
- `projects/street-portraits/street-portraits-10.jpg`
- `projects/street-portraits/street-portraits-11.jpg`
- `projects/street-portraits/street-portraits-12.jpg`
- `projects/street-photography/street-photography-01.jpg`
- `projects/street-photography/street-photography-02.jpg`
- `projects/street-photography/street-photography-03.jpg`
- `projects/street-photography/street-photography-04.jpg`
- `projects/street-photography/street-photography-05.jpg`
- `projects/street-photography/street-photography-06.jpg`
- `projects/street-photography/street-photography-07.jpg`
- `projects/street-photography/street-photography-08.jpg`
- `projects/street-photography/street-photography-09.jpg`
- `projects/street-photography/street-photography-10.jpg`
- `projects/street-photography/street-photography-11.jpg`
- `projects/street-photography/street-photography-12.jpg`
- `projects/overstyr/overstyr-01.jpg`
- `projects/overstyr/overstyr-02.jpg`
- `projects/overstyr/overstyr-03.jpg`
- `projects/overstyr/overstyr-04.jpg`
- `projects/overstyr/overstyr-05.jpg`
- `projects/overstyr/overstyr-06.jpg`
- `projects/overstyr/overstyr-07.jpg`
- `projects/overstyr/overstyr-08.jpg`
- `projects/overstyr/overstyr-09.jpg`
- `projects/overstyr/overstyr-10.jpg`
- `projects/overstyr/overstyr-11.jpg`
- `projects/overstyr/overstyr-12.jpg`
- `film/events/event-film-01-poster.jpg`
- `film/events/event-film-02-poster.jpg`
- `film/documentary/yt-arH-8EXF31E-poster.jpg`
- `film/informational/informational-01-poster.jpg`
- `film/informational/informational-02-poster.jpg`
- `about/noah-portrait.jpg`
- `menu/menu-bg.jpg`

## Videos (assets/videos/)
- `intro/intro-loop.mp4`
- `film/events/event-film-01.mp4`
- `film/events/event-film-02.mp4`
- `film/informational/informational-01.mp4`
- `film/informational/informational-02.mp4`
