#!/usr/bin/env python3
"""Rendert Karussell-Slides (1080x1350 JPG) aus posts/<ordner>/slides.json.

Aufruf:  python3 tools/render.py posts/2026-10-06-website-anfragen
"""
import base64
import html
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
FONT = ROOT / "fonts" / "Archivo-VariableFont.ttf"
W, H = 1080, 1350

CSS = """
@font-face {
  font-family: 'Archivo';
  src: url(data:font/ttf;base64,%(font)s) format('truetype');
  font-weight: 100 900; font-stretch: 62%% 125%%;
}
:root { --bg:#EEF1F5; --ink:#14213D; --accent:#FFC93C; --grey:#5B6B86; }
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:%(w)dpx; height:%(h)dpx; }
body { font-family:'Archivo', sans-serif; background:var(--bg); color:var(--ink);
       -webkit-font-smoothing:antialiased; }
.slide { position:relative; width:100%%; height:100%%; padding:96px 88px;
         display:flex; flex-direction:column; }
.dark { background:var(--ink); color:#fff; }
h1, h2 { font-weight:800; font-stretch:75%%; line-height:.98; letter-spacing:-.01em; }
.counter { position:absolute; top:72px; right:88px; font-size:30px; font-weight:600;
           color:var(--grey); letter-spacing:.04em; }
.dark .counter { color:rgba(255,255,255,.55); }
.handle { position:absolute; bottom:64px; left:88px; font-size:28px; font-weight:600;
          color:var(--grey); }
.dark .handle { color:rgba(255,255,255,.6); }

/* Cover */
.bubble { align-self:flex-start; margin-top:40px; display:flex; gap:24px; align-items:center;
          background:var(--accent); color:var(--ink); border-radius:32px; padding:28px 36px;
          box-shadow:0 24px 60px rgba(0,0,0,.35); transform:rotate(-2deg); }
.bubble .icon { width:64px; height:64px; border-radius:18px; background:var(--ink);
                display:grid; place-items:center; flex:none; }
.bubble .icon svg { width:36px; height:36px; }
.bubble .meta { font-size:24px; font-weight:600; opacity:.7; }
.bubble .msg { font-size:40px; font-weight:800; font-stretch:75%%; margin-top:4px; }
.cover h1 { font-size:118px; margin-top:auto; }
.cover h1 em { font-style:normal; color:var(--accent); }
.cover .sub { font-size:40px; line-height:1.3; margin-top:40px; color:rgba(255,255,255,.82);
              max-width:820px; }
.cover .rule { width:120px; height:10px; background:var(--accent); margin-top:56px;
               margin-bottom:96px; }

/* Inhalt */
.num { font-size:200px; font-weight:800; font-stretch:75%%; line-height:.8; color:var(--accent);
       -webkit-text-stroke:3px var(--ink); margin-top:24px; }
.content h2 { font-size:104px; margin-top:48px; }
.content .text { font-size:40px; line-height:1.38; color:var(--grey); margin-top:40px; }
.fix { margin-top:auto; margin-bottom:72px; background:var(--accent); border-radius:28px;
       padding:40px 44px; }
.fix .label { font-size:26px; font-weight:800; letter-spacing:.12em; text-transform:uppercase; }
.fix .body { font-size:38px; line-height:1.32; font-weight:600; margin-top:14px; }
.outro { font-size:32px; font-weight:700; margin-top:-36px; margin-bottom:72px; }
"""

BELL = ('<svg viewBox="0 0 24 24" fill="none" stroke="#FFC93C" stroke-width="2.2" '
        'stroke-linecap="round" stroke-linejoin="round"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/>'
        '<path d="M13.7 21a2 2 0 0 1-3.4 0"/></svg>')


def e(s):
    return html.escape(s)


def cover(s, i, n):
    meta, msg = s["bubble"]
    return f"""<div class="slide dark cover">
  <div class="counter">{i}/{n}</div>
  <div class="bubble"><div class="icon">{BELL}</div>
    <div><div class="meta">{e(meta)}</div><div class="msg">{e(msg)}</div></div></div>
  <h1>{s["headline_html"]}</h1>
  <p class="sub">{e(s["sub"])}</p>
  <div class="rule"></div>
  <div class="handle">{e(s["footer"])}</div>
</div>"""


def content(s, i, n):
    outro = f'<p class="outro">{e(s["footer"])}</p>' if s.get("footer") else ""
    return f"""<div class="slide content">
  <div class="counter">{i}/{n}</div>
  <div class="num">{i - 1:02d}</div>
  <h2>{e(s["headline"])}</h2>
  <p class="text">{e(s["text"])}</p>
  <div class="fix"><div class="label">So behebst du es</div><div class="body">{e(s["fix"])}</div></div>
  {outro}
  <div class="handle">@efetack</div>
</div>"""


def main(post_dir):
    post = Path(post_dir).resolve()
    slides = json.loads((post / "slides.json").read_text(encoding="utf-8"))
    css = CSS % {"font": base64.b64encode(FONT.read_bytes()).decode(), "w": W, "h": H}
    n = len(slides)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for i, s in enumerate(slides, 1):
            body = cover(s, i, n) if s["type"] == "cover" else content(s, i, n)
            page.set_content(f"<!doctype html><html lang='de'><head><meta charset='utf-8'>"
                             f"<style>{css}</style></head><body>{body}</body></html>")
            page.evaluate("document.fonts.ready")
            out = post / f"slide-{i:02d}.jpg"
            page.screenshot(path=str(out), type="jpeg", quality=92)
            print(out.relative_to(post.parent.parent))
        browser.close()


if __name__ == "__main__":
    main(sys.argv[1])
