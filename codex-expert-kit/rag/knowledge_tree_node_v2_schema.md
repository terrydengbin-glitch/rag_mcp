# CEK-TA Knowledge Tree Node v2 Schema

本文件定义知识树 v2 节点治理 schema。v2 节点不是正式知识条目，它是知识路由、审计、冲突治理和跨项目复用的结构化位置。

## Schema Version

```text
schema_name: cek_ta_knowledge_tree_node_v2
schema_version: 2.0.0
encoding: UTF-8
compatible_with: cek_ta_knowledge_tree_node 1.0.0
```

## Required Object

```json
{
  "schema_version": "2.0.0",
  "node_id": "kt.backtest.bias",
  "canonical_node_id": "kt.trading_engineering.backtest.bias",
  "parent_id": "kt.backtest",
  "canonical_parent_id": "kt.trading_engineering.backtest",
  "aliases": [
    "kt.backtest.bias"
  ],
  "path": "CEK-TA / Trading Engineering / Backtest / Bias",
  "canonical_path": "CEK-TA / Trading Engineering / Backtest / Bias",
  "title": "Backtest Bias",
  "domain": "backtest",
  "capability": "backtest",
  "topic": "bias",
  "subdomain": "bias",
  "level": 3,
  "summary": "Knowledge scope and audit purpose for this node.",
  "scope": "Reusable professional knowledge for this node.",
  "out_of_scope": "Project-private facts, investment advice, unsourced claims.",
  "key_concepts": [],
  "expected_knowledge_types": [
    "definition",
    "principle",
    "procedure",
    "checklist",
    "anti_pattern",
    "eval_case"
  ],
  "status": {
    "node_status": "draft | candidate | reviewing | approved | conditional | potential_conflict | conflicted | deprecated | archived",
    "coverage_status": "empty | partial | covered | overgrown",
    "review_status": "draft | reviewed | approved | needs_review | deprecated",
    "freshness_status": "stable | time_sensitive | stale | deprecated",
    "conflict_status": "none | potential | confirmed | resolved | unchecked",
    "migration_status": "v1_only | alias_supported | canonical_ready | downstream_migrated | deprecated_alias",
    "maturity": "v0 | v1 | v2"
  },
  "routing": {
    "kb_partition": "KB_04_BACKTEST",
    "used_for": [
      "backtest_review",
      "code_review",
      "rag_engineering",
      "mcp",
      "vue_audit_ui"
    ],
    "default_retrieval_allowed": false,
    "allowed_review_statuses_for_default": [
      "approved"
    ],
    "allowed_conflict_statuses_for_default": [
      "none",
      "resolved"
    ],
    "include_children_default": false,
    "routing_policy": "exact_node | include_children | audit_only | deprecated_alias"
  },
  "governance": {
    "risk_level": "low | medium | high | critical",
    "project_binding": "none | project_name | sanitized_project_case | governance_only",
    "evidence_required": [],
    "source_policy": {
      "required": true,
      "preferred_source_types": [],
      "minimum_reliability": "medium"
    },
    "conflict_policy": "block_unresolved | show_conflicts | prefer_higher_fidelity_data | prefer_official_source | governance_only",
    "default_policy": "string | null",
    "approval_policy": "node_approval_only | item_approval_required | audit_only"
  },
  "item_mapping": {
    "allowed_domains": [],
    "allowed_subdomains": [],
    "allowed_rule_types": [],
    "required_metadata_fields": [
      "knowledge_id",
      "tree_node_id",
      "source_evidence",
      "review_status",
      "conflict_status"
    ]
  },
  "audit": {
    "minimum_approved_items": 1,
    "minimum_source_count": 1,
    "requires_applicability_boundary": true,
    "requires_conflict_check": true,
    "requires_freshness_check": false,
    "blocking_conditions": []
  },
  "relations": {
    "related_nodes": [],
    "split_targets": [],
    "merged_from": [],
    "supersedes": [],
    "superseded_by": []
  },
  "ownership": {
    "owner": "core | trading | ai | project_integration | governance",
    "approved_by": null,
    "created_at": "YYYY-MM-DD",
    "updated_at": "YYYY-MM-DD",
    "version": "2026-06"
  }
}
```

## Required Fields

```text
schema_version
node_id
canonical_node_id
parent_id
canonical_parent_id
aliases
path
canonical_path
title
domain
capability
topic
subdomain
level
summary
scope
out_of_scope
expected_knowledge_types
status
routing
governance
item_mapping
audit
relations
ownership
```

