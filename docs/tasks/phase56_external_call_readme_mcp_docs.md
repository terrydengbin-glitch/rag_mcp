# Phase 56: 外部调用 README 与 MCP 接入文档清晰化

## Phase 目标

Phase 56 用于把“其他项目如何调用 CEK-TA 知识库”的入口文档补清楚，降低外部项目接入 MCP/SearchLab/正式知识索引时的理解成本。

本 Phase 的目标是确认：

```text
1. 根 README 能在第一屏说明 CEK-TA 是什么、谁来用、如何通过 MCP 调用知识库。
2. 外部项目有一份短路径 MCP 快速接入手册，覆盖安装、路径、配置、健康检查、查询示例和常见错误。
3. 现有《其他项目接入指南》与 MCP 快速手册互相引用，且不再把关键调用步骤埋在长文档中。
4. MCP server spec 对齐当前运行时能力，包括 --info、--list-tools、--call、--request-json、--request-file、--knowledge-items-path 和只读权限边界。
5. 配置模板明确 enabled=false 与 enabled=true 的使用时机，避免健康检查前误启用。
6. 文档示例遵守路径 resolver / CEK_TA_ROOT / CEK_TA_KNOWLEDGE_ITEMS_PATH 规则，不依赖开发机绝对路径。
```

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-541 | P0 | done | 创建 Phase 56 任务卡、索引入口和文档契约 | `docs/tasks/phase56_external_call_readme_mcp_docs.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-540 |
| CEK-TA-542 | P0 | done | 重写根 README 快速接入区 | `README.md` | CEK-TA-541 |
| CEK-TA-543 | P0 | done | 新增外部项目 MCP 快速接入手册 | `docs/external_mcp_quickstart.md` | CEK-TA-542 |
| CEK-TA-544 | P0 | done | 更新其他项目接入指南中的 MCP 调用入口和启用时机 | `docs/其他项目接入指南.md` | CEK-TA-543 |
| CEK-TA-545 | P0 | done | 对齐 MCP server spec 到当前运行时能力 | `codex-expert-kit/mcp/mcp_server_spec.md` | CEK-TA-544 |
| CEK-TA-546 | P1 | done | 更新 MCP 配置模板和正式索引 README 的调用说明 | `codex-expert-kit/templates/codex_config_mcp.toml`、`codex-expert-kit/rag/indexes/README.md` | CEK-TA-545 |
| CEK-TA-547 | P1 | done | 运行文档链接、UTF-8、MCP CLI smoke 和 Phase 56 验收报告 | `docs/reports/phase56_external_call_docs_acceptance_report.md` | CEK-TA-546 |

## 上游输入

```text
README.md
docs/其他项目接入指南.md
codex-expert-kit/mcp/mcp_server_spec.md
codex-expert-kit/mcp/server.py
codex-expert-kit/templates/codex_config_mcp.toml
codex-expert-kit/templates/project_adapter.md
codex-expert-kit/templates/external_project_healthcheck.md
codex-expert-kit/rag/indexes/README.md
codex-expert-kit/rag/indexes/knowledge_items.json
docs/tasks/phase10_external_project_runtime_integration.md
docs/tasks/phase21_formal_mcp_knowledge_index.md
docs/tasks/phase35_external_ai_active_retrieval_protocol.md
docs/tasks/phase55_runtime_acceptance_baseline.md
```

## 下游输出

```text
1. 面向外部项目的 README 快速入口。
2. 面向外部项目的 MCP 快速接入手册。
3. 更新后的其他项目接入指南。
4. 对齐当前运行时的 MCP server spec。
5. 明确 enabled 时机和路径变量的 MCP 配置模板。
6. 正式知识索引 README 的外部调用说明。
7. Phase 56 验收报告。
```

## 输入契约

### MCP 运行时能力

文档必须以当前运行时为准，至少覆盖：

```text
python codex-expert-kit/mcp/server.py --info
python codex-expert-kit/mcp/server.py --list-tools
python codex-expert-kit/mcp/server.py --call <tool_name> --request-json <json>
python codex-expert-kit/mcp/server.py --call <tool_name> --request-file <path>
python codex-expert-kit/mcp/server.py --knowledge-items-path <path>
```

### 路径解析

文档示例必须说明：

```text
1. 外部项目优先配置 CEK_TA_ROOT。
2. 如需指定正式知识索引，可配置 CEK_TA_KNOWLEDGE_ITEMS_PATH。
3. 示例中的本机路径只能作为示例，不得被描述为运行时依赖。
4. 运行时代码和脚本应通过 path_resolver 或环境变量定位 CEK-TA。
```

### 知识调用边界

文档必须明确：

```text
1. MCP 默认只读。
2. 查询正式知识索引，不把候选队列作为默认指导。
3. reviewed/caveat_only 不等于 approved。
4. default guidance 和 hard gate 权限必须由知识卡 machine_gate / review 字段决定。
5. 返回结果必须关注 source/citation/confidence/conflict/machine_gate。
```

## 输出契约

### 根 README 快速入口

必须包含：

```text
项目定位
适用对象
一分钟接入步骤
MCP CLI smoke 示例
Codex MCP 配置模板链接
常见健康检查
关键文档链接
边界说明
```

### `docs/external_mcp_quickstart.md`

必须包含：

```text
适用场景
目录准备
CEK_TA_ROOT / CEK_TA_KNOWLEDGE_ITEMS_PATH 配置
MCP server --info / --list-tools 验证
search_expert_knowledge 示例
get_knowledge_item 示例
browse_knowledge_tree 示例
Codex MCP 配置示例
enabled=false 到 enabled=true 的启用时机
常见错误与处理
外部 AI 主动检索协议链接
```

### MCP server spec

必须包含：

```text
tool name
purpose
input schema
output schema
error schema
permissions
CLI usage
configuration
path resolver rules
test cases
```

### Phase 56 验收报告

必须包含：

```text
report_id
generated_at
task_ids
documents_checked
links_checked
utf8_check
mcp_cli_smoke
path_variable_check
open_issues
gate_status
```

## 边界范围

范围内：

```text
1. 更新外部项目调用文档、README、MCP spec、配置模板说明。
2. 增加外部 MCP 快速接入手册。
3. 对齐当前 server.py CLI 能力和工具列表。
4. 验证文档链接、UTF-8、MCP CLI smoke。
5. 输出验收报告并更新任务状态。
```

范围外：

```text
1. 不新增 MCP tool。
2. 不改变 MCP 权限。
3. 不改变 MCP 返回 schema。
4. 不修改正式知识内容。
5. 不把 reviewed 升级 approved。
6. 不启用 default guidance。
7. 不启用 hard gate。
8. 不改变 Vue3 信息架构。
9. 不引入数据库、后端框架或外部服务依赖。
10. 不生成交易建议、买卖点、仓位、杠杆、止损止盈或风险阈值。
```

## 不做什么

```text
1. 不把本文档任务扩展成代码重构任务。
2. 不替外部项目写具体业务策略。
3. 不把候选知识作为默认检索源。
4. 不新增 Playwright/ChatGPT 自动审计流程。
5. 不删除旧文档，只做入口整理、链接和内容对齐。
```

## 涉及组件

```text
README.md
docs/external_mcp_quickstart.md
docs/其他项目接入指南.md
codex-expert-kit/mcp/mcp_server_spec.md
codex-expert-kit/templates/codex_config_mcp.toml
codex-expert-kit/rag/indexes/README.md
docs/reports/
docs/index_tasks.md
docs/tasks/README.md
```

## 涉及数据结构

```text
KnowledgeItem
MCPToolSpec
MCPSearchRequest
MCPSearchResponse
MCPGetKnowledgeItemRequest
MCPBrowseKnowledgeTreeRequest
ExternalProjectAdapter
ExternalProjectHealthcheck
Phase56AcceptanceReport
```

## 涉及数据库/存储

不引入数据库，不改变存储架构。继续使用文件化正式知识、聚合索引、候选队列和现有 MCP 运行时。

## 实施步骤

```text
1. 创建 Phase 56 任务卡并更新 docs/index_tasks.md、docs/tasks/README.md。
2. 梳理根 README 的外部接入入口，补一分钟接入和关键链接。
3. 新增 docs/external_mcp_quickstart.md，写清 MCP 调用步骤和健康检查。
4. 更新 docs/其他项目接入指南.md，把快速入口前置并链接 quickstart。
5. 更新 codex-expert-kit/mcp/mcp_server_spec.md，对齐当前 server.py CLI 和工具能力。
6. 更新 codex_config_mcp.toml 与 rag/indexes/README.md 的路径、enabled 时机和正式索引说明。
7. 运行 UTF-8、链接存在性和 MCP CLI smoke。
8. 生成 Phase 56 验收报告。
9. 更新任务状态。
```

## Definition of Done

```text
1. Phase 56 任务卡存在并被 docs/index_tasks.md、docs/tasks/README.md 收录。
2. 根 README 包含外部项目 MCP 快速接入入口。
3. docs/external_mcp_quickstart.md 存在，且可独立指导外部项目完成 smoke test。
4. docs/其他项目接入指南.md 与 quickstart 互相链接。
5. mcp_server_spec.md 与当前 server.py CLI 能力一致。
6. codex_config_mcp.toml 说明 enabled=false/true 的正确时机。
7. rag/indexes/README.md 说明 knowledge_items.json 是正式 MCP 默认索引。
8. 文档中的运行时路径不依赖开发机绝对路径。
9. MCP CLI smoke 能跑通或记录无法执行原因。
10. 中文文档按 UTF-8 读写，无乱码。
11. Phase 56 验收报告存在。
12. 任务状态更新完成。
```

## 测试与验收

建议验收命令：

```text
python codex-expert-kit/mcp/server.py --info
python codex-expert-kit/mcp/server.py --list-tools
python codex-expert-kit/mcp/server.py --call search_expert_knowledge --request-json "{\"query\":\"lookahead bias\",\"top_k\":3}"
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
```

文档验收：

```text
1. 检查新增/更新文档是否 UTF-8 可读。
2. 检查 README、quickstart、接入指南、MCP spec、索引 README 的互链是否存在。
3. 检查用户可见文案是否中文。
4. 检查示例命令不依赖固定盘符。
5. 检查配置示例说明健康检查通过后再启用 MCP。
```

## 风险与回滚

风险：

```text
1. 文档和实际 server.py CLI 漂移，导致外部项目照文档接入失败。
2. enabled=true 时机写得不清楚，导致外部项目健康检查前误启用。
3. 示例路径写成开发机绝对路径，影响迁移复用。
4. reviewed/caveat_only、approved、default guidance、hard gate 语义写混。
```

回滚：

```text
1. 本 Phase 只改文档和索引，可按文件级 diff 回滚。
2. 如果 MCP spec 与运行时不一致，以 server.py 当前 CLI 和测试结果为准修正文档。
3. 如果 quickstart 示例不可运行，先回退示例到 --info / --list-tools 最小 smoke。
```

## 需要开发者确认的问题

当前无需新增数据库、后端框架、MCP tool 或外部服务依赖。

如后续要改变 MCP tool 权限、默认启用写操作、引入远程托管 MCP 服务或改变知识默认指导语义，必须另行确认。

## 状态更新要求

每完成一个任务，必须同步更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase56_external_call_readme_mcp_docs.md
```

如新增 `docs/external_mcp_quickstart.md`，还必须更新：

```text
README.md
docs/其他项目接入指南.md
```
