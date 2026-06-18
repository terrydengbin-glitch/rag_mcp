"""Export Phase 37 Trade Analysis supplemental reviewed reaudit package.

The first reviewed-preparation audit returned 12 ``needs_more_evidence``
decisions because the package lacked inline CEK-TA Trade Analysis contracts.
This exporter includes the internal contract full text, schema extract, and
hash so an external auditor can decide whether the 12 candidates may become
formal reviewed/caveat_only.
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 12).isoformat()
TASK_ID = "CEK-TA-447"
PACKAGE_ID = "phase37_trade_analysis_blocked_supplemental_reaudit_package_20260612"
PARTITION_ID = "KB_07_TRADE_ANALYSIS"
PRIOR_AUDIT_RESULT_ID = "audit_result_phase37_trade_analysis_reviewed_preparation_20260612_strict_v1"

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION_ID, start_file=__file__)
CONTRACT_PATH = resolve_repo_path("docs", "contracts", "phase37_trade_analysis_review_contract.md", start_file=__file__)
AUDIT_PATH = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_trade_analysis_blocked_supplemental_report.json", start_file=__file__
)
RESEARCH_PATH = resolve_repo_path(
    "docs", "research", "phase37_trade_analysis_blocked_supplemental_research.md", start_file=__file__
)
ROOT = resolve_repo_path(".", start_file=__file__)


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def candidate_id(candidate: dict[str, Any]) -> str:
    return str(candidate.get("candidate_id", ""))


def load_candidates() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for path in sorted(CANDIDATE_DIR.glob("cand_20260612_phase37_trade_analysis_*.json")):
        candidate = read_json(path)
        if candidate_id(candidate).startswith("cand_20260612_phase37_trade_analysis_"):
            candidates.append(candidate)
    return sorted(candidates, key=lambda item: str(item.get("research_task_id")))


def contract_payload() -> dict[str, Any]:
    full_text = CONTRACT_PATH.read_text(encoding="utf-8")
    sha256 = hashlib.sha256(full_text.encode("utf-8")).hexdigest()
    return {
        "contract_id": "phase37_trade_analysis_review_contract",
        "version": "1.0.0",
        "path": CONTRACT_PATH.relative_to(ROOT).as_posix(),
        "sha256": sha256,
        "full_text": full_text,
        "schema_extract": {
            "base_record": [
                "review_id",
                "trade_id",
                "trade_plan_id",
                "strategy_id",
                "strategy_rule_version",
                "data_version",
                "market_context_id",
                "risk_policy_id",
                "order_trace_id",
                "fill_trace_id",
                "reviewer_id",
                "reviewed_at",
                "audit_trace_id",
                "schema_version",
            ],
            "r_decomposition": [
                "planned_initial_risk_amount",
                "planned_initial_risk_unit",
                "planned_reward_r",
                "planned_risk_reward_ratio",
                "actual_gross_pnl",
                "actual_net_pnl",
                "realized_r",
                "fee_amount",
                "slippage_amount",
                "risk_basis",
                "cost_basis",
                "exit_basis",
                "calculation_trace_id",
            ],
            "mae_mfe": [
                "price_path_source_id",
                "path_granularity",
                "path_start_time",
                "path_end_time",
                "mae_price",
                "mfe_price",
                "mae_r",
                "mfe_r",
                "missing_path_policy",
                "path_quality_flag",
            ],
            "taxonomy_and_reason_code": [
                "taxonomy_version",
                "labels",
                "primary_label",
                "severity",
                "reason_code_id",
                "category",
                "owner",
                "multi_label_allowed",
                "migration_rule",
            ],
            "quality_review": [
                "quality_dimension",
                "planned_ref",
                "actual_ref",
                "rule_ref",
                "compliance_status",
                "deviation_type",
                "evidence_refs",
                "owner_ref",
            ],
            "hypothesis_lifecycle": [
                "hypothesis_id",
                "source_trade_set_id",
                "hypothesis_statement",
                "validation_protocol_id",
                "oos_required",
                "cost_check_required",
                "regime_check_required",
                "promotion_criteria",
                "status",
            ],
        },
        "owner_boundary_summary": {
            "trade_analysis_owns": [
                "post_trade_review",
                "trade_quality_attribution",
                "reason_code",
                "bad_case_taxonomy",
                "label_candidate",
                "research_hypothesis_generation",
            ],
            "trade_analysis_does_not_own": [
                "R/R-multiple core definition",
                "strategy rule source of truth",
                "market data source of truth",
                "real orders/fills/account facts",
                "risk thresholds/hard gates",
                "LLM model training authority",
            ],
        },
    }


def package_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    review_audit = deep_get(candidate, ("review", "reviewed_preparation_audit"), {})
    return {
        "candidate_id": candidate.get("candidate_id"),
        "research_task_id": candidate.get("research_task_id"),
        "current_status": {
            "review_status": deep_get(candidate, ("status", "review_status")),
            "ingestion_decision": deep_get(candidate, ("status", "ingestion_decision")),
            "workflow_stage": deep_get(candidate, ("workflow", "stage")),
            "queue_group": deep_get(candidate, ("workflow", "queue_group")),
            "reviewed_preparation_audit_result_id": deep_get(candidate, ("workflow", "reviewed_preparation_audit_result_id")),
        },
        "conversion_target": candidate.get("conversion_target", {}),
        "classification": candidate.get("classification", {}),
        "claim": candidate.get("claim", {}),
        "applicability": candidate.get("applicability", {}),
        "source_refs": candidate.get("source_refs", []),
        "source_quality": candidate.get("source_quality", {}),
        "conflict_audit": candidate.get("conflict_audit", {}),
        "llm_usage_policy": candidate.get("llm_usage_policy", {}),
        "machine_gate": candidate.get("machine_gate", {}),
        "prior_reviewed_preparation_audit": review_audit,
        "required_contract_evidence": {
            "contract_id": "phase37_trade_analysis_review_contract",
            "covers_missing_contracts": deep_get(review_audit, ("schema_contract_assessment", "missing_contracts"), []),
            "field_level_gaps_from_prior_audit": deep_get(review_audit, ("schema_contract_assessment", "field_level_gaps"), []),
        },
        "requested_audit_decision": [
            "accepted_for_reviewed_caveat_only",
            "needs_more_evidence",
            "rejected",
            "blocked",
        ],
    }


def build_gate(candidates: list[dict[str, Any]], contract: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    if len(candidates) != 12:
        failures.append(f"expected 12 Trade Analysis candidates, got {len(candidates)}")
    for candidate in candidates:
        if deep_get(candidate, ("status", "ingestion_decision")) != "needs_more_evidence":
            failures.append(f"{candidate_id(candidate)}: expected needs_more_evidence")
        if deep_get(candidate, ("workflow", "next_action")) != "supplement_trade_analysis_contract_schema_then_reaudit":
            failures.append(f"{candidate_id(candidate)}: unexpected next_action")
        for path in [
            ("machine_gate", "approved_allowed"),
            ("machine_gate", "default_guidance_allowed"),
            ("machine_gate", "hard_gate_allowed"),
            ("machine_gate", "risk_threshold_advice_allowed"),
        ]:
            if deep_get(candidate, path) is not False:
                failures.append(f"{candidate_id(candidate)}: {'.'.join(path)} must be false")
    if not contract.get("full_text"):
        failures.append("contract full_text missing")
    if not contract.get("sha256"):
        failures.append("contract sha256 missing")
    counts = Counter(deep_get(candidate, ("status", "ingestion_decision")) for candidate in candidates)
    return {
        "gate_id": "phase37_trade_analysis_blocked_supplemental_gate",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "candidate_count": len(candidates),
        "status_counts": dict(counts),
        "contract_id": contract.get("contract_id"),
        "contract_sha256": contract.get("sha256"),
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本包只请求 reviewed/caveat_only；不得创建 approved、default guidance、hard gate 或风险阈值建议。",
            "Trade Analysis 只做 post-trade 复盘、标签、reason code、质量归因、坏例 taxonomy 和研究假设。",
            "复盘发现不能直接改实时交易规则，必须进入 research hypothesis 并经独立验证。",
        ],
    }


def build_package(candidates: list[dict[str, Any]], contract: dict[str, Any], gate: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": PACKAGE_ID,
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "package_type": "blocked_supplemental_reviewed_caveat_only_reaudit",
        "scope": {
            "phase": "Phase 37",
            "branch": "Trading Engineering",
            "partition_id": PARTITION_ID,
            "tree_node_id": "kt.trade_analysis",
            "candidate_count": len(candidates),
            "prior_audit_result_id": PRIOR_AUDIT_RESULT_ID,
            "target": "复核 12 条 Trade Analysis needs_more_evidence 候选在补充 CEK-TA 内部契约后，是否可转 formal reviewed/caveat_only。",
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
            "必须搜索相关的专业网站、论文、官方文档、资料、案例和数据，对本补证再审包进行严格审计。",
            "本轮重点检查 contract_inline.full_text、schema_extract 和 contract_sha256 是否足以补齐上一轮 12 条 needs_more_evidence 缺口。",
            "逐条判断是否可进入 formal reviewed/caveat_only；不得允许 approved、default guidance、hard gate 或风险阈值建议。",
            "检查 Trade Analysis 是否只负责 post-trade 复盘、标签、reason code、质量归因、bad-case taxonomy 和 research hypothesis。",
            "检查 Quant Foundation、Strategy、Data、Replay、Live Execution、Risk Management、AI Engineering owner 边界是否清晰。",
            "检查是否有中文乱码、mock/test 污染、项目私有参数、账户事实、密钥、交易所私有配置或实盘敏感信息。",
        ],
        "contract_inline": contract,
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": PACKAGE_ID,
            "quality_gate": {"pass": "boolean", "reason": "string"},
            "summary": {
                "total": 12,
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
                    "risk_threshold_advice_allowed": False,
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
        "candidates": [package_candidate(candidate) for candidate in candidates],
    }


def write_research_report(contract: dict[str, Any], gate: dict[str, Any]) -> None:
    text = f"""# Phase 37 Trade Analysis 补证研究说明

