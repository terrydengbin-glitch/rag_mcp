"""Supplement Phase 37 Backtest B11/B12 with inline contract evidence.

CEK-TA-422 handles only candidate enrichment and reaudit package export.
It does not create formal reviewed knowledge, approved knowledge, default
guidance, or hard gates.
"""

from __future__ import annotations

import hashlib
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
TASK_ID = "CEK-TA-422"
PARTITION_ID = "KB_04_BACKTEST"
PACKAGE_ID = "phase37_backtest_b11_b12_inline_contract_reaudit_package_20260611"
PREVIOUS_AUDIT_RESULT_ID = "audit_result_phase37_backtest_reviewed_blocked_supplemental_reaudit_20260611_strict_v1"

ROOT = resolve_repo_path(start_file=__file__)
CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION_ID, start_file=__file__)
CONTRACT_PATH = resolve_repo_path("docs", "contracts", "phase37_backtest_run_manifest_contract.md", start_file=__file__)
SCHEMA_EXTRACT_PATH = resolve_repo_path(
    "docs", "contracts", "phase37_backtest_run_manifest_schema_extract.json", start_file=__file__
)
RESEARCH_PATH = resolve_repo_path(
    "docs", "research", "phase37_backtest_b11_b12_inline_contract_research.md", start_file=__file__
)
AUDIT_PACKAGE_PATH = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_backtest_b11_b12_inline_contract_report.json", start_file=__file__
)

TARGETS = {
    "P37-E-B11": "cand_20260611_phase37_backtest_reproducibility_package_required_001",
    "P37-E-B12": "cand_20260611_phase37_backtest_strategy_version_and_data_version_required_001",
}


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


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def append_unique(values: Any, additions: list[str]) -> list[str]:
    result = [item for item in values if isinstance(item, str)] if isinstance(values, list) else []
    for item in additions:
        if item not in result:
            result.append(item)
    return result


def has_mojibake(value: object) -> bool:
    text = json.dumps(value, ensure_ascii=False)
    return bool(re.search(r"(�|锟|烫|屯|Ã|Â|\?{2,})", text))


