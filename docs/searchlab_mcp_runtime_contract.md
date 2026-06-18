# SearchLab MCP Runtime Contract

## 文档目的

本文定义 Phase 20 中 Vue3 SearchLab 与 CEK-TA Knowledge MCP 同构运行时之间的只读查询契约。它用于让审计人员在界面中看到实际检索请求、命中结果、来源、适用边界、排名原因和阻断原因。

本契约不引入新后端、数据库、外部服务或写入型 MCP tool。SearchLab 在 Phase 20 内可以先消费本地 runtime fixture/adapter，但数据结构必须与 MCP `search_expert_knowledge` 返回保持一致。

## 上游

```text
codex-expert-kit/mcp/search_expert_knowledge.py
codex-expert-kit/mcp/common.py
codex-expert-kit/rag/knowledge/**/*.json
codex-expert-kit/rag/knowledge_tree_aliases.md
codex-expert-kit/rag/knowledge_tree_v2.md
codex-expert-kit/rag/eval_sets/runtime_ranking_eval_cases.json
docs/seed_runtime_validation_plan.md
```

## 下游

```text
ui/src/views/SearchLab.vue
ui/src/stores/auditStore.ts
ui/src/data/runtimeSearchData.ts
docs/reports/searchlab_mcp_runtime_quality_report.md
外部项目接入 smoke test
```

## Request Contract

SearchLab runtime query 必须是只读查询：

```json
{
  "request_id": "searchlab_runtime_001",
  "query": "OHLC same bar take profit stop loss fill model",
  "task_type": "backtest_review",
  "top_k": 5,
  "filters": {
    "domain": "backtest",
    "subdomain": "fill_model",
    "partition_id": "KB_04_BACKTEST",
    "tree_node_id": "kt.backtest.bias",
    "tree_path_prefix": "CEK-TA / Trading Engineering / Backtest",
    "canonical_node_id": "kt.trading_engineering.backtest.fill_assumption",
    "canonical_tree_path_prefix": "CEK-TA / Trading Engineering / Backtest",
    "review_status": "approved",
    "conflict_status": "none"
  },
  "project_context": {
    "market": "general",
    "asset": "general",
    "timeframe": "general",
    "data_granularity": "kline",
    "project_type": "general",
    "project_name": "optional_external_project"
  },
  "include": {
    "sources": true,
    "conflicts": true,
    "deprecated": false,
    "draft": false,
    "reviewed": true,
    "blocked": true,
    "ranking_debug": true
  }
}
```

## Supported Filters

```text
tree_node_id
tree_path
tree_path_prefix
canonical_node_id
canonical_tree_path
canonical_tree_path_prefix
partition_id
domain
subdomain
rule_type
review_status
confidence
freshness
conflict_status
source_type
```

## Canonical / Alias Rules

```text
1. 新知识优先写 metadata.canonical_node_id 和 metadata.canonical_tree_path。
2. 历史知识继续保留 metadata.tree_node_id 和 metadata.tree_path。
3. canonical_node_id 过滤必须匹配 metadata.canonical_node_id。
4. 为兼容迁移期，canonical_node_id 过滤也允许匹配 metadata.tree_node_id。
5. tree_node_id 过滤只表示 v1 精确节点，不自动展开 split_targets。
6. canonical_tree_path_prefix 只匹配 metadata.canonical_tree_path 前缀。
7. tree_path_prefix 只匹配 metadata.tree_path 前缀。
8. split_targets 默认只用于审计提示，不作为默认检索放宽条件。
```

## Response Contract

MCP response 必须保持 Phase 14/19 兼容字段：

```json
{
  "request_id": "searchlab_runtime_001",
  "status": "ok",
  "results": [],
  "blocked_results": [],
  "warnings": [],
  "applied_filters": {},
  "audit": {
    "retrieval_policy_version": "0.1.0",
    "result_count": 0,
    "blocked_count": 0,
    "returned_review_statuses": [],
    "returned_conflict_statuses": []
  },
  "errors": []
}
```

### Result Item

每条 `results[]` 必须包含：

```text
knowledge_id
title
claim
partition_id
tree_node_id
tree_path
canonical_node_id
canonical_tree_path
domain
subdomain
source_refs
confidence
freshness
review_status
conflict_status
applicable_scope
not_applicable_scope
recommended_next_action
why_matched.score
why_matched.reasons
warnings
```

### Blocked Item

每条 `blocked_results[]` 必须包含：

```text
knowledge_id
title
blocked_reason
review_status
conflict_status
freshness
has_source_refs
tree_node_id
canonical_node_id
recommended_fix
```

允许的阻断原因：

```text
missing_source_evidence
confirmed_conflict
deprecated
review_status_draft
review_status_rejected
review_status_reviewed_not_included
project_binding_mismatch
filtered_or_not_allowed
```

## SearchLab Display Requirements

SearchLab 至少展示：

```text
request_id
query
task_type
filters
runtime status
result_count
blocked_count
warnings
命中知识标题、ID、tree/canonical path
来源数量和来源状态
review_status / conflict_status / freshness
recommended_next_action
why_matched.score
why_matched.reasons
blocked_reason
recommended_fix
```

## Error Rules

```text
1. query 为空必须返回 invalid_input。
2. top_k 不在 1..20 必须返回 invalid_input。
3. unsupported filter 必须返回 unsupported_filter。
4. requested_permission 包含写入、交易、账户、密钥权限必须返回 permission_denied。
5. SearchLab 不得把 error response 渲染成可用默认指导。
```

## Boundaries

```text
本契约只定义只读检索。
不允许 SearchLab 审批知识。
不允许写入贡献队列。
不允许读取项目密钥、账户、订单或实时行情。
不引入 HTTP bridge；如后续需要，必须单独建 Phase 和任务卡。
```

## Test Requirements

```text
pytest codex-expert-kit/mcp/tests
npm --prefix ui run build
runtime_ranking_eval_cases.json 可解析
SearchLab fixture 至少包含 1 条 blocked_results
UTF-8 中文无乱码
```
