/* Cloudflare Web Analytics for the storefront.
 *
 * The site's own visitor analytics — separate from the Meta pixel, which only
 * reports ad-attributed events. This answers "who is visiting, from where, to
 * which pages" for ALL traffic, including organic search and direct.
 *
 * Chosen over Google Analytics on purpose: Cloudflare Web Analytics is
 * cookieless and privacy-first, so it needs no cookie-consent banner (one less
 * thing on a compliance-sensitive site), it's free, and the site already sits
 * behind Cloudflare. It samples pageviews and core web vitals server-adjacent,
 * with none of GA4's weight or setup.
 *
 * Inert until TOKEN is filled in — exactly like assets/meta-pixel.js. With an
 * empty token nothing loads and no request leaves the page, so this ships to
 * every page before the analytics site exists in the Cloudflare dashboard and
 * stays harmless until activated.
 *
 * To activate: Cloudflare dashboard -> Web Analytics -> Add a site ->
 * novaflexusa.com -> copy the token from the snippet it shows, paste it below,
 * deploy. That one string is the only edit; every page loads this one file.
 */
(function () {
  var TOKEN = ""; // <-- paste the Cloudflare Web Analytics token here

  // lets you confirm in the console which build a browser actually has, since
  // this file is cached hard by GitHub Pages
  window.__nfCfa = { version: 1, active: !!TOKEN };

  if (!TOKEN) return;

  var s = document.createElement("script");
  s.defer = true;
  s.src = "https://static.cloudflareinsights.com/beacon.min.js";
  s.setAttribute("data-cf-beacon", JSON.stringify({ token: TOKEN }));
  document.head.appendChild(s);
})();
