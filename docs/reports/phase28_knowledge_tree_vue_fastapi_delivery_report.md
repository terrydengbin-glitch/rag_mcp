# Phase 28 验收报告：知识树阅读 UI Vue3 与 FastAPI 落地

## 结论

Phase 28 已完成。

本 Phase 将 Phase 27 的 HTML 原型和用户确认的目标截图体验，落成 Vue3 知识树阅读页面，并补齐 FastAPI 只读契约、运行时方案、后端只读骨架和契约测试。

## 完成任务

| ID | 状态 | 说明 |
| --- | --- | --- |
| CEK-TA-125 | done | 创建 Phase 28 任务卡并登记索引 |
| CEK-TA-126 | done | 定义 KnowledgeTree FastAPI 只读接口契约 |
| CEK-TA-127 | done | 明确 FastAPI 服务位置、依赖和 resolver 路径策略 |
| CEK-TA-128 | done | 将 HTML 原型迁移到 Vue3 `KnowledgeTreeView` 信息架构 |
| CEK-TA-129 | done | 增加 Vue3 KnowledgeTree API adapter 和 fixture fallback |
| CEK-TA-130 | done | 增加知识点搜索、分页、排序、页大小和虚拟列表预留 |
| CEK-TA-131 | done | 实现右侧审计摘要、候选跳转、SearchLab 跳转、复制 canonical_node_id |
| CEK-TA-132 | done | 增加 FastAPI 契约测试、Vue3 build 和 Playwright 验收 |
| CEK-TA-133 | done | 生成本验收报告 |

## 主要交付物

```text
docs/tasks/phase28_knowledge_tree_vue_fastapi_delivery.md
docs/contracts/knowledge_tree_reading_api_contract.md
docs/contracts/knowledge_tree_fastapi_runtime_plan.md
docs/reports/phase28_knowledge_tree_vue_fastapi_delivery_report.md
ui/src/views/KnowledgeTreeView.vue
ui/src/styles.css
ui/src/services/knowledgeTreeApi.ts
ui/src/stores/auditStore.ts
ui/tests/e2e/audit-workbench.spec.ts
codex-expert-kit/api/requirements.txt
codex-expert-kit/api/codex_expert_kit_api/
codex-expert-kit/api/tests/test_knowledge_tree_api_contract.py
```

## Vue3 实现

已实现：

```text
1. 最左侧工作台主导航保持不变。
2. 知识树页顶部增加搜索、覆盖状态、冲突状态、时效过滤。
3. 页面左侧改为 L1/L2/L3 目录树。
4. L3 默认收起，选择 L2 后按当前范围展开。
5. 页面中间展示当前节点说明和知识点网格。
6. 桌面端知识点网格一行 5 个。
7. 支持范围内搜索、状态过滤、冲突过滤、时效过滤、排序、页大小、分页。
8. 知识点详情显示在 Open Gaps 和使用边界之前。
9. 右侧审计摘要展示正式知识、候选、来源、缺口、冲突、时效。
10. 右侧动作支持查看候选、带入 SearchLab、复制 canonical_node_id。
11. API 不可用时显示 fixture fallback 状态。
```

## FastAPI 实现

已实现只读 API 骨架：

```text
GET /api/health
GET /api/knowledge-tree/roots
GET /api/knowledge-tree/nodes/{node_id}
GET /api/knowledge-tree/nodes/{node_id}/children
GET /api/knowledge-tree/nodes/{node_id}/knowledge
GET /api/knowledge-items/{knowledge_id}
GET /api/knowledge-tree/nodes/{node_id}/audit-summary
```

运行时边界：

```text
1. API 目录为 codex-expert-kit/api/。
2. Python import 包为 codex_expert_kit_api。
3. 默认端口策略为 127.0.0.1:8787。
4. 默认数据源为 codex-expert-kit/rag/indexes/knowledge_items.json。
5. 路径读取通过 codex-expert-kit/core/path_resolver.py。
6. 不暴露 POST/PUT/PATCH/DELETE 写接口。
7. 不审批、不回灌、不替代 MCP。
```

## 测试结果

已执行：

```text
python -m pytest codex-expert-kit\api\tests
结果：10 passed

npm run build
结果：通过

npm run test:e2e
结果：16 passed
```

Playwright 覆盖：

```text
1. 候选审计页、知识树页、SearchLab 页桌面和移动端渲染。
2. 知识树候选跳转到 IngestionReview。
3. 知识树三层浏览和 breadcrumb 返回。
4. 13 个 L2 分区对齐。
5. legacy node_id 查询兼容。
6. 知识详情在 Open Gaps 之前。
7. 桌面端知识点网格 5 列。
8. 移动端无横向溢出。
```

FastAPI 契约测试覆盖：

```text
1. /api/health 返回 read_only=true。
2. /api/knowledge-tree/roots 返回 3 个 L1 主枝。
3. children 默认不展开 L3。
4. include_l3=true 可返回 L3。
5. page_size 超限返回 INVALID_QUERY。
6. 知识列表支持分页。
7. 知识详情包含 sources 和适用边界。
8. 未知 node_id 返回 NODE_NOT_FOUND。
9. 未知 knowledge_id 返回 ITEM_NOT_FOUND。
10. 扫描 routes，确认无写接口。
```

## 上下游对齐

上游：

```text
Phase 26 3 级知识树 UI
Phase 27 HTML 阅读原型
Phase 28 API contract/runtime plan
codex-expert-kit/rag/indexes/knowledge_items.json
ui/src/data/mockData.ts
ui/src/data/phase23Candidates.ts
```

下游：

```text
1. Vue3 后续可从 fixture fallback 切到真实 FastAPI adapter。
2. SearchLab 继续通过 canonical_node_id 接收查询范围。
3. IngestionReview 继续通过 tree_node_id 接收候选范围。
4. 外部项目仍通过 MCP 调用知识库。
5. 后续可扩展真实知识树节点索引和更完整的 API mapper。
```

## 遗留边界

```text
1. FastAPI 当前是只读骨架，节点树内置 3 主枝/13 分区基础结构。
2. API 已读取正式 knowledge_items.json，但知识树节点数据后续应从正式知识树索引生成。
3. Vue3 已有 API healthcheck 和 fallback，尚未把知识列表完全切换为 API 返回数据。
4. 不新增数据库。
5. 不改变 MCP tool 权限。
6. 不自动把 candidate/draft 转为 approved。
```

## 回滚方案

```text
1. Vue3 若 API 不可用，会自动保留 fixture fallback。
2. 删除或停用 codex-expert-kit/api/ 不影响 MCP。
3. KnowledgeTreeView 可继续使用 mockData 和 phase23Candidates 离线审计。
4. 若 API 端口冲突，使用 CEK_TA_API_PORT 改端口，不杀其他进程。
```
