"""Build index.html + sw.js dari src/.

- src/plan.py          : data program (sesi, WU/Main/CD, zona, libur, blok, gym)
- src/template.html    : tampilan
- src/sw.template.js   : service worker (PWA, offline)
- src/icon.py          : generator ikon (jalankan terpisah kalau ikon diubah)

Cara pakai:  python3 build.py
"""
import hashlib, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")

subprocess.run([sys.executable, os.path.join(SRC, "plan.py")], check=True, stdout=subprocess.DEVNULL)
data = open(os.path.join(SRC, "plan.json"), encoding="utf-8").read()
json.loads(data)  # validasi
tpl = open(os.path.join(SRC, "template.html"), encoding="utf-8").read()
assert "__DATA__" in tpl
out = tpl.replace("__DATA__", data.replace("</", "<\\/"))
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(out)

h = hashlib.sha1()
for f in [out.encode(), open(os.path.join(ROOT, "manifest.webmanifest"), "rb").read()]:
    h.update(f)
for name in sorted(os.listdir(os.path.join(ROOT, "icons"))):
    h.update(open(os.path.join(ROOT, "icons", name), "rb").read())
ver = h.hexdigest()[:10]
sw = open(os.path.join(SRC, "sw.template.js"), encoding="utf-8").read().replace("__VERSION__", ver)
open(os.path.join(ROOT, "sw.js"), "w", encoding="utf-8").write(sw)
print(f"index.html dibuat ({len(out)/1024:.0f} KB) · sw.js versi {ver}")
