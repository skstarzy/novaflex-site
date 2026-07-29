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

It ALSO writes the static catalog grid into index.html. That second job is the
important one. Generating 25 crawlable product pages achieved nothing while
nothing linked to them: the homepage built its whole catalog client-side, so in
the served HTML there were no product anchors and no compound names at all, and
sitemap.xml was Google's only route in. Pages reachable only from a sitemap,
with no internal links, are the standard profile for "Crawled — currently not
indexed". The grid markup below is a server-rendered copy of what productCard()
in index.html emits for a signed-out visitor; the page's own JS overwrites it
with identical markup on load, so this is a pre-render, not cloaking.

Run from the repo root after any catalog change:
    python3 tools/build-seo.py

IMPORTANT — the pre-rendered body must stay in sync with what product.html's
JS renders. Both read the same PRODUCTS/CONTENT source of truth below, so they
agree by construction. Don't hand-edit the generated files; regenerate them.

index.html keeps its own copy of PRODUCTS (it needs `badge` and `cats`, which
product.html has no use for). check_catalog_drift() compares the two on the
fields that must agree — a price or spec that differs between them is the kind
of bug that only shows up as a failed checkout, so it fails the build loudly
rather than shipping quietly.

Deliberately NOT emitted:
  • The real names of the three renamed compounds. Retatrutide, Tirzepatide and
    BPC-157 display as GL-3RT, NV-2TZ and BP+ on purpose; this script uses the
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
    ("/glp1-gip-glucagon-receptor-agonists.html", "0.7", "monthly"),
    ("/hplc-vs-mass-spectrometry.html", "0.7", "monthly"),
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
        # Booleans matter now that availability is published in the Offer — a
        # sold-out vial marked InStock is a worse error than no markup at all.
        for k, v in re.findall(r"(\w+)\s*:\s*(true|false)\s*(?:,|$)", r):
            d.setdefault(k, v == "true")
        if "slug" in d:
            out.append(d)
    return out


def parse_index_products(src):
    """index.html's PRODUCTS array. Its own parser rather than the one above
    because index carries two fields product.html doesn't — `badge` and the
    boolean `soldOut` — and both change what a card renders."""
    m = re.search(r"const PRODUCTS = \[(.*?)\n\];", src, re.S)
    if not m:
        sys.exit("could not find PRODUCTS in index.html")
    out = []
    for row in re.findall(r"\{([^}]*)\}", m.group(1)):
        d = dict(re.findall(r'(\w+)\s*:\s*"([^"]*)"', row))
        for k, v in re.findall(r"(\w+)\s*:\s*(\d+(?:\.\d+)?)\s*(?:,|$)", row):
            d.setdefault(k, v)
        d["soldOut"] = bool(re.search(r"soldOut\s*:\s*true", row))
        if "slug" in d:
            out.append(d)
    return out


def parse_cat_labels(src):
    m = re.search(r"const CAT_LABELS = \{(.*?)\n\};", src, re.S)
    return dict(re.findall(r'"([\w-]+)"\s*:\s*"([^"]*)"', m.group(1))) if m else {}


def parse_featured_names(src):
    m = re.search(r"const FEATURED_NAMES = \[(.*?)\];", src, re.S)
    return re.findall(r'"([^"]*)"', m.group(1)) if m else []


def check_catalog_drift(index_products, product_products):
    """index.html and product.html each hold a copy of the catalog. They may
    legitimately differ in key order, row order and the index-only fields, but a
    disagreement on price, spec, display name or sold-out state is a real bug:
    checkout resolves a cart line by exact name + spec, so a drifted spec fails
    the whole order, not just that line."""
    by_slug = {p["slug"]: p for p in product_products}
    problems = []
    for p in index_products:
        q = by_slug.get(p["slug"])
        if not q:
            problems.append("%s is in index.html but not product.html" % p["slug"])
            continue
        for field in ("name", "display", "spec", "price", "purity"):
            a, b = p.get(field), q.get(field)
            if (a or "") != (b or ""):
                problems.append(
                    "%s.%s disagrees: index=%r product=%r" % (p["slug"], field, a, b)
                )
    for slug in set(by_slug) - {p["slug"] for p in index_products}:
        problems.append("%s is in product.html but not index.html" % slug)
    return problems


