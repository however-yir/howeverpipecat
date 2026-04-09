#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[dep-security] python3 is required" >&2
  exit 1
fi

TMP_VENV=".venv-dep-audit"
cleanup() {
  rm -rf "$TMP_VENV"
}
trap cleanup EXIT

python3 -m venv "$TMP_VENV"
source "$TMP_VENV/bin/activate"

python -m pip install -q --upgrade pip
python -m pip install -q pip-audit
python -m pip install -q -e .

echo "[dep-security] running pip-audit"
pip-audit --progress-spinner off
