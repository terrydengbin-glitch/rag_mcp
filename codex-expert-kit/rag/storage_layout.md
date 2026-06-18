# CEK-TA RAG Storage Layout

This file defines the file-based MVP storage layout for CEK-TA approved/reviewed knowledge, indexes, examples, and retrieval tests.

It is intentionally database-free. Introducing RAGFlow, a vector database, SQLite, Postgres, or another backend requires a separate task card and developer confirmation.

## Storage Version

```text
schema_name: cek_ta_rag_storage_layout
schema_version: 1.0.0
encoding: UTF-8
root: codex-expert-kit/rag/
```

## Directory Contract

```text
codex-expert-kit/rag/
  knowledge/
    README.md
    KB_01_QUANT_FOUNDATION/
    KB_02_KLINE_STRATEGY/
    KB_03_MARKET_MICROSTRUCTURE/
    KB_04_BACKTEST/
    KB_05_REPLAY_SIMULATION/
    KB_06_LIVE_EXECUTION/
    KB_07_TRADE_ANALYSIS/
    KB_08_LLM_TRAINING/
    KB_09_RAG_ENGINEERING/
    KB_10_PROJECT_RUNBOOKS/
  indexes/
    README.md
    knowledge_index.json
    tree_index.json
    source_index.json
    conflict_index.json
  examples/
    README.md
    sample_knowledge_items.json
    sample_knowledge_index.json
    sample_search_requests.json
    sample_search_results.json
  tests/
    README.md
    retrieval_test_cases.json
```

## Storage Zones

| Zone | Purpose | Retrieval Default |
| --- | --- | --- |
| `knowledge/` | Formal reviewed/approved/deprecated knowledge item files | approved and reviewed only |
| `indexes/` | Generated or hand-maintained local indexes | searchable |
| `examples/` | Sample data for MCP/Vue3/test development | not production truth |
| `tests/` | Retrieval and contract test cases | test only |

## Formal Knowledge Boundary

Allowed formal knowledge sources:

```text
accepted knowledge item
reviewed contribution
approved research candidate
manually approved seed asset
```

Forbidden in `knowledge/`:

```text
unreviewed proposed contribution
unsourced claim
project-private field dictionary
raw order/account data
confirmed unresolved conflict marked as approved
rejected item as normal retrieval candidate
```

## Knowledge File Contract

Recommended path:

```text
knowledge/<partition_id>/<knowledge_id>.json
```

Example:

```text
knowledge/KB_04_BACKTEST/kb_04_backtest.bias.lookahead_boundary.v1.json
```

Each file must follow:

```text
codex-expert-kit/rag/knowledge_item_schema.md
```

Additional tree mapping fields should be present in `metadata`:

```json
{
  "tree_node_id": "kt.backtest.bias",
  "tree_path": "CEK-TA / Trading Engineering / Backtest / Bias",
  "related_nodes": ["kt.backtest.data_quality"]
}
```

## Index Record Contract

`indexes/knowledge_index.json` contains a compact list for search, filtering, and MCP loading.

```json
{
  "index_schema_version": "1.0.0",
  "generated_at": "YYYY-MM-DD",
  "source": "file_mvp",
  "records": [
    {
      "knowledge_id": "string",
      "title": "string",
      "file_path": "codex-expert-kit/rag/knowledge/KB_04_BACKTEST/item.json",
      "partition_id": "KB_04_BACKTEST",
      "tree_node_id": "kt.backtest.bias",
      "tree_path": "CEK-TA / Trading Engineering / Backtest / Bias",
      "domain": "backtest",
      "subdomain": "bias",
      "rule_type": "definition | principle | procedure | formula | checklist | anti_pattern | adapter_rule | schema | incident | eval_case | taxonomy",
      "review_status": "draft | reviewed | approved | rejected | deprecated",
      "conflict_status": "none | potential | confirmed | resolved | deprecated_by_conflict",
      "confidence": "high | medium | low",
      "freshness": "stable | time_sensitive | deprecated",
      "source_count": 1,
      "source_reliability": "high | medium | low",
      "market": "crypto | futures | spot | stock | general",
      "timeframe": "tick | 1s | 1m | 3m | 15m | 1h | 4h | 1d | general",
      "data_granularity": "tick | trade | order_book | second | kline | account_event | general",
      "updated_at": "YYYY-MM-DD",
      "search_terms": ["string"]
    }
  ]
}
```

## Tree Index Contract

`indexes/tree_index.json` maps tree nodes to item IDs.

```json
{
  "index_schema_version": "1.0.0",
  "generated_at": "YYYY-MM-DD",
  "nodes": [
    {
      "node_id": "kt.backtest.bias",
      "path": "CEK-TA / Trading Engineering / Backtest / Bias",
      "partition_id": "KB_04_BACKTEST",
      "coverage_status": "empty | partial | covered | overgrown",
      "review_status": "draft | reviewed | approved | needs_review | deprecated",
      "item_ids": ["knowledge_id"],
      "approved_item_count": 0,
      "reviewed_item_count": 0,
      "conflict_status": "none | potential | confirmed | resolved | unchecked",
      "freshness_status": "stable | time_sensitive | stale | deprecated"
    }
  ]
}
```

## Source Index Contract

`indexes/source_index.json` tracks reusable source profiles:

```json
{
  "index_schema_version": "1.0.0",
  "generated_at": "YYYY-MM-DD",
  "sources": [
    {
      "source_id": "src_001",
      "source_title": "string",
      "source_url": "string | null",
      "source_type": "official_doc | paper | exchange_rule | framework_doc | book | research_report | engineering_article | internal_report | task_card | code_doc | runbook",
      "publisher": "string | null",
      "published_at": "YYYY-MM-DD | null",
      "accessed_at": "YYYY-MM-DD",
      "reliability": "high | medium | low",
      "knowledge_ids": ["string"]
    }
  ]
}
```

## Conflict Index Contract

`indexes/conflict_index.json` tracks conflict audit summaries:

```json
{
  "index_schema_version": "1.0.0",
  "generated_at": "YYYY-MM-DD",
  "conflicts": [
    {
      "candidate_knowledge_id": "string",
      "conflict_status": "none | potential | confirmed | resolved | deprecated_by_conflict",
      "checked_against": ["knowledge_id"],
      "blocking": false,
      "resolution_summary": "string"
    }
  ]
}
```

## Ingestion Gates

Formal indexing must reject:

```text
1. review_status = rejected
2. review_status = draft unless explicit audit mode is requested
3. conflict_status = confirmed without resolution
4. source_evidence is empty
5. tree_node_id is missing for approved items
6. project_binding = project_name unless active project matches
7. contribution status earlier than reviewed unless explicit audit mode is requested
```

## Retrieval Defaults

```yaml
default_review_statuses:
  - approved
optional_review_statuses:
  - reviewed
excluded_review_statuses:
  - rejected
  - draft
  - deprecated
default_conflict_statuses:
  - none
  - resolved
warning_conflict_statuses:
  - potential
excluded_conflict_statuses:
  - confirmed
  - deprecated_by_conflict
```

## MCP Loading Rules

Phase 14 MCP runtime may load:

```text
1. examples/sample_knowledge_items.json for development tests
2. knowledge/**/*.json for formal local retrieval
3. indexes/knowledge_index.json for filtering and preselection
```

MCP must return warnings when using example data.

## Rollback

```text
1. Schema documents remain source of truth.
2. examples/ can be deleted without affecting formal knowledge.
3. indexes/ can be regenerated from knowledge/ files.
4. No database migrations exist in this phase.
```
