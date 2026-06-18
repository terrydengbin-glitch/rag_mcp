# Phase 40 Champion Challenger Release Contract

生成日期：2026-06-10
状态：contract draft
对应任务：CEK-TA-302

## 目标

本文定义交易 AI gating/scoring 持续学习闭环中的 champion/challenger、shadow/paper/canary、发布审批和回滚治理契约。

本契约承接：

```text
CEK-TA-301: DriftReport、RetrainingTriggerDecision、CandidateModelTrainingRequest、RecalibrationReport、ThresholdStabilityReport
```

并为后续候选知识采集、MCP/SearchLab 查询、Vue3 审计和外接项目 AI IDE 开发提供稳定规则。

核心原则：

```text
challenger 不是 champion。
shadow/paper/canary 只是发布证据，不是自动上线许可。
hard gate 启用必须有人工审批。
发布前必须有 rollback target 和 kill switch。
LLM audit assistant 不能成为最终交易 gate。
```

## 上游输入

| 输入 | 来源 | 用途 |
| --- | --- | --- |
| `CandidateModelTrainingRequest` | CEK-TA-301 | 说明候选模型为何训练、用什么数据训练 |
| `CandidateModelManifest` | 训练平台或外接项目 | 记录候选模型、prompt、RAG 包、校准器或阈值策略版本 |
| `RecalibrationReport` | CEK-TA-301 | 证明概率和关键切片校准情况 |
| `ThresholdStabilityReport` | CEK-TA-301 | 证明阈值策略是否可稳定使用 |
| `DatasetVersionManifest` | CEK-TA-300 | 回链训练、校准、评估、shadow、incident 数据集 |
| `DriftReport` | CEK-TA-301 | 解释为什么需要 challenger 或发布冻结 |
| `FeedbackQualityGateReport` | CEK-TA-300 | 阻断低质量数据驱动的发布 |

## 下游输出

| 输出 | 消费者 |
| --- | --- |
| `ChampionChallengerReview` | 人工审批、SearchLab、Vue3 审计 |
| `ShadowPaperCanaryPlan` | 外接交易项目、评估流水线 |
| `ShadowPaperCanaryReport` | 发布审批、风险复盘 |
| `ReleaseManifest` | MCP/SearchLab、部署系统、回滚治理 |
| `RollbackPlan` | incident response、kill switch、发布回滚 |
| `HumanApprovalRecord` | 审计、合规、任务卡追踪 |

## 模型角色

本契约中的“模型”包括但不限于：

```text
numeric_scorer
calibrator
threshold_policy
llm_audit_prompt
llm_audit_rag_pack
llm_audit_model
deterministic_final_gate_policy
```

边界：

```text
numeric_scorer 可以给风险分和 review priority。
LLM audit assistant 可以输出审计建议、reason code、引用和 unsupported claims。
deterministic final gate 才能执行 allow/block/human_review。
Trading Engineering 的风控本体仍优先于 AI 输出。
```

## ChampionChallengerReview 契约

最小字段：

```yaml
champion_challenger_review_id: string
schema_version: phase40_champion_challenger_review_v1
created_at: iso8601
review_status: draft | reviewed | approved_for_shadow | approved_for_paper | approved_for_canary | rejected | deferred

champion:
  artifact_ref: string
  model_role: numeric_scorer | calibrator | threshold_policy | llm_audit_prompt | llm_audit_rag_pack | llm_audit_model | final_gate_policy
  release_manifest_ref: string
  current_scope: object

challenger:
  artifact_ref: string
  candidate_training_request_id: string | null
  candidate_model_manifest_ref: string
  recalibration_report_ref: string | null
  threshold_stability_report_ref: string | null

comparison:
  offline_eval_report_ref: string
  calibration_report_ref: string | null
  risk_slice_report_ref: string
  false_allow_block_report_ref: string
  human_review_cost_report_ref: string | null
  rag_or_prompt_regression_report_ref: string | null

decision:
  action: reject | collect_more_evidence | approve_shadow | approve_paper | approve_canary | freeze_release
  reason_codes: list[string]
  required_followups: list[string]
  reviewer: string | null
```

