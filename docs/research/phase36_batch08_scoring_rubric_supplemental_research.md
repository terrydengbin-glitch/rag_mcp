# Phase 36 第八批 scoring_rubric 候选补证采集记录

## 目标

处理第八批审计中 5 条 `scoring_rubric.*` needs_more_evidence 候选。审计指出的问题是：原 statement 只支持通用 `reason_code_required`，但 normalized_claim 指向具体 rubric 维度。

本次补证只修正候选和导出二审包，不直接转 reviewed，不设置 approved。

## 补证来源

- scikit-learn TimeSeriesSplit：https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html
- scikit-learn GroupKFold：https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html
- scikit-learn threshold tuning：https://scikit-learn.org/stable/modules/classification_threshold.html
- scikit-learn cost-sensitive threshold：https://scikit-learn.org/stable/auto_examples/model_selection/plot_cost_sensitive_learning.html
- scikit-learn probability calibration：https://scikit-learn.org/stable/modules/calibration.html
- FINRA 15-09：https://www.finra.org/rules-guidance/notices/15-09
- NIST AI RMF Core：https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- CEK-TA 内部契约：`docs/contracts/ai_engineering_scoring_rubric_dimension_contract.md`

## 候选处理结果

### cand_20260609_ai_engineering_scoring_rubric_market_regime_fit_v1_001

- 状态：`needs_more_evidence`
- statement：Scoring rubric 只能在存在 owner-defined `market_regime_ref`、`regime_label_source`、证据引用和 reason_codes 时记录 `market_regime_fit`；缺少或冲突的 market regime 上下文必须降级为 `needs_review`，不得由 LLM 自行发明可交易 regime。
- source_refs：6
- 二审包：`docs/audit/phase36_batch08_scoring_rubric_supplemental_audit_package_20260609.json`

### cand_20260609_ai_engineering_scoring_rubric_risk_reward_quality_v1_001

- 状态：`needs_more_evidence`
- statement：`risk_reward_quality` 只能作为结构化 rubric 维度使用，必须引用 `risk_context_ref`、`reward_context_ref` 或 `cost_matrix_ref`、证据和 owner review；AI Engineering 不得计算或暗示策略收益、仓位影响或机会成本。
- source_refs：7
- 二审包：`docs/audit/phase36_batch08_scoring_rubric_supplemental_audit_package_20260609.json`

### cand_20260609_ai_engineering_scoring_rubric_rule_compliance_v1_001

- 状态：`needs_more_evidence`
- statement：`rule_compliance` 只能针对显式 `rule_refs` 或 `policy_refs` 记录 pass/fail/unknown、证据引用和 owner review；LLM 不得发明交易规则，也不得把无 rule_ref 的解释当成合规结论。
- source_refs：6
- 二审包：`docs/audit/phase36_batch08_scoring_rubric_supplemental_audit_package_20260609.json`

### cand_20260609_ai_engineering_scoring_rubric_setup_quality_v1_001

- 状态：`needs_more_evidence`
- statement：`setup_quality` 只能记录为 owner-defined review dimension 或 reason-code category，必须引用 `setup_quality_ref` 与 `strategy_version_ref`；AI Engineering 不得定义交易 setup、K 线结构、入场条件或策略有效性。
- source_refs：6
- 二审包：`docs/audit/phase36_batch08_scoring_rubric_supplemental_audit_package_20260609.json`

### cand_20260609_ai_engineering_scoring_rubric_uncertainty_penalty_v1_001

- 状态：`needs_more_evidence`
- statement：Scoring rubric 必须在未校准、低置信、来源冲突或证据不足时施加 `uncertainty_penalty` 或降级；未引用 `calibration_report_id`、`confidence_status` 和 `uncertainty_reason_code` 的高分不得用于 hard allow。
- source_refs：6
- 二审包：`docs/audit/phase36_batch08_scoring_rubric_supplemental_audit_package_20260609.json`
