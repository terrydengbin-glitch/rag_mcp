# Phase 15: Vue3 知识审计工作台升级任务卡

## Phase 目标

把现有 Vue3 mock 审计界面升级为围绕知识树、采集任务、检索测试、外部项目接入和知识倒灌的专业审计工作台，使用户能够运营知识库质量，而不是只查看静态列表。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-059 | P0 | done | 增加知识树视图 | `ui/src/views/KnowledgeTreeView.vue` |
| CEK-TA-060 | P1 | done | 增加候选知识审计与检索测试台 | `ui/src/views/IngestionReview.vue`、`ui/src/views/SearchLab.vue` |
| CEK-TA-061 | P1 | done | 增加外部项目接入审计视图 | `ui/src/views/ProjectIntegrationAudit.vue` |

## 上游输入

```text
ui/src/App.vue
ui/src/router.ts
ui/src/stores/auditStore.ts
codex-expert-kit/rag/knowledge_tree_schema.md
codex-expert-kit/rag/search_result_contract.md
codex-expert-kit/rag/ingestion_candidate_schema.md
codex-expert-kit/templates/project_adapter.md
```

## 下游输出

```text
知识树运营
候选知识人工审计
检索质量人工测试
外部项目接入检查
知识质量评测数据
```

## 输入契约

Vue store 必须能提供：

```text
knowledge_tree_nodes
knowledge_items
ingestion_candidates
search_test_cases
project_adapters
contributions
loading_state
empty_state
error_state
```

## 输出契约

页面必须展示：

```text
节点覆盖率
节点审计状态
知识条目引用
候选知识状态
冲突提示
检索命中结果
外部项目接入缺口
```

## 边界范围

范围内：

```text
Vue3 路由和视图升级
本地 mock 或文件 adapter 数据展示
知识树浏览
候选知识审计界面
检索测试台
外部项目接入审计
```

范围外：

```text
不做营销页
不直接修改 approved 知识
不接入真实数据库
不绕过 MCP/API 契约直接写入核心知识
不改变整体信息架构，除非开发者确认
```

## 涉及组件

```text
ui/src/router.ts
ui/src/App.vue
ui/src/stores/auditStore.ts
ui/src/data/mockData.ts
ui/src/views/
ui/src/components/
```

## 涉及数据结构

```text
KnowledgeTreeNode
IngestionCandidate
SearchResult
ProjectAdapterStatus
AuditAction
```

## 涉及数据库/存储

第一阶段仍使用前端 mock 数据或只读 adapter。接入真实 MCP/API 前必须对齐 Phase 14 输出契约。

## 实施步骤

1. 增加知识树数据类型和 mock 数据。
2. 增加 `KnowledgeTreeView.vue`。
3. 增加候选知识审计页。
4. 增加检索测试台。
5. 增加外部项目接入审计页。
6. 更新路由与导航。
7. 运行 Vue build 和基础页面检查。

## Definition of Done

```text
新增页面可访问
知识树能显示层级
候选知识能显示来源、范围、冲突、状态
检索测试台能展示 query 和结构化结果
外部项目审计能显示 adapter 缺口
loading/empty/error 状态存在
npm run build 通过
UTF-8 中文无乱码
```

## 测试与验收

```text
npm run build
npm audit --audit-level=moderate
检查新增路由返回 200
检查桌面与移动端布局不重叠
检查中文显示无乱码
```

## 风险与回滚

风险：

```text
页面过多导致导航复杂
mock 数据与后续 MCP 契约不一致
知识树节点层级显示拥挤
```

回滚：

```text
新增页面保持独立路由
不删除已有页面
如新视图不可用，可从导航隐藏
```

## 需要开发者确认的问题

```text
是否允许调整 Vue3 信息架构
是否优先接 MCP 真实数据还是继续 mock
是否需要在页面中提供审计写操作
```

## 状态更新要求

完成后更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase15_vue3_audit_workbench_upgrade.md
```

## 完成记录

```text
completed_at: 2026-06-08
status: done
```

已完成：

```text
1. 增加知识树数据类型和 mock 数据。
2. 增加 KnowledgeTreeView.vue，展示节点层级、覆盖率、审计、时效、冲突、来源和缺口。
3. 增加 IngestionReview.vue，展示候选知识来源、范围、冲突、状态和决策。
4. 增加 SearchLab.vue，展示检索 query、filters、命中结果、warning 和 recommended_next_action。
5. 增加 ProjectIntegrationAudit.vue，展示外部项目 adapter、healthcheck、缺失字段、权限边界和倒灌入口。
6. 更新 router.ts 和 App.vue 导航。
7. 扩展 mockData、auditStore、types。
```

边界说明：

```text
1. 本阶段继续使用本地 mock 数据，不接入真实数据库。
2. 页面只读，不直接修改 approved 知识。
3. 不绕过 Phase 14 MCP/API 契约。
4. 没有改变整体信息架构，只追加独立路由和导航入口。
```

测试：

```text
1. npm run build 通过。
2. npm audit --audit-level=moderate 通过，0 vulnerabilities。
3. /knowledge-tree 返回 200。
4. /ingestion 返回 200。
5. /search-lab 返回 200。
6. /projects 返回 200。
7. 使用 Get-Content -Encoding UTF8 检查中文显示。
```
