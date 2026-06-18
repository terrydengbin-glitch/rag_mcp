# CEK-TA Seed Runtime Validation Report

## Report Identity

```yaml
report_id: cek_ta_seed_runtime_validation_20260608
phase: Phase 19
tested_at: 2026-06-08
created_by: codex
status: approved
```

## Scope

```text
验证对象：Phase 17 首批 10 条 accepted seed 知识
MCP tool：search_expert_knowledge
Vue3 view：SearchLab.vue
存储：codex-expert-kit/rag/knowledge/**/*.json
索引：codex-expert-kit/rag/indexes/*.json
```

## Runtime Inventory

```yaml
seed_item_count: 10
mcp_query_case_count: 10
blocking_case_count: 6
searchlab_case_count: 3
pytest_case_count: 14
```

## MCP Seed Query Result

```yaml
hit_rate: 1.0
source_return_rate: 1.0
boundary_return_rate: 1.0
review_status_pass_rate: 1.0
conflict_status_pass_rate: 1.0
unsafe_default_guidance_rate: 0.0
```

说明：

```text
当前 MCP runtime 使用轻量 lexical scoring，不代表最终向量检索排序质量。
为了验证 10 条 seed 都能被 runtime 命中，seed smoke 查询使用 top_k=10。
排序优化应作为后续检索质量任务单独处理。
```

## Blocking Regression Result

| Blocking Case | Result |
| --- | --- |
| approved but unsourced | pass |
| confirmed conflict | pass |
| deprecated | pass |
| draft | pass |
| rejected | pass |
| project_binding mismatch | pass |

```yaml
blocking_pass_rate: 1.0
```

## SearchLab Result

SearchLab 已展示 3 条 seed 查询样例：

```text
seed_runtime_002_ohlc_same_bar
seed_runtime_004_kill_switch
seed_runtime_009_unsourced_block
```

展示字段包含：

```text
query
task_type
filters
matches[].item_id
matches[].title
matches[].tree_path
matches[].review_status
matches[].conflict_status
matches[].recommended_next_action
warnings
```

## Commands Run

```text
pytest codex-expert-kit/mcp/tests
npm --prefix ui run build
```

结果：

```yaml
pytest: 14 passed
vue_build: pass
```

## Code Changes Verified

```text
codex-expert-kit/mcp/common.py
codex-expert-kit/mcp/tests/test_seed_runtime_validation.py
codex-expert-kit/mcp/tests/test_seed_runtime_blocking.py
codex-expert-kit/mcp/tests/codex_expert_kit_mcp_import.py
ui/src/data/mockData.ts
```

## Failed Cases

```json
[]
```

## Open Gaps

```json
[
  {
    "gap_id": "runtime_gap_001",
    "severity": "medium",
    "area": "ranking",
    "description": "MCP 当前为轻量 lexical scoring，部分查询需要 top_k=10 才能覆盖所有 seed。",
    "recommended_action": "后续在 RAG 数据层增加更稳定的 lexical/metadata/rerank 混合检索。"
  },
  {
    "gap_id": "runtime_gap_002",
    "severity": "medium",
    "area": "canonical_filter",
    "description": "MCP 当前默认 filter 尚未完全支持 canonical_node_id。",
    "recommended_action": "后续按 Phase 18 集成计划增加 canonical_node_id 只读 filter。"
  },
  {
    "gap_id": "runtime_gap_003",
    "severity": "low",
    "area": "searchlab_runtime",
    "description": "SearchLab 当前仍使用本地 mock fixture，不直接调用 MCP server。",
    "recommended_action": "后续增加本地 fixture loader 或只读 API adapter。"
  }
]
```

## Runtime Boundary

```text
1. 未新增 MCP 写入权限。
2. 未新增知识审批工具。
3. 未接入外部 RAGFlow 或向量数据库。
4. 未采集实时行情、K线或订单流数据。
5. 未执行交易、未读取账户、未读取密钥。
```

## Recommended Actions

```json
[
  {
    "action_id": "runtime_next_001",
    "priority": "P0",
    "action_type": "retrieval_ranking",
    "target": "codex-expert-kit/mcp/search_expert_knowledge.py",
    "reason": "提高 seed 查询 top1/top3 命中率。",
    "done_when": "10 条 seed 查询 top_k=3 命中率达到 0.8 以上。"
  },
  {
    "action_id": "runtime_next_002",
    "priority": "P1",
    "action_type": "canonical_filter",
    "target": "codex-expert-kit/mcp/common.py",
    "reason": "兑现 Phase 18 的 canonical_node_id 兼容计划。",
    "done_when": "canonical_node_id 查询与 v1 tree_node_id 查询一致。"
  },
  {
    "action_id": "runtime_next_003",
    "priority": "P1",
    "action_type": "searchlab_runtime_adapter",
    "target": "ui/src/views/SearchLab.vue",
    "reason": "让审计界面从 mock 展示升级为可复现实验输入输出。",
    "done_when": "SearchLab 可加载 seed fixture 或本地 MCP 输出 JSON。"
  }
]
```

## DoD Checklist

```text
1. MCP seed 查询测试存在并通过。pass
2. MCP 阻断回归测试存在并通过。pass
3. SearchLab seed 用例存在。pass
4. Vue3 build 通过。pass
5. 运行时验证报告存在。pass
6. 不改变 MCP 权限。pass
7. UTF-8 中文无乱码。pass
```
