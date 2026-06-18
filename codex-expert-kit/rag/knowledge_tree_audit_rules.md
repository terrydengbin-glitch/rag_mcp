# CEK-TA Knowledge Tree Audit Rules

This file defines how CEK-TA measures node coverage, source quality, conflict risk, freshness risk, and mapping quality for the knowledge tree.

## Purpose

```text
1. Tell users what CEK-TA currently knows.
2. Tell researchers where CEK-TA lacks knowledge.
3. Tell Vue3 which nodes need review.
4. Tell RAG/MCP which nodes are safe for default retrieval.
5. Tell Phase 16 how to compute quality metrics.
```

## Input Contract

Tree audit consumes:

```json
{
  "tree_nodes": ["KnowledgeTreeNode"],
  "knowledge_items": ["KnowledgeItem"],
  "source_profiles": ["SourceProfile"],
  "conflict_audits": ["ConflictAudit"],
  "retrieval_logs": ["RetrievalLog optional"],
  "contribution_records": ["ContributionRecord optional"]
}
```

Required matching fields:

```text
tree_node_id
tree_path
partition_id
domain
subdomain
rule_type
review_status
conflict_status
freshness
source_evidence
source_quality
```

## Coverage Status Rules

```text
empty:
  no reviewed or approved item maps to the node

partial:
  at least one reviewed or approved item maps to the node, but one or more required knowledge types are missing

covered:
  node has the configured minimum approved items, required knowledge types, sources, applicability boundaries, and conflict checks

overgrown:
  node has duplicate or overlapping items that reduce retrieval precision, or more than 30 percent of mapped items conflict or duplicate another item
```

Default thresholds:

```yaml
minimum_approved_items_per_leaf: 1
minimum_reviewed_items_per_leaf: 1
minimum_source_count_per_approved_item: 1
minimum_required_knowledge_type_coverage: 0.6
maximum_duplicate_ratio: 0.3
```

## Required Knowledge Types By Node Class

```yaml
foundation:
  required: [definition, principle]
  recommended: [formula, checklist, anti_pattern]
kline_strategy:
  required: [definition, principle, checklist]
  recommended: [procedure, anti_pattern, eval_case]
market_microstructure:
  required: [definition, principle]
  recommended: [procedure, anti_pattern, eval_case]
backtest:
  required: [definition, checklist, anti_pattern]
  recommended: [procedure, eval_case]
replay_simulation:
  required: [schema, principle, procedure]
  recommended: [checklist, eval_case]
live_execution:
  required: [procedure, checklist]
  recommended: [official_rule_summary, anti_pattern]
trade_analysis:
  required: [taxonomy, definition, procedure]
  recommended: [eval_case, checklist]
llm_training:
  required: [procedure, checklist, eval_case]
  recommended: [schema, anti_pattern]
rag_engineering:
  required: [schema, procedure, checklist]
  recommended: [eval_case, anti_pattern]
project_integration:
  required: [schema, procedure, checklist]
  recommended: [adapter_rule, anti_pattern]
```

## Source Quality Rules

Node source status:

```text
source_empty:
  no mapped item has source evidence

source_weak:
  mapped items use low-reliability or internal-only evidence for default professional claims

source_mixed:
  mapped items have at least one medium/high source but important claims remain weak

source_strong:
  approved items have enough medium/high sources for their scope
```

Preferred source types by domain:

```yaml
quant_trading: [paper, book, official_doc, engineering_article]
kline_strategy: [book, research_report, engineering_article, internal_report]
market_microstructure: [paper, exchange_rule, official_doc, research_report]
backtest: [paper, book, framework_doc, engineering_article]
replay_simulation: [framework_doc, engineering_article, internal_report, official_doc]
live_trading: [official_doc, exchange_rule, engineering_article, internal_report]
trade_analysis: [internal_report, research_report, engineering_article]
llm_training: [official_doc, framework_doc, paper, engineering_article]
rag_engineering: [official_doc, framework_doc, paper, engineering_article]
project_runbooks: [runbook, task_card, code_doc, internal_report]
```