def build_schema_extract(contract_text: str) -> dict[str, Any]:
    contract_hash = sha256_text(contract_text)
    return {
        "schema_extract_id": "phase37_backtest_run_manifest_schema_extract_v1",
        "schema_version": "1.0.0",
        "generated_at": TODAY,
        "contract_path": rel(CONTRACT_PATH),
        "contract_sha256": contract_hash,
        "object": "BacktestRunManifest",
        "purpose": "支撑 Backtest reviewed/caveat_only 知识的复现、版本、指标和审计字段本体。",
        "hard_boundaries": {
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "notes": [
                "本契约只用于回测证据审计和复现追踪。",
                "不得用于生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
                "MLflow、DVC、QuantConnect 等只能作为等价实现示例，不是强制工具依赖。",
            ],
        },
        "sections": {
            "run_identity": {
                "required": True,
                "fields": {
                    "backtest_run_id": {"type": "string", "required": True, "semantics": "回测运行唯一 ID。"},
                    "created_at": {"type": "ISO-8601 timestamp", "required": True, "semantics": "运行创建时间。"},
                    "created_by": {"type": "enum", "required": True, "allowed": ["human", "system", "ci"]},
                    "project_id": {"type": "string", "required": True, "semantics": "外接项目或研究项目 ID。"},
                    "environment": {
                        "type": "enum",
                        "required": True,
                        "allowed": ["research", "validation", "paper_precheck"],
                    },
                    "engine_name": {"type": "string", "required": True, "semantics": "回测引擎名称。"},
                    "engine_version": {"type": "string", "required": True, "semantics": "回测引擎版本。"},
                    "engine_config_hash": {"type": "sha256-or-equivalent", "required": True},
                },
            },
            "strategy_identity": {
                "required": True,
                "owner": "Strategy Engineering",
                "fields": {
                    "strategy_id": {"type": "string", "required": True},
                    "strategy_rule_version": {
                        "type": "semantic-version-or-policy-version",
                        "required": True,
                        "generation_rule": "策略规则、信号定义或决策规则变更时必须递增。",
                        "validation_rule": "同一 backtest_run_id 只能绑定一个 strategy_rule_version。",
                    },
                    "strategy_code_commit": {"type": "git-commit-or-vcs-revision", "required": True},
                    "parameter_set_id": {"type": "string", "required": True},
                    "parameter_hash": {
                        "type": "sha256-or-equivalent",
                        "required": True,
                        "generation_rule": "对规范化参数 JSON 按稳定 key 顺序哈希。",
                        "validation_rule": "参数内容变化必须导致 parameter_hash 变化。",
                    },
                    "signal_schema_version": {"type": "string", "required": True},
                    "decision_policy_version": {"type": "string", "required": True},
                },
            },
            "data_identity": {
                "required": True,
                "owner": "Data Engineering",
                "fields": {
                    "dataset_id": {"type": "string", "required": True},
                    "dataset_version": {
                        "type": "dataset-version-or-snapshot-id",
                        "required": True,
                        "generation_rule": "数据快照、修正、复权或质量规则变化时必须更新。",
                    },
                    "source_dataset_version": {"type": "string", "required": True},
                    "symbol_universe_version": {"type": "string", "required": True},
                    "corporate_action_version": {"type": "string", "required": True},
                    "adjustment_policy_id": {"type": "string", "required": True},
                    "data_quality_report_id": {"type": "string", "required": True},
                    "available_time_policy_id": {"type": "string", "required": True},
                },
            },
            "market_calendar_identity": {
                "required": True,
                "owner": "Market Microstructure / Data Engineering",
                "fields": {
                    "market": {"type": "string", "required": True},
                    "venue": {"type": "string", "required": True},
                    "timezone": {"type": "IANA timezone", "required": True},
                    "calendar_version": {"type": "string", "required": True},
                    "session_template_version": {"type": "string", "required": True},
                    "holiday_calendar_version": {"type": "string", "required": True},
                    "early_close_calendar_version": {"type": "string", "required": True},
                },
            },
            "execution_assumption_identity": {
                "required": True,
                "owner": "Replay / Simulation / Live Execution",
                "fields": {
                    "cost_model_version": {"type": "string", "required": True},
                    "fee_model_version": {"type": "string", "required": True},
                    "slippage_model_version": {"type": "string", "required": True},
                    "spread_model_version": {"type": "string", "required": True},
                    "fill_model_version": {"type": "string", "required": True},
                    "order_type_policy_id": {"type": "string", "required": True},
                    "liquidity_assumption_id": {"type": "string", "required": True},
                },
            },
            "metric_report": {
                "required": True,
                "fields": {
                    "metric_report_id": {"type": "string", "required": True},
                    "metric_schema_version": {"type": "string", "required": True},
                    "gross_metrics": {"type": "object", "required": True},
                    "net_metrics": {"type": "object", "required": True},
                    "research_metrics": {"type": "object", "required": True},
                    "validation_metrics": {"type": "object", "required": True},
                    "trade_count": {"type": "integer", "required": True},
                    "profit_factor": {
                        "type": "number-or-undefined_or_infinite",
                        "required": True,
                        "validation_rule": "gross_loss_abs=0 时必须标记 undefined_or_infinite，不得静默写成极大优势。",
                    },
                    "max_drawdown": {"type": "number", "required": True},
                    "return_over_max_drawdown": {"type": "number", "required": True},
                    "fees": {"type": "number", "required": True},
                    "estimated_slippage": {"type": "number", "required": True},
                    "metric_limitations": {"type": "array[string]", "required": True},
                },
            },
            "reproducibility_package": {
                "required": True,
                "owner": "Backtest / Research Ops",
                "fields": {
                    "package_id": {"type": "string", "required": True},
                    "code_repository": {"type": "string", "required": True},
                    "code_commit": {"type": "git-commit-or-vcs-revision", "required": True},
                    "dependency_lockfile_hash": {"type": "sha256-or-equivalent", "required": True},
                    "container_image_digest": {"type": "string|null", "required": False},
                    "random_seed": {"type": "integer|null", "required": True},
                    "config_file_hash": {"type": "sha256-or-equivalent", "required": True},
                    "input_artifact_ids": {"type": "array[string]", "required": True},
                    "output_artifact_ids": {"type": "array[string]", "required": True},
                    "log_artifact_id": {"type": "string", "required": True},
                    "metric_report_id": {"type": "string", "required": True},
                    "lineage_id": {"type": "string", "required": True},
                    "replay_command_or_ci_job_id": {"type": "string", "required": True},
                    "known_non_determinism": {"type": "array[string]", "required": True},
                },
            },
        },
        "cross_owner_mapping": {
            "strategy_rule_version": "Strategy Engineering owns strategy rule identity.",
            "parameter_hash": "Strategy Engineering owns normalized parameter hashing; Backtest records it immutably.",
            "dataset_version": "Data Engineering owns dataset/version/snapshot semantics.",
            "calendar_version": "Market Microstructure/Data Engineering own session and calendar evidence.",
            "cost_model_version": "Replay/Simulation and Execution owners define cost/fill/slippage assumptions.",
            "fill_model_version": "Replay/Simulation owns fill model assumptions; Backtest records version only.",
            "evaluation_timestamp": "Backtest owns evaluation timestamp and must separate parameter search from final evaluation.",
        },
    }


