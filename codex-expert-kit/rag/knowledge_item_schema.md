# CEK-TA Knowledge Item Schema

This file defines the full structured contract for a CEK-TA knowledge item.

`metadata_schema.md` defines retrieval metadata. This file extends it into an auditable knowledge object that can be used by RAG ingestion, MCP retrieval, Vue3 review, Skills, and knowledge contribution workflows.

## Schema Version

```text
schema_name: cek_ta_knowledge_item
schema_version: 1.1.0
encoding: UTF-8
```

## Required Object

```json
{
  "schema_version": "1.0.0",
  "knowledge_id": "kb_04_backtest.fill_model.same_candle_tp_sl.v1",
  "title": "string",
  "metadata": {
    "partition_id": "KB_01_QUANT_FOUNDATION | KB_02_KLINE_STRATEGY | KB_03_MARKET_MICROSTRUCTURE | KB_04_BACKTEST | KB_05_REPLAY_SIMULATION | KB_06_LIVE_EXECUTION | KB_07_TRADE_ANALYSIS | KB_08_LLM_TRAINING | KB_09_RAG_ENGINEERING | KB_10_PROJECT_RUNBOOKS",
    "domain": "quant_trading | kline_strategy | market_microstructure | backtest | replay_simulation | live_trading | trade_analysis | llm_training | rag_engineering | project_runbooks",
    "subdomain": "string",
    "rule_type": "definition | principle | procedure | formula | checklist | anti_pattern | adapter_rule | schema | incident | eval_case",
    "claim_type": "methodological_constraint | risk_boundary_rule | execution_safety_rule | data_quality_rule | backtest_validity_rule | rag_governance_rule | mcp_contract_rule | knowledge_governance_rule | project_integration_rule | llm_training_rule | llm_eval_rule | training_data_schema_rule | ai_security_rule | ai_governance_rule | llmops_release_rule",
    "content_type": "markdown | json | yaml | code | report | task_card",
    "project_binding": "none | project_name | sanitized_project_case",
    "classification_notes": "string | null",
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
    ]
  },
  "applicability": {
    "market": "crypto | futures | spot | stock | general",
    "asset": "BTC | ETH | multi | general",
    "timeframe": "tick | 1s | 1m | 3m | 15m | 1h | 4h | 1d | general",
    "data_granularity": "tick | trade | order_book | second | kline | account_event | general",
    "project_type": "kline_trend_strategy | abnormal_move_strategy | high_fidelity_simulator | live_binance_futures | trading_llm_assistant | general",
    "applies_when": ["string"],
    "not_applicable_when": ["string"]
  },
  "content": {
    "statement": "single clear rule or knowledge claim",
    "rationale": "why the rule exists",
    "procedure": ["optional execution or review steps"],
    "examples": ["optional generalized examples without private project data"],
    "anti_patterns": ["known misuse cases"],
    "validation": ["how to test or verify this knowledge"],
    "risk_notes": ["side effects, safety risks, model risks, market risks"],
    "citation_notes": "how the evidence supports the statement"
  },
  "assumptions": ["string"],
  "source_evidence": [
    {
      "source_id": "src_001",
      "source_title": "string",
      "source_url": "string | null",
      "source_type": "official_doc | paper | exchange_rule | framework_doc | book | research_report | engineering_article | internal_report | task_card | code_doc | runbook",
      "publisher": "string | null",
      "published_at": "YYYY-MM-DD | null",
      "accessed_at": "YYYY-MM-DD",
      "version": "string | null",
      "reliability": "high | medium | low",
      "relevance": "high | medium | low",
      "evidence_summary": "string",
      "quoted_excerpt_allowed": false
    }
  ],
  "source_quality": {
    "overall_reliability": "high | medium | low",
    "score": 0,
    "score_version": "1.0.0",
    "primary_source_count": 0,
    "supporting_source_count": 0,
    "limitations": ["string"]
  },
  "conflict_audit": {
    "conflict_status": "none | potential | confirmed | resolved | deprecated_by_conflict",
    "checked_against": ["knowledge_id"],
    "conflicts": [
      {
        "knowledge_id": "string",
        "conflict_type": "direct_conflict | scope_conflict | version_conflict | market_conflict | granularity_conflict | assumption_conflict",
        "severity": "blocking | warning | informational",
        "resolution": "string",
        "applicability_boundary": "string"
      }
    ],
    "resolution_summary": "string",
    "default_recommendation": "string | null"
  },
  "llm_usage_policy": {
    "allowed": ["string"],
    "not_allowed": ["string"],
    "required_context": ["string"],
    "fallback_behavior": "deny | ask_for_context | cite_with_caveat"
  },
  "machine_gate": {
    "default_guidance": "allow | caveat_only | deny",
    "reason": "string",
    "requires_human_escalation": true,
    "blocking_reasons": ["string"],
    "checked_at": "YYYY-MM-DD",
    "gate_version": "1.0.0"
  },
  "recommended_extra_sources": [
    {
      "title": "string",
      "source_url": "string | null",
      "source_type": "paper | official_doc | exchange_rule | framework_doc | book | research_report | engineering_article",
      "purpose": "string",
      "status": "proposed | verified | rejected"
    }
  ],
  "review": {
    "confidence": "high | medium | low",
    "freshness": "stable | time_sensitive | deprecated",
    "review_status": "draft | reviewed | approved | rejected | deprecated",
    "reviewer": "codex | human | mixed | null",
    "reviewed_at": "YYYY-MM-DD | null",
    "created_at": "YYYY-MM-DD",
    "updated_at": "YYYY-MM-DD",
    "open_questions": ["string"],
    "decision_log": [
      {
        "at": "YYYY-MM-DD",
        "actor": "codex | human",
        "decision": "created | reviewed | approved | rejected | deprecated | revised",
        "reason": "string"
      }
    ]
  },
  "contribution": {
    "contribution_id": "string | null",
    "source_project": "string | null",
    "sanitization_status": "not_applicable | proposed | sanitized | rejected",
    "private_data_removed": true,
    "generic_mapping_notes": "string | null"
  }
}
```

