#!/usr/bin/env python3
"""Check distros.json: well-formed, honest fields, and every download link still alive.
Run by GitHub on every pull request and once a week; also runnable by hand: python3 check.py"""
import json, sys, urllib.request

REQUIRED = {"name": str, "group": str, "size": str, "live": bool, "install": bool, "status": str, "url": str}
errors = []
try:
    data = json.load(open("distros.json", encoding="utf-8"))
    distros = data["distros"]
except Exception as exc:
    sys.exit(f"distros.json is not valid: {exc}")

names = set()
for i, d in enumerate(distros):
    label = d.get("name", f"entry {i + 1}")
    for key, kind in REQUIRED.items():
        if not isinstance(d.get(key), kind):
            errors.append(f"{label}: '{key}' is missing or not a {kind.__name__}")
    for key in ("name", "group", "status", "size"):
        if "," in str(d.get(key, "")):
            errors.append(f"{label}: '{key}' must not contain a comma (No-Stick's list splits rows on commas)")
    extra = set(d) - set(REQUIRED)
    if extra:
        errors.append(f"{label}: unknown field(s) {sorted(extra)}")
    if label in names:
        errors.append(f"{label}: listed twice")
    names.add(label)
    url = str(d.get("url", ""))
    if not url.startswith("https://"):
        errors.append(f"{label}: the link must start with https://")
        continue
    if not url.endswith(".iso"):
        errors.append(f"{label}: the link must point straight at an .iso file, so No-Stick can download it")
        continue
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "nostick-distros-check"})
        with urllib.request.urlopen(req, timeout=60) as r:
            size = int(r.headers.get("Content-Length") or 0)
        if size < 300 * 1024 * 1024:
            errors.append(f"{label}: the link answers, but with only {size} bytes - not an ISO")
        else:
            print(f"ok   {label}  ({size / 1073741824:.1f}G)")
    except Exception as exc:
        errors.append(f"{label}: link is not reachable ({exc})  {url}")

if errors:
    print("\nProblems:")
    for e in errors:
        print("  - " + e)
    sys.exit(1)
print(f"\nAll {len(distros)} entries are fine.")
