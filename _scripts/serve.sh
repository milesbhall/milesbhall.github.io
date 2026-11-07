#!/usr/bin/env bash
# Local preview at http://localhost:4000 that never writes into this project folder.
# The built site goes to a temp folder instead of ./_site, and the disk cache is off,
# so nothing in the repo is created, deleted, or overwritten.
#
# Usage:  _scripts/serve.sh      (Ctrl+C to stop)

set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
export PATH="/opt/homebrew/lib/ruby/gems/4.0.0/bin:/opt/homebrew/opt/ruby/bin:$PATH"

OUT="${TMPDIR:-/tmp}/personal-website-preview"
echo "Building to $OUT (outside the project)"
exec jekyll serve --livereload --port 4000 --destination "$OUT" --disable-disk-cache
