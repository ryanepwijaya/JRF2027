"""Build index.html dari src/plan.py (data program) + src/template.html (tampilan).

Cara pakai:  python3 build.py
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")

subprocess.run([sys.executable, os.path.join(SRC, "plan.py")], check=True, stdout=subprocess.DEVNULL)
data = open(os.path.join(SRC, "plan.json"), encoding="utf-8").read()
json.loads(data)  # validasi
tpl = open(os.path.join(SRC, "template.html"), encoding="utf-8").read()
assert "__DATA__" in tpl
out = tpl.replace("__DATA__", data.replace("</", "<\\/"))
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(out)
print(f"index.html dibuat ({len(out)/1024:.0f} KB)")
