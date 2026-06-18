# Phase 36 AI Engineering 知识树扩展框架

本文定义 Phase 36 的 AI Engineering 知识扩展蓝图，用于后续联网采集、候选知识生成、审计、formal reviewed 沉淀和 MCP/SearchLab/KnowledgeTree 验证。

本文不是正式知识卡，不提供默认指导。所有具体知识点必须经过来源评分、冲突审计、候选审核和 formal reviewed/approved 治理流程。

## 核心分层

AI Engineering 必须分成两层：

```text
通用 LLM / ML Training Engineering
  -> 交易数据到训练数据的 schema 转换链路
  -> 交易 LLM 任务分类和训练方法选择
  -> 交易 gating / scoring 专用训练约束
  -> 合格 LLM 交易质量审计助手业务闭环
```

原因：

```text
1. 外接项目要训练 LLM 做交易 gating/scoring，不能只有交易安全边界。
2. 训练系统还需要数据集构造、SFT/DPO/PEFT、eval、训练运行管理、训练服务一致性等通用模型训练工程知识。
3. 交易记录不能直接训练 LLM，必须经过 Raw Trade -> Candidate Snapshot -> Decision-Time Features -> Outcome -> Labels -> SFT/Preference/Eval 的 schema 转换链路。
4. 交易 LLM 实际包含 pre-trade scoring、gating、post-trade review、incident explanation、research suggestion 等不同任务，不能混成一个训练任务。
5. 合格 LLM 交易质量审计助手必须有业务验收标准、标签工厂、数据资产分层、线上决策协议、风险账本和反馈治理。
6. 交易 gating/scoring 是高风险决策辅助任务，必须在通用训练工程和训练数据 schema 工程之上再加交易安全约束。
```

## AI Engineering 目标知识树

```text
AI Engineering

KB_09 LLM Training

  KB_09A Model Training Engineering
    1. Training Objective
    2. Dataset Construction
    3. Data Leakage / Contamination
    4. Supervised Fine-Tuning
    5. Preference Training / DPO / RLHF
    6. PEFT / LoRA / QLoRA
    7. Evaluation / Evals
    8. Training Run Management
    9. Safety / Alignment Boundary
    10. Training-Serving Consistency

  KB_09C Training Dataset Schema Engineering
    1. Raw Trade Data Normalization
    2. Trade Candidate Snapshot Schema
    3. Decision-Time Feature Schema
    4. Outcome / Post-Trade Schema
    5. Labeling Schema
    6. Training Example Schema
    7. Preference Pair Schema
    8. Eval Case Schema

  KB_09D Trading LLM Task Taxonomy
    1. Trade Candidate Scoring
    2. Trade Gate Decision
    3. Risk Violation Detection
    4. Data Quality Audit
    5. Strategy Rule Compliance Audit
    6. Post-Trade Review
    7. Incident Explanation
    8. Parameter / Rule Improvement Suggestion

  KB_09E Training Method Selection
    1. RAG First Baseline
    2. SFT Boundary
    3. Preference / DPO Boundary
    4. Eval Baseline Before Fine-Tune
    5. Do Not Train Around Data Problems

  KB_09B Trading Scoring / Gating Training
    1. Trading Role Boundary
    2. Trade Sample Schema
    3. Trading Labeling & Leakage
    4. Scoring / Gating Rubric
    5. Trading Eval & Calibration
    6. Trading Safety Gate

KB_10 RAG Engineering
  1. Retrieval Decision Policy
  2. Metadata / Machine Gate Filtering
  3. Token & Context Budget
  4. Trading Scoring RAG Pack
  5. Citation / Evidence Contract
  6. Retrieval Quality Evaluation

KB_11 MCP / Agent Engineering
  1. MCP Tool Contract
  2. Tool Permission Enforcement
  3. External AI Calling Protocol
  4. Gating / Scoring Agent Flow
  5. Error / No-hit / Conflict Degradation
  6. Agent Non-Delegation Boundary

KB_AI_12 LLMOps / Deployment
  1. Offline Evaluation
  2. Shadow / Paper / Live Rollout
  3. Artifact Lineage
  4. Release Control
  5. Monitoring & Drift
  6. Rollback & Incident Response
  7. Deployment Readiness Gate

KB_AI_13 AI Governance / Audit
  1. Training Data Governance
  2. Knowledge Usage Permission
  3. Human Review Workflow
  4. External Contribution Backflow
  5. Model Output Audit
  6. Dataset Card / Model Card
  7. Incident Governance
  8. Approval / Ownership Workflow

KB_AI_14 Trading AI Safety / Risk Control
  1. Deterministic Risk Gate Precedence
  2. False Allow / False Block Cost Policy
  3. Kill Switch / Emergency Disable
  4. Human Escalation Boundary
  5. Live Trading Permission Boundary
  6. Trading LLM Red Team

KB_AI_15 Business Objective / Acceptance Criteria
  1. LLM Trader Role Definition
  2. Quality Improvement Metrics
  3. Business Cost Metrics
  4. Live Readiness Criteria

KB_AI_16 Label Factory / Annotation Workflow
  1. Auto Label
  2. Human Label
  3. Label Conflict Resolution
  4. Gold Set
  5. Label Quality Score

KB_AI_17 Data Asset Management
  1. Research Pool
  2. Training Pool
  3. Eval Pool
  4. Gold Pool
  5. Shadow Pool
  6. Incident Pool

KB_AI_18 Continuous Learning / Feedback Governance
  1. Live Feedback Boundary
  2. Retraining Dataset Release
  3. Knowledge Backfill
  4. Feedback Loop Risk

KB_AI_19 AI Security / Privacy / Compliance
  1. Prompt Injection / RAG Security
  2. Tool Output Untrusted Boundary
  3. Secret / Account Identifier Redaction
  4. Trade Data Sanitization
  5. Market Data License / Permission
  6. Training Export Approval
```