## Required Fields

```text
schema_version
knowledge_id
title
metadata
applicability
content.statement
content.rationale
assumptions
source_evidence
source_quality
conflict_audit
llm_usage_policy
machine_gate
review
contribution
```

## Schema v1.1 Additions

```text
metadata.claim_type: Machine-readable claim role. It prevents AI from treating a methodology, boundary, or governance rule as a trading signal.
metadata.classification_notes: Explains tree_node_id/canonical_node_id differences or special taxonomy decisions.
llm_usage_policy: Defines what an AI may do, may not do, and must know before using the item.
machine_gate: Direct default-guidance gate consumed by MCP, SearchLab, FastAPI, Vue3, and external projects.
recommended_extra_sources: Proposed source-strengthening queue. These entries are not formal evidence until verified and moved into source_evidence.
```

`reviewed` knowledge must use `machine_gate.default_guidance = caveat_only` unless a later human governance task promotes it to `approved`.

`recommended_extra_sources` must not be counted as `source_evidence`.

## Approval Gate

An item can become `approved` only when:

```text
1. source_evidence has at least one source.
2. source_quality.overall_reliability is high or medium.
3. applicability.applies_when and applicability.not_applicable_when are explicit.
4. assumptions are explicit, even if the list only says "no additional assumptions identified".
5. conflict_audit.conflict_status is none or resolved.
6. freshness is not deprecated.
7. project_binding is none or sanitized_project_case.
8. no secrets, account data, private order data, or project-private fields remain.
9. machine_gate.default_guidance is allow.
```

## State Flow

```text
draft
  -> reviewed
  -> approved
  -> deprecated

draft
  -> reviewed
  -> rejected

approved
  -> reviewed
  -> approved

approved
  -> deprecated
```

Direct `draft -> approved` is forbidden. Direct deletion is forbidden for previously approved items; use `deprecated`.

## RAG Ingestion Rules

```text
1. Ingest only draft, reviewed, approved, or deprecated items; never ingest rejected items as normal retrieval candidates.
2. Retrieval should default to approved items.
3. Draft and reviewed items may appear only in audit views or with explicit caveats.
4. Every chunk derived from the item must retain knowledge_id, source_id references, review_status, conflict_status, confidence, and freshness.
5. Time-sensitive items must carry accessed_at and reviewed_at.
6. Default guidance retrieval must only use items whose machine_gate.default_guidance is allow.
7. reviewed items may be returned only with caveat when machine_gate.default_guidance is caveat_only.
```

## Vue3 Audit UI Minimum Fields

Vue3 must be able to display and filter by:

```text
knowledge_id
title
partition_id
domain
subdomain
rule_type
review_status
conflict_status
confidence
freshness
overall_reliability
score
source_count
claim_type
machine_gate.default_guidance
machine_gate.blocking_reasons
llm_usage_policy
market
timeframe
data_granularity
updated_at
open_questions
```

## Forbidden Cases

```text
1. A knowledge item with no source.
2. A rule that mixes different markets without boundaries.
3. A rule that mixes tick, order book, trade, and K-line assumptions without boundaries.
4. A time-sensitive item without accessed_at.
5. A project-private case marked project_binding = none before sanitization.
6. Two directly conflicting items both marked approved without resolution.
```
