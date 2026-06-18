# Phase 36 AI Engineering ResearchIngestionTask 队列

本队列用于驱动后续联网采集、来源评分、冲突检测、候选知识包生成和候选审核。优先顺序为 P0-Core -> P0-Extended -> P1。

## 执行规则

```text
1. 每批最多采集 8-12 条 P0-Core，避免一次性生成无法审计的大包。
2. 每条任务必须保留 source_url、source_type、source_quality、claim、boundary、conflict_notes。
3. 采集产物进入 codex-expert-kit/rag/candidates/，不得直接进入 formal knowledge。
4. 采集前先检查是否应路由到 Trading Engineering，避免 AI Engineering 污染。
5. 采集后必须导出 AI/人工审计包，再按 Phase 32 候选到 reviewed 工作流沉淀。
```

## P0-Core

| Task ID | knowledge_id | canonical_node_id | 查询方向 | DoD |
| --- | --- | --- | --- | --- |
| RIT-P36-A-T01 | `training_objective.task_definition_required.v1` | `kt.llm_training.model_training_engineering` | training objective task definition required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-A-T02 | `training_objective.rag_vs_finetune_boundary_required.v1` | `kt.llm_training.model_training_engineering` | training objective rag vs finetune boundary required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-A-T03 | `dataset.schema_required.v1` | `kt.llm_training.model_training_engineering` | dataset schema required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-A-T04 | `dataset.source_lineage_required.v1` | `kt.llm_training.model_training_engineering` | dataset source lineage required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-A-T05 | `dataset.version_and_hash_required.v1` | `kt.llm_training.model_training_engineering` | dataset version and hash required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-A-T06 | `dataset.train_validation_test_split_required.v1` | `kt.llm_training.model_training_engineering` | dataset train validation test split required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-A-T08 | `dataset.dataset_card_required.v1` | `kt.llm_training.model_training_engineering` | dataset dataset card required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-A-T09 | `leakage.train_test_contamination_block.v1` | `kt.llm_training.model_training_engineering` | leakage train test contamination block v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-A-T10 | `leakage.label_in_input_forbidden.v1` | `kt.llm_training.model_training_engineering` | leakage label in input forbidden v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-A-T16 | `eval.holdout_test_set_required.v1` | `kt.llm_training.model_training_engineering` | eval holdout test set required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-A-T17 | `eval.production_like_eval_required.v1` | `kt.llm_training.model_training_engineering` | eval production like eval required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-A-T18 | `training_run.config_and_hyperparameter_snapshot_required.v1` | `kt.llm_training.model_training_engineering` | training run config and hyperparameter snapshot required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-A-T19 | `serving_consistency.train_like_serve_required.v1` | `kt.llm_training.model_training_engineering` | serving consistency train like serve required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-A-T20 | `safety.no_tool_permission_escalation.v1` | `kt.llm_training.model_training_engineering` | safety no tool permission escalation v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S05 | `trade_candidate.snapshot_required_before_scoring.v1` | `kt.llm_training.training_dataset_schema_engineering` | trade candidate snapshot required before scoring v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S06 | `trade_candidate.decision_timestamp_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | trade candidate decision timestamp required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S08 | `feature_schema.decision_time_only.v1` | `kt.llm_training.training_dataset_schema_engineering` | feature schema decision time only v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S09 | `feature_schema.feature_timestamp_cutoff_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | feature schema feature timestamp cutoff required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S10 | `feature_schema.post_trade_fields_forbidden_in_input.v1` | `kt.llm_training.training_dataset_schema_engineering` | feature schema post trade fields forbidden in input v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S11 | `outcome_schema.post_trade_fields_separated.v1` | `kt.llm_training.training_dataset_schema_engineering` | outcome schema post trade fields separated v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S12 | `label_schema.no_pnl_only_label.v1` | `kt.llm_training.training_dataset_schema_engineering` | label schema no pnl only label v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S20 | `eval_case.no_training_overlap_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | eval case no training overlap required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-01 | `llm_role_boundary.scorer_not_executor.v1` | `kt.llm_training.trading_scoring_gating_training` | llm role boundary scorer not executor v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-02 | `llm_role_boundary.no_direct_order_execution.v1` | `kt.llm_training.trading_scoring_gating_training` | llm role boundary no direct order execution v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-03 | `llm_role_boundary.cannot_override_hard_risk_gate.v1` | `kt.llm_training.trading_scoring_gating_training` | llm role boundary cannot override hard risk gate v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-08 | `labeling.no_future_information.v1` | `kt.llm_training.trading_scoring_gating_training` | labeling no future information v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-12 | `data_quality.backtest_paper_live_separation.v1` | `kt.llm_training.trading_scoring_gating_training` | data quality backtest paper live separation v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-13 | `data_quality.execution_cost_required.v1` | `kt.llm_training.trading_scoring_gating_training` | data quality execution cost required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-14 | `data_quality.missing_core_fields_block_training.v1` | `kt.llm_training.trading_scoring_gating_training` | data quality missing core fields block training v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-23 | `rag.retrieval_required_before_trade_scoring.v1` | `kt.rag_engineering` | rag retrieval required before trade scoring v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-24 | `rag.approved_machine_gate_allow_only_default_guidance.v1` | `kt.rag_engineering` | rag approved machine gate allow only default guidance v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-25 | `rag.no_source_or_conflict_blocks_default_guidance.v1` | `kt.rag_engineering` | rag no source or conflict blocks default guidance v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-26 | `rag.no_hit_requires_neutral_or_review.v1` | `kt.rag_engineering` | rag no hit requires neutral or review v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-27 | `mcp.read_only_knowledge_access.v1` | `kt.mcp` | mcp read only knowledge access v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-28 | `mcp.server_side_permission_enforcement_required.v1` | `kt.mcp` | mcp server side permission enforcement required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-29 | `deployment.shadow_mode_before_live.v1` | `kt.llmops_deployment` | deployment shadow mode before live v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-30 | `deployment.llm_timeout_or_mcp_failure_fallback_required.v1` | `kt.llmops_deployment` | deployment llm timeout or mcp failure fallback required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-31 | `versioning.model_prompt_rag_strategy_snapshot_required.v1` | `kt.llmops_deployment.artifact_lineage` | versioning model prompt rag strategy snapshot required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-32 | `audit.every_gate_decision_requires_trace.v1` | `kt.ai_governance_audit` | audit every gate decision requires trace v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-33 | `eval.time_split_walk_forward_required.v1` | `kt.llm_training.model_training_engineering` | eval time split walk forward required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-34 | `eval.score_calibration_required_before_gating.v1` | `kt.llm_training.model_training_engineering` | eval score calibration required before gating v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-36 | `governance.dataset_card_and_model_card_required.v1` | `kt.ai_governance_audit` | governance dataset card and model card required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B02 | `business_objective.success_metric_not_only_pnl.v1` | `kt.ai_business_objective` | business objective success metric not only pnl v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B08 | `data_asset.eval_pool_must_not_train.v1` | `kt.ai_data_asset_management` | data asset eval pool must not train v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B09 | `data_asset.gold_set_immutable_required.v1` | `kt.ai_data_asset_management` | data asset gold set immutable required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B10 | `method_selection.rag_first_baseline_required.v1` | `kt.llm_training.training_method_selection` | method selection rag first baseline required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B11 | `method_selection.no_finetune_before_eval_baseline.v1` | `kt.llm_training.training_method_selection` | method selection no finetune before eval baseline v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B16 | `runtime.llm_gate_is_suggestion_not_final_authority.v1` | `kt.trading_ai_safety` | runtime llm gate is suggestion not final authority v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B17 | `runtime.final_gate_deterministic_engine_required.v1` | `kt.trading_ai_safety` | runtime final gate deterministic engine required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B25 | `feedback.model_output_cannot_label_itself.v1` | `kt.ai_feedback_governance` | feedback model output cannot label itself v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-N-01 | `eval.counterfactual_outcome_missing_for_blocked_trades.v1` | `kt.llm_training.model_training_engineering` | eval counterfactual outcome missing for blocked trades v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-N-02 | `eval.off_policy_evaluation_required_for_gate_policy.v1` | `kt.llm_training.model_training_engineering` | eval off policy evaluation required for gate policy v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-N-03 | `eval.blocked_trade_cannot_be_labeled_as_loss.v1` | `kt.llm_training.model_training_engineering` | eval blocked trade cannot be labeled as loss v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-N-04 | `security.rag_context_is_untrusted_input.v1` | `kt.ai_security_privacy_compliance` | security rag context is untrusted input v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-N-05 | `security.prompt_injection_test_required_for_trade_context.v1` | `kt.ai_security_privacy_compliance` | security prompt injection test required for trade context v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-N-06 | `data_privacy.no_secret_or_account_identifier_in_training.v1` | `kt.ai_security_privacy_compliance` | data privacy no secret or account identifier in training v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-N-07 | `data_license.market_data_license_check_required.v1` | `kt.ai_security_privacy_compliance` | data license market data license check required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-N-08 | `eval.deterministic_baseline_required_before_llm_gate.v1` | `kt.llm_training.model_training_engineering` | eval deterministic baseline required before llm gate v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-N-09 | `eval.ablation_required_for_rag_prompt_model_components.v1` | `kt.llm_training.model_training_engineering` | eval ablation required for rag prompt model components v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-N-10 | `label_factory.inter_annotator_agreement_required.v1` | `kt.ai_label_factory` | label factory inter annotator agreement required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-N-11 | `feature_store.feature_schema_registry_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | feature store feature schema registry required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-N-12 | `serving_consistency.training_serving_parity_test_required.v1` | `kt.llm_training.model_training_engineering` | serving consistency training serving parity test required v1 | 2+ sources; boundary; conflict audit; candidate json |

