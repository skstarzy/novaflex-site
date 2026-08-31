#!/usr/bin/env python3
"""
Has the published vial art drifted from the catalog?

On 31 August the NV-6PT 5mg card was found showing a vial labelled 10 MG, and
the 10mg card had no image at all. The catalog data was correct the whole time;
the art was simply built before NV-6PT was split into two sizes and never
rebuilt. Nothing anywhere compared the pictures against the product list, so it
sat on a live listing stating the wrong dose.

The labels are generated, and generation is deterministic: rebuilding from
assets/vials/_original/ produces byte-identical files when nothing has changed.
That makes drift cheap to detect without reading a single pixel - rebuild, and
see whether anything moved.

Three outcomes:
  clean   every published vial matches what the catalog would produce now
  DRIFT   a file changed, so what is published disagrees with the catalog
  MISSING a catalogued product has no source render, so no art can be built

On drift the regenerated files are the correct ones and are left in the working
tree for review; this reports, it does not commit.

Run: python3 tools/art-drift.py
Exit: 0 clean, 1 drift or missing art.
"""

import hashlib, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIALS = os.path.join(ROOT, "docs", "assets", "vials")
INDEX = os.path.join(ROOT, "docs", "index.html")
REBUILD = os.path.join(ROOT, "tools", "rebuild-vial-labels.py")


def digests():
    out = {}
    for f in sorted(os.listdir(VIALS)):
        if f.endswith(".webp"):
            with open(os.path.join(VIALS, f), "rb") as fh:
                out[f] = hashlib.sha256(fh.read()).hexdigest()
    return out


def catalog_slugs():
    src = open(INDEX).read()
    m = re.search(r"const PRODUCTS = \[(.*?)\n\];", src, re.S)
    if not m:
        sys.exit("could not find PRODUCTS in index.html")
    slugs = []
    for row in re.findall(r"\{([^}]*)\}", m.group(1)):
        d = dict(re.findall(r'(\w+)\s*:\s*"([^"]*)"', row))
        if d.get("slug"):
            slugs.append(d["slug"])
    return slugs


def main():
    slugs = catalog_slugs()

    # Every catalogued product needs art, and art needs a source render. A
    # missing source is why the 10mg card served a 404 for as long as it did.
    missing_art, missing_src = [], []
    for s in slugs:
        if not os.path.exists(os.path.join(VIALS, f"NF-{s}.webp")):
            missing_art.append(s)
        if not os.path.exists(os.path.join(VIALS, "_original", f"NF-{s}.webp")):
            missing_src.append(s)

    before = digests()
    r = subprocess.run([sys.executable, REBUILD], capture_output=True, text=True)
    if r.returncode != 0:
        print("FAILED to run the label rebuild:")
        print((r.stderr or r.stdout).strip()[-600:])
        sys.exit(1)
    after = digests()

    changed = sorted(k for k in after if before.get(k) != after[k])
    added = sorted(k for k in after if k not in before)

    print(f"\nNovaFlex vial art — {len(slugs)} catalogued products, {len(after)} rendered\n")
    bad = False
    if missing_src:
        bad = True
        print(f"  MISSING SOURCE  no _original render, so no art can be built: {', '.join(missing_src)}")
    if missing_art:
        bad = True
        print(f"  MISSING ART     catalogued but not rendered: {', '.join(missing_art)}")
    if changed or added:
        bad = True
        for f in changed:
            print(f"  DRIFT           {f} — published art disagrees with the catalog")
        for f in added:
            print(f"  DRIFT           {f} — was not published at all")
        print("\n  The rebuilt files are correct and are left in the working tree.")
        print("  Review them, then commit.")
    if not bad:
        print(f"  clean — all {len(after)} vials match what the catalog produces today")
    print()
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
