"""Supplement P37-B-D11 with inline CEK-TA contract and lineage sources.

This script patches the D11 candidate only, exports a one-item third-audit
package, and never creates formal reviewed knowledge, approved knowledge,
default guidance, or hard gates.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 11).isoformat()
TASK_ID = "CEK-TA-392"
PACKAGE_ID = "phase37_data_engineering_d11_contract_inline_third_audit_package_20260611"

ROOT = resolve_repo_path(".", start_file=__file__)
CANDIDATE_PATH = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "candidates",
    "KB_02_DATA_ENGINEERING",
    "cand_20260611_phase37_data_engineering_raw_vs_adjusted_data_boundary_001.json",
    start_file=__file__,
)
CONTRACT_PATH = resolve_repo_path(
    "docs", "contracts", "phase37_data_engineering_dataset_layers_contract.md", start_file=__file__
)
RESEARCH_PATH = resolve_repo_path(
    "docs", "research", "phase37_data_engineering_d11_contract_inline_third_audit_research.md", start_file=__file__
)
AUDIT_PATH = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_data_engineering_d11_contract_inline_third_audit_report.json", start_file=__file__
)


LINEAGE_SOURCES: list[dict[str, Any]] = [
    {
        "source_title": "Object Model",
        "source_url": "https://openlineage.io/docs/spec/object-model/",
        "source_type": "lineage_standard_doc",
        "publisher": "OpenLineage",
        "reliability": "high",
        "score": 88,
        "evidence_summary": (
            "OpenLineage object model defines lineage around Run, Job, Dataset and lineage events as datasets are created "
            "and transformed."
        ),
        "limitations": [
            "Open lineage standard; supports manifest/lineage requirements, not CEK-TA exact physical table names."
        ],
    },
    {
        "source_title": "Facets & Extensibility",
        "source_url": "https://openlineage.io/docs/spec/facets/",
        "source_type": "lineage_standard_doc",
        "publisher": "OpenLineage",
        "reliability": "high",
        "score": 86,
        "evidence_summary": (
            "OpenLineage facets attach structured metadata to Run, Job and Dataset entities, supporting extensible audit context."
        ),
        "limitations": [
            "Facet vocabulary must be mapped into CEK-TA transformation manifest fields by implementation."
        ],
    },
    {
        "source_title": "Dataset Facets",
        "source_url": "https://openlineage.io/docs/spec/facets/dataset-facets/",
        "source_type": "lineage_standard_doc",
        "publisher": "OpenLineage",
        "reliability": "high",
        "score": 85,
        "evidence_summary": (
            "OpenLineage dataset facets provide schema, version, ownership or other dataset-specific metadata for inputs and outputs."
        ),
        "limitations": [
            "Dataset facets support metadata capture; they do not prescribe trading-specific raw/adjusted semantics."
        ],
    },
    {
        "source_title": "ML Metadata",
        "source_url": "https://www.tensorflow.org/tfx/guide/mlmd",
        "source_type": "ml_metadata_doc",
        "publisher": "TensorFlow / TFX",
        "reliability": "high",
        "score": 86,
        "evidence_summary": (
            "ML Metadata records and retrieves metadata for ML workflows and models artifacts, executions, contexts and lineage."
        ),
        "limitations": [
            "ML workflow metadata model; supports feature/label dataset lineage but not market-data layer naming by itself."
        ],
    },
    {
        "source_title": "OpenLineage Integration",
        "source_url": "https://docs.feast.dev/reference/openlineage",
        "source_type": "feature_store_lineage_doc",
        "publisher": "Feast",
        "reliability": "high",
        "score": 84,
        "evidence_summary": (
            "Feast OpenLineage integration documents automatic lineage tracking for ML feature engineering workflows."
        ),
        "limitations": [
            "Feature-store implementation detail; useful for feature-ready lineage, not a universal requirement to use Feast."
        ],
    },
    {
        "source_title": "Tracking Feature Lineage with OpenLineage",
        "source_url": "https://feast.dev/blog/feast-openlineage-integration/",
        "source_type": "feature_store_lineage_doc",
        "publisher": "Feast",
        "reliability": "medium_high",
        "score": 80,
        "evidence_summary": (
            "Feast engineering post explains using OpenLineage for feature-store operations and feature lineage visibility."
        ),
        "limitations": [
            "Product/engineering blog; supporting evidence only, not a normative contract source."
        ],
    },
]


CONTRACT_SCHEMA_EXTRACT = {
    "layers": [
        {
            "name": "raw",
            "semantics": "原始供应商/交易所事实记录，保留 source provenance 和接收时间。",
            "write_boundary": "append-only；不得被清洗、复权、特征或标签回写覆盖。",
            "typical_fields": [
                "source_id",
                "instrument_id",
                "event_time",
                "receive_time",
                "raw_payload_hash",
                "vendor_sequence",
            ],
        },
        {
            "name": "cleaned",
            "semantics": "对 raw 做校验、去重、隔离、修复候选和质量标记后的可计算层。",
            "write_boundary": "只能从 raw 派生；必须记录质量规则、隔离记录和修复记录。",
            "typical_fields": ["quality_flags", "quarantine_reason", "repair_policy_id", "quality_report_id"],
        },
        {
            "name": "adjusted",
            "semantics": "复权、合约换月、连续合约映射或 back-adjusted 数据层。",
            "write_boundary": "只能从 raw/cleaned 派生；必须记录 adjustment_policy_id 和版本。",
            "typical_fields": ["adjustment_policy_id", "adjustment_factor", "roll_rule_id", "adjusted_price"],
        },
        {
            "name": "feature_ready",
            "semantics": "点时正确的特征层，不包含未来标签。",
            "write_boundary": "必须记录 feature_version、available_time 和输入数据版本。",
            "typical_fields": [
                "feature_name",
                "feature_value",
                "feature_version",
                "available_time",
                "source_dataset_version",
            ],
        },
        {
            "name": "label_ready",
            "semantics": "训练/评估标签层，记录 horizon、label policy 和泄漏边界。",
            "write_boundary": "不得回写 raw/cleaned/adjusted；只能作为训练或评估下游输入。",
            "typical_fields": ["label_name", "label_value", "horizon", "label_policy_id", "label_generated_at"],
        },
    ],
    "transformation_manifest_required_fields": [
        "input_layer",
        "output_layer",
        "source_dataset_version",
        "source_table_snapshot",
        "code_version",
        "parameter_hash",
        "produced_at",
        "actor",
        "quality_report_id",
        "lineage_id",
        "rollback_pointer",
    ],
    "hard_boundaries": [
        "downstream layer 不得回写污染 raw layer。",
        "raw 修正必须以 correction record 或新 dataset version 体现，不得静默覆盖。",
        "adjusted 数据不能替代 raw 数据；回测/训练必须声明使用的数据层。",
        "feature_ready 必须有 available_time，不能含未来标签。",
        "label_ready 必须声明 horizon 和 label policy，不能作为特征源回写。",
        "AI Engineering 只能通过 knowledge_refs 引用本契约，不得改写为模型训练或交易执行规则本体。",
    ],
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def append_unique_strings(existing: Any, additions: list[str]) -> list[str]:
    values = [str(item) for item in existing if isinstance(item, str)] if isinstance(existing, list) else []
    for addition in additions:
        if addition not in values:
            values.append(addition)
    return values


def next_source_index(item: dict[str, Any]) -> int:
    max_id = 0
    for src in item.get("source_refs", []):
        if not isinstance(src, dict):
            continue
        match = re.search(r"(\d+)$", str(src.get("source_id", "")))
        if match:
            max_id = max(max_id, int(match.group(1)))
    return max_id + 1


def append_source(item: dict[str, Any], raw: dict[str, Any], index: int) -> None:
    refs = item.setdefault("source_refs", [])
    if any(isinstance(src, dict) and src.get("source_url") == raw["source_url"] for src in refs):
        return
    refs.append(
        {
            "source_id": f"src_{index:03d}",
            "source_title": raw["source_title"],
            "source_url": raw["source_url"],
            "source_type": raw["source_type"],
            "publisher": raw["publisher"],
            "published_at": None,
            "accessed_at": TODAY,
            "version": None,
            "reliability": raw["reliability"],
            "score": raw["score"],
            "relevance": "high",
            "freshness": "time_sensitive",
            "limitations": raw["limitations"],
            "evidence_summary": raw["evidence_summary"],
            "quoted_excerpt_allowed": False,
        }
    )


def has_mojibake(value: object) -> bool:
    return bool(re.search(r"(�|锟|烫|屯|Ã|Â|\?{2,})", json.dumps(value, ensure_ascii=False)))


def patch_candidate(contract_text: str) -> dict[str, Any]:
    item = read_json(CANDIDATE_PATH)
    start = next_source_index(item)
    for offset, source in enumerate(LINEAGE_SOURCES):
        append_source(item, source, start + offset)

    claim = item.setdefault("claim", {})
    claim["statement"] = (
        "外部数据平台可以采用 raw/validated/enriched 或等价分层架构；CEK-TA 内部数据契约则明确使用 "
        "raw、cleaned、adjusted、feature-ready 和 label-ready 层名，并要求调整、清洗、特征和标签产物不得回写污染 raw 层。"
    )
    claim["evidence_summary"] = (
        "Databricks 支撑通用 layered data architecture；Feast 与 MLflow 支撑 point-in-time feature、dataset lineage "
        "和训练/评估数据追踪；OpenLineage 与 ML Metadata 支撑 Run/Job/Dataset、facets、Artifact/Execution/Context "
        "等 lineage 元数据；CEK-TA 内联契约正文定义 exact layer names、write boundaries、transformation manifest、"
        "feature-ready 和 label-ready 判定字段。"
    )
    claim["interpretation_notes"] = (
        "CEK-TA exact layer names 是内部知识库契约，不是所有外部平台强制物理表名；本轮只导出三审包，"
        "外部 AI/人工返回 reviewed_allowed=true 前不得创建 formal reviewed。"
    )
    claim["claim_strength"] = "medium_high_with_internal_contract_caveat"

    applicability = item.setdefault("applicability", {})
    applicability["applies_when"] = [
        "外接项目建立行情湖、研究数据集、回测缓存、特征表、训练集或标签表时",
        "需要把外部 raw/validated/enriched 分层映射到 CEK-TA raw/cleaned/adjusted/feature-ready/label-ready 契约时",
        "需要为跨层转换保留 source_dataset_version、source_table_snapshot、code_version、parameter_hash、lineage_id 和 rollback_pointer 时",
    ]
    applicability["not_applicable_when"] = [
        "只保存单次人工下载文件且不做下游训练、回测或审计复用时",
        "外部事实层已经以只读方式提供不可变 raw layer，且项目只引用不改写时",
        "外部数据库已有等价分层契约时，可映射到 CEK-TA 层名而不是强制复制物理表名",
        "需要具体交易策略参数、账户事实、交易所私有配置、密钥或实盘权限时，应由外接项目事实层处理",
        "AI Engineering 只能引用本规则，不得把本规则改写为模型训练、MCP 或 RAG 本体规则",
    ]
    applicability["limitations"] = append_unique_strings(
        applicability.get("limitations", []),
        [
            "OpenLineage、ML Metadata、Feast、MLflow 和 Databricks 资料支撑 lineage/feature/dataset pattern，不直接规定 CEK-TA exact layer names。",
            "CEK-TA 内部契约现在已内联到三审包，但仍需要外部 AI/人工确认它与正式知识库无冲突。",
            "本候选不提供任何投资建议或实盘执行许可。",
        ],
    )

    source_quality = item.setdefault("source_quality", {})
    refs = [src for src in item.get("source_refs", []) if isinstance(src, dict)]
    source_quality["overall_reliability"] = "medium_high"
    source_quality["score"] = 83.0
    source_quality["score_version"] = "phase37_data_engineering_d11_contract_inline_source_scoring_v1"
    source_quality["primary_source_count"] = 5
    source_quality["supporting_source_count"] = max(len(refs) - 5, 0)
    source_quality["low_reliability_source_count"] = 0
    source_quality["limitations"] = [
        "CEK-TA 内部 contract 正文已内联，可审计 exact layer names 与 write boundary。",
        "OpenLineage / ML Metadata / Feast lineage 来源支撑 transformation manifest 和 feature lineage，但不替代 CEK-TA 内部契约。",
        "Databricks/Feast/MLflow/Delta/Iceberg/DVC 均按 implementation-pattern 或 tool-specific evidence 使用，不得泛化为所有平台强制实现。",
        "正式 reviewed/caveat_only 仍需外部 AI/人工严格审计返回 reviewed_allowed=true。",
    ]

    conflict = item.setdefault("conflict_audit", {})
    conflict["conflict_status"] = "none_known_in_visible_context"
    conflict["resolution_summary"] = (
        "内联契约后未发现与可见 formal knowledge 的直接冲突；但完整 CEK-TA formal KB 仍需三审方检查。"
        "D11 仍为 Trading Engineering 数据工程规则本体，AI Engineering 只能通过 knowledge_refs 引用。"
    )
    conflict["approval_allowed"] = False
    conflict["default_guidance_allowed"] = False
    conflict["hard_gate_allowed"] = False

    status = item.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "needs_more_evidence"
    status["decision_reason"] = (
        "CEK-TA-392 已内联 CEK-TA 数据层契约正文并补 OpenLineage/ML Metadata/Feast lineage 来源；"
        "仍需三审确认是否可进入 formal reviewed/caveat_only。"
    )
    status["updated_at"] = TODAY

    workflow = item.setdefault("workflow", {})
    workflow["stage"] = "supplemented_for_third_reaudit"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["next_action"] = "external_ai_or_human_third_reaudit"
    workflow["formalization_allowed"] = False
    workflow["default_guidance_allowed"] = False
    workflow["approved_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["ai_audit_result_id"] = f"pending_{PACKAGE_ID}"

    machine_gate = item.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = "D11 已补内联契约并等待三审；不得作为默认指导。"
    machine_gate["requires_human_escalation"] = True
    machine_gate["hidden_from_default_queue"] = True

    conversion = item.setdefault("conversion_target", {})
    conversion["target_review_status"] = "blocked_until_contract_inline_third_reaudit"
    conversion["reviewed_allowed"] = False
    conversion["approved_allowed"] = False
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    review = item.setdefault("review", {})
    review["confidence"] = "medium_high"
    review["open_questions"] = [
        "三审是否认可内联 CEK-TA contract 足以支撑 exact layer names 和 raw write-protection？",
        "三审是否认可 OpenLineage / ML Metadata / Feast lineage 来源足以支撑 transformation manifest 与 feature-ready lineage 字段？",
        "三审是否发现与现有 Data Engineering 或 AI Engineering formal 知识的冲突、重叠或需要拆分的 L3 专题？",
    ]
    audit_log = review.setdefault("audit_log", [])
    if not isinstance(audit_log, list):
        audit_log = []
    audit_log.append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "phase37_data_engineering_d11_contract_inline_supplemented",
            "reason": "CEK-TA-392: 内联 CEK-TA 数据层契约正文，补 OpenLineage/ML Metadata/Feast lineage 来源，并导出 D11 三审包。",
            "audit_result_id": f"pending_{PACKAGE_ID}",
        }
    )
    review["audit_log"] = audit_log
    review["ai_audit"] = {
        "audit_result_id": f"pending_{PACKAGE_ID}",
        "source_package_id": PACKAGE_ID,
        "decision": "pending_third_reaudit",
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "required_checks": [
            "contract_inline_full_text_present",
            "contract_schema_extract_present",
            "lineage_sources_present",
            "source_quality_not_overstated",
            "workflow_hidden_from_default_queue_true",
        ],
    }

    item["_third_audit_contract_inline"] = {
        "contract_path": rel_path(CONTRACT_PATH),
        "contract_text_sha_scope": "full_text_in_audit_package",
        "contract_schema_extract": CONTRACT_SCHEMA_EXTRACT,
        "contract_text_preview": contract_text[:1000],
    }

    write_json(CANDIDATE_PATH, item)
    return item


def write_research() -> None:
    content = f"""# Phase 37 Data Engineering D11 契约内联三审补证记录

