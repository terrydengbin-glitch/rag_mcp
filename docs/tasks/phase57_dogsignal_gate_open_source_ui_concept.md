# Phase 57: DogSignal Gate 开源品牌 UI 方案与 HTML 原型

## Phase 目标

Phase 57 用于把当前 Vue3 审计工作台从 `CEK-TA Audit / MCP 工具感` 调整为 `DogSignal Gate 开源知识与交易 AI 治理平台` 的整体品牌方向。

本 Phase 只产出方案与 HTML 原型，不直接修改 Vue3 代码。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-548 | P0 | done | 创建 Phase 57 任务卡、索引入口和 UI 原型契约 | `docs/tasks/phase57_dogsignal_gate_open_source_ui_concept.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-547 |
| CEK-TA-549 | P0 | done | 梳理 DogSignal Gate 开源品牌 UI 优化方案 | `docs/ui/dogsignal_gate_ui_optimization_plan.md` | CEK-TA-548 |
| CEK-TA-550 | P0 | done | 产出 DogSignal Gate 审计工作台 HTML 原型 | `docs/prototypes/dogsignal_gate_open_source_ui_concept.html` | CEK-TA-549 |
| CEK-TA-551 | P1 | done | 对齐当前 Vue3 导航、模块命名和后续落地拆分 | `docs/ui/dogsignal_gate_ui_optimization_plan.md` | CEK-TA-550 |
| CEK-TA-552 | P1 | done | 运行 HTML/UTF-8/文案边界验收 | `docs/reports/phase57_dogsignal_gate_ui_concept_report.md` | CEK-TA-551 |

## 上游输入

```text
用户提供的 DogSignal Gate 项目 Logo 截图
ui/src/App.vue
ui/src/styles.css
ui/src/router.ts
docs/Vue3知识审计界面需求.md
docs/tasks/phase51_knowledge_tree_large_scope_performance.md
README.md
docs/external_mcp_quickstart.md
```

## 下游输出

```text
1. DogSignal Gate 开源品牌 UI 方案。
2. 可直接浏览的 HTML 原型。
3. 后续 Vue3 实施任务的组件拆分建议。
4. Phase 57 验收报告。
```

## 输入契约

```text
1. Logo 是 DogSignal Gate 项目整体品牌，不是 MCP 子模块标识。
2. 当前 Vue3 是知识审计工作台，不是营销页。
3. 用户可见文案必须中文。
4. MCP/RAG/知识树/候选/倒灌只是平台能力模块。
5. HTML 原型必须能离线打开，不依赖外部 CDN。
```

## 输出契约

### UI 方案

必须包含：

```text
品牌定位
信息架构
导航命名
首页/工作台布局
颜色与字体建议
Logo 使用规则
开源项目 README/GitHub 展示建议
Vue3 落地拆分
不做什么
```

### HTML 原型

必须包含：

```text
DogSignal Gate 品牌栏
全局导航
开源项目状态区
知识库 / MCP / 审计 / 接入模块入口
知识树与审计队列预览
右侧治理摘要
响应式布局
中文用户可见文案
```

## 边界范围

范围内：

```text
1. 产出方案文档和 HTML 原型。
2. 明确 DogSignal Gate 是总体品牌，MCP 是能力模块。
3. 给后续 Vue3 改造提供组件拆分和视觉规范。
4. 保持审计工作台定位，不改成营销落地页。
```

范围外：

```text
1. 不直接改 Vue3 源码。
2. 不引入外部 UI 框架。
3. 不引入后端、数据库或新 API。
4. 不改变 MCP 权限。
5. 不改变知识库 schema。
6. 不生成交易建议、买卖点、仓位、杠杆或风控阈值。
```

## 不做什么

```text
1. 不把 MCP 作为项目主品牌。
2. 不把审计工作台做成纯营销页。
3. 不在 HTML 原型里引用不可用的远程资源。
4. 不把 Logo 截图硬编码成仓库资产；正式落地时需要用户提供原始 Logo 文件。
```

## 涉及组件

```text
ui/src/App.vue
ui/src/styles.css
ui/src/views/DashboardView.vue
ui/src/views/KnowledgeTreeView.vue
ui/src/views/IngestionReview.vue
ui/src/views/SearchLab.vue
docs/ui/
docs/prototypes/
docs/reports/
```

## 涉及数据结构

```text
NavigationItem
BrandHeader
ModuleEntry
KnowledgeSummary
GovernanceSummary
AuditQueueSummary
```

## 涉及数据库/存储

不涉及数据库或存储变更。

## 实施步骤

```text
1. 创建 Phase 57 任务卡并更新索引。
2. 基于当前 Vue3 导航和用户提供 Logo，编写 UI 优化方案。
3. 创建可离线打开的 HTML 原型。
4. 验证文案中文、无乱码、HTML 文件存在。
5. 生成验收报告。
6. 更新任务状态。
```

## Definition of Done

```text
1. Phase 57 任务卡存在并被索引收录。
2. UI 优化方案存在。
3. HTML 原型存在且可离线打开。
4. 方案明确 DogSignal Gate 是整体项目 Logo，MCP 是子能力。
5. 原型用户可见文案为中文。
6. UTF-8 乱码门禁通过。
7. Phase 57 验收报告存在。
8. 任务状态已更新。
```

## 测试与验收

```text
1. 使用 rg 检查 Phase 57 索引入口。
2. 使用 validate_no_mojibake.py 检查 UTF-8 和乱码。
3. 检查 HTML 文件存在并包含 DogSignal Gate、知识库、MCP、审计、接入等关键文案。
```

## 风险与回滚

风险：

```text
1. Logo 原始文件未入库，HTML 原型只能使用占位品牌标识。
2. 如果后续 Vue3 实施时直接套用营销页布局，可能破坏审计工作台效率。
3. 如果品牌色过度偏蓝，可能与当前界面信息密度不协调。
```

回滚：

```text
1. 本 Phase 只新增文档和 HTML 原型，可直接文件级回滚。
2. Vue3 源码未修改，不影响运行时。
```

## 需要开发者确认的问题

```text
1. 正式 Vue3 落地前，需要用户提供 Logo 原始图片文件或 SVG。
2. 是否将项目公开名称统一改为 DogSignal Gate，需要在 README、Vue3、包名和 GitHub 描述中统一确认。
```

## 状态更新要求

每完成任务后同步更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase57_dogsignal_gate_open_source_ui_concept.md
```