```text
task_id: {TASK_ID}
generated_at: {TODAY}
prior_audit_result_id: {PRIOR_AUDIT_RESULT_ID}
contract_id: {contract['contract_id']}
contract_sha256: {contract['sha256']}
gate_status: {gate['gate_status']}
```

## 补证原因

上一轮 reviewed-preparation 严格审计认为 12 条 Trade Analysis 候选方向正确，但缺少 `contract_inline`、schema 正文、字段表、`schema_extract` 或 contract hash，因此全部只能保持 `needs_more_evidence`。

## 本轮补证内容

已新增并内联：

```text
docs/contracts/phase37_trade_analysis_review_contract.md
```

覆盖：

```text
TradeReviewRecord
planned_vs_realized_r_decomposition
MAE/MFE calculation
bad_trade_taxonomy
good_loss_bad_win_policy
entry/exit/risk/execution quality review
rule_compliance
regime_fit_review
reason_code_taxonomy
research_hypothesis_lifecycle
owner boundary
machine gate
```

## 仍保留边界

```text
不得创建 approved
不得启用 default guidance
不得启用 hard gate
不得给出风险阈值数值
不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议
```
"""
    write_text(RESEARCH_PATH, text)


def main() -> int:
    candidates = load_candidates()
    contract = contract_payload()
    gate = build_gate(candidates, contract)
    write_json(REPORT_PATH, gate)
    write_json(AUDIT_PATH, build_package(candidates, contract, gate))
    write_research_report(contract, gate)
    print(
        json.dumps(
            {
                "status": gate["gate_status"],
                "candidate_count": len(candidates),
                "contract_sha256": contract["sha256"],
                "audit_package": str(AUDIT_PATH),
                "report": str(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
