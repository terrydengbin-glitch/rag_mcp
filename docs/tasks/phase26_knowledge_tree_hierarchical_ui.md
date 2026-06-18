# Phase 26: 知识树 3 级目录 UI

## Phase 目标

把现有知识树平铺表格升级为固定 3 级目录浏览 UI，让同一个专业板块下的内容更容易归类、检索和审计。

3 级结构定义：

```text
Level 1: 主枝 / 专业大域
例如：交易工程、回测工程、模拟盘与回放、实盘执行、风险管理、RAG 工程、MCP 工程

Level 2: 分区 / 能力板块
例如：KB_04_BACKTEST、KB_05_REPLAY_SIMULATION、KB_07_RISK_MANAGEMENT、KB_10_RAG_ENGINEERING

Level 3: 专题 / 可沉淀知识叶子
例如：回测偏差、数据泄漏、过拟合、OHLC 同根 TP/SL、fill model、滑点延迟、日亏损闸门
```

本 Phase 先把知识树 UI 的上下游、3 级契约、组件边界和验收标准对齐，再执行实现。第一版不引入后端、不引入数据库、不开放浏览器写入知识库，也不改变 MCP 权限或知识状态。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-114 | P0 | done | 对齐知识树 3 级 UI 上下游、契约和任务卡 | `docs/tasks/phase26_knowledge_tree_hierarchical_ui.md`、`docs/index_tasks.md`、`docs/tasks/README.md` |
| CEK-TA-115 | P0 | done | 建立知识树 3 级 view model | `ui/src/stores/auditStore.ts`、`ui/src/types.ts` |
| CEK-TA-116 | P0 | done | 重构 KnowledgeTreeView 为 3 级目录浏览界面 | `ui/src/views/KnowledgeTreeView.vue`、必要组件 |
| CEK-TA-117 | P1 | done | 增加 Level 3 专题详情、知识条目、候选和缺口联动 | `ui/src/views/KnowledgeTreeView.vue`、`ui/src/components/` |
| CEK-TA-118 | P1 | done | 增加 Playwright 3 级浏览实机验收 | `ui/tests/e2e/audit-workbench.spec.ts`、`docs/reports/phase26_knowledge_tree_hierarchical_ui_report.md` |

## 上游输入

```text
1. codex-expert-kit/rag/knowledge_tree_v2.md
2. codex-expert-kit/rag/knowledge_tree_node_v2_schema.md
3. codex-expert-kit/rag/knowledge_tree_aliases.md
4. codex-expert-kit/rag/kb_partitions_v2.md
5. codex-expert-kit/rag/indexes/knowledge_items.json
6. ui/src/types.ts
7. ui/src/stores/auditStore.ts
8. ui/src/views/KnowledgeTreeView.vue
9. ui/src/data/mockData.ts
10. ui/src/data/phase23Candidates.ts
11. docs/tasks/phase15_vue3_audit_workbench_upgrade.md
12. docs/tasks/phase24_vue3_candidate_audit_workbench_v2.md
13. docs/tasks/phase25_vue3_playwright_visual_acceptance.md
```

## 下游输出

```text
1. 用户能从 Level 1 主枝进入 Level 2 分区。
2. 用户能从 Level 2 分区进入 Level 3 专题。
3. 用户能在 Level 3 专题下查看正式知识、draft、候选、来源、冲突和缺口。
4. 用户能通过面包屑回到任意上级。
5. 用户能从节点候选入口跳转到 /ingestion?tree_node_id=...
6. SearchLab 后续可消费当前 3 级选择作为检索上下文。
7. MCP/Search 后续可按 canonical_node_id、kb_partition、topic 做过滤。
8. 专业知识采集流水线后续可根据 Level 3 缺口生成 ResearchIngestionTask。
9. 外部项目接入时可按“主枝 -> 分区 -> 专题”定位 CEK-TA 覆盖范围。
```

## 上下游链条对齐

