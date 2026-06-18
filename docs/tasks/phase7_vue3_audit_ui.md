# Phase 7 Vue3 知识审计界面任务卡

## Phase 目标

提供 CEK-TA 的 Vue3 知识审计工作台，用于查看、过滤、审计专业知识、来源、冲突、版本、Codex 采集任务和训练数据状态。

首屏必须是工作台，不做介绍页。界面服务于审计、追踪和工程协作，不做营销展示。

## 任务列表

| ID | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- |
| CEK-TA-027 | done | 编写 Vue3 审计界面需求 | `docs/Vue3知识审计界面需求.md` |
| CEK-TA-028 | done | 创建 Vue3 项目骨架 | `ui/` |
| CEK-TA-029 | done | 实现知识列表与过滤 | `ui/src/views/KnowledgeList.vue` |
| CEK-TA-030 | done | 实现知识详情页 | `ui/src/views/KnowledgeDetail.vue` |
| CEK-TA-031 | done | 实现冲突审计页 | `ui/src/views/ConflictReview.vue` |
| CEK-TA-032 | done | 实现 Codex 采集任务记录页 | `ui/src/views/TaskLog.vue` |

## 上游输入

```text
docs/Vue3知识审计界面需求.md
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/source_quality_rules.md
codex-expert-kit/rag/conflict_detection_rules.md
codex-expert-kit/mcp/mcp_server_spec.md
codex-expert-kit/templates/dataset_card.md
codex-expert-kit/templates/eval_report.md
```

## 下游输出

```text
Phase 8 其他项目接入:
  业务项目可通过 UI 查看 CEK-TA 当前知识审计状态和 MCP 接入前置质量。

Phase 9 知识倒灌:
  后续可增加 ContributionQueue 视图，审计倒灌知识。

Codex 审计:
  使用知识列表、详情、冲突、来源和任务记录核对知识是否可用。
```

## 输入契约

当前第一版使用本地 mock 数据，结构对齐：

```text
KnowledgeItem
SourceProfile
ConflictRecord
TaskRecord
DatasetStatus
```

后续接入 MCP/API 时必须保持字段：

```text
knowledge_id
title
domain
subdomain
source
confidence
freshness
review_status
conflict_status
applicability
```

## 输出契约

界面必须提供：

```text
dashboard summary
filtered knowledge rows
knowledge detail
conflict review table
source audit table
task log table
current filter export payload
```

## 边界范围

本 Phase 做：

```text
1. 创建 Vue3 + TypeScript + Vite 项目骨架。
2. 创建 Pinia store 和 Vue Router。
3. 实现 Dashboard、KnowledgeList、KnowledgeDetail、ConflictReview、SourceAudit、TaskLog、Settings。
4. 使用本地 mock 数据展示审计状态。
5. 实现筛选、详情、导出筛选结果。
6. 执行 build 验证并启动本地 dev server。
```

本 Phase 不做：

```text
1. 不引入后端数据库。
2. 不接真实 MCP 服务。
3. 不写入或审批真实知识。
4. 不改变 Vue3 信息架构之外的后端权限。
5. 不处理实盘、账户、密钥。
```

## 涉及组件

```text
ui/package.json
ui/src/main.ts
ui/src/App.vue
ui/src/router.ts
ui/src/stores/auditStore.ts
ui/src/data/mockData.ts
ui/src/views/*
ui/src/components/*
docs/index_tasks.md
docs/tasks/README.md
```

## 涉及数据结构

```text
KnowledgeItem
SourceProfile
ConflictRecord
TaskRecord
AuditFilter
SummaryMetric
```

## 涉及数据库/存储

当前 Phase 不引入数据库。第一版数据为前端 mock。后续接 API/MCP 必须单独定义接口、权限、错误和回滚。

## 实施步骤

```text
1. 创建 Phase 7 任务卡。
2. 创建 Vue3 项目骨架。
3. 定义前端类型和 mock 数据。
4. 实现 store、router、shell、状态 badge。
5. 实现 dashboard、knowledge list、detail、conflict、source、task、settings。
6. 更新任务索引和 README。
7. npm install。
8. npm run build。
9. 启动 dev server 并给出 URL。
```

## Definition of Done

```text
1. Phase 7 任务卡存在。
2. ui/ 项目存在并可 build。
3. 知识列表支持关键词、domain、source_type、freshness、review_status、confidence、conflict 过滤。
4. 知识详情显示规则、适用范围、不适用场景、假设、来源、冲突、版本和审计状态。
5. 冲突审计页显示冲突类型、双方、来源等级、适用范围、版本和消解方式。
6. Codex 任务记录页显示任务 ID、问题、关键词、来源、新增/修改知识、冲突、人工确认和执行时间。
7. 索引状态一致。
8. UTF-8 无乱码。
```

## 测试与验收

```text
1. Test-Path 检查关键文件存在。
2. Select-String 检查关键章节和视图字段。
3. npm run build。
4. 检查 docs/index_tasks.md、docs/tasks/README.md、任务卡状态一致。
5. Get-Content -Encoding UTF8 检查中文文档无乱码。
6. 启动本地 dev server。
```

## 风险与回滚

风险：

```text
1. 第一版 mock 数据不代表真实知识状态。
2. 后续接 MCP/API 时需要处理权限、错误、loading、empty、stale 数据。
3. 审计动作如果变成写操作，必须新增权限和审计日志契约。
```

回滚：

```text
1. 前端文档和代码可通过版本控制回退。
2. 后续接 API 失败时保留 mock 数据作为离线审计演示。
3. 不在本 Phase 写入任何知识，避免数据回滚问题。
```

## 需要开发者确认的问题

当前按既有需求使用 Vue3，不引入数据库、后端框架、真实 MCP 写权限或外部服务，无需确认。

后续如要改变信息架构、接真实 API/MCP 写操作、引入后端或数据库，必须向开发者确认。

## 状态更新要求

完成后必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase7_vue3_audit_ui.md
codex-expert-kit/README.md
```
