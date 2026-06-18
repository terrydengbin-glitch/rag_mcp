"""Import Phase 45 Execution TCA supplemental re-audit result.

This script updates P45-A-TCA03 and P45-A-TCA06 from needs_more_evidence to
accepted_for_draft, then exports a reviewed/caveat_only preparation package for
all six Execution TCA candidates.

It never creates formal reviewed knowledge, approved knowledge, default
guidance, hard gates, risk threshold advice, or trading execution advice.
"""

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
TASK_ID = "CEK-TA-458"
AUDIT_RESULT_ID = "audit_phase45_execution_tca_supplemental_reaudit_20260612_v1"
SOURCE_PACKAGE_ID = "phase45_execution_tca_supplemental_reaudit_package_20260612"
REVIEWED_PACKAGE_ID = "phase45_execution_tca_reviewed_preparation_audit_package_20260612"
PARTITIONS = ["KB_06_LIVE_EXECUTION", "KB_07_TRADE_ANALYSIS"]

AUDIT_RESULT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path("docs", "reports", "phase45_execution_tca_supplemental_reaudit_import_report.json", start_file=__file__)
REVIEWED_PACKAGE = resolve_repo_path("docs", "audit", f"{REVIEWED_PACKAGE_ID}.json", start_file=__file__)
REVIEWED_GAP_REPORT = resolve_repo_path("docs", "reports", "phase45_execution_tca_reviewed_preparation_gap_report.json", start_file=__file__)


SUPPLEMENTAL_RESULTS: list[dict[str, Any]] = [
    {
        "candidate_id": "cand_20260612_phase45_execution_tca_p45_a_tca03_001",
        "research_task_id": "P45-A-TCA03",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reasons": [
            "FIXatdl 官方文档和 IBKR VWAP/TWAP/POV 资料足以支撑 execution scheduling / participation algorithm 边界，但不支撑策略 alpha。"
        ],
        "required_followups": [
            "保留 broker-specific / venue-specific 限制。",
            "明确 VWAP/TWAP/POV 只是 execution scheduling / participation algorithm，不是交易信号。",
            "FIXatdl 只能证明算法订单接口和参数语义，不能证明 TCA 指标、best execution 义务或 CEK-TA 风控边界。",
        ],
        "patch_notes": {
            "source": [
                "FIXatdl 可作为 algo order interface / parameter semantics 主来源。",
                "IBKR VWAP/TWAP/POV 可作为 broker-specific execution algo 示例来源。",
            ],
            "content": [
                "将不得绕过订单、风控、流动性、市场状态约束标记为 CEK-TA 内部边界。"
            ],
            "boundary": [
                "不得输出买卖点、仓位、杠杆、止损止盈或实盘执行建议。"
            ],
            "conflict": [
                "未发现与 Trading Engineering / Live Execution / Execution TCA 分区冲突。"
            ],
        },
    },
    {
        "candidate_id": "cand_20260612_phase45_execution_tca_p45_a_tca06_001",
        "research_task_id": "P45-A-TCA06",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reasons": [
            "Bailey PBO 与 White Reality Check 足以支撑 execution-derived alpha 必须转入独立策略研究验证流程。"
        ],
        "required_followups": [
            "明确本条不证明 execution-derived feature 有 alpha。",
            "若外接项目声称低滑点、VWAP outperform、routing improvement 是 alpha，必须转入 Strategy Research / Backtest Validation 分支。",
            "增加 cross-reference: kt.backtest.bias / kt.strategy_research.validation_boundary。",
        ],
        "patch_notes": {
            "source": [
                "CFA / QuantConnect 支撑 execution cost、fill、slippage、fee、implementation cost 边界。",
                "Bailey PBO / White Reality Check 支撑策略验证、过拟合和 data snooping 边界。",
            ],
            "content": [
                "保留默认只能改善或解释 implementation cost。",
                "保留若写成 alpha，必须独立验证。",
            ],
            "boundary": [
                "不能把执行算法、TCA 优化、低滑点或 benchmark outperform 直接写成交易信号。"
            ],
            "conflict": [
                "与 Execution TCA 分区不冲突，但需要显式引用 Strategy Research 验证分支。"
            ],
        },
    },
]


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def candidate_paths() -> list[Path]:
    paths: list[Path] = []
    for partition in PARTITIONS:
        cand_dir = resolve_repo_path("codex-expert-kit", "rag", "candidates", partition, start_file=__file__)
        paths.extend(sorted(cand_dir.glob("cand_20260612_phase45_execution_tca_*.json")))
    return paths


