#!/usr/bin/env python3
"""
Generates the crawlable surface of the storefront.

Why this exists: every compound used to live at product.html?slug=<x>, which
served ONE static <title> ("NovaFlex Peptides") and one boilerplate meta
description for all 25 products, with the real per-product values written by
JavaScript after load. Google will eventually render that, but until it does
the whole catalog looks like duplicates of a single page — which is about the
most reliable way there is to not rank.

This script emits one real HTML file per product with a served title, meta
description, canonical, Open Graph tags, Product + FAQPage JSON-LD, and a
pre-rendered copy of the page body, then rebuilds sitemap.xml.

Run from the repo root after any catalog change:
    python3 tools/build-seo.py

IMPORTANT — the pre-rendered body must stay in sync with what product.html's
JS renders. Both read the same PRODUCTS/CONTENT source of truth below, so they
agree by construction. Don't hand-edit the generated files; regenerate them.

Deliberately NOT emitted:
  • offers/price in the Product schema. Pricing sits behind the researcher
    sign-in gate; publishing it to Google would defeat that gate. Costs us the
    merchant rich result — a conscious trade, not an oversight.
  • The real names of the three renamed compounds. Retatrutide, Tirzepatide and
    BPC-157 display as NV-3RT, NV-2TZ and BP+ on purpose; this script uses the
    display name so it can't quietly undo that decision.
"""

import json
import os
import re
import sys
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://novaflexusa.com"
BRAND = "NovaFlex Peptides"

# Pages that aren't products but belong in the sitemap.
STATIC_PAGES = [
    ("/", "1.0", "weekly"),
    ("/policies.html", "0.3", "yearly"),
    ("/team.html", "0.4", "monthly"),
    # Linkable asset: free tools are what earn backlinks, which is the thing
    # this domain most lacks. Higher priority than the policy pages.
    ("/reconstitution-calculator.html", "0.7", "monthly"),
    ("/how-to-read-a-coa.html", "0.7", "monthly"),
]


def parse_js_object_list(src, varname):
    """Pull PRODUCTS out of product.html. Kept deliberately simple — the array
    is machine-written and flat, so a real JS parser would be overkill."""
    m = re.search(r"const %s = \[(.*?)\n\];" % varname, src, re.S)
    if not m:
        sys.exit("could not find %s in product.html" % varname)
    rows = re.findall(r"\{([^}]*)\}", m.group(1))
    out = []
    for r in rows:
        d = dict(re.findall(r'(\w+)\s*:\s*"([^"]*)"', r))
        for k, v in re.findall(r"(\w+)\s*:\s*([\d.]+)\s*(?:,|$)", r):
            d.setdefault(k, v)
        if "slug" in d:
            out.append(d)
    return out


def parse_content_map(src):
    """CONTENT is one big object literal of {slug: {...}}. Extract each slug's
    block by brace matching so nested arrays/objects survive."""
    start = src.index("const CONTENT = {")
    i = src.index("{", start)
    depth, j = 0, i
    while j < len(src):
        if src[j] == "{":
            depth += 1
        elif src[j] == "}":
            depth -= 1
            if depth == 0:
                break
        j += 1
    body = src[i + 1 : j]

    out = {}
    for m in re.finditer(r'"([\w.+-]+)"\s*:\s*\{', body):
        slug = m.group(1)
        k = m.end() - 1
        d, e = 0, k
        while e < len(body):
            if body[e] == "{":
                d += 1
            elif body[e] == "}":
                d -= 1
                if d == 0:
                    break
            e += 1
        block = body[k : e + 1]
        entry = {}
        t = re.search(r'tagline\s*:\s*"((?:[^"\\]|\\.)*)"', block)
        o = re.search(r'overview\s*:\s*"((?:[^"\\]|\\.)*)"', block)
        entry["tagline"] = t.group(1) if t else ""
        entry["overview"] = o.group(1) if o else ""
        b = re.search(r"benefits\s*:\s*\[(.*?)\]", block, re.S)
        entry["benefits"] = re.findall(r'"((?:[^"\\]|\\.)*)"', b.group(1)) if b else []
        f = re.search(r"faqs\s*:\s*\[(.*?)\]\s*\}", block, re.S)
        entry["faqs"] = []
        if f:
            for q, a in re.findall(
                r'q\s*:\s*"((?:[^"\\]|\\.)*)"\s*,\s*a\s*:\s*"((?:[^"\\]|\\.)*)"', f.group(1)
            ):
                entry["faqs"].append({"q": q, "a": a})
        out[slug] = entry
    return out


def title_for(p):
    """Mirrors the shape that actually ranks for these queries: compound, size,
    the specific purity figure, and COA — e.g. 'Buy Retatrutide RUO 10mg |
    99.914% Purity'. The purity number is the differentiator competitors lead
    with, so it goes in the title rather than being buried in the body."""
    label = p.get("display") or p["name"]
    # Blends list their components in `display`; that's too long for a title.
    if "·" in label:
        label = p["name"]
    size = p.get("spec", "").replace(" vial", "")
    bits = [label]
    if size:
        bits.append(size)
    head = " ".join(bits)
    purity = p.get("purity")
    if purity:
        return "%s — %s Purity, COA Verified | %s" % (head, purity, BRAND)
    return "%s — Lab Supply | %s" % (head, BRAND)


def description_for(p, c):
    label = p.get("display") or p["name"]
    if "·" in label:
        label = p["name"]
    purity = p.get("purity")
    if purity:
        lead = "%s %s — %s HPLC + mass-spec verified purity, batch Certificate of Analysis on file." % (
            label,
            p.get("spec", ""),
            purity,
        )
    else:
        lead = "%s %s — laboratory supply, batch documented." % (label, p.get("spec", ""))
    tail = " For research use only. Ships from the USA."
    full = lead + tail
    if len(full) <= 158:
        return full
    # Trim on a word boundary — Google truncates with an ellipsis anyway, but a
    # description that ends mid-word looks broken in the snippet.
    return full[:158].rsplit(" ", 1)[0].rstrip(",;—-") + "…"


