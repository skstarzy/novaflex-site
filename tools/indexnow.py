#!/usr/bin/env python3
"""Pushes the sitemap's URLs to IndexNow.

Why bother when a sitemap already exists: a sitemap is a passive invitation —
the crawler comes back when it feels like it, and for a domain with almost no
authority that can be weeks. IndexNow is a push. One request tells Bing,
Yandex and Seznam that these URLs changed, and they fetch on their own
schedule rather than ours.

Bing matters here beyond Bing's own traffic share. It backs ChatGPT's search
results, and robots.txt now lets OAI-SearchBot through, so getting these pages
into Bing's index is what makes them eligible to be cited in an assistant's
answer to "which research compound suppliers publish a COA".

Google does not participate in IndexNow and never has. Google discovery still
depends on the sitemap plus the internal links, which is why the catalog grid
and the related-compound blocks matter more than this does. Run it after a
deploy has gone live — the key file has to be fetchable before the submission
is accepted.

    python3 tools/indexnow.py
"""

import glob
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "novaflexusa.com"
ENDPOINT = "https://api.indexnow.org/indexnow"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) NovaFlex-IndexNow/1.0"


def find_key():
    """The key lives in a file at the site root named after the key itself —
    that file IS the proof of ownership, so it has to ship with the site."""
    for path in glob.glob(os.path.join(ROOT, "*.txt")):
        name = os.path.basename(path)[:-4]
        if re.fullmatch(r"[0-9a-f]{8,128}", name):
            body = open(path).read().strip()
            if body == name:
                return name
    sys.exit("no IndexNow key file found at the site root")


def sitemap_urls():
    sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    return re.findall(r"<loc>(.*?)</loc>", sm)


def main():
    key = find_key()
    urls = sitemap_urls()
    key_location = "https://%s/%s.txt" % (HOST, key)

    # Refuse to submit if the key file isn't actually live — the endpoint
    # answers 200 either way and silently drops the batch, so checking here is
    # the difference between "submitted" and "believed submitted".
    # Cloudflare sits in front of the site and 403s urllib's default
    # User-Agent, so the check has to identify itself like a client.
    probe = urllib.request.Request(key_location, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(probe, timeout=20) as r:
            if r.read().decode().strip() != key:
                sys.exit("key file at %s does not contain the key" % key_location)
    except Exception as e:
        sys.exit("key file not reachable at %s (%s) — deploy first" % (key_location, e))

    payload = {
        "host": HOST,
        "key": key,
        "keyLocation": key_location,
        "urlList": urls,
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": UA},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        code = r.status
    print("submitted %d URLs to IndexNow — HTTP %s" % (len(urls), code))
    print("key file: %s" % key_location)


if __name__ == "__main__":
    main()
