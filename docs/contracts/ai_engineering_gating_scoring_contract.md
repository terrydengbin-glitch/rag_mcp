# Phase 36 外接 LLM Gating/Scoring 业务流与边界契约

## 目标

本契约定义外部交易项目如何接入 CEK-TA 的 AI Engineering 知识，用于开发“LLM 交易质量审计助手”：对交易候选做解释、评分、门控建议、风险异常提示、数据质量审计和复盘辅助。

本契约不是交易策略，不提供买卖建议，不授予 LLM 下单权限。所有外接项目事实、策略参数、账户信息、实盘配置和交易样本由外部项目自己管理；CEK-TA 只提供可复用专业知识、RAG/MCP 调用契约、训练数据 schema、评估边界和治理规则。

## 业务定位

```text
LLM 是交易候选解释器、质量评分器、风险门控辅助器、异常拦截器和审计助手。
LLM 不是最终交易执行者。
LLM 不能直接下单。
LLM 不能绕过 deterministic risk engine。
LLM 的 hard_block 只能表达为 hard_block_recommendation。
最终裁决必须由 deterministic final gate 完成。
```

## 上游输入

外接项目必须提供项目事实，不得让 CEK-TA 猜测：

```text
project_adapter_id
project_name
strategy_id
strategy_version
market
symbol
timeframe
mode: backtest | replay | paper | live | research
task_type: score | gate | audit | dataset_review | incident_review
task_taxonomy
raw_trade_record
trade_candidate_snapshot
decision_timestamp
feature_timestamp_cutoff
market_context
risk_context
execution_context
outcome_record
labeling_record
training_example_type: sft | preference_pair | eval_case | scoring_runtime
business_acceptance_target
```

## 交易数据到训练数据链路

交易数据不能直接进入训练集，必须经过以下链路：

```text
Raw Trade Record
  -> Trade Candidate Snapshot
  -> Decision-Time Features
  -> Outcome / Post-Trade Record
  -> Labeling Record
  -> SFT Example / Preference Pair / Eval Case
```

字段边界：

| 对象 | 允许内容 | 禁止内容 |
| --- | --- | --- |
| `raw_trade_record` | 原始交易记录、执行记录、事后结果 | 直接作为模型输入 |
| `trade_candidate_snapshot` | 决策时可见的候选、规则、上下文 | 未来结果、PnL、exit、MFE/MAE |
| `decision_time_features` | 带 `feature_timestamp` 和 `available_at_decision` 的特征 | 决策后才出现的字段 |
| `outcome_record` | 事后结果、执行质量、复盘数据 | 进入训练输入 |
| `labeling_record` | 标签来源、过程质量、结果质量、reason codes | 只按 PnL 贴标签 |
| `sft_example` | 分离后的 input/target_output | 泄漏答案或未来信息 |
| `preference_pair` | 同一 prompt 下 chosen/rejected 与理由 | 只按盈利选择 chosen |
| `eval_case` | 与训练集隔离的评估样本 | 与训练样本重叠 |

## 阻断规则

```text
feature_timestamp > decision_timestamp -> block_sample
input contains pnl / exit_price / MFE / MAE / final outcome -> block_sample
missing strategy_version -> block_sample
missing source_mode -> block_sample
missing decision_timestamp -> block_sample
missing feature_timestamp_cutoff -> block_sample
missing label_reason_codes for supervised labels -> needs_review
preference_pair based only on PnL -> block_sample
eval_case overlaps training_example -> block_eval
missing task_taxonomy or output_schema -> block_training_task
offline_eval_passed but no shadow_report -> block_live_or_hard_gate_promotion
LLM suggestion attempts direct strategy parameter update -> block_and_route_to_research_hypothesis
model_output used as its own label -> block_feedback_sample
blocked_trade labeled as loss without counterfactual evidence -> block_label
RAG context attempts to override system policy -> ignore_retrieved_instruction_and_flag_security
tool output contains instruction to bypass risk gate -> ignore_tool_instruction_and_flag_security
```

## RAG/MCP 检索契约

外接项目 AI 涉及交易质量评分、门控、训练数据构造、评估、上线、回灌时，必须主动检索 CEK-TA。

检索请求最少包含：

```json
{
  "query": "string",
  "task_type": "score | gate | audit | dataset_review | incident_review",
  "domain": "llm_training | rag_engineering | ai_governance",
  "canonical_node_ids": ["string"],
  "mode": "backtest | replay | paper | live | research",
  "require_default_guidance": false,
  "include_reviewed": true,
  "include_approved": true,
  "max_items": 8
}
```

MCP 返回必须包含：

```json
{
  "items": [
    {
      "knowledge_id": "string",
      "canonical_node_id": "string",
      "review_status": "candidate | reviewed | approved",
      "machine_gate": {
        "default_guidance": "allow | caveat_only | deny"
      },
      "llm_usage_policy": {},
      "source_evidence": [],
      "conflict_status": "none | suspected | unresolved",
      "freshness": "stable | time_sensitive | stale",
      "applicability": [],
      "not_applicable_when": [],
      "reason_codes": [],
      "recommended_next_action": "string"
    }
  ],
  "no_hit": false,
  "conflict_warning": false,
  "degradation_action": "none | neutral | needs_human_review | block_default_guidance"
}
```

