"""Supplement Phase 41 reviewed-preparation needs-more-evidence candidates.

This script adds direct CEK-TA internal contract evidence for P41-B05 and
P41-D03, keeps both candidates out of reviewed/approved/default guidance, and
exports a focused supplemental re-audit package.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 10).isoformat()
TASK_ID = "CEK-TA-326"
PACKAGE_ID = "phase41_reviewed_preparation_supplemental_reaudit_package_20260610"

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
CONTRACT_PATH = resolve_repo_path(
    "docs", "contracts", "phase41_tabular_llm_training_data_contract.md", start_file=__file__
)
AUDIT_PACKAGE_PATH = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
REPORT_JSON_PATH = resolve_repo_path(
    "docs", "reports", "phase41_reviewed_preparation_supplemental_evidence_report.json", start_file=__file__
)
REPORT_MD_PATH = resolve_repo_path(
    "docs", "reports", "phase41_reviewed_preparation_supplemental_evidence_report.md", start_file=__file__
)
FOLLOWUP_PATH = resolve_repo_path(
    "docs", "reports", "phase41_reviewed_preparation_remaining_followups.json", start_file=__file__
)


TARGETS: dict[str, dict[str, Any]] = {
    "P41-B05": {
        "candidate_file": "cand_20260610_phase41_p41_b05_dataset_hash_split_manifest_hash_feature_schema_version_label_policy_version_001.json",
        "schema_name": "TrainingDatasetManifest",
        "source_id": "src_phase41_training_dataset_manifest_contract",
        "evidence_dimension": "training_dataset_manifest_schema",
        "evidence_summary": (
            "Phase 41 training data contract now defines TrainingDatasetManifest with "
            "dataset_hash, split_manifest_hash, feature_schema_version, label_policy_version, "
            "lineage_manifest_ref, source_snapshot_refs, forbidden_fields_scan_ref, owner and "
            "hard gates for dataset manifest review."
        ),
        "decision_reason": (
            "已补充 Phase 41 TrainingDatasetManifest 内部契约，覆盖 dataset_hash、"
            "split_manifest_hash、feature_schema_version、label_policy_version 的组合字段和硬门。"
        ),
        "audit_question": (
            "TrainingDatasetManifest 内部契约是否足以支撑 P41-B05 后续转入 "
            "formal reviewed / caveat_only。"
        ),
    },
    "P41-D03": {
        "candidate_file": "cand_20260610_phase41_p41_d03_feature_lineage_source_object_ref_lineage_ref_schema_version_001.json",
        "schema_name": "FeatureLineageRecord",
        "source_id": "src_phase41_feature_lineage_record_contract",
        "evidence_dimension": "feature_lineage_record_schema",
        "evidence_summary": (
            "Phase 41 training data contract now defines FeatureLineageRecord with "
            "feature_id, source_object_ref, lineage_ref, feature_schema_version, "
            "missing_value_policy, feature_available_time_policy, online_offline_parity_check_ref, "
            "owner, deprecation_policy and hard gates for feature lineage review."
        ),
        "decision_reason": (
            "已补充 Phase 41 FeatureLineageRecord 内部契约，覆盖 source_object_ref、"
            "lineage_ref、feature_schema_version、missing_value_policy、owner 和 deprecation_policy。"
        ),
        "audit_question": (
            "FeatureLineageRecord 内部契约是否足以支撑 P41-D03 后续转入 "
            "formal reviewed / caveat_only。"
        ),
    },
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def append_unique_text(values: list[Any], text: str) -> None:
    if text not in values:
        values.append(text)


def internal_contract_source(target: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": target["source_id"],
        "source_title": f"Phase 41 {target['schema_name']} contract",
        "source_url": repo_rel(CONTRACT_PATH),
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "published_at": TODAY,
        "accessed_at": TODAY,
        "version": "phase41_contract_draft_20260610",
        "reliability": "high",
        "score": 90,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_dimension": target["evidence_dimension"],
        "limitations": [
            "内部契约用于 CEK-TA 知识治理和外接项目开发约束，不等于交易收益、fill model、风控或实盘执行规则。",
            "本来源只补足 schema/contract 证据，仍需外部二审决定是否允许转 formal reviewed。",
        ],
        "evidence_summary": target["evidence_summary"],
        "quoted_excerpt_allowed": False,
    }


def add_source(candidate: dict[str, Any], target: dict[str, Any]) -> None:
    refs = candidate.setdefault("source_refs", [])
    if not isinstance(refs, list):
        raise ValueError(f"{candidate.get('candidate_id')} source_refs must be a list")
    existing = {ref.get("source_id") for ref in refs if isinstance(ref, dict)}
    if target["source_id"] not in existing:
        refs.append(internal_contract_source(target))

    primary_types = {
        "official_doc",
        "standard_doc",
        "governance_framework",
        "internal_contract",
        "research_paper",
        "security_standard",
        "regulator_release",
        "regulator_review",
    }
    primary_count = len([ref for ref in refs if isinstance(ref, dict) and ref.get("source_type") in primary_types])
    quality = candidate.setdefault("source_quality", {})
    quality["overall_reliability"] = "high"
    quality["score"] = max(int(quality.get("score") or 0), 88)
    quality["primary_source_count"] = primary_count
    quality["supporting_source_count"] = max(0, len(refs) - primary_count)
    dimensions = quality.setdefault("claim_specific_dimensions_covered", [])
    if isinstance(dimensions, list):
        append_unique_text(dimensions, target["evidence_dimension"])


def patch_candidate(candidate: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    research_task_id = str(candidate.get("research_task_id"))
    if research_task_id not in TARGETS:
        raise ValueError(f"Unexpected research_task_id: {research_task_id}")

    add_source(candidate, target)

    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "needs_more_evidence"
    status["decision_reason"] = target["decision_reason"] + " 等待二审确认。"
    status["updated_at"] = TODAY

    candidate.setdefault("claim", {})["evidence_summary"] = (
        f"{candidate.get('claim', {}).get('evidence_summary', '')}；"
        f"已新增 CEK-TA 内部契约证据：{target['schema_name']}。"
    ).strip("；")

    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "needs_more_evidence"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["formal_knowledge_id"] = None
    workflow["formal_review_status"] = "blocked"
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False
    workflow["next_action"] = "external_supplemental_reaudit"

    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "blocked"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["requires_human_escalation"] = True
    machine_gate["reason"] = (
        "已补充内部契约证据，但仍等待外部二审；不能生成 formal reviewed、approved、"
        "default guidance 或 hard gate。"
    )

    conflict = candidate.setdefault("conflict_audit", {})
    conflict["approval_allowed"] = False
    checked = conflict.setdefault("checked_against", [])
    if isinstance(checked, list):
        append_unique_text(checked, repo_rel(CONTRACT_PATH))

    review = candidate.setdefault("review", {})
    review["reviewed_allowed"] = False
    review["approved_allowed"] = False
    review["default_guidance_allowed"] = False
    review["hard_gate_allowed"] = False
    review["reviewer"] = "codex_supplemental_evidence_preparation"
    open_questions = review.setdefault("open_questions", [])
    if isinstance(open_questions, list):
        append_unique_text(open_questions, "external_supplemental_reaudit_required")
        append_unique_text(open_questions, target["audit_question"])
    audit_log = review.setdefault("audit_log", [])
    if isinstance(audit_log, list):
        audit_log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase41_reviewed_preparation_internal_contract_evidence_added",
                "reason": target["decision_reason"],
            }
        )

    ai_audit = review.setdefault("ai_audit", {})
    if isinstance(ai_audit, dict):
        ai_audit["source_package_id"] = PACKAGE_ID
        ai_audit["decision"] = "needs_more_evidence"
        ai_audit["reason"] = target["decision_reason"] + " 等待二审确认。"
        ai_audit["reviewed_allowed"] = False
        ai_audit["approved_allowed"] = False
        ai_audit["default_guidance_allowed"] = False
        ai_audit["hard_gate_allowed"] = False
        required = ai_audit.setdefault("required_followups", [])
        if isinstance(required, list):
            append_unique_text(required, "external_supplemental_reaudit")
        source_patch_notes = ai_audit.setdefault("source_patch_notes", [])
        if isinstance(source_patch_notes, list):
            append_unique_text(source_patch_notes, f"Added {target['schema_name']} internal contract evidence.")

    trace = candidate.setdefault("phase41_trace", {})
    contracts = trace.setdefault("related_contracts", [])
    if isinstance(contracts, list):
        append_unique_text(contracts, repo_rel(CONTRACT_PATH))
    trace["reviewed_preparation_supplemental_evidence"] = {
        "prepared_at": TODAY,
        "prepared_by": "codex",
        "schema_name": target["schema_name"],
        "source_id": target["source_id"],
        "contract_path": repo_rel(CONTRACT_PATH),
        "audit_request": target["audit_question"],
        "boundary": (
            "补证只覆盖 AI Engineering 训练/特征治理 schema，不定义 Trading Engineering 的交易收益、"
            "K 线、fill、滑点、手续费、仓位、止损止盈或实盘执行本体。"
        ),
    }
    return candidate


def load_and_patch_targets() -> list[dict[str, Any]]:
    patched: list[dict[str, Any]] = []
    for research_task_id, target in TARGETS.items():
        path = CANDIDATE_DIR / str(target["candidate_file"])
        candidate = read_json(path)
        if candidate.get("research_task_id") != research_task_id:
            raise ValueError(f"{path} research_task_id mismatch")
        patched_candidate = patch_candidate(candidate, target)
        write_json(path, patched_candidate)
        patched_candidate["_audit_export_meta"] = {
            "source_file": repo_rel(path),
            "supplemented_schema": target["schema_name"],
            "supplemented_source_id": target["source_id"],
            "contract_path": repo_rel(CONTRACT_PATH),
            "required_next_decision": (
                "外部二审必须显式给出 accepted_for_draft + reviewed_allowed=true，"
                "后续 Codex 才能生成 formal reviewed；否则继续 needs_more_evidence 或 rejected。"
            ),
        }
        patched.append(patched_candidate)
    return patched


def build_quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    for candidate in candidates:
        candidate_id = str(candidate.get("candidate_id", ""))
        sources = candidate.get("source_refs") if isinstance(candidate.get("source_refs"), list) else []
        source_ids = {str(source.get("source_id")) for source in sources if isinstance(source, dict)}
        research_task_id = str(candidate.get("research_task_id", ""))
        expected_source = TARGETS[research_task_id]["source_id"]
        if expected_source not in source_ids:
            failures.append({"candidate_id": candidate_id, "failure": "missing_internal_contract_source"})
        if candidate.get("workflow", {}).get("queue_group") != "needs_more_evidence":
            failures.append({"candidate_id": candidate_id, "failure": "queue_group_not_needs_more_evidence"})
        if candidate.get("workflow", {}).get("hidden_from_default_queue") is not True:
            failures.append({"candidate_id": candidate_id, "failure": "hidden_from_default_queue_not_true"})
        if candidate.get("workflow", {}).get("visible_in_default_guidance_queue") is not False:
            failures.append({"candidate_id": candidate_id, "failure": "visible_in_default_guidance_queue_not_false"})
        if candidate.get("review", {}).get("reviewed_allowed") is not False:
            failures.append({"candidate_id": candidate_id, "failure": "reviewed_allowed_not_false_before_reaudit"})
        if candidate.get("review", {}).get("approved_allowed") is not False:
            failures.append({"candidate_id": candidate_id, "failure": "approved_allowed_not_false"})
        if candidate.get("review", {}).get("default_guidance_allowed") is not False:
            failures.append({"candidate_id": candidate_id, "failure": "default_guidance_allowed_not_false"})
        if candidate.get("review", {}).get("hard_gate_allowed") is not False:
            failures.append({"candidate_id": candidate_id, "failure": "hard_gate_allowed_not_false"})
        if len(sources) < 4:
            failures.append({"candidate_id": candidate_id, "failure": "source_refs_lt_4_after_supplement"})
    return {
        "gate_id": "phase41_reviewed_preparation_supplemental_evidence_gate",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "candidate_count": len(candidates),
        "expected_count": len(TARGETS),
        "checks": {
            "candidate_count_matches": "pass" if len(candidates) == len(TARGETS) else "fail",
            "internal_contract_sources_present": "pass"
            if not [item for item in failures if item["failure"] == "missing_internal_contract_source"]
            else "fail",
            "kept_out_of_default_guidance": "pass"
            if not [
                item
                for item in failures
                if item["failure"]
                in {"hidden_from_default_queue_not_true", "visible_in_default_guidance_queue_not_false"}
            ]
            else "fail",
            "no_reviewed_or_approved_before_reaudit": "pass"
            if not [
                item
                for item in failures
                if item["failure"]
                in {
                    "reviewed_allowed_not_false_before_reaudit",
                    "approved_allowed_not_false",
                    "default_guidance_allowed_not_false",
                    "hard_gate_allowed_not_false",
                }
            ]
            else "fail",
        },
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
    }


def candidate_for_audit(candidate: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "_audit_export_meta",
        "candidate_id",
        "research_task_id",
        "status",
        "workflow",
        "classification",
        "claim",
        "applicability",
        "source_refs",
        "source_quality",
        "conflict_audit",
        "machine_gate",
        "conversion_target",
        "review",
        "phase41_trace",
    ]
    return {key: candidate.get(key) for key in keys if key in candidate}


def write_audit_package(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> None:
    package = {
        "package_id": PACKAGE_ID,
        "package_type": "candidate_supplemental_reaudit_package",
        "generated_at": TODAY,
        "phase": "41",
        "task_id": TASK_ID,
        "title": "Phase 41 reviewed-preparation 补证二审包",
        "purpose": (
            "审计 P41-B05 和 P41-D03 是否因新增内部契约证据而具备 "
            "accepted_for_draft + reviewed_allowed=true 条件。"
        ),
        "source_previous_audit_result_id": "audit_result_phase41_ai_passed_reviewed_preparation_20260610_strict_v1",
        "quality_gate": gate,
        "candidate_count": len(candidates),
        "allowed_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected"],
        "reviewed_preparation_rules": [
            "若允许后续转 formal reviewed，必须 decision=accepted_for_draft 且 reviewed_allowed=true。",
            "若仍需补证，必须 decision=needs_more_evidence 且 reviewed_allowed=false。",
            "若候选过宽、错分或污染知识库，必须 decision=rejected 且 reviewed_allowed=false。",
            "approved_allowed、default_guidance_allowed、hard_gate_allowed 必须始终为 false。",
            "reviewed 只允许 caveat_only machine_gate，不允许 allow。",
        ],
        "hard_boundaries": [
            "本包不能直接创建 formal reviewed。",
            "本包不能创建 approved。",
            "本包不能启用 default guidance。",
            "本包不能启用 hard gate。",
            "内部契约证据只证明 schema/contract 边界，不证明交易收益或策略有效性。",
            "Trading PnL、fill、slippage、fee、K 线、仓位和实盘执行本体继续归 Trading Engineering。",
        ],
        "audit_questions": [
            TARGETS["P41-B05"]["audit_question"],
            TARGETS["P41-D03"]["audit_question"],
            "这两条候选是否仍保持 AI Engineering 边界，没有混入 Trading Engineering 本体？",
            "如通过，是否只允许后续 Codex 生成 formal reviewed / caveat_only，而不进入 approved/default/hard gate？",
        ],
        "expected_output_schema": {
            "audit_result_id": "audit_result_phase41_reviewed_preparation_supplemental_reaudit_20260610_strict_v1",
            "source_package_id": PACKAGE_ID,
            "decisions": [
                {
                    "candidate_id": "string",
                    "research_task_id": "P41-B05 | P41-D03",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected",
                    "reviewed_allowed": False,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "reason": "string",
                    "source_patch_notes": [],
                    "content_patch_notes": [],
                    "boundary_patch_notes": [],
                    "conflict_patch_notes": [],
                    "required_followups": [],
                }
            ],
            "batch_summary": {
                "accepted_for_reviewed_count": 0,
                "needs_more_evidence_count": 0,
                "rejected_count": 0,
                "reviewed_allowed_count": 0,
                "approved_allowed_count": 0,
                "default_guidance_allowed_count": 0,
                "hard_gate_allowed_count": 0,
            },
        },
        "candidates": [candidate_for_audit(candidate) for candidate in candidates],
    }
    write_json(AUDIT_PACKAGE_PATH, package)


def write_reports(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> None:
    report = {
        "report_id": "phase41_reviewed_preparation_supplemental_evidence_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "phase": "41",
        "conclusion": "已为 P41-B05 与 P41-D03 补充内部契约证据，导出二审包；两条仍不是 formal reviewed/approved/default guidance。",
        "quality_gate": gate,
        "audit_package": repo_rel(AUDIT_PACKAGE_PATH),
        "contract_updated": repo_rel(CONTRACT_PATH),
        "candidate_count": len(candidates),
        "items": [
            {
                "candidate_id": candidate.get("candidate_id"),
                "research_task_id": candidate.get("research_task_id"),
                "schema_name": TARGETS[str(candidate.get("research_task_id"))]["schema_name"],
                "source_id": TARGETS[str(candidate.get("research_task_id"))]["source_id"],
                "source_count": len(candidate.get("source_refs") or []),
                "queue_group": candidate.get("workflow", {}).get("queue_group"),
                "next_action": candidate.get("workflow", {}).get("next_action"),
            }
            for candidate in candidates
        ],
        "boundaries": [
            "补证不改变候选状态语义。",
            "二审通过前不生成 formal reviewed。",
            "即使二审允许 reviewed，仍不得自动 approved/default guidance/hard gate。",
        ],
    }
    write_json(REPORT_JSON_PATH, report)

    lines = [
        "# Phase 41 reviewed-preparation 补证报告",
        "",
        f"生成日期：{TODAY}",
        "",
        "## 结论",
        "",
        "已为 P41-B05 与 P41-D03 补充内部契约证据，并导出二审包。",
        "",
        "两条候选仍保持 `needs_more_evidence`，未生成 formal reviewed，未设置 approved、default guidance 或 hard gate。",
        "",
        "## 交付物",
        "",
        f"- 契约：`{repo_rel(CONTRACT_PATH)}`",
        f"- 二审包：`{repo_rel(AUDIT_PACKAGE_PATH)}`",
        f"- JSON 报告：`{repo_rel(REPORT_JSON_PATH)}`",
        "",
        "## 补证项",
        "",
        "| 任务 | 补充契约 | 来源 ID |",
        "| --- | --- | --- |",
    ]
    for candidate in candidates:
        target = TARGETS[str(candidate.get("research_task_id"))]
        lines.append(f"| {candidate.get('research_task_id')} | {target['schema_name']} | {target['source_id']} |")
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "- 二审通过前不生成 formal reviewed。",
            "- 二审通过后也只能生成 `reviewed / caveat_only`，不能自动 `approved`。",
            "- 不定义交易收益、K 线、fill、滑点、手续费、仓位、止损止盈或实盘执行本体。",
            "",
        ]
    )
    REPORT_MD_PATH.write_text("\n".join(lines), encoding="utf-8")

    followup = {
        "report_id": "phase41_reviewed_preparation_remaining_followups",
        "generated_at": TODAY,
        "source_audit_result_id": "audit_result_phase41_ai_passed_reviewed_preparation_20260610_strict_v1",
        "remaining_count": len(candidates),
        "items": [
            {
                "candidate_id": candidate.get("candidate_id"),
                "research_task_id": candidate.get("research_task_id"),
                "status": "ready_for_supplemental_reaudit",
                "supplemental_reaudit_package": repo_rel(AUDIT_PACKAGE_PATH),
                "reason": TARGETS[str(candidate.get("research_task_id"))]["decision_reason"],
                "required_followups": ["external_ai_or_human_supplemental_reaudit"],
            }
            for candidate in candidates
        ],
        "boundary": "remaining candidates are not reviewed, approved, default guidance, or hard gate enabled.",
    }
    write_json(FOLLOWUP_PATH, followup)


def main() -> int:
    candidates = load_and_patch_targets()
    gate = build_quality_gate(candidates)
    write_audit_package(candidates, gate)
    write_reports(candidates, gate)
    result = {
        "audit_package": repo_rel(AUDIT_PACKAGE_PATH),
        "report_json": repo_rel(REPORT_JSON_PATH),
        "report_md": repo_rel(REPORT_MD_PATH),
        "followup": repo_rel(FOLLOWUP_PATH),
        "gate_status": gate["gate_status"],
        "candidate_count": len(candidates),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