## P0-Extended

| Task ID | knowledge_id | canonical_node_id | 查询方向 | DoD |
| --- | --- | --- | --- | --- |
| RIT-P36-A-T07 | `dataset.deduplication_required.v1` | `kt.llm_training.model_training_engineering` | dataset deduplication required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-A-T11 | `sft.when_to_use_and_not_use.v1` | `kt.llm_training.model_training_engineering` | sft when to use and not use v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-A-T12 | `sft.output_schema_consistency_required.v1` | `kt.llm_training.model_training_engineering` | sft output schema consistency required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-A-T13 | `preference_training.preference_pair_schema_required.v1` | `kt.llm_training.model_training_engineering` | preference training preference pair schema required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-A-T14 | `preference_training.chosen_rejected_reason_required.v1` | `kt.llm_training.model_training_engineering` | preference training chosen rejected reason required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-A-T15 | `dpo.preference_data_quality_required.v1` | `kt.llm_training.model_training_engineering` | dpo preference data quality required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S01 | `trade_data.raw_trade_record_required_fields.v1` | `kt.llm_training.training_dataset_schema_engineering` | trade data raw trade record required fields v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S02 | `trade_data.strategy_id_and_version_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | trade data strategy id and version required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S03 | `trade_data.source_mode_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | trade data source mode required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S04 | `trade_data.fee_slippage_execution_cost_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | trade data fee slippage execution cost required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S07 | `trade_candidate.market_risk_execution_context_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | trade candidate market risk execution context required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S13 | `label_schema.good_loss_bad_win_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | label schema good loss bad win required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S14 | `label_schema.multi_dimensional_trade_quality.v1` | `kt.llm_training.training_dataset_schema_engineering` | label schema multi dimensional trade quality v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S15 | `label_schema.label_reason_codes_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | label schema label reason codes required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S16 | `training_example.sft_schema_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | training example sft schema required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S17 | `training_example.input_target_separation.v1` | `kt.llm_training.training_dataset_schema_engineering` | training example input target separation v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S18 | `preference_pair.not_based_on_pnl_only.v1` | `kt.llm_training.training_dataset_schema_engineering` | preference pair not based on pnl only v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-B-S19 | `eval_case.time_strategy_regime_split_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | eval case time strategy regime split required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-04 | `training_data.trade_sample_schema_required.v1` | `kt.llm_training.trading_scoring_gating_training` | training data trade sample schema required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-05 | `training_data.strategy_version_required.v1` | `kt.llm_training.trading_scoring_gating_training` | training data strategy version required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-06 | `training_data.decision_timestamp_required.v1` | `kt.llm_training.trading_scoring_gating_training` | training data decision timestamp required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-07 | `training_data.feature_timestamp_cutoff_required.v1` | `kt.llm_training.trading_scoring_gating_training` | training data feature timestamp cutoff required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-09 | `labeling.no_pnl_only_labeling.v1` | `kt.llm_training.trading_scoring_gating_training` | labeling no pnl only labeling v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-10 | `labeling.good_loss_bad_win_distinction.v1` | `kt.llm_training.trading_scoring_gating_training` | labeling good loss bad win distinction v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-11 | `labeling.ambiguous_trade_needs_human_review.v1` | `kt.llm_training.trading_scoring_gating_training` | labeling ambiguous trade needs human review v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-20 | `scoring_rubric.reason_code_required.v1` | `kt.llm_training.trading_scoring_gating_training` | scoring rubric reason code required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-21 | `gating.low_confidence_cannot_allow.v1` | `kt.llm_training.trading_scoring_gating_training` | gating low confidence cannot allow v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-C-22 | `gating.false_allow_more_dangerous_than_false_block.v1` | `kt.llm_training.trading_scoring_gating_training` | gating false allow more dangerous than false block v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B01 | `business_objective.llm_trader_acceptance_criteria_required.v1` | `kt.ai_business_objective` | business objective llm trader acceptance criteria required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B03 | `task_taxonomy.pre_trade_post_trade_task_separation.v1` | `kt.llm_training.trading_llm_task_taxonomy` | task taxonomy pre trade post trade task separation v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B04 | `task_taxonomy.each_task_requires_schema_and_eval.v1` | `kt.llm_training.trading_llm_task_taxonomy` | task taxonomy each task requires schema and eval v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B05 | `label_factory.label_guideline_required.v1` | `kt.ai_label_factory` | label factory label guideline required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B06 | `label_factory.gold_set_required.v1` | `kt.ai_label_factory` | label factory gold set required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B07 | `label_factory.label_conflict_resolution_required.v1` | `kt.ai_label_factory` | label factory label conflict resolution required v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B12 | `capability_boundary.llm_not_primary_price_predictor.v1` | `kt.llm_training.trading_llm_task_taxonomy` | capability boundary llm not primary price predictor v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B13 | `capability_boundary.numeric_model_vs_llm_role_split.v1` | `kt.llm_training.trading_llm_task_taxonomy` | capability boundary numeric model vs llm role split v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B18 | `calibration.llm_score_not_probability.v1` | `kt.llm_training.trading_scoring_gating_training` | calibration llm score not probability v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B19 | `calibration.threshold_requires_shadow_data.v1` | `kt.llm_training.trading_scoring_gating_training` | calibration threshold requires shadow data v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B21 | `lineage.model_prompt_rag_data_strategy_bound_together.v1` | `kt.llmops_deployment.artifact_lineage` | lineage model prompt rag data strategy bound together v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B22 | `redteam.hard_gate_override_attempt_test.v1` | `kt.trading_ai_safety` | redteam hard gate override attempt test v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B23 | `approval.hard_gate_enable_requires_approval.v1` | `kt.ai_governance_audit` | approval hard gate enable requires approval v1 | 2+ sources; boundary; conflict audit; candidate json |
| RIT-P36-D-B24 | `readiness.offline_eval_pass_not_equal_live_ready.v1` | `kt.llmops_deployment` | readiness offline eval pass not equal live ready v1 | 2+ sources; boundary; conflict audit; candidate json |

