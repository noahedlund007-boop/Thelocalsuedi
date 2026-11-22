#!/usr/bin/env python3
"""Saves the FIRST FRAME of each film as its poster picture.
Put your video files in assets/originals/video/ named: rehnstroms, uf-gavleborg, bike-festival, lake-jump, redbull, redbull-bts,
blessed-insanity, electric-feelgood, fjarilshuset, slotboythim  (.mp4 or .mov). Needs ffmpeg installed.
Writes assets/images/video/<name>.jpg. For a YouTube film without a file here it falls back to YouTube's own thumbnail (not the first frame)."""
import os, subprocess, shutil, urllib.request
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, DST = os.path.join(HERE, "assets/originals/video"), os.path.join(HERE, "assets/images/video")
YT = {"rehnstroms": "arH-8EXF31E", "uf-gavleborg": "oKfWtkiNzWI", "slotboythim": "C_gGPVL7eAA"}
NAMES = ["rehnstroms", "uf-gavleborg", "bike-festival", "lake-jump", "redbull", "redbull-bts", "blessed-insanity", "electric-feelgood", "fjarilshuset", "slotboythim"]
os.makedirs(DST, exist_ok=True)
if not shutil.which("ffmpeg"): print("ffmpeg not found. Install it first: sudo apt-get install -y ffmpeg")
for n in NAMES:
    out = os.path.join(DST, n + ".jpg"); f = next((os.path.join(SRC, n + e) for e in (".mp4", ".mov", ".MP4", ".MOV") if os.path.exists(os.path.join(SRC, n + e))), None)
    if f and shutil.which("ffmpeg"):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f, "-frames:v", "1", "-vf", "scale='min(1280,iw)':-2", "-q:v", "3", out], check=True); print("first frame:", n)
    elif n in YT:
        try: urllib.request.urlretrieve(f"https://i.ytimg.com/vi/{YT[n]}/maxresdefault.jpg", out); print("YouTube thumbnail (not first frame):", n)
        except Exception as ex: print("MISSING (no video file, no thumbnail):", n, ex)
    else: print("MISSING (add the video file to assets/originals/video/):", n)
