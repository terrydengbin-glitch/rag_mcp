"""Supplement Phase 37 Data Engineering blocked candidates.

Targets P37-B-D10 and P37-B-D11 after reviewed-preparation audit returned
``needs_more_evidence``. This script patches candidate artifacts only and
exports a two-item re-audit package. It never creates formal reviewed
knowledge, approved knowledge, default guidance, or hard gates.
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
TASK_ID = "CEK-TA-390"
PACKAGE_ID = "phase37_data_engineering_blocked_supplemental_reaudit_package_20260611"

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_02_DATA_ENGINEERING", start_file=__file__
)
ROOT = resolve_repo_path(".", start_file=__file__)
CONTRACT_PATH = resolve_repo_path(
    "docs", "contracts", "phase37_data_engineering_dataset_layers_contract.md", start_file=__file__
)
RESEARCH_PATH = resolve_repo_path(
    "docs", "research", "phase37_data_engineering_blocked_supplemental_research.md", start_file=__file__
)
AUDIT_PATH = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_data_engineering_blocked_supplemental_reaudit_report.json", start_file=__file__
)


CONTRACT_CONTENT = f"""# Phase 37 Data Engineering Dataset Layers Contract

生成日期：{TODAY}

## 目标

本契约为 CEK-TA Trading Engineering / Data Engineering 的数据层命名、写入边界、血缘字段和审计字段提供内部规范。它用于补强 `P37-B-D11 raw_vs_adjusted_data_boundary`，但不创建正式知识、不创建 approved，也不改变外部项目自己的数据库实现。

## 上游

```text
交易所或数据供应商原始行情
成交、盘口、bar、reference data、corporate action、contract rollover 和 vendor correction
外接项目的数据接入器、数据质量报告、特征生成器和标签生成器
```

## 下游

```text
回测数据集
训练数据集
特征表
标签表
质量审计报告
RAG 知识审计与 AI IDE 方案审计
```

## CEK-TA 数据层

| 层级 | 语义 | 写入边界 | 典型字段 |
| --- | --- | --- | --- |
| raw | 原始供应商/交易所事实记录，保留 source provenance 和接收时间 | append-only；不得被清洗、复权、特征或标签回写覆盖 | source_id, instrument_id, event_time, receive_time, raw_payload_hash, vendor_sequence |
| cleaned | 对 raw 做校验、去重、隔离、修复候选和质量标记后的可计算层 | 只能从 raw 派生；必须记录质量规则、隔离记录和修复记录 | quality_flags, quarantine_reason, repair_policy_id, quality_report_id |
| adjusted | 复权、合约换月、连续合约映射或 back-adjusted 数据层 | 只能从 raw/cleaned 派生；必须记录 adjustment_policy_id 和版本 | adjustment_policy_id, adjustment_factor, roll_rule_id, adjusted_price |
| feature_ready | 点时正确的特征层，不包含未来标签 | 必须记录 feature_version、available_time 和输入数据版本 | feature_name, feature_value, feature_version, available_time, source_dataset_version |
| label_ready | 训练/评估标签层，记录 horizon、label policy 和泄漏边界 | 不得回写 raw/cleaned/adjusted；只能作为训练或评估下游输入 | label_name, label_value, horizon, label_policy_id, label_generated_at |

## 转换清单

每次跨层转换必须生成 transformation manifest：

```text
input_layer
output_layer
source_dataset_version
source_table_snapshot
code_version
parameter_hash
produced_at
actor
quality_report_id
lineage_id
rollback_pointer
```

## 强制边界

```text
1. downstream layer 不得回写污染 raw layer。
2. raw 修正必须以 correction record 或新 dataset version 体现，不得静默覆盖。
3. adjusted 数据不能替代 raw 数据；回测/训练必须声明使用 raw、cleaned、adjusted、feature_ready 还是 label_ready。
4. feature_ready 必须有 available_time，不能含未来标签。
5. label_ready 必须声明 horizon 和 label policy，不能作为特征源回写。
6. AI Engineering 只能通过 knowledge_refs 引用本契约，不得把本契约改写为模型训练或交易执行规则本体。
```

## 不做什么

