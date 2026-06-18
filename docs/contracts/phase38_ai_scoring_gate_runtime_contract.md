# Phase 38 AI Scoring/Gate Runtime Contract

生成日期：2026-06-10
状态：contract draft
对应任务：CEK-TA-267

## 目标

本文定义外接交易项目在实现 gating/scoring POC 时，`Numeric Scorer`、`LLM Audit Assistant` 和 `Deterministic Final Gate` 的职责边界、输入输出契约、错误处理、权限边界和审计要求。

本契约不是交易策略，不提供买卖建议，不授权 LLM 或 scorer 直接下单。

## 角色边界

```text
Numeric Scorer:
  负责输出质量分、坏交易风险、校准概率、risk bucket、review priority。
  不负责最终 allow/block/size。

LLM Audit Assistant:
  负责解释 scorer 输出、检索 CEK-TA、生成 reason code、risk flag、missing field、知识引用和人工复核摘要。
  不负责最终 allow/block/size。

Deterministic Final Gate:
  负责最终 allow/block/size/kill switch。
  只能由外接项目确定性风控和 owner 审批规则实现。
```

## 上游输入

```json
{
  "project_adapter_id": "string",
  "mode": "research | backtest | replay | paper | live",
  "request_type": "score | gate | audit | evaluate | release",
  "trade_candidate_snapshot_ref": "string",
  "feature_schema_version": "string",
  "label_policy_version": "string",
  "risk_policy_version": "string",
  "strategy_version_ref": "string",
  "rag_index_version": "string",
  "trace_id": "string"
}
```

## Numeric Scorer 输入契约

```json
{
  "schema_version": "numeric_scorer_input_v1",
  "trace_id": "string",
  "candidate_id": "string",
  "decision_time": "ISO-8601",
  "features": {},
  "feature_schema_version": "string",
  "feature_lineage_manifest": "string",
  "strategy_version_ref": "string",
  "market_context_ref": "string",
  "risk_context_ref": "string",
  "execution_context_ref": "string",
  "forbidden_fields_scan": {
    "contains_post_trade_field": false,
    "contains_target_field": false,
    "feature_available_after_decision": false
  }
}
```

阻断条件：

```text
missing decision_time -> block_score
missing feature_schema_version -> block_score
feature_available_after_decision == true -> block_score
contains_post_trade_field == true -> block_score
contains_target_field == true -> block_score
missing strategy_version_ref -> block_score
```

## Numeric Scorer 输出契约

```json
{
  "schema_version": "numeric_scorer_output_v1",
  "trace_id": "string",
  "candidate_id": "string",
  "model_family": "rule_baseline | logistic_regression | lightgbm | xgboost | catboost | other",
  "model_version": "string",
  "score_scale": "0-100",
  "quality_score": 0.0,
  "bad_trade_risk": 0.0,
  "calibrated_probability": 0.0,
  "risk_bucket": "low | medium | high | unknown",
  "review_priority": "low | medium | high | urgent",
  "top_features": [],
  "calibration_policy_version": "string",
  "threshold_policy_version": "string",
  "scorer_must_not_decide_final_gate": true
}
```

## LLM Audit Assistant 输入契约

```json
{
  "schema_version": "llm_audit_input_v1",
  "trace_id": "string",
  "candidate_summary": {},
  "numeric_scorer_output": {},
  "deterministic_rule_hits": [],
  "retrieved_knowledge": [
    {
      "knowledge_id": "string",
      "canonical_node_id": "string",
      "review_status": "reviewed | approved",
      "machine_gate": "allow | caveat_only | deny",
      "source_refs": []
    }
  ],
  "missing_fields": [],
  "allowed_context_policy": {
    "no_secret": true,
    "no_account_identifier": true,
    "no_private_strategy_body": true,
    "no_future_outcome": true
  }
}
```

## LLM Audit Assistant 输出契约

```json
{
  "schema_version": "llm_audit_v1",
  "trace_id": "string",
  "recommendation": "allow_recommendation | soft_block_recommendation | hard_block_recommendation | needs_human_review | neutral",
  "reason_codes": [],
  "risk_flags": [],
  "missing_fields": [],
  "knowledge_refs": [],
  "source_refs": [],
  "unsupported_claims": [],
  "citation_completeness_score": 0.0,
  "requires_human_review": true,
  "llm_must_not_decide_final_gate": true
}
```

强制校验：

```text
必须通过 JSON Schema。
recommendation 必须是枚举值。
knowledge_refs 必须能在 CEK-TA formal index 中解析。
source_refs 必须来自 retrieved_knowledge 或外接项目允许的证据。
unsupported_claims 不为空时，final gate 不得因 LLM 输出而放行。
检索无命中时必须 neutral 或 needs_human_review。
```

## Deterministic Final Gate 输入契约

```json
{
  "schema_version": "final_gate_input_v1",
  "trace_id": "string",
  "numeric_scorer_output": {},
  "llm_audit_output": {},
  "risk_policy_version": "string",
  "threshold_policy_version": "string",
  "deterministic_rule_hits": [],
  "owner_approval_state": "not_required | pending | approved | rejected"
}
```

## Deterministic Final Gate 输出契约

```json
{
  "schema_version": "final_gate_output_v1",
  "trace_id": "string",
  "gate_decision": "allow | soft_block | hard_block | needs_human_review | neutral",
  "position_size_decision": "external_project_owned",
  "risk_policy_version": "string",
  "threshold_policy_version": "string",
  "deterministic_rule_hits": [],
  "llm_recommendation_used_as_context_only": true,
  "audit_trace_id": "string"
}
```

## MCP/RAG 检索要求

涉及以下任务时，外接项目 AI 必须主动检索 CEK-TA：

```text
训练数据生成
scoring/gating 逻辑设计
校准阈值设计
shadow/paper/OPE 评估
LLM 审计输出
模型发布和回滚
事故复盘
```

最小检索响应必须包含：

```text
knowledge_id
canonical_node_id
review_status
machine_gate.default_guidance
llm_usage_policy
source_evidence
conflict_status
freshness
applicability
not_applicable_when
```

## 错误处理

| 错误 | 处理 |
| --- | --- |
| scorer timeout | fallback to deterministic gate only |
| MCP no-hit | neutral 或 needs_human_review |
| RAG conflict hit | block_default_guidance |
| LLM schema invalid | retry once, then abstain |
| missing source citation | needs_human_review |
| feature leakage gate failed | block_score |
| calibration policy missing | block_hard_gate_promotion |
| owner approval missing for hard gate | block_hard_gate_promotion |

## 权限边界

```text
Numeric Scorer 不得下单。
LLM Audit Assistant 不得下单。
MCP 只读，不写知识，不审批，不交易。
Final Gate 不得读取密钥或绕过外接项目权限系统。
CEK-TA 不保存外接项目私有策略正文、账户事实或密钥。
```

## Definition of Done

```text
1. 三个服务职责边界明确。
2. 输入输出 schema 明确。
3. 错误处理和 fallback 明确。
4. LLM 不承担最终 gate。
5. MCP/RAG 只读和 citation 要求明确。
6. 中文 UTF-8 无乱码。
```
