# Phase 20: SearchLab MCP 真实运行时与检索质量闭环任务卡

## Phase 目标

把 Phase 19 中已经验证过的文件化 MCP 查询能力，接到 Vue3 SearchLab 的真实运行时验证路径中，并补齐 canonical filter、检索排序质量评估和阻断策略可视化，让审计人员可以在界面中看到“实际查询了什么、命中了什么、为什么命中、来源是否完整、哪些知识被阻断”。

本阶段的目标不是扩大知识库规模，而是把现有 10 条 seed 知识的运行时链路做实，形成后续专业知识批量沉淀前的质量门禁。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-080 | P0 | done | 定义 SearchLab 调用 MCP runtime 的本地契约 | `docs/searchlab_mcp_runtime_contract.md` |
| CEK-TA-081 | P0 | done | 补齐 MCP `canonical_node_id` / alias / tree path 过滤能力 | `codex-expert-kit/mcp/search_expert_knowledge.py`、`codex-expert-kit/mcp/common.py`、`codex-expert-kit/mcp/tests/` |
| CEK-TA-082 | P0 | done | 建立检索排序质量回归集与指标报告 | `codex-expert-kit/rag/eval_sets/runtime_ranking_eval_cases.json`、`docs/reports/runtime_ranking_quality_report.md` |
| CEK-TA-083 | P1 | done | 让 SearchLab 使用真实 runtime fixture/adapter 展示查询结果 | `ui/src/data/`、`ui/src/stores/`、`ui/src/views/SearchLab.vue` |
| CEK-TA-084 | P1 | done | 增加 SearchLab 阻断审计展示与测试 | `ui/src/views/SearchLab.vue`、`ui/src/types.ts`、`ui/src/data/` |
| CEK-TA-085 | P1 | done | 生成 Phase 20 运行时质量验收报告 | `docs/reports/searchlab_mcp_runtime_quality_report.md` |

## 上游输入

```text
docs/tasks/phase19_seed_runtime_validation.md
docs/seed_runtime_validation_plan.md
docs/reports/seed_runtime_validation_report.md
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/knowledge_tree_v2.md
codex-expert-kit/rag/knowledge_tree_aliases.md
codex-expert-kit/rag/tree_routing_policy.md
codex-expert-kit/rag/search_result_contract.md
codex-expert-kit/rag/eval_sets/
codex-expert-kit/mcp/search_expert_knowledge.py
codex-expert-kit/mcp/common.py
codex-expert-kit/mcp/server.py
ui/src/views/SearchLab.vue
ui/src/stores/auditStore.ts
ui/src/data/mockData.ts
ui/src/types.ts
```

## 下游输出

```text
SearchLab 真实 runtime 查询契约
MCP canonical filter 与 alias 兼容能力
检索排序质量回归集
SearchLab 查询、来源、阻断、排名解释展示
运行时质量验收报告
后续 Phase 21 专业知识规模化入库 gate
外部项目接入 smoke test 的可视化入口
```

## 输入契约

### SearchLab Runtime Query

SearchLab 发起的查询必须显式表达：

```json
{
  "request_id": "string",
  "query": "string",
  "task_type": "strategy_design | code_review | backtest_review | replay | simulation | live_trading | trade_analysis | llm_training | rag_engineering | mcp | vue_audit_ui | project_integration",
  "top_k": 5,
  "filters": {
    "domain": "string optional",
    "subdomain": "string optional",
    "partition_id": "string optional",
    "tree_node_id": "string optional",
    "canonical_node_id": "string optional",
    "tree_path": "string optional",
    "review_status": "approved optional",
    "conflict_status": "none | resolved optional"
  },
  "include": {
    "sources": true,
    "conflicts": true,
    "blocked": true,
    "ranking_debug": true
  }
}
```

### Runtime Fixture / Adapter

本阶段默认不引入后端服务。SearchLab 可以先通过本地 runtime adapter 或 fixture 消费 MCP 同构响应，但结构必须与 MCP 输出保持一致：

```text
request
response.matches[]
response.blocked[]
response.audit
response.warnings[]
response.errors[]
```

## 输出契约

### MCP Search Result

