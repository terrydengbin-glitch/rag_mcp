# Phase 8 其他项目接入任务卡

## Phase 目标

让其他交易、回测、模拟盘、实盘风控、LLM、RAG 项目能够稳定调用 CEK-TA 支持层，并明确项目事实、通用知识、Skill、MCP、Project Adapter 和知识倒灌之间的边界。

核心原则：

```text
业务项目只提供事实。
CEK-TA 提供可复用专家能力。
项目事实优先于通用知识。
项目私有字段不能污染 CEK-TA 通用知识库。
```

## 任务列表

| ID | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- |
| CEK-TA-033 | done | 编写其他项目接入指南 | `docs/其他项目接入指南.md` |
| CEK-TA-034 | done | 创建业务项目 `AGENTS.md` 模板 | `codex-expert-kit/templates/external_project_AGENTS.md` |
| CEK-TA-035 | done | 创建 Project Adapter 模板 | `codex-expert-kit/templates/project_adapter.md` |
| CEK-TA-036 | done | 创建 MCP 接入示例配置 | `codex-expert-kit/templates/codex_config_mcp.toml` |

## 上游输入

```text
docs/其他项目接入指南.md
docs/知识倒灌与反哺规范.md
codex-expert-kit/core/AGENTS.md
codex-expert-kit/templates/project_AGENTS.md
codex-expert-kit/mcp/mcp_server_spec.md
codex-expert-kit/mcp/search_expert_knowledge.py
codex-expert-kit/templates/interface_contract.md
codex-expert-kit/templates/trade_result_schema.md
```

## 下游输出

```text
业务项目:
  复制或引用 external_project_AGENTS.md 和 project_adapter.md，建立项目事实与 CEK-TA 的边界。

Codex:
  通过业务项目 AGENTS.md 知道 CEK-TA 路径、启用 domains、项目事实文档、验证规则和倒灌边界。

MCP/RAG:
  使用 codex_config_mcp.toml 作为只读 Knowledge MCP 接入示例。

Phase 9 知识倒灌:
  业务项目反哺时先创建倒灌任务卡，而不是直接写入 CEK-TA。
```

## 输入契约

业务项目接入 CEK-TA 时必须提供：

```text
project_name
project_type
CEK-TA location
enabled domains
project fact documents
data schema mapping
run commands
validation metrics
rollback path
contribution policy
```

## 输出契约

接入模板必须输出：

```text
业务项目 AGENTS.md
Project Adapter
MCP config example
接入验收 checklist
```

## 边界范围

本 Phase 做：

```text
1. 定义业务项目 AGENTS.md 模板。
2. 定义 Project Adapter 模板。
3. 定义 Codex MCP 配置示例。
4. 更新其他项目接入指南中的 MCP tool 名称。
5. 更新任务索引和 README。
```

本 Phase 不做：

```text
1. 不接入某个真实业务项目。
2. 不复制 CEK-TA 知识到业务项目。
3. 不启用真实 MCP 写操作。
4. 不引入数据库、后端框架或外部服务。
5. 不接受未经脱敏的项目经验倒灌。
```

## 涉及组件

```text
docs/tasks/phase8_external_project_integration.md
docs/其他项目接入指南.md
codex-expert-kit/templates/external_project_AGENTS.md
codex-expert-kit/templates/project_adapter.md
codex-expert-kit/templates/codex_config_mcp.toml
docs/index_tasks.md
docs/tasks/README.md
codex-expert-kit/README.md
```

## 涉及数据结构

```text
ProjectAdapter
ProjectFacts
FieldMapping
DomainMapping
ValidationPlan
McpConfig
ContributionPolicy
```

## 涉及数据库/存储

当前 Phase 不引入数据库。业务项目事实仍存放在业务项目自身文档中，CEK-TA 只提供模板和契约。

## 实施步骤

```text
1. 创建 Phase 8 任务卡。
2. 创建 external_project_AGENTS.md。
3. 创建 project_adapter.md。
4. 创建 codex_config_mcp.toml。
5. 更新 docs/其他项目接入指南.md。
6. 更新 docs/index_tasks.md。
7. 更新 docs/tasks/README.md。
8. 更新 codex-expert-kit/README.md。
9. 执行文件存在性、关键章节、状态一致性和 UTF-8 检查。
```

## Definition of Done

```text
1. Phase 8 任务卡存在，并包含上下游、契约、边界、DoD 和测试。
2. external_project_AGENTS.md 能指导业务项目接入 CEK-TA。
3. project_adapter.md 能声明项目类型、事实文档、字段映射、运行命令、验证和回滚。
4. codex_config_mcp.toml 是只读 Knowledge MCP 示例，不授予交易、账户、密钥或写知识权限。
5. docs/其他项目接入指南.md 与 Phase 3 MCP tool 名称一致。
6. docs/index_tasks.md、docs/tasks/README.md、Phase 任务卡状态一致。
7. 中文文档 UTF-8 读取无乱码。
```

## 测试与验收

```text
1. Test-Path 检查全部交付物存在。
2. Select-String 检查模板关键章节。
3. 检查 Phase 8、CEK-TA-034、CEK-TA-035、CEK-TA-036 均为 done。
4. 检查 MCP 配置只读说明存在。
5. Get-Content -Encoding UTF8 检查中文文档无乱码。
```

## 风险与回滚

风险：

```text
1. 业务项目误把项目事实写进 CEK-TA 通用知识。
2. 业务项目误把 CEK-TA 通用知识复制到本地并形成分叉。
3. MCP 配置被误解为写入或交易能力。
4. Project Adapter 字段映射不完整，导致 Codex 错读项目事实。
```

回滚：

```text
1. 文档模板可通过版本控制回退。
2. 如模板被业务项目采用，后续只新增兼容字段，不直接删除旧字段。
3. 如 MCP server 尚未真实部署，配置模板保持 disabled-by-default 或显式标记草案。
```

## 需要开发者确认的问题

当前 Phase 只创建模板和只读配置示例，不接真实业务项目、不引入外部服务、不改变 MCP 权限，因此无需确认。

后续如果要把某个真实项目接进来、改变 MCP 权限、启用写操作或接入外部服务，必须单独向开发者确认。

## 状态更新要求

完成后必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase8_external_project_integration.md
codex-expert-kit/README.md
```