## UI 三层映射

为了兼容现有知识树 UI 的三层结构，`KB_09A`、`KB_09C`、`KB_09D`、`KB_09E` 和 `KB_09B` 在 UI 中作为 `KB_09 LLM Training` 下的 L3 专题：

```text
L1: AI Engineering
L2: KB_09 LLM Training
L3: KB_09A Model Training Engineering
L3: KB_09C Training Dataset Schema Engineering
L3: KB_09D Trading LLM Task Taxonomy
L3: KB_09E Training Method Selection
L3: KB_09B Trading Scoring / Gating Training
```

`KB_09A` 内部 10 个方向、`KB_09C` 内部 8 个方向、`KB_09D` 内部 8 个任务类型、`KB_09E` 内部 5 个方法选择方向先进入采集矩阵，不作为 UI 的第四级目录。后续如果知识量达到上千条，再评估是否引入专题页内分组或虚拟分组。

## 采集优先级分层

审计融合后，原 101 条不再全部视为同等 P0。它们保留为第一批采集池，并按下列规则重排：

```text
P0-Core：安全启动硬门；缺失或违反时，训练、评估、上线或默认指导必须阻断。
P0-Extended：第一轮工程建设必需；用于补齐上线前的评估、治理、追踪和审计能力。
P1：优化增强项；包括更细的 scoring rubric 维度、更多 drift 指标、更多 risk ledger 细项和方法深挖。
```

原始采集池：

```text
A. 通用模型训练工程：20 条
B. 训练专属 schema 工程：20 条
C. 交易 gating/scoring：36 条
D. 业务闭环治理：25 条
```

新增关键硬门：

```text
N01. eval.counterfactual_outcome_missing_for_blocked_trades.v1
N02. eval.off_policy_evaluation_required_for_gate_policy.v1
N03. eval.blocked_trade_cannot_be_labeled_as_loss.v1
N04. security.rag_context_is_untrusted_input.v1
N05. security.prompt_injection_test_required_for_trade_context.v1
N06. data_privacy.no_secret_or_account_identifier_in_training.v1
N07. data_license.market_data_license_check_required.v1
N08. eval.deterministic_baseline_required_before_llm_gate.v1
N09. eval.ablation_required_for_rag_prompt_model_components.v1
N10. label_factory.inter_annotator_agreement_required.v1
N11. feature_store.feature_schema_registry_required.v1
N12. serving_consistency.training_serving_parity_test_required.v1
```

