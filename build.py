"""Build index.html + sw.js dari src/.

- src/plan.py          : data program (sesi, WU/Main/CD, zona, libur, blok, gym)
- src/template.html    : tampilan
- src/sw.template.js   : service worker (PWA, offline)
- src/icon.py          : generator ikon (jalankan terpisah kalau ikon diubah)
- data/actuals.json    : realisasi latihan (Coros/Strava), diperbarui mingguan
- data/body.json       : berat & komposisi tubuh

Cara pakai:  python3 build.py
"""
import hashlib, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")

subprocess.run([sys.executable, os.path.join(SRC, "plan.py")], check=True, stdout=subprocess.DEVNULL)
data = open(os.path.join(SRC, "plan.json"), encoding="utf-8").read()
plan = json.loads(data)  # validasi
for key, fn in [("actuals", "actuals.json"), ("body", "body.json")]:
    fp = os.path.join(ROOT, "data", fn)
    plan[key] = json.load(open(fp, encoding="utf-8")) if os.path.exists(fp) else None
trp = os.path.join(SRC, "i18n_data_en.json")
plan["tr"] = json.load(open(trp, encoding="utf-8")) if os.path.exists(trp) else {}
data = json.dumps(plan, ensure_ascii=False)
tpl = open(os.path.join(SRC, "template.html"), encoding="utf-8").read()
assert "__DATA__" in tpl
uip = os.path.join(SRC, "i18n_ui_en.json")
ui = open(uip, encoding="utf-8").read() if os.path.exists(uip) else "{}"
json.loads(ui)
out = tpl.replace("__DATA__", data.replace("</", "<\\/")).replace("__UI_EN__", ui.replace("</", "<\\/"))
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