def static_card(p, cat_labels):
    """Server-rendered twin of productCard() in index.html, in its signed-out
    state — which is what a crawler and a first-time visitor both see. Prices
    stay behind the gate here exactly as they do in the JS version, so the
    pre-render can't leak pricing the live page wouldn't show."""
    label = p.get("display") or p["name"]
    slug = p["slug"]
    href = "%s.html" % slug
    sold = p.get("soldOut")

    badge = '<span class="badge soldout">Sold Out</span>' if sold else ""
    purity = '<span class="purity-tag">%s</span>' % escape(p["purity"]) if p.get("purity") else ""
    btn = (
        '<button class="add-btn soldout" disabled aria-disabled="true">Sold Out</button>'
        if sold
        else '<button class="add-btn" onclick="openAuthModal()">Sign in</button>'
    )
    price = '<span class="prod-price locked" onclick="openAuthModal()">Sign in for price</span>'
    alt = "%s %s — NovaFlex Peptides" % (label, p.get("spec", ""))

    return (
        '<div class="prod-card%s" data-cat="%s" data-slug="%s">'
        '<div class="prod-media">%s'
        '<a href="%s" class="prod-media-link" aria-label="View %s details">'
        '<img class="vial-photo" src="assets/vials/NF-%s.webp?v=3" alt="%s" loading="lazy"></a>'
        "%s</div>"
        '<div class="prod-body">'
        '<span class="prod-cat">%s</span>'
        '<a class="prod-name" href="%s">%s</a>'
        '<span class="prod-spec">%s</span>'
        '<div class="prod-foot">%s%s</div>'
        "</div></div>"
    ) % (
        " is-soldout" if sold else "",
        escape(p.get("cat", "")),
        escape(slug),
        badge,
        href,
        escape(label),
        escape(slug),
        escape(alt),
        purity,
        escape(cat_labels.get(p.get("cat", ""), p.get("cat", ""))),
        href,
        escape(label),
        escape(p.get("spec", "")),
        price,
        btn,
    )


MARK_START = "<!--build-seo:grid-->"
MARK_END = "<!--/build-seo:grid-->"


def inject_grid(src, grid_id, html):
    """Write the pre-rendered cards inside a named grid container, replacing any
    block a previous run left there. Idempotent by construction — the markers
    delimit exactly what this script owns, so re-running never nests or
    duplicates, and hand-written markup outside them is left alone."""
    open_tag = '<div class="prod-grid" id="%s">' % grid_id
    i = src.find(open_tag)
    if i < 0:
        sys.exit("could not find #%s in index.html" % grid_id)
    j = i + len(open_tag)
    if src.startswith(MARK_START, j):
        k = src.index(MARK_END, j) + len(MARK_END)
    else:
        k = j
    if not src.startswith("</div>", k):
        sys.exit("unexpected markup inside #%s — refusing to overwrite" % grid_id)
    return src[:j] + MARK_START + html + MARK_END + src[k:]


