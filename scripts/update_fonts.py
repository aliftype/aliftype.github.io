#!/usr/bin/env python3
"""Sync the font versions and assets with the upstream releases.

Asks GitHub for the latest release of every font in _data/config.yml, then
updates the version, the fonts under assets/fonts and the documentation pages
to match it.
"""

import argparse
import contextlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

import yaml

# Missing releases and missing archives are skipped; anything else, a rate
# limit or no network, would leave a font quietly behind.
MISSING = ("release not found", "no assets match the file pattern")


def gh(*args):
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout
    if any(reason in result.stderr for reason in MISSING):
        return None
    raise SystemExit(f"gh {' '.join(args)}: {result.stderr.strip()}")


def latest_release(font):
    out = gh("release", "view", "--repo", f"aliftype/{font}", "--json", "tagName")
    return json.loads(out)["tagName"] if out else None


@contextlib.contextmanager
def release_files(font, config, release):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        asset = f"{config['name']}-{release.lstrip('v')}.zip"
        if gh("release", "download", release, "--repo", f"aliftype/{font}",
              "--pattern", asset, "--dir", str(tmp)) is None:
            yield None
            return
        with zipfile.ZipFile(tmp / asset) as archive:
            archive.extractall(tmp)
        yield tmp


def set_version(text, font, version):
    text, replaced = re.subn(
        rf'(?m)^(\s*version: )"[^"]*"(\s*#\s*{re.escape(font)}\s*)$',
        rf'\g<1>"{version}"\g<2>',
        text,
    )
    if replaced != 1:
        raise SystemExit(
            f"{font}: expected one version line marked '# {font}', found {replaced}"
        )
    return text


def sync(font, config, release, paths, changed, notes):
    docs = paths.root / font / "documentation"
    with release_files(font, config, release) as files:
        if files is None:
            notes.append(f"{config['name']}: no archive in `{release}`, skipped")
            return
        for source in sorted(files.rglob("*")):
            if source.is_dir():
                continue
            for target in (paths.fonts / source.name, docs / source.name):
                if not target.exists():
                    continue
                if target.read_bytes() == source.read_bytes():
                    continue
                shutil.copyfile(source, target)
                changed.append(target.relative_to(paths.root))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=pathlib.Path, required=True,
                        help="the site, holding the per font documentation")
    parser.add_argument("--config", type=pathlib.Path, required=True,
                        help="the yaml listing the fonts")
    parser.add_argument("--fonts", type=pathlib.Path, required=True,
                        help="where the font files live")
    parser.add_argument("--summary", type=pathlib.Path, help="write a report here")
    args = parser.parse_args()

    original = args.config.read_text(encoding="utf-8")
    text = original
    config = yaml.safe_load(text)
    changed, notes, bumped = [], [], []

    for font, entry in config.items():
        release = latest_release(font)
        if release is None:
            continue
        version = release.lstrip("v")
        sync(font, entry, release, args, changed, notes)
        if version != str(entry["version"]):
            text = set_version(text, font, version)
            bumped.append(f"{entry['name']} {entry['version']} → {version}")

    if text != original:
        args.config.write_text(text, encoding="utf-8")
        changed.append(args.config.relative_to(args.root))

    report = []
    if bumped:
        report += ["Released:", *(f"- {line}" for line in bumped), ""]
    report += ["Updated:", *(f"- `{p}`" for p in changed)] if changed else ["Nothing to update."]
    if notes:
        report += ["", "Notes:", *(f"- {note}" for note in notes)]
    report = "\n".join(report)

    print(report)
    if args.summary:
        args.summary.write_text(report + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