每条可用于默认指导的命中必须包含：

```text
knowledge_id
title
claim
source_refs
domain
subdomain
partition_id
tree_node_id
canonical_node_id 或可回溯 alias
tree_path
review_status
conflict_status
freshness
confidence
applicable_scope
not_applicable_scope
recommended_next_action
why_matched.score
why_matched.reasons
```

### Blocked Result

每条被阻断的知识必须说明：

```text
knowledge_id
title
blocked_reason
review_status
conflict_status
freshness
has_source_refs
recommended_fix
```

### SearchLab Display

SearchLab 至少需要展示：

```text
查询条件
命中列表
来源状态
适用/不适用边界
冲突状态
freshness
排名分数或排名原因
阻断列表
阻断原因
runtime audit summary
```

## 边界范围

范围内：

```text
定义 SearchLab -> MCP runtime 查询契约
实现或准备本地只读 runtime adapter/fixture
补齐 MCP canonical_node_id、alias、tree_path 过滤
增加 ranking eval cases，避免 seed 知识只能靠 top_k=10 命中
让 SearchLab 展示真实运行时结构中的命中、来源、边界、阻断原因
生成 Phase 20 运行时质量报告
```

范围外：

```text
不引入数据库
不引入新的后端框架
不改变 MCP tool 权限
不新增写入型 MCP tool
不调用外部 RAGFlow 或向量数据库
不联网采集新知识
不采集行情、K线、订单流或账户数据
不改变 Vue3 主信息架构
不把 mock 数据直接当成真实知识验收结果
```

## 涉及组件

```text
codex-expert-kit/mcp/search_expert_knowledge.py
codex-expert-kit/mcp/common.py
codex-expert-kit/mcp/server.py
codex-expert-kit/mcp/tests/
codex-expert-kit/rag/eval_sets/
codex-expert-kit/rag/knowledge_tree_aliases.md
codex-expert-kit/rag/tree_routing_policy.md
ui/src/views/SearchLab.vue
ui/src/stores/auditStore.ts
ui/src/data/
ui/src/types.ts
docs/reports/
```

## 涉及数据结构

```text
SearchLabRuntimeQuery
SearchLabRuntimeResponse
McpSearchRequest
McpSearchResult
BlockedKnowledgeResult
RuntimeRankingEvalCase
RuntimeQualityReport
KnowledgeTreeAlias
```

## 涉及数据库/存储

```text
继续使用文件化知识存储：
codex-expert-kit/rag/knowledge/**/*.json
codex-expert-kit/rag/indexes/*.json
codex-expert-kit/rag/eval_sets/*.json

不引入数据库。
不做迁移。
不新增外部存储。
```

## 实施步骤

1. 编写 `docs/searchlab_mcp_runtime_contract.md`，明确 SearchLab 查询、响应、错误、阻断和 ranking debug 契约。
2. 阅读 MCP 当前搜索实现，补齐 `canonical_node_id`、alias、tree_path 的只读过滤规则。
3. 增加 MCP 单元测试，覆盖 canonical 命中、alias 命中、tree path 命中、项目不匹配阻断、无来源阻断。
4. 建立 `runtime_ranking_eval_cases.json`，至少覆盖 Phase 19 的 10 条 seed 查询。
5. 调整 ranking 评估目标：优先让目标知识进入 top_k=5，并记录不能进入 top_k=5 的原因。
6. 让 SearchLab 消费与 MCP 输出同构的 runtime fixture/adapter，展示命中、来源、边界、阻断和 audit summary。
7. 增加或更新 UI 类型定义，避免 SearchLab 继续依赖无法表达阻断原因的旧 mock 结构。
8. 运行 MCP tests 和 Vue3 build。
9. 生成 `docs/reports/searchlab_mcp_runtime_quality_report.md`。
10. 更新索引、任务卡状态和 README。

## Definition of Done