降级为 P1 的典型条目：

```text
scoring_rubric.setup_quality.v1
scoring_rubric.risk_reward_quality.v1
scoring_rubric.market_regime_fit.v1
scoring_rubric.rule_compliance.v1
scoring_rubric.uncertainty_penalty.v1
部分 risk_ledger、monitoring drift、research_feedback 细项
```

重复项处理：

```text
schema 组负责字段定义。
gating 组负责缺字段时的阻断、降级或人工复核。
dataset / eval / eval_case / time_split 可以共存，但必须建立 depends_on，不得重复表达同一规则。
```

### A. 通用模型训练工程采集池

```text
T01. training_objective.task_definition_required.v1
T02. training_objective.rag_vs_finetune_boundary_required.v1
T03. dataset.schema_required.v1
T04. dataset.source_lineage_required.v1
T05. dataset.version_and_hash_required.v1
T06. dataset.train_validation_test_split_required.v1
T07. dataset.deduplication_required.v1
T08. dataset.dataset_card_required.v1
T09. leakage.train_test_contamination_block.v1
T10. leakage.label_in_input_forbidden.v1
T11. sft.when_to_use_and_not_use.v1
T12. sft.output_schema_consistency_required.v1
T13. preference_training.preference_pair_schema_required.v1
T14. preference_training.chosen_rejected_reason_required.v1
T15. dpo.preference_data_quality_required.v1
T16. eval.holdout_test_set_required.v1
T17. eval.production_like_eval_required.v1
T18. training_run.config_and_hyperparameter_snapshot_required.v1
T19. serving_consistency.train_like_serve_required.v1
T20. safety.no_tool_permission_escalation.v1
```

### B. 训练专属 schema 工程采集池

```text
S01. trade_data.raw_trade_record_required_fields.v1
S02. trade_data.strategy_id_and_version_required.v1
S03. trade_data.source_mode_required.v1
S04. trade_data.fee_slippage_execution_cost_required.v1
S05. trade_candidate.snapshot_required_before_scoring.v1
S06. trade_candidate.decision_timestamp_required.v1
S07. trade_candidate.market_risk_execution_context_required.v1
S08. feature_schema.decision_time_only.v1
S09. feature_schema.feature_timestamp_cutoff_required.v1
S10. feature_schema.post_trade_fields_forbidden_in_input.v1
S11. outcome_schema.post_trade_fields_separated.v1
S12. label_schema.no_pnl_only_label.v1
S13. label_schema.good_loss_bad_win_required.v1
S14. label_schema.multi_dimensional_trade_quality.v1
S15. label_schema.label_reason_codes_required.v1
S16. training_example.sft_schema_required.v1
S17. training_example.input_target_separation.v1
S18. preference_pair.not_based_on_pnl_only.v1
S19. eval_case.time_strategy_regime_split_required.v1
S20. eval_case.no_training_overlap_required.v1
```

### C. 交易 gating/scoring 采集池