def source_key(source: dict[str, Any]) -> tuple[str, str]:
    return (str(source.get("source_id") or ""), str(source.get("source_url") or source.get("source_title") or ""))


def ensure_source(candidate: dict[str, Any], source: dict[str, Any]) -> None:
    refs = candidate.setdefault("source_refs", [])
    if not isinstance(refs, list):
        refs = []
        candidate["source_refs"] = refs
    keys = {source_key(item) for item in refs if isinstance(item, dict)}
    if source_key(source) not in keys:
        refs.append(source)


def patch_candidate(candidate: dict[str, Any], task_id: str, contract_hash: str, schema_extract: dict[str, Any]) -> dict[str, Any]:
    inline_source = {
        "source_id": f"src_p37_backtest_inline_contract_{task_id.lower().replace('-', '_')}",
        "source_title": "Phase 37 Backtest Run Manifest Contract - inline schema extract",
        "source_url": rel(SCHEMA_EXTRACT_PATH),
        "source_type": "internal_contract_schema_extract",
        "publisher": "CEK-TA",
        "published_at": TODAY,
        "accessed_at": TODAY,
        "version": schema_extract["schema_version"],
        "reliability": "high",
        "relevance": "high",
        "score": 92,
        "evidence_summary": "内联 backtest_run_manifest 字段表、required/optional 标记、字段语义、生成规则、校验规则和 contract sha256。",
        "limitations": ["只支撑 CEK-TA 内部逻辑字段；外部项目可映射等价字段，不要求相同物理表名。"],
        "quoted_excerpt_allowed": False,
    }
    ensure_source(candidate, inline_source)

    candidate["_inline_contract_evidence"] = {
        "task_id": TASK_ID,
        "contract_path": rel(CONTRACT_PATH),
        "schema_extract_path": rel(SCHEMA_EXTRACT_PATH),
        "contract_sha256": contract_hash,
        "schema_extract_id": schema_extract["schema_extract_id"],
        "inline_sections_for_audit": [
            "strategy_identity",
            "data_identity",
            "market_calendar_identity",
            "execution_assumption_identity",
            "reproducibility_package",
        ],
    }

    source_quality = candidate.setdefault("source_quality", {})
    source_quality["internal_contract_evidence_status"] = "inline_schema_extract_added"
    source_quality["internal_contract_sha256"] = contract_hash
    source_quality["limitations"] = append_unique(
        source_quality.get("limitations", []),
        [
            "CEK-TA 内部字段本体现在以 schema extract 和 contract sha256 形式进入再审包。",
            "MLflow、DVC、QuantConnect 只能作为实现语义示例，不能替代 CEK-TA backtest_run_manifest 字段契约。",
            "本轮仍只请求 reviewed/caveat_only，不请求 approved/default guidance/hard gate。",
        ],
    )

    claim = candidate.setdefault("claim", {})
    if task_id == "P37-E-B11":
        claim["statement"] = (
            "回测若要作为可复用研究证据，必须提供可复现实验包；该包至少绑定代码版本、依赖锁定、配置哈希、"
            "随机种子、输入输出 artifact、日志、metric_report、lineage 和 replay job。"
        )
        claim["evidence_summary"] = (
            "CEK-TA 内联 schema extract 定义 reproducibility_package 字段表；MLflow/DVC 支撑实验追踪和可复现 pipeline "
            "的通用实现语义，但不替代 CEK-TA 字段契约。"
        )
    else:
        claim["statement"] = (
            "回测结论必须同时绑定 strategy_rule_version、parameter_hash、data_version、market calendar/session version、"
            "cost/fill/slippage model version 和 evaluation timestamp；否则无法审计策略、数据、日历和执行假设是否一致。"
        )
        claim["evidence_summary"] = (
            "CEK-TA 内联 schema extract 定义 strategy/data/calendar/execution identity 字段；MLflow dataset/model registry "
            "只作为版本追踪 supporting source。"
        )
    claim["claim_strength"] = "reviewed_caveat_only_pending_reaudit"

    applicability = candidate.setdefault("applicability", {})
    applicability["limitations"] = append_unique(
        applicability.get("limitations", []),
        [
            "本候选只约束回测证据包完整性，不证明策略盈利能力。",
            "本候选不生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
            "字段本体由 CEK-TA contract/schema extract 支撑，外部工具文档只支撑等价实现模式。",
        ],
    )

    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "supplemented_for_inline_contract_reaudit"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["current_task_id"] = TASK_ID
    workflow["next_action"] = "external_ai_or_human_inline_contract_reaudit"
    workflow["next_allowed_decisions"] = [
        "accepted_for_reviewed_caveat_only",
        "needs_more_evidence",
        "rejected",
        "blocked",
    ]
    workflow["forbidden_decisions"] = ["approved", "default_guidance", "hard_gate"]
    workflow["formalization_allowed"] = False
    workflow["approved_allowed"] = False
    workflow["default_guidance_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False

    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "ready_for_inline_contract_reaudit"
    status["decision_reason"] = "已补充内联 contract/schema extract、字段表和 schema hash，等待 reviewed/caveat_only 再审。"
    status["updated_at"] = TODAY

    review = candidate.setdefault("review", {})
    review["open_questions"] = [
        "审计方是否认可内联 schema extract 足以支撑 CEK-TA backtest_run_manifest 字段本体？",
        "审计方是否认可 B11/B12 仍只能进入 reviewed/caveat_only，而不能进入 approved/default guidance/hard gate？",
        "审计方是否发现与 Data Engineering、Market Microstructure、Replay 或 Execution owner 字段存在冲突或重复？",
    ]
    audit_log = review.setdefault("audit_log", [])
    if not isinstance(audit_log, list):
        audit_log = []
        review["audit_log"] = audit_log
    audit_log.append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "phase37_backtest_b11_b12_inline_contract_supplemented",
            "reason": "CEK-TA-422: 内联 backtest_run_manifest contract/schema extract，补字段表、schema hash 和 owner 映射。",
            "audit_result_id": f"pending_{PACKAGE_ID}",
        }
    )
    review["inline_contract_reaudit"] = {
        "package_id": PACKAGE_ID,
        "previous_audit_result_id": PREVIOUS_AUDIT_RESULT_ID,
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "required_checks": [
            "full_contract_text_present",
            "schema_extract_present",
            "contract_sha256_present",
            "required_optional_field_table_present",
            "cross_owner_mapping_present",
            "tool_docs_not_used_as_internal_contract",
        ],
    }
    return candidate


