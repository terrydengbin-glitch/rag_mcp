# Phase 10: 外部项目运行时接入增强任务卡

## Phase 目标

让其他交易、回测、模拟盘、实盘、LLM、RAG 项目不仅能阅读 CEK-TA 文档，还能以标准 adapter、AGENTS 模板、MCP 配置和健康检查流程稳定调用本项目，并把项目经验按规范回灌到 CEK-TA。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-044 | P0 | done | 定义外部项目运行时接入协议 | `docs/其他项目接入指南.md`、`codex-expert-kit/templates/project_adapter.md` |
| CEK-TA-045 | P0 | done | 定义外部项目接入健康检查 | `codex-expert-kit/templates/external_project_healthcheck.md` |
| CEK-TA-046 | P1 | done | 定义外部项目知识调用与回灌流程 | `codex-expert-kit/templates/contribution_from_project.md` |

## 上游输入

```text
docs/其他项目接入指南.md
docs/知识倒灌与反哺规范.md
codex-expert-kit/templates/external_project_AGENTS.md
codex-expert-kit/templates/project_adapter.md
codex-expert-kit/templates/codex_config_mcp.toml
codex-expert-kit/rag/contribution_schema.md
```

## 下游输出

```text
外部项目 AGENTS.md 接入
外部项目 Project Adapter
Knowledge MCP 调用参数
知识倒灌任务卡
Vue3 外部项目接入审计页
Phase 14 MCP runtime server
```

## 输入契约

外部项目必须声明：

```text
project_id
project_name
project_type
market
asset_classes
data_sources
strategy_types
runtime_modes
backtest_engine
execution_adapter
risk_scope
private_fields
allowed_cek_ta_tools
contribution_policy
```

## 输出契约

接入产物必须输出：

```text
adapter_status
missing_fields
unsupported_modes
allowed_tools
blocked_tools
project_fact_boundary
knowledge_query_scope
contribution_entrypoint
healthcheck_result
```

## 边界范围

范围内：

```text
定义接入协议
定义 adapter 字段
定义健康检查文档模板
定义知识调用流程
定义回灌入口
更新接入指南
```

范围外：

```text
不直接接入任何真实交易账户
不读取外部项目密钥
不改变 MCP 权限
不引入数据库或后端框架
不自动批准外部项目回灌知识
```

## 涉及组件

```text
docs/其他项目接入指南.md
docs/知识倒灌与反哺规范.md
codex-expert-kit/templates/
codex-expert-kit/mcp/
contributions/
ui/src/views/
```

## 涉及数据结构

```text
ProjectAdapter
ExternalProjectHealthcheck
ContributionFromProject
KnowledgeQueryScope
ToolPermissionProfile
```

## 涉及数据库/存储

第一阶段使用文件模板与 Markdown/JSON 示例，不引入数据库。若后续需要数据库，必须先单独创建任务卡并询问开发者确认。

## 实施步骤

1. 细化 `project_adapter.md`，明确外部项目事实边界。
2. 创建 `external_project_healthcheck.md`，用于检查接入是否完整。
3. 创建 `contribution_from_project.md`，用于从外部项目生成倒灌任务。
4. 更新 `docs/其他项目接入指南.md`，补充调用、健康检查、回灌流程。
5. 更新索引与任务状态。

## Definition of Done

```text
接入协议字段完整
Project Adapter 能区分项目事实和通用知识
健康检查模板存在
回灌入口模板存在
外部项目不能绕过 proposed 状态直接入库
文档链接可追踪
UTF-8 中文无乱码
```

## 测试与验收

```text
检查文件存在
检查关键章节存在
检查 adapter 字段覆盖输入契约
检查回灌状态只能进入 proposed
检查接入指南能链接到相关模板
使用 Get-Content -Encoding UTF8 检查中文显示
```

## 风险与回滚

风险：

```text
外部项目私有字段污染通用知识库
接入模板过宽导致权限边界不清
回灌流程绕过审计
```

回滚：

```text
保留 Phase 8 既有模板
新增模板以独立文件提供
若新流程有问题，可恢复到只读 MCP 查询和手工回灌
```

## 需要开发者确认的问题

```text
是否允许外部项目提交自动化回灌任务
是否需要给不同项目类型定义不同 adapter profile
是否允许 MCP 暴露 submit_knowledge_contribution 工具
```

## 状态更新要求

完成后更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase10_external_project_runtime_integration.md
```

## 完成记录

```text
completed_at: 2026-06-08
status: done
```

已完成：

```text
1. 细化 Project Adapter，增加项目身份、运行模式、数据源、权限、查询范围和运行时输出。
2. 创建外部项目健康检查模板。
3. 创建外部项目回灌入口模板。
4. 更新其他项目接入指南。
5. 回灌入口固定为 proposed，不允许直接写 approved。
```

测试：

```text
1. 检查新增文件存在。
2. 检查关键章节存在。
3. 检查 adapter 字段覆盖 Phase 10 输入契约。
4. 检查回灌模板包含 status: proposed 和 direct_approved_write_allowed: false。
5. 使用 Get-Content -Encoding UTF8 检查中文显示。
```
