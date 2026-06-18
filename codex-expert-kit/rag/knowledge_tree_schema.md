# CEK-TA Knowledge Tree Schema

This file defines the structured contract for CEK-TA knowledge tree nodes.

The knowledge tree is the navigation and audit layer above knowledge items. It does not replace `knowledge_item_schema.md`; it gives every knowledge item a stable professional location.

## Schema Version

```text
schema_name: cek_ta_knowledge_tree_node
schema_version: 1.0.0
encoding: UTF-8
```

## Purpose

```text
1. Organize reusable trading and AI knowledge into a stable tree.
2. Let Vue3 display what CEK-TA knows, lacks, or must review.
3. Let RAG/MCP filter by professional path, not only keyword or domain.
4. Let ingestion tasks classify candidates before review.
5. Let quality evaluation measure coverage and risk by node.
```

## Required Node Object

```json
{
  "schema_version": "1.0.0",
  "node_id": "kt.backtest.bias.lookahead",
  "parent_id": "kt.backtest.bias",
  "path": "Trading Engineering / Backtest / Bias / Lookahead Bias",
  "title": "Lookahead Bias",
  "domain": "backtest",
  "subdomain": "bias",
  "level": 3,
  "summary": "Knowledge scope and audit purpose for this node.",
  "key_concepts": ["lookahead", "future leakage"],
  "expected_knowledge_types": [
    "definition",
    "principle",
    "procedure",
    "checklist",
    "anti_pattern",
    "eval_case"
  ],
  "coverage_status": "empty | partial | covered | overgrown",
  "review_status": "draft | reviewed | approved | needs_review | deprecated",
  "freshness_status": "stable | time_sensitive | stale | deprecated",
  "conflict_status": "none | potential | confirmed | resolved | unchecked",
  "source_policy": {
    "required": true,
    "preferred_source_types": ["paper", "book", "framework_doc", "official_doc"],
    "minimum_reliability": "medium"
  },
  "item_mapping": {
    "partition_id": "KB_04_BACKTEST",
    "allowed_domains": ["backtest"],
    "allowed_subdomains": ["bias"],
    "allowed_rule_types": ["definition", "principle", "procedure", "checklist", "anti_pattern", "eval_case"],
    "required_metadata_fields": [
      "knowledge_id",
      "domain",
      "subdomain",
      "review_status",
      "conflict_status",
      "source_evidence"
    ]
  },
  "audit": {
    "minimum_approved_items": 1,
    "minimum_source_count": 1,
    "requires_applicability_boundary": true,
    "requires_conflict_check": true,
    "requires_freshness_check": false
  },
  "related_nodes": ["kt.backtest.data_quality", "kt.replay_simulation.fill_model"],
  "aliases": ["future data leakage"],
  "owner": "CEK-TA",
  "created_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD"
}
```

## Required Fields

```text
schema_version
node_id
parent_id
path
title
domain
subdomain
level
summary
key_concepts
expected_knowledge_types
coverage_status
review_status
freshness_status
conflict_status
source_policy
item_mapping
audit
related_nodes
aliases
created_at
updated_at
```

## ID Rules

```text
node_id format: kt.<domain_or_area>.<topic>.<subtopic>
root node: kt
top-level node example: kt.trading_engineering
leaf node example: kt.backtest.bias.lookahead
```

Rules:

```text
1. node_id is stable and must not be reused for a different meaning.
2. New nodes are appended; renaming requires aliases and migration notes.
3. parent_id must reference an existing node unless node_id is kt.
4. path must match the parent chain.
5. A node can map to one primary partition and optionally related partitions.
```

## Level Rules

```text
0: root
1: major area
2: domain
3: topic
4: specialized topic
```

Do not create level 5 nodes in the first version unless a Phase task explicitly requires it.

## Coverage Status

```text
empty: no accepted or reviewed knowledge items mapped
partial: at least one reviewed item exists, but required knowledge types are missing
covered: minimum approved items and required knowledge types exist
overgrown: too many overlapping items or duplicates require consolidation
```

## Review Status

```text
draft: node exists but structure is not reviewed
reviewed: node structure is reviewed
approved: node can be used as stable navigation
needs_review: node has stale, conflicting, or unclear mapping
deprecated: node is retained only for history
```

Node approval does not approve the knowledge items under it. Item approval still follows `knowledge_item_schema.md`.

## Freshness Status

```text
stable: taxonomy is unlikely to change quickly
time_sensitive: node depends on exchange/API/framework/model behavior
stale: node requires refresh before high-impact use
deprecated: node is superseded
```

## Conflict Status

```text
none: no known node-level conflict
potential: mapped items may conflict
confirmed: known conflict exists
resolved: conflict is resolved by boundaries
unchecked: not enough mapped items or audit data
```

## Knowledge Item Mapping

Every knowledge item should include or be derivable to:

```text
tree_node_id
tree_path
partition_id
domain
subdomain
rule_type
review_status
conflict_status
source_refs
```

If `tree_node_id` is missing, Phase 13 indexing must infer it from domain, subdomain, title, and tags, then mark the mapping as `needs_review`.

## Vue3 Minimum Display Contract

Vue3 must be able to show:

```text
node_id
path
title
domain
coverage_status
review_status
freshness_status
conflict_status
approved_item_count
reviewed_item_count
source_count
open_gaps
related_nodes
```

## MCP/RAG Minimum Query Contract

MCP tools should support:

```text
tree_node_id
tree_path_prefix
domain
coverage_status
review_status
conflict_status
include_children
```

## Forbidden Cases

```text
1. A node with no parent except the root.
2. A leaf node with no source policy.
3. A node that mixes project-private facts into CEK-TA reusable knowledge.
4. A node that claims coverage when mapped items are not approved or reviewed.
5. A node that hides confirmed conflicts by marking conflict_status = none.
```
