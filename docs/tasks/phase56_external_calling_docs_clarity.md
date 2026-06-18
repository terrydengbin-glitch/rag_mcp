# Phase 56: 外部调用 README 与 MCP 接入文档清晰化

## Phase 目标

Phase 56 用于补齐外部项目调用 CEK-TA 的入口说明。当前 `README.md` 主要是文档索引，`docs/其他项目接入指南.md` 内容完整但较长，`mcp_server_spec.md` 偏契约且部分说明没有对齐当前 Phase 21/55 后的正式索引和运行时 CLI。

本 Phase 的目标是让新外部项目可以在 5 分钟内看懂：

```text
1. CEK-TA 是什么。
2. 什么时候用 AGENTS、Project Adapter、MCP/RAG、Vue3 审计界面和回灌流程。
3. 如何配置 CEK_TA_ROOT、CEK_TA_KNOWLEDGE_ITEMS_PATH 和 .codex/config.toml。
4. 如何用 server.py --info、--list-tools、--call 验证 MCP 能调用正式知识库。
5. MCP 返回的 reviewed/caveat_only 与 approved/default guidance 有什么区别。
6. 外部项目不能让 CEK-TA 读取密钥、账户、下单或写 approved 知识。
```

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-541 | P0 | todo | 创建 Phase 56 任务卡和索引入口 | `docs/tasks/phase56_external_calling_docs_clarity.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-540 |
| CEK-TA-542 | P0 | todo | 重写根 README，补“一分钟了解”和“5 分钟接入” | `README.md` | CEK-TA-541 |
| CEK-TA-543 | P0 | todo | 新增外部 MCP/RAG 快速接入文档 | `docs/external_mcp_quickstart.md` | CEK-TA-542 |
| CEK-TA-544 | P0 | todo | 精简增强其他项目接入指南的 MCP 快速入口 | `docs/其他项目接入指南.md` | CEK-TA-543 |
| CEK-TA-545 | P0 | todo | 更新 MCP server spec，对齐当前 server.py CLI、正式索引、tool list 和权限边界 | `codex-expert-kit/mcp/mcp_server_spec.md` | CEK-TA-544 |
| CEK-TA-546 | P1 | todo | 更新 MCP 配置模板注释，明确 enabled=false 到 enabled=true 的启用条件 | `codex-expert-kit/templates/codex_config_mcp.toml` | CEK-TA-545 |
| CEK-TA-547 | P1 | todo | 运行文档、MCP smoke、乱码和链接入口验收 | `docs/reports/phase56_external_calling_docs_clarity_report.md` | CEK-TA-546 |

## 上游输入

```text
README.md
docs/其他项目接入指南.md
codex-expert-kit/templates/codex_config_mcp.toml
codex-expert-kit/mcp/mcp_server_spec.md
codex-expert-kit/mcp/server.py
codex-expert-kit/rag/indexes/README.md
docs/reports/phase55_knowledge_base_baseline_report.json
docs/reports/phase55_runtime_acceptance_report.json
codex-expert-kit/templates/project_adapter.md
codex-expert-kit/templates/external_project_healthcheck.md
```

## 下游输出

```text
1. 外部项目能从 README 直接找到最小接入步骤。
2. 外部项目能从 docs/external_mcp_quickstart.md 复制 MCP 配置和验证命令。
3. MCP server spec 与当前 server.py 实际 CLI、tool list 和正式知识索引一致。
4. codex_config_mcp.toml 明确健康检查通过后再启用。
5. 其他项目接入指南保留完整链路，同时新增快速入口。
```

## 输入契约

文档读取时必须使用 UTF-8。需要核对的运行时事实包括：

```text
server.py --info
server.py --list-tools
server.py --call <tool> --request-json <json>
server.py --call <tool> --request-file <path>
server.py --knowledge-items-path <path>
CEK_TA_ROOT
CEK_TA_KNOWLEDGE_ITEMS_PATH
codex-expert-kit/rag/indexes/knowledge_items.json
search_expert_knowledge
get_knowledge_item
get_conflict_audit
get_source_profile
list_kb_partitions
browse_knowledge_tree
```

## 输出契约

### README

根 `README.md` 必须包含：

```text
项目定位
当前知识库基线
5 分钟外部项目接入
MCP/RAG 最小配置
本地验证命令
reviewed / approved / caveat_only 边界
文档入口
```

### Quickstart

`docs/external_mcp_quickstart.md` 必须包含：

```text
适用对象
前置条件
最小接入步骤
.codex/config.toml 示例
环境变量说明
server.py CLI 验证命令
search_expert_knowledge 请求示例
get_knowledge_item 请求示例
常见错误和排查
权限边界
验收清单
```

### MCP Spec

`mcp_server_spec.md` 必须对齐：

```text
当前 server version
tool list 包含 browse_knowledge_tree
正式索引默认路径
CLI 调试方式
read-only 权限边界
reviewed/caveat_only 返回语义
approved/default guidance 返回语义
```

## 边界范围

范围内：

```text
1. 文档入口清晰化。
2. README、接入指南、MCP spec、配置模板注释更新。
3. 增加外部 MCP quickstart 文档。
4. 运行 MCP smoke test 和 UTF-8 乱码检查。
5. 更新任务索引。
```

范围外：

```text
1. 不改变 MCP tool 权限。
2. 不改 server.py 行为。
3. 不改正式知识内容。
4. 不新增专业知识。
5. 不引入数据库、后端框架或外部服务。
6. 不改变 Vue3 信息架构。
7. 不把 reviewed 升级为 approved。
8. 不启用 default guidance 或 hard gate。
```

## 涉及组件

```text
README.md
docs/external_mcp_quickstart.md
docs/其他项目接入指南.md
codex-expert-kit/mcp/mcp_server_spec.md
codex-expert-kit/templates/codex_config_mcp.toml
docs/index_tasks.md
docs/tasks/README.md
```

## 涉及数据结构

```text
MCP config
MCP request JSON
MCP normalized response
Project Adapter
External Project Healthcheck
KnowledgeItem review_status / machine_gate
```

## 涉及数据库/存储

不涉及数据库，不改变存储。继续使用正式聚合索引：

```text
codex-expert-kit/rag/indexes/knowledge_items.json
```

## 实施步骤

```text
1. 创建 Phase 56 任务卡并更新索引。
2. 重写 README，增加外部调用最短路径。
3. 新增 docs/external_mcp_quickstart.md。
4. 在 docs/其他项目接入指南.md 顶部增加快速入口和跳转。
5. 更新 mcp_server_spec.md，使其与 server.py、Phase 21/55 基线一致。
6. 更新 codex_config_mcp.toml 注释。
7. 运行 MCP CLI smoke test、文档关键字检查、UTF-8 乱码检查。
8. 生成 Phase 56 验收报告。
9. 更新任务状态。
```

## Definition of Done

```text
1. Phase 56 任务卡存在并写入 docs/index_tasks.md 和 docs/tasks/README.md。
2. README 包含外部项目 5 分钟接入步骤。
3. docs/external_mcp_quickstart.md 存在。
4. docs/其他项目接入指南.md 能在顶部看到 MCP 快速入口。
5. mcp_server_spec.md 与当前 server.py tool list 和 CLI 参数一致。
6. codex_config_mcp.toml 说明 enabled=false 到 true 的启用条件。
7. MCP --info、--list-tools、--call smoke test 通过。
8. validate_no_mojibake.py 通过。
9. 文档不把本机绝对路径写成必须依赖，示例路径必须说明可替换为 CEK_TA_ROOT。
10. 不改变 MCP 权限和知识状态。
11. Phase 56 验收报告存在。
12. 任务状态已更新。
```

## 测试与验收

必须执行：

```text
python codex-expert-kit/mcp/server.py --info
python codex-expert-kit/mcp/server.py --list-tools
python codex-expert-kit/mcp/server.py --call search_expert_knowledge --request-json "{\"query\":\"backtest data leakage\",\"top_k\":2}"
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
```

建议执行：

```text
pytest codex-expert-kit/mcp/tests/test_server_runtime.py
python codex-expert-kit/rag/scripts/validate_phase55_runtime_acceptance.py
```

## 风险与回滚

风险：

```text
1. 文档过长，用户仍找不到最小接入路径。
2. 示例路径让用户误以为必须使用本机绝对路径。
3. MCP spec 如果写过度，会被误认为开放写权限。
```

回滚：

```text
1. 本 Phase 只改文档和模板注释，可按文件回退。
2. 如 quickstart 误导用户，保留完整接入指南作为权威说明并修正 quickstart。
3. 如 MCP spec 与代码不一致，以 server.py 和测试为准，重新修订文档。
```

## 需要开发者确认的问题

```text
1. 是否需要把 docs/external_mcp_quickstart.md 后续同步到插件/Skill 包。
2. 是否需要为不同外部项目类型提供多个 quickstart 变体。
3. 是否需要把 README 的“5 分钟接入”压缩到更短的命令清单。
```
