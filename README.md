# novaflexusa.com

Static storefront for NovaFlex LLC. No build step to deploy — GitHub Pages
serves `docs/` directly.

## Layout

    docs/      the published site. Everything here is public.
    tools/     build scripts. NOT published.
    drafts/    unpublished articles and saved page snippets. NOT published.

**The split is the point.** GitHub Pages used to serve this repo from its root,
which meant `tools/` and `_unpublished/` were reachable at
`novaflexusa.com/tools/…`. That exposed the product copy source — which still
carried the real compound names the storefront had spent August removing — and a
partner-programme page that had been taken down months earlier. Anything that is
not meant to be public must live outside `docs/`.

Before adding a directory, decide which side of that line it belongs on.

## Deployment

Settings → Pages → Build and deployment → Deploy from a branch → `main` / `docs`.

`docs/CNAME` holds the custom domain and `docs/.nojekyll` disables Jekyll
processing; both must stay inside `docs/` or the site breaks.

Pushing to `main` deploys. Allow ~10 minutes for the GitHub Pages edge cache and
Cloudflare to pick up a change, and bump the `?v=` query on an asset whose bytes
changed but whose name did not.

## Tools

All of them resolve paths through `docs/`, and are run from the repo root:

    python3 tools/build-seo.py            regenerate the 25 product pages,
                                          sitemap, index grid and llms.txt
                                          from docs/product.html
    python3 tools/rebuild-vial-labels.py  redraw vial label art
    python3 tools/apply-product-copy.py   rewrite the CONTENT map in product.html
    python3 tools/indexnow.py             ping IndexNow with changed URLs
    python3 tools/add-meta-pixel.py       add/remove the Meta pixel tag
    python3 tools/build-blog.py           rebuild the blog index from drafts/

## Naming

The storefront lists house codes, never compound names — in copy, in filenames,
in image art and in alt text. `_work/novaflex-backend-v2/lib/productCode.js`
translates codes to database names at the API boundary. Old compound-named URLs
survive as redirect stubs in `docs/` and should not be deleted; they carry the
inbound links.