def sanitize_slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", value).strip("_")


def proposed_knowledge_id(candidate: dict[str, Any]) -> str:
    normalized = str(candidate.get("claim", {}).get("normalized_claim") or candidate.get("research_task_id", "")).replace(
        "phase45_execution_tca.", ""
    )
    normalized = normalized.replace(".v1", "")
    return f"kb_phase45_execution_tca.{sanitize_slug(normalized)}.v1"


def archive_audit_result() -> dict[str, Any]:
    result = {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "package_id": SOURCE_PACKAGE_ID,
        "summary": {
            "total": 2,
            "accepted_for_draft": 2,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "candidate_results": SUPPLEMENTAL_RESULTS,
        "hard_boundaries": {
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
        "global_notes": [
            "两条补证候选均可从 needs_more_evidence 升级为 accepted_for_draft。",
            "本次二审不允许 reviewed、approved、default guidance 或 hard gate。",
        ],
    }
    write_json(AUDIT_RESULT_ARCHIVE, result)
    return result


def update_candidates() -> dict[str, Any]:
    paths_by_task: dict[str, Path] = {}
    data_by_task: dict[str, dict[str, Any]] = {}
    for path in candidate_paths():
        data = read_json(path)
        task_id = str(data.get("research_task_id"))
        paths_by_task[task_id] = path
        data_by_task[task_id] = data

    missing: list[str] = []
    updated: list[dict[str, Any]] = []
    results_by_task = {str(item["research_task_id"]): item for item in SUPPLEMENTAL_RESULTS}

    for task_id, result in results_by_task.items():
        path = paths_by_task.get(task_id)
        if not path:
            missing.append(task_id)
            continue
        data = data_by_task[task_id]
        data["status"]["review_status"] = "accepted"
        data["status"]["ingestion_decision"] = "accepted_for_draft"
        data["status"]["decision_reason"] = result["reasons"][0]
        data["status"]["updated_at"] = TODAY
        data.setdefault("review", {})["ai_audit"] = {
            "audit_result_id": AUDIT_RESULT_ID,
            "decision": "accepted_for_draft",
            "confidence": result["confidence"],
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "required_followups": result["required_followups"],
            "patch_notes": result["patch_notes"],
        }
        data.setdefault("review", {}).setdefault("audit_log", []).append(
            {
                "at": TODAY,
                "actor": "external_ai_strict_audit",
                "action": "phase45_execution_tca_supplemental_reaudit_imported",
                "reason": "accepted_for_draft / confidence=high",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )
        data.setdefault("workflow", {})["stage"] = "formal_draft_queue"
        data["workflow"]["queue_group"] = "ai_passed"
        data["workflow"]["allowed_next_decisions"] = ["reviewed_preparation", "needs_more_evidence", "rejected"]
        data["workflow"]["forbidden_next_decisions"] = ["approved", "default_guidance", "hard_gate"]
        data["workflow"]["conversion_target"] = {
            "proposed_knowledge_id": proposed_knowledge_id(data),
            "target_review_status": "reviewed",
            "target_machine_gate": "caveat_only",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        }
        write_json(path, data)
        updated.append({"research_task_id": task_id, "candidate_id": data.get("candidate_id"), "path": str(path)})

    # Normalize all accepted Execution TCA candidates for the reviewed-preparation package.
    for task_id, data in data_by_task.items():
        if not task_id.startswith("P45-A-TCA"):
            continue
        if data.get("status", {}).get("ingestion_decision") != "accepted_for_draft":
            continue
        path = paths_by_task[task_id]
        data.setdefault("workflow", {})["stage"] = "formal_draft_queue"
        data["workflow"]["queue_group"] = "ai_passed"
        data["workflow"]["conversion_target"] = {
            "proposed_knowledge_id": proposed_knowledge_id(data),
            "target_review_status": "reviewed",
            "target_machine_gate": "caveat_only",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        }
        data.setdefault("machine_gate", {})["default_guidance"] = "deny"
        data["machine_gate"]["approved_allowed"] = False
        data["machine_gate"]["default_guidance_allowed"] = False
        data["machine_gate"]["hard_gate_allowed"] = False
        data["machine_gate"]["risk_threshold_advice_allowed"] = False
        write_json(path, data)

    return {"updated": updated, "missing": missing}


def load_reviewed_prep_candidates() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for path in candidate_paths():
        data = read_json(path)
        if data.get("status", {}).get("ingestion_decision") == "accepted_for_draft":
            candidates.append(data)
    return sorted(candidates, key=lambda item: str(item.get("research_task_id")))


def candidate_gaps(candidate: dict[str, Any]) -> list[str]:
    gaps: list[str] = []
    cid = str(candidate.get("candidate_id"))
    if candidate.get("status", {}).get("review_status") != "accepted":
        gaps.append("status.review_status_not_accepted")
    if candidate.get("status", {}).get("ingestion_decision") != "accepted_for_draft":
        gaps.append("status.ingestion_decision_not_accepted_for_draft")
    if candidate.get("workflow", {}).get("stage") != "formal_draft_queue":
        gaps.append("workflow.stage_not_formal_draft_queue")
    if candidate.get("workflow", {}).get("queue_group") != "ai_passed":
        gaps.append("workflow.queue_group_not_ai_passed")
    if not candidate.get("workflow", {}).get("conversion_target", {}).get("proposed_knowledge_id"):
        gaps.append("conversion_target.proposed_knowledge_id_missing")
    if len(candidate.get("source_refs", [])) < 3:
        gaps.append("source_refs_less_than_3")
    gate = candidate.get("machine_gate", {})
    if gate.get("default_guidance") != "deny":
        gaps.append("machine_gate.default_guidance_not_deny")
    for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "risk_threshold_advice_allowed"):
        if gate.get(field) is not False:
            gaps.append(f"machine_gate.{field}_not_false")
    blob = json.dumps(candidate, ensure_ascii=False)
    if "�" in blob or "????" in blob:
        gaps.append(f"{cid}: possible_mojibake")
    return gaps


def build_reviewed_package(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": REVIEWED_PACKAGE_ID,
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "package_type": "reviewed_caveat_only_preparation_audit",
        "scope": {
            "phase": "Phase 45",
            "branch": "Trading Engineering",
            "batch": "P45-A Execution TCA",
            "candidate_count": len(candidates),
            "source_audit_results": [
                "audit_phase45_execution_tca_p45_a_20260612_external_strict_v1",
                AUDIT_RESULT_ID,
            ],
            "target": "判断 6 条 Execution TCA accepted_for_draft 候选是否可转 formal reviewed/caveat_only。",
        },
        "hard_boundaries": {
            "candidate_is_not_formal_knowledge": True,
            "this_package_may_allow_reviewed_caveat_only": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
            "must_not_generate": ["买卖点", "仓位", "杠杆", "止损止盈参数", "实盘执行建议", "风险阈值数值"],
        },
        "audit_instructions": [
            "必须搜索相关专业网站、官方文档、监管资料、协议文档、论文、案例和数据，对本 reviewed/caveat_only 准备包进行严格审计。",
            "逐条判断是否可进入 formal reviewed/caveat_only；不得允许 approved、default guidance 或 hard gate。",
            "重点复核 TCA01/TCA02/TCA04/TCA05 首轮 followups 是否足以进入 reviewed/caveat_only。",
            "重点复核 TCA03/TCA06 的二审补证是否足以进入 reviewed/caveat_only。",
            "检查 Execution TCA 是否只表达执行成本、benchmark、routing context 和执行质量边界，不混入策略 alpha、交易许可或风控阈值。",
            "检查是否有中文乱码、mock/test 污染、项目私有参数、账户事实、密钥、交易所私有配置或实盘敏感信息。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": REVIEWED_PACKAGE_ID,
            "summary": {
                "total": 6,
                "accepted_for_reviewed_caveat_only": 0,
                "needs_more_evidence": 0,
                "rejected": 0,
                "blocked": 0,
            },
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | high",
                    "reviewed_allowed": "boolean",
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
            ],
        },
        "quality_gate": gate,
        "candidates": [
            {
                "candidate_id": candidate.get("candidate_id"),
                "research_task_id": candidate.get("research_task_id"),
                "status": candidate.get("status", {}),
                "workflow": candidate.get("workflow", {}),
                "classification": candidate.get("classification", {}),
                "claim": candidate.get("claim", {}),
                "applicability": candidate.get("applicability", {}),
                "source_refs": candidate.get("source_refs", []),
                "source_quality": candidate.get("source_quality", {}),
                "conflict_audit": candidate.get("conflict_audit", {}),
                "llm_usage_policy": candidate.get("llm_usage_policy", {}),
                "machine_gate": candidate.get("machine_gate", {}),
                "review": candidate.get("review", {}),
                "quality_gate": {
                    "package_ready": not candidate_gaps(candidate),
                    "gaps": candidate_gaps(candidate),
                },
            }
            for candidate in candidates
        ],
    }


def export_reviewed_package(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    if len(candidates) != 6:
        failures.append(f"expected 6 accepted_for_draft candidates, got {len(candidates)}")
    expected = {f"P45-A-TCA{idx:02d}" for idx in range(1, 7)}
    actual = {str(item.get("research_task_id")) for item in candidates}
    if actual != expected:
        failures.append(f"unexpected research_task_id set: {sorted(actual ^ expected)}")
    for candidate in candidates:
        for gap in candidate_gaps(candidate):
            failures.append(f"{candidate.get('candidate_id')}: {gap}")
    gate = {
        "gate_id": "phase45_execution_tca_reviewed_preparation_gap_report",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "package_id": REVIEWED_PACKAGE_ID,
        "candidate_count": len(candidates),
        "expected_count": 6,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本包只请求 reviewed/caveat_only 准备审计；不得创建 approved、default guidance 或 hard gate。",
            "Execution TCA reviewed 仍只能作为执行成本和执行质量审计上下文，不得生成交易许可。",
        ],
    }
    write_json(REVIEWED_GAP_REPORT, gate)
    write_json(REVIEWED_PACKAGE, build_reviewed_package(candidates, gate))
    return gate


def main() -> int:
    audit_result = archive_audit_result()
    update_report = update_candidates()
    candidates = load_reviewed_prep_candidates()
    gate = export_reviewed_package(candidates)
    write_json(
        IMPORT_REPORT,
        {
            "report_id": "phase45_execution_tca_supplemental_reaudit_import_report",
            "generated_at": TODAY,
            "phase": PHASE,
            "task_id": TASK_ID,
            "audit_result_id": AUDIT_RESULT_ID,
            "source_package_id": SOURCE_PACKAGE_ID,
            "audit_summary": audit_result["summary"],
            "updated": update_report["updated"],
            "missing": update_report["missing"],
            "reviewed_preparation_package": str(REVIEWED_PACKAGE),
            "reviewed_preparation_gap_report": str(REVIEWED_GAP_REPORT),
            "reviewed_preparation_gate_status": gate["gate_status"],
            "formal_reviewed_created": 0,
            "approved_created": 0,
            "default_guidance_enabled": False,
            "hard_gate_enabled": False,
        },
    )
    print(
        json.dumps(
            {
                "status": gate["gate_status"],
                "updated_count": len(update_report["updated"]),
                "reviewed_preparation_candidate_count": len(candidates),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if gate["gate_status"] == "pass" and not update_report["missing"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
