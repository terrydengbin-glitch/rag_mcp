# CEK-TA Knowledge Tree Routing Policy

This file defines how RAG, MCP, Vue3, and ingestion workflows route queries and candidates through v1/v2 knowledge tree identifiers.

## Purpose

```text
1. Route queries through professional knowledge paths before broad keyword retrieval.
2. Support v1 tree_node_id and v2 canonical_node_id during migration.
3. Apply status, conflict, freshness, project, and risk filters before returning guidance.
4. Keep candidate/review/deprecated/conflicted knowledge out of default guidance.
```

## Routing Inputs

```json
{
  "query": "string",
  "task_type": "strategy_design | code_review | backtest_review | replay | simulation | live_trading | trade_analysis | llm_training | rag_engineering | mcp | vue_audit_ui | project_integration",
  "filters": {
    "tree_node_id": "kt.backtest.bias",
    "canonical_node_id": "kt.trading_engineering.backtest.bias",
    "tree_path_prefix": "CEK-TA / Trading Engineering / Backtest",
    "canonical_tree_path_prefix": "CEK-TA / Trading Engineering / Backtest",
    "partition_id": "KB_04_BACKTEST",
    "domain": "backtest",
    "subdomain": "bias",
    "review_status": "approved",
    "conflict_status": "none",
    "freshness": "stable",
    "project_binding": "none",
    "include_aliases": true,
    "include_children": false
  },
  "project_context": {
    "project_name": "string | null",
    "market": "crypto | futures | spot | stock | general | null",
    "asset": "BTC | ETH | multi | general | null",
    "timeframe": "tick | 1s | 1m | 3m | 15m | 1h | 4h | 1d | general | null",
    "data_granularity": "tick | trade | order_book | second | kline | account_event | general | null",
    "project_type": "string | null"
  },
  "mode": "default_guidance | audit | browse | ingestion_classification | quality_eval"
}
```

## Routing Flow

```text
User Query
  -> Task Intent Classification
  -> Project Adapter Detection
  -> v1/v2 Alias Resolution
  -> Knowledge Tree Path Routing
  -> Partition Routing
  -> Metadata Filter
  -> Status Filter
  -> Conflict Filter
  -> Freshness Filter
  -> Project Binding Filter
  -> Retrieval
  -> Rerank
  -> Return with Evidence and Warnings
```

## Alias Resolution

Resolution uses `knowledge_tree_aliases.md`.

Order:

```text
1. exact canonical_node_id
2. exact v1 tree_node_id
3. aliases[]
4. v1_path
5. canonical_path
6. no_match
```

Rules:

```text
1. If tree_node_id and canonical_node_id are both supplied, they must resolve to the same alias record.
2. If they conflict, return schema_mismatch or unsupported_filter.
3. split_targets are not included by default.
4. include_children may include split_targets only in audit, browse, or explicit broad search mode.
5. Alias matches must be included in retrieval audit.
```

## Mode Policy

### default_guidance

Allowed:

```text
review_status: approved
conflict_status: none | resolved
freshness: stable | time_sensitive with warning
project_binding: none | active project | sanitized_project_case with caveat
```

Blocked:

```text
draft
candidate
reviewing-only
rejected
deprecated
confirmed unresolved conflict
unsourced
project_binding mismatch
```

### audit

Allowed:

```text
draft
reviewed
candidate
conditional
potential_conflict
deprecated
archived
```

Required display:

```text
review_status
node_status
conflict_status
freshness
migration_status
source_count
warnings
recommended_next_action
```

### browse

Allowed:

```text
empty nodes
partial nodes
candidate nodes
alias nodes
governance nodes
```

Browse mode returns taxonomy and coverage, not professional guidance.

### ingestion_classification

Rules:

```text
1. Prefer canonical_node_id.
2. Also store v1 tree_node_id when alias exists.
3. Candidate must keep classification_confidence.
4. Candidate must not become accepted unless node is resolvable and conflict check is complete.
```

### quality_eval

Rules:

```text
1. Evaluate v1 and canonical route consistency.
2. Track missing aliases.
3. Track ambiguous mappings.
4. Track status and conflict filter failures.
```

## Task Type Routing

