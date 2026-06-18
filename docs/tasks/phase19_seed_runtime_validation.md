# Phase 19: Seed 知识运行时验证任务卡

## Phase 目标

验证 Phase 17 首批 10 条 accepted seed 知识不仅存在于文件和索引中，而且能在 MCP runtime 与 Vue3 SearchLab 查询路径中被正确命中、正确返回来源、正确保留边界，并能阻断无来源、冲突、过期或不允许默认指导的知识。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-075 | P0 | done | 定义 seed 运行时验证计划与查询用例 | `docs/seed_runtime_validation_plan.md` |
| CEK-TA-076 | P0 | done | 增加 MCP seed 知识 runtime 查询测试 | `codex-expert-kit/mcp/tests/test_seed_runtime_validation.py` |
| CEK-TA-077 | P0 | done | 增加阻断回归测试：无来源、冲突、过期、draft/rejected | `codex-expert-kit/mcp/tests/test_seed_runtime_blocking.py` |
| CEK-TA-078 | P1 | done | 对齐 SearchLab seed 查询用例展示 | `ui/src/data/*`、`ui/src/views/SearchLab.vue` |
| CEK-TA-079 | P1 | done | 生成 seed 运行时验证报告 | `docs/reports/seed_runtime_validation_report.md` |

## 上游输入

```text
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/indexes/knowledge_index.json
codex-expert-kit/rag/indexes/source_index.json
codex-expert-kit/rag/indexes/conflict_index.json
codex-expert-kit/rag/search_result_contract.md
codex-expert-kit/rag/tree_routing_policy.md
codex-expert-kit/rag/eval_sets/
codex-expert-kit/mcp/search_expert_knowledge.py
codex-expert-kit/mcp/common.py
codex-expert-kit/mcp/server.py
ui/src/views/SearchLab.vue
docs/reports/seed_knowledge_quality_report.md
```

## 下游输出

```text
MCP runtime 可查询 seed 知识
SearchLab 可审计 seed 查询结果
阻断规则可回归测试
运行时验证报告
后续外部项目接入的 smoke test 基线
```

## 输入契约

### MCP Search Request

每个 seed runtime 查询用例必须包含：

```json
{
  "request_id": "seed_runtime_backtest_same_bar",
  "query": "string",
  "task_type": "strategy_design | code_review | backtest_review | replay | simulation | live_trading | trade_analysis | llm_training | rag_engineering | mcp | vue_audit_ui | project_integration",
  "top_k": 5,
  "filters": {
    "domain": "string optional",
    "partition_id": "string optional",
    "tree_node_id": "string optional",
    "review_status": "approved optional",
    "conflict_status": "none optional"
  },
  "project_context": {
    "market": "general | crypto | futures | spot | stock",
    "asset": "general | BTC | ETH | multi",
    "timeframe": "general | tick | 1m | 1h | 1d",
    "data_granularity": "general | kline | tick | trade | order_book | account_event",
    "project_type": "general | kline_trend_strategy | high_fidelity_simulator | live_binance_futures | trading_llm_assistant"
  },
  "include": {
    "sources": true,
    "conflicts": true,
    "deprecated": false,
    "draft": false,
    "reviewed": true
  }
}
```

### MCP Search Response

每个成功命中的结果必须包含：

```text
knowledge_id
title
claim
partition_id
tree_node_id
tree_path
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
audit.result_count
audit.blocked_count
```

### 阻断用例输入

阻断回归测试必须至少构造：

```text
unsourced approved item
confirmed conflict item
deprecated item
draft item
rejected item
project_binding mismatch item
```

## 输出契约

`docs/reports/seed_runtime_validation_report.md` 必须包含：

```text
report_id
phase
tested_at
seed_item_count
mcp_query_case_count
searchlab_case_count
blocking_case_count
hit_rate
source_return_rate
boundary_return_rate
unsafe_default_guidance_rate
blocking_pass_rate
failed_cases
open_gaps
recommended_actions
runtime_boundary
DoD checklist
```

## 边界范围

范围内：

```text
验证 MCP read-only 查询能命中 Phase 17 seed 知识
验证 source_refs、适用边界、冲突状态、freshness、recommended_next_action 返回
验证 default guidance 阻断无来源、冲突、过期、draft/rejected 知识
让 Vue3 SearchLab 展示 seed 查询用例和结果状态
生成运行时验证报告
```

范围外：

```text
不引入向量数据库
不接入外部 RAGFlow 服务
不改变 MCP tool 权限
不新增知识写入或审批 MCP tool
不改变 Vue3 主信息架构
不采集实时行情、K线或订单流数据
不执行任何交易或读取账户
```

## 涉及组件

