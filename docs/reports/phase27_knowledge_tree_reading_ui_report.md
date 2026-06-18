# Phase 27 知识树阅读体验优化验收报告

## 结论

Phase 27 已完成。知识树页面已经从原型迁移到 Vue3，实现左侧可折叠知识树、中间高密度知识点阅读区、下方知识点详情、右侧审计摘要，以及搜索、过滤、分页和虚拟滚动预留。

## 交付物

```text
ui/src/views/KnowledgeTreeView.vue
ui/src/types.ts
ui/src/stores/auditStore.ts
ui/src/styles.css
ui/tests/e2e/audit-workbench.spec.ts
ui/tests/e2e/knowledge-tree-performance.spec.ts
docs/prototypes/knowledge_tree_reading_ui_prototype.html
```

## 上下游对齐

上游输入继续来自正式知识、候选知识、知识树节点和知识树范围索引 fixture。页面不直接读取候选队列作为默认知识，不改变 candidate/reviewed/approved 状态流。

下游输出继续服务 Vue3 审计工作台、候选页跳转、SearchLab 查询跳转和人工知识审计阅读。MCP 权限、回灌入口、后端服务和知识状态流不在本 Phase 修改。

## 契约实现

```text
1. KnowledgeTreeView 使用 KnowledgeTreeThreeLevelViewModel 解析 L1/L2/L3 当前范围。
2. auditStore 提供 node_id -> knowledge_ids / candidate_ids 范围索引读取。
3. 知识点列表只展示正式知识，候选和缺口在下方审计区独立展示。
4. 点击知识点后再读取详情，避免主列表一次铺开完整内容。
5. 旧 tree_node_id 查询通过 alias 与 resolveTreeSelection 兼容。
```

## 阅读体验

```text
1. 左侧树默认展示 L1/L2，L3 只在对应 L2 展开后展示。
2. L1/L2/L3 使用低饱和浅底深字区分，长标题可换行和截断。
3. 中间知识点列表支持搜索、状态过滤、冲突过滤、时效过滤、排序和每页数量。
4. 桌面宽屏知识点摘要卡为 5 列高密度网格。
5. 详情区位于 Open Gaps 和使用边界之前。
6. 右侧审计栏展示正式知识、候选、来源、缺口、冲突和时效统计。
```

## 测试

```text
npm run build
npx playwright test tests/e2e/audit-workbench.spec.ts tests/e2e/knowledge-tree-performance.spec.ts
```

测试结果：

```text
build: pass
Playwright: 26 passed
```

覆盖项：

```text
1. 知识树页面、候选页、SearchLab 页面不白屏。
2. 桌面和移动端无横向溢出。
3. 三层浏览、面包屑返回和 legacy node_id 跳转可用。
4. 当前正式知识树分区数量：Trading Engineering 12、AI Engineering 22、Project Integration 3。
5. Phase 38 RAG Pack 可作为 L3 专题进入。
6. 知识点详情在 Open Gaps 前展示。
7. 桌面知识点摘要卡为 5 列。
8. 大分支首屏 2 秒内可交互，虚拟窗口只渲染当前摘要卡。
9. 短搜索显示中文提示，不触发大范围检索。
```

## 修复记录

```text
1. 补齐 CandidateReviewStatus 的 formalized_reviewed 类型，避免候选 fixture 构建失败。
2. 更新 Playwright 中知识树 L2 数量基线，纳入 Phase 53 新增 Market Conduct、Market Access、Audit Trace、Security Governance 和 Supply Chain Governance。
```

## 风险与回滚

本 Phase 只修改 Vue3 视图、类型契约、样式和 e2e 验收，不改变 MCP 权限、知识状态流、回灌入口和后端服务。若回滚，可恢复 `KnowledgeTreeView.vue`、`types.ts`、`styles.css` 与 e2e 测试到本次前状态。