### 上游事实

```text
knowledge_tree_v2.md 定义 canonical_node_id、parent、children、level、summary、kb_partition、risk_level。
knowledge_tree_node_v2_schema.md 定义节点治理字段和兼容边界。
kb_partitions_v2.md 定义 13 个正式知识分区，是 Level 2 的主要来源。
ui/src/types.ts 当前 KnowledgeTreeNode 已有 node_id、parent_id、path、level、status、counts 和 gaps。
auditStore 当前提供 knowledgeTreeNodes、findTreeNode、getCandidateCoverageForNode、candidateMatchesTreeNodeId。
KnowledgeTreeView 当前是平铺 table，支持候选覆盖跳转，但不支持固定 3 级浏览。
Phase 25 已提供 Playwright 实机验收框架。
```

### 下游消费方

```text
Vue3 KnowledgeTreeView 消费 3 级目录 view model。
IngestionReview 消费 tree_node_id query 继续展示候选过滤结果。
SearchLab 后续可消费 Level 1/2/3 当前选择生成检索测试上下文。
MCP/Search 后续可消费 canonical_node_id、kb_partition、topic 过滤契约。
其他项目接入时可用 3 级目录判断 CEK-TA 覆盖范围。
知识采集 Phase 后续可根据 Level 3 空节点和 open_gaps 生成 ResearchIngestionTask。
```

### 影响边界

```text
本 Phase 允许改变 KnowledgeTreeView 内部信息架构。
本 Phase 不改变全局导航结构。
本 Phase 不改变知识树源文件 schema。
本 Phase 不改变 MCP 默认检索策略。
本 Phase 不把 draft/candidate 展示为 approved 指导。
本 Phase 不强制 knowledge_tree_v2.md 只能有 3 层，UI 只把展示归一到 3 级。
```

## 输入契约

### KnowledgeTreeNode 输入

第一版使用现有前端 `KnowledgeTreeNode`，并通过 `node_id`、`parent_id`、`level` 构建 3 级关系。若上游节点实际层级超过 3 级，UI 归并到 Level 3 专题下展示，不继续下钻。

```yaml
node_id: string
parent_id: string | null
path: string
title: string
domain: string
subdomain: string
level: 1 | 2 | 3 | number
summary: string
coverage_status: empty | partial | covered | overgrown
review_status: draft | reviewed | approved | needs_review | deprecated
freshness_status: stable | time_sensitive | stale | deprecated
conflict_status: none | potential | confirmed | resolved | unchecked
approved_item_count: number
reviewed_item_count: number
source_count: number
open_gaps: string[]
related_nodes: string[]
```

### 3 级 ViewModel 输入

实现时需要在 store 中形成以下派生结构：

```yaml
selected_level1_id: string | null
selected_level2_id: string | null
selected_level3_id: string | null
level1_nodes: KnowledgeTreeNode[]
level2_nodes: KnowledgeTreeNode[]
level3_nodes: KnowledgeTreeNode[]
current_scope:
  level: 1 | 2 | 3
  node_id: string
  title: string
  path: string
ancestor_chain: KnowledgeTreeNode[]
scope_summary:
  node_count: number
  approved_item_count: number
  reviewed_item_count: number
  candidate_count: number
  draft_count: number
  source_count: number
  open_gap_count: number
  conflict_count: number
```

### Level 归一规则

```text
1. parent_id 为 null 的业务主节点进入 Level 1。
2. kb_partition 或 13 分区节点进入 Level 2。
3. 具体可沉淀知识主题进入 Level 3。
4. 如果原始节点 level > 3，UI 不继续增加 Level 4，而是归并为对应 Level 3 专题的关联内容。
5. 如果节点缺少 parent_id，优先用 path/canonical path 推导，推导失败时进入“未归类”审计桶。
```

## 输出契约

### UI 行为

