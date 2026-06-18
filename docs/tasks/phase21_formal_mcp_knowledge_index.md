# Phase 21: MCP 正式知识聚合索引任务卡

## Phase 目标

生成正式 `codex-expert-kit/rag/indexes/knowledge_items.json` 聚合索引，让其他项目通过 MCP 默认读取 Phase 17 以后沉淀的正式知识库，而不是回退到 sample 数据；同时更新 MCP 示例配置、接入说明和运行时测试，确保外部项目可以稳定通过只读 MCP 调用正式知识。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-086 | P0 | done | 创建正式知识聚合索引生成脚本 | `codex-expert-kit/rag/scripts/build_knowledge_items_index.py` |
| CEK-TA-087 | P0 | done | 生成正式 `knowledge_items.json` | `codex-expert-kit/rag/indexes/knowledge_items.json` |
| CEK-TA-088 | P0 | done | 更新 MCP 默认路径测试 | `codex-expert-kit/mcp/tests/test_server_runtime.py` |
| CEK-TA-089 | P1 | done | 更新 MCP 示例配置和外部接入说明 | `codex-expert-kit/templates/codex_config_mcp.toml`、`docs/其他项目接入指南.md` |
| CEK-TA-090 | P1 | done | 生成 Phase 21 验收报告 | `docs/reports/formal_mcp_knowledge_index_report.md` |

## 上游输入

```text
codex-expert-kit/rag/knowledge/**/*.json
codex-expert-kit/rag/indexes/
codex-expert-kit/mcp/server.py
codex-expert-kit/mcp/common.py
codex-expert-kit/templates/codex_config_mcp.toml
docs/其他项目接入指南.md
docs/reports/searchlab_mcp_runtime_quality_report.md
```

## 下游输出

```text
其他项目 MCP 默认查询正式知识库
server.py --info 显示 formal knowledge_items.json
search_expert_knowledge 默认命中 Phase 17 seed 知识
get_knowledge_item / get_source_profile / get_conflict_audit 默认读取正式知识
后续知识入库后的可重复索引生成流程
```

## 输入契约

正式知识文件必须位于：

```text
codex-expert-kit/rag/knowledge/**/*.json
```

每个知识文件必须是 UTF-8 JSON object，并至少包含：

```text
knowledge_id
metadata.partition_id
metadata.domain
metadata.tree_node_id
source_evidence
review.review_status
review.freshness
conflict_audit.conflict_status
applicability.applies_when
applicability.not_applicable_when
```

## 输出契约

`knowledge_items.json` 必须是 MCP `load_knowledge_items` 可读取的 object：

```json
{
  "schema": "cek_ta_knowledge_items_index",
  "schema_version": "1.0.0",
  "generated_at": "YYYY-MM-DD",
  "source_root": "codex-expert-kit/rag/knowledge",
  "item_count": 10,
  "items": []
}
```

`items[]` 保留完整知识条目，不做压缩、不删字段。

## 边界范围

范围内：

```text
生成正式知识聚合索引
更新 MCP 默认路径验证
更新外部项目示例配置
验证默认 MCP 查询正式知识
```

范围外：

```text
不引入数据库
不引入向量数据库
不改变 MCP 权限
不新增写入型 MCP tool
不联网采集新知识
不修改已 approved 知识内容
不改变知识 schema
```

## 涉及组件

```text
codex-expert-kit/rag/scripts/build_knowledge_items_index.py
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/indexes/README.md
codex-expert-kit/mcp/server.py
codex-expert-kit/mcp/tests/test_server_runtime.py
codex-expert-kit/templates/codex_config_mcp.toml
docs/其他项目接入指南.md
```

## 涉及数据结构

```text
FormalKnowledgeItemsIndex
KnowledgeItem
McpServerInfo
McpSearchResponse
```

## 涉及数据库/存储

```text
只使用文件化 JSON 聚合索引。
不引入数据库。
不做迁移。
```

## 实施步骤

1. 创建 `build_knowledge_items_index.py`。
2. 从 `rag/knowledge/**/*.json` 读取正式知识。
3. 校验 `knowledge_id` 唯一。
4. 按 `knowledge_id` 排序后写入 `rag/indexes/knowledge_items.json`。
5. 更新 `rag/indexes/README.md`。
6. 更新 MCP server 测试，确认默认路径指向 formal index。
7. 更新 `codex_config_mcp.toml` 和 `docs/其他项目接入指南.md`。
8. 运行 MCP tests。
9. 生成验收报告。
10. 更新索引和任务状态。

## Definition of Done

```text
Phase 21 任务卡存在并已索引
生成脚本存在
knowledge_items.json 存在且 item_count 为正式知识数量
MCP --info 默认路径指向 knowledge_items.json
默认 search_expert_knowledge 能命中正式 seed 知识
只读权限阻断测试继续通过
示例配置不再误导用户使用 sample 数据
不改变 MCP 权限
pytest 通过
UTF-8 中文无乱码
```

## 测试与验收

必须执行：

```text
python codex-expert-kit/rag/scripts/build_knowledge_items_index.py
python codex-expert-kit/mcp/server.py --info
python codex-expert-kit/mcp/server.py --call search_expert_knowledge --request-file <formal request>
pytest codex-expert-kit/mcp/tests
JSON parse check for knowledge_items.json
UTF-8 no mojibake scan
```

关键断言：

```text
1. knowledge_items.json item_count == 10。
2. server.py --info knowledge_items_path 指向 rag/indexes/knowledge_items.json。
3. 默认 MCP 查询 `OHLC same bar take profit stop loss fill model` 命中 `kb_04_backtest.fill_model.ohlc_same_bar_path_ambiguity.v1`。
4. requested_permission=trade 仍然 permission_denied。
```

## 风险与回滚

风险：

```text
聚合索引变旧，新增知识后未重新生成。
聚合索引过大后 CLI 读取性能下降。
正式知识 JSON 中如有重复 knowledge_id，会导致 MCP 结果不确定。
```

回滚：

```text
删除或重命名 knowledge_items.json 后，server.py 会回退到 sample 数据。
如正式索引生成失败，不改动 server.py 权限和工具。
如发现重复 knowledge_id，停止生成并修复源知识文件。
```

## 状态更新要求

完成后更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase21_formal_mcp_knowledge_index.md
README.md
```

## 进度记录

```yaml
current_status: done
completed_tasks:
  - CEK-TA-086
  - CEK-TA-087
  - CEK-TA-088
  - CEK-TA-089
  - CEK-TA-090
in_progress_tasks: []
remaining_tasks: []
deliverables:
  - codex-expert-kit/rag/scripts/build_knowledge_items_index.py
  - codex-expert-kit/rag/indexes/knowledge_items.json
  - codex-expert-kit/rag/indexes/README.md
  - codex-expert-kit/mcp/tests/test_server_runtime.py
  - codex-expert-kit/templates/codex_config_mcp.toml
  - docs/其他项目接入指南.md
  - docs/reports/formal_mcp_knowledge_index_report.md
notes:
  - 本阶段没有改变 MCP 权限。
  - 本阶段没有引入数据库、后端框架或外部服务。
```
