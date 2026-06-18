"""Export Phase 37 Replay / Simulation candidates for strict external audit."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-11"
PHASE = "37"
TASK_ID = "CEK-TA-425"
PARTITION = "KB_05_REPLAY_SIMULATION"
TREE_NODE = "kt.replay_simulation"
PACKAGE_ID = "phase37_replay_simulation_candidate_audit_package_20260611"

CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
AUDIT_PACKAGE = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
PACKAGE_GATE = resolve_repo_path("docs", "reports", "phase37_replay_simulation_candidate_audit_package_quality_gate.json", start_file=__file__)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_candidates() -> list[dict[str, Any]]:
    candidates = []
    for path in sorted(CAND_DIR.glob("cand_20260611_phase37_replay_simulation_*.json")):
        data = read_json(path)
        if (
            data.get("status", {}).get("ingestion_decision") == "candidate_ready"
            and data.get("workflow", {}).get("stage") == "pending_external_audit"
        ):
            candidates.append(data)
    return candidates


def package_quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    if len(candidates) != 12:
        failures.append(f"expected 12 candidate_ready candidates, got {len(candidates)}")
    ids = [item.get("candidate_id") for item in candidates]
    if len(ids) != len(set(ids)):
        failures.append("duplicate candidate_id detected")
    expected_tasks = {f"P37-F-R{idx:02d}" for idx in range(1, 13)}
    actual_tasks = {str(item.get("research_task_id")) for item in candidates}
    if actual_tasks != expected_tasks:
        failures.append(f"unexpected research_task_id set: {sorted(actual_tasks ^ expected_tasks)}")
    for item in candidates:
        cid = item.get("candidate_id", "<unknown>")
        if item.get("classification", {}).get("partition_id") != PARTITION:
            failures.append(f"{cid}: partition_id mismatch")
        if item.get("classification", {}).get("canonical_node_id") != TREE_NODE:
            failures.append(f"{cid}: canonical_node_id mismatch")
        if item.get("status", {}).get("review_status") != "candidate_ready":
            failures.append(f"{cid}: review_status is not candidate_ready")
        if item.get("status", {}).get("ingestion_decision") != "candidate_ready":
            failures.append(f"{cid}: ingestion_decision is not candidate_ready")
        if item.get("workflow", {}).get("stage") != "pending_external_audit":
            failures.append(f"{cid}: workflow.stage is not pending_external_audit")
        if item.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append(f"{cid}: default guidance must be deny")
        if item.get("machine_gate", {}).get("approved_allowed") is not False:
            failures.append(f"{cid}: approved_allowed must be false")
        if item.get("machine_gate", {}).get("hard_gate_allowed") is not False:
            failures.append(f"{cid}: hard_gate_allowed must be false")
        if len(item.get("source_refs", [])) < 3:
            failures.append(f"{cid}: source_refs < 3")
        if item.get("source_quality", {}).get("primary_source_count", 0) < 1:
            failures.append(f"{cid}: primary_source_count < 1")
        blob = json.dumps(item, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake detected")
        if re.search(r"\b(api_key|secret|private_key|password)\b", blob, flags=re.IGNORECASE):
            failures.append(f"{cid}: possible secret/private field detected")
    warnings.append("本包只审计 candidate；不得直接创建 reviewed、approved、default guidance 或 hard gate。")
    warnings.append("Replay / Simulation 知识只约束模拟、回放、成交、延迟、交易所规则和 gap report 边界，不得证明任何策略盈利。")
    return {
        "gate_id": "phase37_replay_simulation_candidate_audit_package_quality_gate",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "package_id": PACKAGE_ID,
        "candidate_count": len(candidates),
        "expected_count": 12,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": warnings,
    }


def build_package(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": PACKAGE_ID,
        "created_at": TODAY,
        "created_by": "codex",
        "phase": PHASE,
        "task_id": TASK_ID,
        "scope": {
            "branch": "Trading Engineering",
            "partition_id": PARTITION,
            "tree_node_id": TREE_NODE,
            "batch": "P37-F Replay / Simulation / 回放与模拟",
            "candidate_count": len(candidates),
            "target": "审计回放与模拟本体知识候选，包括事件时钟、同根 K TP/SL、fill model、partial fill、latency、paper/live gap、交易所规则、最小下单量、拒单/撤单、tick replay 和执行成本一致性。",
        },
        "hard_boundaries": {
            "candidate_not_formal": True,
            "accepted_for_draft_not_reviewed": True,
            "reviewed_not_approved": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "must_not_create_formal_knowledge": True,
            "must_not_generate": ["买卖点", "仓位", "杠杆", "止损止盈参数", "实盘执行建议"],
        },
        "audit_instructions": [
            "必须搜索相关的专业网站、论文、官方文档、资料、案例和数据，对本审计包进行严格审计。",
            "逐条检查来源是否足以支撑 claim，平台/框架/交易所文档不得被过度泛化。",
            "检查是否正确归类到 Trading Engineering / Replay Simulation，不得混入 Backtest、Live Execution、Risk Management 或 AI Engineering 本体。",
            "检查每条候选是否清楚声明适用范围、不适用场景、假设、限制、来源质量和 AI 使用边界。",
            "重点审计事件时钟、OHLC 同根 K TP/SL 顺序、fill model、partial fill、latency、paper/live gap、交易所规则、最小下单量、拒单/撤单和 tick replay 边界。",
            "检查是否有中文乱码、mock/test 污染、项目私有策略参数、账户事实、密钥或实盘敏感信息。",
            "输出只能是 accepted_for_draft、needs_more_evidence、rejected 或 blocked；不得输出 reviewed、approved、default guidance 或 hard gate。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "auditor": "string",
            "audited_at": "YYYY-MM-DD",
            "package_id": PACKAGE_ID,
            "summary": {
                "total": 12,
                "accepted_for_draft": 0,
                "needs_more_evidence": 0,
                "rejected": 0,
                "blocked": 0,
            },
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | high",
                    "reviewed_allowed": False,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "reasons": ["string"],
                    "required_followups": ["string"],
                    "patch_notes": {
                        "source": ["string"],
                        "content": ["string"],
                        "boundary": ["string"],
                        "conflict": ["string"],
                    },
                    "source_assessment": {
                        "source_count": 0,
                        "missing_sources": ["string"],
                        "weak_sources": ["string"],
                        "recommended_extra_sources": ["string"],
                    },
                    "classification_assessment": {
                        "is_correct_branch": True,
                        "expected_branch": "Trading Engineering / Replay Simulation",
                        "misplaced_topics": ["string"],
                    },
                }
            ],
        },
        "quality_gate": gate,
        "candidates": candidates,
    }


def main() -> int:
    candidates = load_candidates()
    gate = package_quality_gate(candidates)
    package = build_package(candidates, gate)
    write_json(PACKAGE_GATE, gate)
    write_json(AUDIT_PACKAGE, package)
    print(json.dumps({"status": gate["gate_status"], "candidate_count": len(candidates), "audit_package": str(AUDIT_PACKAGE)}, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
