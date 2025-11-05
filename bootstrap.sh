#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"                     # → .tools (when used as submodule)

# 1) Minimal venv létrehozása, ha hiányzik
if [[ ! -d .venv ]]; then
  echo "⚙️  Creating minimal .venv (uv venv)…"
  uv venv .venv      # szimlinkalapú, ultrakönnyű venv (UV-szabvány)
fi

# 2) Agent-tools telepítése / frissítése, CLI-extrával (colorama is)
cd agt
uv pip install -e ".[cli]"
cd ..

echo "✅  agent-tools ready in .tools/.venv (cache: ${UV_CACHE_DIR:-not set})"

