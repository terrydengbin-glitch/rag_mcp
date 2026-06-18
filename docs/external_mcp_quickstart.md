# 外部项目 MCP 快速接入手册

本文给外部项目使用，用来快速验证业务项目是否可以通过 CEK-TA MCP 只读查询正式知识库。

## 适用场景

```text
1. 业务项目希望让 Codex / AI IDE 查询 CEK-TA 专业知识。
2. 项目需要搜索 AI Engineering、Trading Engineering、RAG、MCP、数据库、记忆层等正式知识。
3. 项目只需要读取知识、来源、冲突状态和 machine gate，不需要写入 CEK-TA。
4. 项目准备后续通过知识倒灌流程贡献新知识。
```

不适用：

```text
1. 不用于下单。
2. 不读取账户、密钥或交易所私有配置。
3. 不把候选知识当默认指导。
4. 不自动批准知识。
```

## 目录准备

外部项目推荐保留自己的业务事实，并通过环境变量引用 CEK-TA：

```text
your_project/
├── AGENTS.md
├── docs/
│   └── project_adapter.md
└── src/
```

CEK-TA 可以通过本地路径、Git submodule 或共享目录存在。运行时不要依赖固定盘符。

## 环境变量

PowerShell 示例：

```powershell
$env:CEK_TA_ROOT = "替换为你的 CEK-TA 根目录"
$env:CEK_TA_KNOWLEDGE_ITEMS_PATH = "$env:CEK_TA_ROOT\codex-expert-kit\rag\indexes\knowledge_items.json"
```

说明：

```text
CEK_TA_ROOT: CEK-TA 根目录。
CEK_TA_KNOWLEDGE_ITEMS_PATH: 可选。指定正式知识聚合索引。
```

不设置 `CEK_TA_KNOWLEDGE_ITEMS_PATH` 时，MCP 运行时会优先使用：

```text
codex-expert-kit/rag/indexes/knowledge_items.json
```

## 健康检查

在 CEK-TA 根目录执行：

```powershell
cd $env:CEK_TA_ROOT
python codex-expert-kit/mcp/server.py --info
python codex-expert-kit/mcp/server.py --list-tools
```

预期：

```text
name = cek-ta-knowledge-mcp
version = 0.2.0
mode = read_only
tools 包含 search_expert_knowledge、get_knowledge_item、get_conflict_audit、get_source_profile、list_kb_partitions、browse_knowledge_tree
```

## 查询正式知识

### 搜索知识

```powershell
python codex-expert-kit/mcp/server.py --call search_expert_knowledge --request-json "{\"query\":\"lookahead bias\",\"top_k\":3}"
```

返回结果需要关注：

```text
data.results[].knowledge_id
data.results[].title
data.results[].source_refs
data.results[].review_status
data.results[].conflict_status
data.results[].machine_gate
warnings
errors
```

### 读取单条知识

先从搜索结果中复制 `knowledge_id`，再执行：

```powershell
python codex-expert-kit/mcp/server.py --call get_knowledge_item --request-json "{\"knowledge_id\":\"替换为 knowledge_id\"}"
```

### 浏览知识树

```powershell
python codex-expert-kit/mcp/server.py --call browse_knowledge_tree --request-json "{\"domain\":\"AI Engineering\",\"include_children\":true}"
```

也可以按节点查询：

```powershell
python codex-expert-kit/mcp/server.py --call browse_knowledge_tree --request-json "{\"node_id\":\"kt.ai_engineering\",\"include_children\":true}"
```

## Codex MCP 配置

模板位置：

```text
codex-expert-kit/templates/codex_config_mcp.toml
```

建议流程：

```text
1. 复制模板到业务项目的 Codex 配置。
2. 替换 CEK_TA_ROOT 和 server.py 路径。
3. 保持 enabled = false。
4. 先在命令行跑通 --info、--list-tools、search_expert_knowledge。
5. 健康检查通过后再改为 enabled = true。
```

不要在健康检查前直接启用 MCP。这样可以避免外部项目启动时因为路径、Python 环境或索引不存在导致 AI IDE 工具初始化失败。

## 主动检索规则

外部项目 AI 遇到以下情况必须主动检索 CEK-TA：

```text
1. 涉及交易、回测、回放、模拟盘、实盘、风控、订单、数据、AI 训练、RAG、MCP、知识治理。
2. 需要做专业判断、代码审计、方案设计、任务拆分、上线前检查。
3. 需要引用来源、判断边界、处理冲突或确认 machine gate。
4. 用户要求“按 CEK-TA 知识库”“查知识库”“引用来源”。
```

详见：

[外部项目 AI 主动检索协议](./tasks/phase35_external_ai_active_retrieval_protocol.md)

## 常见错误

| 现象 | 可能原因 | 处理 |
| --- | --- | --- |
| `storage_unavailable` | `knowledge_items.json` 不存在或路径错误 | 运行索引重建，或设置 `CEK_TA_KNOWLEDGE_ITEMS_PATH` |
| `Unknown tool` | 工具名拼错或配置引用旧 spec | 执行 `--list-tools` 查看当前工具 |
| 查询无结果 | query 太窄、过滤条件过严、知识未进入正式索引 | 放宽 query，确认知识已进入 `knowledge_items.json` |
| 返回 `reviewed/caveat_only` | 知识可用于审计/检索，但不是默认指导 | 不得当作 approved 或 hard gate |
| MCP 启动失败 | 业务项目配置了错误路径或 Python 环境 | 先在 CEK-TA 根目录跑 CLI smoke |

## 边界提醒

```text
MCP 只读。
正式知识索引是默认查询源。
候选知识不能作为默认指导。
reviewed 不等于 approved。
default guidance 和 hard gate 必须读取 machine_gate / review 字段。
CEK-TA 不生成买卖点、仓位、杠杆、止损止盈、风险阈值或实盘执行建议。
```
