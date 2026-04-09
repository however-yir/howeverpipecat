#
# Copyright (c) 2026, however-yir
#
# SPDX-License-Identifier: BSD 2-Clause License
#

"""Health-check helpers for however runtime dependencies."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import socket
import time

from pipecat.utils.however_runtime_config import HoweverRuntimeConfig, load_however_runtime_config


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    detail: str
    latency_ms: int
    fault_type: str

    @property
    def ok(self) -> bool:
        return self.status == "ok"


def _parse_host_port(url: str, default_port: int) -> tuple[str, int]:
    parsed = urlparse(url)
    return parsed.hostname or "127.0.0.1", parsed.port or default_port


def _fault_type_from_error(name: str, detail: str) -> str:
    lowered = detail.lower()
    if "401" in lowered or "403" in lowered or "unauthorized" in lowered or "forbidden" in lowered:
        return "auth_error"
    if "connection refused" in lowered or "timed out" in lowered or "name or service not known" in lowered:
        return "network_error"
    if "invalid" in lowered or "must use one of" in lowered:
        return "config_error"
    if name in ("postgres", "redis", "ollama", "telemetry"):
        return "network_error"
    return "unknown_error"


def _check_tcp(name: str, host: str, port: int, timeout_s: float) -> CheckResult:
    start = time.monotonic()
    try:
        with socket.create_connection((host, port), timeout=timeout_s):
            latency = int((time.monotonic() - start) * 1000)
            return CheckResult(name=name, status="ok", detail=f"connected {host}:{port}", latency_ms=latency, fault_type="none")
    except OSError as exc:
        latency = int((time.monotonic() - start) * 1000)
        detail = f"{host}:{port} - {exc}"
        return CheckResult(
            name=name,
            status="fail",
            detail=detail,
            latency_ms=latency,
            fault_type=_fault_type_from_error(name, detail),
        )


def _check_http(name: str, url: str, timeout_s: float) -> CheckResult:
    start = time.monotonic()
    try:
        req = Request(url=url, method="GET")
        with urlopen(req, timeout=timeout_s) as resp:
            latency = int((time.monotonic() - start) * 1000)
            if 200 <= resp.status < 400:
                return CheckResult(name=name, status="ok", detail=f"http {resp.status} {url}", latency_ms=latency, fault_type="none")
            detail = f"http {resp.status} {url}"
            return CheckResult(
                name=name,
                status="fail",
                detail=detail,
                latency_ms=latency,
                fault_type=_fault_type_from_error(name, detail),
            )
    except OSError as exc:
        latency = int((time.monotonic() - start) * 1000)
        detail = f"{url} - {exc}"
        return CheckResult(
            name=name,
            status="fail",
            detail=detail,
            latency_ms=latency,
            fault_type=_fault_type_from_error(name, detail),
        )


def run_however_checks(
    cfg: HoweverRuntimeConfig | None = None,
    *,
    skip_network: bool = False,
) -> tuple[dict[str, object], list[CheckResult]]:
    resolved_cfg = cfg or load_however_runtime_config()
    if skip_network:
        checks = [
            CheckResult("postgres", "ok", "skipped", 0, "none"),
            CheckResult("redis", "ok", "skipped", 0, "none"),
            CheckResult("ollama", "ok", "skipped", 0, "none"),
            CheckResult("telemetry", "ok", "skipped", 0, "none"),
        ]
    else:
        timeout_s = resolved_cfg.startup_check_timeout_ms / 1000.0
        db_host, db_port = _parse_host_port(resolved_cfg.db_url, 5432)
        redis_host, redis_port = _parse_host_port(resolved_cfg.redis_url, 6379)
        ollama_url = f"{resolved_cfg.ollama_base_url.rstrip('/')}/api/tags"
        checks = [
            _check_tcp("postgres", db_host, db_port, timeout_s),
            _check_tcp("redis", redis_host, redis_port, timeout_s),
            _check_http("ollama", ollama_url, timeout_s),
            _check_http("telemetry", resolved_cfg.telemetry_endpoint, timeout_s),
        ]

    payload = {
        "env": resolved_cfg.env,
        "region": resolved_cfg.region,
        "strict_startup_checks": resolved_cfg.strict_startup_checks,
    }
    return payload, checks


def build_however_health_result(
    cfg: HoweverRuntimeConfig | None = None,
    *,
    skip_network: bool = False,
) -> dict[str, object]:
    meta, checks = run_however_checks(cfg, skip_network=skip_network)
    all_ok = all(item.ok for item in checks)
    result = {
        **meta,
        "all_ok": all_ok,
        "checks": [asdict(item) for item in checks],
    }
    return result
