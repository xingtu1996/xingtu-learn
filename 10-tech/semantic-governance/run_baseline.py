#!/usr/bin/env python3
"""标准库基线：不是 Semantica 性能测试。仅对模拟审批数据进行确定性校验。"""
from __future__ import annotations

import json
import sys
import time
import tracemalloc
from datetime import datetime
from pathlib import Path


def evaluate(item: dict) -> dict:
    reasons = []
    approvals = item.get("approvals", [])
    tests = item.get("tests", [])
    release_at = datetime.fromisoformat(item["release_at"])

    statuses = {a.get("status") for a in approvals}
    if len(statuses) > 1:
        reasons.append("approval_conflict")
    eligible = [
        a for a in approvals
        if a.get("status") == "approved"
        and a.get("source_id")
        and datetime.fromisoformat(a["at"]) <= release_at
    ]
    if not eligible:
        reasons.append("no_proven_pre_release_approval")
    if not tests or any(
        t.get("status") != "passed" or not t.get("source_id")
        for t in tests
    ):
        reasons.append("test_missing_failed_or_unproven")

    actual = "block" if reasons else "allow"
    return {
        "id": item["id"],
        "actual": actual,
        "expected": item["expected"],
        "match": actual == item["expected"],
        "reasons": reasons,
    }


def main() -> int:
    path = Path(__file__).resolve().parent / "data" / "requirements.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    tracemalloc.start()
    started = time.perf_counter()
    results = [evaluate(item) for item in data["cases"]]
    elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
    peak_python_kib = round(tracemalloc.get_traced_memory()[1] / 1024, 1)
    tracemalloc.stop()

    print(json.dumps({
        "dataset": str(path.name),
        "total": len(results),
        "correct": sum(r["match"] for r in results),
        "elapsed_ms": elapsed_ms,
        "peak_python_kib_tracemalloc": peak_python_kib,
        "results": results,
    }, ensure_ascii=False, indent=2))
    return 0 if all(r["match"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
