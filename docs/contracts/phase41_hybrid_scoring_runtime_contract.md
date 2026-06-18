# Phase 41 Hybrid Scoring 运行时契约

生成日期：2026-06-10
状态：contract draft
对应任务：CEK-TA-320

## 目标

本文定义外接交易 LLM gating/scoring 项目调用 CEK-TA 知识库时，`Tabular Numeric Scorer`、`Calibrator`、`Qwen3 Audit Assistant`、`RAG Citation Resolver` 和 `Deterministic Final Gate` 的组合运行时契约。

核心原则：

```text
表格/统计模型负责数值 scoring、风险排序和 review priority。
Calibrator 负责把模型分数转换成可审计的校准概率、风险分桶和不确定性分桶。
Qwen3/LLM 负责审计解释、reason code、RAG 引用、缺字段检查和人工复核摘要。
Deterministic Final Gate 负责最终交易权限、阻断、降级、仓位上限、安全停机和审计追踪。
```

本契约不提供买卖建议，不训练模型，不部署模型服务，不授权任何 LLM 或 tabular scorer 直接执行交易。

## 上下游链条

| 环节 | 上游输入 | 下游输出 | 权限边界 |
| --- | --- | --- | --- |
| Trade Candidate Snapshot | 外接交易项目事实 | 决策时快照引用 | 只提供事实，不写 CEK-TA |
| Tabular Numeric Scorer | 决策时特征、模型版本 | raw score、risk rank、top features | 不允许 allow/block/size |
| Calibrator | raw score、校准器版本、校准集版本 | calibrated probability、risk bucket、uncertainty bucket | 不允许交易放行 |
| RAG Citation Resolver | 查询意图、canonical node、知识索引版本 | 知识引用、来源、冲突与 machine gate | 只读检索 |
| Qwen3 Audit Assistant | scorer/calibrator 输出、RAG 引用、候选快照 | 审计 JSON、reason code、缺字段、unsupported claim | 不允许最终 gate |
| Deterministic Final Gate | 风控策略、阈值策略、Qwen3 审计摘要、人工审批 | allow/block/review/skip/kill_switch | 唯一最终交易权限来源 |
| Audit Trace Writer | 全链路输入输出 | audit_trace、release_manifest_ref | 只记录，不改写事实 |

## 全局请求契约

外接项目请求 hybrid scoring 时，必须提供：

```json
{
  "schema_version": "phase41_hybrid_scoring_request_v1",
  "project_adapter_id": "string",
  "trace_id": "string",
  "mode": "research | backtest | replay | paper | live",
  "requested_decision": "score | audit | gate | review | release",
  "trade_candidate_snapshot_ref": "string",
  "decision_time": "ISO-8601",
  "strategy_version_ref": "string",
  "feature_schema_version": "string",
  "label_policy_version": "string",
  "scorer_version": "string",
  "calibrator_version": "string",
  "qwen_model_version": "string",
  "prompt_version": "string",
  "rag_index_version": "string",
  "reason_taxonomy_version": "string",
  "threshold_policy_version": "string",
  "risk_policy_version": "string",
  "release_manifest_version": "string"
}
```

缺失以下字段时必须降级或阻断：

```text
trace_id 缺失 -> block_request
decision_time 缺失 -> block_score
trade_candidate_snapshot_ref 缺失 -> block_score
feature_schema_version 缺失 -> block_score
scorer_version 缺失 -> block_score
calibrator_version 缺失 -> block_calibration
rag_index_version 缺失 -> qwen_audit_must_abstain
threshold_policy_version 缺失 -> final_gate_block
risk_policy_version 缺失 -> final_gate_block
release_manifest_version 缺失且 mode 为 paper/live -> final_gate_block
```

## Tabular Numeric Scorer 输入契约

```json
{
  "schema_version": "tabular_numeric_scorer_input_v1",
  "trace_id": "string",
  "candidate_id": "string",
  "decision_time": "ISO-8601",
  "model_family": "rule_baseline | logistic_regression | lightgbm | xgboost | catboost",
  "scorer_version": "string",
  "feature_schema_version": "string",
  "feature_lineage_manifest_ref": "string",
  "features": {},
  "entity_keys": {
    "strategy_id": "string",
    "symbol": "string",
    "timeframe": "string",
    "venue": "string"
  },
  "forbidden_fields_scan": {
    "contains_post_trade_field": false,
    "contains_target_field": false,
    "feature_available_after_decision": false,
    "contains_human_audit_label": false
  }
}
```