```text
1. 默认进入 /knowledge-tree 时展示 Level 1 主枝。
2. 点击 Level 1 后展示该主枝下的 Level 2 分区，并展示主枝聚合统计。
3. 点击 Level 2 后展示该分区下的 Level 3 专题，并展示分区聚合统计。
4. 点击 Level 3 后展示专题详情、知识条目、候选、缺口、来源和冲突。
5. 面包屑展示 Level 1 -> Level 2 -> Level 3，可点击返回任意上级。
6. 当前范围有候选时，保留跳转 /ingestion?tree_node_id=<node_id>。
7. 空节点必须展示 open_gaps，不展示为“已有专业知识”。
8. draft/candidate 只作为审计对象展示，不作为默认指导展示。
9. 旧平铺表格保留为“全量列表”辅助区，便于审计扫描。
```

### URL 状态

推荐使用 3 级 query 参数保留选中目录：

```text
/knowledge-tree?l1=trading_engineering
/knowledge-tree?l1=trading_engineering&l2=KB_04_BACKTEST
/knowledge-tree?l1=trading_engineering&l2=KB_04_BACKTEST&l3=backtest_bias
```

兼容旧入口：

```text
/knowledge-tree?node_id=kt.backtest.bias
```

URL 契约：

```text
1. l1/l2/l3 不存在时回退到默认 Level 1 列表。
2. l1/l2/l3 找不到时展示错误/空状态，不抛异常白屏。
3. node_id 存在时优先解析到对应 3 级位置，并同步 UI 选中状态。
4. 点击目录时更新 query，便于分享和刷新恢复。
```

## 边界范围

范围内：

```text
1. KnowledgeTreeView 从平铺表格升级为 3 级目录浏览。
2. 增加 Level 1 主枝、Level 2 分区、Level 3 专题和面包屑。
3. 增加范围聚合统计和候选覆盖联动。
4. 增加 empty/loading/error 状态。
5. 保留旧全量表格作为辅助审计视图。
6. 增加 Playwright 桌面/移动端验收。
```

范围外：

```text
1. 不新增数据库。
2. 不新增后端服务。
3. 不开放浏览器写入知识库。
4. 不改变 MCP tool 权限。
5. 不改变知识状态流。
6. 不把候选或 draft 标记为 approved。
7. 不采集行情、K 线、订单簿或交易原始数据。
8. 不改变全局导航，除非后续开发者确认。
9. 不在本 Phase 重构 knowledge_tree_v2.md 的全部知识内容。
```

## 涉及组件

```text
ui/src/types.ts
ui/src/stores/auditStore.ts
ui/src/views/KnowledgeTreeView.vue
ui/src/components/KnowledgeTreeBreadcrumb.vue
ui/src/components/KnowledgeTreeLevelColumn.vue
ui/src/components/KnowledgeTreeTopicDetail.vue
ui/src/components/KnowledgeTreeCoveragePanel.vue
ui/src/styles.css
ui/tests/e2e/audit-workbench.spec.ts
```

组件名为建议命名，最终实现可在不改变 3 级信息架构的前提下按代码风格调整。

## 涉及数据结构

```text
KnowledgeTreeNode
KnowledgeTreeLevel
KnowledgeTreeThreeLevelViewModel
KnowledgeTreeScopeSummary
CandidateCoverageSummary
KnowledgeItem
IngestionCandidate
```

## 涉及数据库/存储

不涉及数据库。第一版继续使用前端本地数据和静态 fixture：

```text
ui/src/data/mockData.ts
ui/src/data/phase23Candidates.ts
codex-expert-kit/rag/indexes/knowledge_items.json
```

后续如要接真实文件索引、MCP browse tree runtime 或在线审计写入，需要单独任务卡确认。

## 实施步骤

