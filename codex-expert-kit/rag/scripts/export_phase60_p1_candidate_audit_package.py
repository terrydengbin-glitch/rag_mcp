"""Export Phase 60 P1 enhanced environment governance candidates for strict audit."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-17"
TASK_ID = "CEK-TA-583"
PACKAGE_ID = "phase60_p1_candidate_audit_package_20260617"
PARTITIONS = ["KB_05_REPLAY_SIMULATION", "KB_06_LIVE_EXECUTION", "KB_07_RISK_MANAGEMENT"]
EXPECTED_TASKS = {f"P60-P1-0{idx}" for idx in range(1, 7)}


def repo_path(*parts: str) -> Path:
    return resolve_repo_path(*parts, start_file=__file__)


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_candidates() -> tuple[list[dict[str, Any]], list[Path]]:
    candidates: list[dict[str, Any]] = []
    paths: list[Path] = []
    for partition in PARTITIONS:
        cand_dir = repo_path("codex-expert-kit", "rag", "candidates", partition)
        for path in sorted(cand_dir.glob("cand_20260617_phase60_p1_*.json")):
            item = read_json(path)
            if item.get("research_task_id") in EXPECTED_TASKS:
                candidates.append(item)
                paths.append(path)
    ordered = sorted(zip(candidates, paths, strict=True), key=lambda pair: str(pair[0].get("research_task_id")))
    return [item for item, _ in ordered], [path for _, path in ordered]


def package_quality_gate(candidates: list[dict[str, Any]], paths: list[Path]) -> dict[str, Any]:
    failures: list[str] = []
    actual_tasks = {str(item.get("research_task_id")) for item in candidates}
    if actual_tasks != EXPECTED_TASKS:
        failures.append(f"unexpected research_task_id set: {sorted(actual_tasks ^ EXPECTED_TASKS)}")
    if len(candidates) != 6:
        failures.append(f"expected 6 candidates, got {len(candidates)}")
    ids = [item.get("candidate_id") for item in candidates]
    if len(ids) != len(set(ids)):
        failures.append("duplicate candidate_id detected")
    for item, path in zip(candidates, paths, strict=True):
        cid = str(item.get("candidate_id", "<unknown>"))
        if item.get("status", {}).get("review_status") != "candidate_ready":
            failures.append(f"{cid}: review_status is not candidate_ready")
        if item.get("workflow", {}).get("stage") != "candidate_ready":
            failures.append(f"{cid}: workflow.stage is not candidate_ready")
        if item.get("classification", {}).get("partition_id") not in PARTITIONS:
            failures.append(f"{cid}: partition_id mismatch")
        if len(item.get("source_refs", [])) < 3:
            failures.append(f"{cid}: source_refs < 3")
        gate = item.get("machine_gate", {})
        if gate.get("default_guidance") != "deny":
            failures.append(f"{cid}: default guidance must be deny")
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "trade_execution_advice_allowed", "risk_threshold_advice_allowed"):
            if gate.get(field) is not False:
                failures.append(f"{cid}: {field} must be false")
        blob = json.dumps(item, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake detected")
        if re.search(r"\b(api_key|secret|private_key|password)\b", blob, flags=re.IGNORECASE):
            failures.append(f"{cid}: possible secret/private field detected")
        if not path.exists():
            failures.append(f"{cid}: path missing")
    return {
        "gate_id": "phase60_p1_candidate_audit_package_quality_gate",
        "checked_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "phase": "60",
        "task_id": TASK_ID,
        "package_id": PACKAGE_ID,
        "candidate_count": len(candidates),
        "expected_count": 6,
        "candidate_paths": [rel(path) for path in paths],
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本包只审计 candidate；不得直接创建 reviewed、approved、default guidance 或 hard gate。",
            "Phase 60 P1 是增强治理知识，不替代 P0 EnvironmentManifest / PromotionDecision / GapReport。",
            "FIX、broker、paper、canary、monitoring 来源均必须保留平台、工具或工程语境边界。",
        ],
    }


def build_package(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": PACKAGE_ID,
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "created_by": "codex",
        "phase": "Phase 60",
        "task_id": TASK_ID,
        "scope": {
            "branch": "Trading Engineering",
            "partitions": PARTITIONS,
            "batch": "P1 enhanced sandbox / replay / paper environment governance",
            "candidate_count": len(candidates),
            "target": "审计 FIX/券商认证、场景回放库、paper account reset、实时模拟健康监控、live canary rollback、环境漂移监控 6 条增强治理候选。",
        },
        "hard_boundaries": {
            "candidate_not_formal": True,
            "accepted_for_draft_not_reviewed": True,
            "reviewed_not_allowed_in_this_round": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "must_not_create_formal_knowledge": True,
            "must_search_professional_sources": True,
            "must_check_sources_cases_and_data": True,
            "must_not_generate": ["买卖点", "仓位", "杠杆", "止损止盈", "风险阈值", "实盘执行建议", "上线许可"],
        },
        "audit_instructions": [
            "必须搜索相关的专业网站、官方文档、工程资料、论文、案例和数据，对本审计包进行严格审计。",
            "逐条检查来源是否足以支撑 claim；FIX、broker、framework、SRE、canary 来源不得过度泛化。",
            "检查候选是否正确归属于 Replay Simulation、Live Execution 或 Risk Management，不得混入 Strategy alpha 或 AI Engineering 本体。",
            "检查是否把 sandbox、paper、replay、canary、certification、monitoring 结果误写成 live-ready、收益证明、交易许可或 hard gate。",
            "检查是否存在中文乱码、mock/test 污染、私有策略参数、账户事实、密钥或实盘敏感信息。",
        ],
        "allowed_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected", "blocked"],
        "forbidden_decisions": ["reviewed", "approved", "default_guidance", "hard_gate"],
        "expected_output_schema": {
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | medium_high | high",
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
                }
            ]
        },
        "quality_gate": gate,
        "candidates": candidates,
    }


def main() -> int:
    candidates, paths = load_candidates()
    gate = package_quality_gate(candidates, paths)
    package = build_package(candidates, gate)
    audit_path = repo_path("docs", "audit", f"{PACKAGE_ID}.json")
    gate_path = repo_path("docs", "reports", "phase60_p1_candidate_audit_package_quality_gate.json")
    write_json(audit_path, package)
    write_json(gate_path, gate)
    report = {
        "report_id": "phase60_p1_candidate_audit_package_export_report",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "task_id": TASK_ID,
        "candidate_count": len(candidates),
        "audit_package_path": rel(audit_path),
        "quality_gate_path": rel(gate_path),
        "gate_status": gate["gate_status"],
        "next_action": "Submit audit package for external strict AI/human audit.",
    }
    report_path = repo_path("docs", "reports", "phase60_p1_candidate_audit_package_export_report.json")
    write_json(report_path, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
