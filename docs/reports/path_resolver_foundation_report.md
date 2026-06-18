# Path Resolver Foundation Report

## Report Identity

```text
report_id: cek_ta_path_resolver_foundation_20260608
phase: Phase 22
tested_at: 2026-06-08
scope: portable path resolver, MCP runtime path resolution, formal index generation, development rule knowledge item
```

## Completed Tasks

| Task | Result | Deliverable |
| --- | --- | --- |
| CEK-TA-091 | done | `codex-expert-kit/core/path_resolver.py` |
| CEK-TA-092 | done | `codex-expert-kit/mcp/server.py` |
| CEK-TA-093 | done | `codex-expert-kit/rag/scripts/build_knowledge_items_index.py` |
| CEK-TA-094 | done | `AGENTS.md`、`codex-expert-kit/rag/knowledge/KB_10_PROJECT_RUNBOOKS/kb_10_project_runbooks.path_resolver.portable_paths.v1.json` |
| CEK-TA-095 | done | `docs/其他项目接入指南.md`、`codex-expert-kit/templates/codex_config_mcp.toml`、tests |
| CEK-TA-096 | done | `docs/reports/path_resolver_foundation_report.md`、`codex-expert-kit/rag/indexes/knowledge_items.json` |

## Resolver Contract

```text
resolve_project_root(start_file=None, env_var="CEK_TA_ROOT") -> Path
resolve_repo_path(*parts, start_file=None) -> Path
```

解析优先级：

```text
1. CEK_TA_ROOT 环境变量，且必须是有效 CEK-TA 根目录。
2. 从 start_file 向上查找 AGENTS.md、docs/index_tasks.md、codex-expert-kit/。
3. 失败时抛出 ValueError。
```

## Runtime Integration

MCP server:

```text
server.py 使用 resolve_project_root / resolve_repo_path 定位正式 knowledge_items.json。
server.py --info 当前返回 rag/indexes/knowledge_items.json。
CEK_TA_ROOT 环境变量覆盖路径时，测试通过。
```

正式知识索引生成脚本：

```text
build_knowledge_items_index.py 使用 resolver 定位 rag/knowledge 和 rag/indexes。
重新生成后 item_count: 11。
```

## Knowledge Rule

新增正式知识：

```text
kb_10_project_runbooks.path_resolver.portable_paths.v1
```

该知识已进入：

```text
codex-expert-kit/rag/indexes/knowledge_items.json
```

MCP 查询：

```text
query: path resolver portable paths hardcoded absolute path CEK_TA_ROOT
filters.domain: project_runbooks
matched: kb_10_project_runbooks.path_resolver.portable_paths.v1
source_refs: present
review_status: approved
conflict_status: none
```

## Tests

```text
pytest codex-expert-kit/core/tests
5 passed

pytest codex-expert-kit/mcp/tests
21 passed

python codex-expert-kit/rag/scripts/build_knowledge_items_index.py
wrote knowledge_items.json with 11 items
```

## Boundaries

```text
未引入数据库。
未引入后端框架。
未接入外部服务。
未改变 MCP tool 权限。
未新增写入型 MCP tool。
未重构所有历史文档中的示例绝对路径。
```

## Open Gaps

```text
1. 历史文档中仍可能保留 E:\collector\rag 示例路径，但现在要求说明它只是示例。
2. Node/Vue 构建脚本尚未统一接入 resolver，后续如有运行时路径需求再扩展。
3. Plugin 分发配置后续需要单独验证 resolver 与安装目录的关系。
```

## DoD Checklist

```text
resolver 存在且有测试: pass
MCP server 使用 resolver 定位根目录: pass
正式索引脚本使用 resolver 定位根目录: pass
AGENTS.md 写入路径 resolver 开发规则: pass
正式知识库新增路径 resolver 规则知识项: pass
knowledge_items.json 重新生成并包含该知识项: pass
MCP 默认查询能检索到 path resolver 规则: pass
pytest 通过: pass
UTF-8 中文无乱码: pass
```
