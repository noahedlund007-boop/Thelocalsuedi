#!/usr/bin/env python3
"""thelocalsuedi. - static site generator (Swedish + English). Edit CONTENT, run `python3 build.py`."""
import os, sys, json, glob, subprocess
from html import escape as e
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://YOUR-USERNAME.github.io/YOUR-REPO"   # TODO: real address, no trailing slash
EMAIL = "Noahedlund007@gmail.com"
INSTAGRAM = "https://www.instagram.com/thelocalsuedi/"
YOUTUBE = "https://www.youtube.com/@thelocalsuedi"
TIKTOK = "https://www.tiktok.com/@thelocalsuedi"
LINKEDIN = "https://www.linkedin.com/in/noah-edlund-1a8960258"
SITE = "thelocalsuedi."
GOATCOUNTER = ""   # your GoatCounter code, e.g. "thelocalsuedi". Empty = no statistics. Read README about commercial-use terms first.
AVAILABLE = {"en": "Available for assignments.", "sv": "Tillgänglig för uppdrag."}   # empty text hides the line
BASE = "" if "YOUR-" in SITE_URL else SITE_URL + "/"
FAV = '<link rel="icon" href="{p}favicon.svg" type="image/svg+xml"><link rel="icon" href="{p}favicon.ico" sizes="48x48"><link rel="apple-touch-icon" href="{p}apple-touch-icon.png"><link rel="manifest" href="{p}site.webmanifest">'

