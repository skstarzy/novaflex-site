#!/usr/bin/env python3
"""Rebuilds the compound label on every vial render.

The shipped vial art is a good 3D render with three flat black rectangles
composited over the label: the compound name, the dose, and a purity/RUO block.
They overhang the glass on both sides, they sit square on a cylinder that is
clearly lit from the left, and the source template's own "[DOSAGE]" placeholder
is visible peeking out from under one of them. At the 96px thumbnail the
storefront used to show, nobody noticed. On a full-width product page — and in
a paid ad at 1080px — it is the first thing the eye lands on, and it undercuts
the one thing this brand sells, which is that the documentation is real.

Rather than cover the boxes, this resynthesises that stretch of label:

  1. Clip the alpha back to the true glass silhouette, killing the overhang.
     The body taper is linear across this range — measured (53,358) at y=440 and
     (71,377) at y=670, and that interpolation predicts the known-clean row at
     y=540 to within a pixel — so two endpoints describe it exactly.
  2. Rebuild the label surface by tiling a clean scanline, rescaled to the body
     width at each row, so it inherits the real cylinder shading and the gold
     edge lines. The donor is a per-pixel median of the flattest rows on the
     label, not any single row: one row always catches a little antialiasing
     from the letters above it, and tiling that turns one stray grey pixel into
     a vertical streak down the whole vial. Brightness is anchored to the
     untouched rows immediately above and below, which removes both seams by
     construction instead of by a guessed falloff.
  3. Set the type properly — tracked out, with the horizontal squeeze a label
     wrapped around a cylinder actually has, and auto-fitted so a long name like
     TESAMORELIN holds the same margins as NAD+.

Everything printed on the label is a supply fact: compound, dose, assayed
purity, research-use-only. Same line the rest of the business runs on.

The catalog is read from index.html's PRODUCTS, so this can never label a vial
with a name or purity the storefront doesn't show. Originals are preserved in
assets/vials/_original/ on first run and every later run reads from there, so
rebuilding twice can't compound artefacts.

    python3 tools/rebuild-vial-labels.py
"""

import os
import re
import shutil
import sys

from PIL import Image, ImageDraw, ImageFont

# The published site lives in docs/ so that GitHub Pages serves only what is
# meant to be public. Build tooling and drafts sit beside it in the repo and
# are never deployed - which is the bug this layout exists to prevent, after
# tools/ and _unpublished/ turned out to be readable at novaflexusa.com.
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
VIALS = os.path.join(ROOT, "assets", "vials")
ORIGINAL = os.path.join(VIALS, "_original")

# Glass silhouette, from an alpha scan of the source renders (all 450x798).
Y0, Y1 = 421, 668            # composited boxes, plus the discontinued brand line above them
# Y0 was 446, which cleared the boxes only. The brand on the label read
# the two-word lockup and the business dropped the second word, so the band now
# starts at 421 and swallows that line too. The NOVAFLEX wordmark sits at
# y=386-414 and is deliberately left alone; measured from an alpha/brightness
# scan of the source render, not guessed.
EDGE_A, EDGE_B = 440, 670    # rows the taper was measured on
L_A, R_A = 53.0, 358.0
L_B, R_B = 71.0, 377.0
DONOR_RANGE = (290, 380)     # clean label rows above the wordmark
# Pulled back from (282, 444): that range ran through the dropped word, and
# tiling a row of faint letter antialiasing streaks it down the whole vial.
DONOR_N = 14                 # how many of the flattest to median together
STRIP_W = 305

GOLD = (201, 162, 57)
WHITE = (247, 244, 238)
MUTED = (150, 143, 130)

FONT_PATH = "/System/Library/Fonts/HelveticaNeue.ttc"
FONT_IDX = {"regular": 0, "bold": 1, "medium": 10}


def edges(y):
    t = (y - EDGE_A) / (EDGE_B - EDGE_A)
    return L_A + t * (L_B - L_A), R_A + t * (R_B - R_A)


