# CEK-TA RAG Metadata Schema

This schema defines metadata required for every CEK-TA knowledge item.

It is a contract for ingestion, retrieval, MCP output, conflict audit, Vue3 review UI, and knowledge contribution workflows.

## Required Object

```json
{
  "knowledge_id": "string",
  "title": "string",
  "partition_id": "KB_01_QUANT_FOUNDATION | KB_02_KLINE_STRATEGY | KB_03_MARKET_MICROSTRUCTURE | KB_04_BACKTEST | KB_05_REPLAY_SIMULATION | KB_06_LIVE_EXECUTION | KB_07_TRADE_ANALYSIS | KB_08_LLM_TRAINING | KB_09_RAG_ENGINEERING | KB_10_PROJECT_RUNBOOKS",
  "domain": "quant_trading | kline_strategy | market_microstructure | backtest | replay_simulation | live_trading | trade_analysis | llm_training | rag_engineering | project_runbooks",
  "subdomain": "string",
  "rule_type": "definition | principle | procedure | formula | checklist | anti_pattern | adapter_rule | schema | incident | eval_case",
  "claim_type": "methodological_constraint | risk_boundary_rule | execution_safety_rule | data_quality_rule | backtest_validity_rule | rag_governance_rule | mcp_contract_rule | knowledge_governance_rule | project_integration_rule",
  "content_type": "markdown | json | yaml | code | report | task_card",
  "source_type": "official_doc | paper | exchange_rule | framework_doc | book | research_report | engineering_article | internal_report | task_card | code_doc | runbook",
  "source": {
    "title": "string",
    "url": "string | null",
    "publisher": "string | null",
    "published_at": "YYYY-MM-DD | null",
    "accessed_at": "YYYY-MM-DD",
    "version": "string | null",
    "reliability": "high | medium | low"
  },
  "project_binding": "none | project_name | sanitized_project_case",
  "classification_notes": "string | null",
  "applies_to": {
    "market": "crypto | futures | spot | stock | general",
    "asset": "BTC | ETH | multi | general",
    "timeframe": "tick | 1s | 1m | 3m | 15m | 1h | 4h | 1d | general",
    "data_granularity": "tick | trade | order_book | second | kline | account_event | general",
    "project_type": "kline_trend_strategy | abnormal_move_strategy | high_fidelity_simulator | live_binance_futures | trading_llm_assistant | general"
  },
  "used_for": [
    "strategy_design",
    "code_review",
    "backtest_review",
    "replay",
    "simulation",
    "live_trading",
    "trade_analysis",
    "llm_training",
    "rag_engineering",
    "mcp",
    "vue_audit_ui"
  ],
  "assumptions": ["string"],
  "not_applicable_when": ["string"],
  "evidence_summary": "string",
  "conflict_status": "none | potential | confirmed | resolved | deprecated_by_conflict",
  "conflicts": [
    {
      "knowledge_id": "string",
      "conflict_type": "direct_conflict | scope_conflict | version_conflict | market_conflict | granularity_conflict | assumption_conflict",
      "resolution": "string"
    }
  ],
  "confidence": "high | medium | low",
  "freshness": "stable | time_sensitive | deprecated",
  "review_status": "draft | reviewed | approved | rejected | deprecated",
  "created_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD"
}
```

## ID Rules

```text
knowledge_id format:
<partition_id_lowercase>.<subdomain>.<slug>.v<version>

example:
kb_04_backtest.fill_model.same_candle_tp_sl.v1
```

## Required Fields

```text
knowledge_id
title
partition_id
domain
subdomain
rule_type
claim_type
content_type
source_type
source
project_binding
classification_notes
applies_to
used_for
assumptions
not_applicable_when
evidence_summary
conflict_status
claim_type
machine_gate.default_guidance
machine_gate.reason
confidence
freshness
review_status
created_at
updated_at
```

## Review Status Rules

```text
draft: newly created, not reviewed
reviewed: checked by Codex or reviewer, not approved
approved: allowed for retrieval as trusted CEK-TA knowledge
rejected: not allowed for retrieval
deprecated: retained for history, not recommended
```

Only `approved` items can be used as default professional guidance. Other statuses require explicit caveats.

## Claim Type Rules

```text
methodological_constraint: Method or research-process constraint, not a trading signal.
risk_boundary_rule: Boundary rule that prevents unsafe or overgeneralized usage.
execution_safety_rule: Execution, live-trading, adapter, order, or kill-switch safety rule.
data_quality_rule: Data alignment, leakage, missingness, or versioning rule.
backtest_validity_rule: Backtest credibility, fill model, overfitting, or metric-validity rule.
rag_governance_rule: RAG metadata, citation, retrieval, or source-quality rule.
mcp_contract_rule: MCP tool contract, permission, error, or read-only boundary rule.
knowledge_governance_rule: Knowledge lifecycle, source audit, conflict, or approval rule.
project_integration_rule: External project adapter, healthcheck, or backflow boundary rule.
```

Knowledge items must never be interpreted as trading signals solely from `rule_type`; `claim_type` is the safer AI routing field.

## Machine Gate Rules

```text
allow: approved, source-backed, no blocking conflict, not deprecated, no private data, default_guidance_allowed=true.
caveat_only: reviewed but not approved; usable for audit/search with explicit caveat.
deny: draft/rejected/deprecated, unsourced, confirmed conflict, low source quality, or private data risk.
```

MCP/RAG default guidance must use `machine_gate.default_guidance`, not only `review_status`.

## Freshness Rules

```text
stable: concepts unlikely to change quickly
time_sensitive: exchange rules, model APIs, market microstructure data-source behavior, library behavior
deprecated: outdated or superseded
```

Time-sensitive items must be rechecked before use in high-impact decisions.

## Project Binding Rules

```text
none: fully reusable general knowledge
project_name: tied to a specific project and not reusable by default
sanitized_project_case: contributed project case after sanitization
```

Reusable knowledge should normally use `none`.

## Conflict Rules

No item with `conflict_status = confirmed` can become `approved` unless the conflict resolution and applicability boundary are explicit.

## Retrieval Output Minimum

Any MCP/RAG retrieval result must return:

```text
knowledge_id
title
partition_id
domain
subdomain
content excerpt or summary
source
confidence
freshness
review_status
conflict_status
```