def build_index(index_path, product_products):
    src = open(index_path, encoding="utf-8").read()
    products = parse_index_products(src)
    cat_labels = parse_cat_labels(src)
    featured_names = parse_featured_names(src)

    problems = check_catalog_drift(products, product_products)
    if problems:
        sys.exit(
            "catalog drift between index.html and product.html:\n  "
            + "\n  ".join(problems)
        )

    # Mirrors renderFeatured(): match on name or "name spec", cap at 8.
    featured = [
        p
        for p in products
        if any(
            n in ("%s %s" % (p["name"], p.get("spec", ""))) or p["name"] == n
            for n in featured_names
        )
    ][:8]

    # Mirrors renderCatalog("All","az") — the default view on page load.
    catalog = sorted(products, key=lambda p: (p.get("display") or p["name"]).lower())

    src = inject_grid(src, "featuredGrid", "".join(static_card(p, cat_labels) for p in featured))
    src = inject_grid(src, "catalogGrid", "".join(static_card(p, cat_labels) for p in catalog))
    open(index_path, "w", encoding="utf-8").write(src)
    return len(featured), len(catalog)


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
        for field in ("analytical", "handling"):
            m2 = re.search(r'%s\s*:\s*"((?:[^"\\]|\\.)*)"' % field, block)
            entry[field] = m2.group(1) if m2 else ""
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
    # "COA Verified" used to sit here too, which pushed most of these past the
    # ~60 characters a result actually displays and got the brand truncated. The
    # purity figure is the differentiator worth the space; COA is covered in the
    # description and on the page.
    if purity:
        return "%s — %s Purity | %s" % (head, purity, BRAND)
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
    # Offers were withheld here originally, on the reasoning that pricing sits
    # behind the researcher sign-in gate and publishing it would defeat the gate.
    # That reasoning no longer holds: index.html emits an ItemList with a full
    # Offer — price, currency and availability — for all 25 products, so every
    # price is already published to search. Withholding it only on the product
    # pages cost the rich result without protecting anything. One source, one
    # answer: emit it here too.
    if p.get("price"):
        data["offers"] = {
            "@type": "Offer",
            "price": "%.2f" % float(p["price"]),
            "priceCurrency": "USD",
            "availability": "https://schema.org/OutOfStock"
            if p.get("soldOut")
            else "https://schema.org/InStock",
            "url": url,
            "seller": {"@type": "Organization", "name": BRAND},
        }
    return data


def breadcrumb_jsonld(p, url, cat_labels):
    """Breadcrumbs give the result a readable path instead of a bare URL, and
    they tell Google the catalog has a shape — which matters more than usual
    here, where every product sits one hop from the homepage and nothing else."""
    label = p.get("display") or p["name"]
    if "·" in label:
        label = p["name"]
    cat = cat_labels.get(p.get("cat", ""), "Catalog")
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "NovaFlex Peptides", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": cat, "item": SITE + "/#catalog"},
            {"@type": "ListItem", "position": 3, "name": label, "item": url},
        ],
    }


def related_for(p, products, n=4):
    """Nearest neighbours by research focus, falling back to the wider catalog
    so even a thin category gets a full row.

    The neighbours are the n entries FOLLOWING this one in its category, wrapping
    around, rather than the first n. Taking the first n every time means the
    alphabetically-early slugs collect all the links and the late ones receive
    none — which is how a fix for orphan pages quietly leaves orphan pages. A
    cyclic window makes every product appear as a neighbour exactly as often as
    it has neighbours itself. Ordering is by slug, so it's stable across builds;
    links that reshuffle on every deploy read as churn to a crawler."""
    same = sorted(
        (q for q in products
         if q["slug"] != p["slug"]
         and (q.get("cat") == p.get("cat") or p.get("cat") in (q.get("cats") or ""))),
        key=lambda q: q["slug"],
    )
    ring = sorted(products, key=lambda q: q["slug"])
    idx = [q["slug"] for q in ring].index(p["slug"])

    if len(same) >= n:
        cat_ring = sorted(
            (q for q in products if q.get("cat") == p.get("cat")), key=lambda q: q["slug"]
        )
        i = [q["slug"] for q in cat_ring].index(p["slug"])
        return [cat_ring[(i + k) % len(cat_ring)] for k in range(1, n + 1)]

    # Thin category: take everything in it, then continue around the full
    # catalog from this product's position so the overflow spreads too.
    picks = list(same)
    k = 1
    while len(picks) < n and k < len(ring):
        cand = ring[(idx + k) % len(ring)]
        if cand["slug"] != p["slug"] and cand not in picks:
            picks.append(cand)
        k += 1
    return picks[:n]


