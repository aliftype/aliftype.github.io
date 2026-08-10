#!/bin/sh
# Bring the fonts in line with the upstream releases: versions, whole fonts and
# documentation from the release archives, web fonts subset to the characters
# the site renders and compressed with woff2_compress.
#
# Writes a combined report to $1 if given. Needs python with the requirements
# installed, playwright's chromium, and woff2_compress on PATH.
set -eu

root=$(cd "$(dirname "$0")/.." && pwd)
build=$(mktemp -d)
trap 'rm -rf "$build"' EXIT

config="$root/_data/config.yml"
fonts="$root/assets/fonts"

python3 "$root/scripts/update_fonts.py" \
    --root "$root" --config "$config" --fonts "$fonts" \
    --summary "$build/update.md"
python3 "$root/scripts/subset_fonts.py" \
    --config "$config" --fonts "$fonts" --settings "$root/publishconf.py" \
    --output "$build/fonts"

for font in "$build"/fonts/*.ttf; do
    [ -e "$font" ] || continue
    woff2_compress "$font" >/dev/null
    cp "${font%.ttf}.woff2" "$fonts/"
done

# Which web fonts the subsetting actually changed, as opposed to rewrote.
report() {
    cat "$build/update.md"
    subset=$(git -C "$root" status --porcelain -- "$fonts" | awk '{print $2}' | grep '\.woff2$' || true)
    if [ -n "$subset" ]; then
        echo
        echo "Subset:"
        echo "$subset" | sed 's|^|- `|; s|$|`|'
    fi
}

if [ $# -gt 0 ]; then
    report > "$1"
else
    report
fi