### Scorer 阻断条件

```text
feature_available_after_decision == true -> block_score
contains_post_trade_field == true -> block_score
contains_target_field == true -> block_score
contains_human_audit_label == true -> block_score
feature_lineage_manifest_ref 缺失 -> block_score
model_family 不在注册清单 -> block_score
scorer_version 未绑定训练数据版本 -> block_score
```

## Tabular Numeric Scorer 输出契约

```json
{
  "schema_version": "tabular_numeric_scorer_output_v1",
  "trace_id": "string",
  "candidate_id": "string",
  "scorer_version": "string",
  "model_family": "string",
  "raw_score": 0.0,
  "score_direction": "higher_is_better | higher_is_riskier",
  "risk_rank": 0,
  "review_priority": "low | medium | high | critical",
  "top_features": [
    {
      "feature_name": "string",
      "importance_direction": "positive | negative | unknown",
      "importance_value": 0.0,
      "explanation_type": "coefficient | gain | shap | rule_hit"
    }
  ],
  "scorer_warnings": [],
  "scorer_decision_permission": "none"
}
```

硬规则：

```text
scorer_output 不能包含 allow/block/size/kill_switch。
raw_score 不能被 final gate 直接读取为交易权限。
top_features 只能用于审计和 debug，不能作为因果结论。
```

## Calibrator 输入契约

```json
{
  "schema_version": "calibrator_input_v1",
  "trace_id": "string",
  "candidate_id": "string",
  "raw_score": 0.0,
  "scorer_version": "string",
  "calibrator_version": "string",
  "calibration_dataset_version": "string",
  "calibration_method": "platt | isotonic | beta | none",
  "regime_key": {
    "market_regime": "string",
    "strategy_family": "string",
    "timeframe": "string"
  }
}
```

### Calibrator 输出契约

```json
{
  "schema_version": "calibrator_output_v1",
  "trace_id": "string",
  "candidate_id": "string",
  "calibrator_version": "string",
  "calibrated_probability": 0.0,
  "probability_target": "bad_trade | false_allow | expected_quality | custom",
  "risk_bucket": "low | medium | high | critical",
  "uncertainty_bucket": "low | medium | high | unknown",
  "calibration_quality": {
    "brier_score_ref": "string",
    "ece_ref": "string",
    "calibration_curve_ref": "string",
    "sample_size_bucket": "small | medium | large | insufficient"
  },
  "calibrator_warnings": []
}
```

阻断和降级规则：

```text
calibration_dataset_version 缺失 -> final_gate_block
calibration_method == none -> output may be used only as rank, not probability
sample_size_bucket == insufficient -> final_gate_requires_human_review
uncertainty_bucket == high 或 unknown -> final_gate_requires_human_review 或 block，取决于 threshold_policy
```

## RAG Citation Resolver 契约

Qwen3 审计前必须先通过 CEK-TA 正式知识索引检索相关知识。

```json
{
  "schema_version": "rag_citation_request_v1",
  "trace_id": "string",
  "query": "string",
  "canonical_node_filters": [
    "kt.ai_engineering.numeric_scoring.model_family_selection",
    "kt.ai_engineering.calibration_threshold.uncertainty",
    "kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant",
    "kt.ai_engineering.model_release_governance.hybrid_runtime_contract"
  ],
  "review_status_filter": ["reviewed", "approved"],
  "machine_gate_filter": ["allow", "caveat_only"],
  "include_sources": true,
  "include_conflict_audit": true,
  "max_items": 8
}
```

返回必须包含：

```json
{
  "schema_version": "rag_citation_response_v1",
  "trace_id": "string",
  "items": [
    {
      "knowledge_id": "string",
      "canonical_node_id": "string",
      "review_status": "reviewed | approved",
      "machine_gate": "allow | caveat_only | deny",
      "source_count": 0,
      "conflict_status": "none | resolved | potential | unresolved",
      "citation_summary": "string"
    }
  ],
  "no_hit": false,
  "conflict_or_freshness_warnings": []
}
```

降级规则：

```text
no_hit == true -> Qwen3 必须输出 no_hit_abstain。
source_count == 0 -> 该知识不能作为支持引用。
conflict_status == unresolved -> 不能作为默认指导。
machine_gate == deny -> 只能作为反例或阻断说明。
```