```text
1. 优化 Phase 26 任务卡，把目标收敛为固定 3 级知识树 UI。
2. 更新 docs/index_tasks.md 和 docs/tasks/README.md。
3. 在 types.ts 定义 KnowledgeTreeLevel / KnowledgeTreeThreeLevelViewModel / KnowledgeTreeScopeSummary 类型。
4. 在 auditStore 增加 getLevel1Nodes、getLevel2Nodes、getLevel3Nodes、resolveTreeSelection、getTreeScopeSummary。
5. 重构 KnowledgeTreeView：主视图展示 Level 1 / Level 2 / Level 3 三段式目录。
6. 增加面包屑和 l1/l2/l3 URL query，同时兼容 node_id。
7. 增加 Level 3 专题详情、知识条目、候选、缺口、来源和冲突展示。
8. 保留旧全量表格作为辅助审计视图。
9. 补充响应式布局，移动端不能重叠或横向溢出。
10. 更新 Playwright：测试点击 Level 1、Level 2、Level 3、返回上级、候选跳转。
11. 生成 Phase 26 验收报告并更新任务状态。
```

## Definition of Done

```text
1. Phase 26 已登记到 docs/index_tasks.md。
2. docs/tasks/README.md 已登记 Phase 26。
3. 本任务卡包含 3 级上下游、契约、边界、DoD 和测试。
4. KnowledgeTreeView 支持 Level 1 -> Level 2 -> Level 3 点击浏览。
5. 面包屑可返回上级目录。
6. 当前范围详情能展示覆盖、审计、来源、冲突、候选和缺口。
7. 候选跳转到 /ingestion?tree_node_id=... 可用。
8. 空节点不会被误展示为已有专业知识。
9. 旧 node_id 跳转入口不失效。
10. npm run build 通过。
11. npm run test:e2e 通过或报告明确失败原因。
12. 中文文档保持 UTF-8。
```

## 测试与验收

```text
npm run build
npm run test:e2e
```

Playwright 必须覆盖：

```text
1. /knowledge-tree 默认展示 Level 1 主枝。
2. 点击 Level 1 后展示 Level 2 分区。
3. 点击 Level 2 后展示 Level 3 专题。
4. 点击 Level 3 后当前专题详情更新。
5. 面包屑点击可返回 Level 1 或 Level 2。
6. /knowledge-tree?node_id=... 仍能定位到对应 3 级位置。
7. 候选覆盖链接跳转到 /ingestion?tree_node_id=...
8. 桌面和移动端无空白、无横向溢出、关键容器非 0 尺寸。
```

## 风险与回滚

风险：

```text
1. 当前 mockData 和 knowledge_tree_v2.md 的节点 ID 层级可能不完全一致。
2. 13 分区与 UI Level 2 的映射可能存在别名，需要兼容 knowledge_tree_aliases.md。
3. 原始树如果超过 3 层，归并到 Level 3 时可能损失细粒度展示。
4. 只用 path startsWith 判断父子覆盖可能误伤 alias，需要优先使用 parent_id。
5. 用户可能误把空节点当成可用知识，需要明确展示 coverage_status。
```

回滚：

```text
1. 保留旧表格视图作为 fallback。
2. 如果 3 级 view model 有误，退回现有 KnowledgeTreeView 平铺表格。
3. 不删除原始 knowledgeTreeNodes 数据。
4. 不改动知识库 JSON 和 MCP runtime。
```

## 需要开发者确认的问题

```text
1. 3 级结构是否固定为“主枝 -> KB 分区 -> 专题”？当前按你的要求默认采用。
2. 是否保留旧表格作为“全量列表”辅助区？当前建议保留。
3. URL 是否使用 /knowledge-tree?l1=...&l2=...&l3=... 固化选中目录？当前建议使用，并兼容 node_id。
4. 如果原始节点超过 3 层，是否允许归并到 Level 3 专题详情中？当前建议允许。
```

## 状态更新要求

完成任一子任务后必须更新：

```text
1. docs/index_tasks.md
2. docs/tasks/README.md
3. 本任务卡任务列表状态
4. 如新增报告，更新 docs/index_tasks.md 文档入口
```