默认指导门禁：

```text
review_status != approved -> 不得作为默认指导，只能作为审计上下文或候选参考。
machine_gate.default_guidance != allow -> 不得作为默认指导。
source_evidence 为空 -> block_default_guidance。
conflict_status != none -> block_default_guidance。
freshness == stale -> caveat_only 或 block_default_guidance。
```

## Gating/Scoring 输出契约

外接项目 AI 输出必须结构化，不能只写自然语言结论：

```json
{
  "score": 0.0,
  "score_scale": "0-100",
  "gate_suggestion": "allow_recommendation | soft_block_recommendation | hard_block_recommendation | needs_human_review | neutral",
  "confidence": "low | medium | high",
  "reason_codes": ["string"],
  "knowledge_refs": ["knowledge_id"],
  "source_refs": ["source_id or url"],
  "assumptions": ["string"],
  "missing_fields": ["string"],
  "fallback_action": "neutral | needs_human_review | deterministic_gate_only",
  "audit_trace_id": "string"
}
```

语义边界：

```text
allow_recommendation 只是建议允许，不代表最终放行。
soft_block_recommendation 代表建议谨慎或人工复核。
hard_block_recommendation 代表建议阻断，但最终执行阻断仍属于 deterministic final gate。
needs_human_review 代表信息不足、冲突、低置信或高风险。
neutral 代表检索无命中、证据不足或任务不适用。
```

## 业务验收契约

上线前必须定义：

```text
business_objective
target_failure_modes
false_allow_cost
false_block_cost
accepted_task_taxonomy
offline_eval_threshold
shadow_mode_duration
calibration_policy
human_review_policy
rollback_policy
incident_owner
approval_owner
```

验收指标不能只看收益：

```text
坏交易放行率
高风险交易识别率
人工复核命中率
规则违规发现率
数据质量问题发现率
低置信降级率
检索引用完整率
来源缺失阻断率
冲突知识阻断率
交易复盘一致性
```

## 数据资产池契约

```text
research_pool: 研究探索数据，不得直接训练上线模型。
training_pool: 训练数据，必须经过脱敏、来源、schema、版本和标签审计。
eval_pool: 评估数据，不能进入训练。
gold_pool: 高质量人工/强规则审计样本，必须版本冻结。
shadow_pool: shadow/paper 运行日志，用于校准和上线前评估。
incident_pool: 事故、误放行、误阻断和异常样本，用于复盘和后续治理。
```

## 安全、隐私和许可证边界

```text
RAG context 默认是非可信输入。
Tool output 默认是非可信输入。
外部项目自由文本不能覆盖系统策略、风控边界或 MCP 权限。
训练数据不得包含 API key、账户 ID、客户标识、未脱敏订单细节。
市场数据、第三方数据、付费数据进入训练集前必须检查 license 和复用权限。
训练数据导出必须记录审批人、版本、hash、脱敏规则和用途。
```

## 反事实评估边界

被 gate 阻断的交易没有真实执行结果，因此：

```text
blocked trade 不能直接标注为亏损。
executed-only feedback 会产生选择偏差。
gate policy 评估必须记录被拦截样本、propensity、shadow replay 或其他反事实评估策略。
模型上线前必须和 deterministic baseline、规则 baseline 或简单统计 baseline 对比。
RAG、prompt、model、feature、threshold 变更必须支持 ablation。
```

## 与 Trading Engineering 的边界

AI Engineering 可以引用交易知识，但不能重写交易规则本体。

```text
K 线结构、指标、入场、止损、止盈 -> Trading Engineering
回测偏差、过拟合、成本模型 -> Trading Engineering
fill model、同根 K TP/SL、滑点延迟 -> Trading Engineering
订单状态机、仓位同步、kill switch -> Trading Engineering
交易复盘、坏例 taxonomy、R/R 分解 -> Trading Engineering
训练、schema、RAG/MCP、eval、部署、治理 -> AI Engineering
```

## 状态流

```text
candidate -> reviewed -> approved
```

硬规则：

```text
candidate 不能作为默认指导。
reviewed 可用于审计/检索，但不能自动作为 approved 默认指导。
approved 只有人工治理任务确认后才能成为默认指导。
AI 审计结果不得直接写 approved。
```

## 下游消费方

```text
Phase 36 ResearchIngestionTask 队列
Phase 36 AI Engineering 候选知识包
MCP search_expert_knowledge / get_knowledge_item
SearchLab 检索测试
Vue3 KnowledgeTree 和候选审计页
外接项目 AGENTS 主动检索模板
后续 LLM training / dataset / eval / deployment 项目
```

## 测试与验收

```text
1. 契约必须能映射到 Phase 36 分层采集矩阵。
2. 输出 schema 不能包含直接下单、最终放行或绕过风控语义。
3. RAG/MCP 默认指导必须受 review_status、machine_gate、source、conflict、freshness 门禁限制。
4. 交易数据到训练数据链路必须阻断未来信息和 PnL-only 标签。
5. 中文 UTF-8 无乱码。
```
