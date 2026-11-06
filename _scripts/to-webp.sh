#!/usr/bin/env bash
# Converts every JPG/PNG under assets/images/ to WebP, deletes the original,
# and rewrites references to them across the site's source files.
#
# Usage:  _scripts/to-webp.sh            (run from anywhere in the repo)
# Needs:  cwebp  ->  brew install webp
#
# Safe to re-run: files that are already WebP are left alone.
# Originals stay recoverable from git history.

set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

command -v cwebp >/dev/null || { echo "cwebp not found. Run: brew install webp" >&2; exit 1; }

QUALITY=82   # lossy quality for photos (JPG); PNGs are encoded losslessly

converted=0
while IFS= read -r -d '' src; do
  out="${src%.*}.webp"
  case "${src##*.}" in
    png|PNG) cwebp -quiet -lossless -m 6 "$src" -o "$out" ;;
    *)       cwebp -quiet -q "$QUALITY" -m 6 "$src" -o "$out" ;;
  esac
  before=$(stat -f%z "$src"); after=$(stat -f%z "$out")
  printf '%-60s %7d -> %7d bytes\n' "$src" "$before" "$after"
  rm "$src"
  converted=$((converted + 1))
done < <(find assets/images -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \) -print0)

# Rewrite /assets/images/....jpg|jpeg|png -> .webp in source files
# (this includes commented-out placeholders, so they're ready when you add those images).
find . \( -path ./.git -o -path ./_site -o -path ./_reference -o -path ./node_modules -o -path ./.jekyll-cache \) -prune -o \
  -type f \( -name '*.html' -o -name '*.md' -o -name '*.css' -o -name '*.scss' -o -name '*.yml' -o -name '*.yaml' -o -name '*.json' -o -name '*.js' \) -print0 |
  xargs -0 grep -lE 'assets/images/[^"'"'"')[:space:]]+\.(jpe?g|png)' 2>/dev/null |
  while IFS= read -r f; do
    perl -pi -e 's{(assets/images/[^"\x27)\s]+)\.(?:jpe?g|png)\b}{$1.webp}gi' "$f"
    echo "updated references: $f"
  done || true

echo "Done: $converted image(s) converted."
