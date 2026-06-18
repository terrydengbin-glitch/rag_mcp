"""Import Phase 45 P2 first audit result and export supplemental re-audit.

This script archives the external strict audit result, updates nine P2
candidates to accepted_for_draft, supplements DATA05 and CRYPTO05, and exports
a supplemental re-audit package for those two needs_more_evidence candidates.

It never creates formal reviewed knowledge, approved knowledge, default
guidance, hard gates, legal license conclusions, risk thresholds, or trading
execution advice.
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
TASK_ID = "CEK-TA-471"
AUDIT_RESULT_ID = "audit_phase45_p2_candidate_20260612_external_strict"
PACKAGE_ID = "phase45_p2_candidate_audit_package_20260612"
SUPPLEMENTAL_PACKAGE_ID = "phase45_p2_needs_evidence_supplemental_reaudit_package_20260612"

REPO_ROOT = resolve_repo_path(".", start_file=__file__)
AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path("docs", "reports", "phase45_p2_candidate_audit_import_report.json", start_file=__file__)
SUPPLEMENTAL_RESEARCH = resolve_repo_path("docs", "research", "phase45_p2_needs_evidence_supplemental_research.md", start_file=__file__)
SUPPLEMENTAL_PACKAGE = resolve_repo_path("docs", "audit", f"{SUPPLEMENTAL_PACKAGE_ID}.json", start_file=__file__)
SUPPLEMENTAL_GATE = resolve_repo_path("docs", "reports", "phase45_p2_needs_evidence_supplemental_reaudit_package_quality_gate.json", start_file=__file__)
CONTRACT_PATH = resolve_repo_path("docs", "contracts", "phase45_market_data_ingestion_lineage_contract.md", start_file=__file__)


DECISIONS: dict[str, dict[str, Any]] = {
    "P45-G-DATA01": {
        "decision": "accepted_for_draft",
        "confidence": "medium_high",
        "reason": "市场数据授权边界可进 draft；training/evaluation 只能写成必须声明授权边界，不能写成已获授权。",
        "required_followups": ["补 active agreement / vendor legal owner / training-use clause 字段。"],
    },
    "P45-G-DATA02": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "Databento point-in-time instrument definitions 来源足够，PIT reference data 方向正确。",
        "required_followups": ["进入 reviewed 前补内部 point_in_time_reference_data schema。"],
    },
    "P45-G-DATA03": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "tick size、round lot、price limit 等版本化 reference metadata 来源足够，不能硬编码为永久常量。",
        "required_followups": ["进入 reviewed 前补 internal tick_lot_limit_metadata schema。"],
    },
    "P45-G-DATA04": {
        "decision": "accepted_for_draft",
        "confidence": "medium_high",
        "reason": "dataset coverage / universe 可进 draft；delisting / symbol change 后续需补更直接来源。",
        "required_followups": ["补 delisting / symbol change / corporate action 直接来源。"],
    },
    "P45-G-DATA05": {
        "decision": "needs_more_evidence",
        "confidence": "medium",
        "reason": "当前来源支撑 vendor schema 字段，但不足以支撑 parser_version、normalization_version、raw_snapshot、source digest 的治理要求。",
        "required_followups": [
            "补 internal ingestion lineage contract。",
            "补 parser_version、normalization_version、raw_snapshot_uri、source_digest、schema_version 字段表。",
            "补数据血缘 / reproducibility / audit trail 来源。",
        ],
    },
    "P45-G-DATA06": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "reference data 不是 alpha、买卖点、仓位、风控阈值或实盘许可，边界正确。",
        "required_followups": ["若 reference data 派生为 feature，必须转入 Feature Engineering / AI Engineering 泄漏与验证流程。"],
    },
    "P45-H-CRYPTO01": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "mark price、index price、last trade price 和 liquidation trigger 必须分开建模，来源足够。",
        "required_followups": ["进入 reviewed 前补 internal crypto_perp_price_snapshot schema。"],
    },
    "P45-H-CRYPTO02": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "funding rate、funding interval、timestamp、direction 和 funding fee 是 perpetual 独立现金流，来源足够。",
        "required_followups": ["进入 reviewed 前补 funding_cashflow_event schema。"],
    },
    "P45-H-CRYPTO03": {
        "decision": "accepted_for_draft",
        "confidence": "medium_high",
        "reason": "liquidation 不等同普通止损可进 draft；reviewed 前需补 margin mode / partial liquidation 直接来源。",
        "required_followups": ["补 maintenance margin tier / margin mode / partial liquidation 官方来源。"],
    },
    "P45-H-CRYPTO04": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "ADL、insurance fund、bankruptcy loss coverage 是 venue-specific 风险机制，来源足够。",
        "required_followups": ["进入 reviewed 前补 adl_insurance_event schema。"],
    },
    "P45-H-CRYPTO05": {
        "decision": "needs_more_evidence",
        "confidence": "medium",
        "reason": "当前来源不足以完整支撑 exchange outage、API/WebSocket disconnect、mark price anomaly、clawback/loss-socialization 全部 claim。",
        "required_followups": [
            "补 exchange outage / maintenance 官方来源。",
            "补 API/WebSocket disconnect、reconnect、heartbeat、data-gap 文档。",
            "补 mark price anomaly / index component abnormal handling 来源。",
            "补 clawback / loss socialization 官方规则，或删除 clawback 字段。",
        ],
    },
}


SUPPLEMENTAL_SOURCES: dict[str, dict[str, Any]] = {
    "cek_ta_ingestion_lineage_contract": {
        "source_title": "Phase 45 Market Data Ingestion Lineage Contract",
        "source_url": "docs/contracts/phase45_market_data_ingestion_lineage_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "reliability": "high",
        "score": 88,
        "freshness": "stable",
        "relevance": "high",
        "evidence_summary": "CEK-TA internal contract defines vendor_id, dataset_id, schema_version, parser_version, normalization_version, raw_snapshot_uri, raw_snapshot_digest and lineage_id.",
        "limitations": ["Internal contract; reviewed import still needs external audit and must not imply market-data license permission."],
    },
    "openlineage_dataset_facets": {
        "source_title": "OpenLineage Dataset Facets",
        "source_url": "https://openlineage.io/docs/spec/facets/dataset-facets/",
        "source_type": "official_spec",
        "publisher": "OpenLineage",
        "reliability": "high",
        "score": 86,
        "freshness": "stable",
        "relevance": "high",
        "evidence_summary": "OpenLineage dataset facets support attaching common, input and output metadata to datasets for lineage events.",
        "limitations": ["Lineage standard pattern; not a CEK-TA market-data schema by itself."],
    },
    "openlineage_object_model": {
        "source_title": "OpenLineage Object Model",
        "source_url": "https://openlineage.io/docs/spec/object-model/",
        "source_type": "official_spec",
        "publisher": "OpenLineage",
        "reliability": "high",
        "score": 86,
        "freshness": "stable",
        "relevance": "high",
        "evidence_summary": "OpenLineage object model links jobs, runs and input/output datasets to create lineage graphs across platforms.",
        "limitations": ["General lineage model; field names must be mapped to CEK-TA contract."],
    },
    "mlflow_dataset_tracking": {
        "source_title": "MLflow Dataset Tracking",
        "source_url": "https://mlflow.org/docs/latest/ml/dataset/",
        "source_type": "official_framework_doc",
        "publisher": "MLflow",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "MLflow Dataset Tracking supports tracking, versioning and managing datasets for training, validation and evaluation with lineage from raw data to predictions.",
        "limitations": ["MLflow implementation pattern; not required as CEK-TA's only storage tool."],
    },
    "mlflow_dataset_api": {
        "source_title": "MLflow Dataset API",
        "source_url": "https://mlflow.org/docs/latest/python_api/mlflow.data.html",
        "source_type": "official_framework_doc",
        "publisher": "MLflow",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "MLflow Dataset includes name, digest, schema, profile and source information for a dataset.",
        "limitations": ["MLflow data model; CEK-TA still requires parser and normalizer version fields."],
    },
    "iceberg_spec": {
        "source_title": "Apache Iceberg Specification",
        "source_url": "https://iceberg.apache.org/spec/",
        "source_type": "official_spec",
        "publisher": "Apache Iceberg",
        "reliability": "high",
        "score": 86,
        "freshness": "stable",
        "relevance": "medium_high",
        "evidence_summary": "Iceberg snapshots and manifest lists record table state and metadata about manifests and data files.",
        "limitations": ["Table format pattern; not a requirement to use Iceberg in CEK-TA."],
    },
    "dvc_pipelines": {
        "source_title": "DVC Data Pipelines",
        "source_url": "https://doc.dvc.org/start/data-pipelines/data-pipelines",
        "source_type": "official_framework_doc",
        "publisher": "DVC",
        "reliability": "high",
        "score": 84,
        "freshness": "stable",
        "relevance": "medium_high",
        "evidence_summary": "DVC pipelines capture, organize, version and reproduce data science and machine learning workflows.",
        "limitations": ["Workflow versioning pattern; not a market-data entitlement or vendor schema source."],
    },
    "binance_ws_market_streams": {
        "source_title": "Binance USDⓈ-M Futures WebSocket Market Streams",
        "source_url": "https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams",
        "source_type": "official_api_doc",
        "publisher": "Binance Developers",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "Binance WebSocket market streams document ping/pong, disconnect behavior, message limits and stream limits.",
        "limitations": ["Binance-specific API behavior; not universal to all crypto venues."],
    },
    "binance_ws_api_general": {
        "source_title": "Binance Futures WebSocket API General Info",
        "source_url": "https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-api-general-info",
        "source_type": "official_api_doc",
        "publisher": "Binance Developers",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "Binance WebSocket API notes that a single connection is valid for 24 hours and ping/pong failure leads to disconnection.",
        "limitations": ["Binance WebSocket API context; not a full outage incident source."],
    },
    "binance_maintenance_updates": {
        "source_title": "Binance Maintenance Updates",
        "source_url": "https://www.binance.com/en/support/announcement/list/157",
        "source_type": "official_platform_doc",
        "publisher": "Binance",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "relevance": "medium_high",
        "evidence_summary": "Binance publishes scheduled maintenance and upgrade notices that can affect services.",
        "limitations": ["Announcement list; incident-specific evidence still depends on the exact event notice."],
    },
    "bybit_ws_connect": {
        "source_title": "Bybit WebSocket Connect",
        "source_url": "https://bybit-exchange.github.io/docs/v5/ws/connect",
        "source_type": "official_api_doc",
        "publisher": "Bybit",
        "reliability": "high",
        "score": 85,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "Bybit recommends sending ping heartbeat packets every 20 seconds to maintain WebSocket connections.",
        "limitations": ["Bybit-specific connectivity guidance; not a universal outage policy."],
    },
    "binance_mark_price": {
        "source_title": "Binance Mark Price API",
        "source_url": "https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Mark-Price",
        "source_type": "official_api_doc",
        "publisher": "Binance Developers",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "Binance Mark Price API exposes markPrice, indexPrice, lastFundingRate, nextFundingTime and time, supporting mark-price monitoring fields.",
        "limitations": ["Does not by itself define all mark-price anomaly handling rules."],
    },
    "binance_adl": {
        "source_title": "Binance Auto-Deleveraging",
        "source_url": "https://www.binance.com/en/support/faq/detail/360033525471",
        "source_type": "official_platform_doc",
        "publisher": "Binance",
        "reliability": "high",
        "score": 84,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "Binance states ADL is the final liquidation step if the futures insurance fund cannot accept a bankrupt position.",
        "limitations": ["Binance-specific ADL process; not a universal clawback policy."],
    },
    "binance_insurance_fund": {
        "source_title": "Binance Futures Insurance Funds",
        "source_url": "https://www.binance.com/en/support/faq/detail/360033525371",
        "source_type": "official_platform_doc",
        "publisher": "Binance",
        "reliability": "high",
        "score": 84,
        "freshness": "time_sensitive",
        "relevance": "medium_high",
        "evidence_summary": "Binance describes futures insurance funds as safety nets for liquidation and bankrupt positions.",
        "limitations": ["Not a guarantee; not a complete loss-socialization policy for all venues."],
    },
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def candidate_paths() -> list[Path]:
    paths: list[Path] = []
    for partition in ("KB_02_DATA_ENGINEERING", "KB_03_MARKET_MICROSTRUCTURE", "KB_07_RISK_MANAGEMENT"):
        cand_dir = resolve_repo_path("codex-expert-kit", "rag", "candidates", partition, start_file=__file__)
        paths.extend(sorted(cand_dir.glob("cand_20260612_phase45_reference_data_entitlement_*.json")))
        paths.extend(sorted(cand_dir.glob("cand_20260612_phase45_crypto_perp_*.json")))
    return sorted(set(paths))


def source_ref(source_key: str, source_id: str) -> dict[str, Any]:
    source = dict(SUPPLEMENTAL_SOURCES[source_key])
    source.update({"source_id": source_id, "accessed_at": TODAY, "version": None, "quoted_excerpt_allowed": False})
    return source


def upsert_source_refs(candidate: dict[str, Any], refs: list[dict[str, Any]]) -> None:
    existing_urls = {ref.get("source_url") for ref in candidate.get("source_refs", [])}
    source_refs = list(candidate.get("source_refs", []))
    for ref in refs:
        if ref.get("source_url") not in existing_urls:
            source_refs.append(ref)
    candidate["source_refs"] = source_refs
    primary_types = {"official_exchange_policy", "official_exchange_doc", "official_vendor_doc", "official_api_doc", "official_platform_doc", "official_framework_doc", "official_spec", "internal_contract"}
    primary_count = sum(1 for ref in source_refs if ref.get("source_type") in primary_types)
    candidate.setdefault("source_quality", {})["primary_source_count"] = primary_count
    candidate["source_quality"]["supporting_source_count"] = len(source_refs) - primary_count
    candidate["source_quality"]["score"] = round(sum(float(ref.get("score", 70)) for ref in source_refs) / len(source_refs), 2)


def archive_audit_result() -> dict[str, Any]:
    result = {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "GPT-5.5 Thinking",
        "audited_at": TODAY,
        "package_id": PACKAGE_ID,
        "summary": {
            "total": 11,
            "accepted_for_draft": 9,
            "needs_more_evidence": 2,
            "rejected": 0,
            "blocked": 0,
        },
        "candidate_results": [
            {
                "research_task_id": task,
                "decision": data["decision"],
                "confidence": data["confidence"],
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
                "trade_execution_advice_allowed": False,
                "legal_license_conclusion_allowed": False,
                "reasons": [data["reason"]],
                "required_followups": data["required_followups"],
            }
            for task, data in DECISIONS.items()
        ],
        "global_notes": [
            "9 条候选可进入 accepted_for_draft。",
            "P45-G-DATA05 需要补 internal schema/parser/normalization/source-digest lineage contract。",
            "P45-H-CRYPTO05 需要补 exchange outage、API/WebSocket disconnect、mark-price anomaly、clawback/loss-socialization 官方来源或收窄 claim。",
            "本审计结果不允许 reviewed、approved、default guidance 或 hard gate。",
        ],
    }
    write_json(AUDIT_RESULT_PATH, result)
    return result


def supplement_data05(candidate: dict[str, Any]) -> None:
    upsert_source_refs(
        candidate,
        [
            source_ref("cek_ta_ingestion_lineage_contract", "src_supp_data05_001"),
            source_ref("openlineage_dataset_facets", "src_supp_data05_002"),
            source_ref("openlineage_object_model", "src_supp_data05_003"),
            source_ref("mlflow_dataset_tracking", "src_supp_data05_004"),
            source_ref("mlflow_dataset_api", "src_supp_data05_005"),
            source_ref("iceberg_spec", "src_supp_data05_006"),
            source_ref("dvc_pipelines", "src_supp_data05_007"),
        ],
    )
    candidate["claim"]["statement"] = (
        "市场数据 ingestion、解析、标准化和导出必须记录 vendor、dataset、venue、schema_version、field_dictionary_ref、parser_version、"
        "parser_code_hash、normalization_version、normalization_code_hash、raw_snapshot_uri、raw_snapshot_digest、lineage_id、"
        "input_dataset_version 和 output_dataset_version；供应商字段、单位、枚举或语义变化不得静默影响回测、训练、TCA 或实盘审计。"
    )
    candidate["claim"]["evidence_summary"] = (
        "Databento / Nasdaq 来源支撑 vendor schema 和字段字典；CEK-TA internal contract 定义 parser_version、normalization_version、"
        "raw_snapshot_digest 和 lineage_id；OpenLineage、MLflow Dataset Tracking、Iceberg 和 DVC 支撑数据血缘、dataset digest、snapshot 和可复现 pipeline 模式。"
    )
    candidate.setdefault("applicability", {}).setdefault("limitations", []).extend(
        [
            "OpenLineage、MLflow、Iceberg、DVC 只作为 lineage / digest / snapshot / reproducibility 模式来源，不是强制工具依赖。",
            "CEK-TA internal contract 支撑字段本体，但不产生市场数据授权、训练授权或再分发许可。",
        ]
    )


def supplement_crypto05(candidate: dict[str, Any]) -> None:
    upsert_source_refs(
        candidate,
        [
            source_ref("binance_ws_market_streams", "src_supp_crypto05_001"),
            source_ref("binance_ws_api_general", "src_supp_crypto05_002"),
            source_ref("binance_maintenance_updates", "src_supp_crypto05_003"),
            source_ref("bybit_ws_connect", "src_supp_crypto05_004"),
            source_ref("binance_mark_price", "src_supp_crypto05_005"),
            source_ref("binance_adl", "src_supp_crypto05_006"),
            source_ref("binance_insurance_fund", "src_supp_crypto05_007"),
        ],
    )
    candidate["claim"]["statement"] = (
        "Crypto perpetual 项目必须单独审计交易所维护/服务中断、API/WebSocket 断连、heartbeat/ping-pong 失败、stream 限流、"
        "mark price / index price 异常监控、预上市 perpetual、ADL/insurance-fund 事件和交易所特定 loss-allocation 机制；"
        "不得把 24/7 连续交易假设等同于无停机、无断连、无数据缺口或无交易所机制风险。"
    )
    candidate["claim"]["evidence_summary"] = (
        "Databento status schema 支撑市场状态字段；Binance / Bybit WebSocket 文档支撑断连、heartbeat、限流和连接有效期风险；"
        "Binance maintenance updates 支撑维护窗口来源；Binance Mark Price API 支撑 mark/index 监控字段；Binance ADL 与 insurance fund 来源支撑交易所特定 loss-allocation 机制。"
    )
    candidate.setdefault("applicability", {}).setdefault("limitations", []).extend(
        [
            "本候选将 clawback 收窄为 exchange-specific loss-allocation mechanism；若外接项目使用特定 clawback 术语，必须补对应 venue rulebook。",
            "Binance / Bybit / OKX / Databento 来源只能证明各自平台、API 或 schema 语境，不能泛化为所有 crypto venue。",
        ]
    )


def apply_decisions() -> dict[str, Any]:
    paths_by_task: dict[str, Path] = {}
    data_by_task: dict[str, dict[str, Any]] = {}
    for path in candidate_paths():
        data = read_json(path)
        task_id = str(data.get("research_task_id"))
        if task_id in DECISIONS:
            paths_by_task[task_id] = path
            data_by_task[task_id] = data

    missing: list[str] = []
    updated: list[dict[str, Any]] = []
    for task_id, decision in DECISIONS.items():
        path = paths_by_task.get(task_id)
        if not path:
            missing.append(task_id)
            continue
        data = data_by_task[task_id]
        data.setdefault("review", {})["ai_audit"] = {
            "audit_result_id": AUDIT_RESULT_ID,
            "decision": decision["decision"],
            "confidence": decision["confidence"],
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
            "legal_license_conclusion_allowed": False,
            "required_followups": decision["required_followups"],
        }
        data.setdefault("review", {}).setdefault("audit_log", []).append(
            {
                "at": TODAY,
                "actor": "external_ai_strict_audit",
                "action": "phase45_p2_first_audit_imported",
                "reason": f"{decision['decision']} / confidence={decision['confidence']}",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )
        if decision["decision"] == "accepted_for_draft":
            data["status"]["review_status"] = "accepted"
            data["status"]["ingestion_decision"] = "accepted_for_draft"
            data["status"]["decision_reason"] = decision["reason"]
            data["workflow"]["stage"] = "formal_draft_queue"
            data["workflow"]["queue_group"] = "ai_passed"
            data["workflow"]["allowed_next_decisions"] = ["reviewed_preparation", "needs_more_evidence", "rejected"]
        else:
            data["status"]["review_status"] = "needs_more_evidence"
            data["status"]["ingestion_decision"] = "needs_more_evidence"
            data["status"]["decision_reason"] = decision["reason"]
            data["workflow"]["stage"] = "needs_more_evidence"
            data["workflow"]["queue_group"] = "needs_more_evidence"
            data["workflow"]["allowed_next_decisions"] = ["accepted_for_draft", "needs_more_evidence", "rejected", "blocked"]
            if task_id == "P45-G-DATA05":
                supplement_data05(data)
            if task_id == "P45-H-CRYPTO05":
                supplement_crypto05(data)
            data.setdefault("review", {}).setdefault("audit_log", []).append(
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "phase45_p2_candidate_supplemented",
                    "reason": "按首轮审计要求补证并导出二审包。",
                }
            )
        data["workflow"]["forbidden_next_decisions"] = ["reviewed", "approved", "default_guidance", "hard_gate"]
        data["status"]["updated_at"] = TODAY
        write_json(path, data)
        updated.append({"research_task_id": task_id, "candidate_id": data.get("candidate_id"), "decision": decision["decision"], "path": repo_relative(path)})
    return {"updated": updated, "missing": missing}


def load_supplemented_candidates() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for path in candidate_paths():
        data = read_json(path)
        if data.get("research_task_id") in {"P45-G-DATA05", "P45-H-CRYPTO05"}:
            candidates.append(data)
    return sorted(candidates, key=lambda item: str(item.get("research_task_id")))


def supplemental_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    expected = {"P45-G-DATA05", "P45-H-CRYPTO05"}
    actual = {str(item.get("research_task_id")) for item in candidates}
    if len(candidates) != 2:
        failures.append(f"expected 2 supplemented candidates, got {len(candidates)}")
    if actual != expected:
        failures.append(f"unexpected research_task_id set: {sorted(actual ^ expected)}")
    for item in candidates:
        cid = item.get("candidate_id", "<unknown>")
        if len(item.get("source_refs", [])) < 8:
            failures.append(f"{cid}: source_refs < 8 after supplement")
        if item.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append(f"{cid}: default guidance must remain deny")
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "risk_threshold_advice_allowed", "trade_execution_advice_allowed"):
            if item.get("machine_gate", {}).get(field) is not False:
                failures.append(f"{cid}: {field} must remain false")
        blob = json.dumps(item, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake")
    return {
        "gate_id": "phase45_p2_needs_evidence_supplemental_reaudit_package_quality_gate",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "package_id": SUPPLEMENTAL_PACKAGE_ID,
        "candidate_count": len(candidates),
        "expected_count": 2,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本包只复审 P45-G-DATA05 与 P45-H-CRYPTO05 补证候选；不得直接创建 reviewed、approved、default guidance 或 hard gate。",
            "DATA05 的 OpenLineage、MLflow、Iceberg、DVC 只作为 lineage / digest / snapshot / reproducibility 模式来源，不是强制工具依赖。",
            "CRYPTO05 的 Binance / Bybit 来源只能证明各自 API / venue 行为，不输出清算规避、仓位、杠杆或停机 hard gate。",
        ],
    }


def write_supplemental_research() -> None:
    lines = [
        "# Phase 45 P2 DATA05 / CRYPTO05 补证记录",
        "",
        "## 补证目标",
        "",
        "首轮审计中 P45-G-DATA05 与 P45-H-CRYPTO05 被判定为 `needs_more_evidence`。本文件记录补证来源和修补边界。",
        "",
        "## 补充来源",
        "",
        "| source_id | 来源 | 类型 | URL | 用途 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for key, source in SUPPLEMENTAL_SOURCES.items():
        lines.append(f"| `{key}` | {source['source_title']} | `{source['source_type']}` | {source['source_url']} | {source['evidence_summary']} |")
    lines.extend(
        [
            "",
            "## 修补后边界",
            "",
            "```text",
            "1. DATA05：vendor schema 与 CEK-TA parser/normalizer lineage 分开；parser_version、normalization_version、raw_snapshot_digest 和 lineage_id 由内部契约支撑。",
            "2. DATA05：OpenLineage、MLflow、Iceberg、DVC 只作为 lineage / digest / snapshot / reproducibility 模式来源，不作为强制技术栈。",
            "3. CRYPTO05：exchange outage、maintenance、WebSocket disconnect、heartbeat、rate-limit、mark price monitoring、ADL/insurance-fund loss allocation 分开建模。",
            "4. CRYPTO05：clawback 已收窄为 exchange-specific loss-allocation mechanism；若外接项目使用特定 clawback 术语，必须补对应 venue rulebook。",
            "5. 两条均不输出法律授权结论、交易许可、仓位、杠杆、清算规避、实盘执行建议或 hard gate。",
            "```",
        ]
    )
    SUPPLEMENTAL_RESEARCH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def export_supplemental_package(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> None:
    package = {
        "package_id": SUPPLEMENTAL_PACKAGE_ID,
        "created_at": TODAY,
        "created_by": "codex",
        "phase": PHASE,
        "task_id": TASK_ID,
        "scope": {
            "branch": "Trading Engineering / P2 supplemental re-audit",
            "candidate_count": len(candidates),
            "target": "复审 P45-G-DATA05 与 P45-H-CRYPTO05，确认补充 internal lineage contract、OpenLineage/MLflow/Iceberg/DVC、Binance/Bybit API/WebSocket/maintenance/ADL 证据后是否可进入 accepted_for_draft。",
        },
        "hard_boundaries": {
            "candidate_not_formal": True,
            "accepted_for_draft_not_reviewed": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "legal_license_conclusion_allowed": False,
            "must_not_create_formal_knowledge": True,
        },
        "audit_instructions": [
            "必须搜索相关专业网站、官方文档、数据血缘/可复现性资料、交易所/crypto venue/API 文档、案例和数据，对补证内容进行严格再审。",
            "检查 DATA05 是否已充分区分 vendor schema、parser_version、normalization_version、raw_snapshot_digest、source digest 和 lineage_id。",
            "检查 DATA05 的内部契约是否足以支撑字段本体，外部来源是否仅作为 lineage / digest / snapshot / reproducibility 模式证据。",
            "检查 CRYPTO05 是否已补 API/WebSocket disconnect、heartbeat、maintenance/status、mark price monitoring 和 ADL/insurance-fund loss-allocation 证据。",
            "检查 CRYPTO05 是否已把 clawback 收窄为 exchange-specific loss-allocation mechanism，且未输出清算规避或 hard gate。",
            "输出只能是 accepted_for_draft、needs_more_evidence、rejected 或 blocked；不得输出 reviewed、approved、default guidance 或 hard gate。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": SUPPLEMENTAL_PACKAGE_ID,
            "summary": {"total": 2, "accepted_for_draft": 0, "needs_more_evidence": 0, "rejected": 0, "blocked": 0},
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "P45-G-DATA05 | P45-H-CRYPTO05",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | high",
                    "reviewed_allowed": False,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "risk_threshold_advice_allowed": False,
                    "trade_execution_advice_allowed": False,
                    "legal_license_conclusion_allowed": False,
                    "reasons": ["string"],
                    "required_followups": ["string"],
                    "patch_notes": {"source": ["string"], "content": ["string"], "boundary": ["string"], "conflict": ["string"]},
                }
            ],
        },
        "quality_gate": gate,
        "candidates": candidates,
    }
    write_json(SUPPLEMENTAL_PACKAGE, package)


def main() -> int:
    audit_result = archive_audit_result()
    apply_report = apply_decisions()
    candidates = load_supplemented_candidates()
    gate = supplemental_gate(candidates)
    write_json(SUPPLEMENTAL_GATE, gate)
    write_supplemental_research()
    export_supplemental_package(candidates, gate)
    write_json(
        IMPORT_REPORT,
        {
            "report_id": "phase45_p2_candidate_audit_import_report",
            "generated_at": TODAY,
            "phase": PHASE,
            "task_id": TASK_ID,
            "audit_result_id": AUDIT_RESULT_ID,
            "audit_result_path": repo_relative(AUDIT_RESULT_PATH),
            "updated": apply_report["updated"],
            "missing": apply_report["missing"],
            "supplemental_package_id": SUPPLEMENTAL_PACKAGE_ID,
            "supplemental_package_path": repo_relative(SUPPLEMENTAL_PACKAGE),
            "supplemental_gate": gate,
            "accepted_for_draft_count": sum(1 for item in apply_report["updated"] if item["decision"] == "accepted_for_draft"),
            "needs_more_evidence_count": sum(1 for item in apply_report["updated"] if item["decision"] == "needs_more_evidence"),
            "formal_reviewed_created": 0,
            "approved_created": 0,
            "default_guidance_enabled": False,
            "hard_gate_enabled": False,
        },
    )
    print(json.dumps({"status": gate["gate_status"], "updated": len(apply_report["updated"]), "supplemental_candidates": len(candidates)}, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" and not apply_report["missing"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