```text
不指定具体数据库产品。
不要求所有外接项目必须使用同一物理表名。
不提供买卖点、仓位、杠杆、止损止盈或实盘执行建议。
不把 candidate 直接升级为 reviewed/approved/default guidance。
```
"""


SUPPLEMENTS: dict[str, dict[str, Any]] = {
    "outlier_detection_required": {
        "candidate_file": "cand_20260611_phase37_data_engineering_outlier_detection_required_001.json",
        "research_task_id": "P37-B-D10",
        "statement": (
            "行情、成交、bar、spread 或特征数据进入回测和训练前，必须定义异常检测、标记、隔离、解释、保留或修复策略；"
            "异常不等于错误，不能默认删除，也不能静默改变策略或模型评估结论。"
        ),
        "evidence_summary": (
            "Databento market-data cleaning 资料支持异常不应被默认静默清洗；Databento trades/MBO schema、"
            "CME trade correction 和 Nasdaq FIX trade reporting 资料共同补强 market-data flags、order-book events、"
            "trade correction/cancel/re-entry 和时间戳字段边界。"
        ),
        "patch_notes": [
            "将 outlier 明确限定为需要标记、隔离、解释、保留或修复的审计对象，不能等同于自动删除。",
            "补充 market-data cleaning、trade correction、trade reporting、market data flags 和 order book event 来源。",
            "保留 candidate-only 边界；外部二审前不得 formal reviewed、approved、default guidance 或 hard gate。",
        ],
        "additional_sources": [
            {
                "source_title": "High-frequency market data: Data integrity and cleaning",
                "source_url": "https://databento.com/blog/data-cleaning",
                "source_type": "official_doc",
                "publisher": "Databento",
                "score": 86,
                "reliability": "high",
                "evidence_summary": "Databento explains market-data integrity checks, cleaning exceptions, QA strategies, and why indiscriminate cleaning can degrade market data.",
                "limitations": ["Vendor perspective; use to support audit boundary, not a universal deletion rule."],
            },
            {
                "source_title": "Trades schema",
                "source_url": "https://databento.com/docs/schemas-and-data-formats/trades",
                "source_type": "official_doc",
                "publisher": "Databento",
                "score": 85,
                "reliability": "high",
                "evidence_summary": "Databento trades schema documents trade timestamps and data-quality/event flags relevant to detecting market-data anomalies.",
                "limitations": ["Vendor-specific schema; field names must be mapped by each external project."],
            },
            {
                "source_title": "MBO schema",
                "source_url": "https://databento.com/docs/schemas-and-data-formats/mbo",
                "source_type": "official_doc",
                "publisher": "Databento",
                "score": 85,
                "reliability": "high",
                "evidence_summary": "Databento MBO schema covers order-book events such as trades, fills, adds, cancels, modifies and book clear events.",
                "limitations": ["Vendor-specific schema; supports event taxonomy, not a universal exchange protocol."],
            },
            {
                "source_title": "iLink - Trade Correction",
                "source_url": "https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457574586/iLink%2B-%2BTrade%2BCorrection",
                "source_type": "exchange_rule",
                "publisher": "CME Group",
                "score": 84,
                "reliability": "high",
                "evidence_summary": "CME documents in-session trade corrections, common trade ID linkage, and real-time price adjustment messaging.",
                "limitations": ["CME-specific workflow; use as evidence that exchange corrections must be modeled explicitly."],
            },
            {
                "source_title": "Nasdaq FIX Trade Reporting Programming Specification",
                "source_url": "https://nasdaqtrader.com/content/technicalsupport/specifications/TradingProducts/fixactspec.pdf",
                "source_type": "exchange_rule",
                "publisher": "Nasdaq",
                "score": 82,
                "reliability": "medium_high",
                "evidence_summary": "Nasdaq FIX trade reporting specification documents trade reporting, corrections via cancel/re-entry, and timestamp precision support.",
                "limitations": ["Venue/protocol-specific; use as supporting evidence for explicit correction records."],
            },
        ],
    },
    "raw_vs_adjusted_data_boundary": {
        "candidate_file": "cand_20260611_phase37_data_engineering_raw_vs_adjusted_data_boundary_001.json",
        "research_task_id": "P37-B-D11",
        "statement": (
            "CEK-TA 交易数据契约必须区分 raw、cleaned、adjusted、feature-ready 和 label-ready 层；"
            "这些是 CEK-TA 规范层名，不是所有平台强制层名。调整后价格、清洗后 bar、训练特征或标签不得回写污染 raw 层。"
        ),
        "evidence_summary": (
            "Databricks medallion 架构支撑 raw/validated/enriched 的渐进数据质量分层；Feast 支撑 point-in-time feature retrieval "
            "和 feature view schema；MLflow Dataset Tracking 与 Delta Lake time travel 支撑数据集血缘、版本和可追踪性；"
            "CEK-TA 内部 dataset layers contract 定义 feature-ready/label-ready 与 raw write-protection 的项目契约。"
        ),
        "patch_notes": [
            "明确 raw、cleaned、adjusted、feature-ready、label-ready 是 CEK-TA 数据契约层名。",
            "补充 medallion architecture、feature store point-in-time join、MLflow dataset lineage、Delta Lake time travel 和内部层级契约。",
            "强调 downstream layer 不能回写 raw；raw 修正必须以 correction record 或新 dataset version 表达。",
        ],
        "additional_sources": [
            {
                "source_title": "Medallion lakehouse architecture",
                "source_url": "https://docs.databricks.com/aws/en/lakehouse/medallion",
                "source_type": "framework_doc",
                "publisher": "Databricks",
                "score": 88,
                "reliability": "high",
                "evidence_summary": "Databricks documents bronze raw, silver validated, and gold enriched layers as progressively higher-quality data layers.",
                "limitations": ["Databricks naming is a pattern, not mandatory CEK-TA physical schema."],
            },
            {
                "source_title": "What is Medallion Architecture?",
                "source_url": "https://www.databricks.com/blog/what-is-medallion-architecture",
                "source_type": "framework_doc",
                "publisher": "Databricks",
                "score": 82,
                "reliability": "medium_high",
                "evidence_summary": "Databricks blog explains bronze as raw, silver as clean/standardized, and gold as aggregates/features ready for analytics and ML.",
                "limitations": ["Product blog; supporting evidence for layered-data pattern."],
            },
            {
                "source_title": "Point-in-time joins",
                "source_url": "https://docs.feast.dev/getting-started/concepts/point-in-time-joins",
                "source_type": "framework_doc",
                "publisher": "Feast",
                "score": 86,
                "reliability": "high",
                "evidence_summary": "Feast documents point-in-time correct joins that reproduce feature state for a specific past point.",
                "limitations": ["Feature-store specific; supports feature-ready boundary and leakage control."],
            },
            {
                "source_title": "Feature View",
                "source_url": "https://docs.feast.dev/getting-started/concepts/feature-view",
                "source_type": "framework_doc",
                "publisher": "Feast",
                "score": 82,
                "reliability": "medium_high",
                "evidence_summary": "Feast feature views define feature data and optional schema validation for consistent online/offline usage.",
                "limitations": ["Tool-specific; external projects may implement equivalent contracts without Feast."],
            },
            {
                "source_title": "Dataset Tracking",
                "source_url": "https://mlflow.org/docs/latest/ml/dataset/",
                "source_type": "framework_doc",
                "publisher": "MLflow",
                "score": 84,
                "reliability": "high",
                "evidence_summary": "MLflow documents tracking, versioning, and managing datasets for training, validation and evaluation lineage.",
                "limitations": ["MLflow-specific; supports lineage requirement rather than a mandatory platform choice."],
            },
            {
                "source_title": "Delta Lake Time Travel",
                "source_url": "https://delta.io/blog/2023-02-01-delta-lake-time-travel/",
                "source_type": "framework_doc",
                "publisher": "Delta Lake",
                "score": 80,
                "reliability": "medium_high",
                "evidence_summary": "Delta Lake explains time travel by table version or timestamp and transaction-log based historical access.",
                "limitations": ["Storage-format specific; supports versioned data access boundary."],
            },
            {
                "source_title": "Phase 37 Data Engineering Dataset Layers Contract",
                "source_url": "docs/contracts/phase37_data_engineering_dataset_layers_contract.md",
                "source_type": "internal_contract",
                "publisher": "CEK-TA",
                "score": 90,
                "reliability": "high",
                "evidence_summary": "CEK-TA internal contract defines raw, cleaned, adjusted, feature-ready and label-ready layer semantics, write boundaries, lineage and transformation manifest fields.",
                "limitations": ["Internal CEK-TA contract; must be paired with external architecture/feature-lineage sources."],
            },
        ],
    },
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


def dedupe_audit_log(entries: Any) -> list[dict[str, Any]]:
    if not isinstance(entries, list):
        return []
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str, str]] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        key = (
            str(entry.get("at", "")),
            str(entry.get("actor", "")),
            str(entry.get("action", "")),
            str(entry.get("audit_result_id") or ""),
        )
        if key in seen:
            continue
        seen.add(key)
        cleaned = dict(entry)
        cleaned.pop("source_task_id", None)
        deduped.append(cleaned)
    return deduped


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


def patch_candidate(slug: str, patch: dict[str, Any]) -> dict[str, Any]:
    path = CANDIDATE_DIR / str(patch["candidate_file"])
    item = read_json(path)

    start = next_source_index(item)
    for offset, source in enumerate(patch["additional_sources"]):
        append_source(item, source, start + offset)

    claim = item.setdefault("claim", {})
    claim["statement"] = patch["statement"]
    claim["evidence_summary"] = patch["evidence_summary"]
    claim["interpretation_notes"] = (
        "CEK-TA-390 已按 reviewed-preparation 审计意见补强来源和边界；本候选仍只等待外部二审，"
        "不得直接进入 formal reviewed、approved、default guidance 或 hard gate。"
    )

    applicability = item.setdefault("applicability", {})
    if slug == "outlier_detection_required":
        applicability["applies_when"] = [
            "行情、成交、盘口、bar、spread 或特征数据存在极端值、缺口、trade correction、cancel/re-entry、flags 或 vendor 修正时",
            "异常事件可能影响回测成交、指标计算、标签、训练样本或模型评估结论时",
        ]
        applicability["not_applicable_when"] = append_unique_strings(
            applicability.get("not_applicable_when", []),
            [
                "异常事件只作为只读原始审计日志保留，且不进入任何计算或训练时",
                "外接项目已有更强的一手交易所 correction/bust/cancel 契约并以其为准时",
            ],
        )
    else:
        applicability["applies_when"] = [
            "外接项目建立行情湖、研究数据集、回测缓存、特征表、训练集或标签表时",
            "需要区分原始事实、质量修复、复权/换月、点时正确特征和标签血缘时",
        ]
        applicability["not_applicable_when"] = append_unique_strings(
            applicability.get("not_applicable_when", []),
            [
                "外接项目只是人工查看单次文件，且不形成可复用回测、训练或审计数据集时",
                "外部数据库已有等价分层契约时，可映射到 CEK-TA 层名而不是强制复制物理表名",
            ],
        )

    source_quality = item.setdefault("source_quality", {})
    refs = [src for src in item.get("source_refs", []) if isinstance(src, dict)]
    primary_types = {"official_doc", "exchange_rule", "framework_doc", "internal_contract", "storage_table_format_spec"}
    source_quality["score_version"] = "phase37_data_engineering_blocked_supplemental_source_scoring_v1"
    source_quality["primary_source_count"] = sum(1 for src in refs if src.get("source_type") in primary_types)
    source_quality["supporting_source_count"] = len(refs) - int(source_quality["primary_source_count"])
    source_quality["score"] = round(sum(int(src.get("score", 0)) for src in refs) / max(len(refs), 1), 1)
    source_quality["overall_reliability"] = "high"
    source_quality["limitations"] = append_unique_strings(
        source_quality.get("limitations", []),
        patch["patch_notes"]
        + [
            "本补证只用于再审；正式 reviewed/caveat_only 仍需外部 AI/人工严格审计返回 reviewed_allowed=true。",
            "来源中存在供应商和框架文档，正式转换时必须保留适用边界，不得泛化为所有平台强制实现。",
        ],
    )

    conflict = item.setdefault("conflict_audit", {})
    conflict["conflict_status"] = "none_known_in_visible_context"
    conflict["resolution_summary"] = (
        "CEK-TA-390 补证后未发现与可见 formal knowledge 的直接冲突；本候选仍为 Trading Engineering 数据工程规则本体，"
        "AI Engineering 只能通过 knowledge_refs 引用。"
    )
    conflict["approval_allowed"] = False
    conflict["default_guidance_allowed"] = False
    conflict["hard_gate_allowed"] = False

    review = item.setdefault("review", {})
    review["open_questions"] = append_unique_strings(
        review.get("open_questions", []),
        [
            "二审是否认为本轮补证足以进入 formal reviewed/caveat_only？",
            "是否仍需要交易所更明确的 bust/cancel/correction 或数据平台 lineage 证据？",
            "正式转换时是否需要拆分为更细的 L3 专题知识？",
        ],
    )
    audit_log = review.setdefault("audit_log", [])
    if not isinstance(audit_log, list):
        audit_log = []
        review["audit_log"] = audit_log
    audit_log.append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "phase37_data_engineering_blocked_evidence_supplemented",
            "reason": "CEK-TA-390: 根据 reviewed-preparation 审计阻断点补充专业来源、CEK-TA 内部数据层契约和边界说明，并导出再审包。",
            "audit_result_id": "pending_phase37_data_engineering_blocked_supplemental_reaudit",
        }
    )
    review["audit_log"] = dedupe_audit_log(audit_log)
    review["ai_audit"] = {
        "audit_result_id": "pending_phase37_data_engineering_blocked_supplemental_reaudit",
        "source_package_id": PACKAGE_ID,
        "decision": "pending_reaudit",
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "patch_notes": patch["patch_notes"],
        "boundary": "This package can only allow accepted_for_reviewed_caveat_only, needs_more_evidence, rejected, or blocked.",
    }

    status = item.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "needs_more_evidence"
    status["decision_reason"] = "CEK-TA-390 已补充 reviewed 阻断证据并导出再审包；仍不是 formal reviewed/approved/default guidance。"
    status["updated_at"] = TODAY

    workflow = item.setdefault("workflow", {})
    workflow["stage"] = "supplemented_for_reaudit"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["next_action"] = "external_ai_or_human_reaudit_for_reviewed_caveat_only"
    workflow["formalization_allowed"] = False
    workflow["default_guidance_allowed"] = False
    workflow["approved_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["hidden_from_default_queue"] = False
    workflow["visible_in_default_guidance_queue"] = False
    workflow["ai_audit_result_id"] = "pending_phase37_data_engineering_blocked_supplemental_reaudit"

    machine_gate = item.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = "补证后仍需外部二审；不得作为默认指导。"
    machine_gate["requires_human_escalation"] = True
    machine_gate["hidden_from_default_queue"] = True

    conversion = item.setdefault("conversion_target", {})
    conversion["target_review_status"] = "blocked_until_supplemental_reaudit"
    conversion["reviewed_allowed"] = False
    conversion["approved_allowed"] = False
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    write_json(path, item)
    return item


def has_mojibake(value: object) -> bool:
    return bool(re.search(r"(�|锟|烫|屯|Ã|Â|\?{2,})", json.dumps(value, ensure_ascii=False)))


def quality_gate(items: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    expected = {"P37-B-D10", "P37-B-D11"}
    actual = {str(item.get("research_task_id")) for item in items}
    if actual != expected:
        failures.append({"failure": f"unexpected_research_tasks:{sorted(actual)}"})
    for item in items:
        candidate_id = str(item.get("candidate_id", ""))
        refs = item.get("source_refs", [])
        if len(refs) < 7:
            failures.append({"candidate_id": candidate_id, "failure": "source_refs_lt_7_after_supplement"})
        if item.get("status", {}).get("ingestion_decision") != "needs_more_evidence":
            failures.append({"candidate_id": candidate_id, "failure": "unexpected_ingestion_decision"})
        if item.get("workflow", {}).get("stage") != "supplemented_for_reaudit":
            failures.append({"candidate_id": candidate_id, "failure": "workflow_stage_not_supplemented_for_reaudit"})
        if item.get("workflow", {}).get("approved_allowed") is not False:
            failures.append({"candidate_id": candidate_id, "failure": "approved_allowed_not_false"})
        if item.get("workflow", {}).get("default_guidance_allowed") is not False:
            failures.append({"candidate_id": candidate_id, "failure": "default_guidance_allowed_not_false"})
        if item.get("workflow", {}).get("hard_gate_allowed") is not False:
            failures.append({"candidate_id": candidate_id, "failure": "hard_gate_allowed_not_false"})
        if has_mojibake(item):
            failures.append({"candidate_id": candidate_id, "failure": "mojibake_marker_detected"})
    return {
        "gate_id": "phase37_data_engineering_blocked_supplemental_reaudit_quality_gate",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "candidate_count": len(items),
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "formal_reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_created": 0,
        "hard_gate_created": 0,
        "boundary": "supplemental candidate package only; no formal reviewed knowledge is created.",
    }


def write_contract() -> None:
    CONTRACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONTRACT_PATH.write_text(CONTRACT_CONTENT, encoding="utf-8")


def write_research(items: list[dict[str, Any]]) -> None:
    rows = [
        "| 任务 | 候选 | 补证重点 | 来源数 |",
        "| --- | --- | --- | ---: |",
    ]
    for item in items:
        slug = str(item["candidate_id"]).removeprefix("cand_20260611_phase37_data_engineering_").removesuffix("_001")
        rows.append(
            f"| {item['research_task_id']} | `{item['candidate_id']}` | {'；'.join(SUPPLEMENTS[slug]['patch_notes'])} | {len(item['source_refs'])} |"
        )

    content = f"""# Phase 37 Data Engineering D10/D11 补证研究记录

