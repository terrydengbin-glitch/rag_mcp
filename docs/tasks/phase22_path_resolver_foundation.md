# Phase 22: Path Resolver 移植复用地基任务卡

## Phase 目标

建立 CEK-TA 的路径解析地基，要求核心脚本、MCP 运行时、外部项目接入配置和后续开发规则都通过 resolver 定位项目根目录与内部文件，不再依赖硬编码绝对路径。该任务解决项目迁移、Git submodule、团队复用、不同磁盘路径和 CI 环境下路径失效的问题。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-091 | P0 | done | 定义并实现 CEK-TA path resolver | `codex-expert-kit/core/path_resolver.py` |
| CEK-TA-092 | P0 | done | 让 MCP server 使用 resolver 定位根目录和正式知识索引 | `codex-expert-kit/mcp/server.py` |
| CEK-TA-093 | P0 | done | 让正式知识索引生成脚本使用 resolver | `codex-expert-kit/rag/scripts/build_knowledge_items_index.py` |
| CEK-TA-094 | P0 | done | 把路径 resolver 规则写入 AGENTS.md 和知识库 | `AGENTS.md`、`codex-expert-kit/rag/knowledge/KB_10_PROJECT_RUNBOOKS/*.json` |
| CEK-TA-095 | P1 | done | 更新外部接入说明、MCP 配置和测试 | `docs/其他项目接入指南.md`、`codex-expert-kit/templates/codex_config_mcp.toml`、`codex-expert-kit/core/tests/`、`codex-expert-kit/mcp/tests/` |
| CEK-TA-096 | P1 | done | 生成 Phase 22 验收报告并重建正式知识索引 | `docs/reports/path_resolver_foundation_report.md`、`codex-expert-kit/rag/indexes/knowledge_items.json` |

## 上游输入

```text
AGENTS.md
docs/其他项目接入指南.md
codex-expert-kit/mcp/server.py
codex-expert-kit/rag/scripts/build_knowledge_items_index.py
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/indexes/knowledge_items.json
```

## 下游输出

```text
所有后续代码任务的路径开发规则
MCP runtime 默认路径解析
正式知识索引生成路径解析
外部项目接入和迁移复用规则
正式知识库中的开发规则知识项
```

## 输入契约

path resolver 输入：

```text
start_file: 当前模块或脚本文件路径，可选
CEK_TA_ROOT: 可选环境变量，显式指定 CEK-TA 根目录
relative parts: 从项目根目录开始的相对路径片段
```

## 输出契约

path resolver 输出：

```text
resolve_project_root() -> pathlib.Path
resolve_repo_path(*parts) -> pathlib.Path
```

`resolve_project_root()` 必须按优先级解析：

```text
1. CEK_TA_ROOT 环境变量，如果存在且包含 AGENTS.md 和 codex-expert-kit/
2. 从 start_file 或当前文件向上查找，直到发现 AGENTS.md、docs/index_tasks.md、codex-expert-kit/
3. 解析失败时抛出 ValueError，不静默返回错误路径
```

## 边界范围

范围内：

```text
新增 resolver
改 MCP server 和正式索引脚本使用 resolver
新增测试
新增知识库规则
更新开发规范和接入说明
重建正式知识聚合索引
```

范围外：

```text
不重构全部历史文档中的示例绝对路径
不引入外部路径库
不改变 MCP 权限
不引入数据库、后端服务或外部服务
不修改业务项目本身
```

## 涉及组件

```text
codex-expert-kit/core/path_resolver.py
codex-expert-kit/core/tests/test_path_resolver.py
codex-expert-kit/mcp/server.py
codex-expert-kit/mcp/tests/test_server_runtime.py
codex-expert-kit/rag/scripts/build_knowledge_items_index.py
codex-expert-kit/rag/knowledge/KB_10_PROJECT_RUNBOOKS/
AGENTS.md
docs/其他项目接入指南.md
codex-expert-kit/templates/codex_config_mcp.toml
```

## 涉及数据结构

```text
PathResolver
KnowledgeItem
FormalKnowledgeItemsIndex
McpServerInfo
```

## 涉及数据库/存储

```text
只涉及文件路径解析和文件化 JSON 索引。
不引入数据库。
不做迁移。
```

## Definition of Done

```text
resolver 存在且有测试
MCP server 使用 resolver 定位根目录
正式索引脚本使用 resolver 定位根目录
AGENTS.md 写入路径 resolver 开发规则
正式知识库新增路径 resolver 规则知识项
knowledge_items.json 重新生成并包含该知识项
MCP 默认查询能检索到 path resolver 规则
pytest 通过
UTF-8 中文无乱码
```

## 测试与验收

必须执行：

```text
pytest codex-expert-kit/core/tests
pytest codex-expert-kit/mcp/tests
python codex-expert-kit/rag/scripts/build_knowledge_items_index.py
python codex-expert-kit/mcp/server.py --info
python codex-expert-kit/mcp/server.py --call search_expert_knowledge --request-file <path resolver request>
UTF-8 no mojibake scan
```

## 风险与回滚

风险：

```text
错误 resolver 可能导致 MCP 找不到正式索引。
环境变量 CEK_TA_ROOT 指向错误目录时会导致路径误解析。
历史示例仍有绝对路径，可能让使用者误解为必须写死路径。
```

回滚：

```text
resolver 失败时回滚 server.py 和 build 脚本到原有 parents 推导。
删除新增知识项后重新生成 knowledge_items.json。
保留 CEK_TA_ROOT 作为显式覆盖方式。
```

## 状态更新要求

完成后更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase22_path_resolver_foundation.md
README.md
```

## 进度记录

```yaml
current_status: done
completed_tasks:
  - CEK-TA-091
  - CEK-TA-092
  - CEK-TA-093
  - CEK-TA-094
  - CEK-TA-095
  - CEK-TA-096
in_progress_tasks: []
remaining_tasks: []
deliverables:
  - codex-expert-kit/core/path_resolver.py
  - codex-expert-kit/core/tests/test_path_resolver.py
  - codex-expert-kit/mcp/server.py
  - codex-expert-kit/rag/scripts/build_knowledge_items_index.py
  - AGENTS.md
  - codex-expert-kit/rag/knowledge/KB_10_PROJECT_RUNBOOKS/kb_10_project_runbooks.path_resolver.portable_paths.v1.json
  - codex-expert-kit/rag/indexes/knowledge_items.json
  - docs/reports/path_resolver_foundation_report.md
notes:
  - 本阶段不改变 MCP 权限。
  - 本阶段不引入数据库、后端框架或外部服务。
```