def write_research(contract_hash: str, schema_extract: dict[str, Any]) -> None:
    content = f"""# Phase 37 Backtest B11/B12 内联契约补证记录

生成日期：{TODAY}

## 任务

`CEK-TA-422` 只处理：

```text
P37-E-B11 backtest.reproducibility_package_required
P37-E-B12 backtest.strategy_version_and_data_version_required
```

上一轮审计认为 B11/B12 的外部来源足以支持 MLflow/DVC 等实验追踪模式，但不足以支持 CEK-TA 内部字段本体，因为 `backtest_run_manifest_contract.md` 只被路径引用，没有内联正文、字段表、schema extract 或 hash。

## 本轮补丁

```text
contract_path: {rel(CONTRACT_PATH)}
schema_extract_path: {rel(SCHEMA_EXTRACT_PATH)}
contract_sha256: {contract_hash}
schema_extract_id: {schema_extract["schema_extract_id"]}
```

## 字段范围

本轮重点内联：

```text
reproducibility_package:
  code_repository, code_commit, dependency_lockfile_hash, container_image_digest,
  random_seed, config_file_hash, input_artifact_ids, output_artifact_ids,
  log_artifact_id, metric_report_id, lineage_id, replay_command_or_ci_job_id,
  known_non_determinism

strategy_identity:
  strategy_rule_version, strategy_code_commit, parameter_hash, signal_schema_version,
  decision_policy_version

data_identity:
  dataset_version, source_dataset_version, symbol_universe_version,
  corporate_action_version, adjustment_policy_id, data_quality_report_id,
  available_time_policy_id

market_calendar_identity:
  calendar_version, session_template_version, holiday_calendar_version,
  early_close_calendar_version

execution_assumption_identity:
  cost_model_version, fee_model_version, slippage_model_version,
  spread_model_version, fill_model_version, order_type_policy_id,
  liquidity_assumption_id
```

## 审计边界

```text
1. candidate 不是 formal knowledge。
2. 本包最多允许 accepted_for_reviewed_caveat_only。
3. 不允许 approved。
4. 不允许 default guidance。
5. 不允许 hard gate。
6. 不允许生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。
```
"""
    RESEARCH_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_PATH.write_text(content, encoding="utf-8")