硬门：

```text
missing champion artifact -> block_review
missing challenger artifact -> block_review
missing offline_eval_report -> block_review
critical calibration fail -> reject_or_collect_more_evidence
false_allow_cost worsens in critical slice -> reject_or_collect_more_evidence
LLM audit schema regression -> reject_or_prompt_rag_fix
reviewer missing for canary approval -> block_canary
```

## ShadowPaperCanaryPlan 契约

候选通过 champion/challenger review 后，必须先生成验证计划。

最小字段：

```yaml
shadow_paper_canary_plan_id: string
schema_version: phase40_shadow_paper_canary_plan_v1
created_at: iso8601
target_artifact_ref: string
target_model_role: string
planned_stage: shadow | paper | soft_gate | canary

scope:
  strategy_versions: list[string]
  symbols: list[string]
  market_regimes: list[string]
  time_range:
    start: iso8601
    end: iso8601
  traffic_limit: string | null
  capital_limit: string | null
  human_review_required: true | false

guardrails:
  stop_conditions: list[string]
  max_false_allow_cost: string
  max_review_queue_pressure: string
  required_citation_rate: string | null
  required_schema_validity: string | null
  kill_switch_policy_ref: string
```

阶段边界：

| 阶段 | 允许 | 禁止 |
| --- | --- | --- |
| `shadow` | 记录建议，不影响真实交易 | 改变交易决策 |
| `paper` | 模拟或回放环境验证 | 宣称等同实盘收益 |
| `soft_gate` | 给人工复核排序或提示 | 自动 hard block/allow |
| `canary` | 小范围受控启用 | 无 rollback target 上线 |

## ShadowPaperCanaryReport 契约

最小字段：

```yaml
shadow_paper_canary_report_id: string
plan_id: string
created_at: iso8601
stage: shadow | paper | soft_gate | canary
stage_status: pass | warning | fail | stopped | insufficient_data

metrics:
  candidate_count: integer
  allow_count: integer
  block_count: integer
  human_review_count: integer
  false_allow_estimate: string | null
  false_block_estimate: string | null
  review_queue_pressure: low | medium | high | unknown
  schema_validity_rate: string | null
  citation_completeness_rate: string | null
  no_hit_rate: string | null
  latency_summary: object | null

incidents:
  incident_refs: list[string]
  stop_condition_hits: list[string]

decision:
  recommended_next_stage: stop | remain | shadow | paper | soft_gate | canary | release_review
  reason_codes: list[string]
```

硬门：

```text
stage_status fail -> cannot_promote
stop_condition_hits not empty -> freeze_and_review
critical incident -> rollback_review
schema_validity_rate below threshold for LLM audit -> prompt_rag_fix_required
paper/replay fill assumptions missing -> cannot_claim_execution_quality
```

## ReleaseManifest 契约

任何影响外接项目决策链路的发布都必须有 release manifest。

最小字段：

```yaml
release_manifest_id: string
schema_version: phase40_release_manifest_v1
created_at: iso8601
release_status: draft | reviewed | approved | deployed | rolled_back | frozen | rejected
release_type: numeric_scorer | calibrator | threshold_policy | llm_prompt | rag_pack | llm_model | final_gate_policy | composite

artifacts:
  model_artifact_hash: string | null
  calibrator_hash: string | null
  threshold_policy_version: string | null
  prompt_version: string | null
  rag_index_version: string | null
  final_gate_policy_version: string | null
  code_version_hash: string

evidence:
  dataset_manifest_refs: list[string]
  champion_challenger_review_ref: string
  shadow_paper_canary_report_refs: list[string]
  recalibration_report_ref: string | null
  threshold_stability_report_ref: string | null
  security_privacy_review_ref: string | null

scope:
  allowed_strategy_versions: list[string]
  allowed_symbols: list[string]
  allowed_market_regimes: list[string]
  effective_from: iso8601 | null
  expiry_or_review_at: iso8601 | null

controls:
  rollback_plan_ref: string
  kill_switch_policy_ref: string
  monitoring_plan_ref: string
  human_approval_record_ref: string
```

