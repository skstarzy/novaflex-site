#!/usr/bin/env python3
"""Build blog.html — the guides hub the site never had.

To add a guide: drop its page in the repo, add a tuple to SECTIONS below,
rerun this, then rerun tools/build-seo.py so the sitemap and llms.txt follow.

The four reference pages already existed but only two of them were reachable:
`hplc-vs-mass-spectrometry` and `glp1-gip-glucagon-receptor-agonists` each had a
single inbound link, both from the COA guide. That is the same orphan profile
that kept the 25 product pages out of the index — discoverable in the sitemap,
effectively invisible in the link graph.

The page is spliced out of an existing article rather than written fresh, so it
inherits the real stylesheet, header and footer instead of an approximation of
them. Only the <main> is new, plus a small block of grid CSS.
"""

import os, re

# Repo-relative so this keeps working if the checkout moves.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DONOR = os.path.join(ROOT, "hplc-vs-mass-spectrometry.html")
OUT = os.path.join(ROOT, "blog.html")
SITE = "https://novaflexusa.com"

TITLE = "Guides &amp; Reference | NovaFlex Peptides"
TITLE_PLAIN = "Guides & Reference | NovaFlex Peptides"
DESC = ("Plain-English guides for sourcing research peptides: how to read a Certificate of "
        "Analysis, what HPLC and mass spec each prove, and a reconstitution calculator.")

# Grouped because the grouping is true, not decorative: two pieces teach you to
# audit a supplier's paperwork, one explains how a class of compounds is
# distinguished in the literature, one is a calculator.
SECTIONS = [
    ("Verifying what you receive",
     "The two documents any supplier should be able to hand you, and how to tell a real one from a decorative one.",
     [
        ("how-to-read-a-coa.html",
         "How to read a peptide Certificate of Analysis",
         "What the purity figure actually measures, why identity is a separate question, and how to spot a certificate that was designed rather than produced.",
         "Guide"),
        ("hplc-vs-mass-spectrometry.html",
         "HPLC vs mass spectrometry: what each test proves",
         "One measures how pure the material is, the other confirms what it is. A sample can be 99% pure and still be the wrong molecule.",
         "Guide"),
     ]),
    ("Compound reference",
     "How compounds are grouped and distinguished in the published literature — mechanism, not outcomes.",
     [
        ("glp1-gip-glucagon-receptor-agonists.html",
         "GLP-1, GIP and glucagon receptor agonists explained",
         "Why single, dual and triple receptor agonists are treated as distinct classes, and what the receptor targets actually refer to.",
         "Reference"),
     ]),
    ("Tools",
     "Free, no account required.",
     [
        ("reconstitution-calculator.html",
         "Peptide reconstitution calculator",
         "Enter vial mass and diluent volume for working concentration in mg/mL, plus the aliquot volume for any target mass.",
         "Calculator"),
     ]),
]

