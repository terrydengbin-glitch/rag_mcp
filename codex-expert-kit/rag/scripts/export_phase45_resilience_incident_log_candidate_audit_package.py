"""Export Phase 45 Resilience / Incident / Log candidates for strict audit."""

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


TODAY = "2026-06-12"
PHASE = "45"
TASK_ID = "CEK-TA-464"
PACKAGE_ID = "phase45_resilience_incident_log_candidate_audit_package_20260612"
PARTITIONS = ["KB_06_LIVE_EXECUTION", "KB_AI_26_DATABASE_STORAGE"]

AUDIT_PACKAGE = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
PACKAGE_GATE = resolve_repo_path("docs", "reports", "phase45_resilience_incident_log_candidate_audit_package_quality_gate.json", start_file=__file__)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_candidates() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for partition in PARTITIONS:
        cand_dir = resolve_repo_path("codex-expert-kit", "rag", "candidates", partition, start_file=__file__)
        for path in sorted(cand_dir.glob("cand_20260612_phase45_resilience_incident_log_*.json")):
            data = read_json(path)
            if data.get("status", {}).get("ingestion_decision") == "candidate_ready" and data.get("workflow", {}).get("stage") == "pending_external_audit":
                candidates.append(data)
    return sorted(candidates, key=lambda item: str(item.get("research_task_id")))


def package_quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    if len(candidates) != 6:
        failures.append(f"expected 6 candidate_ready Resilience / Incident / Log candidates, got {len(candidates)}")
    expected_tasks = {f"P45-D-OPS{idx:02d}" for idx in range(1, 7)}
    actual_tasks = {str(item.get("research_task_id")) for item in candidates}
    if actual_tasks != expected_tasks:
        failures.append(f"unexpected research_task_id set: {sorted(actual_tasks ^ expected_tasks)}")
    ids = [item.get("candidate_id") for item in candidates]
    if len(ids) != len(set(ids)):
        failures.append("duplicate candidate_id detected")
    allowed_nodes = {"kt.live_execution.resilience_incident_log", "kt.ai_engineering.database_storage_engineering.audit_log_ledger"}
    for item in candidates:
        cid = item.get("candidate_id", "<unknown>")
        if item.get("classification", {}).get("partition_id") not in PARTITIONS:
            failures.append(f"{cid}: partition_id mismatch")
        if item.get("classification", {}).get("canonical_node_id") not in allowed_nodes:
            failures.append(f"{cid}: canonical_node_id mismatch")
        if item.get("status", {}).get("review_status") != "candidate_ready":
            failures.append(f"{cid}: review_status is not candidate_ready")
        if item.get("workflow", {}).get("stage") != "pending_external_audit":
            failures.append(f"{cid}: workflow.stage is not pending_external_audit")
        if len(item.get("source_refs", [])) < 4:
            failures.append(f"{cid}: source_refs < 4")
        if item.get("source_quality", {}).get("primary_source_count", 0) < 3:
            failures.append(f"{cid}: primary_source_count < 3")
        gate = item.get("machine_gate", {})
        if gate.get("default_guidance") != "deny":
            failures.append(f"{cid}: default guidance must be deny")
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "risk_threshold_advice_allowed"):
            if gate.get(field) is not False:
                failures.append(f"{cid}: {field} must be false")
        blob = json.dumps(item, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake detected")
        if re.search(r"\b(api_key|secret|private_key|password)\b", blob, flags=re.IGNORECASE):
            failures.append(f"{cid}: possible secret/private field detected")
    return {
        "gate_id": "phase45_resilience_incident_log_candidate_audit_package_quality_gate",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "package_id": PACKAGE_ID,
        "candidate_count": len(candidates),
        "expected_count": 6,
        "partitions": PARTITIONS,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本包只审计 candidate；不得直接创建 reviewed、approved、default guidance 或 hard gate。",
            "Resilience / Incident / Log 只能用于运行时韧性、事故响应、恢复/replay 和日志治理边界，不得输出交易动作或风险阈值。",
            "SEC/FINRA/NIST/AWS/Google SRE/OpenTelemetry 来源具有监管、标准或工程实践边界，不得过度泛化。",
        ],
    }


def build_package(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": PACKAGE_ID,
        "created_at": TODAY,
        "created_by": "codex",
        "phase": PHASE,
        "task_id": TASK_ID,
        "scope": {
            "branch": "Trading Engineering / Live Execution / Resilience Incident Log",
            "partitions": PARTITIONS,
            "batch": "P45-D Resilience / Incident / Log / 系统韧性、事故响应与日志治理",
            "candidate_count": len(candidates),
            "target": "审计 BC/DR、降级/只读模式、failover/recovery/replay、incident taxonomy、post-incident review 和 runtime log retention/integrity 候选知识。",
        },
        "hard_boundaries": {
            "candidate_not_formal": True,
            "accepted_for_draft_not_reviewed": True,
            "reviewed_not_approved": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "must_not_create_formal_knowledge": True,
            "must_not_generate": ["买卖点", "仓位", "杠杆", "止损止盈参数", "实盘执行建议", "风险阈值数值", "停机阈值", "自动重发订单", "自动撤单"],
        },
        "audit_instructions": [
            "必须搜索相关的专业网站、官方文档、监管资料、交易所/行业资料、工程案例和数据，对本审计包进行严格审计。",
            "逐条检查来源是否足以支撑 claim；SEC/FINRA/NIST/AWS/Google SRE/OpenTelemetry 不得被过度泛化。",
            "检查 Resilience / Incident / Log 是否正确归入 Live Execution 或 Database/Storage owner，不得把 AI Engineering、策略 alpha、风控阈值或实盘动作混进本分支。",
            "检查每条候选是否清楚声明适用范围、不适用场景、假设、限制、来源质量和 AI 使用边界。",
            "重点审计 BC/DR、degraded/read-only mode、failover/recovery/replay、incident taxonomy、post-incident review、runtime log retention/integrity。",
            "检查是否有中文乱码、mock/test 污染、项目私有策略参数、账户事实、密钥、交易所私有配置、真实阈值或实盘敏感信息。",
            "输出只能是 accepted_for_draft、needs_more_evidence、rejected 或 blocked；不得输出 reviewed、approved、default guidance 或 hard gate。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "auditor": "string",
            "audited_at": "YYYY-MM-DD",
            "package_id": PACKAGE_ID,
            "summary": {
                "total": 6,
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
                    "risk_threshold_advice_allowed": False,
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
                        "expected_branch": "Trading Engineering / Live Execution / Resilience Incident Log 或 AI Engineering / Database Storage / Audit Log Ledger",
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
    write_json(PACKAGE_GATE, gate)
    write_json(AUDIT_PACKAGE, build_package(candidates, gate))
    print(json.dumps({"status": gate["gate_status"], "candidate_count": len(candidates), "audit_package": str(AUDIT_PACKAGE)}, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
