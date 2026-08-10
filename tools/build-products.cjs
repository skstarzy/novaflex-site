#!/usr/bin/env node
/**
 * build-products.cjs — generate one static, indexable page per product.
 *
 *   node tools/build-products.cjs
 *
 * Why this exists
 * ---------------
 * Every product used to live at product.html?slug=X. That is a single URL with
 * a single <title>, and the product markup only appeared after JS ran. Crawlers
 * saw one page, so 25 products competed as one.
 *
 * This emits products/<slug>/index.html for each item, each with a real title,
 * description, canonical, OG tags, Product + BreadcrumbList JSON-LD, and the
 * product markup already in the HTML source.
 *
 * How
 * ---
 * Rather than reimplement render() here (which would drift the moment
 * product.html changes), we load the real page in Chromium, let its own
 * render() run, and snapshot the DOM it produced. product.html stays the single
 * source of truth for both markup and copy. Re-run this after editing it.
 */

const fs   = require('fs');
const path = require('path');
const { chromium } = require('/opt/node22/lib/node_modules/playwright');

const ROOT     = path.resolve(__dirname, '..');
const SRC      = path.join(ROOT, 'product.html');
const OUT_DIR  = path.join(ROOT, 'products');
const ORIGIN   = 'https://novaflexusa.com';
const BROWSER  = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

const src = fs.readFileSync(SRC, 'utf8');

/* Pull the catalog straight out of product.html so there is one source of truth. */
function extract(name, open, close) {
  const start = src.indexOf(`const ${name} = ${open}`);
  if (start === -1) throw new Error(`Could not find "const ${name} = ${open}" in product.html`);
  const end = src.indexOf(`\n${close};`, start);
  if (end === -1) throw new Error(`Could not find the end of ${name}`);
  return src.slice(start + `const ${name} = `.length, end + 1 + close.length);
}
const PRODUCTS = new Function(`return ${extract('PRODUCTS', '[', ']')}`)();
const CONTENT  = new Function(`return ${extract('CONTENT', '{', '}')}`)();

const esc = s => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');

/* Insert once, and fail loudly rather than silently producing a broken page. */
function replaceOnce(hay, needle, repl, label) {
  const i = hay.indexOf(needle);
  if (i === -1) throw new Error(`Anchor missing (${label}): ${needle.slice(0, 60)}`);
  if (hay.indexOf(needle, i + 1) !== -1) throw new Error(`Anchor not unique (${label})`);
  return hay.slice(0, i) + repl + hay.slice(i + needle.length);
}

function buildPage(p, snap) {
  const url   = `${ORIGIN}/products/${p.slug}/`;
  const img   = `${ORIGIN}/assets/vials/NF-${p.slug}.webp`;
  const title = snap.title;
  const desc  = snap.description;

  const product = {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": (p.seoName || p.name) + ' ' + p.spec,
    "category": snap.category,
    "image": img,
    "brand": { "@type": "Brand", "name": "NovaFlex Peptides" },
    "description": snap.overview,
    "offers": {
      "@type": "Offer",
      "price": p.price.toFixed(2),
      "priceCurrency": "USD",
      "availability": p.soldOut ? "https://schema.org/OutOfStock" : "https://schema.org/InStock",
      "url": url
    }
  };

  const crumbs = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Home",          "item": `${ORIGIN}/` },
      { "@type": "ListItem", "position": 2, "name": "Catalog",       "item": `${ORIGIN}/#catalog` },
      { "@type": "ListItem", "position": 3, "name": snap.category,   "item": `${ORIGIN}/#catalog` },
      { "@type": "ListItem", "position": 4, "name": p.display || p.name, "item": url }
    ]
  };

  const faqs = (snap.faqs || []).filter(f => f.q && f.a);
  const faqLd = faqs.length ? {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": faqs.map(f => ({
      "@type": "Question", "name": f.q,
      "acceptedAnswer": { "@type": "Answer", "text": f.a }
    }))
  } : null;

  let out = src;

  /* Pages sit two levels deep, so relative paths need a root base. Safe here:
     product.html has no bare "#" anchors and SHOP_API is absolute. */
  out = replaceOnce(out,
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    + '<base href="/">',
    'viewport/base');

  /* Real head metadata instead of the shared placeholder. */
  const head = [
    `<title>${esc(title)}</title>`,
    `<meta name="description" content="${esc(desc)}">`,
    `<link rel="canonical" href="${url}">`,
    `<meta property="og:type" content="product">`,
    `<meta property="og:site_name" content="NovaFlex Peptides">`,
    `<meta property="og:title" content="${esc(title)}">`,
    `<meta property="og:description" content="${esc(desc)}">`,
    `<meta property="og:url" content="${url}">`,
    `<meta property="og:image" content="${img}">`,
    `<meta name="twitter:card" content="summary_large_image">`,
    `<script type="application/ld+json" data-nf-product>${JSON.stringify(product)}</script>`,
    `<script type="application/ld+json">${JSON.stringify(crumbs)}</script>`,
    faqLd ? `<script type="application/ld+json">${JSON.stringify(faqLd)}</script>` : null
  ].filter(Boolean).join('\n');

  out = replaceOnce(out, '<title>NovaFlex Peptides</title>', head, 'title');
  out = replaceOnce(out,
    '<meta name="description" content="Research-grade peptide details — third-party verified purity. For research use only.">',
    '', 'old description');

  /* The markup itself, so a crawler sees the product without executing JS. */
  out = replaceOnce(out, '<div id="pdContent"></div>',
    `<div id="pdContent">${snap.html}</div>`, 'pdContent');

  /* Tell the page's own render() which product it is. */
  out = replaceOnce(out, '<script>\nconst CHECKOUT_API_URL',
    `<script>window.NF_SLUG=${JSON.stringify(p.slug)};</script>\n<script>\nconst CHECKOUT_API_URL`,
    'NF_SLUG');

  return out;
}

