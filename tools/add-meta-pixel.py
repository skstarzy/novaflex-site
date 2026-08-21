#!/usr/bin/env python3
"""Adds (or removes) the Meta pixel tag on every page of the storefront.

The tag is one line pointing at assets/meta-pixel.js, so the pixel ID lives in
exactly one file. That is the whole point: activating tracking later is a
one-string edit, not a 37-file sweep.

    python3 tools/add-meta-pixel.py            # inject, idempotent
    python3 tools/add-meta-pixel.py --remove   # take it back out
    python3 tools/add-meta-pixel.py --check    # report only, change nothing

Re-run after tools/build-seo.py — that script regenerates the per-product pages
from product.html, so a rebuild can drop the tag from generated output. Running
this again is safe and costs nothing when everything is already tagged.
"""
import argparse
import pathlib
import re
import sys

# The published site lives in docs/ so that GitHub Pages serves only what is
# meant to be public. Build tooling and drafts sit beside it in the repo and
# are never deployed - which is the bug this layout exists to prevent, after
# tools/ and _unpublished/ turned out to be readable at novaflexusa.com.
ROOT = pathlib.Path(__file__).resolve().parent.parent / "docs"
MARKER = "assets/meta-pixel.js"
TAG = '<script src="assets/meta-pixel.js" defer></script>'
LINE = f"\n<!-- Meta pixel — ID lives in assets/meta-pixel.js -->\n{TAG}\n"

parser = argparse.ArgumentParser()
parser.add_argument("--remove", action="store_true")
parser.add_argument("--check", action="store_true")
args = parser.parse_args()

pages = sorted(p for p in ROOT.glob("*.html"))
if not pages:
    sys.exit(f"no .html files found in {ROOT}")

changed, already, missing_head = [], [], []

for page in pages:
    html = page.read_text(encoding="utf-8")
    has_tag = MARKER in html

    if args.check:
        (already if has_tag else changed).append(page.name)
        continue

    if args.remove:
        if not has_tag:
            continue
        # drop the tag plus the comment line and surrounding blank lines
        cleaned = re.sub(
            r"\n*<!-- Meta pixel[^>]*-->\n*<script src=\"assets/meta-pixel\.js\"[^>]*>\s*</script>\n*",
            "\n",
            html,
        )
        if cleaned == html:  # tag present but not in the expected shape
            cleaned = re.sub(
                r"\n*<script src=\"assets/meta-pixel\.js\"[^>]*>\s*</script>\n*", "\n", html
            )
        page.write_text(cleaned, encoding="utf-8")
        changed.append(page.name)
        continue

    if has_tag:
        already.append(page.name)
        continue

    if "</head>" not in html:
        missing_head.append(page.name)
        continue

    # last </head> guards against one appearing inside a JS string earlier on
    head_close = html.rfind("</head>")
    page.write_text(html[:head_close] + LINE + html[head_close:], encoding="utf-8")
    changed.append(page.name)

verb = "would tag" if args.check else ("removed from" if args.remove else "tagged")
print(f"{verb}: {len(changed)} page(s)")
if already:
    print(f"already {'tagged' if not args.check else 'done'}: {len(already)} page(s)")
if missing_head:
    print(f"SKIPPED (no </head>): {', '.join(missing_head)}")