```text
Phase 20 任务卡存在并已被索引
SearchLab MCP runtime 契约文档存在
MCP 支持 canonical_node_id / alias / tree_path 过滤或明确记录剩余缺口
10 条 seed ranking eval cases 存在
目标知识 top_k=5 命中率有报告
SearchLab 能展示 runtime 查询结果、来源、边界、阻断原因和 audit summary
阻断无来源、冲突、过期、draft/rejected 的测试继续通过
不改变 MCP 权限
不引入数据库、后端框架或外部服务
pytest 通过或记录失败原因
Vue3 build 通过或记录失败原因
中文文档 UTF-8 无乱码
```

## 测试与验收

必须执行或记录原因：

```text
pytest codex-expert-kit/mcp/tests
npm --prefix ui run build
JSON eval fixture 解析检查
SearchLab runtime fixture 渲染检查
UTF-8 中文读取检查
无乱码检查
```

关键断言：

```text
1. canonical_node_id 过滤不会误放其他节点知识。
2. alias 过滤能回溯到 canonical 节点。
3. tree_path 过滤结果必须属于对应路径或其受允许的子路径。
4. 无 source_refs 的知识不得进入默认指导。
5. confirmed conflict / deprecated / draft / rejected 不得进入默认指导。
6. SearchLab 必须能展示至少 1 条 blocked result。
7. SearchLab 命中结果必须展示来源状态。
8. runtime quality report 必须记录 top_k=5 命中率和剩余 ranking gap。
```

## 风险与回滚

风险：

```text
SearchLab 直接调用 MCP server 可能需要后端桥接，超出本阶段默认边界。
当前 MCP 轻量词法排序可能无法稳定达到 top_k=5。
canonical tree path 与历史 tree_node_id / alias 的映射可能存在缺口。
UI 类型扩展可能影响已有 SearchLab mock 展示。
```

回滚：

```text
如真实 MCP 调用需要新后端，先保留同构 runtime fixture，不引入框架。
如 ranking 无法达到 top_k=5，记录 ranking_gap，不降低阻断规则。
如 canonical alias 映射不足，先限制过滤到已映射节点，并在报告中列出缺失节点。
如 UI 构建失败，回滚 SearchLab 类型改动，保留契约与 MCP 测试。
```

## 需要开发者确认的问题

```text
是否允许后续 Phase 引入本地 HTTP bridge，把 Vue3 SearchLab 直接连 MCP runtime？
是否允许把 top_k=5 命中率作为后续新增知识入库的强制质量门槛？
是否需要优先优化排序算法，还是先保证 canonical filter 和阻断展示？
```

当前默认执行假设：

```text
1. Phase 20 先不引入新后端、数据库或外部服务。
2. SearchLab 先使用 MCP 同构 runtime fixture/adapter，后续再决定是否接 HTTP bridge。
3. MCP 权限保持 read-only。
4. 排名优化先用可测试的轻量规则，无法达标则记录到质量报告。
```

## 状态更新要求

完成后更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase20_searchlab_mcp_runtime_quality.md
README.md
```

## 进度记录

```yaml
current_status: done
completed_tasks:
  - CEK-TA-080
  - CEK-TA-081
  - CEK-TA-082
  - CEK-TA-083
  - CEK-TA-084
  - CEK-TA-085
in_progress_tasks: []
remaining_tasks: []
deliverables:
  - docs/searchlab_mcp_runtime_contract.md
  - codex-expert-kit/mcp/common.py
  - codex-expert-kit/mcp/search_expert_knowledge.py
  - codex-expert-kit/mcp/tests/test_phase20_runtime_quality.py
  - codex-expert-kit/rag/eval_sets/runtime_ranking_eval_cases.json
  - docs/reports/runtime_ranking_quality_report.md
  - ui/src/types.ts
  - ui/src/data/runtimeSearchData.ts
  - ui/src/stores/auditStore.ts
  - ui/src/views/SearchLab.vue
  - docs/reports/searchlab_mcp_runtime_quality_report.md
notes:
  - Phase 20 承接 Phase 19 的 ranking、canonical filter 和 SearchLab runtime integration 缺口。
  - 本阶段默认不新增数据库、后端框架、外部服务或 MCP 写权限。
  - pytest codex-expert-kit/mcp/tests: 18 passed.
  - npm --prefix ui run build: pass.
  - top_k=5 seed ranking hit rate: 1.0.
```