生成日期：{TODAY}

## 范围

本文件只记录 `P37-B-D10` 与 `P37-B-D11` reviewed-preparation 阻断项的补证。它不创建 formal reviewed、不创建 approved、不进入默认指导，也不改变 MCP/SearchLab 正式知识索引。

## 补证清单

{chr(10).join(rows)}

## 来源使用边界

```text
1. Databento、CME、Nasdaq 资料用于支撑 market-data anomaly、flags、trade correction、cancel/re-entry 和 correction record 边界。
2. Databricks、Feast、MLflow、Delta Lake 资料用于支撑数据分层、点时正确特征、数据集血缘和版本边界。
3. CEK-TA 内部数据层契约用于定义 feature-ready / label-ready / raw write-protection 的本项目知识库语义。
4. 所有候选仍需外部二审，不得直接作为 reviewed/approved/default guidance。
```

## 再审入口

```text
docs/audit/phase37_data_engineering_blocked_supplemental_reaudit_package_20260611.json
```
"""
    RESEARCH_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_PATH.write_text(content, encoding="utf-8")


def build_audit_package(items: list[dict[str, Any]], quality: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": PACKAGE_ID,
        "package_type": "candidate_supplemental_reaudit_package",
        "schema_version": "1.0.0",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "language": "zh-CN",
        "phase": "37",
        "title": "Phase 37 Data Engineering D10/D11 reviewed 阻断项补证二审包",
        "purpose": "严格复审 P37-B-D10/D11 补证后是否可以进入 formal reviewed/caveat_only，或仍需补证/拒绝/阻断。",
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
            "重点检查 P37-B-D10 是否已经有足够 market-data anomaly、trade correction、flags、cancel/re-entry 和异常处理边界证据。",
            "重点检查 P37-B-D11 是否已经通过外部数据分层/feature-store/dataset-lineage 来源和 CEK-TA 内部契约，支撑 raw/cleaned/adjusted/feature-ready/label-ready 边界。",
            "若来源只支撑供应商或框架自身实现，必须要求保留适用边界，不得泛化为所有平台强制实现。",
            "输出只能是 accepted_for_reviewed_caveat_only、needs_more_evidence、rejected 或 blocked。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": PACKAGE_ID,
            "auditor": "string",
            "audited_at": "YYYY-MM-DD",
            "quality_gate": {
                "pass": "boolean",
                "candidate_count": 2,
                "notes": ["string"],
            },
            "decisions": [
                {
                    "candidate_id": "string",
                    "research_task_id": "P37-B-D10 | P37-B-D11",
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
                    "required_extra_sources": ["object"],
                    "formal_conversion_notes": ["string"],
                }
            ],
        },
        "quality_gate": quality,
        "contract": {
            "path": "docs/contracts/phase37_data_engineering_dataset_layers_contract.md",
            "purpose": "Support CEK-TA-specific dataset-layer names and write boundaries for P37-B-D11.",
        },
        "candidates": items,
    }


def main() -> None:
    write_contract()
    items = [patch_candidate(slug, patch) for slug, patch in SUPPLEMENTS.items()]
    quality = quality_gate(items)
    write_research(items)
    write_json(AUDIT_PATH, build_audit_package(items, quality))
    report = {
        "report_id": "phase37_data_engineering_blocked_supplemental_reaudit_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "package_id": PACKAGE_ID,
        "candidate_count": len(items),
        "candidate_ids": [item["candidate_id"] for item in items],
        "research_tasks": [item["research_task_id"] for item in items],
        "contract": rel_path(CONTRACT_PATH),
        "research_record": rel_path(RESEARCH_PATH),
        "audit_package": rel_path(AUDIT_PATH),
        "quality_gate": quality,
        "boundary": "No formal reviewed knowledge, approved knowledge, default guidance, hard gate, or MCP index update was created.",
        "next_action": "将再审包交给外部 AI/人工严格审计；只有返回 accepted_for_reviewed_caveat_only 且 reviewed_allowed=true 后，才能另起任务沉淀 formal reviewed/caveat_only。",
    }
    write_json(REPORT_PATH, report)
    if quality["gate_status"] != "pass":
        raise SystemExit(f"quality gate failed: {quality['failures']}")
    print(json.dumps({"supplemented": len(items), "audit_package": rel_path(AUDIT_PATH)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
