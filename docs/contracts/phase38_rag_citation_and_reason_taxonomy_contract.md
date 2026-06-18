# Phase 38 RAG 引用、Reason Taxonomy 与默认指导门禁契约

## 目标

本契约用于补齐 Phase 38 P0-Core 审计中 D03、D04、D05、D06、G01、G03 和 G04 暴露的内部契约缺口。它定义外接交易 LLM gating/scoring 项目在调用 CEK-TA 知识库时，如何解析引用、处理无命中、约束 reason code、阻断 unsupported claims，并通过 machine gate 与 review status 控制默认指导。

## 上游输入

```text
docs/contracts/external_ai_active_retrieval_protocol.md
docs/contracts/knowledge_item_schema_v1_1_contract.md
docs/contracts/phase38_ai_scoring_gate_runtime_contract.md
docs/contracts/phase38_training_data_and_eval_contract.md
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/knowledge/
```

## 下游输出

```text
1. LLM Audit Assistant 的 knowledge_refs 校验规则。
2. SearchLab/MCP 的 no-hit 降级规则。
3. reason_code taxonomy v1 的最小枚举和版本字段。
4. unsupported_claims 的阻断和人工复核路由。
5. machine_gate + review_status 的默认指导准入规则。
6. 上下文预算和字段裁剪规则，避免外部 AI IDE 读入过多无关字段。
```

## Formal Index Schema

`knowledge_items.json` 必须至少暴露以下可解析字段：

```json
{
  "knowledge_id": "string",
  "canonical_node_id": "string",
  "title": "string",
  "content_summary": "string",
  "review_status": "draft | reviewed | approved | deprecated",
  "approval_status": "not_requested | requested | approved | rejected",
  "machine_gate": {
    "default_guidance": "allow | deny | caveat_only",
    "requires_human_escalation": "boolean"
  },
  "source_evidence": [
    {
      "source_id": "string",
      "source_title": "string",
      "source_url": "string",
      "source_type": "string"
    }
  ],
  "conflict_status": "none | resolved | confirmed | unchecked",
  "freshness": "stable | time_sensitive",
  "updated_at": "string"
}
```

## Citation Resolver Contract

LLM Audit Assistant 输出的 `knowledge_refs` 必须满足：

```text
1. 每个 ref 必须能解析到 formal index 中的 knowledge_id。
2. 每个 ref 必须返回至少一个 source_evidence。
3. ref 的 review_status 至少为 reviewed，或者明确标注为 draft/candidate 且不得作为默认指导。
4. ref 的 conflict_status 不得为 confirmed 或 unchecked。
5. 解析失败时不得补猜来源，不得把普通 RAG 文本当成已验证知识。
```

引用解析失败时输出：

```json
{
  "citation_status": "unresolved",
  "recommendation": "abstain",
  "requires_human_review": true,
  "unsupported_claims": ["无法被 formal index 解析的 claim"]
}
```

## No-Hit 与无来源降级

当 MCP/SearchLab/外部 AI IDE 检索不到可引用的正式知识时：

```text
1. 不得生成默认指导。
2. 不得把候选知识当成正式规则。
3. 输出 recommendation=neutral 或 abstain。
4. 记录 no_hit_query、filters、top_k、canonical_node_id 和缺口描述。
5. 若任务属于交易 gating/scoring、模型发布、实盘安全或数据泄漏风险，必须提示人工复核。
```

## Unsupported Claims 路由

`unsupported_claims` 不为空时：

```text
1. LLM recommendation 不能为 allow。
2. Final gate 不得读取 unsupported_claims 作为通过理由。
3. 该任务进入 human_review 或 supplemental_evidence 队列。
4. 如果 unsupported_claim 涉及交易规则本体，应路由到 Trading Engineering 分支。
5. 如果 unsupported_claim 涉及缺少来源，应创建补证采集任务。
```

## Reason Code Taxonomy v1

Phase 38 POC 的 reason code 必须来自受控 taxonomy，并带 `reason_taxonomy_version`。

最小枚举：

```text
DATA_LEAKAGE_RISK
POINT_IN_TIME_VIOLATION
MISSING_SOURCE
UNRESOLVED_CITATION
UNSUPPORTED_CLAIM
SCHEMA_VALIDATION_ERROR
MODEL_UNCALIBRATED
THRESHOLD_POLICY_MISSING
FINAL_GATE_BOUNDARY_VIOLATION
TRADING_RULE_ROUTING_REQUIRED
COUNTERFACTUAL_LABEL_RISK
RELEASE_GOVERNANCE_MISSING
HUMAN_REVIEW_REQUIRED
```

LLM 输出未登记 reason code 时：

```text
1. 设置 schema_valid=false。
2. recommendation 降级为 neutral。
3. requires_human_review=true。
4. 记录 unknown_reason_codes。
```

## Machine Gate 与默认指导准入

默认指导只允许：

```text
review_status == approved
approval_status == approved
machine_gate.default_guidance == allow
conflict_status in ["none", "resolved"]
source_evidence_count > 0
```

以下状态只能作为审计或研究参考，不能默认指导：

```text
candidate
accepted_for_draft
draft
reviewed
needs_more_evidence
rejected
deprecated
machine_gate.default_guidance == deny
machine_gate.default_guidance == caveat_only
```

## 上下文预算与字段裁剪

外部 AI IDE 调用 CEK-TA 时，默认只取最小必要字段：

```text
knowledge_id
title
canonical_node_id
claim_type
content_summary
applicability
not_applicable_when
llm_usage_policy
machine_gate
source_evidence
conflict_status
recommended_next_action
```

默认不返回：

```text
完整候选审计日志
长 source 摘要
无关 canonical 分支
候选正文全文
历史版本全文
```

需要详细审计时，必须由调用方显式请求 `include_audit_detail=true`，并保留 top-k、字段白名单和 token budget。

## 外部来源锚点

```text
JSON Schema: https://json-schema.org/docs
OpenAI Structured Outputs: https://developers.openai.com/api/docs/guides/structured-outputs
OWASP Prompt Injection: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
Ragas faithfulness: https://docs.ragas.io/en/v0.1.21/concepts/metrics/faithfulness.html
DeepEval faithfulness: https://deepeval.com/docs/metrics-faithfulness
```

这些来源只能支撑 JSON schema、结构化输出、prompt injection、RAG faithfulness/groundedness 的通用工程原则；CEK-TA 的默认指导门禁、formal index、reason taxonomy 和工作流状态仍以本契约为准。

## Definition of Done

```text
1. D03-D06/G01/G03/G04 能引用本契约作为内部契约来源。
2. accepted_for_draft 仍不得直接进入 reviewed、approved 或 default guidance。
3. MCP/SearchLab/知识树仍只读取正式知识索引。
4. 中文 UTF-8 无乱码。
```