```text
01. llm_role_boundary.scorer_not_executor.v1
02. llm_role_boundary.no_direct_order_execution.v1
03. llm_role_boundary.cannot_override_hard_risk_gate.v1
04. training_data.trade_sample_schema_required.v1
05. training_data.strategy_version_required.v1
06. training_data.decision_timestamp_required.v1
07. training_data.feature_timestamp_cutoff_required.v1
08. labeling.no_future_information.v1
09. labeling.no_pnl_only_labeling.v1
10. labeling.good_loss_bad_win_distinction.v1
11. labeling.ambiguous_trade_needs_human_review.v1
12. data_quality.backtest_paper_live_separation.v1
13. data_quality.execution_cost_required.v1
14. data_quality.missing_core_fields_block_training.v1
15. scoring_rubric.setup_quality.v1
16. scoring_rubric.risk_reward_quality.v1
17. scoring_rubric.market_regime_fit.v1
18. scoring_rubric.rule_compliance.v1
19. scoring_rubric.uncertainty_penalty.v1
20. scoring_rubric.reason_code_required.v1
21. gating.low_confidence_cannot_allow.v1
22. gating.false_allow_more_dangerous_than_false_block.v1
23. rag.retrieval_required_before_trade_scoring.v1
24. rag.approved_machine_gate_allow_only_default_guidance.v1
25. rag.no_source_or_conflict_blocks_default_guidance.v1
26. rag.no_hit_requires_neutral_or_review.v1
27. mcp.read_only_knowledge_access.v1
28. mcp.server_side_permission_enforcement_required.v1
29. deployment.shadow_mode_before_live.v1
30. deployment.llm_timeout_or_mcp_failure_fallback_required.v1
31. versioning.model_prompt_rag_strategy_snapshot_required.v1
32. audit.every_gate_decision_requires_trace.v1
33. eval.time_split_walk_forward_required.v1
34. eval.score_calibration_required_before_gating.v1
35. llm_judge.position_and_format_bias_check_required.v1
36. governance.dataset_card_and_model_card_required.v1
```

### D. 业务闭环治理采集池

```text
B01. business_objective.llm_trader_acceptance_criteria_required.v1
B02. business_objective.success_metric_not_only_pnl.v1
B03. task_taxonomy.pre_trade_post_trade_task_separation.v1
B04. task_taxonomy.each_task_requires_schema_and_eval.v1
B05. label_factory.label_guideline_required.v1
B06. label_factory.gold_set_required.v1
B07. label_factory.label_conflict_resolution_required.v1
B08. data_asset.eval_pool_must_not_train.v1
B09. data_asset.gold_set_immutable_required.v1
B10. method_selection.rag_first_baseline_required.v1
B11. method_selection.no_finetune_before_eval_baseline.v1
B12. capability_boundary.llm_not_primary_price_predictor.v1
B13. capability_boundary.numeric_model_vs_llm_role_split.v1
B14. research_feedback.llm_suggestion_is_hypothesis_only.v1
B15. research_feedback.no_auto_strategy_parameter_update.v1
B16. runtime.llm_gate_is_suggestion_not_final_authority.v1
B17. runtime.final_gate_deterministic_engine_required.v1
B18. calibration.llm_score_not_probability.v1
B19. calibration.threshold_requires_shadow_data.v1
B20. risk_ledger.false_allow_cost_record_required.v1
B21. lineage.model_prompt_rag_data_strategy_bound_together.v1
B22. redteam.hard_gate_override_attempt_test.v1
B23. approval.hard_gate_enable_requires_approval.v1
B24. readiness.offline_eval_pass_not_equal_live_ready.v1
B25. feedback.model_output_cannot_label_itself.v1
```

## 上下游边界

```text
上游：Phase 35 外部项目 AI 主动检索协议、Phase 34 知识卡 Schema v1.1、现有知识树。
下游：Phase 36 采集矩阵、候选知识包、formal reviewed 知识、MCP/SearchLab/KnowledgeTree 验证。
```

## 跨分支知识边界

AI Engineering 不能变成所有交易知识的垃圾桶。它只沉淀 AI/LLM/RAG/MCP/训练数据 schema/评估/部署/治理知识。

交易专业规则本体必须进入 Trading Engineering 对应分支：

```text
K 线结构、指标、入场、止损、止盈 -> KB_02_KLINE_STRATEGY
市场微观结构、盘口、流动性、订单流 -> KB_03_MARKET_MICROSTRUCTURE
回测偏差、过拟合、成本模型、指标解释 -> KB_04_BACKTEST
回放、模拟盘、fill model、滑点延迟 -> KB_05_REPLAY_SIMULATION
实盘订单、执行适配器、仓位同步、kill switch -> KB_06_LIVE_EXECUTION
交易复盘、坏例 taxonomy、R/R 分解 -> KB_07_TRADE_ANALYSIS
```

