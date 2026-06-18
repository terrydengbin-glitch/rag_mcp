# Phase 28: 知识树阅读 UI Vue3 与 FastAPI 落地

## Phase 目标

把 Phase 27 已对齐的 HTML 原型、用户截图目标和任务文档，落成真实可运行的 Vue3 知识树阅读页面，并补齐 FastAPI 只读数据服务契约。

本 Phase 的核心不是新增知识内容，而是把“人类可读、可审核、可检索、可扩展到上千知识点”的知识树页面接到稳定的数据入口上，让后续 MCP、SearchLab、候选审计、知识回灌和外部项目接入都能复用同一套节点与知识条目契约。

目标页面结构：

```text
最左侧：CEK-TA 审计工作台主导航
顶部：知识树范围搜索、覆盖状态、冲突状态、候选状态、时效过滤
页面左侧：3 级知识树目录，默认展示 L1/L2，L3 默认收起，L1/L2 可点击收起/展开
页面中间：当前节点说明、范围内知识点 5 列紧凑网格、知识点详情、Open Gaps、使用边界
页面右侧：审计摘要、下一步动作、人工审核提醒
移动端：目录 / 内容 / 审计分区可切换，不出现横向溢出
```

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-125 | P0 | done | 创建 Phase 28 任务卡并对齐 HTML、截图、文档、Vue3、FastAPI 落地范围 | `docs/tasks/phase28_knowledge_tree_vue_fastapi_delivery.md`、`docs/index_tasks.md`、`docs/tasks/README.md` |
| CEK-TA-126 | P0 | done | 定义 KnowledgeTree FastAPI 只读接口契约 | `docs/contracts/knowledge_tree_reading_api_contract.md` |
| CEK-TA-127 | P0 | done | 明确 FastAPI 服务位置、依赖和 resolver 路径策略 | `docs/contracts/knowledge_tree_fastapi_runtime_plan.md`、`codex-expert-kit/api/`、`codex-expert-kit/core/path_resolver.py` |
| CEK-TA-128 | P0 | done | 将 HTML 原型迁移到 Vue3 `KnowledgeTreeView` 信息架构 | `ui/src/views/KnowledgeTreeView.vue`、`ui/src/styles.css`、`ui/tests/e2e/audit-workbench.spec.ts` |
| CEK-TA-129 | P1 | done | 为 Vue3 增加 KnowledgeTree 数据 adapter，支持 FastAPI 与 fixture fallback | `ui/src/services/knowledgeTreeApi.ts`、`ui/src/stores/auditStore.ts`、`ui/src/views/KnowledgeTreeView.vue` |
| CEK-TA-130 | P1 | done | 增加上千知识点场景的搜索、分页、排序、页大小和虚拟列表预留 | `ui/src/views/KnowledgeTreeView.vue`、`ui/src/styles.css`、`ui/tests/e2e/audit-workbench.spec.ts` |
| CEK-TA-131 | P1 | done | 实现右侧审计摘要、候选跳转、SearchLab 跳转、复制 canonical_node_id | `ui/src/views/KnowledgeTreeView.vue`、`ui/tests/e2e/audit-workbench.spec.ts` |
| CEK-TA-132 | P1 | done | 增加 FastAPI 契约测试、Vue3 build 和 Playwright 实机验收 | `codex-expert-kit/api/tests/`、`ui/tests/e2e/audit-workbench.spec.ts` |
| CEK-TA-133 | P1 | done | 生成 Phase 28 验收报告 | `docs/reports/phase28_knowledge_tree_vue_fastapi_delivery_report.md` |

## 上游输入

```text
1. docs/prototypes/knowledge_tree_reading_ui_prototype.html
2. 用户在对话中确认的目标截图：全局左导航、顶部过滤、页面左树、中间 5 列知识点网格、右侧审计摘要
3. docs/tasks/phase27_knowledge_tree_reading_ui.md
4. docs/tasks/phase26_knowledge_tree_hierarchical_ui.md
5. docs/reports/phase26_knowledge_tree_hierarchical_ui_report.md
6. docs/Vue3知识审计界面需求.md
7. codex-expert-kit/rag/kb_partitions_v2.md
8. codex-expert-kit/rag/indexes/knowledge_items.json
9. codex-expert-kit/core/path_resolver.py
10. ui/src/views/KnowledgeTreeView.vue
11. ui/src/stores/auditStore.ts
12. ui/src/types.ts
13. ui/src/data/mockData.ts
14. ui/src/data/phase23Candidates.ts
15. docs/searchlab_mcp_runtime_contract.md
16. codex-expert-kit/mcp/search_expert_knowledge.py
```

## 下游输出

