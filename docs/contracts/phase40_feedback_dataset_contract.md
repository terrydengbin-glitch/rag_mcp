# Phase 40 Feedback Dataset Contract

生成日期：2026-06-10
状态：contract draft
对应任务：CEK-TA-300

## 目标

本文定义交易 AI gating/scoring 持续学习闭环中的反馈日志、标签更新、数据集版本和审计追踪契约。

它承接 Phase 38 的训练数据与评估契约，但关注点不同：

```text
Phase 38: 第一版 POC 如何构造训练、校准、评估、shadow/paper 和发布前数据。
Phase 40: 模型长期运行后，如何持续记录反馈、刷新标签、构建新版本数据集，并保持可审计、可回滚、不可自动上线。
```

核心原则：

```text
所有候选都要记录，不只记录成交交易。
标签不能只看 PnL。
反馈记录不是训练真值，必须经过标签策略和审计门禁。
再训练数据集必须可追溯到原始 feedback、label、schema、策略版本和审计记录。
任何反馈数据都不能绕过 reviewed/approved 知识治理和人工审批。
```

## 上游输入

| 输入 | 来源 | 用途 |
| --- | --- | --- |
| `TradeCandidateSnapshot` | Phase 38 / 外接交易项目 | 记录决策时可见的候选交易事实 |
| `DecisionTimeFeatureFrame` | Phase 38 / 特征生成链路 | 记录模型真实可见特征 |
| `NumericScorerOutput` | Phase 38 numeric scorer | 记录数值打分与风险排序 |
| `LlmAuditOutput` | Phase 38 LLM audit assistant | 记录 LLM 审计建议、引用、unsupported claims |
| `FinalGateDecision` | Phase 38 deterministic final gate | 记录最终 allow/block/human_review |
| `ExecutionOrBlockOutcome` | 交易执行或阻断链路 | 记录执行结果或阻断原因 |
| `PostTradeOutcome` | 事后复盘链路 | 仅用于标签观察，不得进入决策时输入 |
| `HumanReviewRecord` | 人工审核链路 | 记录修正意见、复核原因和 reviewer |
| `KnowledgeRefs` | CEK-TA formal knowledge index | 记录当时可引用的知识版本 |

## 下游输出

| 输出 | 消费者 |
| --- | --- |
| `FeedbackRecord` | label refresh、drift monitor、incident review |
| `LabelUpdateRecord` | dataset builder、eval set、gold set |
| `DatasetVersionManifest` | retraining pipeline、calibration pipeline、MCP/SearchLab 审计 |
| `AuditTraceRecord` | 人工审计、发布审批、回滚复盘 |
| `FeedbackQualityGateReport` | Phase 40 候选知识、外接项目 CI、Vue3 审计页 |

## 生命周期状态

### FeedbackRecord 状态

```text
captured -> sanitized -> schema_checked -> lineage_checked -> label_pending -> label_ready -> dataset_candidate -> archived
```

状态含义：

| 状态 | 含义 |
| --- | --- |
| `captured` | 原始反馈已捕获，尚未脱敏和校验 |
| `sanitized` | 已去除私有字段、账户、密钥和项目私有策略正文 |
| `schema_checked` | 通过 schema、必填字段、枚举值和时间字段校验 |
| `lineage_checked` | 决策时特征和事后结果隔离已校验 |
| `label_pending` | 等待标签刷新或人工复核 |
| `label_ready` | 标签已经生成并通过基础审计 |
| `dataset_candidate` | 可进入数据集候选池，但还不是训练集 |
| `archived` | 已归档，仅用于审计或事故复盘 |

禁止跳转：

```text
captured -> dataset_candidate
label_pending -> retraining_dataset
schema_failed -> label_ready
lineage_failed -> dataset_candidate
```

### LabelUpdateRecord 状态

```text
proposed -> reviewed -> accepted -> superseded
proposed -> rejected
```

硬规则：

```text
proposed 不能直接进入训练集。
reviewed 不等于 gold label。
accepted 仍需绑定 label_policy_version。
superseded 必须保留旧标签引用，不能覆盖删除。
```

## FeedbackRecord 契约

最小字段：

```yaml
feedback_record_id: string
schema_version: phase40_feedback_record_v1
source_project_id: string
source_project_type: backtest | replay | paper | live | research
created_at: iso8601
captured_at: iso8601
status: captured | sanitized | schema_checked | lineage_checked | label_pending | label_ready | dataset_candidate | archived

candidate_snapshot_ref: string
decision_time_feature_frame_ref: string
numeric_scorer_output_ref: string | null
llm_audit_output_ref: string | null
final_gate_decision_ref: string
execution_or_block_outcome_ref: string
post_trade_outcome_ref: string | null
human_review_ref: string | null

strategy_version: string
symbol: string
timeframe: string | null
market_regime: string | null
decision_time: iso8601
label_observation_end_time: iso8601 | null

knowledge_index_version: string
retrieved_knowledge_refs: list[string]
feature_schema_version: string
scorer_version: string | null
llm_audit_version: string | null
final_gate_policy_version: string

privacy_status: raw | sanitized | rejected_private_data
lineage_status: unchecked | pass | fail
quality_gate_status: unchecked | pass | needs_review | block
```

