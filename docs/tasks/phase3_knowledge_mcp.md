# Phase 3 Knowledge MCP 任务卡

## Phase 目标

建立 CEK-TA Knowledge MCP 的只读服务规格，让 Codex 在其他交易、回测、模拟盘、实盘风控、LLM、RAG 项目中，可以通过 MCP 查询 CEK-TA 专业知识，并且每次返回都携带来源、适用边界、置信度、时效性、审计状态和冲突状态。

Phase 3 的关键目标不是先做复杂实现，而是先把 MCP tool 契约写清楚，避免后续接入项目时出现权限、返回字段、冲突处理和审计责任不明确的问题。

## 任务列表

| ID | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- |
| CEK-TA-010 | done | 编写 MCP server 规格 | `codex-expert-kit/mcp/mcp_server_spec.md` |
| CEK-TA-011 | done | 实现 `search_expert_knowledge` 草案 | `codex-expert-kit/mcp/search_expert_knowledge.py` |
| CEK-TA-012 | done | 实现 adapter/reason_code 查询草案 | `codex-expert-kit/mcp/get_*.py` |

## 上游输入

```text
codex-expert-kit/rag/kb_partitions.md
codex-expert-kit/rag/metadata_schema.md
codex-expert-kit/rag/chunking_rules.md
codex-expert-kit/rag/retrieval_policy.md
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/conflict_detection_rules.md
codex-expert-kit/rag/source_quality_rules.md
docs/其他项目接入指南.md
docs/知识倒灌与反哺规范.md
```

## 下游输出

```text
Phase 8 其他项目接入:
  使用 MCP server 规格生成业务项目的 Codex MCP 配置和 AGENTS.md 接入说明。

Phase 7 Vue3 知识审计界面:
  使用 MCP 输出契约展示检索结果、来源、冲突、freshness 和审计状态。

Phase 9 知识倒灌与反哺:
  使用只读查询结果判断候选贡献是否与现有知识冲突。

业务项目 Codex:
  在任务执行前查询 CEK-TA 专业知识，而不是把全部知识硬塞进上下文。
```

## 输入契约

MCP 查询输入必须包含：

```text
query
task_type
project_context
filters
top_k
include
```

其中 `project_context` 只能用于过滤适用范围，不允许把业务项目私有字段写入 CEK-TA 通用知识。

## 输出契约

MCP 返回必须包含：

```text
results
warnings
applied_filters
audit
errors
```

每条 result 必须携带：

```text
knowledge_id
title
partition_id
domain
subdomain
summary
source
confidence
freshness
review_status
conflict_status
applicability
score
```

## 边界范围

本 Phase 做：

```text
1. 定义 MCP server 的只读工具集合。
2. 定义 tool 输入、输出、错误、权限、限流和测试。
3. 定义检索结果如何处理来源、冲突、freshness 和 project_binding。
4. 为后续 Python 草案实现提供契约。
```

本 Phase 不做：

```text
1. 不引入数据库。
2. 不引入新的后端框架。
3. 不写入或修改知识库内容。
4. 不提供实盘交易、下单、账户、密钥、资金相关能力。
5. 不把项目私有事实提升为通用知识。
6. 不改变现有 MCP 权限原则，默认只读。
```

## 涉及组件

```text
docs/tasks/phase3_knowledge_mcp.md
codex-expert-kit/mcp/mcp_server_spec.md
codex-expert-kit/mcp/search_expert_knowledge.py
codex-expert-kit/mcp/get_*.py
codex-expert-kit/templates/codex_config_mcp.toml
```

## 涉及数据结构

```text
mcp_request
mcp_response
knowledge_result
source_citation
applicability_filter
audit_warning
error_response
```

## 涉及数据库/存储

当前 Phase 不引入数据库。MCP server 规格只定义查询契约；真实数据源可以是 RAGFlow、向量库、Markdown 索引或后续实现的存储层，但必须在后续实现任务中单独定义数据源适配契约。

## 实施步骤

```text
1. 创建 Phase 3 任务卡。
2. 编写 mcp_server_spec.md。
3. 更新 docs/index_tasks.md：Phase 3 标记 done，CEK-TA-010 标记 done。
4. 更新 docs/tasks/README.md：Phase 3 任务卡标记 done。
5. 更新 codex-expert-kit/README.md 的 MCP 入口。
6. 执行文件存在性、关键章节、UTF-8、索引状态检查。
7. 实现 search_expert_knowledge.py 草案。
8. 实现 get_knowledge_item.py、get_conflict_audit.py、get_source_profile.py、list_kb_partitions.py 草案。
9. 执行 Python 编译和函数级契约测试。
```

## Definition of Done

```text
1. Phase 3 任务卡存在，并包含上下游、契约、边界、DoD 和测试。
2. mcp_server_spec.md 存在。
3. MCP server 规格包含 name、purpose、input schema、output schema、error schema、permissions、rate limit、test cases。
4. MCP 权限默认为只读，不包含写入、交易、账户、密钥能力。
5. 返回契约包含 source/citation/confidence/freshness/review_status/conflict_status。
6. docs/index_tasks.md、docs/tasks/README.md、Phase 任务卡状态一致。
7. 中文文档 UTF-8 读取无乱码。
8. search_expert_knowledge.py 可处理 valid search、empty query、permission denied、unsupported filter。
9. get_*.py 查询草案可按 knowledge_id、source_id、scope 和 partitions 返回只读结果。
```

## 测试与验收

```text
1. Test-Path 检查任务卡和 mcp_server_spec.md 存在。
2. Select-String 检查 MCP 规格关键章节。
3. 检查 Phase 3 在索引中为 done。
4. 检查 CEK-TA-010、CEK-TA-011 和 CEK-TA-012 均为 done。
5. Get-Content -Encoding UTF8 检查中文文档无乱码。
6. python -m py_compile 检查 MCP Python 草案语法。
7. 用样例 knowledge_item 执行 search/get/list 函数级测试。
```

## 风险与回滚

风险：

```text
1. MCP 输出过宽会导致外部项目误用 draft 或 conflict 知识。
2. MCP 权限过宽会破坏支持层边界。
3. 如果数据源契约不清楚，后续实现会把 RAG、Markdown、数据库逻辑混在一起。
```

回滚：

```text
1. 文档规格可通过版本控制回退。
2. 若后续实现发现字段不足，新增 schema version，不破坏旧字段。
3. 如需要改变 MCP 权限，必须新开决策问题让开发者确认。
```

## 需要开发者确认的问题

当前只定义只读 MCP 规格，不引入数据库、后端框架、外部服务，也不改变权限原则，因此无需确认。

后续如要：

```text
1. 连接真实 RAGFlow 服务。
2. 引入数据库或向量库。
3. 增加写入、审计动作、倒灌提交类 MCP tool。
4. 改变 MCP 权限。
```

必须先向开发者确认。

## 状态更新要求

完成 Phase 3 后必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase3_knowledge_mcp.md
codex-expert-kit/README.md
```
