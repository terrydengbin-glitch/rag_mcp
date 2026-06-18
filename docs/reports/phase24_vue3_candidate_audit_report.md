# Phase 24 Vue3 Candidate Audit Report

## 报告定位

本报告用于验收 Phase 24 Vue3 候选知识审计工作台 v2，确认前端已经可以承接 Phase 23 首批候选知识的查看、来源审计、冲突审计、知识树覆盖联动、转换预览和 `CEK-TA-102` 交接。

本报告不是知识入库批准单。候选知识仍不能被视为 approved 知识，也不能进入 MCP 默认指导；后续必须由 `CEK-TA-102` 转换为正式知识 `draft`，再走正式审计、索引重建和运行时验证。

## 上下游

上游输入：

```text
1. codex-expert-kit/rag/candidates/**/*.json
2. codex-expert-kit/rag/ingestion_candidate_schema.md
3. codex-expert-kit/rag/knowledge_item_schema.md
4. docs/reports/phase23_candidate_quality_report.md
5. docs/reports/phase24_candidate_audit_handoff.md
6. codex-expert-kit/rag/knowledge_tree_v2.md
7. codex-expert-kit/rag/indexes/knowledge_items.json
```

下游输出：

```text
1. ui/src/data/phase23Candidates.ts
2. ui/src/views/IngestionReview.vue
3. ui/src/components/CandidateSourcePanel.vue
4. ui/src/components/CandidateConflictPanel.vue
5. ui/src/components/CandidateGovernancePanel.vue
6. ui/src/components/CandidateConversionPanel.vue
7. docs/reports/phase24_candidate_audit_handoff.md
8. CEK-TA-102 accepted 候选转正式知识 draft
```

## 已完成范围

```text
CEK-TA-103 done: Vue3 候选审计类型、字段映射和状态契约已补齐。
CEK-TA-104 done: 使用 path resolver 从 Phase 23 候选包生成前端 fixture。
CEK-TA-105 done: IngestionReview 已重构为候选审计工作台。
CEK-TA-106 done: 来源、冲突、治理、转换预览面板已接入。
CEK-TA-107 done: KnowledgeTreeView 已支持候选覆盖联动和 tree_node_id 过滤。
CEK-TA-108 done: 已生成 CEK-TA-102 handoff 报告和前端导出能力。
CEK-TA-109 done: 本报告完成构建、布局和审计链路验收。
```

## 数据验收

执行命令：

```text
python codex-expert-kit\rag\scripts\build_ui_candidate_fixture.py
```

结果：

```text
wrote ui/src/data/phase23Candidates.ts with 7 candidates
```

验收结论：

```text
1. fixture 从 codex-expert-kit/rag/candidates/ 聚合生成，不依赖手工 mock。
2. 本批次共 7 条候选，覆盖 KB_04、KB_05、KB_06、KB_07、KB_10、KB_11、KB_13。
3. handoff 报告显示 7 条候选均建议 accepted_for_draft。
4. 7 条候选均有 source_refs。
5. missing_fields_present 为 0。
6. blocking_issues_present 为 0。
7. 转换预览目标状态限定为 draft，不允许直接 approved。
```

## Vue3 验收

执行命令：

```text
npm run build
```

结果：

```text
vue-tsc --noEmit && vite build
dist/index.html
dist/assets/index-p_Sr30nA.css
dist/assets/index-BZgX71zC.js
build passed
```

验收结论：

```text
1. TypeScript 类型检查通过。
2. Vite 生产构建通过。
3. 候选列表、候选详情、来源证据、冲突审计、治理检查和转换预览均有代码路径承接。
4. KnowledgeTreeView 可以通过 /ingestion?tree_node_id=... 联动候选审计过滤。
5. IngestionReview 支持候选过滤、风险排序、空状态和 tree_node_id 过滤提示。
6. 审计交接支持 JSON 与 Markdown 下载。
7. SearchLab/MCP 默认指导未接入候选知识，候选仍停留在审计链路。
```

## 布局验收

已检查关键样式：

```text
1. candidate-workbench 使用稳定网格布局。
2. detail-section-grid 固定详情区结构。
3. evidence-row 对来源标题、摘要、URL 做换行约束。
4. gate-row 对治理检查项做稳定布局。
5. @media (max-width: 960px) 下 candidate-workbench、detail-section-grid、evidence-row、gate-row 均收敛为单列。
```

未执行浏览器截图或 Playwright 视觉回归。当前验收以 `npm run build`、代码路径检查和响应式 CSS 检查为准。

## 边界确认

```text
1. 本 Phase 未引入数据库。
2. 本 Phase 未引入新的后端服务。
3. 本 Phase 未开放 MCP 写权限。
4. 本 Phase 未让浏览器直接写入 candidates/ 或 knowledge/。
5. 本 Phase 未把候选知识标记为 approved。
6. 本 Phase 未采集行情、K 线、订单簿或交易原始数据。
7. 本 Phase 新增脚本使用 path resolver，不依赖开发机绝对路径。
```

## 风险与后续

风险：

```text
1. 当前 handoff 是审计交接草案，不替代人工复核。
2. 当前未做浏览器截图级布局验收，后续可在引入 Playwright 后补充。
3. CEK-TA-102 转 draft 时仍需再次检查来源、冲突、适用边界和重复知识关系。
```

下一步：

```text
1. 执行 CEK-TA-102，把 accepted_for_draft 候选转换为正式知识 draft。
2. 重建 codex-expert-kit/rag/indexes/knowledge_items.json。
3. 运行 MCP/SearchLab 验证，确认 draft 不作为默认 approved 指导返回。
```

## DoD 结论

Phase 24 的交付物、上下游、契约、边界和测试均已闭环。`CEK-TA-109` 可以标记为 done，Phase 24 可以标记为 done。