def build_audit_package(candidates: list[dict[str, Any]], contract_text: str, schema_extract: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": PACKAGE_ID,
        "package_type": "candidate_inline_contract_reaudit_package",
        "schema_version": "1.0.0",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "language": "zh-CN",
        "phase": "37",
        "title": "Phase 37 Backtest B11/B12 内联契约再审包",
        "purpose": "严格复审 B11/B12 在补齐 CEK-TA backtest_run_manifest contract 正文、schema extract、字段表和 hash 后，是否可进入 formal reviewed/caveat_only。",
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
            "重点检查内联 contract/schema extract 是否足以支撑 CEK-TA reproducibility_package 和 version identity 字段本体。",
            "检查 MLflow/DVC/QuantConnect 等工具文档是否只作为实现语义示例，而没有被误写成强制依赖。",
            "检查 B11 是否完整覆盖代码版本、依赖、配置、随机种子、输入输出 artifact、日志、lineage 和 replay job。",
            "检查 B12 是否完整覆盖 strategy/data/calendar/execution assumption identity，以及跨 Data Engineering、Market Microstructure、Replay、Execution owner 映射。",
            "如果仍缺来源、字段定义、owner 映射、冲突审计或边界，必须返回 needs_more_evidence 或 blocked。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": PACKAGE_ID,
            "auditor": "string",
            "audited_at": "YYYY-MM-DD",
            "quality_gate": {"pass": "boolean", "candidate_count": 2, "notes": ["string"]},
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "P37-E-B11 | P37-E-B12",
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | medium_high | high",
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
        "contract_inline": {
            "path": rel(CONTRACT_PATH),
            "full_text": contract_text,
            "schema_extract_path": rel(SCHEMA_EXTRACT_PATH),
            "schema_extract": schema_extract,
        },
        "source_review_notes": {
            "internal_contract_source": "CEK-TA contract/schema extract 是字段本体主来源。",
            "external_tool_sources": "MLflow、DVC、QuantConnect 等只能作为 implementation pattern 或 supporting source。",
            "source_quality_boundary": "不得把 tool-specific docs 写成 universal platform requirement。",
        },
        "candidates": candidates,
    }


