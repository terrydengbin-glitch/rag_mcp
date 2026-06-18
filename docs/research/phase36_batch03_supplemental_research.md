# Phase 36 第三批 needs_more_evidence 补证采集记录

## 任务信息

```text
Phase: Phase 36 AI Engineering gating/scoring 知识扩充
任务 ID: CEK-TA-213
下游任务: CEK-TA-214
创建日期: 2026-06-09
状态: done
```

## 目标

为第三批审计中 5 条 `needs_more_evidence` 候选补充直接来源、重写 statement，并导出二次审计包。

本任务只处理候选补证，不把候选转成正式知识，不设置 `reviewed`，不设置 `approved`，也不允许进入默认指导。

## 补证对象

| candidate_id | normalized_claim | 补证重点 |
| --- | --- | --- |
| `cand_20260609_ai_engineering_eval_ablation_required_for_rag_prompt_model_components_v1_001` | `eval.ablation_required_for_rag_prompt_model_components.v1` | 检查 rewritten statement 是否从泛化评估改为组件级 ablation，source_refs 是否能直接支撑 RAG/prompt/model/tool 组件消融。 |
| `cand_20260609_ai_engineering_eval_blocked_trade_cannot_be_labeled_as_loss_v1_001` | `eval.blocked_trade_cannot_be_labeled_as_loss.v1` | 检查 blocked trade 不能直接标 loss 的 label action 是否有 counterfactual/logged feedback 来源支撑，并是否与父规则 counterfactual_outcome_missing 区分。 |
| `cand_20260609_ai_engineering_eval_deterministic_baseline_required_before_llm_gate_v1_001` | `eval.deterministic_baseline_required_before_llm_gate.v1` | 检查 statement 是否明确 deterministic/current baseline before LLM gate，且不把 Trading Engineering 的交易规则本体写入 AI Engineering。 |
| `cand_20260609_ai_engineering_eval_score_calibration_required_before_gating_v1_001` | `eval.score_calibration_required_before_gating.v1` | 检查是否补足 calibration 直接来源，并是否与 calibration.llm_score_not_probability、calibration.threshold_requires_shadow_data 正确区分或互链。 |
| `cand_20260609_ai_engineering_eval_time_split_walk_forward_required_v1_001` | `eval.time_split_walk_forward_required.v1` | 检查是否从泛化评估改为 time-aware / walk-forward split，source_refs 是否包含 TimeSeriesSplit 或金融 purged/embargoed CV 直接来源。 |

## 联网来源与用途

### eval.ablation_required_for_rag_prompt_model_components.v1

补证后 statement：RAG、prompt、model、reranker、tool 或 MCP 组件变更在进入 gate/scoring promotion 前，必须在同一隔离 eval set 上执行组件级 ablation，对比 baseline、component-disabled、component-enabled 和 combined 配置差异。