生成日期：{TODAY}

## 任务

`CEK-TA-392` 只处理 `P37-B-D11 raw_vs_adjusted_data_boundary`，目标是把 CEK-TA 内部数据层契约正文、机器可校验契约摘要和 lineage/feature-store 来源放入三审包。

## 外部来源

| 来源 | 用途 | 边界 |
| --- | --- | --- |
| OpenLineage Object Model | 支撑 Run / Job / Dataset 以及跨转换 lineage event | 不规定 CEK-TA 物理表名 |
| OpenLineage Facets / Dataset Facets | 支撑 schema、version、输入输出 metadata 等 transformation manifest 字段 | 需要映射到项目字段 |
| TensorFlow TFX ML Metadata | 支撑 Artifact / Execution / Context 与 ML workflow lineage | 不定义交易 raw/adjusted 语义 |
| Feast OpenLineage Integration | 支撑 feature engineering lineage 和 feature-ready 血缘 | Feast 不是强制依赖 |

## 内联契约

```text
{rel_path(CONTRACT_PATH)}
```

三审包内同时包含：

```text
contract_inline.full_text
contract_inline.schema_extract.layers
contract_inline.schema_extract.transformation_manifest_required_fields
contract_inline.schema_extract.hard_boundaries
```

## 审计边界