## ID Contract

```text
node_id: v1 stable identifier. Must remain resolvable.
canonical_node_id: v2 path-inherited identifier. Preferred for new routing.
parent_id: v1 parent identifier.
canonical_parent_id: v2 parent identifier.
aliases: legacy IDs, alternate names, and temporary migration handles.
```

规则：

```text
1. `node_id` 不得复用为不同含义。
2. `canonical_node_id` 必须继承父路径。
3. `canonical_node_id` 不得指向多个不同语义节点。
4. v1 节点拆分时，原 v1 node_id 保持为 alias，primary canonical 指向最安全的上层节点。
5. root `kt` 的 node_id 与 canonical_node_id 均为 `kt`。
```

## Status Contract

`node_status` 用于节点治理，不等于知识条目 `review_status`。

```text
draft: 节点设计未审计。
candidate: 节点来自建议或候选分类，等待确认。
reviewing: 节点正在审计。
approved: 节点可作为稳定导航位置。
conditional: 节点下知识通常依赖明确条件。
potential_conflict: 节点下知识可能存在冲突。
conflicted: 节点治理层面已确认冲突。
deprecated: 节点被新节点替代，只保留兼容。
archived: 历史归档，仅审计参考。
```

`migration_status`：

```text
v1_only: 只有 v1 节点。
alias_supported: alias 表可解析到 canonical。
canonical_ready: v2 节点已定义，可用于审计。
downstream_migrated: RAG/MCP/Vue3 已支持 canonical。
deprecated_alias: v1 alias 仅历史兼容。
```

## Routing Contract

默认指导检索必须满足：

```text
1. default_retrieval_allowed = true。
2. returned item review_status 在 allowed_review_statuses_for_default 内。
3. returned item conflict_status 在 allowed_conflict_statuses_for_default 内。
4. source_evidence 非空。
5. project_binding 与项目上下文兼容。
```

审计检索可以返回：

```text
draft
reviewed
candidate
conditional
potential_conflict
deprecated
```

但必须展示 caveat、conflict_status、freshness_status 和 migration_status。

## Governance Contract

`risk_level` 默认规则：

```text
critical: live execution, exchange permissions, kill switch, leverage, account safety.
high: fill model, risk management, backtest credibility, data leakage, LLM safety.
medium: strategy design, indicators, retrieval policy, project integration.
low: taxonomy, glossary, navigation-only nodes.
```

`project_binding`：

```text
none: 通用知识节点。
project_name: 绑定某个项目，不默认进入 CEK-TA 通用知识。
sanitized_project_case: 脱敏项目案例。
governance_only: 仅治理流程节点，不承载交易规则。
```

## Forbidden Cases

```text
1. canonical_node_id 缺失。
2. v1 node_id 删除或复用。
3. alias 映射到多个 primary canonical 节点。
4. default_retrieval_allowed = true 但未要求 approved/none-or-resolved。
5. high/critical 风险节点无 evidence_required。
6. 项目私有事实标记 project_binding = none。
7. 节点 status = approved 被误解为知识条目 approved。
```

## Mapping To v1

v2 字段回退到 v1：

| v2 Field | v1 Field |
| --- | --- |
| `node_id` | `node_id` |
| `parent_id` | `parent_id` |
| `path` | `path` |
| `title` | `title` |
| `domain` | `domain` |
| `subdomain` | `subdomain` |
| `level` | `level` |
| `summary` | `summary` |
| `status.coverage_status` | `coverage_status` |
| `status.review_status` | `review_status` |
| `status.freshness_status` | `freshness_status` |
| `status.conflict_status` | `conflict_status` |
| `governance.source_policy` | `source_policy` |
| `item_mapping` | `item_mapping` |
| `relations.related_nodes` | `related_nodes` |
| `ownership.created_at` | `created_at` |
| `ownership.updated_at` | `updated_at` |

## Test Checklist

```text
1. 每个 v2 节点有 canonical_node_id。
2. canonical_parent_id 可解析。
3. aliases 不为空，至少包含 v1 node_id，root 除外。
4. 高风险节点有 evidence_required。
5. routing 不允许 draft/conflicted 作为默认指导。
6. governance 不允许项目私有事实污染通用节点。
7. UTF-8 中文可读。
```

