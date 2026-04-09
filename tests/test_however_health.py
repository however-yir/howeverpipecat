from pipecat.utils.however_health import build_however_health_result


def test_however_health_offline_payload_shape():
    result = build_however_health_result(skip_network=True)
    assert result["all_ok"] is True
    assert result["env"] == "dev"
    assert result["region"] == "local"
    checks = result["checks"]
    assert len(checks) == 4
    for item in checks:
        assert item["status"] == "ok"
        assert item["fault_type"] == "none"
