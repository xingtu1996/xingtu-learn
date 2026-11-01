#!/usr/bin/env python3
"""Semantica 小图谱实验：合成数据、无云端 LLM、无数据库依赖。
本脚本依据官方 ContextGraph 文档编写；首次提交时尚未在用户本机验证。
参见 https://docs.getsemantica.ai/reference/context/
"""
from __future__ import annotations

import json
from pathlib import Path

from semantica.context import ContextGraph
from run_baseline import evaluate

ROOT = Path(__file__).resolve().parent


def main() -> None:
    data = json.loads((ROOT / "data" / "requirements.json").read_text(encoding="utf-8"))
    graph = ContextGraph(advanced_analytics=False)
    for item in data["cases"]:
        case_id = item["id"]
        graph.add_node(case_id, "requirement", properties={"title": item["title"]})
        release_id = case_id + ":release"
        graph.add_node(release_id, "release_candidate", properties={"at": item["release_at"]})
        graph.add_edge(case_id, release_id, "has_candidate_release")
        for index, approval in enumerate(item["approvals"]):
            approval_id = case_id + ":approval:" + str(index)
            graph.add_node(approval_id, "approval", properties=approval)
            graph.add_edge(case_id, approval_id, "has_approval")
        for index, test in enumerate(item["tests"]):
            test_id = case_id + ":test:" + str(index)
            graph.add_node(test_id, "test_result", properties=test)
            graph.add_edge(case_id, test_id, "has_test_result")
        verdict = evaluate(item)  # 同一基线规则；不是宣称 Semantica 自动完成核验
        graph.record_decision(
            category="synthetic_release_gate",
            scenario="Release candidate for " + case_id,
            reasoning="Rule-based evaluation; evidence must be separately authenticated",
            outcome=verdict["actual"],
            confidence=1.0,
            entities=[case_id],
            decision_maker="example_rule_engine",
        )
        assert verdict["match"], verdict

    output_dir = ROOT / "output"
    output_dir.mkdir(exist_ok=True)
    graph_path = output_dir / "context_graph.json"
    graph.save_to_file(str(graph_path))
    restored = ContextGraph(advanced_analytics=False)
    restored.load_from_file(str(graph_path))
    assert restored.find_node("R-001") is not None, "graph restore failed"
    print(json.dumps({
        "cases": len(data["cases"]),
        "graph_stats": graph.stats(),
        "restored_stats": restored.stats(),
        "saved_to": str(graph_path),
        "note": "This example uses the baseline policy, not a Semantica policy engine.",
    }, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