```text
1. Vue3 知识树页面使用同一套 3 级知识树 view model，不再只靠临时展示结构。
2. FastAPI 只读服务为 Vue3 提供知识树节点、知识点列表、知识点详情、审计摘要和健康检查。
3. SearchLab 可以继续通过 tree_node_id / canonical_node_id 定位当前范围。
4. IngestionReview 可以继续通过 tree_node_id 查看候选知识，不改变候选状态流。
5. 外部项目仍然通过 MCP 读取专业知识；FastAPI 只服务 CEK-TA 审计 UI，不替代 MCP。
6. 知识回灌仍然进入 contributions/proposed，不允许通过知识树页面直接写入正式知识。
```

## 输入契约

### KnowledgeTreeNode

```text
id: string
canonical_node_id: string
parent_id: string | null
level: 1 | 2 | 3
title: string
subtitle: string
summary: string
keywords: string[]
children_count: number
knowledge_count: number
candidate_count: number
open_gap_count: number
coverage_status: none | partial | reviewed
review_status: draft | candidate | reviewed | approved | rejected | gap
freshness_status: fresh | aging | stale | unknown
conflict_status: none | potential | conflict
aliases: string[]
sort_order: number
```

### KnowledgeItemCard

```text
id: string
title: string
tree_node_id: string
canonical_node_id: string
status: draft | candidate | reviewed | approved | rejected | gap
source_count: number
conflict_status: none | potential | conflict
freshness_status: fresh | aging | stale | unknown
summary: string
updated_at: string | null
```

### KnowledgeItemDetail

```text
id: string
title: string
summary: string
content: string
tree_node_id: string
canonical_node_id: string
applicable_scope: string
not_applicable_scope: string
sources: SourceRef[]
conflict_handling: string
status: string
review_notes: string[]
```

### AuditSummary

```text
node_id: string
approved_count: number
candidate_count: number
source_count: number
open_gap_count: number
conflict_count: number
stale_count: number
next_actions: AuditAction[]
manual_review_hints: string[]
```

## FastAPI 只读接口契约

FastAPI 服务只做 UI 数据读取和审计视图聚合，不写知识、不审批、不回灌、不替代 MCP。

```text
GET /api/health
GET /api/knowledge-tree/roots
GET /api/knowledge-tree/nodes/{node_id}
GET /api/knowledge-tree/nodes/{node_id}/children?depth=1
GET /api/knowledge-tree/nodes/{node_id}/knowledge?query=&status=&conflict_status=&freshness_status=&sort=&page=&page_size=
GET /api/knowledge-items/{knowledge_id}
GET /api/knowledge-tree/nodes/{node_id}/audit-summary
```

错误结构：

```text
error_code: string
message: string
details: object
request_id: string
```

硬性要求：

```text
1. 所有仓库路径必须通过 codex-expert-kit/core/path_resolver.py 或显式环境变量解析。
2. 不允许硬编码 E:\collector\rag。
3. 默认读取 codex-expert-kit/rag/indexes/knowledge_items.json。
4. 允许通过 CEK_TA_KNOWLEDGE_ITEMS_PATH 覆盖知识索引路径。
5. FastAPI 返回必须包含 source/citation/confidence/review_status 可审计字段。
6. 不允许暴露写入、审批、删除、交易、实盘、订单相关接口。
```

## Vue3 组件契约

```text
KnowledgeTreeView
职责：知识树阅读、范围内知识点浏览、知识详情查看、审计摘要查看。

输入：
- route query: tree_node_id, canonical_node_id, item_id, query, status, conflict_status, freshness_status
- store: knowledge tree nodes, knowledge item page, selected item detail, audit summary

输出事件：
- select-node(node_id)
- select-item(item_id)
- open-ingestion-review(tree_node_id)
- open-searchlab(canonical_node_id, query)
- copy-canonical-node-id(canonical_node_id)

状态：
- loading
- empty
- error
- degraded fixture fallback
- api healthy
- api unavailable
```

## 边界范围

范围内：

```text
1. 创建 Phase 28 任务卡和索引。
2. 定义 FastAPI 只读接口契约。
3. 对齐 HTML 原型、用户截图目标和 Vue3 信息架构。
4. 优化知识树页面的人类阅读体验。
5. 支持 L1/L2/L3 展开收起、L3 默认收起。
6. 支持上千知识点的分页/虚拟列表预留。
7. 支持右侧审计摘要和下游跳转。
8. 使用 resolver 处理路径。
```

范围外：

