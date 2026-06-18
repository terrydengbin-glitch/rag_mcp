# KnowledgeItem Schema v1.1 Contract

## 目标

`schema_version = 1.1.0` 在 v1.0 的正式知识卡片基础上增加 AI 使用边界和机器门控字段，让 MCP、SearchLab、FastAPI、Vue3 和外部项目调用同一套默认指导规则。

本契约不引入数据库，不改变正式知识的文件化存储方式。

## 上游

```text
codex-expert-kit/rag/knowledge/**/*.json
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/metadata_schema.md
codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
```

## 下游

```text
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/mcp/search_expert_knowledge.py
codex-expert-kit/mcp/get_knowledge_item.py
codex-expert-kit/api/codex_expert_kit_api/
ui/src/data/formalKnowledgeItems.ts
ui/src/views/KnowledgeTreeView.vue
ui/src/views/KnowledgeDetail.vue
ui/src/views/SearchLab.vue
其他项目 MCP 调用方
```

## v1.1 新增字段

### metadata.claim_type

用于定义知识 claim 的机器可读类型，避免 AI 把方法论边界误用成交易信号。

```text
methodological_constraint
risk_boundary_rule
execution_safety_rule
data_quality_rule
backtest_validity_rule
rag_governance_rule
mcp_contract_rule
knowledge_governance_rule
project_integration_rule
llm_training_rule
llm_eval_rule
training_data_schema_rule
ai_security_rule
ai_governance_rule
llmops_release_rule
```

### metadata.classification_notes

用于解释 UI 挂载节点和 canonical 节点不一致、或领域归类需要说明的情况。

### llm_usage_policy

```json
{
  "allowed": ["string"],
  "not_allowed": ["string"],
  "required_context": ["string"],
  "fallback_behavior": "deny | ask_for_context | cite_with_caveat"
}
```

规则：

```text
1. allowed 必须说明 AI 可以如何使用该知识。
2. not_allowed 必须说明 AI 不得如何使用该知识。
3. required_context 必须说明使用该知识前需要哪些项目事实。
4. fallback_behavior 用于项目事实不足时的默认行为。
```

### machine_gate

```json
{
  "default_guidance": "allow | caveat_only | deny",
  "reason": "string",
  "requires_human_escalation": true,
  "blocking_reasons": ["string"],
  "checked_at": "YYYY-MM-DD",
  "gate_version": "1.0.0"
}
```

判定规则：

```text
allow:
  review.review_status = approved
  review.default_guidance_allowed = true
  conflict_audit.conflict_status in [none, resolved]
  source_evidence 至少 1 条
  source_quality.overall_reliability in [high, medium]
  review.freshness != deprecated
  contribution.private_data_removed = true

caveat_only:
  review.review_status = reviewed
  review.default_guidance_allowed = false
  来源、冲突、污染门禁通过
  但未经过 approved 治理

deny:
  draft / rejected / deprecated
  无来源
  confirmed conflict
  来源质量为 low
  私有数据未脱敏
  命中污染门禁
```

### recommended_extra_sources

待核验来源增强队列。它不是正式证据，不能替代 `source_evidence`。

```json
[
  {
    "title": "string",
    "source_url": "string | null",
    "source_type": "paper | official_doc | exchange_rule | framework_doc | book | research_report | engineering_article",
    "purpose": "string",
    "status": "proposed | verified | rejected"
  }
]
```

## MCP 契约

`search_expert_knowledge` 结果必须返回：

```text
claim_type
classification_notes
llm_usage_policy
machine_gate
recommended_extra_sources_count
recommended_next_action
```

默认指导模式只能使用：

```text
machine_gate.default_guidance = allow
```

`caveat_only` 只能作为审计、研究、检索提示返回，并必须带 caveat。

## FastAPI 契约

知识列表卡片和详情响应必须包含：

```text
claim_type
classification_notes
llm_usage_policy
machine_gate
recommended_extra_sources_count
```

缺字段时返回兼容默认值，不能返回 500。

## Vue3 契约

Vue3 知识树和知识详情页至少展示：

```text
知识类型
默认指导状态
AI 可用范围
AI 禁止范围
必需上下文
分类说明
阻断原因
推荐补充来源数量
```

## 禁止事项

```text
1. 禁止把 reviewed 当成 allow。
2. 禁止把 recommended_extra_sources 当成 source_evidence。
3. 禁止无来源知识进入 allow。
4. 禁止 unresolved confirmed conflict 进入 allow。
5. 禁止把项目私有知识标记为通用默认指导。
```

## 验收

```text
1. 所有正式知识通过 v1.1 validator。
2. knowledge_items.json 包含新增字段。
3. MCP 默认指导只返回 allow。
4. FastAPI 和 Vue3 可展示新增字段。
5. 污染门禁和候选工作流门禁继续通过。
```
