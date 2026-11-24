#!/usr/bin/env python3
"""Checks world/dist: no em dashes, no figures that are disputed or retired, every local link and asset exists, every img has alt, ids unique."""
import re, sys, html
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "world" / "dist"
text = (D / "index.html").read_text(encoding="utf-8")
fails = []
if "—" in text or "–" in text:
    fails.append("em/en dash present")
for bad in ["98.03", "7.89", "7.81", "2,12,267", "466", "60+ years", "10+ countries", "88.0%", "stamps", "Shake", "waitlist", "49 "]:
    if bad in text:
        fails.append(f"retired or disputed string present: {bad!r}")
ids = re.findall(r'\sid="([^"]+)"', text)
dup = {i for i in ids if ids.count(i) > 1}
if dup:
    fails.append(f"duplicate ids: {sorted(dup)}")
for m in re.finditer(r"<img\b[^>]*>", text):
    if "alt=" not in m.group(0):
        fails.append("img without alt: " + m.group(0)[:80])
refs = set(re.findall(r'(?:src|href)="([^"#?][^"]*)"', text)) | set(re.findall(r"url\(([^)]+)\)", (D / "assets/css/world.css").read_text()))
for r in sorted(refs):
    r = html.unescape(r).strip("'\"")
    if r.startswith(("http", "mailto:", "data:")):
        continue
    if not (D / r.replace("../", "assets/")).exists() and not (D / "assets/css" / r).exists():
        fails.append("missing local file: " + r)
print("FAIL" if fails else "PASS", len(fails))
for f in fails:
    print(" -", f)
sys.exit(1 if fails else 0)