```text
1. candidate 不是正式知识。
2. 本包最多允许 accepted_for_reviewed_caveat_only。
3. 不允许 approved/default guidance/hard gate。
4. 不允许生成交易建议、买卖点、仓位、杠杆或实盘执行许可。
```
"""
    RESEARCH_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_PATH.write_text(content, encoding="utf-8")


def quality_gate(candidate: dict[str, Any], package: dict[str, Any]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    if candidate.get("research_task_id") != "P37-B-D11":
        failures.append({"failure": "candidate_not_p37_b_d11"})
    if candidate.get("workflow", {}).get("stage") != "supplemented_for_third_reaudit":
        failures.append({"failure": "workflow_stage_not_supplemented_for_third_reaudit"})
    if candidate.get("workflow", {}).get("hidden_from_default_queue") is not True:
        failures.append({"failure": "workflow_hidden_from_default_queue_not_true"})
    for key in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed"):
        if candidate.get("workflow", {}).get(key) is not False:
            failures.append({"failure": f"workflow_{key}_not_false"})
    if package.get("contract_inline", {}).get("full_text", "").strip() == "":
        failures.append({"failure": "contract_inline_missing"})
    if len(package.get("candidates", [])) != 1:
        failures.append({"failure": "candidate_count_not_1"})
    if has_mojibake(candidate) or has_mojibake(package):
        failures.append({"failure": "mojibake_marker_detected"})
    return {
        "gate_id": "phase37_data_engineering_d11_contract_inline_third_audit_quality_gate",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "candidate_count": 1,
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "formal_reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_created": 0,
        "hard_gate_created": 0,
    }


def build_package(candidate: dict[str, Any], contract_text: str) -> dict[str, Any]:
    return {
        "package_id": PACKAGE_ID,
        "package_type": "candidate_contract_inline_third_audit_package",
        "schema_version": "1.0.0",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "language": "zh-CN",
        "phase": "37",
        "title": "Phase 37 Data Engineering D11 契约内联三审包",
        "purpose": "严格复审 P37-B-D11 在内联 CEK-TA 数据层契约和补充 lineage 来源后，是否可进入 formal reviewed/caveat_only。",
        "strict_boundaries": [
            "candidate 不是正式知识。",
            "本次审计最多只能允许 accepted_for_reviewed_caveat_only。",
            "不得创建 approved。",
            "不得启用 default guidance。",
            "不得启用 hard gate。",
            "不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
        ],
        "audit_instructions": [
            "必须搜索相关的专业网站、资料、案例和数据，对审计报告进行严格审计。",
            "重点检查内联 CEK-TA contract 是否足以支撑 exact layer names、raw write-protection、feature-ready、label-ready 和 transformation manifest。",
            "重点检查 OpenLineage、ML Metadata、Feast lineage 来源是否足以支撑 lineage manifest 字段，而不是被误用为 CEK-TA 层名来源。",
            "检查 source_quality 是否保守：内部 contract 支撑内部层名，外部标准/工具只支撑通用 pattern 和 lineage。",
            "若发现仍缺少来源、契约、边界、冲突审计或字段一致性，必须返回 needs_more_evidence 或 blocked。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": PACKAGE_ID,
            "auditor": "string",
            "audited_at": "YYYY-MM-DD",
            "quality_gate": {"pass": "boolean", "candidate_count": 1, "notes": ["string"]},
            "decisions": [
                {
                    "candidate_id": "cand_20260611_phase37_data_engineering_raw_vs_adjusted_data_boundary_001",
                    "research_task_id": "P37-B-D11",
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | high",
                    "reviewed_allowed": "boolean",
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "reasons": ["string"],
                    "required_patches": {
                        "source": ["string"],
                        "content": ["string"],
                        "boundary": ["string"],
                        "conflict": ["string"],
                    },
                    "formal_conversion_notes": ["string"],
                }
            ],
        },
        "contract_inline": {
            "path": rel_path(CONTRACT_PATH),
            "full_text": contract_text,
            "schema_extract": CONTRACT_SCHEMA_EXTRACT,
        },
        "source_review_notes": {
            "external_pattern_sources": [
                "Databricks medallion supports layered raw/validated/enriched style architecture.",
                "Feast point-in-time and OpenLineage integration support feature-ready lineage and leakage boundary.",
                "OpenLineage and ML Metadata support lineage/metadata object models for transformations and ML workflows.",
            ],
            "internal_contract_source": "CEK-TA contract supports exact raw/cleaned/adjusted/feature-ready/label-ready names and write boundaries.",
            "source_quality_boundary": "Do not count tool-specific implementation docs as universal platform requirements.",
        },
        "candidates": [candidate],
    }


def main() -> None:
    contract_text = CONTRACT_PATH.read_text(encoding="utf-8")
    candidate = patch_candidate(contract_text)
    write_research()
    package = build_package(candidate, contract_text)
    gate = quality_gate(candidate, package)
    package["quality_gate"] = gate
    write_json(AUDIT_PATH, package)
    report = {
        "report_id": "phase37_data_engineering_d11_contract_inline_third_audit_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "package_id": PACKAGE_ID,
        "candidate_id": candidate["candidate_id"],
        "research_task_id": candidate["research_task_id"],
        "candidate_file": rel_path(CANDIDATE_PATH),
        "contract_path": rel_path(CONTRACT_PATH),
        "research_record": rel_path(RESEARCH_PATH),
        "audit_package": rel_path(AUDIT_PATH),
        "quality_gate": gate,
        "boundary": "Candidate supplement only; no formal reviewed knowledge, approved knowledge, default guidance, hard gate, or MCP index update was created.",
        "next_action": "将三审包交给外部 AI/人工严格审计；若返回 accepted_for_reviewed_caveat_only 且 reviewed_allowed=true，再另起 CEK-TA-393 沉淀 formal reviewed/caveat_only。",
    }
    write_json(REPORT_PATH, report)
    if gate["gate_status"] != "pass":
        raise SystemExit(f"quality gate failed: {gate['failures']}")
    print(json.dumps({"candidate": candidate["candidate_id"], "audit_package": rel_path(AUDIT_PATH)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
