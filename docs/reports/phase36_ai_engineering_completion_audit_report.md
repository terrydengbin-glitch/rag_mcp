# Phase 36 AI Engineering 知识库完整性复审报告

生成时间：2026-06-09

## 审计结论

Phase 36 规划的 AI Engineering 交易 LLM gating/scoring 知识点已经完成候选采集、外部审计、补证、二审、formal reviewed 沉淀、MCP 索引、Vue3 fixture 和质量门禁闭环。

本次复审结论：

```text
Phase 36 规划知识点：113 条
正式索引中命中：113 条
缺失：0 条
Phase 36 候选文件：113 条
候选状态：113 条 accepted / formalized
候选正式知识回链缺失：0 条
Phase 36 formal knowledge：113 条 reviewed
approved：0 条
machine_gate.default_guidance：113 条 caveat_only
最少来源数：3
少于 2 个来源：0 条
```

这说明 Phase 36 作为“外接交易 LLM gating/scoring 项目”的 AI Engineering 专业知识支撑层，已经达到当前预期：可检索、可引用、可审计、可回链。MCP 默认会把这些正式入库的 reviewed 知识作为 accepted_reference 返回，但不会把它们误提升为 approved 默认交易指导。

## 上下游对齐

上游输入：

```text
docs/research/phase36_ai_engineering_p0_collection_matrix.md
docs/research/phase36_ai_engineering_research_task_queue.md
docs/audit/phase36_ai_engineering_batches/
docs/audit/*phase36*_reaudit*.json
codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/
```

下游输出：

```text
codex-expert-kit/rag/knowledge/KB_09_LLM_TRAINING/
codex-expert-kit/rag/knowledge/KB_AI_ENGINEERING/
codex-expert-kit/rag/indexes/knowledge_items.json
ui/src/data/formalKnowledgeItems.ts
ui/src/data/phase23Candidates.ts
codex-expert-kit/mcp/search_expert_knowledge.py
```

外部项目调用边界：

```text
默认 MCP 检索返回正式入库知识，包括 approved/allow 和 reviewed/caveat_only。
Phase 36 当前为 reviewed/caveat_only，外部项目 AI IDE 可默认检索并作为 accepted_reference 使用。
reviewed 不等于 approved，不允许作为高风险交易行为的默认交易指导；live/risk/high-impact 行为变更仍需要 allow 或人工确认。
```

## 契约检查

正式知识满足以下契约：

```text
knowledge_id 存在
metadata.domain/subdomain/tree_node_id/canonical_node_id 存在
content.statement 存在
applicability.applies_when / not_applicable_when 存在
source_evidence 存在且每条至少 3 个来源
source_quality 存在
conflict_audit 存在
review.review_status = reviewed
review.approval_status = not_requested
review.default_guidance_allowed = false
machine_gate.default_guidance = caveat_only
llm_usage_policy 存在
```

候选知识满足以下契约：

```text
候选源文件保留
status.review_status = accepted
workflow.queue_group = formalized
workflow.formal_knowledge_id 存在
formal knowledge 回链存在
```

## MCP / SearchLab 抽样验证

默认 reviewed 检索请求：

```json
{
  "filters": {
    "review_status": "reviewed"
  },
  "include": {
    "reviewed": true,
    "default_guidance_only": false,
    "sources": true,
    "conflicts": true
  }
}
```

抽样结果：

| 查询 | 预期知识 | 是否命中 | 返回动作 |
| --- | --- | --- | --- |
| `strategy_version_ref lineage` | `kb_ai_engineering.trade_data.strategy_id_and_version_required.v1` | yes | `cite_with_caveat` |
| `SFT schema input target separation` | `kb_ai_engineering.training_example.sft_schema_required.v1` | yes | `cite_with_caveat` |
| `LLM gate deterministic final authority` | `kb_ai_engineering.runtime.final_gate_deterministic_engine_required.v1` | yes | `cite_with_caveat` |
| `RAG context untrusted prompt injection` | `kb_ai_engineering.security.rag_context_is_untrusted_input.v1` | yes | `cite_with_caveat` |

兼容 allow-only 检索请求：

```text
include.default_guidance_only = true
reviewed/caveat_only 会进入 blocked_results
```

这符合预期：MCP 默认可返回正式入库的 reviewed 知识作为已采纳参考；调用方若明确要求 allow-only，高风险默认指导仍会阻断 caveat_only。

## 测试与门禁

已执行：

```text
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
python codex-expert-kit/rag/scripts/build_knowledge_items_index.py
python codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py
python codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py
cd ui && npm run build
```

结果：

```text
candidate_to_reviewed：pass，candidate_count 120，knowledge_count 130
schema v1.1：pass，item_count 130，allow 10，caveat_only 120
no_mojibake：pass，scanned_count 372，failure_count 0
knowledge_pollution：pass，scanned_count 130，polluted_count 0
knowledge_items.json：130 items
formalKnowledgeItems.ts：130 formal knowledge items
phase23Candidates.ts：120 candidates
Vue3 build：pass
```

Vue3 build 仍有 Vite 大 chunk 提示，这是体积优化提示，不影响本次知识完整性验收。

## 发现的问题与处理

发现：

```text
CEK-TA-187 和 CEK-TA-188 仍保留早期 blocked 状态，但后续批量导入、补证二审、索引重建和运行时抽样已经完成。
```

处理：

```text
已将 CEK-TA-187 / CEK-TA-188 更新为 done。
已新增 CEK-TA-261 记录本次完整性复审。
```

## 剩余注意点

```text
1. 当前 113 条全部是 reviewed/caveat_only，MCP 默认返回时属于 accepted_reference，不是 approved_guidance。
2. 如后续希望成为高风险默认交易指导，需要单独创建 approved 治理 Phase，并由人工决定哪些知识可升级。
3. 部分知识之间存在父子化/合并建议，例如 strategy_version、SFT schema、lineage/release manifest，这不影响当前 reviewed 使用，但后续可做知识树治理优化。
4. Phase 36 已覆盖 AI Engineering；K 线、策略、回测、实盘执行和交易风控本体继续由 Phase 37 Trading Engineering 承接。
```

## 最终判断

```text
Phase 36 AI Engineering 知识库已完整达到当前预期。
它已经可以支持外接交易 LLM gating/scoring 项目的开发 AI 通过 MCP/SearchLab 主动检索、带来源引用、以 accepted_reference 方式使用。
它不能直接作为 approved 默认交易指导，也不会绕过 deterministic risk engine。
```