AI Engineering 可以引用这些交易知识，但不能重写它们的规则本体。允许进入 AI Engineering 的是：

```text
如何检索这些交易知识
如何把这些交易知识放进 retrieved_knowledge
如何在 TradeCandidate / LabelingRecord / EvalCase 中引用它们
如何用它们做训练数据 gate、eval gate、runtime gate
如何记录 knowledge_refs、reason_codes、audit_trace
```

审计规则：

```text
如果某个 AI Engineering 知识点开始讲“某种 K 线形态应该如何交易”，必须拆分。
交易规则本体回到 Trading Engineering。
AI Engineering 只保留“LLM 如何引用、审计、训练、评估或治理该规则”的部分。
```

外接项目负责提供：

```text
项目事实
策略版本
交易样本
训练目标
真实运行模式
私有配置和代码路径
```

CEK-TA 负责提供：

```text
通用训练工程知识
交易数据到训练数据的转换 schema
交易 LLM 任务分类和训练方法选择
交易 scoring/gating 安全边界
业务验收、标签工厂、数据资产治理、反馈治理
RAG/MCP 调用协议
知识治理和审计流程
可复用的 schema、rubric、gate 和 eval 方法
```

## 不进入本框架的内容

```text
不沉淀外接项目私有策略参数。
不沉淀单个交易账户事实。
不沉淀交易所密钥、订单 API 权限或实盘配置。
不把某个策略的盈利样本泛化为通用训练规则。
不把 post-trade outcome、PnL、MFE、MAE 混入决策时输入。
不把 LLM 建议直接变成策略参数更新。
不把 live result 或模型输出自动变成训练标签。
不把未经来源审计的训练经验标成 approved。
```

## 交易数据到训练数据转换链路

```text
Raw Trade Record
  -> Trade Candidate Snapshot
  -> Decision-Time Features
  -> Outcome / Post-Trade Record
  -> Labeling Record
  -> SFT Example
  -> Preference Pair
  -> Eval Case
```

关键边界：

```text
1. Raw Trade Record 可以包含完整事后结果，但不能直接作为模型输入。
2. Trade Candidate Snapshot 只能包含 decision_timestamp 当时可见的信息。
3. 每个 Decision-Time Feature 必须有 feature_timestamp 和 available_at_decision。
4. Outcome / Post-Trade Record 只能用于 label、eval、复盘和审计。
5. Labeling Record 必须区分 outcome label 和 process quality label。
6. SFT Example 必须分离 input 与 target_output。
7. Preference Pair 必须基于同一 prompt，不能只按 PnL 选 chosen/rejected。
8. Eval Case 必须与训练集隔离，并声明 time/strategy/regime split。
```

## 合格 LLM 交易质量审计助手业务闭环

完整业务闭环必须覆盖：

```text
业务目标定义
  -> 交易任务分类
  -> 数据资产治理
  -> 标签工厂
  -> 训练方法选择
  -> 离线评估
  -> 模拟盘 shadow
  -> 实盘辅助
  -> 事故复盘
  -> 知识/数据/模型回灌
```

硬边界：

```text
1. LLM 交易质量审计助手的 KPI 不是声称赚钱，而是在确定性风控约束下减少坏交易放行、提高风险识别和提升复盘一致性。
2. Pre-trade gating、post-trade review、incident explanation 和 research suggestion 是不同任务，必须有各自 schema 和 eval。
3. Gold set 必须由人工或强规则高质量审核，不能被训练集污染。
4. LLM suggestion 只能是 research hypothesis，不能自动改策略或参数。
5. LLM gate 是建议，不是最终裁决；最终裁决必须由 deterministic final gate 完成。
6. LLM score 不是胜率概率，阈值必须基于 shadow 数据和分策略/分 regime 校准。
7. 模型输出不能给自己贴标签；live feedback 必须经过治理和审核。
```