### Citation Resolver 与 Unsupported Claim 门禁

RAG 检索结果、用户交易摘要和外部项目传入的上下文都必须按不可信输入处理。Qwen3 生成审计结果前，必须先执行 citation resolver 和 unsupported claim detector。

```json
{
  "schema_version": "phase41_citation_resolver_v1",
  "trace_id": "string",
  "retrieved_items": [
    {
      "knowledge_id": "string",
      "source_refs": ["string"],
      "claim_scope": "string",
      "machine_gate": "allow | caveat_only | deny",
      "conflict_status": "none | resolved | potential | unresolved"
    }
  ],
  "qwen_claims": [
    {
      "claim_id": "string",
      "claim_text": "string",
      "supporting_knowledge_ids": ["string"],
      "citation_resolution_status": "resolved | no_source | conflict_unresolved | stale | out_of_scope",
      "unsupported_reason": "string | null"
    }
  ],
  "unsupported_claims": ["string"],
  "result": "resolved | abstain | needs_human_review"
}
```

硬门：

```text
任何 qwen_claim 无 supporting_knowledge_ids -> abstain 或 needs_human_review
citation_resolution_status in [no_source, conflict_unresolved, stale, out_of_scope] -> 不得进入 final gate
unsupported_claims 非空 -> Qwen3 recommendation 只能作为审计问题，不能作为事实
RAG context 包含 prompt injection 指令 -> 丢弃该上下文并记录 security_event_ref
```

## Qwen3 Audit Assistant 输入契约

```json
{
  "schema_version": "qwen3_audit_input_v1",
  "trace_id": "string",
  "candidate_id": "string",
  "mode": "research | backtest | replay | paper | live",
  "qwen_model_version": "string",
  "prompt_version": "string",
  "thinking_mode": "enabled | disabled",
  "trade_candidate_snapshot_ref": "string",
  "scorer_output_ref": "string",
  "calibrator_output_ref": "string",
  "rag_citation_response": {},
  "reason_taxonomy_version": "string",
  "required_fields_policy_version": "string"
}
```

## Review Capacity 与 Threshold Policy 契约

阈值策略不能只看模型分数，还必须绑定业务成本、人工复核容量、溢出策略和 owner approval。

```json
{
  "schema_version": "phase41_review_capacity_policy_v1",
  "threshold_policy_version": "string",
  "cost_matrix_version": "string",
  "false_allow_cost_ref": "string",
  "false_block_cost_ref": "string",
  "review_capacity_snapshot_ref": "string",
  "review_capacity": {
    "max_daily_reviews": 0,
    "max_live_queue_depth": 0,
    "overflow_policy": "fail_closed | auto_block | defer_to_human | research_only"
  },
  "owner_approval_ref": "string",
  "valid_from": "ISO-8601",
  "valid_until": "ISO-8601 | null"
}
```

硬门：

```text
cost_matrix_version 缺失 -> final_gate_block
review_capacity_snapshot_ref 缺失 -> final_gate_requires_human_review
overflow_policy 缺失 -> final_gate_block
owner_approval_ref 缺失且 mode 为 paper/live -> final_gate_block
```

## Composite Release Manifest 契约

Hybrid scoring 的发布单位不是单个模型，而是一组必须一起追踪和回滚的版本集合。

```json
{
  "schema_version": "phase41_composite_release_manifest_v1",
  "release_manifest_version": "string",
  "scorer_version": "string",
  "calibrator_version": "string",
  "threshold_policy_version": "string",
  "qwen_model_version": "string",
  "qwen_prompt_version": "string",
  "rag_index_version": "string",
  "reason_taxonomy_version": "string",
  "citation_resolver_version": "string",
  "unsupported_claim_detector_version": "string",
  "owner_approval_ref": "string",
  "rollback_target": {
    "release_manifest_version": "string",
    "scorer_version": "string",
    "calibrator_version": "string",
    "threshold_policy_version": "string",
    "qwen_prompt_version": "string",
    "rag_index_version": "string"
  },
  "kill_switch_ref": "string"
}
```

硬门：

```text
任一核心版本缺失 -> release_block
rollback_target 缺失 -> release_block
owner_approval_ref 缺失 -> release_block
kill_switch_ref 缺失且 mode 为 paper/live -> release_block
Qwen3 prompt 或 RAG index 变更后未更新 manifest -> release_block
```