硬门：

```text
missing rollback_plan_ref -> block_release
missing kill_switch_policy_ref -> block_release
missing human_approval_record_ref -> block_release
missing champion_challenger_review_ref -> block_release
missing dataset_manifest_refs -> block_release
release_type composite but missing component hashes -> block_release
LLM model release without prompt/RAG regression -> block_release
```

## RollbackPlan 契约

最小字段：

```yaml
rollback_plan_id: string
schema_version: phase40_rollback_plan_v1
created_at: iso8601
target_release_manifest_id: string
rollback_target_release_manifest_id: string
rollback_scope:
  components: list[numeric_scorer | calibrator | threshold_policy | llm_prompt | rag_pack | llm_model | final_gate_policy]
  strategy_versions: list[string]
  symbols: list[string]
  market_regimes: list[string]

triggers:
  incident_severity_threshold: string
  metric_thresholds: object
  manual_override_allowed: true | false
  kill_switch_policy_ref: string

procedure:
  steps: list[string]
  owner: string
  expected_recovery_time: string
  verification_checks: list[string]
```

回滚后要求：

```text
冻结相关 release manifest。
记录 incident 或 rollback audit trace。
停止同一 artifact 的进一步 canary。
回填 feedback/label/dataset 中的事故样本。
必要时降低 machine_gate 或 review_status，不直接删除知识。
```

## HumanApprovalRecord 契约

最小字段：

```yaml
human_approval_record_id: string
created_at: iso8601
approver: string
approval_scope: shadow | paper | canary | release | rollback
approved_object_type: champion_challenger_review | shadow_paper_canary_plan | release_manifest | rollback_plan
approved_object_id: string
decision: approve | reject | defer
reason_codes: list[string]
required_followups: list[string]
```

禁止：

```text
external_ai 直接审批 release。
Codex 自动批准 hard gate。
无审批记录启用 live hard gate。
用 reviewed 知识状态替代发布审批。
```

## 发布决策流

```text
CandidateModelManifest
  -> ChampionChallengerReview
  -> ShadowPaperCanaryPlan
  -> ShadowPaperCanaryReport
  -> ReleaseManifest
  -> HumanApprovalRecord
  -> Controlled Deployment
  -> Monitoring
  -> RollbackPlan / Incident Review
```

不可跳过的门禁：

```text
candidate model -> release
offline eval -> hard gate
shadow pass -> live full traffic
paper pass -> live full traffic
LLM audit assistant -> final gate
approved knowledge -> release approval
```

## 与 MCP/SearchLab/Vue3 的关系

| 组件 | 使用方式 |
| --- | --- |
| MCP | 检索本契约，返回发布、回滚、审批、shadow/paper/canary 的规则和来源 |
| SearchLab | 验证外接 AI 能按“challenger 能否上线”“缺少 rollback 是否阻断”等问题命中知识 |
| Vue3 知识树 | 展示 champion/challenger、shadow/paper/canary、rollback governance 覆盖情况 |
| 候选审计页 | 审计 Phase 40 相关候选知识是否有来源、边界和机器门控 |

## 与 Trading Engineering 的边界

本契约不定义：

```text
交易策略有效性
K 线形态规则
订单状态机
风控阈值本体
fill model
实盘执行适配器
交易所故障处理
```

本契约只要求发布时引用这些组件的版本、契约和风险状态。

## CEK-TA-302 DoD

```text
1. 本契约文件存在。
2. 已定义 ChampionChallengerReview、ShadowPaperCanaryPlan、ShadowPaperCanaryReport、ReleaseManifest、RollbackPlan、HumanApprovalRecord。
3. 已明确 challenger 不等于 champion。
4. 已明确 shadow/paper/canary 不等于自动上线许可。
5. 已明确 hard gate 启用必须有人工审批。
6. 已明确 release 必须有 rollback target 和 kill switch。
7. 已写清与 MCP/SearchLab/Vue3 和 Trading Engineering 的边界。
8. UTF-8 无乱码。
```