# ======================= parent run: both languages + shared files =======================
if len(sys.argv) < 2:
    for f in glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "en", "*.html")) + glob.glob(os.path.join(ROOT, "sv", "*.html")): os.remove(f)
    for l in ("en", "sv"): subprocess.check_call([sys.executable, os.path.abspath(__file__), l])
    pg = open(os.path.join(ROOT, ".pages")).read().split(); os.remove(os.path.join(ROOT, ".pages"))
    W = lambda n, t: open(os.path.join(ROOT, n), "w", encoding="utf-8").write(t)
    urls = f"<url><loc>{SITE_URL}/index.html</loc></url>" + "".join(
        f'<url><loc>{SITE_URL}/{d}/{p}.html</loc><xhtml:link rel="alternate" hreflang="en" href="{SITE_URL}/en/{p}.html"/><xhtml:link rel="alternate" hreflang="sv" href="{SITE_URL}/sv/{p}.html"/></url>' for p in pg for d in ("en", "sv"))
    W("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">{urls}</urlset>')
    W("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    W("llms.txt", f"""# thelocalsuedi.
> Personal website of Noah Edlund (creative name: thelocalsuedi.), a photographer and filmmaker based in Hälsingland, Sweden. Svenska: fotograf och filmare i Hälsingland.

Work: event photography, portraits, live music photography, event films, documentary, informational and company videos, and personal projects (street photography, street portraits, life on film, documentary). Available for assignments for local businesses, events and people.

- English: {SITE_URL}/en/index.html
- Svenska: {SITE_URL}/sv/index.html
- Work: {SITE_URL}/en/work.html
- Personal projects: {SITE_URL}/en/projects.html
- Video: {SITE_URL}/en/video.html
- About and contact: {SITE_URL}/en/about.html
- Instagram: {INSTAGRAM}
- YouTube: {YOUTUBE}
- TikTok: {TIKTOK}
- LinkedIn: {LINKEDIN}
- Email: {EMAIL}
""")
    head = lambda t, d, p="": (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{t}</title>'
        f'<meta name="description" content="{d}">{FAV.format(p=p)}<link rel="stylesheet" href="{p}assets/css/style.css">')
    W("index.html", head("thelocalsuedi. | Noah Edlund", "Noah Edlund (thelocalsuedi.), photographer and filmmaker in Hälsingland, Sweden. Fotograf och filmare i Hälsingland.") +
      f'<link rel="canonical" href="{SITE_URL}/index.html"><link rel="alternate" hreflang="en" href="{SITE_URL}/en/index.html"><link rel="alternate" hreflang="sv" href="{SITE_URL}/sv/index.html"><link rel="alternate" hreflang="x-default" href="{SITE_URL}/index.html"></head>'
      '<body class="choose"><main class="choose-main"><h1>thelocalsuedi.</h1><p>Noah Edlund. Photographer and filmmaker / Fotograf och filmare. Hälsingland, Sweden.</p>'
      '<nav class="choose-links" aria-label="Language"><a href="sv/index.html" hreflang="sv" lang="sv">Svenska</a><a href="en/index.html" hreflang="en" lang="en">English</a></nav></main>'
      "<script>(function(){var l=(navigator.languages&&navigator.languages[0])||navigator.language||'en';location.replace(/^sv/i.test(l)?'sv/index.html':'en/index.html');})();</script></body></html>")
    W("404.html", head("404 | thelocalsuedi.", "Page not found.", BASE).replace("<html lang=\"en\">", "<html lang=\"en\">") + '<meta name="robots" content="noindex"></head>'
      '<body class="choose nf"><main class="choose-main">'
      '<div data-l="sv" hidden><h1 class="nf-h"></h1><p>Sidan du letade efter finns inte, eller har flyttat.</p><nav class="choose-links"><a href="' + BASE + 'sv/index.html">Till startsidan</a></nav></div>'
      '<div data-l="en" hidden><h1 class="nf-h"></h1><p>The page you were looking for doesn’t exist, or has moved.</p><nav class="choose-links"><a href="' + BASE + 'en/index.html">Back to the start</a></nav></div>'
      "</main><script>(function(){var T={sv:['Den här bilden blev aldrig framkallad.','Filmrullen tog slut.','Ur fokus. Sidan finns inte.'],en:['This one never got developed.','The roll ran out.','Out of focus. This page doesn’t exist.']};"
      "var sv=location.pathname.indexOf('/sv/')>-1||(location.pathname.indexOf('/en/')<0&&/^sv/i.test(navigator.language||''));var k=sv?'sv':'en';document.documentElement.lang=k;"
      "var d=document.querySelector('[data-l='+k+']');d.hidden=false;d.querySelector('.nf-h').textContent=T[k][Math.floor(Math.random()*3)];})();</script></body></html>")
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#fff"/><circle cx="32" cy="32" r="22" fill="none" stroke="#0d0d0d" stroke-width="5"/><circle cx="32" cy="32" r="9" fill="#0d0d0d"/></svg>'
    W("favicon.svg", svg)
    W("site.webmanifest", json.dumps({"name": "thelocalsuedi.", "short_name": "thelocalsuedi.", "start_url": "index.html", "display": "browser", "background_color": "#ffffff", "theme_color": "#ffffff",
        "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=1))
    try:
        from PIL import Image, ImageDraw
        def ico(n):
            S = n * 4; im = Image.new("RGB", (S, S), "white"); d = ImageDraw.Draw(im); c = S / 2
            d.ellipse([c - S * .344, c - S * .344, c + S * .344, c + S * .344], outline="#0d0d0d", width=int(S * .078)); d.ellipse([c - S * .14, c - S * .14, c + S * .14, c + S * .14], fill="#0d0d0d")
            return im.resize((n, n), Image.LANCZOS)
        ico(512).save(os.path.join(ROOT, "icon-512.png")); ico(192).save(os.path.join(ROOT, "icon-192.png")); ico(180).save(os.path.join(ROOT, "apple-touch-icon.png"))
        ico(256).save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    except ImportError:
        print("Pillow missing: only favicon.svg created (pip install pillow, then run again for png/ico)")
    print("built: en + sv + shared files"); sys.exit()

# ======================= child run: one language =======================
LANG = sys.argv[1]
OUT = os.path.join(ROOT, LANG); os.makedirs(OUT, exist_ok=True)
P = "../"; A = P + "assets/"
def L(en, sv): return en if LANG == "en" else sv
PH = {}   # real photos, written by tools/import_photos.py
if os.path.exists(os.path.join(ROOT, "data", "photos.json")): PH = json.load(open(os.path.join(ROOT, "data", "photos.json"), encoding="utf-8"))["galleries"]

# ---------------- CONTENT ----------------
WORK = [("portraits", "Portraits"), ("events", "Events"), ("live-music", "Live Music"), ("commercial", "Commercial")]
# (slug, title, group, year, place, intro) - add a line to add a project
PROJECTS = [
    ("life-on-film", "Life on Film", "Life on Film", "", "", "Everyday life on analogue film."),
    ("street-portraits", "Street Portraits", "Street Portraits", "", "", "Meetings with people on the street. I want the portraits to feel real, not like studio portraits."),
    ("street-photography", "Street Photography", "Street Photography", "", "", "Moments as they happen on the street."),
    ("documentary", "Documentary", "Documentary", "", "", "Documentary photography about people and places."),
]
ONE = "One or two lines: what it is, where, for whom."
FILMS = [
    ("events", "Events", [("event-film-01", "Event film title", ONE), ("event-film-02", "Event film title", ONE)]),
    ("documentary", "Documentary", [("yt:arH-8EXF31E", "Documentary title", "Paste the description from YouTube here, a few lines.")]),
    ("informational", "Informational", [("informational-01", "Film title", ONE), ("informational-02", "Film title", ONE)]),
]
CV = [("Beaparachute", "2026–present", "Photography, video production and visual marketing material, including information material and creative content. I also do sales towards companies, associations and school classes."),
      ("Freelance Photographer", "2026–present", "Portraits, events and photography assignments for local businesses and others. I’d like to work with artists, musicians, DJs, companies and organisers."),
      ("Järvsöfoto UF", "2025–2026", "Ran my own student company in photography and video: worked with customers and developed a visual style."),
      ("JärvsöLAN", "2025", "Communication, photography and video production for the event.")]
GEAR = ""   # default gear for pictures without EXIF data. Empty = leave gear out (never guessed)
# Per-file info. Key = file path (as in README). Leave out what you don't know.
# "work/events/events-01.jpg": {"year": "2025", "gear": "Canon M50 + Sigma 30mm f/1.4", "about": "English text", "about_sv": "Svensk text"}
INFO = {}

# ---------------- HELPERS ----------------
IMAGES, VIDEOS = [], []
TEMPL = [[1.5,.8,.8],[.8,1.5,.67,1.5],[1.78,.75],[.8,.8,1.5,.67,1.0],[1.5,1.5],[.67,1.0,.8,1.5],[1.0,.75,.75],[.75,1.5,.75,1.33,.8],[2.0,.8],[.8,1.33,.8]]
WID = [100, 100, 84, 100, 70, 100, 92]; GAP = [1, 5, 1, 1, 6, 1, 4]
TR = {"Documentary photography about people and places.": "Dokumentärfoto om människor och platser.", "Commercial": "Kommersiellt", "Everyday life on analogue film.": "Vardagen på analog film.", "Meetings with people on the street. I want the portraits to feel real, not like studio portraits.": "Möten med människor på gatan. Porträtten ska kännas äkta, inte som studioporträtt.", "Moments as they happen on the street.": "Ögonblick som de ser ut på gatan.", "A documentary photo project.": "Ett dokumentärt fotoprojekt.", "Events": "Event", "Portraits": "Porträtt", "Live Music": "Livemusik", "Documentary": "Dokumentär", "Informational": "Informationsfilm",
      "Life on Film": "Life on Film", "Street Portraits": "Gatuporträtt", "Street Photography": "Gatufoto", "Untitled": "Utan titel",
      "Year": "År", "Place": "Plats", "Work": "Arbeten", "Personal Projects": "Egna projekt",
      "A few lines about this project.": "Några rader om projektet.", "Film title": "Filmtitel", "Event film title": "Filmtitel",
      "Documentary title": "Dokumentärens titel", "Paste the description from YouTube here, a few lines.": "Klistra in beskrivningen från YouTube här.",
      ONE: "En eller två rader: vad det är, var, åt vem.", "Events, portraits, live music": "Event, porträtt, livemusik",
      "Life on film, street, documentary": "Life on film, gata, dokumentär", "Events, documentary, informational": "Event, dokumentär, information",
      "Freelance Photographer": "Frilansfotograf", "2026–present": "2026–nu",
      "Photography, video production and visual marketing material, including information material and creative content. I also do sales towards companies, associations and school classes.": "Foto, videoproduktion och visuellt marknadsföringsmaterial, bland annat informationsmaterial och kreativt innehåll. Jag jobbar också med försäljning mot företag, föreningar och klasser.",
      "Portraits, events and photography assignments for local businesses and others. I’d like to work with artists, musicians, DJs, companies and organisers.": "Porträtt, event och fotouppdrag åt lokala företag och andra. Jag vill gärna jobba med artister, musiker, DJs, företag och arrangörer.",
      "Ran my own student company in photography and video: worked with customers and developed a visual style.": "Drev mitt eget UF-företag inom foto och video: jobbade med kunder och utvecklade ett eget visuellt uttryck.",
      "Communication, photography and video production for the event.": "Kommunikation, foto och videoproduktion i samband med eventet."}
def tr(x): return TR.get(x, x) if LANG == "sv" else x

def im(path, alt, r=1.5):
    IMAGES.append(path); stem = path.rsplit(".", 1)[0]; c = "l" if r > 1.1 else "p" if r < .9 else "s"
    fast = os.path.exists(os.path.join(ROOT, "assets/images", stem + "-1000.webp"))   # made by tools/optimize.py
    img = f'<img src="{A}images/{path}" alt="{e(alt)}" loading="lazy" decoding="async">'
    if fast: img = (f'<picture><source type="image/webp" srcset="{A}images/{stem}-1000.webp 1000w, {A}images/{stem}-2000.webp 2000w" sizes="(max-width:800px) 100vw, 50vw">{img}</picture>')
    return (f'<figure class="f {c}" style="--r:{r}"><div class="frame" tabindex="0" role="button" aria-label="{e(alt)} ({L("open larger","öppna större")})">{img}'
            f'<span class="note">Add image<br>assets/images/{path}</span></div></figure>')

def flow(paths, alt, notes=None):
    seed = sum(map(ord, paths[0])); out = []; i = k = 0
    while i < len(paths):
        t = TEMPL[(seed + k) % len(TEMPL)][:len(paths) - i]
        w = WID[(seed + k * 3) % len(WID)]; ml = (100 - w) if k % 2 else 0
        if len(t) == 1: w, ml = 62, (38 if k % 2 else 0)
        al = "end" if (seed + k) % 3 == 0 else "start"
        row = "".join(im(paths[i + j], f"{alt}: {L('photo','foto')} {i + j + 1}, Noah Edlund", r) for j, r in enumerate(t))
        out.append(f'<div class="irow" style="--rw:{w}%;--rml:{ml}%;--al:{al};--rg:{GAP[(seed + k) % len(GAP)]}rem">{row}</div>')
        if notes and k in notes: out.append(f'<p class="interlude">{e(notes[k])}</p>')
        i += len(t); k += 1
    return '<div class="flow">' + "".join(out) + "</div>"

def rows(items):
    out = ""
    for href, title, meta, img in items:
        d = ""
        if img: IMAGES.append(img); d = f' data-img="{A}images/{img}"'
        out += f'<a class="row" href="{href}"{d}><span class="rt">{e(title)}</span><span class="rm">{e(meta)}</span></a>'
    return f'<nav class="index" aria-label="Index">{out}</nav>'

def pim(it, alt):
    r = round(it["w"] / it["h"], 3); c = "l" if r > 1.1 else "p" if r < .9 else "s"; i = it["id"]; src = f"{A}images/{i}"
    img = (f'<picture><source type="image/webp" srcset="{src}-480.webp 480w, {src}-1000.webp 1000w, {src}-2000.webp 2000w" sizes="(max-width:800px) 100vw, 50vw">'
           f'<img src="{src}.jpg" alt="{e(alt)}" width="{it["w"]}" height="{it["h"]}" loading="lazy" decoding="async"></picture>')
    return (f'<figure class="f {c}" style="--r:{r}"><div class="frame" tabindex="0" role="button" aria-label="{e(alt)} ({L("open larger","öppna större")})">{img}'
            f'<span class="note">Missing image<br>{i}</span></div></figure>')

def real_flow(items, alt, key):
    """Rows built from the real picture shapes: 2-5 per row, varied widths, no lonely last picture."""
    seed = sum(map(ord, key)); out = []; i = k = 0; n = len(items)
    while i < n:
        target = [3.4, 2.6, 4.0, 3.0, 3.6][(seed + k) % 5]; row = []; sm = 0
        while i < n and len(row) < 5 and (not row or sm < target):
            row.append(items[i]); sm += items[i]["w"] / items[i]["h"]; i += 1
        if n - i == 1 and len(row) > 2: i -= 1; row.pop()
        w = WID[(seed + k * 3) % len(WID)]
        if len(row) == 1: w = min(w, 62)
        ml = (100 - w) if k % 2 else 0; al = "end" if (seed + k) % 3 == 0 else "start"
        cells = "".join(pim(it, f"{alt}: {L('photo','foto')} {n_ + 1}, Noah Edlund") for n_, it in zip(range(i - len(row), i), row))
        out.append(f'<div class="irow" style="--rw:{w}%;--rml:{ml}%;--al:{al};--rg:{GAP[(seed + k) % len(GAP)]}rem">{cells}</div>'); k += 1
    return '<div class="flow">' + "".join(out) + "</div>"

def gallery(key, alt, n):
    if PH.get(key): return real_flow(PH[key], alt, key)
    return flow([f"{key}/{key.split('/')[-1]}-{i:02d}.jpg" for i in range(1, n + 1)], alt)

def cover(key, fb):
    its = PH.get(key); return (its[0]["id"] + ".jpg") if its else fb

def vid(path, poster, title, desc):
    if path.startswith("yt:"):   # loads from YouTube only after the visitor presses play
        IMAGES.append(poster)
        inner = (f'<button class="yt" type="button" data-id="{path[3:]}" data-title="{e(title)}"><img src="{A}images/{poster}" alt="" loading="lazy">'
                 f'<span class="yt-play">{L("Play","Spela")}</span><span class="yt-hint">{L("Loads from YouTube when you press play.","Laddas från YouTube när du trycker på play.")}</span>'
                 f'<span class="note">Add image<br>assets/images/{poster}</span></button>')
    else:
        VIDEOS.append(path); IMAGES.append(poster)
        inner = (f'<video controls preload="metadata" playsinline poster="{A}images/{poster}"><source src="{A}videos/{path}" type="video/mp4"></video>'
                 f'<span class="note">Add video<br>assets/videos/{path}</span>')
    return f'<article class="film"><div class="vid">{inner}</div><h3>{e(title)}</h3><p>{e(desc)}</p></article>'

def socials():
    return (f'<p class="soc"><a href="{INSTAGRAM}" target="_blank" rel="me noopener">Instagram</a> <a href="{YOUTUBE}" target="_blank" rel="me noopener">YouTube</a> '
            f'<a href="{TIKTOK}" target="_blank" rel="me noopener">TikTok</a> <a href="{LINKEDIN}" target="_blank" rel="me noopener">LinkedIn</a></p>')

def menu(fn):
    o = "sv" if LANG == "en" else "en"
    return f'''<header class="top"><a class="mark" href="index.html">{SITE}</a>
<div class="tools"><a class="lang" href="../{o}/{fn}.html" hreflang="{o}" lang="{o}">{"Svenska" if LANG == "en" else "English"}</a>
<button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="{L("Open menu","Öppna meny")}"><span class="ap"></span></button></div></header>
<div class="menu" id="menu" hidden><div class="menu-bg"></div>
<ul class="menu-list">
<li><a href="about.html"><span>{L("About","Om mig")}</span></a></li>
<li class="has-sub"><button type="button" aria-expanded="false"><span>{L("Gallery","Galleri")}</span></button>
<ul class="sub"><li><a href="work.html">{tr("Work")}</a></li><li><a href="projects.html">{tr("Personal Projects")}</a></li></ul></li>
<li><a href="video.html"><span>Video</span></a></li>
<li><a href="about.html#contact"><span>{L("Contact","Kontakt")}</span></a></li></ul>
<p class="menu-foot"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a><a href="{YOUTUBE}" target="_blank" rel="noopener">YouTube</a><a href="{TIKTOK}" target="_blank" rel="noopener">TikTok</a><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></p></div>'''

PERSON = {"@context": "https://schema.org", "@type": "Person", "name": "Noah Edlund", "alternateName": "thelocalsuedi", "jobTitle": ["Photographer", "Filmmaker"],
          "url": SITE_URL + "/", "email": EMAIL, "address": {"@type": "PostalAddress", "addressRegion": "Hälsingland", "addressCountry": "SE"},
          "sameAs": [INSTAGRAM, YOUTUBE, TIKTOK, LINKEDIN], "image": SITE_URL + "/assets/images/og/og-image.jpg", "knowsLanguage": ["sv", "en"],
          "knowsAbout": ["Photography", "Film", "Event photography", "Portrait photography", "Live music photography", "Documentary", "Street photography"]}
PAGES = []
def page(fn, title, desc, body, home=False, cls="", person=False):
    IMAGES.append("og/og-image.jpg"); PAGES.append(fn)
    full = title if home else f"{title} | {SITE}"; url = f"{SITE_URL}/{LANG}/{fn}.html"; ld = ""
    if person or home:
        d = dict(PERSON); d["description"] = desc; ld = f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>'
    stats = (f'<script data-goatcounter="https://{GOATCOUNTER}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>' if GOATCOUNTER else "")
    html = f'''<!doctype html>
<html lang="{LANG}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(full)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{SITE_URL}/en/{fn}.html"><link rel="alternate" hreflang="sv" href="{SITE_URL}/sv/{fn}.html"><link rel="alternate" hreflang="x-default" href="{SITE_URL}/index.html">
<meta property="og:title" content="{e(full)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{url}">
<meta property="og:site_name" content="{SITE}"><meta property="og:locale" content="{L("en_GB","sv_SE")}"><meta property="og:image" content="{SITE_URL}/assets/images/og/og-image.jpg"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#ffffff">{FAV.format(p=P)}<link rel="stylesheet" href="{A}css/style.css">{ld}</head>
<body class="{cls}"><a class="skip" href="#main">{L("Skip to content","Hoppa till innehållet")}</a>{menu(fn)}
<main id="main">{body}</main>
<footer class="foot"><a href="mailto:{EMAIL}">{EMAIL}</a><span>Hälsingland, Sweden</span>{socials()}<span>© 2026 Noah Edlund &nbsp; <a href="privacy.html">{L("Privacy","Integritet")}</a></span></footer>
<div class="peek" aria-hidden="true"><img alt=""></div><script src="{A}js/main.js" defer></script>{stats}</body></html>'''
    open(os.path.join(OUT, fn + ".html"), "w", encoding="utf-8").write(html)

head = lambda t: f'<section class="pagehead"><h1>{e(t)}</h1></section>'
SEO = {"events": ("Event photographer in Hälsingland", "Eventfotograf i Hälsingland"), "portraits": ("Portrait photographer in Hälsingland", "Porträttfotograf i Hälsingland"),
       "live-music": ("Live music and concert photography", "Konsertfotograf och livemusikfoto"),
       "commercial": ("Commercial photography in Hälsingland", "Kommersiell fotografering i Hälsingland")}
BY = L("Photographs by Noah Edlund (thelocalsuedi.), Hälsingland, Sweden.", "Bilder av Noah Edlund (thelocalsuedi.), Hälsingland.")
AV = AVAILABLE[LANG]; AVP = f'<p class="avail">{e(AV)}</p>' if AV else ""

hero = (
    f'<section class="hero">'
    f'<h1>{SITE}</h1>'
    f'<p>{L("Photographer and filmmaker, Hälsingland, Sweden.","Fotograf och filmare i Hälsingland.")}</p>'
    f'</section>'
)

# ---------------- PAGES ----------------
intro = (f'<section class="note-block"><p>{L("I’m Noah. I photograph and film people, music and the places around me in Hälsingland, on digital and on film.","Jag heter Noah. Jag fotar och filmar människor, musik och platserna runt omkring mig i Hälsingland, både digitalt och på film.")}</p>'
         f'<p>{L("I work at Beaparachute and take freelance jobs: portraits, events and video for local businesses.","Jag jobbar på Beaparachute och tar frilansuppdrag: porträtt, event och video åt lokala företag.")} '
         f'<a href="about.html">{L("About me","Om mig")}</a> / <a href="video.html#documentary">{L("Watch my documentary","Se min dokumentär")}</a></p>{AVP}</section>')
home_idx = rows([("work.html", tr("Work"), tr("Events, portraits, live music"), ""), ("projects.html", tr("Personal Projects"), tr("Life on film, street, documentary"), ""), ("video.html", "Video", tr("Events, documentary, informational"), "")])
page("index", L("Noah Edlund – Photographer and filmmaker in Hälsingland | thelocalsuedi.", "Noah Edlund – Fotograf och filmare i Hälsingland | thelocalsuedi."),
     L("Noah Edlund (thelocalsuedi.) is a photographer and filmmaker in Hälsingland, Sweden. Event, portrait and live music photography, documentary and video.",
       "Noah Edlund (thelocalsuedi.) är fotograf och filmare i Hälsingland. Event, porträtt, livemusik, dokumentär och video."),
     hero + intro + f'<section class="home-index">{home_idx}</section>', home=True, cls="home")

page("work", L("Photography: events, portraits and live music", "Fotografi: event, porträtt och livemusik"), BY,
     head(tr("Work")) + rows([(f"work-{s}.html", tr(t), "", cover(f"work/{s}", f"work/{s}/cover.jpg")) for s, t in WORK]))
for s, t in WORK:
    page(f"work-{s}", L(*SEO[s]), f"{L(*SEO[s])}. {BY}", f'<section class="pagehead"><h1>{tr(t)}</h1><p class="back"><a href="work.html">{tr("Work")}</a></p></section>'
         + gallery(f"work/{s}", L(*SEO[s]), 14))

known = {p[0] for p in PROJECTS}
for k in PH:
    if k.startswith("projects/") and k.split("/", 1)[1] not in known:
        sl = k.split("/", 1)[1]; PROJECTS.append((sl, sl.replace("-", " ").title(), "Documentary", "", "", ""))
body = head(tr("Personal Projects")) + rows([(f"project-{p[0]}.html", tr(p[1]), tr(p[3]), cover(f"projects/{p[0]}", f"projects/{p[0]}/cover.jpg")) for p in PROJECTS])
page("projects", L("Personal projects: street photography, life on film, documentary", "Egna projekt: gatufoto, life on film, dokumentär"), BY, body)
for s, t, g, yr, pl, txt in PROJECTS:
    meta = (e(tr(g)) if g != t else "") + (("<br>" if g != t else "") + e(", ".join(x for x in (tr(yr), tr(pl)) if x)) if (yr or pl) else "")
    hd = (f'<section class="pagehead project-head"><h1>{e(tr(t))}</h1><div>' + (f"<p>{e(tr(txt))}</p>" if txt else "") + (f'<p class="meta">{meta}</p>' if meta else "") +
          f'<p class="back"><a href="projects.html">{tr("Personal Projects")}</a></p></div></section>')
    page(f"project-{s}", tr(t) if g == t else f"{tr(t)} ({tr(g)})", f"{tr(t)}: {tr(g)}. {BY}", hd + gallery(f"projects/{s}", tr(t), 12))

# ---------------- VIDEO: curated film portfolio (descriptions hidden until "Read description") ----------------
FE = ("Filming & editing", "Filmning & klippning")
def V(g, id, src, title, role, place, year, en, sv): return dict(g=g, id=id, src=src, title=title, role=role, place=place, year=year, en=en, sv=sv)
FILMS_ = [
 V("feature", "rehnstroms", ("yt", "arH-8EXF31E"), "Rehnströms: a camera store in transition", ("Concept, planning, filming, directing & editing", "Idé, planering, filmning, regi & klippning"), "", "",
   "A documentary about the people, history and everyday life behind Rehnströms, a camera store in an industry that keeps changing. Independently produced, from concept and planning to filming and final edit.",
   "En dokumentär om människorna, historien och vardagen bakom Rehnströms, en kamerabutik i en bransch som ständigt förändras. Producerad på egen hand, från idé och planering till filmning och slutklipp."),
 V("event", "uf-gavleborg", ("yt", "oKfWtkiNzWI"), "Ung Företagsamhet Gävleborg: UF event", FE, "Bollnäs", "",
   "A promotional film from a regional UF event in Bollnäs, where young businesses from across Gävleborg gathered for exhibitions, competitions, presentations and activities. Made for Ung Företagsamhet Gävleborg.",
   "En promotionfilm från ett regionalt UF-event i Bollnäs, där unga företag från hela Gävleborg samlades för utställningar, tävlingar, presentationer och aktiviteter. Gjord för Ung Företagsamhet Gävleborg."),
 V("event", "bike-festival", ("ig", "DbgyoDkOb13"), "Järvsö Bike Festival: event edit", FE, "Järvsö", "",
   "A fast edit from Järvsö Bike Festival, filmed and edited by me and later shared on the festival’s own channels.",
   "En snabb eventfilm från Järvsö Bike Festival, filmad och klippt av mig och senare delad på festivalens egna kanaler."),
 V("event", "lake-jump", ("ig", "Dbh8zyCOc4c"), "Lake Jump: Järvsö 2026", FE, "Järvsö", "2026",
   "A summer event where mountain bikers gathered to jump into the lake. Fast, with a lot of movement and spontaneous moments.",
   "Ett sommarevent där mountainbikecyklister samlades för att hoppa i sjön. Snabbt, med mycket rörelse och spontana ögonblick."),
 V("event", "redbull", ("ig", "DbgzTxNOzz0"), "Red Bull: Järvsö Bike Festival", FE, "Järvsö", "",
   "A spontaneous edit built around a rider handing out Red Bull cans during Järvsö Bike Festival. A simple idea turned into a short film.",
   "En spontan film byggd kring en cyklist som delar ut Red Bull-burkar under Järvsö Bike Festival. En enkel idé som blev en kort film."),
 V("event", "redbull-bts", ("ig", "DbsbrcRujua"), "Behind the scenes: Red Bull edit", None, "Järvsö", "",
   "Behind the scenes of the Red Bull edit, showing some of the process behind the finished film.",
   "Bakom kulisserna av Red Bull-filmen, med en titt på en del av processen bakom den färdiga filmen."),
 V("live", "blessed-insanity", ("ig", "Da_FULTO6au"), "Blessed Insanity: live", FE, "", "",
   "A commissioned live film of Blessed Insanity’s performance, made as a visual edit for the band.",
   "En beställd livefilm av Blessed Insanitys spelning, gjord som en visuell klippning åt bandet."),
 V("live", "electric-feelgood", ("ig", "DMnTS4Bts04"), "Electric Feelgood: live at Rosehills", FE, "Rosehills", "2025",
   "A personal live project filmed at Rosehills in 2025. I brought my camera, filmed the band and cut the footage into a short film.",
   "Ett eget liveprojekt filmat på Rosehills 2025. Jag tog med kameran, filmade bandet och klippte materialet till en kort film."),
 V("personal", "fjarilshuset", ("ig", "DJNbZHpKOmG"), "Fjärilshuset: Stockholm", FE, "Stockholm", "",
   "A short personal film made during a visit to Fjärilshuset in Stockholm. I brought my camera and turned the visit into an edit.",
   "En kort personlig film gjord under ett besök på Fjärilshuset i Stockholm. Jag tog med kameran och gjorde besöket till en klippning."),
 V("edit", "slotboythim", ("yt", "C_gGPVL7eAA"), "Slotboythim: video edit", ("Video editing", "Videoklippning"), "", "",
   "An editing project where I took on the post-production of an entire video, working in a visual style and editing approach that was new to me.",
   "Ett klippprojekt där jag tog hand om hela efterbearbetningen av en video, i en visuell stil och klippmetod som var ny för mig."),
]
def vcard(v):
    yt = v["src"][0] == "yt"; sid = v["src"][1]; IMAGES.append(f"video/{v['id']}.jpg")
    link = f"https://youtu.be/{sid}" if yt else f"https://www.instagram.com/reel/{sid}/"
    meta = " · ".join(x for x in [L(*v["role"]) if v["role"] else "", v["place"], v["year"]] if x)
    src_name = "YouTube" if yt else "Instagram"
    return (f'<article class="vc {"h" if yt else "v"}" id="{v["id"]}"><div class="vframe"><img src="{A}images/video/{v["id"]}.jpg" alt="" loading="lazy" decoding="async">'
            f'<span class="note">Add image<br>assets/images/video/{v["id"]}.jpg</span>'
            f'<button class="vplay" type="button" data-k="{v["src"][0]}" data-id="{sid}" data-title="{e(v["title"])}"><span class="vplay-t">{L("Play","Spela")}</span>'
            f'<span class="vplay-h">{L("Loads from " + src_name + " when you press play.", "Laddas från " + src_name + " när du trycker på play.")}</span></button></div>'
            f'<div class="vmeta"><h3>{e(v["title"])}</h3>' + (f'<p class="vsub">{e(meta)}</p>' if meta else "") +
            f'<button class="vmore" type="button" aria-expanded="false" aria-controls="d-{v["id"]}">{L("Read description","Läs beskrivning")}</button>'
            f'<div class="vdesc" id="d-{v["id"]}"><div><p>{e(v["en"] if LANG == "en" else v["sv"])}</p></div></div>'
            f'<a class="vlink" href="{link}" target="_blank" rel="noopener">{L("Watch on","Se på")} {src_name}</a></div></article>')
byid = {v["id"]: v for v in FILMS_}; grp = lambda g: [v for v in FILMS_ if v["g"] == g]
ev = "".join(vcard(byid[i]) for i in ("uf-gavleborg", "bike-festival", "lake-jump"))
pair = f'<div class="vpair" role="group" aria-label="Red Bull">{vcard(byid["redbull"])}{vcard(byid["redbull-bts"])}</div>'
vb = ('<section class="pagehead"><h1>Video</h1><p class="jump"><a href="#documentary">' + tr("Documentary") + f'</a> <a href="#events">{L("Events","Event")}</a> <a href="#live">{tr("Live Music")}</a> '
      f'<a href="#personal">{L("Personal","Personligt")}</a> <a href="#editing">{L("Editing","Klippning")}</a></p></section>'
      f'<section class="vsec vfeat" id="documentary"><h2>{tr("Documentary")}</h2>{vcard(byid["rehnstroms"])}</section>'
      f'<section class="vsec" id="events"><h2>{L("Events and promotion","Event och promotion")}</h2><div class="vrow">{ev}{pair}</div></section>'
      f'<section class="vsec" id="live"><h2>{tr("Live Music")}</h2><div class="vrow">{"".join(vcard(v) for v in grp("live"))}</div></section>'
      f'<section class="vsec" id="personal"><h2>{L("Personal","Personligt")}</h2><div class="vrow">{vcard(byid["fjarilshuset"])}</div></section>'
      f'<section class="vsec" id="editing"><h2>{L("Editing","Klippning")}</h2><div class="vrow">{vcard(byid["slotboythim"])}</div></section>')
page("video", L("Video: documentary, event films and live music", "Video: dokumentär, eventfilmer och livemusik"),
     L("Films by Noah Edlund (thelocalsuedi.): documentary, event films, live music and edits, Hälsingland, Sweden.", "Filmer av Noah Edlund (thelocalsuedi.): dokumentär, eventfilmer, livemusik och klippning, Hälsingland."), vb)

cvh = "".join(f'<div class="cv-row"><h3>{e(tr(n))}</h3><span>{tr(y)}</span><p>{e(tr(x))}</p></div>' for n, y, x in CV)
what = "".join(f'<div class="cv-row"><h3>{n}</h3><p>{x}</p></div>' for n, x in [
    (L("Photography", "Foto"), L("Events, portraits and live music.", "Event, porträtt och livemusik.")),
    (L("Film", "Film"), L("Event films, documentary and videos for companies.", "Eventfilmer, dokumentär och filmer åt företag.")),
    (L("Personal projects", "Egna projekt"), L("Street photography, street portraits, life on film and documentary.", "Gatufoto, gatuporträtt, life on film och dokumentär."))])
edu = f'<div class="cv-row"><h3>Järvsögymnasiet</h3><span>2023–2026</span><p>{L("Aesthetic programme, media specialisation. Graduated 2026.","Estetiska programmet, inriktning media. Tog studenten 2026.")}</p></div>'
gear = "".join(f'<div class="cv-row"><h3>{n}</h3><p>{x}</p></div>' for n, x in [
    (L("Digital", "Digitalt"), "Canon M50, Sigma 30mm f/1.4"), (L("Analogue", "Analogt"), "Mamiya RB67, Canon AE-1, Yashica-C")])
IMAGES.append("about/noah-portrait.jpg")
page("about", L("About Noah Edlund, photographer and filmmaker in Hälsingland", "Om Noah Edlund, fotograf och filmare i Hälsingland"),
     L("Noah Edlund (thelocalsuedi.) is a photographer and filmmaker from Hälsingland, Sweden. Experience, services and contact details.", "Noah Edlund (thelocalsuedi.) är fotograf och filmare från Hälsingland. Erfarenhet, tjänster och kontaktuppgifter."),
     f'''<section class="about"><div class="portrait"><div class="frame" style="--r:4/5"><img src="{A}images/about/noah-portrait.jpg" alt="{L("Portrait of Noah Edlund, photographer","Porträtt av Noah Edlund, fotograf")}">
<span class="note">Portrait placeholder<br>assets/images/about/noah-portrait.jpg</span></div></div>
<div class="about-text"><h1>Noah Edlund</h1><p class="lead">{L("Photographer and filmmaker from Hälsingland, Sweden.","Fotograf och filmare från Hälsingland.")}</p>
<p>{L("I photograph and film people, places and situations that haven’t been arranged. What happens in front of the camera interests me more than what I can set up, and a picture should say something, not just be technically right.","Jag fotar och filmar människor, platser och situationer som inte är tillrättalagda. Det som händer framför kameran intresserar mig mer än det jag kan arrangera, och en bild ska säga något, inte bara vara tekniskt rätt.")}</p>
<p>{L("Hälsingland is where I’m from and a big part of what I do. I shoot both digital and analogue, and film and medium format are a big interest. I like dark rooms, available light and places with character.","Hälsingland är min hembygd och en stor del av det jag gör. Jag fotar både digitalt och analogt, och film och mellanformat är ett stort intresse. Jag gillar mörka miljöer, befintligt ljus och platser med karaktär.")}</p>
<p>{L("I want to do more documentary work: longer stories about people and society, music, and my own projects. Alongside that I take assignments: portraits, events, concerts and film.","Jag vill göra mer dokumentärt arbete: längre berättelser om människor och samhälle, musik och egna projekt. Vid sidan av det tar jag uppdrag: porträtt, event, konserter och film.")}</p>{AVP}
<h2>{L("What I do","Vad jag gör")}</h2><div class="cv">{what}</div><h2>{L("Experience","Erfarenhet")}</h2><div class="cv">{cvh}</div>
<h2>{L("Education","Utbildning")}</h2><div class="cv">{edu}</div>
<h2>{L("Gear","Utrustning")}</h2><div class="cv">{gear}</div>
<h2>{L("Latest","Senast")}</h2><p>{L("My documentary is on the","Min dokumentär finns på")} <a href="video.html#documentary">{L("video page","videosidan")}</a>.</p>
<div id="contact" class="contactbox"><h2>{L("Work with me","Anlita mig")}</h2><p>{L("I’m based in Hälsingland and take assignments elsewhere too: portraits, events, concerts and video. Location, scope and content are agreed before booking. Prices on request. I write in Swedish and English.","Jag utgår från Hälsingland men tar uppdrag på andra orter också: porträtt, event, konserter och film. Plats, omfattning och innehåll bestämmer vi innan bokning. Pris efter förfrågan. Jag skriver på svenska och engelska.")}</p>
<p class="lead"><a href="mailto:{EMAIL}">{EMAIL}</a></p>{socials()}</div></div></section>''', person=True)

stat_en = ("<h2>Cookies and statistics</h2><p>This site doesn’t use cookies or advertising. I count visits with GoatCounter, which doesn’t use cookies or identify individual visitors. It records things like which page was opened, and roughly which country, browser and referrer it came from.</p>" if GOATCOUNTER
           else "<h2>Cookies and statistics</h2><p>This site doesn’t use cookies, analytics or advertising.</p>")
stat_sv = ("<h2>Cookies och statistik</h2><p>Sidan använder inga cookies och ingen reklam. Jag räknar besök med GoatCounter, som inte använder cookies och inte identifierar enskilda besökare. Det registreras till exempel vilken sida som öppnades, och ungefär vilket land, vilken webbläsare och vilken länk besöket kom från.</p>" if GOATCOUNTER
           else "<h2>Cookies och statistik</h2><p>Sidan använder inga cookies, ingen statistik och ingen reklam.</p>")
page("privacy", L("Privacy and contact details", "Integritet och kontaktuppgifter"), L("Contact details, privacy information and copyright for thelocalsuedi.", "Kontaktuppgifter, integritetsinformation och upphovsrätt för thelocalsuedi."),
     head(L("Privacy and contact", "Integritet och kontakt")) + '<section class="legal">' + L(
     f"""<h2>Who runs this site</h2><p>Noah Edlund (thelocalsuedi.)<br>[PO box or c/o address to be added], Sweden<br>Email: <a href="mailto:{EMAIL}">{EMAIL}</a></p>{stat_en}
<h2>Videos</h2><p>YouTube and Instagram videos only load after you press play. Then YouTube (Google) or Instagram (Meta) receives data such as your IP address, under their own privacy policies. Every film also has a direct link to the original.</p>
<h2>People in my pictures</h2><p>My photos and films show real people. If you appear in something and want it removed, email me and I’ll take care of it.</p>
<h2>If you email me</h2><p>I use your message and email address only to reply to you. You can ask me to delete them. Complaints about how I handle personal data can go to the Swedish Authority for Privacy Protection (IMY), imy.se.</p>
<h2>Copyright</h2><p>All photographs, films and text on this site are © Noah Edlund. Please don’t copy or reuse them without asking.</p>""",
     f"""<h2>Vem som driver sidan</h2><p>Noah Edlund (thelocalsuedi.)<br>[Postbox eller c/o-adress läggs till], Sverige<br>E-post: <a href="mailto:{EMAIL}">{EMAIL}</a></p>{stat_sv}
<h2>Videor</h2><p>YouTube- och Instagram-videor laddas först när du trycker på play. Då får YouTube (Google) eller Instagram (Meta) uppgifter som din IP-adress, enligt deras egna integritetspolicyer. Varje film har också en direktlänk till originalet.</p>
<h2>Personer i mina bilder</h2><p>Mina foton och filmer visar riktiga människor. Om du syns i något och vill att det tas bort, mejla mig så ordnar jag det.</p>
<h2>Om du mejlar mig</h2><p>Jag använder ditt meddelande och din e-postadress bara för att svara dig. Du kan be mig radera dem. Klagomål på hur jag hanterar personuppgifter kan skickas till Integritetsskyddsmyndigheten (IMY), imy.se.</p>
<h2>Upphovsrätt</h2><p>Alla foton, filmer och texter på sidan är © Noah Edlund. Kopiera eller återanvänd dem inte utan att fråga.</p>""") + "</section>")

if LANG == "en":
    open(os.path.join(ROOT, ".pages"), "w").write(" ".join(PAGES))
    u = lambda l: list(dict.fromkeys(l))
    open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write(f"""# thelocalsuedi.
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
""" + "\n".join(f"- `{p}`" for p in u(IMAGES + ["menu/menu-bg.jpg"])) + "\n\n## Videos (assets/videos/)\n" + "\n".join(f"- `{p}`" for p in u(VIDEOS)) + "\n")
print(LANG, "done")
