from pathlib import Path

import pytest

from pipecat.utils.however_runtime_config import load_however_runtime_config


def test_load_however_runtime_config_defaults(tmp_path: Path):
    cfg = load_however_runtime_config(
        env_path=tmp_path / ".env.missing",
        environ={},
    )
    assert cfg.env == "dev"
    assert cfg.region == "local"
    assert cfg.db_url.startswith("postgresql://")
    assert cfg.redis_url.startswith("redis://")
    assert cfg.ollama_base_url.startswith("http")
    assert cfg.startup_check_timeout_ms == 1500


def test_load_however_runtime_config_env_override(tmp_path: Path):
    cfg = load_however_runtime_config(
        env_path=tmp_path / ".env.missing",
        environ={
            "HOWEVER_ENV": "staging",
            "HOWEVER_REGION": "cn-sh",
            "HOWEVER_DB_URL": "postgresql://hc:pw@db.internal.example:5432/hc",
            "HOWEVER_REDIS_URL": "redis://redis.internal.example:6380/1",
            "HOWEVER_OLLAMA_BASE_URL": "http://ollama.internal.example:11434/v1",
            "HOWEVER_TELEMETRY_ENDPOINT": "https://telemetry.internal.example/events",
            "HOWEVER_STARTUP_CHECK_TIMEOUT_MS": "2800",
            "HOWEVER_STRICT_STARTUP_CHECKS": "false",
        },
    )
    assert cfg.env == "staging"
    assert cfg.region == "cn-sh"
    assert cfg.startup_check_timeout_ms == 2800
    assert cfg.strict_startup_checks is False


def test_load_however_runtime_config_rejects_invalid_url(tmp_path: Path):
    with pytest.raises(ValueError):
        load_however_runtime_config(
            env_path=tmp_path / ".env.missing",
            environ={
                "HOWEVER_DB_URL": "sqlite:///tmp/demo.db",
            },
        )
