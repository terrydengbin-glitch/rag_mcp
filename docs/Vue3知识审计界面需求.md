# Vue3 知识审计界面需求

本项目需要提供 Vue3 界面，用于查看、检索、审计和维护专业知识库。界面不是营销页，而是面向知识审计和工程协作的工作台。

## 目标用户

```text
1. 策略开发者
2. 回测/模拟盘工程师
3. 实盘风控审计者
4. LLM/RAG 工程师
5. Codex 任务执行者
```

## 核心视图

### 1. 知识总览

展示知识库整体状态：

```text
domain 分布
review_status 分布
conflict 状态
freshness 状态
source_type 分布
最近更新
待审计数量
```

### 2. 知识检索

必须支持：

```text
关键词搜索
domain 过滤
subdomain 过滤
source_type 过滤
freshness 过滤
review_status 过滤
confidence 过滤
是否存在 conflict 过滤
```

### 3. 知识详情

单条知识详情必须显示：

```text
规则内容
适用范围
不适用场景
前置假设
来源列表
证据摘要
冲突列表
冲突消解说明
版本历史
审计状态
```

### 4. 冲突审计

用于集中处理理论冲突：

```text
冲突类型
冲突双方
来源等级对比
适用范围对比
版本对比
推荐消解方式
人工审计结论
```

### 5. 来源审计

用于查看资料质量：

```text
来源标题
来源 URL
来源类型
发布方
发布时间
访问时间
可靠性
引用了哪些知识条目
是否过期
```

### 6. Codex 任务记录

用于记录 Codex 如何采集、归类、消解冲突：

```text
任务 ID
问题
检索关键词
使用来源
新增知识
修改知识
发现冲突
人工确认项
执行时间
```

## 建议技术栈

```text
Vue 3
TypeScript
Vite
Pinia
Vue Router
TanStack Table 或同类表格组件
ECharts 或 Chart.js
Markdown 渲染组件
```

## 信息架构

```text
/dashboard
/knowledge
/knowledge/:id
/conflicts
/sources
/tasks
/settings
```

## 数据接口需求

第一阶段可以读取本地 JSON/Markdown 索引，后续接入 MCP 或后端 API。

建议接口：

```text
GET /api/knowledge
GET /api/knowledge/:id
GET /api/conflicts
GET /api/sources
GET /api/tasks
POST /api/review/:id
```

## 审计状态流

```text
draft
  -> reviewed
  -> approved
  -> deprecated

draft
  -> rejected
```

## 界面硬规则

```text
1. 首屏必须是知识审计工作台，不做介绍页。
2. 所有知识条目必须能追溯来源。
3. 冲突知识必须有明显状态标记。
4. 未审计知识不能混入 approved 规则。
5. 时间敏感知识必须显示更新时间和过期风险。
6. 支持按 domain 快速过滤。
7. 支持导出当前筛选结果用于 Codex 审计。
```
