#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

OUT_DIR="reports/dependency-baseline/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT_DIR"

python3 -m pip freeze > "$OUT_DIR/pip-freeze.txt" || true
python3 -m pip list --format=freeze > "$OUT_DIR/pip-list-freeze.txt" || true
python3 --version > "$OUT_DIR/python-version.txt"

echo "Saved dependency baseline to $OUT_DIR"
