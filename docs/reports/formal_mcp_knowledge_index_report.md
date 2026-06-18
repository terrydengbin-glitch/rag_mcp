# Formal MCP Knowledge Index Report

## Report Identity

```text
report_id: cek_ta_formal_mcp_knowledge_index_20260608
phase: Phase 21
tested_at: 2026-06-08
scope: formal knowledge_items.json aggregate index and MCP default runtime path
```

## Completed Tasks

| Task | Result | Deliverable |
| --- | --- | --- |
| CEK-TA-086 | done | `codex-expert-kit/rag/scripts/build_knowledge_items_index.py` |
| CEK-TA-087 | done | `codex-expert-kit/rag/indexes/knowledge_items.json` |
| CEK-TA-088 | done | `codex-expert-kit/mcp/tests/test_server_runtime.py` |
| CEK-TA-089 | done | `codex-expert-kit/templates/codex_config_mcp.toml`、`docs/其他项目接入指南.md` |
| CEK-TA-090 | done | `docs/reports/formal_mcp_knowledge_index_report.md` |

## Formal Index

```text
path: codex-expert-kit/rag/indexes/knowledge_items.json
schema: cek_ta_knowledge_items_index
schema_version: 1.0.0
source_root: codex-expert-kit/rag/knowledge
item_count: 11
```

该文件由正式知识目录机械生成：

```text
python codex-expert-kit/rag/scripts/build_knowledge_items_index.py
```

## MCP Runtime Default

`server.py --info` 当前默认返回：

```text
knowledge_items_path: E:\collector\rag\codex-expert-kit\rag\indexes\knowledge_items.json
mode: read_only
```

默认查询不再回退到 sample fixture。

## Runtime Smoke Test

请求：

```text
query: OHLC same bar take profit stop loss fill model
top_k: 5
filters.review_status: approved
```

结果：

```text
matched: kb_04_backtest.fill_model.ohlc_same_bar_path_ambiguity.v1
source_refs: present
review_status: approved
conflict_status: none
recommended_next_action: use_as_guidance
```

## Tests

```text
python codex-expert-kit/rag/scripts/build_knowledge_items_index.py
wrote knowledge_items.json with 11 items

python codex-expert-kit/mcp/server.py --info
pass

python codex-expert-kit/mcp/server.py --call search_expert_knowledge --request-file .tmp_phase21_request.json
pass

pytest codex-expert-kit/mcp/tests
20 passed

knowledge_items.json parse check
item_count: 11
```

## Boundaries

```text
未引入数据库。
未引入后端框架。
未接入外部服务。
未改变 MCP tool 权限。
未新增写入型 MCP tool。
未修改 approved 知识内容。
```

## External Project Impact

其他项目现在可以通过 MCP 默认读取正式知识库。推荐 `.codex/config.toml` 显式配置：

```text
CEK_TA_KNOWLEDGE_ITEMS_PATH = E:\collector\rag\codex-expert-kit\rag\indexes\knowledge_items.json
```

如果不配置该环境变量，只要 `knowledge_items.json` 存在，`server.py` 也会默认使用它。

## Open Gaps

```text
1. 新增或修改正式知识后，需要重新运行 build_knowledge_items_index.py。
2. 当前仍是文件化聚合索引，不是向量数据库。
3. 外部项目健康检查仍需项目侧创建 AGENTS.md 和 docs/project_adapter.md。
```

## DoD Checklist

```text
Phase 21 任务卡存在并已索引: pass
生成脚本存在: pass
knowledge_items.json 存在且 item_count 为 11: pass
MCP --info 默认路径指向 knowledge_items.json: pass
默认 search_expert_knowledge 能命中正式 seed 知识: pass
只读权限阻断测试继续通过: pass
示例配置不再误导用户使用 sample 数据: pass
不改变 MCP 权限: pass
pytest 通过: pass
UTF-8 中文无乱码: pass
```
