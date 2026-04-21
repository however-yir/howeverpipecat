#!/usr/bin/env python3
#
# Copyright (c) 2026, however-yir
#
# SPDX-License-Identifier: BSD 2-Clause License
#

"""Lightweight naming checks for however fork conventions."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _fail(msg: str) -> None:
    print(f"[naming-lint] {msg}", file=sys.stderr)


def check_new_script_prefix() -> bool:
    ok = True
    required_prefix_scripts = [
        "however_service_health.py",
        "however_set_repo_metadata.sh",
        "however_naming_lint.py",
        "however_secrets_scan.sh",
        "however_dependency_security_scan.sh",
        "however_dependency_baseline.sh",
    ]
    for rel in required_prefix_scripts:
        if not (ROOT / "scripts" / rel).exists():
            _fail(f"missing required script: scripts/{rel}")
            ok = False
    return ok


def check_env_prefix() -> bool:
    ok = True
    env_file = ROOT / "env.however.example"
    content = env_file.read_text(encoding="utf-8")
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key = stripped.split("=", 1)[0]
        allowed = (
            key.startswith("HOWEVER_")
            or key.endswith("_API_KEY")
            or key in {"OPENAI_API_KEY", "DEEPGRAM_API_KEY", "CARTESIA_API_KEY"}
        )
        if not allowed:
            _fail(f"unexpected env key in env.however.example: {key}")
            ok = False
    return ok


def check_ollama_naming() -> bool:
    ok = True
    target = ROOT / "src/pipecat/services/ollama/llm.py"
    text = target.read_text(encoding="utf-8")
    if "class OllamaLLMService" not in text:
        _fail("class OllamaLLMService not found")
        ok = False
    # Legacy alias is allowed, but only as class declaration and warning text.
    offenders = []
    for idx, line in enumerate(text.splitlines(), start=1):
        if "OLLamaLLMService" in line:
            if (
                line.strip().startswith("class OLLamaLLMService")
                or "OLLamaLLMService is deprecated" in line
                or "from pipecat.services.ollama.llm import OLLamaLLMService" in line
                or "Use ``settings=OllamaLLMService.Settings" in line
            ):
                continue
            offenders.append(idx)
    if offenders:
        _fail(f"unexpected OLLamaLLMService references at lines: {offenders}")
        ok = False
    return ok


def check_release_tag_pattern_documented() -> bool:
    ok = True
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "vX.Y.Z-however.N" not in readme:
        _fail("release naming rule vX.Y.Z-however.N not found in README")
        ok = False
    return ok


def main() -> int:
    checks = [
        check_new_script_prefix(),
        check_env_prefix(),
        check_ollama_naming(),
        check_release_tag_pattern_documented(),
    ]
    if all(checks):
        print("[naming-lint] ok")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