def font(size, weight="bold"):
    return ImageFont.truetype(FONT_PATH, size, index=FONT_IDX[weight])


def donor_strip(im):
    """A clean label scanline: the flattest rows above the boxes, normalised to
    one width and medianed per pixel so no letter edge survives into the tile."""
    rows = []
    for y in range(*DONOR_RANGE):
        l, r = edges(y)
        row = im.crop((int(round(l)), y, int(round(r)), y + 1)).convert("RGB")
        vals = list(row.resize((STRIP_W, 1), Image.LANCZOS).getdata())
        rough = sum(abs(a[0] - b[0]) for a, b in zip(vals, vals[1:]))
        rows.append((rough, vals))
    rows.sort(key=lambda t: t[0])
    picked = [v for _, v in rows[:DONOR_N]]
    mid = len(picked) // 2

    strip = Image.new("RGB", (STRIP_W, 1))
    strip.putdata(
        [
            tuple(sorted(p[i][c] for p in picked)[mid] for c in range(3))
            for i in range(STRIP_W)
        ]
    )
    return strip


def tracked(draw, cx, y, text, fnt, fill, track=0.0, squeeze=1.0):
    """Centred text with letter-spacing, drawn on a scratch layer so the
    cylinder squeeze can be applied without resampling the label beneath it."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + track * (len(text) - 1)
    pad = 8
    layer = Image.new("RGBA", (int(total) + pad * 2, fnt.size * 2 + pad * 2), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    x = pad
    for ch, w in zip(text, widths):
        ld.text((x, pad), ch, font=fnt, fill=fill + (255,))
        x += w + track
    if squeeze != 1.0:
        layer = layer.resize((max(1, int(layer.width * squeeze)), layer.height), Image.LANCZOS)
    return layer, (int(cx - layer.width / 2), int(y - pad))


def rebuild(src_path, dst_path, name, dose, purity):
    im = Image.open(src_path).convert("RGBA")
    if im.size != (450, 798):
        sys.exit("%s is %dx%d; the measured geometry assumes 450x798" % (src_path, *im.size))

    strip = donor_strip(im)

    def row_mean(y):
        l, r = edges(y)
        row = im.crop((int(round(l)) + 6, y, int(round(r)) - 6, y + 1)).convert("L")
        return sum(row.getdata()) / row.width

    m0 = sum(strip.convert("L").getdata()) / STRIP_W
    top_mean, bot_mean = row_mean(Y0 - 3), row_mean(Y1 + 1)

    band = Image.new("RGBA", im.size, (0, 0, 0, 0))
    for y in range(Y0, Y1):
        l, r = edges(y)
        w = int(round(r - l))
        t = (y - Y0) / (Y1 - Y0)
        k = (top_mean + t * (bot_mean - top_mean)) / max(m0, 1e-6)
        row = strip.resize((w, 1), Image.LANCZOS).point(lambda v, k=k: min(255, int(v * k)))

        rowa = row.convert("RGBA")
        mask = Image.new("L", (w, 1), 255)      # soften the glass boundary so the
        md = mask.load()                        # band doesn't cut a hard edge
        md[0, 0] = md[w - 1, 0] = 150
        rowa.putalpha(mask)
        band.paste(rowa, (int(round(l)), y), rowa)

    d = ImageDraw.Draw(band)
    cx = sum(edges(500)) / 2

    # Hold a margin so every SKU reads as the same label, however long the name.
    max_w = (edges(474)[1] - edges(474)[0]) * 0.74
    size = 34
    while size > 18 and d.textlength(name, font=font(size)) + 1.5 * (len(name) - 1) > max_w:
        size -= 1

    lines = [(name, 474, font(size), WHITE, 1.5)]
    if purity:
        lines.append((dose, 548, font(21, "medium"), GOLD, 4.0))
        lines.append(("%s PURITY" % purity, 600, font(14, "medium"), MUTED, 3.6))
        lines.append(("RESEARCH USE ONLY", 626, font(14, "medium"), GOLD, 3.6))
    else:
        # Solvents carry no assay, so the label centres volume over the notice
        # rather than leaving a conspicuous gap where a purity figure would be.
        lines.append((dose, 556, font(21, "medium"), GOLD, 4.0))
        lines.append(("STERILE DILUENT", 606, font(14, "medium"), MUTED, 3.6))
        lines.append(("RESEARCH USE ONLY", 632, font(14, "medium"), GOLD, 3.6))

    for text, y, fnt, fill, track in lines:
        layer, pos = tracked(d, cx, y, text, fnt, fill, track, squeeze=0.94)
        band.alpha_composite(layer, pos)

    for yy, alpha in ((522, 150), (523, 60)):
        l, r = edges(yy)
        d.line([(l + 34, yy), (r - 34, yy)], fill=GOLD + (alpha,))

    out = im.copy()
    px = out.load()
    for y in range(Y0 - 2, Y1 + 4):
        l, r = edges(y)
        for x in range(out.width):
            if x < l - 2 or x > r + 2:
                p = px[x, y]
                px[x, y] = (p[0], p[1], p[2], 0)
    out.alpha_composite(band)
    # Write to a sibling temp file and rename over the target. Saving straight
    # onto dst_path means an interrupted run - a timeout, a sleep, a Ctrl-C -
    # leaves a half-written .webp in the published tree that no longer decodes.
    # That happened while testing the drift guard: one interrupted rebuild left
    # NF-nv5ks-5mg.webp corrupt and serveable. rename() on the same filesystem
    # is atomic, so the published file is either the old one or the new one.
    tmp = dst_path + ".tmp"
    out.save(tmp, "WEBP", quality=90, method=6)
    os.replace(tmp, dst_path)


def catalog():
    """Compound, dose and purity straight from the storefront's PRODUCTS, so a
    vial can never be labelled with something the catalog doesn't sell."""
    src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    m = re.search(r"const PRODUCTS = \[(.*?)\n\];", src, re.S)
    if not m:
        sys.exit("could not find PRODUCTS in index.html")

    out = []
    for row in re.findall(r"\{([^}]*)\}", m.group(1)):
        d = dict(re.findall(r'(\w+)\s*:\s*"([^"]*)"', row))
        if "slug" not in d:
            continue
        label = d.get("display") or d["name"]
        # Multi-component vials list their components in `display`. That used to
        # fall back to the house name, but those names ("Wolverine Stack",
        # "Glow Blend") are the branded wording being removed from the storefront,
        # so the components are now what goes on the label. set_type auto-fits,
        # so the four-component vial still holds its margins.
        dose = d.get("spec", "").replace(" vial", "").upper().replace("MG", " MG").replace("ML", " ML")
        out.append((d["slug"], label, " ".join(dose.split()), d.get("purity")))
    return out


def main():
    if not os.path.isdir(ORIGINAL):
        os.makedirs(ORIGINAL)
        for f in os.listdir(VIALS):
            if f.endswith(".webp"):
                shutil.copy2(os.path.join(VIALS, f), os.path.join(ORIGINAL, f))
        print("preserved %d source renders in assets/vials/_original/"
              % len(os.listdir(ORIGINAL)))

    done = 0
    for slug, name, dose, purity in catalog():
        fn = "NF-%s.webp" % slug
        src = os.path.join(ORIGINAL, fn)
        if not os.path.exists(src):
            print("  skip %-18s (no source render)" % slug)
            continue
        rebuild(src, os.path.join(VIALS, fn), name, dose, purity)
        print("  %-18s %-14s %-8s %s" % (slug, name, dose, purity or "—"))
        done += 1
    print("relabelled %d vials" % done)


if __name__ == "__main__":
    main()
