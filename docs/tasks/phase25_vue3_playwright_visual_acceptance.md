# Phase 25: Vue3 审计界面实机验收

## Phase 目标

用 Playwright 对 Vue3 知识审计工作台执行真实浏览器验收，覆盖候选审计页、知识树页、SearchLab 页的桌面端和移动端截图，并检查页面无空白、关键内容可见、无横向溢出、过滤跳转可用。

本 Phase 是 Phase 24 的实机补验收，不改变 Vue3 信息架构，不引入数据库、不引入后端服务、不开放 MCP 写权限，也不改变知识入库状态。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-110 | P0 | done | 创建 Phase 25 任务卡并登记任务索引 | `docs/tasks/phase25_vue3_playwright_visual_acceptance.md`、`docs/index_tasks.md`、`docs/tasks/README.md` |
| CEK-TA-111 | P0 | done | 增加 Playwright 实机验收配置与测试 | `ui/playwright.config.ts`、`ui/tests/e2e/audit-workbench.spec.ts` |
| CEK-TA-112 | P0 | done | 执行桌面/移动端截图和交互验证 | `ui/test-results/`、`ui/playwright-report/` |
| CEK-TA-113 | P1 | done | 生成 Phase 25 实机验收报告 | `docs/reports/phase25_vue3_playwright_visual_acceptance_report.md` |

## 上游输入

```text
1. docs/tasks/phase24_vue3_candidate_audit_workbench_v2.md
2. docs/reports/phase24_vue3_candidate_audit_report.md
3. ui/src/views/IngestionReview.vue
4. ui/src/views/KnowledgeTreeView.vue
5. ui/src/views/SearchLab.vue
6. ui/src/data/phase23Candidates.ts
7. ui/src/stores/auditStore.ts
8. ui/src/styles.css
```

## 下游输出

```text
1. Playwright 实机验收测试，供后续每次前端改版回归使用。
2. 桌面端和移动端截图，供人工审计 UI 是否空白、错位、重叠。
3. Phase 25 验收报告，说明实机测试结果、限制和后续风险。
```

## 输入契约

Playwright 测试必须以 Vue3 生产构建或 Vite 本地服务为入口，访问以下路由：

```yaml
routes:
  - path: /ingestion
    expected_heading: 候选知识审计
    expected_content:
      - 审计队列
      - 来源证据
      - 冲突审计
      - 转换预览
  - path: /knowledge-tree
    expected_heading: 知识树
    expected_content:
      - 候选覆盖
      - candidates
  - path: /search-lab
    expected_heading: 检索测试台
    expected_content:
      - Matches
      - Blocked
```

视口契约：

```yaml
desktop:
  width: 1440
  height: 1000
mobile:
  width: 390
  height: 844
```

## 输出契约

每个测试用例必须至少产出：

```text
1. 页面可访问。
2. 页面标题或核心 heading 可见。
3. 页面 body 文本非空。
4. 关键审计内容可见。
5. document 横向滚动宽度不得超过 viewport 宽度超过容差。
6. 主要面板、队列、表格、匹配列表不能是 0 宽或 0 高。
7. 知识树 candidates 链接点击后进入 /ingestion?tree_node_id=... 并显示过滤 banner。
8. 桌面和移动端截图写入 test-results。
```

## 边界范围

范围内：

```text
1. 增加 Playwright dev dependency 和测试脚本。
2. 使用 Vite webServer 启动本地 Vue3。
3. 对 /ingestion、/knowledge-tree、/search-lab 做桌面和移动端验收。
4. 生成测试报告和截图。
5. 记录无法自动判断的视觉风险。
```

范围外：

```text
1. 不改动知识库内容。
2. 不改变 MCP 权限。
3. 不引入后端服务或数据库。
4. 不实现在线人工审核写入。
5. 不把候选或 draft 改成 approved。
6. 不采集行情、K 线、订单簿或交易原始数据。
```

## 涉及组件

```text
ui/package.json
ui/playwright.config.ts
ui/tests/e2e/audit-workbench.spec.ts
ui/src/views/IngestionReview.vue
ui/src/views/KnowledgeTreeView.vue
ui/src/views/SearchLab.vue
docs/reports/phase25_vue3_playwright_visual_acceptance_report.md
```

## 涉及数据结构

```text
Playwright TestResult
Screenshot artifact
Viewport profile
Route acceptance case
Visual acceptance report
```

## 涉及数据库/存储

不涉及数据库。测试产物为本地文件：

```text
ui/test-results/
ui/playwright-report/
```

## 实施步骤

```text
1. 创建 Phase 25 任务卡。
2. 更新 docs/index_tasks.md 和 docs/tasks/README.md。
3. 安装或登记 Playwright 测试依赖。
4. 增加 Playwright config，配置 Vite webServer。
5. 编写桌面和移动端页面验收测试。
6. 增加知识树 candidates 链接到候选审计页的跳转验证。
7. 运行 npm run build 和 Playwright 测试。
8. 生成 Phase 25 验收报告。
9. 更新任务状态。
```

## Definition of Done

```text
1. Phase 25 已登记到 docs/index_tasks.md。
2. docs/tasks/README.md 已登记 Phase 25。
3. Playwright 配置和测试文件存在。
4. npm run build 通过。
5. Playwright 桌面端和移动端测试通过，或报告明确失败原因。
6. 候选审计页、知识树页、SearchLab 页均有截图产物。
7. 知识树 candidates 链接能跳转到候选审计过滤页。
8. 测试报告记录无空白、无横向溢出、关键面板非 0 尺寸。
9. 中文文档保持 UTF-8。
```

## 测试与验收

```text
npm run build
npm run test:e2e
```

验收重点：

```text
1. /ingestion 桌面和移动端都能显示候选队列、候选详情和审计面板。
2. /knowledge-tree 桌面和移动端都能显示知识树表格和候选覆盖入口。
3. /search-lab 桌面和移动端都能显示检索用例、Matches 和 Blocked。
4. 页面没有空白首屏。
5. 页面没有横向溢出。
6. 知识树候选链接跳转后 URL 包含 tree_node_id，并显示过滤 banner。
```

## 风险与回滚

风险：

```text
1. 本地环境首次运行 Playwright 可能需要下载 Chromium。
2. 自动化测试只能覆盖关键布局与交互，不能替代人工审美判断。
3. 截图文件较大，默认不进入 docs 文档正文。
```

回滚：

```text
1. 移除 ui/playwright.config.ts。
2. 移除 ui/tests/e2e/。
3. 移除 package.json 中 Playwright 相关脚本和依赖。
4. 删除 test-results/playwright-report 临时产物，不影响正式知识库。
```

## 需要开发者确认的问题

```text
1. 是否需要把 Playwright 截图纳入版本管理？当前默认不强制纳入，只保留本地测试产物。
2. 是否后续引入更严格的视觉 diff baseline？当前 Phase 只做实机截图和关键布局断言。
```

## 状态更新要求

完成任一子任务后必须更新：

```text
1. docs/index_tasks.md
2. docs/tasks/README.md
3. 本任务卡任务列表状态
4. 如新增报告，更新 docs/index_tasks.md 文档入口
```
