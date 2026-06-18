"""Export Phase 37 Trade Analysis candidates for strict external audit."""

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
PHASE = "37"
TASK_ID = "CEK-TA-443"
PACKAGE_ID = "phase37_trade_analysis_candidate_audit_package_20260612"
PARTITION = "KB_07_TRADE_ANALYSIS"

CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
AUDIT_PACKAGE = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
PACKAGE_GATE = resolve_repo_path("docs", "reports", "phase37_trade_analysis_candidate_audit_package_quality_gate.json", start_file=__file__)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_candidates() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for path in sorted(CAND_DIR.glob("cand_20260612_phase37_trade_analysis_*.json")):
        data = read_json(path)
        if (
            data.get("status", {}).get("ingestion_decision") == "candidate_ready"
            and data.get("workflow", {}).get("stage") == "pending_external_audit"
        ):
            candidates.append(data)
    return sorted(candidates, key=lambda item: str(item.get("research_task_id")))


def package_quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    if len(candidates) != 12:
        failures.append(f"expected 12 candidate_ready candidates, got {len(candidates)}")
    expected_tasks = {f"P37-H-T{idx:02d}" for idx in range(1, 13)}
    actual_tasks = {str(item.get("research_task_id")) for item in candidates}
    if actual_tasks != expected_tasks:
        failures.append(f"unexpected research_task_id set: {sorted(actual_tasks ^ expected_tasks)}")
    ids = [item.get("candidate_id") for item in candidates]
    if len(ids) != len(set(ids)):
        failures.append("duplicate candidate_id detected")
    for item in candidates:
        cid = item.get("candidate_id", "<unknown>")
        if item.get("classification", {}).get("partition_id") != PARTITION:
            failures.append(f"{cid}: partition_id mismatch")
        if item.get("status", {}).get("review_status") != "candidate_ready":
            failures.append(f"{cid}: review_status is not candidate_ready")
        if item.get("workflow", {}).get("stage") != "pending_external_audit":
            failures.append(f"{cid}: workflow.stage is not pending_external_audit")
        gate = item.get("machine_gate", {})
        if gate.get("default_guidance") != "deny":
            failures.append(f"{cid}: default guidance must be deny")
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed"):
            if gate.get(field) is not False:
                failures.append(f"{cid}: {field} must be false")
        if len(item.get("source_refs", [])) < 3:
            failures.append(f"{cid}: source_refs < 3")
        if item.get("source_quality", {}).get("primary_source_count", 0) < 1:
            failures.append(f"{cid}: primary_source_count < 1")
        blob = json.dumps(item, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake detected")
        if re.search(r"\b(api_key|secret|private_key|password)\b", blob, flags=re.IGNORECASE):
            failures.append(f"{cid}: possible secret/private field detected")
    return {
        "gate_id": "phase37_trade_analysis_candidate_audit_package_quality_gate",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "package_id": PACKAGE_ID,
        "candidate_count": len(candidates),
        "expected_count": 12,
        "partition_id": PARTITION,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本包只审计 candidate；不得直接创建 reviewed、approved、default guidance 或 hard gate。",
            "Trade Analysis 知识只约束复盘、标签、reason code、质量归因和研究假设边界，不得证明策略盈利。",
            "Vendor journal sources 只能作为复盘工作流示例，不得单独支撑 reviewed 级字段本体。",
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
            "branch": "Trading Engineering",
            "partitions": [PARTITION],
            "batch": "P37-H Trade Analysis / 交易复盘",
            "candidate_count": len(candidates),
            "target": "审计交易复盘候选，包括计划/实际 R、MAE/MFE、坏例 taxonomy、好亏损/坏盈利、入场/出场/风险/执行质量、规则符合性、市场状态适配、reason code 和研究假设验证。",
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
            "must_not_generate": ["买卖点", "仓位", "杠杆", "止损止盈参数", "实盘执行建议", "风险阈值数值"],
        },
        "audit_instructions": [
            "必须搜索相关的专业网站、官方文档、论文、交易复盘工具资料、案例和数据，对本审计包进行严格审计。",
            "逐条检查来源是否足以支撑 claim；CFA、论文、平台文档和 journal vendor sources 不得被过度泛化。",
            "检查 Trade Analysis 是否正确分区，不得把实时风控、实盘执行、回测统计或 AI Engineering 本体混进本分支。",
            "检查每条候选是否清楚声明适用范围、不适用场景、假设、限制、来源质量和 AI 使用边界。",
            "重点审计 planned vs realized R、MAE/MFE post-trade-only、bad trade taxonomy、good loss/bad win、entry/exit/risk/execution quality、rule compliance、regime fit、reason code 和 research hypothesis validation。",
            "检查是否有中文乱码、mock/test 污染、项目私有策略参数、账户事实、密钥、交易所私有配置或实盘敏感信息。",
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
                        "expected_branch": "Trading Engineering / Trade Analysis",
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
