# Phase 25 Vue3 Playwright Visual Acceptance Report

## 报告定位

本报告用于验收 Phase 25：Vue3 审计界面实机验收。验收对象是候选审计页、知识树页和 SearchLab 页，覆盖桌面端与移动端真实 Chromium 渲染、截图产物、页面非空、关键内容可见、无页面级横向溢出、主要面板非 0 尺寸，以及知识树 candidates 链接到候选审计过滤页的跳转。

## 上下游

上游输入：

```text
1. Phase 24 Vue3 候选知识审计工作台 v2
2. ui/src/views/IngestionReview.vue
3. ui/src/views/KnowledgeTreeView.vue
4. ui/src/views/SearchLab.vue
5. ui/src/data/phase23Candidates.ts
6. ui/src/styles.css
```

下游输出：

```text
1. ui/playwright.config.ts
2. ui/tests/e2e/audit-workbench.spec.ts
3. ui/test-results/**/*.png
4. ui/playwright-report/
5. 后续 Vue3 改版的实机回归入口
```

## 实现内容

```text
1. 增加 @playwright/test dev dependency。
2. 增加 npm 脚本：test:e2e、test:e2e:report。
3. 增加 Playwright 配置，使用 Vite preview 作为 webServer。
4. 增加 desktop-chromium 视口：1440x1000。
5. 增加 mobile-chromium 视口：390x844。
6. 增加 /ingestion、/knowledge-tree、/search-lab 页面验收。
7. 增加知识树 candidates 链接跳转 /ingestion?tree_node_id=... 的交互验收。
8. 根据实机失败结果修复移动端页面级横向溢出。
```

## 修复记录

第一轮 Playwright 验收发现：

```text
1. 测试断言的中文面板名与实际英文面板名不一致。
2. 移动端 SearchLab 和候选审计页存在页面级横向溢出。
3. 移动端顶部导航内部滚动内容会撑大 document scrollWidth。
```

已修复：

```text
1. 测试断言改为实际界面标题：Source Evidence、Conflict Audit、Draft Conversion Preview。
2. SearchLab match-row 在移动端改为单列。
3. 长 ID、URL、badge、metadata 值增加 overflow-wrap。
4. 移动端导航改为内部横向滚动。
5. html/body/app-shell 增加页面级 overflow-x hidden，保留导航自身横向滚动。
```

## 测试结果

执行命令：

```text
npm run build
npm run test:e2e
```

结果：

```text
npm run build: passed
npm run test:e2e: 8 passed
```

通过用例：

```text
desktop-chromium /ingestion renders with audit content
mobile-chromium /ingestion renders with audit content
desktop-chromium /knowledge-tree renders with audit content
mobile-chromium /knowledge-tree renders with audit content
desktop-chromium /search-lab renders with audit content
mobile-chromium /search-lab renders with audit content
desktop-chromium knowledge tree candidate link filters ingestion review
mobile-chromium knowledge tree candidate link filters ingestion review
```

## 截图产物

```text
ui/test-results/audit-workbench-ingestion-review-renders-with-audit-content-desktop-chromium/ingestion-review-desktop-chromium.png
ui/test-results/audit-workbench-ingestion-review-renders-with-audit-content-mobile-chromium/ingestion-review-mobile-chromium.png
ui/test-results/audit-workbench-knowledge-tree-renders-with-audit-content-desktop-chromium/knowledge-tree-desktop-chromium.png
ui/test-results/audit-workbench-knowledge-tree-renders-with-audit-content-mobile-chromium/knowledge-tree-mobile-chromium.png
ui/test-results/audit-workbench-search-lab-renders-with-audit-content-desktop-chromium/search-lab-desktop-chromium.png
ui/test-results/audit-workbench-search-lab-renders-with-audit-content-mobile-chromium/search-lab-mobile-chromium.png
ui/test-results/audit-workbench-knowledge--8c817-nk-filters-ingestion-review-desktop-chromium/knowledge-tree-filter-hop-desktop-chromium.png
ui/test-results/audit-workbench-knowledge--8c817-nk-filters-ingestion-review-mobile-chromium/knowledge-tree-filter-hop-mobile-chromium.png
```

## 验收结论

```text
1. 候选审计页、知识树页、SearchLab 页均可在桌面端和移动端真实渲染。
2. 页面 body 文本非空，关键 heading 和审计内容可见。
3. 页面级横向溢出已阻断。
4. 主要容器、表格、队列、详情面板和匹配列表均非 0 尺寸。
5. 知识树 candidates 链接可跳转到候选审计页，并携带 tree_node_id 过滤参数。
6. Playwright 截图已生成，可供人工复核。
```

## 边界确认

```text
1. 本 Phase 未改动知识库内容。
2. 本 Phase 未改变 MCP 权限。
3. 本 Phase 未引入后端服务或数据库。
4. 本 Phase 未实现浏览器写入 candidates/ 或 knowledge/。
5. 本 Phase 未把候选或 draft 改成 approved。
6. 本 Phase 未采集行情、K 线、订单簿或交易原始数据。
```

## 后续建议

```text
1. 后续每次改 Vue3 审计工作台，执行 npm run build 和 npm run test:e2e。
2. 如果 UI 进入稳定版，可在后续 Phase 增加视觉 diff baseline。
3. 截图默认作为本地验收产物，不强制写入长期文档。
```

## DoD 结论

Phase 25 已完成。Vue3 审计界面从构建级验收升级为真实浏览器桌面/移动端实机验收，且关键交互链路已通过。
