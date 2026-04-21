#
# Copyright (c) 2026, however-yir
#
# SPDX-License-Identifier: BSD 2-Clause License
#

"""Runtime config helpers for however Pipecat deployments."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping
from urllib.parse import urlparse


def _parse_env_file(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def _to_bool(value: str | bool | None, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return value.strip().lower() in ("1", "true", "yes", "on")


def _validate_url(name: str, value: str, allowed_schemes: tuple[str, ...]) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in allowed_schemes or not parsed.hostname:
        allowed = ", ".join(allowed_schemes)
        raise ValueError(f"{name} must use one of [{allowed}] and include host: {value}")
    return value


def _pick(
    key: str,
    default: str,
    env_vars: Mapping[str, str],
    env_file_vars: Mapping[str, str],
) -> str:
    if key in env_vars and env_vars[key]:
        return env_vars[key]
    if key in env_file_vars and env_file_vars[key]:
        return env_file_vars[key]
    return default


@dataclass(frozen=True)
class HoweverRuntimeConfig:
    """Normalized runtime configuration for however Pipecat services."""

    env: str
    region: str
    db_url: str
    redis_url: str
    ollama_base_url: str
    telemetry_endpoint: str
    strict_startup_checks: bool
    startup_check_timeout_ms: int


def load_however_runtime_config(
    env_path: str | Path = ".env.however.local",
    environ: Mapping[str, str] | None = None,
) -> HoweverRuntimeConfig:
    """Load local deployment config from env and optional env file."""
    path_env = Path(env_path)
    file_env = _parse_env_file(path_env)
    env_vars = dict(os.environ if environ is None else environ)

    timeout_raw = _pick(
        "HOWEVER_STARTUP_CHECK_TIMEOUT_MS",
        "1500",
        env_vars=env_vars,
        env_file_vars=file_env,
    )
    try:
        timeout_ms = int(timeout_raw)
    except ValueError:
        timeout_ms = 1500
    timeout_ms = min(max(timeout_ms, 100), 30000)

    cfg = HoweverRuntimeConfig(
        env=_pick("HOWEVER_ENV", "dev", env_vars=env_vars, env_file_vars=file_env),
        region=_pick("HOWEVER_REGION", "local", env_vars=env_vars, env_file_vars=file_env),
        db_url=_validate_url(
            "HOWEVER_DB_URL",
            _pick(
                "HOWEVER_DB_URL",
                "postgresql://hc_user:change_me@postgres.internal.example:5432/howeverpipecat",
                env_vars=env_vars,
                env_file_vars=file_env,
            ),
            allowed_schemes=("postgresql", "postgres"),
        ),
        redis_url=_validate_url(
            "HOWEVER_REDIS_URL",
            _pick(
                "HOWEVER_REDIS_URL",
                "redis://redis.internal.example:6379/0",
                env_vars=env_vars,
                env_file_vars=file_env,
            ),
            allowed_schemes=("redis", "rediss"),
        ),
        ollama_base_url=_validate_url(
            "HOWEVER_OLLAMA_BASE_URL",
            _pick(
                "HOWEVER_OLLAMA_BASE_URL",
                "http://ollama.internal.example:11434/v1",
                env_vars=env_vars,
                env_file_vars=file_env,
            ),
            allowed_schemes=("http", "https"),
        ),
        telemetry_endpoint=_validate_url(
            "HOWEVER_TELEMETRY_ENDPOINT",
            _pick(
                "HOWEVER_TELEMETRY_ENDPOINT",
                "https://telemetry.internal.example/pipecat/events",
                env_vars=env_vars,
                env_file_vars=file_env,
            ),
            allowed_schemes=("http", "https"),
        ),
        strict_startup_checks=_to_bool(
            _pick(
                "HOWEVER_STRICT_STARTUP_CHECKS",
                "true",
                env_vars=env_vars,
                env_file_vars=file_env,
            ),
            True,
        ),
        startup_check_timeout_ms=timeout_ms,
    )
    return cfg
