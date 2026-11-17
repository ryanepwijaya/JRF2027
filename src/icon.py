"""Generate ikon app (runner) -> icons/*.png + icons/icon.svg. Jalankan: python3 src/icon.py"""
import os
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "icons")

RUNNER = '''<g fill="none" stroke="#fff" stroke-linecap="round" stroke-linejoin="round">
  <g stroke-width="22" opacity=".55"><line x1="62" y1="236" x2="128" y2="236"/><line x1="42" y1="292" x2="118" y2="292"/><line x1="70" y1="348" x2="122" y2="348"/></g>
  <g stroke-width="40">
    <polyline points="268,208 210,240 168,206"/>
    <polyline points="244,306 198,376 126,394"/>
    <line x1="290" y1="182" x2="244" y2="306"/>
    <polyline points="244,306 330,340 300,432"/>
    <polyline points="276,214 338,252 384,214"/>
  </g>
  <circle cx="318" cy="120" r="42" fill="#fff" stroke="none"/>
</g>'''
GRAD = '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff7a3d"/><stop offset="1" stop-color="#f0430f"/></linearGradient></defs>'

def svg(kind):
    if kind == "maskable":   # full bleed, figure inside 70% safe zone
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">{GRAD}<rect width="512" height="512" fill="url(#g)"/><g transform="translate(256 256) scale(.72) translate(-246 -270)">{RUNNER}</g></svg>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">{GRAD}<rect width="512" height="512" rx="116" fill="url(#g)"/><g transform="translate(256 256) scale(.9) translate(-246 -270)">{RUNNER}</g></svg>'

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "icon.svg"), "w").write(svg("any"))
    targets = [("icon-192.png", "any", 192), ("icon-512.png", "any", 512), ("maskable-512.png", "maskable", 512),
               ("maskable-192.png", "maskable", 192), ("apple-touch-icon.png", "maskable", 180), ("favicon-32.png", "any", 32)]
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, kind, size in targets:
            pg = b.new_page(viewport={"width": size, "height": size})
            pg.set_content(f'<html><body style="margin:0;background:transparent">{svg(kind).replace("<svg ", f"<svg width=\'{size}\' height=\'{size}\' ", 1)}</body></html>')
            pg.screenshot(path=os.path.join(OUT, name), omit_background=True, clip={"x": 0, "y": 0, "width": size, "height": size})
            pg.close()
        b.close()
    print("ikon dibuat:", ", ".join(t[0] for t in targets))