| Task Type | Primary v2 Partitions | Primary Path Prefix |
| --- | --- | --- |
| `strategy_design` | `KB_01_QUANT_FOUNDATION`, `KB_03_STRATEGY_ENGINEERING`, `KB_07_RISK_MANAGEMENT` | `kt.trading_engineering.strategy_engineering` |
| `code_review` | all relevant by adapter | exact or inferred |
| `backtest_review` | `KB_04_BACKTEST`, `KB_05_REPLAY_SIMULATION`, `KB_02_DATA_ENGINEERING` | `kt.trading_engineering.backtest` |
| `replay` | `KB_05_REPLAY_SIMULATION`, `KB_02_DATA_ENGINEERING` | `kt.trading_engineering.replay_simulation` |
| `simulation` | `KB_05_REPLAY_SIMULATION`, `KB_07_RISK_MANAGEMENT` | `kt.trading_engineering.replay_simulation` |
| `live_trading` | `KB_06_LIVE_EXECUTION`, `KB_07_RISK_MANAGEMENT` | `kt.trading_engineering.live_execution` |
| `trade_analysis` | `KB_08_TRADE_ANALYSIS`, `KB_03_STRATEGY_ENGINEERING` | `kt.trading_engineering.trade_analysis` |
| `llm_training` | `KB_09_LLM_TRAINING`, `KB_10_RAG_ENGINEERING` | `kt.ai_engineering.llm_training` |
| `rag_engineering` | `KB_10_RAG_ENGINEERING`, `KB_13_KNOWLEDGE_GOVERNANCE` | `kt.ai_engineering.rag_engineering` |
| `mcp` | `KB_11_MCP_ENGINEERING`, `KB_12_PROJECT_INTEGRATION` | `kt.ai_engineering.mcp_engineering` |
| `vue_audit_ui` | `KB_10_RAG_ENGINEERING`, `KB_13_KNOWLEDGE_GOVERNANCE` | `kt.knowledge_governance` |
| `project_integration` | `KB_12_PROJECT_INTEGRATION`, `KB_13_KNOWLEDGE_GOVERNANCE` | `kt.project_integration` |

## Critical Caveat Routing

Trading knowledge that depends on assumptions must ask for or display:

```text
market
asset
timeframe
data_granularity
fee_model
slippage_model
latency_model
order_type
fill_model
project_type
```

Examples:

```text
same-candle TP/SL -> require data_granularity and fill_model
funding/OI interpretation -> require market, contract type, timeframe, source freshness
kill switch -> require runtime mode, exchange adapter, permissions, account scope
RAG source quality -> require source_type, accessed_at, review_status
```

## Output Audit Contract

Every routed retrieval should include:

```json
{
  "routing": {
    "input_tree_node_id": "string | null",
    "resolved_tree_node_id": "string | null",
    "canonical_node_id": "string | null",
    "alias_used": false,
    "migration_status": "v1_only | alias_supported | canonical_ready | downstream_migrated | deprecated_alias | null",
    "partition_id": "string | null",
    "mode": "default_guidance | audit | browse | ingestion_classification | quality_eval",
    "warnings": []
  }
}
```

## Blocking Rules

Do not return default guidance when:

```text
1. Alias resolution fails for a requested node.
2. Requested v1 and canonical IDs disagree.
3. The item has no source evidence.
4. review_status is draft, rejected, or deprecated.
5. conflict_status is confirmed and unresolved.
6. project_binding does not match the active project.
7. high-impact time_sensitive knowledge is stale or lacks accessed_at.
8. a critical-risk node lacks required project context.
```

## Rollback

```text
1. Disable canonical filters.
2. Continue using v1 tree_node_id and tree_path_prefix.
3. Keep alias table as documentation only.
4. Do not change default MCP permissions or Vue3 IA.
```

## Test Checklist

```text
1. v1 tree_node_id resolves to canonical_node_id.
2. canonical_node_id resolves without v1 fallback.
3. conflicting v1/canonical filters are blocked.
4. split_targets are excluded in default_guidance.
5. default_guidance blocks draft, rejected, deprecated, unsourced, and confirmed unresolved conflict.
6. audit mode can show candidate and deprecated nodes with warnings.
7. UTF-8 Chinese display remains readable.
```

