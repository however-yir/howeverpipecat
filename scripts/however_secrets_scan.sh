#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[secrets-scan] scanning tracked files for common secret patterns"

# Exclude generated/virtualenv folders and lockfiles with hashes.
EXCLUDES=(
  ".venv-test"
  ".git"
  "uv.lock"
)

RG_ARGS=()
for item in "${EXCLUDES[@]}"; do
  RG_ARGS+=("-g" "!${item}/**")
done

PATTERN='(AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,}|AIza[0-9A-Za-z\\-_]{35}|-----BEGIN (RSA|EC|OPENSSH|DSA) PRIVATE KEY-----)'

if rg -n -S "${RG_ARGS[@]}" "$PATTERN" .; then
  echo "[secrets-scan] potential secret detected; please rotate and remove." >&2
  exit 1
fi

echo "[secrets-scan] no high-risk secret pattern found"
