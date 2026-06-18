# CEK-TA Search Result Contract

This file defines the structured response contract for RAG/MCP knowledge retrieval.

The contract is designed for Codex, Knowledge MCP, Vue3 audit views, retrieval tests, and future quality evaluation.

## Contract Version

```text
schema_name: cek_ta_search_result
schema_version: 1.0.0
encoding: UTF-8
```

## Search Request

```json
{
  "request_id": "string",
  "query": "string",
  "task_type": "strategy_design | code_review | backtest_review | replay | simulation | live_trading | trade_analysis | llm_training | rag_engineering | mcp | vue_audit_ui | project_integration",
  "top_k": 5,
  "filters": {
    "tree_node_id": "kt.backtest.bias",
    "tree_path_prefix": "CEK-TA / Trading Engineering / Backtest",
    "partition_id": "KB_04_BACKTEST",
    "domain": "backtest",
    "subdomain": "bias",
    "review_status": "approved",
    "conflict_status": "none",
    "confidence": "high",
    "freshness": "stable",
    "source_type": "book"
  },
  "project_context": {
    "project_name": "string | null",
    "market": "crypto | futures | spot | stock | general | null",
    "asset": "BTC | ETH | multi | general | null",
    "timeframe": "tick | 1s | 1m | 3m | 15m | 1h | 4h | 1d | general | null",
    "data_granularity": "tick | trade | order_book | second | kline | account_event | general | null",
    "project_type": "string | null"
  },
  "include": {
    "sources": true,
    "conflicts": true,
    "deprecated": false,
    "draft": false,
    "reviewed": true,
    "tree_context": true
  }
}
```

## Search Response

```json
{
  "request_id": "string",
  "status": "ok | warning | error",
  "query": "string",
  "matched_items": [
    {
      "item_id": "knowledge_id",
      "title": "string",
      "claim": "single clear rule or knowledge claim",
      "summary": "short retrieval summary",
      "partition_id": "KB_04_BACKTEST",
      "tree_node_id": "kt.backtest.bias",
      "tree_path": "CEK-TA / Trading Engineering / Backtest / Bias",
      "domain": "backtest",
      "subdomain": "bias",
      "rule_type": "definition | principle | procedure | formula | checklist | anti_pattern | adapter_rule | schema | incident | eval_case | taxonomy",
      "applicable_scope": {
        "market": "general",
        "asset": "general",
        "timeframe": "general",
        "data_granularity": "kline",
        "project_type": "general",
        "applies_when": ["string"]
      },
      "not_applicable_scope": ["string"],
      "source_refs": [
        {
          "source_id": "src_001",
          "source_title": "string",
          "source_url": "string | null",
          "source_type": "official_doc | paper | exchange_rule | framework_doc | book | research_report | engineering_article | internal_report | task_card | code_doc | runbook",
          "publisher": "string | null",
          "published_at": "YYYY-MM-DD | null",
          "accessed_at": "YYYY-MM-DD",
          "reliability": "high | medium | low",
          "evidence_summary": "string"
        }
      ],
      "confidence": "high | medium | low",
      "freshness": "stable | time_sensitive | deprecated",
      "review_status": "draft | reviewed | approved | rejected | deprecated",
      "conflict_status": "none | potential | confirmed | resolved | deprecated_by_conflict",
      "conflict_summary": "string | null",
      "why_matched": {
        "match_type": "tree_node | tree_path_prefix | metadata | lexical | semantic | manual",
        "matched_fields": ["query", "tree_node_id", "domain"],
        "score": 0.0,
        "notes": ["string"]
      },
      "warnings": ["string"],
      "recommended_next_action": "use_as_guidance | cite_with_caveat | review_conflict | refresh_source | ask_human | no_default_guidance"
    }
  ],
  "warnings": ["string"],
  "applied_filters": {},
  "audit": {
    "retrieval_policy_version": "1.0.0",
    "storage_layout_version": "1.0.0",
    "result_count": 0,
    "blocked_count": 0,
    "returned_review_statuses": [],
    "returned_conflict_statuses": [],
    "tree_nodes_used": [],
    "source_count": 0
  },
  "errors": []
}
```

## Error Schema

```json
{
  "code": "invalid_input | unsupported_filter | not_found | conflict_blocked | permission_denied | storage_unavailable | schema_mismatch",
  "message": "string",
  "field": "string | null",
  "details": {}
}
```

## Required Return Fields

Every matched item must include:

```text
item_id
title
claim
summary
tree_node_id
tree_path
domain
applicable_scope
not_applicable_scope
source_refs
confidence
freshness
review_status
conflict_status
why_matched
recommended_next_action
```

## Recommended Next Action Rules

```text
use_as_guidance:
  review_status = approved, conflict_status = none or resolved, source_refs present

cite_with_caveat:
  review_status = reviewed, or conflict_status = potential, or freshness = time_sensitive

review_conflict:
  conflict_status = potential or confirmed

refresh_source:
  freshness = time_sensitive and high-impact task depends on it

ask_human:
  live_trading or risk_review with stale/conflicted knowledge

no_default_guidance:
  rejected, deprecated, draft-only, unsourced, or confirmed unresolved conflict
```

## Blocking Rules

Do not return as default guidance when:

```text
1. source_refs is empty.
2. review_status is rejected.
3. review_status is draft and audit mode is false.
4. conflict_status is confirmed without resolution.
5. freshness is deprecated.
6. project_binding does not match the active project.
7. tree_node_id is missing for approved knowledge.
```

## Vue3 Display Mapping

Vue3 can map:

```text
matched_items[].tree_path -> knowledge tree breadcrumb
matched_items[].source_refs -> source drawer
matched_items[].warnings -> warning banner
matched_items[].recommended_next_action -> action badge
audit.tree_nodes_used -> tree filter chip
```

## MCP Compatibility Notes

Phase 3 draft tools may return `results` instead of `matched_items`. Phase 14 should normalize to this contract:

```text
results -> matched_items
knowledge_id -> item_id
source -> source_refs[0]
applicability -> applicable_scope
score -> why_matched.score
```