## Conflict Audit Rules

Node conflict status is derived from mapped items:

```text
none:
  no mapped item has potential or confirmed conflict

potential:
  at least one mapped item has conflict_status = potential

confirmed:
  at least one mapped item has conflict_status = confirmed and no resolution

resolved:
  conflicts exist but every conflict has an applicability boundary and resolution

unchecked:
  no mapped item has a conflict audit
```

Blocking conditions:

```text
1. confirmed conflict with missing resolution
2. approved item with unchecked conflict_status
3. general rule whose evidence is market-specific without boundary
4. K-line rule without timeframe boundary
5. fill/execution rule without data granularity and latency/fill assumptions
```

## Freshness Audit Rules

Freshness status:

```text
stable:
  node taxonomy and mapped knowledge are mostly conceptual

time_sensitive:
  node depends on exchange rules, APIs, libraries, model behavior, MCP runtime, data vendor behavior, or live execution requirements

stale:
  time_sensitive node has no current review date or source accessed_at is outside the review window

deprecated:
  node or mapped item is superseded
```

Default review windows:

```yaml
exchange_rule: 30d
official_doc: 90d
framework_doc: 90d
model_api_behavior: 30d
library_behavior: 180d
paper_or_book_concept: 730d
internal_runbook: 180d
```

High-impact use cases that require freshness warning:

```text
live_trading
risk_review
exchange_adapter_review
llm_training_data_policy
mcp_tool_permission
```

## Mapping Quality Rules

A mapped item is valid when:

```text
1. tree_node_id exists and references an existing node.
2. domain and subdomain are compatible with the node mapping.
3. partition_id matches the node primary partition or documented related partition.
4. rule_type is allowed or explicitly justified.
5. source_evidence exists for reviewed or approved items.
```

Mapping status:

```text
mapped:
  item references an existing compatible node

inferred:
  item lacks tree_node_id but can be inferred by domain/subdomain/title

ambiguous:
  item could map to multiple nodes

invalid:
  item references missing node or incompatible domain
```

Invalid mapping must block approved ingestion until fixed.

## Node Audit Output Contract

```json
{
  "node_id": "string",
  "path": "string",
  "coverage_status": "empty | partial | covered | overgrown",
  "review_status": "draft | reviewed | approved | needs_review | deprecated",
  "source_status": "source_empty | source_weak | source_mixed | source_strong",
  "freshness_status": "stable | time_sensitive | stale | deprecated",
  "conflict_status": "none | potential | confirmed | resolved | unchecked",
  "mapping_status": "mapped | inferred | ambiguous | invalid",
  "approved_item_count": 0,
  "reviewed_item_count": 0,
  "draft_item_count": 0,
  "source_count": 0,
  "missing_required_knowledge_types": ["string"],
  "blocking_issues": ["string"],
  "warnings": ["string"],
  "recommended_actions": ["string"]
}
```

## Vue3 Display Rules

Vue3 should highlight:

```text
red: confirmed conflict, invalid mapping, stale high-impact node, or fail status
amber: partial coverage, potential conflict, weak source, or ambiguous mapping
green: covered node with strong or mixed sources and no blocking conflict
gray: empty node intentionally waiting for Phase 12 or Phase 17
```

Vue3 must not present an empty or partial node as approved professional guidance.

## Retrieval Rules

RAG/MCP should:

```text
1. Prefer covered or partial nodes with approved items.
2. Return node path with every result.
3. Warn when a node is empty, stale, conflicted, or source_weak.
4. Use tree_path_prefix for broad browse/search.
5. Avoid using draft-only nodes as default guidance.
```

## Audit Test Checklist

```text
1. Does every node_id have a valid parent_id?
2. Are node_ids unique?
3. Does every top-level trading/AI area map to a partition or documented related partition?
4. Do all reviewed/approved items have source evidence?
5. Do all approved items have conflict_status none or resolved?
6. Do time_sensitive nodes have a review window?
7. Can Vue3 compute coverage, source, conflict, freshness, and mapping status from the contract?
```
