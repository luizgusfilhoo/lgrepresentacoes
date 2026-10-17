#!/bin/zsh
source /Users/luizfilho/.codex/tools/activate.sh
cd "${0:A:h}" || exit 1
npm run build || exit 1
exec python3 scripts/preview.py
