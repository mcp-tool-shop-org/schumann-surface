#!/usr/bin/env bash
# verify: test + build + smoke in one command. Exit 0 = ship-ready for this checkout.
set -euo pipefail
cd "$(dirname "$0")"

echo "== tests"
python -m pytest -q tests

echo "== version matches CHANGELOG"
v=$(grep -E '^version = "' pyproject.toml | sed -E 's/version = "([^"]+)"/\1/')
grep -q "## \[$v\]" CHANGELOG.md || { echo "CHANGELOG has no entry for $v"; exit 1; }

echo "== viewer template is a complete page"
grep -q '/\*__DATA__\*/null' viewer/template.html || { echo "template lost its data hook"; exit 1; }

if [ -f data/derived/SN_1310_0.npz ]; then
  echo "== build (Oct 2013 present)"
  python scripts/build_viewer.py 1310 --main >/dev/null
  test -s viewer/index.html
else
  echo "== build skipped (no derived month in this checkout; run the pipeline first)"
fi

if [ -d site ]; then
  echo "== site build"
  (cd site && npm run build --silent)
  test -f site/dist/index.html
fi

echo "verify: OK ($v)"
