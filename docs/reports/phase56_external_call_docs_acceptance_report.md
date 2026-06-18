# Phase 56 外部调用文档验收报告

```json
{
  "report_id": "phase56_external_call_docs_acceptance_report",
  "generated_at": "2026-06-14",
  "phase": "Phase 56",
  "task_ids": [
    "CEK-TA-541",
    "CEK-TA-542",
    "CEK-TA-543",
    "CEK-TA-544",
    "CEK-TA-545",
    "CEK-TA-546",
    "CEK-TA-547"
  ],
  "gate_status": "pass"
}
```

## 验收范围

本次验收覆盖外部项目调用 CEK-TA 知识库所需的文档入口和 MCP 只读调用说明：

```text
README.md
docs/external_mcp_quickstart.md
docs/其他项目接入指南.md
codex-expert-kit/mcp/mcp_server_spec.md
codex-expert-kit/templates/codex_config_mcp.toml
codex-expert-kit/rag/indexes/README.md
docs/tasks/phase56_external_call_readme_mcp_docs.md
docs/index_tasks.md
docs/tasks/README.md
```

## 文档交付物

```text
1. 根 README 已增加 CEK-TA 项目定位、一分钟 MCP 接入、健康检查、关键文档链接和只读边界。
2. 新增 docs/external_mcp_quickstart.md，覆盖环境变量、MCP smoke、search/get/tree 查询、Codex 配置和常见错误。
3. docs/其他项目接入指南.md 已把 MCP 快速入口前置，并说明 enabled=false 到 enabled=true 的启用时机。
4. codex-expert-kit/mcp/mcp_server_spec.md 已对齐 server.py 当前 0.2.0 运行时、CLI、工具列表、权限和错误结构。
5. codex-expert-kit/templates/codex_config_mcp.toml 已补充健康检查通过前保持 enabled=false 的说明。
6. codex-expert-kit/rag/indexes/README.md 已说明 knowledge_items.json 是 MCP 默认正式知识索引。
```

## MCP CLI 验收

### `--info`

```text
命令：python codex-expert-kit/mcp/server.py --info
结果：pass
确认：name=cek-ta-knowledge-mcp，version=0.2.0，mode=read_only。
```

### `--list-tools`

```text
命令：python codex-expert-kit/mcp/server.py --list-tools
结果：pass
确认：工具包含 search_expert_knowledge、get_knowledge_item、get_conflict_audit、get_source_profile、list_kb_partitions、browse_knowledge_tree。
```

### 查询 smoke

```text
命令：python codex-expert-kit/mcp/server.py --call search_expert_knowledge --request-json '{"query":"lookahead bias","top_k":3}'
结果：pass
ok=True
status=warning
result_count=3
warnings=483
errors=0
```

说明：`status=warning` 来自大量 reviewed 但未 approved 的知识边界提醒，符合 CEK-TA 治理语义，不影响只读查询可用性。

### 权限阻断

```text
命令：python codex-expert-kit/mcp/server.py --call place_order --request-json '{}'
结果：pass
ok=False
status=error
error_code=permission_denied
```

## UTF-8 验收

```text
命令：python codex-expert-kit/rag/scripts/validate_no_mojibake.py
结果：pass
scanned_count=1662
failure_count=0
```

## 路径与启用时机检查

```text
1. 外部项目文档推荐使用 CEK_TA_ROOT。
2. 正式索引可通过 CEK_TA_KNOWLEDGE_ITEMS_PATH 指定。
3. MCP 配置模板保留本机路径作为示例，并明确替换为项目实际路径。
4. README、quickstart 和接入指南均说明健康检查通过后再启用 enabled=true。
5. 运行时代码路径仍由 codex-expert-kit/core/path_resolver.py 负责。
```

## 边界检查

```text
1. 未新增 MCP tool。
2. 未改变 MCP 权限。
3. 未改变 MCP 返回 schema。
4. 未修改正式知识内容。
5. 未把 reviewed 升级 approved。
6. 未启用 default guidance。
7. 未启用 hard gate。
8. 未改变 Vue3 信息架构。
9. 未引入数据库、后端框架或外部服务依赖。
```

## 未完成项

```text
无阻断项。
```

后续如果 MCP 运行时新增工具、参数或返回字段，必须同步更新：

```text
docs/external_mcp_quickstart.md
codex-expert-kit/mcp/mcp_server_spec.md
codex-expert-kit/templates/codex_config_mcp.toml
```