def related_html(p, products, cat_labels):
    picks = related_for(p, products)
    if not picks:
        return ""
    cards = []
    for q in picks:
        label = q.get("display") or q["name"]
        if "·" in label:
            label = q["name"]
        cards.append(
            '<a class="pd-related-card" href="%s.html">'
            '<img src="assets/vials/NF-%s.webp?v=3" alt="" loading="lazy" aria-hidden="true">'
            '<span><span class="n">%s</span><span class="s">%s</span></span></a>'
            % (escape(q["slug"]), escape(q["slug"]), escape(label), escape(q.get("spec", "")))
        )
    heading = cat_labels.get(p.get("cat", ""), "the catalog")
    return (
        "<h2>More in %s</h2><div class=\"pd-related-grid\">%s</div>"
        % (escape(heading), "".join(cards))
    )


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
    if c.get("analytical"):
        parts.append(
            '<section class="pd-section"><h2>What the testing shows</h2><p>%s</p></section>'
            % escape(c["analytical"])
        )
    if c.get("benefits"):
        lis = "".join("<li>%s</li>" % escape(b) for b in c["benefits"])
        parts.append(
            '<section class="pd-section"><h2>Specifications</h2><ul>%s</ul></section>' % lis
        )
    if c.get("handling"):
        parts.append(
            '<section class="pd-section"><h2>Storage &amp; reconstitution</h2><p>%s</p></section>'
            % escape(c["handling"])
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

    index_path = os.path.join(ROOT, "index.html")
    cat_labels = parse_cat_labels(open(index_path, encoding="utf-8").read())

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
        head.append(
            '<script type="application/ld+json">%s</script>'
            % json.dumps(breadcrumb_jsonld(p, url, cat_labels), ensure_ascii=False)
        )
        head.append("<script>window.__SLUG__=%s;</script>" % json.dumps(slug))

        page = src
        # Replace the generic head tags with the product-specific ones.
        page = page.replace("<title>NovaFlex Peptides</title>", "\n".join(head), 1)
        # The template carries noindex so it can't rank as a duplicate of
        # whichever product it happens to load. The generated pages are the ones
        # meant to be found, so they get the indexable directive back.
        before = page
        page = page.replace(
            '<meta name="robots" content="noindex, follow"><!--build-seo:robots-->',
            '<meta name="robots" content="index, follow, noai, noimageai">',
            1,
        )
        if page == before:
            sys.exit(
                "product.html is missing the build-seo:robots marker — generated "
                "pages would inherit noindex and drop out of the index"
            )
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
        # Related compounds, outside #pdContent so the page's JS can't wipe them.
        rel_before = page
        page = page.replace(
            '<nav id="pdRelated" class="pd-related" aria-label="Related compounds"></nav>',
            '<nav id="pdRelated" class="pd-related" aria-label="Related compounds">%s</nav>'
            % related_html(p, products, cat_labels),
            1,
        )
        if page == rel_before:
            sys.exit("product.html is missing the #pdRelated container")

        out = os.path.join(ROOT, "%s.html" % slug)
        open(out, "w", encoding="utf-8").write(page)
        written.append((url, slug))

    # sitemap
    urls = []
    for path, prio, freq in STATIC_PAGES:
        urls.append((SITE + path if path != "/" else SITE + "/", prio, freq))
    for url, _slug in written:
        urls.append((url, "0.8", "weekly"))

    # <lastmod> from the file's own mtime rather than "today": stamping every
    # URL with the run date on every build teaches crawlers the dates mean
    # nothing, which is worse than omitting them.
    def lastmod_for(url):
        path = url.replace(SITE, "").lstrip("/") or "index.html"
        full = os.path.join(ROOT, path)
        if not os.path.exists(full):
            return None
        return __import__("datetime").date.fromtimestamp(os.path.getmtime(full)).isoformat()

    sm = ['<?xml version="1.0" encoding="UTF-8"?>']
    sm.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url, prio, freq in urls:
        sm.append("  <url>")
        sm.append("    <loc>%s</loc>" % url)
        lm = lastmod_for(url)
        if lm:
            sm.append("    <lastmod>%s</lastmod>" % lm)
        sm.append("    <changefreq>%s</changefreq>" % freq)
        sm.append("    <priority>%s</priority>" % prio)
        sm.append("  </url>")
    sm.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm) + "\n")

    # Last, because it needs the product pages to exist before it links to them.
    n_feat, n_cat = build_index(os.path.join(ROOT, "index.html"), products)

    print("generated %d product pages" % len(written))
    print("sitemap.xml now lists %d URLs" % len(urls))
    print("index.html: pre-rendered %d featured + %d catalog cards" % (n_feat, n_cat))


if __name__ == "__main__":
    main()