(async () => {
  const browser = await chromium.launch({ executablePath: BROWSER, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.route('**/*', r => {
    const u = r.request().url();
    return (u.startsWith('file://') || u.startsWith('data:')) ? r.continue() : r.abort();
  });
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));

  let written = 0;
  for (const p of PRODUCTS) {
    errors.length = 0;
    await page.goto(`file://${SRC}?slug=${p.slug}`, { waitUntil: 'domcontentloaded' });
    await page.waitForFunction(
      () => { const el = document.getElementById('pdContent'); return el && el.children.length > 0; },
      { timeout: 15000 }
    );

    const snap = await page.evaluate(() => {
      const md = document.querySelector('meta[name="description"]');
      const cat = document.querySelector('.pd-cat');
      return {
        html: document.getElementById('pdContent').innerHTML,
        title: document.title,
        description: md ? md.getAttribute('content') : '',
        category: cat ? cat.textContent.trim() : ''
      };
    });

    if (/Product not found/.test(snap.html)) throw new Error(`render() failed for ${p.slug}`);
    if (errors.length) throw new Error(`JS errors on ${p.slug}: ${errors.join(' | ')}`);

    const c = CONTENT[p.slug] || {};
    snap.overview = c.overview || snap.description;
    snap.faqs = c.faqs || [];

    const dir = path.join(OUT_DIR, p.slug);
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, 'index.html'), buildPage(p, snap));
    written++;
    console.log(`  products/${p.slug}/index.html  —  ${snap.title}`);
  }

  await browser.close();

  /* sitemap — every static page plus the top-level ones */
  const today = new Date().toISOString().slice(0, 10);
  const urls = [
    { loc: `${ORIGIN}/`,              pri: '1.0', freq: 'weekly' },
    { loc: `${ORIGIN}/team.html`,     pri: '0.5', freq: 'monthly' },
    { loc: `${ORIGIN}/policies.html`, pri: '0.3', freq: 'yearly' },
    ...PRODUCTS.map(p => ({ loc: `${ORIGIN}/products/${p.slug}/`, pri: '0.8', freq: 'weekly' }))
  ];
  fs.writeFileSync(path.join(ROOT, 'sitemap.xml'),
    '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    urls.map(u =>
      `  <url>\n    <loc>${u.loc}</loc>\n    <lastmod>${today}</lastmod>\n` +
      `    <changefreq>${u.freq}</changefreq>\n    <priority>${u.pri}</priority>\n  </url>`
    ).join('\n') +
    '\n</urlset>\n');

  console.log(`\n${written} product pages · sitemap.xml now lists ${urls.length} URLs`);
})().catch(e => { console.error('\nBUILD FAILED:', e.message); process.exit(1); });