## P1

| Task ID | knowledge_id | canonical_node_id | 查询方向 | DoD |
| --- | --- | --- | --- | --- |
| RIT-P36-C-15 | `scoring_rubric.setup_quality.v1` | `kt.llm_training.trading_scoring_gating_training` | scoring rubric setup quality v1 | 2+ sources; boundary; candidate notes |
| RIT-P36-C-16 | `scoring_rubric.risk_reward_quality.v1` | `kt.llm_training.trading_scoring_gating_training` | scoring rubric risk reward quality v1 | 2+ sources; boundary; candidate notes |
| RIT-P36-C-17 | `scoring_rubric.market_regime_fit.v1` | `kt.llm_training.trading_scoring_gating_training` | scoring rubric market regime fit v1 | 2+ sources; boundary; candidate notes |
| RIT-P36-C-18 | `scoring_rubric.rule_compliance.v1` | `kt.llm_training.trading_scoring_gating_training` | scoring rubric rule compliance v1 | 2+ sources; boundary; candidate notes |
| RIT-P36-C-19 | `scoring_rubric.uncertainty_penalty.v1` | `kt.llm_training.trading_scoring_gating_training` | scoring rubric uncertainty penalty v1 | 2+ sources; boundary; candidate notes |
| RIT-P36-C-35 | `llm_judge.position_and_format_bias_check_required.v1` | `kt.llm_training.model_training_engineering` | llm judge position and format bias check required v1 | 2+ sources; boundary; candidate notes |
| RIT-P36-D-B14 | `research_feedback.llm_suggestion_is_hypothesis_only.v1` | `kt.ai_feedback_governance` | research feedback llm suggestion is hypothesis only v1 | 2+ sources; boundary; candidate notes |
| RIT-P36-D-B15 | `research_feedback.no_auto_strategy_parameter_update.v1` | `kt.ai_feedback_governance` | research feedback no auto strategy parameter update v1 | 2+ sources; boundary; candidate notes |
| RIT-P36-D-B20 | `risk_ledger.false_allow_cost_record_required.v1` | `kt.trading_ai_safety.false_allow_block_policy` | risk ledger false allow cost record required v1 | 2+ sources; boundary; candidate notes |