thinking mode 策略：

```text
复杂审计、冲突检查、缺字段原因分析、release review -> thinking_mode enabled。
低延迟结构化检查、固定 schema 验证、批量预筛 -> thinking_mode disabled。
thinking 内容不得作为用户可见审计结论直接入库，不保存私有 chain-of-thought，只保留最终 strict JSON、reason code、citation 和 audit summary。
RAG context、用户交易摘要和检索文档必须视为不可信输入；Qwen3 输出进入审计链路前必须经过 prompt-injection guard、citation resolver、unsupported_claim detector 和 schema validation。
```

## Qwen3 Audit Assistant 输出契约

Qwen3 必须输出 strict JSON：

```json
{
  "schema_version": "qwen3_audit_output_v1",
  "trace_id": "string",
  "candidate_id": "string",
  "recommendation": "allow_with_caveat | block | needs_human_review | abstain",
  "reason_codes": [
    {
      "code": "string",
      "severity": "info | warning | critical",
      "evidence_refs": ["string"]
    }
  ],
  "risk_flags": [],
  "missing_fields": [],
  "unsupported_claims": [],
  "knowledge_refs": [
    {
      "knowledge_id": "string",
      "canonical_node_id": "string",
      "how_used": "support | caveat | contradiction | no_hit"
    }
  ],
  "citation_completeness_score": 0.0,
  "requires_human_review": true,
  "qwen_decision_permission": "none"
}
```

硬规则：

```text
Qwen3 输出不能包含最终 allow/block/size/kill_switch 权限。
recommendation 只是审计建议，不是交易 gate 决策。
knowledge_refs 为空时必须 abstain 或 needs_human_review。
unsupported_claims 非空时 final gate 不得自动 allow。
citation_completeness_score 低于阈值时必须 requires_human_review。
```

## Deterministic Final Gate 输入契约

```json
{
  "schema_version": "final_gate_input_v1",
  "trace_id": "string",
  "candidate_id": "string",
  "mode": "research | backtest | replay | paper | live",
  "risk_policy_version": "string",
  "threshold_policy_version": "string",
  "release_manifest_version": "string",
  "strategy_version_ref": "string",
  "scorer_output_ref": "string",
  "calibrator_output_ref": "string",
  "qwen_audit_output_ref": "string",
  "deterministic_rule_hits": [],
  "human_approval_ref": "string | null"
}
```

## Deterministic Final Gate 输出契约

```json
{
  "schema_version": "final_gate_output_v1",
  "trace_id": "string",
  "candidate_id": "string",
  "gate_decision": "allow | block | needs_human_review | skip | kill_switch",
  "position_permission": "none | capped | project_policy_default",
  "deterministic_rule_hits": [],
  "threshold_policy_version": "string",
  "risk_policy_version": "string",
  "release_manifest_version": "string",
  "audit_trace_id": "string",
  "gate_reason": "string"
}
```

final gate 必须遵守：

```text
可以读取校准后的 scorer 风险信号、risk_bucket、uncertainty_bucket 和 threshold_policy，但不接受模型直接放行命令。
不得直接服从 Qwen3 recommendation、自然语言建议、raw_score 或未校准概率。
只由 deterministic rules、calibrated risk signal、risk_policy、threshold_policy、release_manifest、human_approval 共同决定。
paper/live 模式下 release_manifest_version 缺失必须 block。
kill_switch 命中时必须优先于所有模型输出。
human_approval_ref 缺失时，不得执行需要人工批准的 release 或 live hard-gate 变更。
```

## Latency / Fallback 契约

hybrid scoring runtime 必须定义每个组件的延迟预算、超时和降级行为：

```json
{
  "schema_version": "phase41_latency_fallback_policy_v1",
  "scorer_timeout_ms": 0,
  "calibrator_timeout_ms": 0,
  "rag_timeout_ms": 0,
  "qwen_audit_timeout_ms": 0,
  "final_gate_timeout_ms": 0,
  "fallback_policy": {
    "scorer_timeout": "fail_to_review | fail_closed",
    "calibrator_timeout": "fail_to_review | fail_closed",
    "rag_no_hit_or_timeout": "qwen_abstain_then_human_review",
    "qwen_timeout": "needs_human_review | fail_closed",
    "final_gate_timeout": "fail_closed"
  }
}
```