必须记录的候选范围：

```text
allow: 进入执行或模拟执行的候选。
block: 被 deterministic final gate 阻断的候选。
skip: 因数据不足、RAG no-hit、冲突、权限或系统异常跳过的候选。
human_review: 进入人工复核的候选。
error: 因工具、交易适配器、数据源或检索失败产生的候选。
```

禁止：

```text
只记录 allow 或成交交易。
把 post_trade_outcome 写入 decision_time_feature_frame。
把 LLM 自己的解释直接当作标签。
把未脱敏账号、密钥、私有策略正文写入 FeedbackRecord。
用 FeedbackRecord 直接训练模型。
```

## TradeCandidateSnapshot 回链要求

`FeedbackRecord` 不重复保存完整候选交易事实，而是必须回链到 `TradeCandidateSnapshot`。

回链必须能回答：

```text
1. 当时是什么策略版本？
2. 当时看到哪些市场、风险、执行上下文？
3. 当时哪些特征在 decision_time 前可用？
4. 当时引用了哪些 CEK-TA reviewed/approved 知识？
5. 当时 final gate 为什么 allow/block/human_review/skip？
```

如果缺少 `candidate_snapshot_ref`：

```text
status = schema_failed
quality_gate_status = block
不能进入 label_ready 或 dataset_candidate
```

## FinalGateDecision 回链要求

最小字段：

```yaml
final_gate_decision_id: string
decision: allow | block | skip | human_review | error
decision_time: iso8601
policy_version: string
reason_codes: list[string]
risk_gate_refs: list[string]
numeric_scorer_output_ref: string | null
llm_audit_output_ref: string | null
retrieved_knowledge_refs: list[string]
unsupported_claims: list[string]
missing_required_fields: list[string]
operator_override_ref: string | null
```

硬门：

```text
decision 缺失 -> block_feedback
reason_codes 缺失 -> needs_review
policy_version 缺失 -> block_feedback
human_review 但没有 human_review_ref -> needs_review
allow 但风险 gate 未记录 -> block_release_dataset
```

## LabelUpdateRecord 契约

最小字段：

```yaml
label_update_id: string
feedback_record_id: string
label_policy_version: string
created_at: iso8601
created_by: rule | human | hybrid | postmortem
status: proposed | reviewed | accepted | rejected | superseded

primary_label:
  bad_trade_flag: true | false | unknown
  trade_quality_bucket: good | neutral | bad | unknown
  review_priority: low | medium | high | critical

quality_dimensions:
  rule_compliance_quality: pass | fail | unknown
  risk_quality: pass | fail | unknown
  execution_quality: pass | fail | unknown
  setup_quality: strong | medium | weak | unknown
  market_regime_fit: good | neutral | poor | unknown

cost_dimensions:
  realized_pnl_bucket: gain | flat | loss | unknown
  false_allow_cost_bucket: none | low | medium | high | unknown
  false_block_cost_bucket: none | low | medium | high | unknown
  review_cost_bucket: low | medium | high | unknown

explanation:
  label_reason_codes: list[string]
  evidence_refs: list[string]
  human_review_ref: string | null
  post_trade_outcome_ref: string | null
  uncertainty_notes: string | null
```

标签原则：

```text
PnL 是结果字段，不是唯一标签。
好亏损 good loss 不能简单标成 bad。
坏盈利 bad win 不能简单标成 good。
被阻断候选不能在没有反事实证据时标成 loss。
人工复核可以提出标签修正，但必须保留 reviewer、reason 和版本。
```

阻断规则：

```text
label based only on realized_pnl -> block_label
missing label_reason_codes -> needs_review
human label without reviewer trace -> needs_review
model output used as own label -> block_feedback_loop
post_trade field used before decision_time -> block_lineage
```

## DatasetVersionManifest 契约

每次构建持续学习数据集必须生成独立 manifest。

最小字段：

```yaml
dataset_version_id: string
dataset_role: research | training | calibration | validation | test | gold | shadow | incident
created_at: iso8601
created_by: string
source_project_ids: list[string]
time_range:
  start: iso8601
  end: iso8601

source_feedback_record_ids: list[string]
source_label_update_ids: list[string]
excluded_feedback_record_ids: list[string]
exclusion_reason_codes: list[string]

feature_schema_version: string
label_policy_version: string
knowledge_index_version: string
scorer_version_scope: list[string]
llm_audit_version_scope: list[string]
final_gate_policy_version_scope: list[string]
strategy_version_scope: list[string]
symbol_scope: list[string]
market_regime_scope: list[string]

split_policy:
  split_method: time_based | group_based | stratified_time | manual
  embargo_policy: string
  dedup_policy: string
  leakage_scan_report_ref: string

hashes:
  dataset_hash: string
  manifest_hash: string
  source_index_hash: string

review:
  reviewer: string | null
  review_status: draft | reviewed | approved_for_training | rejected
  reviewed_at: iso8601 | null
```

