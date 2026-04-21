#!/usr/bin/env python3
#
# Copyright (c) 2026, however-yir
#
# SPDX-License-Identifier: BSD 2-Clause License
#

"""Health check for local however Pipecat service dependencies."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from pipecat.utils.however_health import build_however_health_result
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from pipecat.utils.however_health import build_however_health_result


def main() -> int:
    parser = argparse.ArgumentParser(description="however Pipecat service health check")
    parser.add_argument("--skip-network", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_however_health_result(skip_network=args.skip_network)
    all_ok = bool(result["all_ok"])

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for item in result["checks"]:
            status = "OK" if item["status"] == "ok" else "FAIL"
            print(
                f"[{status}] {item['name']:9} {item['latency_ms']:4d}ms "
                f"{item['detail']} fault_type={item['fault_type']}"
            )
        print(f"all_ok={all_ok} strict_startup_checks={result['strict_startup_checks']}")

    if result["strict_startup_checks"] and not all_ok:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
