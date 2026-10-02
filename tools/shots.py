#!/usr/bin/env python3
"""Viewport screenshots of the demo build (desktop / tablet / phone)."""
import pathlib
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8741/"
OUT = pathlib.Path(__file__).resolve().parent.parent / "shots"
OUT.mkdir(exist_ok=True)

PAGES = ["index.html", "about.html", "team.html", "contact.html"]
VIEWS = [("desktop", 1280, 720), ("tablet", 834, 720), ("phone", 390, 760)]

with sync_playwright() as p:
    b = p.chromium.launch()
    for vname, w, h in VIEWS:
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        for page in PAGES:
            pg.goto(BASE + page, wait_until="load")
            pg.wait_for_timeout(450)
            stem = page.replace(".html", "")
            pg.screenshot(path=str(OUT / f"{vname}-{stem}-top.png"))
            # second viewport-sized frame further down the page
            pg.evaluate("window.scrollTo(0, Math.min(document.body.scrollHeight, window.innerHeight*1.7))")
            pg.wait_for_timeout(350)
            pg.screenshot(path=str(OUT / f"{vname}-{stem}-mid.png"))
        if vname == "phone":
            pg.goto(BASE + "index.html", wait_until="load")
            pg.click(".nav-toggle")
            pg.wait_for_timeout(300)
            pg.screenshot(path=str(OUT / "phone-nav-open.png"))
        errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.close()
    b.close()
print("shots written to", OUT)