数据集角色边界：

| 角色 | 允许用途 | 禁止用途 |
| --- | --- | --- |
| `research` | 探索、错误分析、候选特征研究 | 训练或发布指标宣称 |
| `training` | 训练 candidate model | 校准、最终评估、gold set |
| `calibration` | 概率校准、阈值策略 | 模型训练 |
| `validation` | 训练期间选择超参 | 最终发布宣称 |
| `test` | 冻结评估 | 训练、校准 |
| `gold` | 回归测试、人审一致性 | 训练 |
| `shadow` | shadow/paper 观察池 | 训练前泄漏 |
| `incident` | 事故复盘和修复验证 | 未审计直接训练 |

硬门：

```text
training 与 calibration 重叠 -> block_dataset
training 与 test 重叠 -> block_dataset
gold set 被训练使用 -> block_release
dataset_hash 缺失 -> block_release
label_policy_version 缺失 -> block_dataset
knowledge_index_version 缺失 -> needs_review
```

## AuditTraceRecord 契约

每次状态变化、标签变化、数据集构建和人工审批必须记录审计追踪。

最小字段：

```yaml
audit_trace_id: string
object_type: feedback_record | label_update | dataset_manifest | release_manifest
object_id: string
event_type: created | status_changed | label_changed | excluded | included | reviewed | approved | rejected | superseded
event_time: iso8601
actor_type: system | codex | human | external_ai
actor_id: string
before_state: object | null
after_state: object
reason_codes: list[string]
source_refs: list[string]
related_task_id: string | null
```

审计要求：

```text
任何状态变更必须可回放。
任何人工覆盖必须有 human_review_ref。
任何 external_ai 建议必须回到 Codex/人工治理流程，不得直接改 approved。
任何删除都必须以 superseded/archive 表达，不得物理抹除审计链。
```

## FeedbackQualityGateReport 契约

每次把 feedback/label/dataset 推向后续再训练或审计时，必须生成质量门禁报告。

最小字段：

```yaml
quality_gate_report_id: string
created_at: iso8601
scope:
  dataset_version_id: string | null
  feedback_record_count: integer
  label_update_count: integer
checks:
  schema_check: pass | fail
  privacy_check: pass | fail
  lineage_check: pass | fail
  label_policy_check: pass | fail
  split_overlap_check: pass | fail | not_applicable
  source_trace_check: pass | fail
  feedback_loop_risk_check: pass | fail | needs_review
decision: pass | needs_review | block
blocking_reasons: list[string]
review_required: true | false
```

## 存储约定

本 Phase 不新增数据库，默认只定义文件化契约和外接项目可实现的 schema。

建议外接项目实现时至少保留：

```text
feedback_records/
label_updates/
dataset_manifests/
audit_traces/
quality_gate_reports/
```

CEK-TA 本项目只沉淀通用知识、任务卡、契约、审计包和 reviewed 知识，不保存外接项目私有交易明细。

## 与 MCP/SearchLab/Vue3 的关系

| 组件 | 约束 |
| --- | --- |
| MCP | 只读检索本契约和相关 reviewed 知识，不写入外接项目 feedback |
| SearchLab | 用于测试“持续学习/标签/数据集版本”相关知识能否命中和引用 |
| Vue3 知识树 | 展示 Phase 40 L3 专题覆盖、候选、缺口和来源状态 |
| 候选审计页 | 审计 Phase 40 候选知识，不审计外接项目私有 feedback 数据 |
| 回灌机制 | 其他项目只能提交脱敏后的通用经验，不得倒灌私有交易流水 |

## 与 Phase 37 Trading Engineering 的边界

以下内容必须路由到 Trading Engineering，不进入本契约：

```text
K 线形态规则
市场微观结构解释
回测 fill model
订单状态机
实盘仓位同步
交易所异常处理
风控本体阈值
```

本契约只允许引用这些事实的摘要或引用 ID，用于解释为什么某个 feedback/label/dataset 需要保留上下文。

## CEK-TA-300 DoD

```text
1. 本契约文件存在。
2. 已定义 FeedbackRecord、LabelUpdateRecord、DatasetVersionManifest、AuditTraceRecord。
3. 已定义 feedback 和 label 生命周期状态。
4. 已定义阻断规则和质量门禁。
5. 已写清与 Phase 38、Phase 37、MCP/SearchLab/Vue3 的上下游边界。
6. 明确不新增数据库、不训练真实模型、不自动上线。
7. UTF-8 无乱码。
```
