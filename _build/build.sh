#!/usr/bin/env bash
# Rebuild upliftavtech.com from the sources in _build/ and write the output to the repo root.
# Usage:  bash _build/build.sh            (publishes posts dated today or earlier, America/New_York)
#         BUILD_DATE=2026-11-03 bash _build/build.sh   (preview a future date)
# Then:   git add -A && git commit -m "..." && git push   (Cloudflare deploys main automatically)
#         python3 _build/indexnow.py       (after the deploy is live: notify Bing/Yahoo/DuckDuckGo)
set -euo pipefail
R="$(cd "$(dirname "$0")/.." && pwd)"
W="$(mktemp -d)"
cp "$R"/_build/*.py "$R"/_build/site.css "$W"/
cp -r "$R"/images "$W"/images
cp -r "$R"/fonts "$W"/fonts
python3 -c "import markdown" 2>/dev/null || pip install -q --break-system-packages markdown
(cd "$W" && python3 gen.py)
mkdir -p "$W"/out/images "$W"/out/fonts
cp "$W"/images/* "$W"/out/images/
cp "$W"/fonts/* "$W"/out/fonts/
cp -r "$W"/out/* "$R"/
rm -rf "$W"
echo "Built into $R"