EXTRA_CSS = """
  /* Guides hub */
  .hub-wrap{max-width:920px;margin:0 auto;padding:0 24px;}
  .hub-head{padding:44px 0 4px;max-width:760px;}
  .hub-head h1{font-size:clamp(28px,4.4vw,40px);color:var(--silver-bright);line-height:1.12;letter-spacing:-.022em;}
  .hub-head .lede{margin-top:16px;font-size:17px;line-height:1.7;color:var(--text-muted);}
  .hub-sec{margin-top:40px;}
  .hub-sec > h2{font-size:19px;color:var(--silver-bright);letter-spacing:-.01em;}
  .hub-sec > .sec-note{margin-top:7px;font-size:14.5px;line-height:1.6;color:var(--text-muted);max-width:640px;}
  .hub-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;margin-top:18px;}
  /* auto-fill, not auto-fit: a section holding one card should keep the same
     card width as the two-up sections rather than stretching across the row. */
  .hub-card{display:block;border:1px solid var(--line);border-radius:12px;padding:22px 24px;
    background:var(--bg-alt);transition:border-color .2s ease,transform .2s ease,box-shadow .2s ease;}
  .hub-card:hover{border-color:var(--line-strong);transform:translateY(-2px);
    box-shadow:0 12px 28px rgba(60,48,20,.07);}
  .hub-card .tag{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.14em;
    text-transform:uppercase;color:var(--gold-bright);}
  .hub-card h3{margin-top:10px;font-size:18px;line-height:1.3;color:var(--silver-bright);letter-spacing:-.012em;}
  .hub-card p{margin:10px 0 0;font-size:14.5px;line-height:1.65;color:var(--text-muted);}
  .hub-card .go{margin-top:14px;font-size:13.5px;font-weight:600;color:var(--gold-bright);}
  .hub-note{margin:44px 0 8px;padding:20px 22px;border:1px solid var(--line);border-radius:12px;
    background:var(--bg-alt-2);font-size:14px;line-height:1.7;color:var(--text-muted);}
  .hub-note b{color:var(--silver-bright);}
  .crumb{padding-top:22px;font-size:13px;color:var(--text-muted);}
  .crumb a{color:var(--gold-bright);font-weight:600;}
  @media(max-width:640px){.hub-grid{grid-template-columns:1fr;}}
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def jsonld():
    items = []
    n = 0
    for _t, _n, entries in SECTIONS:
        for href, title, desc, _tag in entries:
            n += 1
            items.append(
                '{"@type":"ListItem","position":%d,"url":"%s/%s","name":"%s"}'
                % (n, SITE, href, title.replace('"', "'"))
            )
    blog = ('{"@context":"https://schema.org","@type":"Blog","name":"NovaFlex Guides & Reference",'
            '"description":"%s","url":"%s/blog.html",'
            '"publisher":{"@type":"Organization","name":"NovaFlex Peptides","url":"%s/"}}'
            % (DESC.replace('"', "'"), SITE, SITE))
    lst = ('{"@context":"https://schema.org","@type":"ItemList","itemListElement":[%s]}'
           % ",".join(items))
    crumb = ('{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
             '{"@type":"ListItem","position":1,"name":"Home","item":"%s/"},'
             '{"@type":"ListItem","position":2,"name":"Guides & Reference","item":"%s/blog.html"}]}'
             % (SITE, SITE))
    return "\n".join('<script type="application/ld+json">%s</script>' % s for s in (blog, lst, crumb))


def main_html():
    out = ['<main>', '  <div class="hub-wrap">',
           '    <div class="crumb"><a href="index.html">Home</a> &rsaquo; Guides &amp; Reference</div>',
           '    <div class="hub-head">',
           '      <div class="eyebrow">Reference Library</div>',
           '      <h1>Guides &amp; reference</h1>',
           '      <p class="lede">Everything here is about how material is verified and documented &mdash; what the '
           'tests measure, what a certificate should contain, and how compounds are classified in the '
           'literature. No claims about results, because that is not what we sell.</p>',
           '    </div>']
    for name, note, entries in SECTIONS:
        out.append('    <section class="hub-sec">')
        out.append('      <h2>%s</h2>' % esc(name))
        out.append('      <p class="sec-note">%s</p>' % esc(note))
        out.append('      <div class="hub-grid">')
        for href, title, desc, tag in entries:
            out.append('        <a class="hub-card" href="%s">' % href)
            out.append('          <div class="tag">%s</div>' % esc(tag))
            out.append('          <h3>%s</h3>' % esc(title))
            out.append('          <p>%s</p>' % esc(desc))
            out.append('          <div class="go">Read &rarr;</div>')
            out.append('        </a>')
        out.append('      </div>')
        out.append('    </section>')
    out.append('    <div class="hub-note"><b>Why these exist.</b> Sourcing research material means reading '
               'paperwork you did not produce. These pages explain how to audit that paperwork &mdash; '
               'including ours. Every compound we list ships with the certificate for its own lot, and '
               'the guides above are what let you check it rather than take it on trust.</div>')
    out.append('  </div>')
    out.append('</main>')
    return "\n".join(out)


def build():
    src = open(DONOR, encoding="utf-8").read()

    style_end = src.index("</style>")
    head_and_style = src[:style_end]
    after_style = src[style_end:]

    hdr_start = after_style.index("<header")
    hdr_end = after_style.index("</header>") + len("</header>")
    header = after_style[hdr_start:hdr_end]

    ftr_start = after_style.index("<footer")
    tail = after_style[ftr_start:]

    # Swap the donor's per-article head metadata for this page's.
    head = head_and_style
    head = re.sub(r"<title>.*?</title>", "<title>%s</title>" % TITLE, head, flags=re.S)
    head = re.sub(r'<meta name="description" content=".*?">',
                  '<meta name="description" content="%s">' % DESC, head, flags=re.S)
    head = re.sub(r'<link rel="canonical" href=".*?">',
                  '<link rel="canonical" href="%s/blog.html">' % SITE, head)
    head = re.sub(r'<meta property="og:type" content=".*?">',
                  '<meta property="og:type" content="website">', head)
    head = re.sub(r'<meta property="og:title" content=".*?">',
                  '<meta property="og:title" content="%s">' % TITLE, head)
    head = re.sub(r'<meta property="og:description" content=".*?">',
                  '<meta property="og:description" content="%s">' % DESC, head)
    head = re.sub(r'<meta property="og:url" content=".*?">',
                  '<meta property="og:url" content="%s/blog.html">' % SITE, head)
    # The donor's Article + FAQPage blocks describe the donor, not this page.
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", head, flags=re.S)
    head = head.replace("<style>", jsonld() + "\n<style>", 1)

    # This page is the canonical Guides destination, so the nav should point here.
    header = header.replace('<a href="how-to-read-a-coa.html">Guides</a>',
                            '<a href="blog.html" aria-current="page">Guides</a>')

    html = head + EXTRA_CSS + "</style>\n</head>\n<body>\n" + header + "\n\n" + main_html() + "\n\n" + tail
    open(OUT, "w", encoding="utf-8").write(html)
    return html


if __name__ == "__main__":
    h = build()
    print("wrote blog.html — %d bytes" % len(h))
    for tag in ("<html", "</html>", "<head", "</head>", "<body", "</body>", "<main", "</main>",
                "<header", "</header>", "<footer", "</footer>", "<style", "</style>"):
        print("  %-10s %d" % (tag, h.count(tag)))
