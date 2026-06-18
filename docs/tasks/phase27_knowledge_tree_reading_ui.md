# Phase 27: 知识树阅读体验优化

## Phase 目标

只针对 Vue3 知识树页面优化人类阅读体验。先产出独立 HTML 原型，验证信息架构，再迁移到 `KnowledgeTreeView.vue`。

目标展示方式：

```text
最左侧：审计工作台主导航，包含总览、知识、知识树、候选、测试、冲突、来源、任务、接入、倒灌、设置
页面左侧：可折叠知识树导航
页面中间：当前节点阅读区
页面右侧：审计摘要 / 来源 / 候选 / 缺口
页面顶部：搜索、过滤、面包屑
移动端：目录 / 内容 / 审计 Tabs
```

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-119 | P0 | done | 创建包含工作台主导航的知识树阅读型 HTML 原型 | `docs/prototypes/knowledge_tree_reading_ui_prototype.html` |
| CEK-TA-120 | P0 | done | 对齐 HTML 原型到 Vue3 组件契约 | `ui/src/views/KnowledgeTreeView.vue`、`ui/src/types.ts`、`ui/src/stores/auditStore.ts` |
| CEK-TA-121 | P0 | done | 实现左侧可折叠知识树导航 | `ui/src/views/KnowledgeTreeView.vue`、必要组件 |
| CEK-TA-122 | P1 | done | 实现节点阅读区和右侧审计栏 | `ui/src/views/KnowledgeTreeView.vue`、必要组件 |
| CEK-TA-123 | P1 | done | 实现树内搜索、状态过滤和移动端 Tabs | `ui/src/views/KnowledgeTreeView.vue`、`ui/src/styles.css` |
| CEK-TA-124 | P1 | done | 增加 Playwright 阅读体验验收 | `ui/tests/e2e/audit-workbench.spec.ts`、`docs/reports/phase27_knowledge_tree_reading_ui_report.md` |

## 上游输入

```text
1. docs/tasks/phase26_knowledge_tree_hierarchical_ui.md
2. docs/reports/phase26_knowledge_tree_hierarchical_ui_report.md
3. ui/src/views/KnowledgeTreeView.vue
4. ui/src/stores/auditStore.ts
5. ui/src/types.ts
6. ui/src/data/mockData.ts
7. codex-expert-kit/rag/kb_partitions_v2.md
```

## 下游输出

```text
1. HTML 原型用于和开发者对齐完整工作台下的知识树阅读体验。
2. Vue3 知识树页面后续按原型迁移。
3. MCP/SearchLab/IngestionReview 仍继续消费 tree_node_id/canonical_node_id。
4. 回灌和人工审核逻辑不在本 Phase 改动。
```

## 输入契约

```text
KnowledgeTreeNode
KnowledgeTreeThreeLevelViewModel
KnowledgeTreeScopeSummary
IngestionCandidate
KnowledgeItem
```

## 输出契约

```text
1. 最左侧必须保留工作台主导航，并突出当前“知识树”页面。
2. 页面左侧树必须展示正式知识树 fixture 中的 3 个主枝和当前全部 Level 2 分区，分区数量随知识树扩展自动对齐。
3. 1 级、2 级、3 级导航必须有不同颜色和等级标签，但颜色必须低饱和、浅底深字，保证长时间阅读和文字可读性。
4. 中间阅读区必须区分主枝页、分区页、专题页。
5. 进入 2 级分区时必须展示其树下所有知识点。
6. 如果 2 级下面有 3 级专题，只在左侧树导航展示 3 级导航；中间区域不再额外展示专题卡片，避免重复。
7. 左侧树默认只展示 L1 和 L2，L3 默认收起；用户可以点击 L1 或 L2 展开/收起子节点。
8. 点击 3 级专题后，中间主区域整页展示该专题下的知识点。
9. 知识点可能达到上千条，知识点列表必须支持范围内搜索、状态过滤、排序、每页数量、分页或虚拟列表预留，禁止一次性铺满页面。
10. 知识点列表必须采用高密度网格样式，桌面宽屏默认一行 5 个知识点，适合上千条知识点扫描。
11. 点击知识点后，页面下方必须展示该知识点的内容、适用范围、不适用范围、来源和冲突处理。
12. 知识点内容必须放在 Open Gaps 和使用边界之前，便于先读知识正文再读审计缺口。
13. 右侧审计栏必须展示 coverage/review/freshness/conflict/source/candidate/open gap。
14. 顶部搜索过滤必须只影响知识树页面。
15. 旧 tree_node_id 跳转入口必须保留。
```

## 边界范围

范围内：

```text
1. HTML 原型。
2. 知识树页面信息架构。
3. 后续 Vue3 组件迁移计划。
```

范围外：

```text
1. 不改 MCP 权限。
2. 不改知识状态流。
3. 不改回灌入口。
4. 不新增数据库。
5. 不新增后端服务。
6. 不采集行情或交易原始数据。
```

## Definition of Done

```text
1. Phase 27 已登记到 docs/index_tasks.md。
2. docs/tasks/README.md 已登记 Phase 27。
3. HTML 原型存在且可直接打开。
4. 原型覆盖工作台主导航、页面左侧树、中间整页知识点列表、知识点详情、右侧审计栏、搜索过滤、移动端 Tabs。
5. 1/2/3 级导航有明显但不刺眼的颜色区分，标签文字清晰可读。
6. 知识点列表必须体现上千条场景下的分页/虚拟列表预留。
7. 中间区域不保留重复的专题卡片。
8. 知识点卡片样式紧凑，桌面宽屏一行 5 个，适合高密度阅读。
9. 左侧树 L3 默认收起，L1/L2 支持展开和收起。
10. 中文文档保持 UTF-8。
```

## 测试与验收

```text
1. Get-Content -Encoding UTF8 可正常读取。
2. HTML 文件存在。
3. 关键 UI 区块可通过文本检索。
```

## 风险与回滚

```text
1. 原型不影响现有 Vue3 页面，可直接删除或废弃。
2. 若原型方向不合适，不进入 CEK-TA-120。
```

## 状态更新要求

```text
1. docs/index_tasks.md
2. docs/tasks/README.md
3. 本任务卡
```