def product_jsonld(p, c, url):
    label = p.get("display") or p["name"]
    if "·" in label:
        label = p["name"]
    data = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": ("%s %s" % (label, p.get("spec", ""))).strip(),
        "sku": p["slug"],
        "url": url,
        "image": "%s/assets/vials/NF-%s.webp" % (SITE, p["slug"]),
        "description": c.get("overview", ""),
        "brand": {"@type": "Brand", "name": BRAND},
        "category": "Laboratory research compound",
    }
    if p.get("purity"):
        data["additionalProperty"] = [
            {
                "@type": "PropertyValue",
                "name": "Verified purity (HPLC + MS)",
                "value": p["purity"],
            }
        ]
    return data


def faq_jsonld(c):
    if not c.get("faqs"):
        return None
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f["q"],
                "acceptedAnswer": {"@type": "Answer", "text": f["a"]},
            }
            for f in c["faqs"]
        ],
    }


def prerendered_body(p, c):
    """A static copy of what the page's JS renders. Crawlers get real content
    on the first pass instead of an empty <div>; the JS overwrites it with the
    same content once it runs, so this is not cloaking."""
    label = p.get("display") or p["name"]
    if "·" in label:
        label = p["name"]
    parts = [
        '<div class="pd-hero"><div class="pd-info">',
        "<h1 class=\"pd-name\">%s</h1>" % escape(label),
        '<div class="pd-sub"><span>%s</span>' % escape(p.get("spec", "")),
    ]
    if p.get("purity"):
        parts.append('<span class="dot">•</span><span>%s purity</span>' % escape(p["purity"]))
    parts.append("</div>")
    if c.get("tagline"):
        parts.append('<p class="pd-tagline">%s</p>' % escape(c["tagline"]))
    parts.append("</div></div>")
    if c.get("overview"):
        parts.append(
            '<section class="pd-section"><h2>What it is</h2><p>%s</p></section>'
            % escape(c["overview"])
        )
    if c.get("benefits"):
        lis = "".join("<li>%s</li>" % escape(b) for b in c["benefits"])
        parts.append(
            '<section class="pd-section"><h2>Specifications</h2><ul>%s</ul></section>' % lis
        )
    if c.get("faqs"):
        qs = "".join(
            "<h3>%s</h3><p>%s</p>" % (escape(f["q"]), escape(f["a"])) for f in c["faqs"]
        )
        parts.append('<section class="pd-section"><h2>Questions</h2>%s</section>' % qs)
    return "".join(parts)


def main():
    src_path = os.path.join(ROOT, "product.html")
    src = open(src_path, encoding="utf-8").read()
    products = parse_js_object_list(src, "PRODUCTS")
    content = parse_content_map(src)

    written = []
    for p in products:
        slug = p["slug"]
        c = content.get(slug, {})
        url = "%s/%s.html" % (SITE, slug)

        head = []
        head.append("<title>%s</title>" % escape(title_for(p)))
        head.append(
            '<meta name="description" content="%s">' % escape(description_for(p, c))
        )
        head.append('<link rel="canonical" href="%s">' % url)
        head.append('<meta property="og:type" content="product">')
        head.append('<meta property="og:title" content="%s">' % escape(title_for(p)))
        head.append(
            '<meta property="og:description" content="%s">' % escape(description_for(p, c))
        )
        head.append('<meta property="og:url" content="%s">' % url)
        head.append(
            '<meta property="og:image" content="%s/assets/vials/NF-%s.webp">' % (SITE, slug)
        )
        head.append('<meta name="twitter:card" content="summary_large_image">')
        head.append(
            '<script type="application/ld+json">%s</script>'
            % json.dumps(product_jsonld(p, c, url), ensure_ascii=False)
        )
        faq = faq_jsonld(c)
        if faq:
            head.append(
                '<script type="application/ld+json">%s</script>'
                % json.dumps(faq, ensure_ascii=False)
            )
        head.append("<script>window.__SLUG__=%s;</script>" % json.dumps(slug))

        page = src
        # Replace the generic head tags with the product-specific ones.
        page = page.replace("<title>NovaFlex Peptides</title>", "\n".join(head), 1)
        page = re.sub(
            r'<meta name="description" content="Research-grade peptide details[^"]*">',
            "",
            page,
            count=1,
        )
        # Seed the container the JS later fills, so there's content without JS.
        page = page.replace(
            '<div id="pdContent"></div>',
            '<div id="pdContent">%s</div>' % prerendered_body(p, c),
            1,
        )

        out = os.path.join(ROOT, "%s.html" % slug)
        open(out, "w", encoding="utf-8").write(page)
        written.append((url, slug))

    # sitemap
    urls = []
    for path, prio, freq in STATIC_PAGES:
        urls.append((SITE + path if path != "/" else SITE + "/", prio, freq))
    for url, _slug in written:
        urls.append((url, "0.8", "weekly"))

    sm = ['<?xml version="1.0" encoding="UTF-8"?>']
    sm.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url, prio, freq in urls:
        sm.append("  <url>")
        sm.append("    <loc>%s</loc>" % url)
        sm.append("    <changefreq>%s</changefreq>" % freq)
        sm.append("    <priority>%s</priority>" % prio)
        sm.append("  </url>")
    sm.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm) + "\n")

    print("generated %d product pages" % len(written))
    print("sitemap.xml now lists %d URLs" % len(urls))


if __name__ == "__main__":
    main()
