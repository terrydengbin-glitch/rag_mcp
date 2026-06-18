# CEK-TA Local Indexes

本目录保存 CEK-TA 文件化索引。正式知识的源头仍然是：

```text
codex-expert-kit/rag/knowledge/
```

索引可以从正式知识目录重建，它们不是知识源头本身。

Files:

```text
knowledge_index.json
knowledge_items.json
tree_index.json
source_index.json
conflict_index.json
```

Phase 13 定义文件化索引契约。Phase 21 增加 MCP 正式知识聚合索引。

`knowledge_items.json` 是 Phase 14+ MCP 运行时默认读取的正式知识聚合索引。外部项目通过 MCP 查询 CEK-TA 时，默认应指向这个文件，而不是候选队列或 sample fixture。

修改 `../knowledge/**/*.json` 后重建：

```text
python codex-expert-kit/rag/scripts/build_knowledge_items_index.py
```

外部项目可通过环境变量显式指定：

```powershell
$env:CEK_TA_KNOWLEDGE_ITEMS_PATH = "$env:CEK_TA_ROOT\codex-expert-kit\rag\indexes\knowledge_items.json"
```

MCP smoke：

```powershell
python codex-expert-kit/mcp/server.py --info
python codex-expert-kit/mcp/server.py --call search_expert_knowledge --request-json "{\"query\":\"lookahead bias\",\"top_k\":3}"
```

边界：

```text
1. knowledge_items.json 只聚合正式知识。
2. 候选知识不作为默认 MCP 查询源。
3. reviewed/caveat_only 不等于 approved。
4. default guidance 和 hard gate 必须读取 knowledge item 的 review / machine_gate 字段。
```