```text
codex-expert-kit/mcp/search_expert_knowledge.py
codex-expert-kit/mcp/common.py
codex-expert-kit/mcp/server.py
codex-expert-kit/mcp/tests/
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/indexes/
ui/src/views/SearchLab.vue
ui/src/data/
docs/reports/
```

## 涉及数据结构

```text
KnowledgeItem
SearchRequest
SearchResponse
RuntimeValidationCase
BlockingRegressionCase
SearchLabCase
SeedRuntimeValidationReport
```

## 涉及数据库/存储

```text
只使用 Phase 13 的文件化正式知识存储和索引。
不引入数据库。
不做迁移。
索引可从 knowledge/**/*.json 重建。
```

## 实施步骤

1. 编写 seed runtime 验证计划。
2. 准备 MCP 查询测试数据加载路径，优先直接读取 `knowledge/**/*.json` 或由测试聚合为内存列表。
3. 为 10 条 seed 编写 MCP default_guidance 查询用例。
4. 编写阻断用例，覆盖无来源、confirmed conflict、deprecated、draft、rejected、project mismatch。
5. 运行 pytest，确认 runtime 查询和阻断通过。
6. 对齐 SearchLab mock/fixture 数据，使界面可以看到 seed 查询用例、命中结果、来源和警告。
7. 运行 Vue3 build 或记录无法运行原因。
8. 生成运行时验证报告。
9. 更新索引和任务状态。

## Definition of Done

```text
运行时验证计划存在
MCP seed 查询测试存在
MCP 阻断回归测试存在
10 条 seed 至少有 8 条能通过目标查询命中
命中结果 source_refs 返回率为 100%
命中结果 applicability/not_applicable 返回率为 100%
阻断用例通过率为 100%
SearchLab 有 seed 查询用例展示或明确记录待接入原因
运行时验证报告存在
不改变 MCP 权限
UTF-8 中文无乱码
```

## 测试与验收

必须执行或记录原因：

```text
pytest codex-expert-kit/mcp/tests
SearchLab 相关单元或 build 检查
JSON fixture 解析检查
Get-Content -Encoding UTF8 中文显示检查
无乱码检查
```

关键断言：

```text
1. default_guidance 不返回无来源知识。
2. default_guidance 不返回 confirmed unresolved conflict。
3. default_guidance 不返回 deprecated。
4. default_guidance 不返回 rejected。
5. draft 默认被阻断。
6. source_refs 必须存在。
7. applicable_scope 与 not_applicable_scope 必须存在。
8. live_trading time_sensitive 必须有 warning 或 recommended_next_action。
```

## 风险与回滚

风险：

```text
当前 MCP 只做轻量 lexical scoring，可能无法覆盖最终向量检索质量。
SearchLab 当前使用 mock data，可能尚未直接连 MCP runtime。
v2 canonical_node_id 当前可能未被 MCP filter 原生支持。
```

回滚：

```text
测试失败不降级 seed 知识，先记录 runtime gap。
如阻断规则失败，优先修复 common.py filter_items，不改动知识内容。
SearchLab 如未能接 runtime，保留 mock fixture 并在报告中标记 integration_gap。
不改变已完成 Phase 17 的 accepted 状态，除非发现来源、冲突或边界本身错误。
```

## 需要开发者确认的问题

```text
是否允许在 Phase 19 内补充 MCP 对 canonical_node_id 的可选 filter 支持？
是否允许 SearchLab 从 mock data 升级为读取本地 seed fixture？
是否需要把 MCP runtime 验证作为后续每次知识入库的强制 gate？
```

当前默认执行假设：

```text
1. 不改变 MCP 权限。
2. 允许增加只读 filter 和测试 fixture。
3. SearchLab 先用本地 fixture 展示 seed 查询用例，不引入后端服务。
```

## 状态更新要求

完成后更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase19_seed_runtime_validation.md
README.md
```

## 进度记录

```yaml
current_status: done
completed_tasks:
  - CEK-TA-075
  - CEK-TA-076
  - CEK-TA-077
  - CEK-TA-078
  - CEK-TA-079
in_progress_tasks: []
remaining_tasks: []
deliverables:
  - docs/seed_runtime_validation_plan.md
  - codex-expert-kit/mcp/tests/test_seed_runtime_validation.py
  - codex-expert-kit/mcp/tests/test_seed_runtime_blocking.py
  - codex-expert-kit/mcp/tests/codex_expert_kit_mcp_import.py
  - ui/src/data/mockData.ts
  - docs/reports/seed_runtime_validation_report.md
notes:
  - Phase 19 已验证运行时读取、检索、返回来源和阻断行为。
  - 本阶段不新增数据库、外部服务或 MCP 写入权限。
  - pytest codex-expert-kit/mcp/tests: 14 passed.
  - npm --prefix ui run build: pass.
```
