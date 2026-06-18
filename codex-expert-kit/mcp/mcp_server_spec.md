# CEK-TA Knowledge MCP Server Spec

本文定义 CEK-TA 知识 MCP 运行时契约。当前运行时入口是：

```text
codex-expert-kit/mcp/server.py
```

该服务是只读专业知识访问层。它不得交易、下单、读取密钥、读取账户、修改业务项目状态、写入知识或批准知识。

## Server Identity

```yaml
name: cek-ta-knowledge-mcp
version: 0.2.0
mode: read_only
encoding: UTF-8
default_index: codex-expert-kit/rag/indexes/knowledge_items.json
purpose: >
  让外部项目通过 MCP 查询 CEK-TA 正式知识库，获得适用范围、来源、置信度、
  freshness、review_status、conflict_status 和 machine_gate。
```

## 上游契约

```text
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/conflict_detection_rules.md
codex-expert-kit/rag/source_quality_rules.md
codex-expert-kit/rag/retrieval_policy.md
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/core/path_resolver.py
```

## 路径解析规则

运行时不得依赖开发机绝对路径。

优先级：

```text
1. CEK_TA_KNOWLEDGE_ITEMS_PATH 指定的正式知识索引。
2. 通过 path_resolver 定位 codex-expert-kit/rag/indexes/knowledge_items.json。
3. 如果正式索引不存在，才回退到 sample_knowledge_items.json。
```

外部项目推荐设置：

```powershell
$env:CEK_TA_ROOT = "替换为你的 CEK-TA 根目录"
$env:CEK_TA_KNOWLEDGE_ITEMS_PATH = "$env:CEK_TA_ROOT\codex-expert-kit\rag\indexes\knowledge_items.json"
```

## CLI 用法

```text
python codex-expert-kit/mcp/server.py --info
python codex-expert-kit/mcp/server.py --list-tools
python codex-expert-kit/mcp/server.py --call <tool_name> --request-json <json>
python codex-expert-kit/mcp/server.py --call <tool_name> --request-file <path>
python codex-expert-kit/mcp/server.py --knowledge-items-path <path>
```

示例：

```powershell
python codex-expert-kit/mcp/server.py --call search_expert_knowledge --request-json "{\"query\":\"lookahead bias\",\"top_k\":3}"
```

## JSON-RPC 方法

stdio 模式支持：

```text
initialize
tools/list
tools/call
```

`tools/call` 参数：

```json
{
  "name": "search_expert_knowledge",
  "arguments": {
    "query": "lookahead bias",
    "top_k": 3
  }
}
```

## Permission Model

默认权限：

```yaml
read_knowledge: true
read_sources: true
read_conflict_status: true
read_project_private_data: false
write_knowledge: false
approve_knowledge: false
submit_contribution: false
trade: false
read_account: false
read_secret: false
```

禁止能力：

```text
submit_knowledge_contribution
approve_knowledge_item
write_approved_knowledge
place_order
read_project_secrets
read_account_data
```

规则：

```text
1. MCP 工具默认只读。
2. 不暴露密钥、API key、账户数据、原始订单或业务项目私有事实。
3. project_context 只能作为过滤或解释上下文，不能写成 CEK-TA 新知识。
4. reviewed/caveat_only 可用于审计和检索，但不等于 approved。
5. rejected 不得作为普通指导返回。
6. confirmed unresolved conflict 必须阻断权威指导。
7. default guidance 和 hard gate 必须由 knowledge item 的 review / machine_gate 字段决定。
```

## Tool List

当前运行时暴露：

```text
search_expert_knowledge
get_knowledge_item
get_conflict_audit
get_source_profile
list_kb_partitions
browse_knowledge_tree
```

## Common Input Fields

```json
{
  "request_id": "string | null",
  "trace_id": "string | null",
  "project_context": {
    "project_name": "string | null",
    "project_type": "string | null",
    "market": "crypto | futures | spot | stock | general | null",
    "asset": "BTC | ETH | multi | general | null",
    "timeframe": "tick | 1s | 1m | 3m | 15m | 1h | 4h | 1d | general | null",
    "data_granularity": "tick | trade | order_book | second | kline | account_event | general | null"
  },
  "include": {
    "sources": true,
    "conflicts": true,
    "deprecated": false,
    "draft": false,
    "reviewed": true
  }
}
```

## Common Runtime Output Wrapper

`server.py --call` 会把工具结果包装成统一结构：

```json
{
  "ok": true,
  "tool": "search_expert_knowledge",
  "status": "ok",
  "data": {},
  "sources": [],
  "confidence": "high | medium | low | \"\"",
  "warnings": [],
  "errors": [],
  "trace_id": "string"
}
```

## Error Schema

```json
{
  "code": "invalid_input | unsupported_filter | permission_denied | retrieval_failed | storage_unavailable | conflict_blocked | freshness_recheck_required | not_found",
  "message": "string",
  "field": "string | null",
  "details": {}
}
```

## Tool: search_expert_knowledge

用途：按自然语言和结构化过滤条件搜索 CEK-TA 正式知识。

输入：

```json
{
  "query": "string",
  "filters": {
    "partition_id": ["string"],
    "domain": ["string"],
    "subdomain": ["string"],
    "review_status": ["approved", "reviewed"],
    "conflict_status": ["none", "resolved", "potential"],
    "source_type": ["string"]
  },
  "project_context": {},
  "include": {
    "sources": true,
    "conflicts": true,
    "reviewed": true,
    "deprecated": false
  },
  "top_k": 5
}
```

输出重点字段：

```text
results[].knowledge_id
results[].title
results[].summary
results[].source_refs
results[].review_status
results[].conflict_status
results[].machine_gate
warnings
errors
audit
```

## Tool: get_knowledge_item

用途：按 `knowledge_id` 读取单条正式知识。

输入：

```json
{
  "knowledge_id": "string",
  "include": {
    "sources": true,
    "conflicts": true
  }
}
```

输出重点字段：

```text
item
item.source_evidence
item.review
item.machine_gate
item.conflict_audit
errors
```

## Tool: get_conflict_audit

用途：读取单条知识或范围的冲突审计结果。

输入：

```json
{
  "knowledge_id": "string | null",
  "scope": "string | null"
}
```

## Tool: get_source_profile

用途：读取来源证据画像。

输入：

```json
{
  "knowledge_id": "string | null",
  "source_id": "string | null"
}
```

## Tool: list_kb_partitions

用途：列出知识库分区。

输入：

```json
{
  "include_domains": true
}
```

## Tool: browse_knowledge_tree

用途：按节点、父节点、路径前缀或 domain 浏览知识树。

输入：

```json
{
  "node_id": "string | null",
  "parent_id": "string | null",
  "tree_path_prefix": "string | null",
  "domain": "string | null",
  "include_children": true
}
```

## 测试用例

最小 smoke：

```powershell
python codex-expert-kit/mcp/server.py --info
python codex-expert-kit/mcp/server.py --list-tools
python codex-expert-kit/mcp/server.py --call search_expert_knowledge --request-json "{\"query\":\"lookahead bias\",\"top_k\":3}"
```

权限阻断：

```powershell
python codex-expert-kit/mcp/server.py --call place_order --request-json "{}"
```

预期返回 `permission_denied`。
