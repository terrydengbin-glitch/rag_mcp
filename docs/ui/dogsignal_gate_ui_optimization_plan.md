# DogSignal Gate 开源品牌 UI 优化方案

## 结论

DogSignal Gate 应作为整个开源项目的总品牌。MCP、RAG、知识树、候选审计、SearchLab、外部接入和知识倒灌都应作为平台能力模块呈现，而不是让 MCP 或 CEK-TA Audit 占据主品牌位置。

建议目标：

```text
左上角：DogSignal Gate 项目品牌
副标题：交易 AI 知识库与审计工作台
模块层级：知识库 / 审计 / 检索 / 接入 / 治理
MCP 定位：只读知识检索接口模块
```

## 当前问题

当前 Vue3 `App.vue` 的品牌区是：

```text
CEK-TA
Audit
```

这会带来三个问题：

```text
1. 对开源用户来说，项目品牌不明确。
2. MCP 容易被误解为整个项目，而不是能力模块之一。
3. GitHub 访问者难以在第一眼理解项目价值：交易 AI 知识库、审计治理、外部项目接入。
```

## 品牌定位

建议公开表达：

```text
DogSignal Gate
交易 AI 知识库与审计工作台
```

一句话说明：

```text
面向交易系统和 AI IDE 的专业知识库、RAG/MCP 检索、审计治理与外部项目接入平台。
```

不建议：

```text
1. 把项目说成单纯 MCP server。
2. 把项目说成交易策略系统。
3. 把项目说成自动交易机器人。
4. 把审计工作台改成营销落地页。
```

## 信息架构

建议把导航分为五组：

| 分组 | 页面 | 说明 |
| --- | --- | --- |
| 工作台 | 总览、任务 | 当前知识库和治理状态 |
| 知识资产 | 知识、知识树、来源 | 正式知识、分类、来源 |
| 审计治理 | 候选、冲突、倒灌 | 候选审计、冲突处理、知识回灌 |
| 运行工具 | 测试、接入 | SearchLab、MCP、外部项目健康检查 |
| 系统 | 设置 | 路径、索引、权限、版本 |

当前导航可以保留，但品牌层级需要变成：

```text
DogSignal Gate
交易 AI 知识库与审计工作台
```

而不是：

```text
CEK-TA / Audit
```

## 首页布局

开源项目需要第一屏说明“这是什么”和“现在能做什么”，但应用首屏仍应是可操作工作台。

建议首页结构：

```text
顶部品牌栏：
  DogSignal Gate
  交易 AI 知识库与审计工作台
  GitHub / 文档 / MCP 状态

左侧导航：
  总览
  知识库
  知识树
  候选审计
  SearchLab
  MCP 接入
  冲突治理
  来源审计
  任务
  倒灌
  设置

中间主工作区：
  当前知识库基线
  AI Engineering / Trading Engineering 双主线状态
  候选审计队列
  SearchLab 快速测试

右侧治理摘要：
  MCP 只读状态
  reviewed / approved / caveat_only 统计
  最近验收报告
  外部项目接入入口
```

## 视觉风格

参考用户提供的 Logo，建议使用克制的深蓝、冰蓝和白底系统色。

颜色建议：

```text
主色：#0b2a4a 深海军蓝
强调色：#0ea5e9 科技蓝
亮强调：#22d3ee 青蓝
背景：#f5f8fb 冷白灰
面板：#ffffff
边框：#d7e2ee
文本主色：#0f172a
文本次色：#5b6b7f
成功：#0f9f6e
警告：#c47a00
风险：#d04545
```

原则：

```text
1. 不做大面积深色，审计工作台需要长时间阅读。
2. 不使用花哨渐变作为主要背景。
3. 品牌蓝只用于导航选中、按钮、关键指标和链接。
4. 知识卡片保持紧凑，适合上千条知识浏览。
5. 所有用户可见文案使用中文。
```

## Logo 使用规则

当前用户提供的是项目整体 Logo，应放在：

```text
1. 左侧导航顶部。
2. 开源 README 顶部。
3. 登录/加载页。
4. GitHub social preview。
```

不建议把 Logo 放在：

```text
1. 每张知识卡片上。
2. 每个 MCP 工具按钮上。
3. 审计详情正文里反复出现。
```

正式落地时需要新增资产：

```text
ui/public/brand/dogsignal-gate-logo.png
ui/public/brand/dogsignal-gate-mark.png
ui/public/brand/dogsignal-gate-social.png
```

## 模块命名建议

| 当前名称 | 建议展示名称 | 说明 |
| --- | --- | --- |
| CEK-TA Audit | DogSignal Gate | 项目总品牌 |
| 知识 | 知识库 | 更明确 |
| 测试 | SearchLab | 保留工具属性 |
| 接入 | MCP 接入 | 更明确 |
| 候选 | 候选审计 | 更明确 |
| 倒灌 | 知识倒灌 | 更明确 |

## GitHub 开源展示建议

README 顶部建议：

```text
DogSignal Gate
交易 AI 知识库与审计工作台

为交易系统、回测、模拟盘、实盘风控、AI IDE 和 RAG 项目提供：
专业知识库、MCP 检索、候选审计、知识树、外部接入和知识倒灌。
```

GitHub topics 建议：

```text
trading
rag
mcp
ai-engineering
knowledge-base
vue3
audit
quant-trading
```

## Vue3 落地拆分

后续实际实现建议拆成：

```text
BrandHeader.vue
SidebarNavigation.vue
ModuleStatusCard.vue
GovernanceSummaryPanel.vue
OpenSourceProjectBanner.vue
QuickActionPanel.vue
```

改造顺序：

```text
1. 替换 App.vue 品牌区和导航命名。
2. 增加 DogSignal Gate logo 资产。
3. 调整 DashboardView 为开源工作台首页。
4. 保持 KnowledgeTree / Candidate / SearchLab 的既有数据流不变。
5. 用 Playwright 验证桌面和移动端无重叠、无白屏。
```

## 不做什么

```text
1. 不把 Vue3 改成纯官网。
2. 不削弱审计、候选、来源、冲突、MCP 检索能力。
3. 不把 reviewed/caveat_only 视觉上伪装成 approved。
4. 不让 Logo 占用过多工作台空间。
5. 不引入外部 UI 框架或远程字体依赖。
```

## 原型文件

HTML 原型：

[dogsignal_gate_open_source_ui_concept.html](../prototypes/dogsignal_gate_open_source_ui_concept.html)

