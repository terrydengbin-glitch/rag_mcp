# Phase 26 知识树 3 级目录 UI 验收报告

## 验收结论

Phase 26 已完成。Vue3 知识树从平铺表格升级为固定 3 级目录 UI：

```text
Level 1: 主枝 / 专业大域
Level 2: 分区 / 能力板块
Level 3: 专题 / 可沉淀知识叶子
```

本次改造只调整前端审计展示和本地 view model，不改变 MCP 权限、知识状态流、外部项目接入方式、知识回灌入口或正式知识入库逻辑。

## 上下游对齐

### MCP / SearchLab

```text
1. 保留 tree_node_id 和 canonical_node_id 兼容入口。
2. /knowledge-tree?node_id=... 可解析到 3 级选中状态。
3. 不改变 search_expert_knowledge、browse_knowledge_tree 或 MCP read_only 权限。
4. SearchLab 后续可消费 Level 1/2/3 当前范围作为检索上下文。
```

### 其他项目接入

```text
1. 外部项目仍通过 CEK-TA MCP/RAG 只读查询专业知识。
2. 外部项目仍以 tree_node_id/canonical_node_id 定位知识范围。
3. 本 Phase 不改变 Project Adapter、healthcheck 或接入配置。
```

### 知识回灌

```text
1. 回灌仍走 contributions/proposed。
2. Vue3 知识树只展示回灌和候选的审计入口，不允许浏览器直接写 approved 知识。
3. 其他项目贡献知识仍必须经过 proposed -> sanitized -> sourced -> classified -> conflict_checked -> reviewed -> accepted。
```

### 人工审核

```text
1. Level 3 专题详情显示候选覆盖。
2. 候选入口继续跳转 /ingestion?tree_node_id=...
3. IngestionReview 继续承担候选知识人工审核。
4. 正式 draft 转换仍走 CEK-TA-102 交接，不在知识树页面直接入库。
```

## 交付物

```text
ui/src/types.ts
ui/src/stores/auditStore.ts
ui/src/views/KnowledgeTreeView.vue
ui/src/styles.css
ui/tests/e2e/audit-workbench.spec.ts
docs/tasks/phase26_knowledge_tree_hierarchical_ui.md
docs/reports/phase26_knowledge_tree_hierarchical_ui_report.md
```

## 已完成任务

```text
CEK-TA-115 建立知识树 3 级 view model
CEK-TA-116 重构 KnowledgeTreeView 为 3 级目录浏览界面
CEK-TA-117 增加 Level 3 专题详情、知识条目、候选和缺口联动
CEK-TA-118 增加 Playwright 3 级浏览实机验收
```

## 功能验收

```text
1. /knowledge-tree 默认展示 Level 1 主枝。
2. 点击 Level 1 后展示 Level 2 分区。
3. 点击 Level 2 后展示 Level 3 专题。
4. 点击 Level 3 后展示专题详情、知识条目、候选、缺口、来源、冲突和契约边界。
5. 面包屑可返回 Level 1 或 Level 2。
6. /knowledge-tree?node_id=... 仍能定位到对应 3 级位置。
7. 候选覆盖链接可跳转到 /ingestion?tree_node_id=...
8. 旧全量表格已保留，作为审计扫描和回滚兜底。
```

## 测试结果

```text
npm run build: pass
npm run test:e2e: pass
```

Playwright 结果：

```text
12 passed
desktop-chromium: pass
mobile-chromium: pass
```

覆盖页面：

```text
/ingestion
/knowledge-tree
/search-lab
```

覆盖交互：

```text
1. 候选审计页渲染。
2. 知识树页渲染。
3. SearchLab 页渲染。
4. 知识树候选跳转到 IngestionReview。
5. 知识树 3 级点击浏览。
6. 面包屑返回。
7. legacy node_id query 兼容。
8. 桌面和移动端无横向溢出。
```

## 风险与后续

```text
1. 当前前端仍主要消费 mockData 和 phase23Candidates fixture，后续如接真实 knowledge_tree_v2 文件或 MCP browse runtime，需要单独任务卡。
2. 当前 Level 2 主要按现有节点和 path 推导，后续可以补充 13 分区到 UI 节点的正式映射表。
3. 如果后续要在知识树页面做审核动作，需要新增写入契约、权限边界和审计日志任务，不能直接在本页面扩展。
```
