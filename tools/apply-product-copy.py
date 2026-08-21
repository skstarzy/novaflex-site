#!/usr/bin/env python3
"""Rewrites the CONTENT map in product.html from the copy in content_a/content_b.

Why this is a script and not a hand edit: the map is a 20KB JS object literal
holding 25 entries, and the previous version was 94-99% duplicated between
entries. Regenerating it from a Python source of truth means the copy can be
revised without anyone hand-editing JavaScript string literals, and the
brace-matching that finds the block is the same logic build-seo.py already uses
to parse it.

Emits JSON-quoted strings so an apostrophe or an em-dash in the copy can't
terminate a literal early.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from product_copy_a import CONTENT_A
from product_copy_b import CONTENT_B

# The published site lives in docs/ so that GitHub Pages serves only what is
# meant to be public. Build tooling and drafts sit beside it in the repo and
# are never deployed - which is the bug this layout exists to prevent, after
# tools/ and _unpublished/ turned out to be readable at novaflexusa.com.
SITE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
CONTENT = {**CONTENT_A, **CONTENT_B}


def js_entry(slug, e):
    faqs = ",".join(
        "{q:%s,a:%s}" % (json.dumps(q, ensure_ascii=False), json.dumps(a, ensure_ascii=False))
        for q, a in e["faqs"]
    )
    benefits = ",".join(json.dumps(b, ensure_ascii=False) for b in e["benefits"])
    return "%s:{tagline:%s,overview:%s,analytical:%s,handling:%s,benefits:[%s],faqs:[%s]}" % (
        json.dumps(slug),
        json.dumps(e["tagline"], ensure_ascii=False),
        json.dumps(e["overview"], ensure_ascii=False),
        json.dumps(e["analytical"], ensure_ascii=False),
        json.dumps(e["handling"], ensure_ascii=False),
        benefits,
        faqs,
    )


def find_block(src):
    """The CONTENT object literal, located by brace matching rather than regex —
    the copy contains braces and a regex would stop at the first one."""
    start = src.index("const CONTENT = {")
    i = src.index("{", start)
    depth, j = 0, i
    while j < len(src):
        if src[j] == "{":
            depth += 1
        elif src[j] == "}":
            depth -= 1
            if depth == 0:
                return i, j + 1
        j += 1
    sys.exit("unterminated CONTENT literal")


def main():
    path = os.path.join(SITE, "product.html")
    src = open(path, encoding="utf-8").read()
    i, j = find_block(src)
    existing = re.findall(r'"([\w.+-]+)"\s*:\s*\{', src[i:j])

    missing = [s for s in existing if s not in CONTENT]
    extra = [s for s in CONTENT if s not in existing]
    if missing:
        sys.exit("no copy written for: %s" % ", ".join(missing))
    if extra:
        sys.exit("copy written for slugs not in the catalog: %s" % ", ".join(extra))

    # Preserve catalog order so a diff of the generated pages stays readable.
    body = ",\n  ".join(js_entry(s, CONTENT[s]) for s in existing)
    new = "{\n  " + body + "\n}"
    open(path, "w", encoding="utf-8").write(src[:i] + new + src[j:])

    words = lambda e: len(
        (e["tagline"] + " " + e["overview"] + " " + e["analytical"] + " " + e["handling"] + " "
         + " ".join(e["benefits"]) + " "
         + " ".join(q + " " + a for q, a in e["faqs"])).split()
    )
    counts = {s: words(CONTENT[s]) for s in existing}
    print("rewrote %d entries (%d -> %d bytes)" % (len(existing), j - i, len(new)))
    print("unique words per product: min %d, max %d, mean %d"
          % (min(counts.values()), max(counts.values()), sum(counts.values()) / len(counts)))
    thin = {s: n for s, n in counts.items() if n < 250}
    print("under 250 words:", thin or "none")


if __name__ == "__main__":
    main()
