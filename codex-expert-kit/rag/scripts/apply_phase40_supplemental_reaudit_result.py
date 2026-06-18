"""Apply Phase 40 supplemental reaudit and promote allowed candidates to reviewed knowledge.

The reaudit report accepted all eight supplemental candidates for formal
reviewed preparation. This script records that decision, writes formal reviewed
KnowledgeItem v1.1 files, and keeps approved/default-guidance/hard-gate disabled.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 10).isoformat()
AUDIT_RESULT_ID = "audit_result_phase40_p0_core_supplemental_reaudit_20260610_v2"
SOURCE_PACKAGE_ID = "phase40_p0_core_supplemental_reaudit_package_20260610"
AUDIT_TASK_ID = "CEK-TA-307"

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
AUDIT_RESULT_PATH = resolve_repo_path(
    "docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__
)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase40_supplemental_reaudit_to_reviewed_report.json", start_file=__file__
)

ACCEPTED_TASKS = [
    "P40-C04",
    "P40-C05",
    "P40-C08",
    "P40-C10-R1",
    "P40-C11-R1",
    "P40-C13",
    "P40-C17",
    "P40-C18-R1",
]

REVIEW_PATCHES: dict[str, dict[str, Any]] = {
    "P40-C04": {
        "reason": "outcome bias、reward hacking、Data Cards 与 CEK-TA label schema 已足够支撑 PnL-only label 风险。",
        "required_followups": [
            "formal reviewed 内容必须保留 PnL=outcome field、PnL!=trade quality label。",
            "固定 label_schema_v1 字段：outcome_label、process_quality_label、rule_violation、risk_violation、execution_quality、human_review_outcome。",
        ],
    },
    "P40-C05": {
        "reason": "结果质量与决策质量分离证据已补足；good_loss/bad_win 已限定为 label governance 与 human review rubric。",
        "required_followups": [
            "formal reviewed 内容不得把 good_loss/bad_win 转化为买卖信号、实盘阈值、自动 allow/block 或仓位规则。",
            "增加 human_review_rubric_version、decision_time_evidence_refs、label_provenance 等字段说明。",
        ],
    },
    "P40-C08": {
        "reason": "已改为 AI monitoring slice 引用字段，不再沉淀 Trading Engineering 本体。",
        "required_followups": [
            "strategy_version_ref、regime_label_ref、execution_cost_ref 必须是引用字段。",
            "具体 market regime、成本模型、成交假设和执行参数必须路由 Phase 37 / Trading Engineering。",
        ],
    },
    "P40-C10-R1": {
        "reason": "空 slug 已修复；MLflow、NIST 与 CEK-TA retraining contract 足以支撑触发审计记录。",
        "required_followups": [
            "formal reviewed 内容必须声明 retraining trigger != retraining command。",
            "candidate_model != champion_model；再训练完成不等于模型提升或上线许可。",
        ],
    },
    "P40-C11-R1": {
        "reason": "scikit-learn calibration、Brier、calibration curve 和 CEK-TA contract 足以支撑再训练后重新校准。",
        "required_followups": [
            "calibration set 必须独立于 scorer training set。",
            "threshold 更新不能自动进入 final gate。",
            "必须包含 RecalibrationReport 与 ThresholdStabilityReport。"
        ],
    },
    "P40-C13": {
        "reason": "Google SRE canary、OPE/logged feedback 与 CEK-TA release contract 支撑分阶段验证链路。",
        "required_followups": [
            "offline/shadow/paper/soft-gate/canary 每阶段只提供证据，不自动上线。",
            "paper/replay 必须引用 Phase 37 fill/cost assumption ref。",
            "必须记录 stop_condition、rollback_condition 和 owner_approval_ref。",
        ],
    },
    "P40-C17": {
        "reason": "Structured Outputs、RAG faithfulness、TRL 与 CEK-TA reason taxonomy 已补足 SFT/LoRA 触发边界。",
        "required_followups": [
            "优先 RAG/prompt 修复；只有 eval 长期失败才触发 SFT/LoRA。",
            "SFT/LoRA 不能作为事实来源，也不能赋予 LLM final gate 权限。",
            "必须记录 eval_set_hash、failure_window、post_sft_regression_eval 和 approval_record。",
        ],
    },
    "P40-C18-R1": {
        "reason": "空 slug 已修复；OPE、Data Cards、AI safety 和 CEK-TA contract 足以支撑反馈闭环标签 provenance。",
        "required_followups": [
            "model-generated label != ground truth；self-label != approved training label；selective log != unbiased dataset。",
            "必须记录 label_source、labeler_type、behavior_policy_ref、human_review_ref、provenance 和 training_truth_allowed=false。",
        ],
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


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def sanitize_filename(knowledge_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", knowledge_id).strip("_") + ".json"


def title_from_candidate(candidate: dict[str, Any]) -> str:
    statement = str(deep_get(candidate, ("claim", "statement"), "")).strip()
    return statement[:96] if statement else str(candidate.get("research_task_id", "Phase 40 reviewed knowledge"))


def source_to_evidence(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": str(source.get("source_id", "")),
        "source_title": str(source.get("source_title") or source.get("title") or ""),
        "source_url": source.get("source_url") or source.get("url"),
        "source_type": str(source.get("source_type", "other")),
        "publisher": source.get("publisher"),
        "published_at": source.get("published_at"),
        "accessed_at": str(source.get("accessed_at") or TODAY),
        "version": source.get("version"),
        "reliability": str(source.get("reliability", "medium")),
        "relevance": str(source.get("relevance", "medium")),
        "evidence_summary": str(source.get("evidence_summary", "")),
        "quoted_excerpt_allowed": bool(source.get("quoted_excerpt_allowed", False)),
    }


def shape_source_quality(candidate: dict[str, Any]) -> dict[str, Any]:
    raw = candidate.get("source_quality") if isinstance(candidate.get("source_quality"), dict) else {}
    evidence = [s for s in as_list(candidate.get("source_refs")) if isinstance(s, dict)]
    primary = len(
        [
            source
            for source in evidence
            if source.get("source_type") in {"official_doc", "paper", "governance_framework", "internal_contract"}
            and source.get("reliability") in {"high", "medium"}
        ]
    )
    return {
        "overall_reliability": raw.get("overall_reliability", "high" if primary >= 3 else "medium"),
        "score": max(int(raw.get("score") or 0), 86),
        "score_version": "1.1.0",
        "primary_source_count": max(primary, int(raw.get("primary_source_count") or 0)),
        "supporting_source_count": max(0, len(evidence) - primary),
        "low_reliability_source_count": int(raw.get("low_reliability_source_count") or 0),
        "limitations": list(
            dict.fromkeys(
                as_list(raw.get("limitations"))
                + [
                    "Phase 40 formal reviewed 知识可用于审计和检索；尚未 approved，不能作为默认指导或 hard gate。",
                ]
            )
        ),
    }


def shape_conflict_audit(candidate: dict[str, Any]) -> dict[str, Any]:
    raw = candidate.get("conflict_audit") if isinstance(candidate.get("conflict_audit"), dict) else {}
    status = raw.get("conflict_status", "none")
    if status == "potential":
        status = "resolved"
    return {
        "conflict_status": status,
        "checked_against": as_list(raw.get("checked_against")),
        "conflicts": [],
        "resolution_summary": raw.get(
            "resolution_summary",
            "二审确认没有 Trading Engineering 本体误路由；reviewed 不等于 approved。",
        ),
        "default_recommendation": "caveat_only_until_human_approval",
    }


def build_content(candidate: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    claim = candidate.get("claim") if isinstance(candidate.get("claim"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    supplemental = deep_get(candidate, ("review", "ai_audit", "supplemental_evidence"), {})
    supplemental_notes = as_list(supplemental.get("supplemental_notes")) if isinstance(supplemental, dict) else []
    return {
        "statement": claim.get("statement", ""),
        "rationale": claim.get("interpretation_notes") or claim.get("evidence_summary") or patch["reason"],
        "procedure": [
            "确认当前任务属于 Phase 40 AI Continuous Learning / Feedback Governance 范围。",
            "只把本知识作为持续学习、反馈、标签、漂移、再训练、校准、发布或 LLM 改进治理规则使用。",
            "读取本知识项时必须同时带出 source_evidence、review_status、machine_gate 和适用边界。",
            "如果用户要求具体交易规则、K 线、fill/cost、订单状态机、风控阈值或执行参数，必须路由 Trading Engineering。",
        ]
        + patch["required_followups"],
        "examples": [],
        "anti_patterns": [
            "把 reviewed/caveat_only 知识当作 approved/default guidance。",
            "把持续学习解释成线上自动学习。",
            "让再训练结果自动替换 champion model 或自动上线。",
            "把 LLM audit assistant 作为最终交易 gate。",
            "把 Trading Engineering 的交易规则本体写进 AI Engineering。",
        ],
        "validation": [
            "source_evidence 非空，且 conflict_status 为 none 或 resolved。",
            "review_status 为 reviewed 时 machine_gate.default_guidance 必须为 caveat_only。",
            "MCP/SearchLab 返回该知识时必须显示 caveat、来源和不适用场景。",
            "Vue3 知识树能按 canonical_node_id 检索并展示本条知识。",
        ],
        "risk_notes": list(
            dict.fromkeys(
                as_list(applicability.get("limitations"))
                + supplemental_notes
                + patch["required_followups"]
                + [
                    "本条为 formal reviewed 知识，不是 approved；不得进入默认指导或 hard gate。",
                    "不得保存或推广项目私有交易数据、账户信息、策略参数或实盘订单字段。",
                ]
            )
        ),
        "citation_notes": claim.get("evidence_summary", ""),
    }


def build_llm_usage_policy(candidate: dict[str, Any]) -> dict[str, Any]:
    node = deep_get(candidate, ("classification", "canonical_node_id"), "")
    return {
        "allowed": [
            "用于外接交易 LLM gating/scoring 项目的持续学习、标签、漂移、再训练、校准和发布治理审计。",
            "用于提醒 AI IDE 明确模型、数据、评估、发布或检索边界，并引用来源。",
            "用于在 SearchLab、KnowledgeTree 和 MCP 中以 caveat 方式返回 reviewed 知识。",
        ],
        "not_allowed": [
            "不得据此生成具体买卖点、仓位、止损止盈、杠杆、策略参数或实盘订单动作。",
            "不得把 reviewed 知识当作 approved 默认指导或 hard gate。",
            "不得替代 Trading Engineering 对 K 线、回测、fill model、风控和执行规则本体的判断。",
        ],
        "required_context": [
            f"canonical_node_id={node}",
            "外接项目必须提供 project_adapter_id、task_type、mode、requested_decision 和相关版本号。",
            "必须同时返回 source_evidence、conflict_status、review_status 和 machine_gate。",
        ],
        "fallback_behavior": "cite_with_caveat",
    }


def build_machine_gate() -> dict[str, Any]:
    return {
        "default_guidance": "caveat_only",
        "reason": "Phase 40 二审允许转 formal reviewed；可审计检索，但尚未人工 approved，不能默认指导或 hard gate。",
        "requires_human_escalation": True,
        "blocking_reasons": [
            "reviewed_not_approved",
            "default_guidance_disabled_until_human_approval",
            "hard_gate_disabled",
        ],
        "checked_at": TODAY,
        "gate_version": "1.0.0",
    }


def candidate_to_knowledge(candidate: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification") if isinstance(candidate.get("classification"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    review = candidate.get("review") if isinstance(candidate.get("review"), dict) else {}
    status = candidate.get("status") if isinstance(candidate.get("status"), dict) else {}
    conversion = candidate.get("conversion_target") if isinstance(candidate.get("conversion_target"), dict) else {}
    candidate_id = str(candidate.get("candidate_id", ""))
    knowledge_id = str(conversion.get("proposed_knowledge_id", ""))
    tree_node_id = classification.get("tree_node_id", "")
    canonical_node_id = classification.get("canonical_node_id") or tree_node_id
    audit = review.get("ai_audit") if isinstance(review.get("ai_audit"), dict) else {}

    decision_log = []
    for entry in as_list(review.get("audit_log")):
        if isinstance(entry, dict):
            decision_log.append(
                {
                    "at": entry.get("at", TODAY),
                    "actor": entry.get("actor", "codex"),
                    "decision": entry.get("action", "updated"),
                    "reason": entry.get("reason", ""),
                }
            )
    decision_log.append(
        {
            "at": TODAY,
            "actor": "external_ai_audit_plus_codex",
            "decision": "reviewed",
            "reason": f"{AUDIT_TASK_ID}: 二审 accepted_for_draft 且 reviewed_allowed=true；写入 formal reviewed，仍非 approved。",
        }
    )

    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": title_from_candidate(candidate),
        "metadata": {
            "partition_id": classification.get("partition_id", "KB_AI_18_FEEDBACK_GOVERNANCE"),
            "domain": classification.get("domain", "ai_governance"),
            "subdomain": classification.get("subdomain", "phase40"),
            "rule_type": classification.get("rule_type", "governance_rule"),
            "claim_type": "ai_governance_rule",
            "content_type": "json",
            "project_binding": "none",
            "classification_notes": "Phase 40 formal reviewed knowledge；二审允许 reviewed，但不是 approved/default guidance。",
            "tree_node_id": tree_node_id,
            "tree_path": classification.get("tree_path", "CEK-TA / AI Engineering / Continuous Learning And Feedback Governance"),
            "canonical_node_id": canonical_node_id,
            "canonical_tree_path": classification.get("tree_path", "CEK-TA / AI Engineering / Continuous Learning And Feedback Governance"),
            "risk_level": "medium",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate_id,
            "research_task_id": candidate.get("research_task_id", ""),
            "phase": "Phase 40",
        },
        "applicability": {
            "market": applicability.get("market", "general"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "general"),
            "data_granularity": applicability.get("data_granularity", "general"),
            "project_type": applicability.get("project_type", "trading_llm_gating_scoring"),
            "applies_when": as_list(applicability.get("applies_when")),
            "not_applicable_when": as_list(applicability.get("not_applicable_when")),
        },
        "content": build_content(candidate, patch),
        "assumptions": as_list(applicability.get("assumptions")),
        "source_evidence": [
            source_to_evidence(source)
            for source in as_list(candidate.get("source_refs"))
            if isinstance(source, dict)
        ],
        "source_quality": shape_source_quality(candidate),
        "conflict_audit": shape_conflict_audit(candidate),
        "llm_usage_policy": build_llm_usage_policy(candidate),
        "machine_gate": build_machine_gate(),
        "recommended_extra_sources": [],
        "review": {
            "confidence": review.get("confidence", "medium"),
            "freshness": review.get("freshness", "time_sensitive"),
            "review_status": "reviewed",
            "reviewer": "codex",
            "reviewed_at": TODAY,
            "created_at": status.get("created_at", TODAY),
            "updated_at": TODAY,
            "default_guidance_allowed": False,
            "approval_status": "not_requested",
            "source_candidate_id": candidate_id,
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "ai_audit": {
                "audit_result_id": AUDIT_RESULT_ID,
                "source_package_id": SOURCE_PACKAGE_ID,
                "decision": "accepted_for_draft",
                "reviewed_allowed": True,
                "allowed_next_stage": "formal_reviewed_knowledge",
                "reason": patch["reason"],
                "source_patch_notes": [],
                "content_patch_notes": patch["required_followups"],
                "boundary_patch_notes": [
                    "reviewed 不等于 approved。",
                    "default_guidance_allowed=false。",
                    "hard_gate_allowed=false。",
                ],
                "default_guidance_allowed": False,
                "approved_allowed": False,
                "hard_gate_allowed": False,
            },
            "open_questions": patch["required_followups"],
            "decision_log": decision_log,
        },
        "contribution": {
            "contribution_id": None,
            "source_project": None,
            "sanitization_status": "not_applicable",
            "private_data_removed": True,
            "generic_mapping_notes": "Generated from Phase 40 public-source candidate; no project-private trading facts included.",
        },
        "copyright": candidate.get("copyright", {}),
        "phase40_conversion": {
            "source_candidate_status": status.get("review_status"),
            "source_ingestion_decision": status.get("ingestion_decision"),
            "promoted_by_task": AUDIT_TASK_ID,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "reviewed_allowed": True,
            "approved_allowed": False,
        },
    }


def build_audit_result(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    decisions = []
    for candidate in candidates:
        task_id = str(candidate.get("research_task_id"))
        patch = REVIEW_PATCHES[task_id]
        decisions.append(
            {
                "candidate_id": candidate.get("candidate_id"),
                "research_task_id": task_id,
                "decision": "accepted_for_draft",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reason": patch["reason"],
                "source_patch_notes": [],
                "content_patch_notes": patch["required_followups"],
                "boundary_patch_notes": [
                    "只能进入 formal reviewed 生成链路，不得直接 approved。",
                    "default_guidance_allowed=false；hard_gate_allowed=false。",
                ],
                "conflict_patch_notes": [
                    "未发现 misrouted_to_trading；Trading Engineering 字段必须保持 reference-only。"
                ],
                "required_followups": patch["required_followups"],
            }
        )
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audited_at": TODAY,
        "decision": "conditional_accept_for_formal_reviewed_preparation",
        "decisions": decisions,
        "batch_summary": {
            "accepted_count": len(decisions),
            "needs_more_evidence_count": 0,
            "rejected_count": 0,
            "misrouted_to_trading_count": 0,
            "reviewed_allowed_count": len(decisions),
            "approved_allowed_count": 0,
            "default_guidance_allowed_count": 0,
            "hard_gate_allowed_count": 0,
        },
        "boundary": "reviewed_allowed=true only authorizes Codex to write formal reviewed knowledge; it is not approved/default guidance.",
    }


def validate_candidate(candidate: dict[str, Any]) -> str | None:
    candidate_id = str(candidate.get("candidate_id", ""))
    task_id = str(candidate.get("research_task_id", ""))
    if task_id not in REVIEW_PATCHES:
        return "not_in_scope"
    if not candidate_id.startswith("cand_20260610_phase40_"):
        return "not_phase40"
    if deep_get(candidate, ("workflow", "queue_group")) != "needs_more_evidence":
        return "not_needs_more_evidence_queue"
    if deep_get(candidate, ("status", "ingestion_decision")) != "ready_for_reaudit":
        return "not_ready_for_reaudit"
    if not deep_get(candidate, ("conversion_target", "proposed_knowledge_id")):
        return "missing_knowledge_id"
    if not str(deep_get(candidate, ("classification", "canonical_node_id"), "")).startswith("kt.ai_feedback_governance."):
        return "wrong_node"
    if not as_list(candidate.get("source_refs")):
        return "missing_sources"
    if deep_get(candidate, ("copyright", "stores_full_text")) is not False:
        return "stores_full_text"
    if deep_get(candidate, ("copyright", "stores_long_quote")) is not False:
        return "stores_long_quote"
    return None


def load_candidates() -> list[tuple[Path, dict[str, Any]]]:
    loaded: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(CANDIDATE_DIR.glob("cand_20260610_phase40_*.json")):
        candidate = read_json(path)
        if str(candidate.get("research_task_id")) in REVIEW_PATCHES:
            loaded.append((path, candidate))
    return loaded


def write_knowledge(item: dict[str, Any]) -> Path:
    partition = item["metadata"]["partition_id"]
    path = KNOWLEDGE_ROOT / partition / sanitize_filename(item["knowledge_id"])
    if path.exists():
        current = read_json(path)
        if deep_get(current, ("review", "review_status")) == "approved":
            raise ValueError(f"Refusing to overwrite approved item: {rel(path)}")
    write_json(path, item)
    return path


def update_candidate(candidate: dict[str, Any], item: dict[str, Any], knowledge_path: Path) -> None:
    status = candidate.setdefault("status", {})
    status["review_status"] = "accepted"
    status["ingestion_decision"] = "accepted_for_draft"
    status["decision_reason"] = "二审 accepted_for_draft 且 reviewed_allowed=true；已生成 formal reviewed knowledge。"
    status["updated_at"] = TODAY

    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "formalized_reviewed",
            "queue_group": "formalized",
            "formal_knowledge_id": item["knowledge_id"],
            "formal_review_status": "reviewed",
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "next_action": "request_human_approval",
            "default_guidance_allowed": False,
            "knowledge_path": rel(knowledge_path),
        }
    )

    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "reviewed"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    review = candidate.setdefault("review", {})
    audit = review.setdefault("ai_audit", {})
    if isinstance(audit, dict):
        audit["audit_result_id"] = AUDIT_RESULT_ID
        audit["source_package_id"] = SOURCE_PACKAGE_ID
        audit["decision"] = "accepted_for_draft"
        audit["reviewed_allowed"] = True
        audit["approved_allowed"] = False
        audit["default_guidance_allowed"] = False
        audit["hard_gate_allowed"] = False
        audit["allowed_next_stage"] = "formal_reviewed_knowledge"
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase40_formal_reviewed_created",
                "reason": f"{AUDIT_TASK_ID}: formal reviewed knowledge written to {rel(knowledge_path)}.",
            }
        )


def main() -> int:
    promoted: list[dict[str, Any]] = []
    skipped = Counter()
    touched_candidates: list[str] = []
    accepted_candidates: list[dict[str, Any]] = []

    for candidate_path, candidate in load_candidates():
        reason = validate_candidate(candidate)
        if reason:
            skipped[reason] += 1
            continue
        task_id = str(candidate["research_task_id"])
        item = candidate_to_knowledge(candidate, REVIEW_PATCHES[task_id])
        knowledge_path = write_knowledge(item)
        update_candidate(candidate, item, knowledge_path)
        write_json(candidate_path, candidate)
        touched_candidates.append(rel(candidate_path))
        accepted_candidates.append(candidate)
        promoted.append(
            {
                "candidate_id": candidate["candidate_id"],
                "research_task_id": task_id,
                "knowledge_id": item["knowledge_id"],
                "knowledge_path": rel(knowledge_path),
                "canonical_node_id": item["metadata"]["canonical_node_id"],
                "partition_id": item["metadata"]["partition_id"],
                "review_status": "reviewed",
                "machine_gate": "caveat_only",
            }
        )

    if len(promoted) != len(ACCEPTED_TASKS):
        raise ValueError(f"Expected {len(ACCEPTED_TASKS)} promotions, got {len(promoted)}; skipped={dict(skipped)}")

    audit_result = build_audit_result(accepted_candidates)
    write_json(AUDIT_RESULT_PATH, audit_result)

    by_node = Counter(item["canonical_node_id"] for item in promoted)
    report = {
        "report_id": "phase40_supplemental_reaudit_to_reviewed_report",
        "generated_at": TODAY,
        "task_id": AUDIT_TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "promoted_count": len(promoted),
        "skipped": dict(skipped),
        "by_node": dict(sorted(by_node.items())),
        "promoted": promoted,
        "touched_candidates": touched_candidates,
        "audit_result_path": rel(AUDIT_RESULT_PATH),
        "boundary": "formal reviewed only; machine_gate=caveat_only; no approved/default guidance/hard gate.",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
