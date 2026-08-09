#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetch the ground-truth source text this deck is built from.

Downloads all 18 chapters of "Discover Canada: The Rights and Responsibilities
of Citizenship" plus the live IRCC citizenship-test pages, strips them to plain
text, and writes them to <outdir>/text/ and <outdir>/examtext/.

factcheck.py reads those directories. Run this first if you are verifying the
deck from a clean checkout.

Usage:  python fetch_sources.py [outdir]        (default: ./sources)

No Python dependencies. Fetching goes through `curl` because canada.ca sits
behind a CDN that stalls or 403s other clients (Claude Code's WebFetch gets a
403; a plain urllib request hangs). urllib is kept only as a fallback for
machines without curl.
"""

import html
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

GUIDE_BASE = ("https://www.canada.ca/en/immigration-refugees-citizenship/"
              "corporate/publications-manuals/discover-canada/read-online")

TEST_BASE = ("https://www.canada.ca/en/immigration-refugees-citizenship/"
             "services/canadian-citizenship/test")

# The 18 chapters, in the order they appear in the guide.
GUIDE_PAGES = [
    "notice",
    "message-readers",
    "oath-citizenship",
    "applying-citizenship",
    "rights-resonsibilities-citizenship",   # sic - canada.ca spells it this way
    "who-are-canadians",
    "canadas-history",
    "modern-canada",
    "how-canadians-govern-themselves",
    "federal-elections",
    "justice-system",
    "canadian-symbols",
    "canadas-economy",
    "canadas-regions",
    "memorable-quotes",
    "study-questions",
    "authorities",
    "more-information",
]

# Live IRCC pages describing the test itself (format, scoring, process).
TEST_PAGES = ["how-it-works", "study", "online", "results", "invitation", "missed"]

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


HAVE_CURL = shutil.which("curl") is not None


def fetch(url):
    """Fetch a URL as text. Prefers curl; see module docstring for why."""
    if HAVE_CURL:
        # Do NOT set -A here: canada.ca's CDN resets the HTTP/2 stream for
        # spoofed browser User-Agents. curl's own default UA works fine.
        p = subprocess.run(
            ["curl", "-sSL", "--fail", "--max-time", "60", url],
            capture_output=True,
        )
        if p.returncode != 0:
            raise OSError("curl exit %d: %s"
                          % (p.returncode, p.stderr.decode("utf-8", "replace").strip()))
        return p.stdout.decode("utf-8", errors="replace")

    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def to_text(raw_html):
    """Reduce a canada.ca page to the plain text of its main content area."""
    h = raw_html
    m = re.search(r"<main\b[^>]*>(.*?)</main>", h, re.S | re.I)
    if m:
        h = m.group(1)
    h = re.sub(r"<(script|style|noscript)\b.*?</\1>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<nav\b.*?</nav>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<(br|/p|/div|/li|/h[1-6]|/tr|/table|/ul|/ol|/blockquote|/section)\b[^>]*>",
               "\n", h, flags=re.I)
    h = re.sub(r"<(p|li|h[1-6]|tr|div|blockquote|section)\b[^>]*>", "\n", h, flags=re.I)
    h = re.sub(r"<(td|th)\b[^>]*>", " | ", h, flags=re.I)
    h = re.sub(r"<[^>]+>", "", h)
    h = html.unescape(h)
    h = re.sub(r"[ \t\xa0]+", " ", h)
    h = re.sub(r" *\n *", "\n", h)
    h = re.sub(r"\n{3,}", "\n\n", h)
    return h.strip()


def grab(base, pages, outdir, label):
    os.makedirs(outdir, exist_ok=True)
    ok = failed = 0
    for name in pages:
        url = "%s/%s.html" % (base, name)
        try:
            text = to_text(fetch(url))
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            print("  FAIL  %-38s %s" % (name, e))
            failed += 1
            continue
        with open(os.path.join(outdir, name + ".txt"), "w", encoding="utf-8") as fh:
            fh.write(text)
        print("  ok    %-38s %6d chars" % (name, len(text)))
        ok += 1
        time.sleep(0.3)          # be polite to canada.ca
    print("%s: %d fetched, %d failed\n" % (label, ok, failed))
    return failed


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "sources"
    print("Fetching Discover Canada chapters -> %s/text/" % out)
    f1 = grab(GUIDE_BASE, GUIDE_PAGES, os.path.join(out, "text"), "Guide")

    print("Fetching IRCC citizenship-test pages -> %s/examtext/" % out)
    f2 = grab(TEST_BASE, TEST_PAGES, os.path.join(out, "examtext"), "Test pages")

    if f1 or f2:
        print("Some pages could not be fetched. Do NOT fall back to memory - "
              "fix the fetch or report the failure.")
        return 1
    print("All sources fetched. Now run:  python factcheck.py %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