def quality_gate(package: dict[str, Any], schema_extract: dict[str, Any]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    candidates = package.get("candidates", [])
    if not isinstance(candidates, list) or len(candidates) != 2:
        failures.append({"failure": "candidate_count_not_2"})
    if not package.get("contract_inline", {}).get("full_text"):
        failures.append({"failure": "contract_full_text_missing"})
    if not schema_extract.get("contract_sha256"):
        failures.append({"failure": "contract_sha256_missing"})
    required_sections = {
        "strategy_identity",
        "data_identity",
        "market_calendar_identity",
        "execution_assumption_identity",
        "reproducibility_package",
    }
    if not required_sections.issubset(set(schema_extract.get("sections", {}).keys())):
        failures.append({"failure": "required_schema_sections_missing"})
    for candidate in candidates if isinstance(candidates, list) else []:
        workflow = candidate.get("workflow", {}) if isinstance(candidate, dict) else {}
        if workflow.get("stage") != "supplemented_for_inline_contract_reaudit":
            failures.append({"failure": f"{candidate.get('candidate_id')}:workflow_stage_wrong"})
        for key in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed"):
            if workflow.get(key) is not False:
                failures.append({"failure": f"{candidate.get('candidate_id')}:workflow_{key}_not_false"})
        if workflow.get("hidden_from_default_queue") is not True:
            failures.append({"failure": f"{candidate.get('candidate_id')}:hidden_from_default_queue_not_true"})
    if has_mojibake(package):
        failures.append({"failure": "mojibake_marker_detected"})
    return {
        "gate_id": "phase37_backtest_b11_b12_inline_contract_quality_gate",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "candidate_count": len(candidates) if isinstance(candidates, list) else 0,
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "formal_reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_created": 0,
        "hard_gate_created": 0,
    }


def main() -> int:
    contract_text = CONTRACT_PATH.read_text(encoding="utf-8")
    schema_extract = build_schema_extract(contract_text)
    write_json(SCHEMA_EXTRACT_PATH, schema_extract)

    candidates: list[dict[str, Any]] = []
    for task_id, candidate_id in TARGETS.items():
        path = CANDIDATE_DIR / f"{candidate_id}.json"
        candidate = read_json(path)
        patched = patch_candidate(candidate, task_id, schema_extract["contract_sha256"], schema_extract)
        write_json(path, patched)
        candidates.append(patched)

    write_research(schema_extract["contract_sha256"], schema_extract)
    package = build_audit_package(candidates, contract_text, schema_extract)
    gate = quality_gate(package, schema_extract)
    package["quality_gate"] = gate
    write_json(AUDIT_PACKAGE_PATH, package)

    report = {
        "report_id": "phase37_backtest_b11_b12_inline_contract_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "package_id": PACKAGE_ID,
        "targets": list(TARGETS.keys()),
        "schema_extract": rel(SCHEMA_EXTRACT_PATH),
        "contract_path": rel(CONTRACT_PATH),
        "contract_sha256": schema_extract["contract_sha256"],
        "research_record": rel(RESEARCH_PATH),
        "audit_package": rel(AUDIT_PACKAGE_PATH),
        "quality_gate": gate,
        "boundary": "Candidate supplement only; no formal reviewed knowledge, approved knowledge, default guidance, hard gate, or MCP index change was created.",
        "next_action": "把再审包交给外部 AI/人工严格审计；若返回 accepted_for_reviewed_caveat_only 且 reviewed_allowed=true，再执行 CEK-TA-423。",
    }
    write_json(REPORT_PATH, report)
    if gate["gate_status"] != "pass":
        raise SystemExit(f"quality gate failed: {gate['failures']}")
    print(json.dumps({"audit_package": rel(AUDIT_PACKAGE_PATH), "quality_gate": gate["gate_status"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