硬规则：

```text
任何组件故障不得默认 allow。
paper/live 模式下 final_gate_timeout 必须 fail_closed。
Qwen3 或 RAG 不可用时，不得生成无引用的默认指导。
scorer/calibrator 不可用时，只能 needs_human_review、skip 或 fail_closed，具体取决于 risk_policy。
```

## Audit Trace 契约

每次 hybrid scoring 必须落审计追踪：

```json
{
  "schema_version": "phase41_hybrid_audit_trace_v1",
  "trace_id": "string",
  "created_at": "ISO-8601",
  "project_adapter_id": "string",
  "mode": "string",
  "candidate_id": "string",
  "input_refs": {
    "trade_candidate_snapshot_ref": "string",
    "feature_lineage_manifest_ref": "string",
    "rag_index_version": "string"
  },
  "artifact_versions": {
    "scorer_version": "string",
    "calibrator_version": "string",
    "qwen_model_version": "string",
    "prompt_version": "string",
    "reason_taxonomy_version": "string",
    "threshold_policy_version": "string",
    "risk_policy_version": "string",
    "release_manifest_version": "string"
  },
  "output_refs": {
    "scorer_output_ref": "string",
    "calibrator_output_ref": "string",
    "rag_citation_response_ref": "string",
    "qwen_audit_output_ref": "string",
    "final_gate_output_ref": "string"
  },
  "final_decision": "allow | block | needs_human_review | skip | kill_switch"
}
```

## 错误结构

所有运行时组件的错误必须使用统一结构：

```json
{
  "error": {
    "code": "string",
    "severity": "info | warning | error | critical",
    "component": "scorer | calibrator | rag | qwen_audit | final_gate | trace_writer",
    "message": "string",
    "blocked": true,
    "retryable": false,
    "recommended_next_action": "string"
  }
}
```

关键错误码：

```text
missing_required_version
feature_leakage_detected
post_trade_field_detected
unregistered_model_version
calibration_missing
rag_no_hit
rag_unresolved_conflict
qwen_schema_invalid
qwen_unsupported_claim
final_gate_policy_missing
release_manifest_missing
kill_switch_active
human_approval_required
```

## MCP/SearchLab 调用边界

```text
1. MCP/SearchLab 只读 CEK-TA 正式知识索引。
2. MCP/SearchLab 不接收交易密钥、账户信息、实盘订单或私有项目字段。
3. 查询必须带 canonical_node_id 或 task_type，避免把 Trading 本体错误路由到 AI Engineering。
4. 返回必须带 source/citation/conflict/machine_gate。
5. no-hit、无来源、冲突未消解、machine_gate deny 时，调用方必须降级、阻断或人工复核。
```

## 权限边界

| 组件 | 可以做 | 禁止做 |
| --- | --- | --- |
| Tabular Scorer | 输出分数、风险排序、top features | 直接 allow/block/size |
| Calibrator | 输出校准概率和不确定性 | 绕过阈值策略 |
| Qwen3 Audit Assistant | 输出审计 JSON、reason code、引用、缺字段 | 作为 final gate 或 numeric scorer |
| RAG Citation Resolver | 返回正式知识和来源 | 从候选队列读取默认指导 |
| Deterministic Final Gate | 输出最终 gate_decision | 接受模型自然语言作为放行命令 |
| Trace Writer | 记录审计链路 | 修改交易事实或知识库正式内容 |

## 与 Phase 37 Trading 的边界

```text
K 线结构、指标规则、fill model、滑点、订单状态机、仓位和风控本体归 Trading Engineering。
Phase 41 只读取这些规则的版本、命中结果、摘要引用和约束，不复制规则本体。
如果知识主要描述交易规则本体，应路由到 Phase 37，而不是 KB_AI_*。
```

## Definition of Done

```text
1. 本契约定义全局请求、scorer、calibrator、RAG、Qwen3、final gate 和 audit trace。
2. 明确 Qwen3 和 tabular scorer 不具备最终交易权限。
3. 明确 final gate 是唯一最终交易权限来源。
4. 明确 MCP/SearchLab 只读正式知识索引。
5. 明确错误结构、阻断条件、降级条件和审计追踪字段。
6. 不引入数据库、不部署服务、不新增外部依赖。
7. 文档以 UTF-8 保存，无乱码。
```
