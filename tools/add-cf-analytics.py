#!/usr/bin/env python3
"""Adds (or removes) the Cloudflare Web Analytics tag on every storefront page.

One line per page pointing at assets/cf-analytics.js, so the token lives in
exactly one file — activating analytics later is a one-string edit, not a
37-file sweep. Mirror of tools/add-meta-pixel.py.

    python3 tools/add-cf-analytics.py            # inject, idempotent
    python3 tools/add-cf-analytics.py --remove   # take it back out
    python3 tools/add-cf-analytics.py --check    # report only

Re-run after tools/build-seo.py, which regenerates the per-product pages from
product.html and could drop the tag from generated output.
"""
import argparse, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARKER = "assets/cf-analytics.js"
TAG = '<script src="assets/cf-analytics.js" defer></script>'
LINE = f"\n<!-- Cloudflare Web Analytics — token lives in assets/cf-analytics.js -->\n{TAG}\n"

ap = argparse.ArgumentParser()
ap.add_argument("--remove", action="store_true")
ap.add_argument("--check", action="store_true")
args = ap.parse_args()

pages = sorted(p for p in ROOT.glob("*.html"))
if not pages:
    sys.exit(f"no .html files found in {ROOT}")

changed, already, missing_head = [], [], []
for page in pages:
    html = page.read_text(encoding="utf-8")
    has = MARKER in html
    if args.check:
        (already if has else changed).append(page.name); continue
    if args.remove:
        if not has: continue
        cleaned = re.sub(
            r"\n*<!-- Cloudflare Web Analytics[^>]*-->\n*<script src=\"assets/cf-analytics\.js\"[^>]*>\s*</script>\n*",
            "\n", html)
        if cleaned == html:
            cleaned = re.sub(r"\n*<script src=\"assets/cf-analytics\.js\"[^>]*>\s*</script>\n*", "\n", html)
        page.write_text(cleaned, encoding="utf-8"); changed.append(page.name); continue
    if has:
        already.append(page.name); continue
    if "</head>" not in html:
        missing_head.append(page.name); continue
    hc = html.rfind("</head>")
    page.write_text(html[:hc] + LINE + html[hc:], encoding="utf-8")
    changed.append(page.name)

verb = "would tag" if args.check else ("removed from" if args.remove else "tagged")
print(f"{verb}: {len(changed)} page(s)")
if already: print(f"already done: {len(already)} page(s)")
if missing_head: print(f"SKIPPED (no </head>): {', '.join(missing_head)}")
