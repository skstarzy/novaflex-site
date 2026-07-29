/* Meta pixel for the storefront.
 *
 * Inert until PIXEL_ID is filled in — an empty ID means nothing loads, nothing
 * fires, and no requests leave the page. That is deliberate: the tag ships to
 * every page via tools/add-meta-pixel.py before the pixel exists in Business
 * Manager, so it has to be harmless in the meantime.
 *
 * To activate: create the dataset in Events Manager, paste its ID below, deploy.
 * That is the only edit needed — every page loads this one file.
 *
 * Events sent:
 *   PageView    every page
 *   ViewContent generated product pages, read from the Product JSON-LD that
 *               build-seo.py already emits (so no per-page markup to maintain)
 *   AddToCart   by wrapping window.addToCart, not by editing the cart
 *   Purchase    on order-confirmed.html once the backend confirms 'paid'
 *
 * The wrapping approach matters: none of the store's own code changes, so a
 * mistake here can break tracking but cannot break checkout.
 */
(function () {
  var PIXEL_ID = "1053607190400345"; // "NovaFlex Web" dataset, NovaFlex portfolio

  // lets you confirm in the console which build a browser actually has, since
  // this file is cached hard by GitHub Pages
  window.__nfPixel = { version: 3, active: !!PIXEL_ID, capiDedup: true };

  if (!PIXEL_ID) return;

  /* ---- standard Meta bootstrap ---- */
  !function (f, b, e, v, n, t, s) {
    if (f.fbq) return; n = f.fbq = function () {
      n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
    };
    if (!f._fbq) f._fbq = n;
    n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = [];
    t = b.createElement(e); t.async = !0; t.src = v;
    s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
  }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');

  fbq('init', PIXEL_ID);
  fbq('track', 'PageView');

  /* ---- ViewContent, off the Product JSON-LD ---- */
  function productFromJsonLd() {
    var nodes = document.querySelectorAll('script[type="application/ld+json"]');
    for (var i = 0; i < nodes.length; i++) {
      try {
        var d = JSON.parse(nodes[i].textContent);
        var list = Array.isArray(d) ? d : [d];
        for (var j = 0; j < list.length; j++) {
          if (list[j] && list[j]['@type'] === 'Product') return list[j];
        }
      } catch (e) { /* a malformed block shouldn't stop the others */ }
    }
    return null;
  }

  var product = productFromJsonLd();
  if (product) {
    var offer = product.offers || {};
    fbq('track', 'ViewContent', {
      content_name: product.name,
      content_type: 'product',
      value: Number(offer.price) || undefined,
      currency: offer.priceCurrency || 'USD'
    });
  }

  /* ---- AddToCart, by wrapping the store's own functions ----
   * Two different functions add to the cart and they take different arguments:
   *   index.html      addToCart(name, spec, price)
   *   product.html    addCurrentToCart(product)   <- takes the whole object
   * Wrapping both is what makes AddToCart fire on product pages, which is where
   * most paid traffic lands.
   */
  function track(name, spec, price) {
    try {
      fbq('track', 'AddToCart', {
        content_name: name,
        content_type: 'product',
        value: Number(price) || undefined,
        currency: 'USD'
      });
    } catch (e) { /* never let tracking take the cart down with it */ }
  }

  function wrap(fnName, read) {
    var fn = window[fnName];
    if (typeof fn !== 'function' || fn.__nfWrapped) return false;
    var wrapped = function () {
      var result = fn.apply(this, arguments);
      var info = read(arguments);
      if (info) track(info.name, info.spec, info.price);
      return result;
    };
    wrapped.__nfWrapped = true;
    window[fnName] = wrapped;
    return true;
  }

  function wrapCartFns() {
    var a = wrap('addToCart', function (args) {
      return { name: args[0], spec: args[1], price: args[2] };
    });
    var b = wrap('addCurrentToCart', function (args) {
      var p = args[0] || {};
      return { name: p.name, spec: p.spec, price: p.price };
    });
    return a || b;
  }

  // the store defines these in inline scripts, which may run after this file
  // depending on defer ordering — so try now, then again on DOM ready
  wrapCartFns();
  document.addEventListener('DOMContentLoaded', wrapCartFns);

  /* ---- Purchase, on the confirmation page ---- */
  if (/order-confirmed/.test(location.pathname)) {
    var orderId = new URLSearchParams(location.search).get('order') || '';
    var dedupeKey = 'nf_fbq_purchase_' + orderId;

    var fire = function (total) {
      // order-confirmed polls the backend, so render('paid') can be called more
      // than once for one order. Session-scoped guard keeps Purchase to one.
      try {
        if (!orderId || sessionStorage.getItem(dedupeKey)) return;
        sessionStorage.setItem(dedupeKey, '1');
      } catch (e) { /* private mode: accept the small double-count risk */ }
      // eventID must match event_id from the server-side Conversions API in
      // the backend's lib/metaCapi.js — Meta collapses the browser event and
      // the server event into one only when event_name AND event id agree.
      // Without this the same purchase is counted twice, which would make a
      // losing campaign read as profitable.
      fbq('track', 'Purchase', {
        value: Number(total) || undefined,
        currency: 'USD',
        content_type: 'product'
      }, { eventID: 'order_' + orderId });
    };

    var hookRender = function () {
      if (typeof window.render !== 'function' || window.render.__nfWrapped) return false;
      var original = window.render;
      var wrapped = function (state, total) {
        var result = original.apply(this, arguments);
        if (state === 'paid' && typeof total === 'number') {
          try { fire(total); } catch (e) {}
        }
        return result;
      };
      wrapped.__nfWrapped = true;
      window.render = wrapped;
      return true;
    };

    if (!hookRender()) document.addEventListener('DOMContentLoaded', hookRender);
  }
})();