```text
1. 不新增数据库，除非开发者再次确认。
2. 不改变 MCP tool 权限。
3. 不通过 FastAPI 写入知识、审批知识或执行回灌。
4. 不采集行情/K线/交易原始数据。
5. 不直接操作实盘、订单或账户。
6. 不改变知识生命周期：proposed -> sanitized -> sourced -> classified -> conflict_checked -> reviewed -> accepted。
7. 不把候选知识自动升级为 approved。
```

## 涉及组件

```text
docs/prototypes/knowledge_tree_reading_ui_prototype.html
ui/src/views/KnowledgeTreeView.vue
ui/src/stores/auditStore.ts
ui/src/types.ts
ui/src/styles.css
ui/src/data/mockData.ts
ui/src/data/phase23Candidates.ts
ui/tests/e2e/audit-workbench.spec.ts
codex-expert-kit/core/path_resolver.py
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/mcp/search_expert_knowledge.py
```

## 涉及存储

```text
1. 当前默认文件化数据层：codex-expert-kit/rag/indexes/knowledge_items.json。
2. 当前 Vue3 fixture：ui/src/data/mockData.ts、ui/src/data/phase23Candidates.ts。
3. 本 Phase 不新增数据库。
4. 若后续需要 SQLite/Postgres/向量库，必须另开 Phase 并由开发者确认。
```

## 实施步骤

```text
1. 创建 Phase 28 任务卡并更新索引。
2. 把 FastAPI 只读接口契约拆成正式 contract 文档。
3. 决定 FastAPI 服务目录：api/ 或 codex-expert-kit/api/。
4. 实现 resolver 驱动的数据读取服务。
5. 为 Vue3 增加 API adapter 和 fixture fallback。
6. 将 HTML 原型迁移到 KnowledgeTreeView。
7. 增加 5 列知识点网格、分页/页大小/排序/过滤。
8. 增加知识点详情、Open Gaps、使用边界、右侧审计摘要。
9. 增加 Playwright 桌面/移动端截图与跳转验证。
10. 生成 Phase 28 验收报告。
```

## Definition of Done

```text
1. Phase 28 已登记到 docs/index_tasks.md。
2. docs/tasks/README.md 已登记 Phase 28。
3. Phase 28 任务卡存在，且包含上下游、契约、边界、DoD、测试。
4. FastAPI 只读接口契约明确，不包含写入/审批/交易能力。
5. 路径 resolver 要求写入任务卡。
6. Vue3 组件输入、输出、状态契约明确。
7. 后续实现完成时，Vue3 build 通过。
8. 后续实现完成时，Playwright 覆盖知识树桌面和移动端。
9. 后续实现完成时，FastAPI contract tests 通过或说明未执行原因。
10. 中文文档保持 UTF-8。
```

## 测试与验收

文档阶段：

```text
1. 检查任务卡文件存在。
2. 检查 docs/index_tasks.md 包含 Phase 28。
3. 检查 docs/tasks/README.md 包含 Phase 28。
4. 检查任务卡包含 FastAPI 只读契约、Vue3 契约、resolver 边界。
```

实现阶段：

```text
1. npm run build
2. npm run test:e2e
3. FastAPI contract tests
4. API healthcheck
5. 桌面端截图：全局左导航、顶部过滤、页面左树、5 列知识点、右侧审计摘要无重叠。
6. 移动端截图：目录 / 内容 / 审计可切换，无横向溢出。
7. 点击 L1/L2/L3、知识点、候选跳转、SearchLab 跳转、复制 canonical_node_id 可用。
```

## 风险与回滚

```text
1. FastAPI 是新的后端运行面；若依赖或目录未确认，只先保留 contract，不落代码。
2. Vue3 API adapter 必须保留 fixture fallback，避免后端未启动时页面完全不可用。
3. 若 5 列网格在窄屏可读性下降，桌面保持 5 列，平板/移动端自动降列。
4. 若真实知识数据字段不足，先通过 mapper 补默认值，不修改正式知识 schema。
5. 若 API 与 MCP 语义冲突，以 MCP 只读检索和知识 governance 规则为准。
```

## 需要开发者确认的问题

```text
1. FastAPI 服务目录已确定为 `codex-expert-kit/api/`。
2. 后续实现阶段是否允许新增 FastAPI、uvicorn、pytest、httpx 依赖？
3. Vue3 已确定先 healthcheck，API 可用则使用 FastAPI adapter，不可用则 fixture fallback。
4. 知识树页面应保留当前 mock fixture 作为离线审计模式。
```

## 状态更新要求

```text
1. 完成 CEK-TA-126 后更新本任务卡、docs/index_tasks.md、docs/tasks/README.md。
2. 完成 Vue3 或 FastAPI 实现后必须生成 Phase 28 验收报告。
3. 未通过测试不得把 CEK-TA-128 至 CEK-TA-133 标记为 done。
```