| source_id | 来源 | 用途 |
| --- | --- | --- |
| `src_openai_model_optimization_baseline` | [Model optimization | OpenAI API](https://platform.openai.com/docs/guides/model-optimization) | OpenAI model optimization 文档支持先写 evals 建立 baseline，再围绕 prompt、fine-tuning 和模型输出质量进行迭代。 |
| `src_openai_evals_api_runs` | [Evals | OpenAI API Reference](https://platform.openai.com/docs/api-reference/evals/createRun?api-mode=chat) | OpenAI Evals API 支持创建评估结构并在不同模型和参数上运行，可支撑同一 eval set 下的配置对比。 |
| `src_pmlr_ablator_ablation_experiments` | [ABLATOR: Robust Horizontal-Scaling of Machine Learning Ablation Experiments](https://proceedings.mlr.press/v224/fostiropoulos23a.html) | PMLR ABLATOR 论文直接说明 ablation experiments 用于理解方法、组件和训练设置的有效性。 |
| `src_coling_2025_rag_best_practices_ablation` | [Enhancing Retrieval-Augmented Generation: A Study of Best Practices](https://aclanthology.org/2025.coling-main.449.pdf) | 该 RAG 最佳实践研究使用 ablation studies 分析 RAG 组件和配置对效果的影响，可作为 RAG 组件级消融的直接来源。 |

建议字段：

```text
ablation_run_id
baseline_config_id
component_name
component_version
component_disabled
eval_dataset_id
eval_dataset_hash
metric_set_id
failure_case_ids
delta_vs_baseline
decision
reviewer
```

### eval.blocked_trade_cannot_be_labeled_as_loss.v1

补证后 statement：被 gate 阻断或过滤的交易没有 observed execution outcome，不能仅因为被阻断就标记为 loss；除非有 approved off-policy、simulation 或 human review evidence，否则应标记为 counterfactual_missing、blocked_no_outcome 或 needs_human_review。

| source_id | 来源 | 用途 |
| --- | --- | --- |
| `src_pmlr_counterfactual_risk_minimization` | [Counterfactual Risk Minimization: Learning from Logged Bandit Feedback](https://proceedings.mlr.press/v37/swaminathan15.html) | CRM 文献说明 logged bandit feedback 只包含历史策略选择动作的反馈，学习或评估新策略需要反事实处理。 |
| `src_arxiv_off_policy_logged_bandit_surrogate` | [Off-Policy Evaluation and Learning from Logged Bandit Feedback: Error Reduction via Surrogate Policy](https://arxiv.org/abs/1808.00232) | 该论文讨论从 logged bandit feedback 做 off-policy evaluation 和 learning，支持历史日志反馈不完整时不能直接当普通监督标签。 |
| `src_arxiv_effective_eval_multiple_loggers` | [Effective Evaluation using Logged Bandit Feedback from Multiple Loggers](https://arxiv.org/abs/1703.06180) | 该文说明可用不同 logging policies 的日志进行 counterfactual estimators 评估，支持记录 logging policy 与反馈可观测性。 |

建议字段：

```text
trade_candidate_id
gate_decision
executed_flag
observed_outcome_available
counterfactual_outcome_status
label_value
label_reason_code
ope_method_id
simulation_ref
reviewer
```

### eval.deterministic_baseline_required_before_llm_gate.v1

补证后 statement：LLM gate/scoring 在进入 promotion、shadow 或 hard gate 讨论前，必须先与 deterministic baseline、规则 baseline 或当前生产 gate baseline 在同一隔离 eval set 上比较；没有 baseline comparison 不得声称 LLM 带来增益。

| source_id | 来源 | 用途 |
| --- | --- | --- |
| `src_openai_model_optimization_baseline` | [Model optimization | OpenAI API](https://platform.openai.com/docs/guides/model-optimization) | OpenAI model optimization 明确支持先写 evals 建立 performance/accuracy baseline，再进行 prompt、fine-tuning 或模型优化。 |
| `src_openai_evals_api_runs` | [Evals | OpenAI API Reference](https://platform.openai.com/docs/api-reference/evals/createRun?api-mode=chat) | OpenAI Evals API 支持在不同模型和参数上运行评估，可支撑同一 eval set 下的 baseline 对比。 |
| `src_rules_ml_baseline` | [Rules of Machine Learning](https://martin.zinkevich.org/rules_of_ml/rules_of_ml.pdf) | Rules of ML 支持从简单、可解释、可监控的 baseline 开始，并围绕生产目标持续比较和迭代。 |

建议字段：

```text
baseline_config_id
baseline_type
llm_gate_config_id
eval_dataset_id
metric_set_id
baseline_score
llm_score
delta
failure_case_ids
decision
reviewer
```

### eval.score_calibration_required_before_gating.v1

补证后 statement：LLM raw score、rubric score、verbal confidence 或 logprob-derived score 在用于 gating 前，必须在独立 holdout 或 shadow 数据上完成校准或验证，并记录 reliability、subgroup 和样本量；未校准前不得 hard allow。

| source_id | 来源 | 用途 |
| --- | --- | --- |
| `src_sklearn_probability_calibration` | [Probability calibration | scikit-learn](https://scikit-learn.org/stable/modules/calibration.html) | scikit-learn 概率校准文档支持 reliability diagrams、proper scoring rules 和校准/区分能力拆分分析。 |
| `src_sklearn_calibration_curve` | [calibration_curve | scikit-learn](https://scikit-learn.org/1.5/modules/generated/sklearn.calibration.calibration_curve.html) | calibration_curve 文档支持计算 true/predicted probabilities，并说明 calibration curves 也称 reliability diagrams。 |
| `src_acl_2024_llm_confidence_calibration_survey` | [A Survey of Confidence Estimation and Calibration in Large Language Models](https://aclanthology.org/2024.naacl-long.366/) | NAACL 2024 survey 系统总结 LLM confidence estimation 和 calibration 的挑战与技术进展，支持 LLM 分数和置信度不得未经校准进入高影响门禁。 |

建议字段：

```text
raw_score_type
calibration_dataset_id
calibration_method
calibrated_score
ece
brier_score
reliability_bucket
subgroup_key
sample_count
calibration_report_id
```

### eval.time_split_walk_forward_required.v1

补证后 statement：涉及 chronological market data 的交易 LLM gate/scoring 评估必须使用 time-aware split，例如 walk-forward、rolling window、expanding window 或明确 train-before-test cutoff；除非有 leakage analysis 批准，否则不得使用随机切分作为最终评估。

| source_id | 来源 | 用途 |
| --- | --- | --- |
| `src_sklearn_time_series_split` | [TimeSeriesSplit | scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html) | TimeSeriesSplit 文档直接说明时间序列交叉验证应保证 train/test 时间顺序，其他 CV 方法不适合时间排序数据。 |
| `src_sklearn_cross_validation_time_series` | [Cross-validation: evaluating estimator performance | scikit-learn](https://scikit-learn.org/stable/modules/cross_validation.html) | scikit-learn cross-validation 文档支持按任务选择合适 split 方法，并为时间序列切分提供上下文。 |
| `src_lopez_de_prado_afml_purged_kfold` | [Advances in Financial Machine Learning](https://philpapers.org/rec/LPEAIF) | 该书包含金融机器学习交叉验证章节，讨论为什么普通 K-Fold 在金融场景失败，并提出 Purged K-Fold 与 Embargo 思路。 |
| `src_pmc_financial_time_series_purged_kfold` | [A Bayesian-based classification framework for financial time series trend prediction](https://pmc.ncbi.nlm.nih.gov/articles/PMC9521884/) | 该金融时间序列研究讨论 serial correlation 与 purging/embargoing cross-validation，可作为金融时序评估补充来源。 |

建议字段：

```text
split_method
train_start
train_end
validation_start
validation_end
test_start
test_end
gap_or_embargo
walk_forward_window_id
rolling_or_expanding
time_leakage_check_id
```

## 边界

```text
1. candidate 不是 formal knowledge。
2. accepted_for_draft 不是 approved。
3. 二次审计前不得进入 reviewed/approved/default guidance。
4. AI Engineering 只沉淀评估、数据、训练、RAG/MCP、部署和治理规则。
5. K 线、策略、回测、实盘执行、交易风控、订单和仓位规则本体必须路由到 Trading Engineering。
```
