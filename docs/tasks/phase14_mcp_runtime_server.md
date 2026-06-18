# Phase 14: Knowledge MCP 运行时服务任务卡

## Phase 目标

把 Phase 3 的 MCP 工具草案升级为可运行、可测试、可被其他项目配置调用的 Knowledge MCP 服务，同时保持只读优先、来源可追踪、权限边界明确。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-056 | P0 | done | 实现 MCP server 入口 | `codex-expert-kit/mcp/server.py` |
| CEK-TA-057 | P0 | done | 对齐 MCP tools 与 RAG 数据层 | `codex-expert-kit/mcp/*.py` |
| CEK-TA-058 | P1 | done | 增加 MCP 运行时测试与示例配置 | `codex-expert-kit/mcp/tests/`、`codex-expert-kit/templates/codex_config_mcp.toml` |

## 上游输入

```text
codex-expert-kit/mcp/mcp_server_spec.md
codex-expert-kit/mcp/search_expert_knowledge.py
codex-expert-kit/rag/search_result_contract.md
codex-expert-kit/rag/storage_layout.md
codex-expert-kit/rag/examples/
codex-expert-kit/templates/codex_config_mcp.toml
```

## 下游输出

```text
外部项目 Codex MCP 配置
Vue3 API/MCP adapter
知识树浏览工具
检索测试台
知识质量评测
```

## 输入契约

MCP tool 输入必须显式定义：

```text
query
domain
tree_node_id
project_adapter
review_status_filter
include_conflicts
limit
```

## 输出契约

MCP tool 输出必须包含：

```text
ok
data
sources
confidence
warnings
errors
trace_id
```

## 边界范围

范围内：

```text
实现本地 MCP server 入口
加载本地文件化 RAG 数据
暴露只读查询工具
暴露 proposed 级回灌提交工具时必须单独确认权限
提供测试样例
```

范围外：

```text
不连接真实交易账户
不读取密钥
不下单
不修改 approved 知识
不默认启用写入型工具
不引入外部服务依赖，除非开发者确认
```

## 涉及组件

```text
codex-expert-kit/mcp/
codex-expert-kit/rag/
codex-expert-kit/templates/codex_config_mcp.toml
docs/其他项目接入指南.md
```

## 涉及数据结构

```text
McpToolInput
McpToolOutput
KnowledgeSearchRequest
KnowledgeSearchResponse
ProjectRelevantKnowledgeRequest
McpError
```

## 涉及数据库/存储

读取 Phase 13 定义的本地文件化知识数据层。MCP server 不直接拥有数据库迁移职责。

## 实施步骤

1. 选择最小可运行 MCP server 入口实现方式。
2. 实现 `server.py`。
3. 对齐现有 tool 的输入输出结构。
4. 增加知识树浏览工具草案。
5. 增加运行时测试。
6. 更新 MCP 配置示例。
7. 更新外部项目接入指南。

## Definition of Done

```text
server.py 存在并可运行
核心只读工具可调用
返回值包含 source、confidence、warnings、trace_id
错误输入有明确错误结构
MCP 配置示例可追踪到真实入口
不暴露实盘和密钥能力
UTF-8 中文无乱码
```

## 测试与验收

```text
运行 MCP 单元测试或脚本测试
测试 search_expert_knowledge 正常输入
测试空 query
测试未知 domain
测试缺失数据目录
测试配置文件路径
检查中文输出无乱码
```

## 风险与回滚

风险：

```text
MCP SDK 或运行方式变化
工具权限边界不清
路径配置在不同项目中失效
```

回滚：

```text
保留 Phase 3 单文件工具草案
server.py 可独立禁用
模板配置默认 disabled
```

## 需要开发者确认的问题

```text
是否允许引入 MCP SDK 依赖
是否允许暴露 submit_knowledge_contribution
是否需要把 server.py 作为默认启用入口
```

## 状态更新要求

完成后更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase14_mcp_runtime_server.md
```

## 完成记录

```text
completed_at: 2026-06-08
status: done
```

已完成：

```text
1. 创建 dependency-free 的 `server.py` 本地运行时入口。
2. 支持 CLI 调用、工具列表、JSON-RPC-like stdio loop。
3. 只暴露只读工具：search_expert_knowledge、get_knowledge_item、get_conflict_audit、get_source_profile、list_kb_partitions、browse_knowledge_tree。
4. 新增知识树浏览工具 `browse_knowledge_tree.py`。
5. 对齐 Phase 13 文件化样例数据和 tree_node_id/tree_path 检索。
6. 增加运行时测试。
7. 更新 MCP 配置示例和其他项目接入指南。
```

边界说明：

```text
1. 未引入 MCP SDK 或任何外部依赖。
2. 未暴露 submit_knowledge_contribution。
3. 未默认启用业务项目 MCP 配置，模板仍为 enabled = false。
4. 不读取密钥、账户数据、原始订单，不下单，不写 approved 知识。
```

测试：

```text
1. python codex-expert-kit/mcp/server.py --list-tools
2. search_expert_knowledge 正常输入
3. search_expert_knowledge 空 query
4. place_order 禁止工具
5. browse_knowledge_tree 树节点浏览
6. --request-file UTF-8 JSON 请求文件
7. pytest codex-expert-kit/mcp/tests/test_server_runtime.py
```
