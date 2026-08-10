#!/usr/bin/env python3
"""Subset the web fonts to the characters the site renders in them."""

import argparse
import contextlib
import functools
import glob
import http.server
import io
import os
import pathlib
import socketserver
import sys
import tempfile
import threading

import uharfbuzz as hb
import yaml

from update_fonts import latest_release, release_files

COLLECT = """(names) => {
  const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const found = Object.fromEntries(names.map(n => [n, ""]));
  for (let node = walk.nextNode(); node; node = walk.nextNode()) {
    const el = node.parentElement;
    if (!el || !node.nodeValue.trim()) continue;
    if (["script", "style"].includes(el.tagName.toLowerCase())) continue;
    const stack = getComputedStyle(el).fontFamily;
    for (const name of names) {
      if (new RegExp(`\\\\b${name}\\\\b`, "i").test(stack)) found[name] += node.nodeValue;
    }
  }
  return found;
}"""


@contextlib.contextmanager
def served(directory):
    """The pages need a real origin: their stylesheets are absolute paths."""

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    handler = functools.partial(Quiet, directory=str(directory))
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()


def collect(names, settings):
    """Build the site once and note which characters it renders in each family."""
    from playwright.sync_api import sync_playwright

    from pelican import main as pelican

    found = {name: set() for name in names}
    with tempfile.TemporaryDirectory() as site:
        # Quiet while it works, but say what happened if it does not.
        log = io.StringIO()
        try:
            with contextlib.redirect_stdout(log):
                pelican(["--settings", str(settings), "-o", site,
                         "--fatal", "errors", "--quiet"])
        except BaseException:
            sys.stderr.write(log.getvalue())
            raise
        # A page with no stylesheet cannot name any of these families, and the
        # redirect stubs navigate away before they finish loading.
        pages = [p for p in sorted(glob.glob(f"{site}/**/*.html", recursive=True))
                 if 'rel="stylesheet"' in pathlib.Path(p).read_text(encoding="utf-8")]
        with served(site) as base, sync_playwright() as driver:
            browser = driver.chromium.launch()
            page = browser.new_page()
            for path in pages:
                page.goto(f"{base}/{os.path.relpath(path, site)}", wait_until="load")
                for name, text in page.evaluate(COLLECT, names).items():
                    found[name] |= set(text)
            browser.close()
    return found


def subset(data, chars):
    face = hb.Face(data)
    request = hb.SubsetInput()
    request.unicode_set.set({ord(c) for c in chars})
    # Keep all features
    features = request.sets(hb.SubsetInputSets.LAYOUT_FEATURE_TAG)
    features.clear()
    features.invert()
    # Keep only user name IDs, CSS color palettes seem to require them
    names = request.sets(hb.SubsetInputSets.NAME_ID)
    names.clear()
    names.add_range(255, 0xFFFF)
    return hb.subset(face, request).blob.data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=pathlib.Path, required=True,
                        help="the yaml listing the fonts")
    parser.add_argument("--fonts", type=pathlib.Path, required=True,
                        help="the web fonts to be replaced, which say what to subset")
    parser.add_argument("--settings", type=pathlib.Path, required=True,
                        help="the pelican settings used to build the site")
    parser.add_argument("--output", type=pathlib.Path, required=True,
                        help="where to write the subset ttf files")
    parser.add_argument("--summary", type=pathlib.Path, help="write a report here")
    args = parser.parse_args()

    config = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    wanted = collect([entry["name"] for entry in config.values()], args.settings)
    args.output.mkdir(parents=True, exist_ok=True)
    written = []

    for font, entry in config.items():
        release = latest_release(font)
        if release is None:
            continue
        with release_files(font, entry, release) as files:
            if files is None:
                continue
            for source in sorted(files.rglob("*")):
                if source.suffix not in (".ttf", ".otf"):
                    continue
                if not (args.fonts / (source.stem + ".woff2")).exists():
                    continue
                target = args.output / (source.stem + ".ttf")
                target.write_bytes(subset(source.read_bytes(), wanted[entry["name"]]))
                written.append(f"`{target.name}`")

    report = ["Subset:", *(f"- {line}" for line in written)] if written else ["Nothing to subset."]
    report = "\n".join(report)
    print(report)
    if args.summary:
        args.summary.write_text(report + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
