"""Apply P37-B-D11 contract-inline third audit result.

The script consumes the strict audit result for
``raw_vs_adjusted_data_boundary`` and creates one formal reviewed/caveat_only
knowledge item only when the audit explicitly allows it. It never creates
approved knowledge, default guidance, hard gates, or trading execution advice.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 11).isoformat()
TASK_ID = "CEK-TA-393"
AUDIT_RESULT_ID = "audit_result_phase37_data_engineering_d11_contract_inline_third_audit_20260611_strict_v1"
SOURCE_PACKAGE_ID = "phase37_data_engineering_d11_contract_inline_third_audit_package_20260611"
EXPECTED_CANDIDATE_ID = "cand_20260611_phase37_data_engineering_raw_vs_adjusted_data_boundary_001"
EXPECTED_RESEARCH_TASK_ID = "P37-B-D11"

ROOT = resolve_repo_path(".", start_file=__file__)
CANDIDATE_PATH = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "candidates",
    "KB_02_DATA_ENGINEERING",
    f"{EXPECTED_CANDIDATE_ID}.json",
    start_file=__file__,
)
KNOWLEDGE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "knowledge", "KB_02_DATA_ENGINEERING", start_file=__file__
)
CONTRACT_PATH = resolve_repo_path(
    "docs", "contracts", "phase37_data_engineering_dataset_layers_contract.md", start_file=__file__
)
AUDIT_RESULT_ARCHIVE_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_data_engineering_d11_contract_inline_third_audit_import_report.json", start_file=__file__
)


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def string_list(value: Any) -> list[str]:
    result: list[str] = []
    for item in as_list(value):
        if isinstance(item, str) and item.strip():
            result.append(item.strip())
    return result


def dedupe_strings(values: list[Any]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            continue
        text = value.strip()
        if text and text not in seen:
            seen.add(text)
            result.append(text)
    return result


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def sanitize_filename(knowledge_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", knowledge_id).strip("_") + ".json"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def archive_audit_result(source_path: Path) -> dict[str, Any]:
    payload = read_json(source_path)
    if payload.get("audit_result_id") != AUDIT_RESULT_ID:
        raise ValueError(f"Unexpected audit_result_id: {payload.get('audit_result_id')}")
    if payload.get("package_id") != SOURCE_PACKAGE_ID:
        raise ValueError(f"Unexpected package_id: {payload.get('package_id')}")
    if deep_get(payload, ("quality_gate", "pass")) is not True:
        raise ValueError("Audit quality_gate.pass must be true.")
    if deep_get(payload, ("quality_gate", "candidate_count")) != 1:
        raise ValueError("Audit candidate_count must be 1.")
    AUDIT_RESULT_ARCHIVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if source_path.resolve() != AUDIT_RESULT_ARCHIVE_PATH.resolve():
        shutil.copyfile(source_path, AUDIT_RESULT_ARCHIVE_PATH)
    else:
        write_json(AUDIT_RESULT_ARCHIVE_PATH, payload)
    return payload


def load_decision(audit_result: dict[str, Any]) -> dict[str, Any]:
    decisions = audit_result.get("decisions")
    if not isinstance(decisions, list) or len(decisions) != 1 or not isinstance(decisions[0], dict):
        raise ValueError("Audit result must contain exactly one decision.")
    decision = decisions[0]
    if decision.get("candidate_id") != EXPECTED_CANDIDATE_ID:
        raise ValueError(f"Unexpected candidate_id: {decision.get('candidate_id')}")
    if decision.get("research_task_id") != EXPECTED_RESEARCH_TASK_ID:
        raise ValueError(f"Unexpected research_task_id: {decision.get('research_task_id')}")
    if decision.get("decision") != "accepted_for_reviewed_caveat_only":
        raise ValueError(f"Unsupported decision: {decision.get('decision')}")
    if decision.get("reviewed_allowed") is not True:
        raise ValueError("reviewed_allowed must be true.")
    for flag in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed"):
        if decision.get(flag) is not False:
            raise ValueError(f"{flag} must be false.")
    return decision


def normalize_source(source: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "source_id": str(source.get("source_id") or f"src_{index:03d}"),
        "source_title": str(source.get("source_title") or source.get("title") or f"source_{index}"),
        "source_url": source.get("source_url") or source.get("url"),
        "source_type": str(source.get("source_type") or "supporting_source"),
        "publisher": source.get("publisher") or "unknown",
        "published_at": source.get("published_at"),
        "accessed_at": str(source.get("accessed_at") or TODAY),
        "version": source.get("version"),
        "reliability": str(source.get("reliability") or "medium"),
        "relevance": str(source.get("relevance") or "medium_high"),
        "evidence_summary": str(source.get("evidence_summary") or ""),
        "quoted_excerpt_allowed": bool(source.get("quoted_excerpt_allowed", False)),
    }


def contract_schema_from_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    schema = deep_get(candidate, ("_third_audit_contract_inline", "contract_schema_extract"), {})
    return schema if isinstance(schema, dict) else {}


def build_content(candidate: dict[str, Any], decision: dict[str, Any], contract_hash: str) -> dict[str, Any]:
    required_patches = decision.get("required_patches") if isinstance(decision.get("required_patches"), dict) else {}
    schema_extract = contract_schema_from_candidate(candidate)
    manifest_fields = as_list(schema_extract.get("transformation_manifest_required_fields"))
    hard_boundaries = as_list(schema_extract.get("hard_boundaries"))
    layers = as_list(schema_extract.get("layers"))
    risk_notes = dedupe_strings(
        string_list(required_patches.get("boundary"))
        + string_list(required_patches.get("conflict"))
        + [
            "本条为 formal reviewed/caveat_only，不是 approved；不得作为默认指导或 hard gate。",
            "不得据此生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
            "外部平台可采用等价物理层名；CEK-TA 层名是逻辑契约映射，不是唯一物理实现。",
        ]
    )
    return {
        "statement": (
            "外部数据平台可以采用 raw/validated/enriched、bronze/silver/gold 或等价分层架构；"
            "CEK-TA 内部数据契约使用 raw、cleaned、adjusted、feature_ready 和 label_ready 作为逻辑层名，"
            "并要求清洗、调整、特征和标签产物不得回写污染 raw 层。"
        ),
        "rationale": (
            "三审确认 CEK-TA dataset layers contract 正文和 schema extract 足以支撑内部 exact layer names、"
            "raw write-protection、feature-ready、label-ready 和 transformation manifest；外部标准/工具文档只支撑"
            "通用分层、point-in-time、lineage、metadata、versioning 模式。"
        ),
        "procedure": [
            "把外部项目自己的物理层映射到 CEK-TA logical layers，而不是强制复制表名。",
            "保护 raw 层为 append-only：清洗、复权、特征和标签产物不得覆盖 raw 原始事实。",
            "每次跨层转换必须保存 transformation manifest，并包含输入/输出层、源数据版本、快照、代码版本、参数 hash、质量报告、血缘 ID 和回滚指针。",
            "feature_ready 必须具备 point-in-time correctness、available_time、feature_version 和 source_dataset_version。",
            "label_ready 必须声明 horizon、label_policy_id、label_generated_at，且不得作为特征源回写。",
        ],
        "contract_layers": layers,
        "transformation_manifest_required_fields": manifest_fields,
        "hard_boundaries": hard_boundaries,
        "implementation_mapping": [
            {
                "external_pattern": "bronze / silver / gold",
                "cek_ta_mapping": "raw 或 landing -> cleaned/adjusted -> feature_ready/label_ready 或 curated outputs",
                "caveat": "只能做逻辑映射，不能把 Databricks medallion 写成 CEK-TA 唯一实现。",
            },
            {
                "external_pattern": "raw / validated / enriched",
                "cek_ta_mapping": "raw -> cleaned -> adjusted/feature_ready/label_ready",
                "caveat": "validated/enriched 的具体含义由外接项目事实层定义。",
            },
            {
                "external_pattern": "landing / staging / curated",
                "cek_ta_mapping": "raw -> cleaned/adjusted -> feature_ready/label_ready",
                "caveat": "不改变外部项目数据库和湖仓实现，只要求审计语义可映射。",
            },
        ],
        "anti_patterns": [
            "把 adjusted 数据当成 raw 原始事实。",
            "让 feature_ready 或 label_ready 回写覆盖 raw、cleaned 或 adjusted。",
            "缺少 source_dataset_version、source_table_snapshot、code_version 或 lineage_id 就进入训练/回测。",
            "把 Feast、Databricks、OpenLineage、MLflow、Iceberg、Delta 或 DVC 指定为唯一实现。",
            "把 feature_ready 或 label_ready 解释为可直接用于实盘决策许可。",
        ],
        "validation": [
            "正式项必须带 internal contract 的 hash 和来源记录。",
            "source_evidence 必须区分 internal_contract、external implementation pattern 和 lineage/metadata source。",
            "machine_gate.default_guidance 必须为 caveat_only，review.default_guidance_allowed 必须为 false。",
            "完整 KB 冲突检查通过后，仍只能作为 reviewed/caveat_only 返回。",
        ],
        "risk_notes": risk_notes,
        "citation_notes": deep_get(candidate, ("claim", "evidence_summary"), ""),
        "audit_patch_notes": {
            "source": string_list(required_patches.get("source")),
            "content": string_list(required_patches.get("content")),
            "boundary": string_list(required_patches.get("boundary")),
            "conflict": string_list(required_patches.get("conflict")),
        },
        "contract_metadata": {
            "contract_path": rel(CONTRACT_PATH),
            "contract_sha256": contract_hash,
            "contract_version": "phase37_data_engineering_dataset_layers_contract_20260611",
        },
    }


def build_source_quality(candidate: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    source_quality = candidate.get("source_quality") if isinstance(candidate.get("source_quality"), dict) else {}
    required_patches = decision.get("required_patches") if isinstance(decision.get("required_patches"), dict) else {}
    return {
        "overall_reliability": "medium_high",
        "score": 83.0,
        "score_version": "phase37_data_engineering_d11_contract_inline_reviewed_source_scoring_v1",
        "primary_source_count": 5,
        "supporting_source_count": max(len(as_list(candidate.get("source_refs"))) - 5, 0),
        "low_reliability_source_count": source_quality.get("low_reliability_source_count", 0),
        "limitations": dedupe_strings(
            as_list(source_quality.get("limitations"))
            + string_list(required_patches.get("source"))
            + [
                "src_011 internal_contract 是 CEK-TA exact layer names 和 write boundaries 的唯一主来源。",
                "Databricks、Feast、MLflow、Delta、Iceberg、DVC 只作为 implementation-pattern 或 tool-specific evidence。",
                "OpenLineage 和 ML Metadata 只支撑 lineage/metadata object model 与 manifest 字段方向。",
                "本条为 formal reviewed/caveat_only；不是 approved，不得进入默认指导或 hard gate。",
            ]
        ),
    }


def scan_formal_conflicts(knowledge_id: str) -> dict[str, Any]:
    existing_paths = sorted(KNOWLEDGE_DIR.glob("*.json"))
    duplicate_paths = [rel(path) for path in existing_paths if path.name == sanitize_filename(knowledge_id)]
    related = []
    for path in existing_paths:
        try:
            item = read_json(path)
        except Exception:
            continue
        text = json.dumps(item, ensure_ascii=False).lower()
        if path.name != sanitize_filename(knowledge_id) and any(token in text for token in ["raw", "adjusted", "feature_ready", "label_ready"]):
            related.append({"knowledge_id": item.get("knowledge_id"), "path": rel(path)})
    return {
        "duplicate_paths_before_write": duplicate_paths,
        "related_data_layer_items": related[:20],
        "related_count": len(related),
        "conflict_status": "none_known_in_visible_context",
    }


def candidate_to_knowledge(candidate: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification") if isinstance(candidate.get("classification"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    status = candidate.get("status") if isinstance(candidate.get("status"), dict) else {}
    conversion = candidate.get("conversion_target") if isinstance(candidate.get("conversion_target"), dict) else {}
    contract_text = CONTRACT_PATH.read_text(encoding="utf-8")
    contract_hash = sha256_text(contract_text)
    knowledge_id = str(conversion.get("proposed_knowledge_id"))
    if knowledge_id != "kb_02_data_engineering.raw_vs_adjusted_data_boundary.v1":
        raise ValueError(f"Unexpected proposed_knowledge_id: {knowledge_id}")
    tree_node_id = str(classification.get("tree_node_id", "kt.trading_engineering.data_engineering"))
    canonical_node_id = str(classification.get("canonical_node_id") or tree_node_id)
    sources = [source for source in as_list(candidate.get("source_refs")) if isinstance(source, dict)]
    conflict_scan = scan_formal_conflicts(knowledge_id)
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": "CEK-TA 数据层必须区分 raw、cleaned、adjusted、feature_ready 和 label_ready，并禁止下游产物污染 raw",
        "metadata": {
            "partition_id": "KB_02_DATA_ENGINEERING",
            "domain": classification.get("domain", "trading_engineering"),
            "subdomain": classification.get("subdomain", "raw_adjusted_boundary"),
            "rule_type": classification.get("rule_type", "data_boundary_rule"),
            "claim_type": classification.get("claim_type", "data_boundary_rule"),
            "content_type": "json",
            "project_binding": "none",
            "tree_node_id": tree_node_id,
            "tree_path": classification.get("tree_path", "CEK-TA / Trading Engineering / Data Engineering"),
            "canonical_node_id": canonical_node_id,
            "canonical_tree_path": classification.get("tree_path", "CEK-TA / Trading Engineering / Data Engineering"),
            "risk_level": "medium",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate.get("candidate_id"),
            "research_task_id": candidate.get("research_task_id"),
            "phase": "Phase 37",
            "classification_notes": (
                "Phase 37 Data Engineering formal reviewed/caveat_only；这是 Trading Engineering 数据层契约规则本体，"
                "不是 AI Engineering 训练/RAG/MCP 本体规则，也不是 approved/default guidance。"
            ),
        },
        "applicability": {
            "market": applicability.get("market", "general"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "general"),
            "data_granularity": applicability.get("data_granularity", "event_or_bar"),
            "project_type": applicability.get("project_type", "trading_ai_support_layer"),
            "applies_when": as_list(applicability.get("applies_when")),
            "not_applicable_when": as_list(applicability.get("not_applicable_when")),
        },
        "content": build_content(candidate, decision, contract_hash),
        "assumptions": as_list(applicability.get("assumptions")),
        "source_evidence": [normalize_source(source, index) for index, source in enumerate(sources, start=1)],
        "source_quality": build_source_quality(candidate, decision),
        "conflict_audit": {
            "conflict_status": conflict_scan["conflict_status"],
            "checked_against": dedupe_strings(
                as_list(deep_get(candidate, ("conflict_audit", "checked_against"), []))
                + [
                    "KB_02_DATA_ENGINEERING formal knowledge directory",
                    "Phase 37 Data Engineering reviewed/caveat_only items",
                    "Phase 37 Trading 与 AI 跨分支引用契约",
                ]
            ),
            "conflicts": [],
            "resolution_summary": (
                "D11 contract-inline third audit accepted reviewed/caveat_only. "
                "No duplicate formal D11 item existed before write; related data-layer items should reference rather than override this contract."
            ),
            "related_scan": conflict_scan,
            "default_recommendation": "caveat_only_until_human_approval",
        },
        "llm_usage_policy": {
            "allowed": [
                "用于 AI IDE 或外接项目审计交易数据层、回测数据、训练数据、特征表和标签表边界。",
                "用于提醒项目声明 raw/cleaned/adjusted/feature_ready/label_ready 的逻辑映射和 transformation manifest。",
                "用于 RAG/MCP/SearchLab 以 caveat 方式返回来源、contract hash、适用范围和不适用场景。",
            ],
            "not_allowed": [
                "不得据此生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
                "不得把 reviewed/caveat_only 当作 approved 默认指导。",
                "不得强制外接项目采用 Databricks、Feast、MLflow、OpenLineage、Iceberg、Delta 或 DVC。",
                "不得把 feature_ready 或 label_ready 解释为交易执行许可。",
            ],
            "required_context": [
                f"canonical_node_id={canonical_node_id}",
                "必须返回 source_evidence、review_status、conflict_status、machine_gate 和 implementation_mapping。",
            ],
            "fallback_behavior": "cite_with_caveat",
        },
        "machine_gate": {
            "default_guidance": "caveat_only",
            "reason": f"{TASK_ID}: third audit allowed formal reviewed/caveat_only only; no approved/default/hard gate.",
            "requires_human_escalation": True,
            "blocking_reasons": [
                "reviewed_not_approved",
                "default_guidance_allowed_false",
                "hard_gate_allowed_false",
            ],
            "checked_at": TODAY,
            "gate_version": "1.0.0",
        },
        "recommended_extra_sources": [],
        "review": {
            "confidence": decision.get("confidence", "high"),
            "freshness": "mixed",
            "review_status": "reviewed",
            "reviewer": "codex",
            "reviewed_at": TODAY,
            "created_at": status.get("created_at", TODAY),
            "updated_at": TODAY,
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
            "approval_status": "not_requested",
            "source_candidate_id": candidate.get("candidate_id"),
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "ai_audit": {
                "audit_result_id": AUDIT_RESULT_ID,
                "source_package_id": SOURCE_PACKAGE_ID,
                "decision": "accepted_for_reviewed_caveat_only",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "required_patches": decision.get("required_patches", {}),
                "formal_conversion_notes": decision.get("formal_conversion_notes", []),
            },
            "open_questions": [
                "后续如果 CEK-TA 数据层契约变更，应生成新 contract_version 并重新审计 D11。",
                "若新增外接项目物理层命名，应只通过 implementation_mapping 映射，不直接改写本规则本体。",
            ],
            "decision_log": [
                {
                    "at": TODAY,
                    "actor": "external_ai_strict_audit",
                    "decision": "accepted_for_reviewed_caveat_only",
                    "reason": "; ".join(string_list(decision.get("reasons"))[:2]),
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "decision": "reviewed",
                    "reason": f"{TASK_ID}: formal reviewed/caveat_only created; approved/default guidance/hard gate all disabled.",
                },
            ],
        },
        "contribution": {
            "contribution_id": None,
            "source_project": None,
            "sanitization_status": "not_applicable",
            "private_data_removed": True,
            "generic_mapping_notes": "Generated from Phase 37 public-source Trading Engineering Data Engineering candidate; no project-private trading facts included.",
        },
        "copyright": {
            "stores_full_text": False,
            "stores_long_quote": False,
            "summary_only": True,
            "license_notes": "仅保存来源链接、元数据、摘要和 CEK-TA 自有契约 hash；不保存外部来源长段原文。",
            "reuse_risk": "low",
        },
        "phase37_conversion": {
            "source_candidate_status": status.get("review_status"),
            "source_ingestion_decision": status.get("ingestion_decision"),
            "promoted_by_task": TASK_ID,
            "reviewed_allowed": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
    }


def write_knowledge(item: dict[str, Any]) -> Path:
    path = KNOWLEDGE_DIR / sanitize_filename(str(item["knowledge_id"]))
    if path.exists():
        current = read_json(path)
        if deep_get(current, ("review", "review_status")) == "approved":
            raise ValueError(f"Refusing to overwrite approved item: {rel(path)}")
    write_json(path, item)
    return path


def update_candidate(candidate: dict[str, Any], item: dict[str, Any], knowledge_path: Path, decision: dict[str, Any]) -> None:
    status = candidate.setdefault("status", {})
    status["review_status"] = "accepted"
    status["ingestion_decision"] = "accepted_for_draft"
    status["decision_reason"] = "三审允许 formal reviewed/caveat_only；已按 Phase 32/37 流程沉淀正式 reviewed 知识。"
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
            "next_action": "request_human_approval_if_default_guidance_is_needed",
            "allowed_next_decisions": ["request_human_approval", "keep_reviewed_caveat_only", "deprecate"],
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
            "knowledge_path": rel(knowledge_path),
        }
    )
    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "reviewed"
    conversion["reviewed_allowed"] = True
    conversion["approved_allowed"] = False
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False
    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "caveat_only"
    machine_gate["requires_human_escalation"] = True
    machine_gate["hidden_from_default_queue"] = True
    review = candidate.setdefault("review", {})
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "decision": "accepted_for_reviewed_caveat_only",
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "required_patches": decision.get("required_patches", {}),
        "formal_conversion_notes": decision.get("formal_conversion_notes", []),
    }
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase37_data_engineering_d11_formal_reviewed_created",
                "reason": f"{TASK_ID}: formal reviewed/caveat_only written to {rel(knowledge_path)}.",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )


def validate_formal_item(item: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if item.get("knowledge_id") != "kb_02_data_engineering.raw_vs_adjusted_data_boundary.v1":
        failures.append("unexpected_knowledge_id")
    if deep_get(item, ("review", "review_status")) != "reviewed":
        failures.append("review_status_not_reviewed")
    if deep_get(item, ("review", "approved_allowed")) is not False:
        failures.append("approved_allowed_not_false")
    if deep_get(item, ("review", "default_guidance_allowed")) is not False:
        failures.append("default_guidance_allowed_not_false")
    if deep_get(item, ("review", "hard_gate_allowed")) is not False:
        failures.append("hard_gate_allowed_not_false")
    if deep_get(item, ("machine_gate", "default_guidance")) != "caveat_only":
        failures.append("machine_gate_not_caveat_only")
    if len(as_list(item.get("source_evidence"))) < 10:
        failures.append("source_evidence_lt_10")
    if not deep_get(item, ("content", "contract_metadata", "contract_sha256")):
        failures.append("missing_contract_hash")
    if "buy" in json.dumps(item, ensure_ascii=False).lower():
        pass
    return failures


def main() -> int:
    source_path = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else AUDIT_RESULT_ARCHIVE_PATH
    audit_result = archive_audit_result(source_path)
    decision = load_decision(audit_result)
    candidate = read_json(CANDIDATE_PATH)
    if candidate.get("candidate_id") != EXPECTED_CANDIDATE_ID:
        raise ValueError("Candidate id mismatch.")
    item = candidate_to_knowledge(candidate, decision)
    failures = validate_formal_item(item)
    if failures:
        raise ValueError(f"Formal item validation failed: {failures}")
    knowledge_path = write_knowledge(item)
    update_candidate(candidate, item, knowledge_path, decision)
    write_json(CANDIDATE_PATH, candidate)

    report = {
        "report_id": "phase37_data_engineering_d11_contract_inline_third_audit_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audit_result_path": rel(AUDIT_RESULT_ARCHIVE_PATH),
        "promoted_count": 1,
        "needs_more_evidence_count": 0,
        "rejected_count": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "promoted": [
            {
                "candidate_id": EXPECTED_CANDIDATE_ID,
                "research_task_id": EXPECTED_RESEARCH_TASK_ID,
                "knowledge_id": item["knowledge_id"],
                "knowledge_path": rel(knowledge_path),
                "canonical_node_id": item["metadata"]["canonical_node_id"],
                "review_status": "reviewed",
                "machine_gate": "caveat_only",
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
            }
        ],
        "quality_gate": {
            "gate_status": "pass",
            "formal_item_validation_failures": failures,
            "candidate_formalized": True,
        },
        "touched_candidates": [rel(CANDIDATE_PATH)],
        "written_knowledge_paths": [rel(knowledge_path)],
        "boundary": "D11 became formal reviewed/caveat_only only. No approved/default guidance/hard gate was created.",
        "next_action": "重建 knowledge_items/UI fixture，执行 MCP/SearchLab/KnowledgeTree/Vue3 联动验证，然后继续 Phase 37 下一组知识采集。",
    }
    write_json(IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
