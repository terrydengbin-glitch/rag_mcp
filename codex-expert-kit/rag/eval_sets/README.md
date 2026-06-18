# CEK-TA Eval Sets

本目录存放知识质量、检索质量、问答质量和 v1/v2 知识树路由一致性的文件化评测集。

## 目录目标

```text
1. 为 RAG/MCP 检索提供可回归的测试用例。
2. 为 Codex 问答和知识引用提供人工评测样例。
3. 为知识树 v1/v2 alias 迁移提供一致性评测。
4. 为 Phase 17 首批真实知识资产提供验收基线。
```

## 文件清单

| 文件 | 用途 |
| --- | --- |
| `retrieval_eval_cases.json` | 检索回归用例，检查命中、引用、边界和阻断规则 |
| `qa_eval_cases.json` | 问答评测用例，检查回答是否有来源、边界、冲突提示和安全动作 |
| `tree_routing_eval_cases.json` | v1/v2 路由一致性、alias mismatch、split target 阻断评测 |

## 通用字段

每个评测用例必须包含：

```json
{
  "case_id": "string",
  "category": "kline | backtest | risk | execution | llm_rag | tree_routing | contribution",
  "priority": "P0 | P1 | P2",
  "task_type": "string",
  "query": "string",
  "mode": "default_guidance | audit | browse | ingestion_classification | quality_eval",
  "filters": {},
  "project_context": {},
  "expected": {},
  "must_not": {},
  "metrics": ["string"],
  "review_notes": "string"
}
```

## 评测边界

```text
1. 本目录的样例是结构和回归基线，不代表已经沉淀了完整专业知识。
2. 用例不采集实时 K 线、行情或订单数据。
3. 用例只验证专业知识检索、来源、适用边界、冲突和路由安全。
4. 缺少真实 accepted 知识时，允许 expected_knowledge_ids 为空，但必须验证阻断和 warning 行为。
5. Phase 17 增加真实知识资产后，应把 expected_knowledge_ids 补充为真实 ID。
```

## 质量门槛

```text
smoke:
  所有 P0 用例必须满足 contract、source、boundary 和 blocking 检查。

regression:
  unsafe_default_guidance_rate 必须为 0。
  citation_completeness 必须达到 0.95。
  v1_v2_route_consistency_rate 必须达到 0.95。
  alias_mismatch_block_rate 必须为 1.0。

release:
  所有 P0/P1 用例必须有明确 expected_node_ids 或 expected_knowledge_ids。
  所有 high/critical 风险节点必须有来源、边界和冲突检查。
```

## 更新规则

```text
1. 新增知识树主枝或高风险叶子节点时，必须增加至少 1 条检索或路由用例。
2. 发现检索误命中、漏命中或错误默认指导时，必须增加回归用例。
3. 接受其他项目回灌知识后，必须增加相关 contribution 或 boundary 用例。
4. 修改 MCP/RAG 检索契约后，必须同步本目录字段。
```
