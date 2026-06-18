# Phase 36 AI Engineering 分层知识点采集矩阵

本文承接 `docs/tasks/phase36_ai_engineering_gating_scoring_knowledge.md` 和 `docs/audit/phase36_ai_engineering_knowledge_scope_for_audit.json`，把原 101 条采集池与 12 条新增硬门合并为 113 条可执行采集项。

本文不是正式知识卡，不得作为 MCP/SearchLab/外部项目默认指导。所有条目必须后续经过联网采集、来源评分、冲突审计、candidate 审核、formal reviewed/approved 治理流程。

## 分层统计

| 层级 | 数量 | 语义 |
| --- | ---: | --- |
| P0-Core | 62 | 安全启动硬门；缺失或违反时必须阻断训练、评估、上线或默认指导。 |
| P0-Extended | 42 | 第一轮工程建设必需，用于补齐上线前评估、治理、追踪和审计能力。 |
| P1 | 9 | 优化增强项，后续补充具体 rubric、drift、risk ledger、方法细节。 |

## 矩阵

| ResearchTask | 层级 | 分组 | knowledge_id | canonical_node_id | 来源种子 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| RIT-P36-A-T01 | P0-Core | 通用模型训练工程 | `training_objective.task_definition_required.v1` | `kt.llm_training.model_training_engineering` | OpenAI model optimization docs / Hugging Face training docs | candidate_ready |
| RIT-P36-A-T02 | P0-Core | 通用模型训练工程 | `training_objective.rag_vs_finetune_boundary_required.v1` | `kt.llm_training.model_training_engineering` | OpenAI model optimization docs / Hugging Face training docs | candidate_ready |
| RIT-P36-A-T03 | P0-Core | 通用模型训练工程 | `dataset.schema_required.v1` | `kt.llm_training.model_training_engineering` | Datasheets for Datasets paper / ML data validation docs | candidate_ready |
| RIT-P36-A-T04 | P0-Core | 通用模型训练工程 | `dataset.source_lineage_required.v1` | `kt.llm_training.model_training_engineering` | Datasheets for Datasets paper / ML data validation docs | candidate_ready |
| RIT-P36-A-T05 | P0-Core | 通用模型训练工程 | `dataset.version_and_hash_required.v1` | `kt.llm_training.model_training_engineering` | Datasheets for Datasets paper / ML data validation docs | candidate_ready |
| RIT-P36-A-T06 | P0-Core | 通用模型训练工程 | `dataset.train_validation_test_split_required.v1` | `kt.llm_training.model_training_engineering` | Datasheets for Datasets paper / ML data validation docs | candidate_ready |
| RIT-P36-A-T08 | P0-Core | 通用模型训练工程 | `dataset.dataset_card_required.v1` | `kt.llm_training.model_training_engineering` | Datasheets for Datasets paper / ML data validation docs | candidate_ready |
| RIT-P36-A-T09 | P0-Core | 通用模型训练工程 | `leakage.train_test_contamination_block.v1` | `kt.llm_training.model_training_engineering` | scikit-learn common pitfalls / time-series validation docs | candidate_ready |
| RIT-P36-A-T10 | P0-Core | 通用模型训练工程 | `leakage.label_in_input_forbidden.v1` | `kt.llm_training.model_training_engineering` | scikit-learn common pitfalls / time-series validation docs | candidate_ready |
| RIT-P36-A-T16 | P0-Core | 通用模型训练工程 | `eval.holdout_test_set_required.v1` | `kt.llm_training.model_training_engineering` | OpenAI evals docs / ML evaluation papers | candidate_ready |
| RIT-P36-A-T17 | P0-Core | 通用模型训练工程 | `eval.production_like_eval_required.v1` | `kt.llm_training.model_training_engineering` | OpenAI evals docs / ML evaluation papers | candidate_ready |
| RIT-P36-A-T18 | P0-Core | 通用模型训练工程 | `training_run.config_and_hyperparameter_snapshot_required.v1` | `kt.llm_training.model_training_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-A-T19 | P0-Core | 通用模型训练工程 | `serving_consistency.train_like_serve_required.v1` | `kt.llm_training.model_training_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-A-T20 | P0-Core | 通用模型训练工程 | `safety.no_tool_permission_escalation.v1` | `kt.llm_training.model_training_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-B-S05 | P0-Core | 训练专属 schema 工程 | `trade_candidate.snapshot_required_before_scoring.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-B-S06 | P0-Core | 训练专属 schema 工程 | `trade_candidate.decision_timestamp_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-B-S08 | P0-Core | 训练专属 schema 工程 | `feature_schema.decision_time_only.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-B-S09 | P0-Core | 训练专属 schema 工程 | `feature_schema.feature_timestamp_cutoff_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-B-S10 | P0-Core | 训练专属 schema 工程 | `feature_schema.post_trade_fields_forbidden_in_input.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-B-S11 | P0-Core | 训练专属 schema 工程 | `outcome_schema.post_trade_fields_separated.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-B-S12 | P0-Core | 训练专属 schema 工程 | `label_schema.no_pnl_only_label.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-B-S20 | P0-Core | 训练专属 schema 工程 | `eval_case.no_training_overlap_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-C-01 | P0-Core | 交易 gating/scoring | `llm_role_boundary.scorer_not_executor.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-02 | P0-Core | 交易 gating/scoring | `llm_role_boundary.no_direct_order_execution.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-03 | P0-Core | 交易 gating/scoring | `llm_role_boundary.cannot_override_hard_risk_gate.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-08 | P0-Core | 交易 gating/scoring | `labeling.no_future_information.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-12 | P0-Core | 交易 gating/scoring | `data_quality.backtest_paper_live_separation.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-13 | P0-Core | 交易 gating/scoring | `data_quality.execution_cost_required.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-14 | P0-Core | 交易 gating/scoring | `data_quality.missing_core_fields_block_training.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-23 | P0-Core | 交易 gating/scoring | `rag.retrieval_required_before_trade_scoring.v1` | `kt.rag_engineering` | OpenAI file search docs / RAG evaluation docs | candidate_ready |
| RIT-P36-C-24 | P0-Core | 交易 gating/scoring | `rag.approved_machine_gate_allow_only_default_guidance.v1` | `kt.rag_engineering` | OpenAI file search docs / RAG evaluation docs | candidate_ready |
| RIT-P36-C-25 | P0-Core | 交易 gating/scoring | `rag.no_source_or_conflict_blocks_default_guidance.v1` | `kt.rag_engineering` | OpenAI file search docs / RAG evaluation docs | candidate_ready |
| RIT-P36-C-26 | P0-Core | 交易 gating/scoring | `rag.no_hit_requires_neutral_or_review.v1` | `kt.rag_engineering` | OpenAI file search docs / RAG evaluation docs | candidate_ready |
| RIT-P36-C-27 | P0-Core | 交易 gating/scoring | `mcp.read_only_knowledge_access.v1` | `kt.mcp` | MCP specification / MCP tool contract docs | candidate_ready |
| RIT-P36-C-28 | P0-Core | 交易 gating/scoring | `mcp.server_side_permission_enforcement_required.v1` | `kt.mcp` | MCP specification / MCP tool contract docs | candidate_ready |
| RIT-P36-C-29 | P0-Core | 交易 gating/scoring | `deployment.shadow_mode_before_live.v1` | `kt.llmops_deployment` | official_doc / paper | candidate_ready |
| RIT-P36-C-30 | P0-Core | 交易 gating/scoring | `deployment.llm_timeout_or_mcp_failure_fallback_required.v1` | `kt.llmops_deployment` | official_doc / paper | candidate_ready |
| RIT-P36-C-31 | P0-Core | 交易 gating/scoring | `versioning.model_prompt_rag_strategy_snapshot_required.v1` | `kt.llmops_deployment.artifact_lineage` | official_doc / paper | candidate_ready |
| RIT-P36-C-32 | P0-Core | 交易 gating/scoring | `audit.every_gate_decision_requires_trace.v1` | `kt.ai_governance_audit` | official_doc / paper | candidate_ready |
| RIT-P36-C-33 | P0-Core | 交易 gating/scoring | `eval.time_split_walk_forward_required.v1` | `kt.llm_training.model_training_engineering` | OpenAI evals docs / ML evaluation papers | candidate_ready |
| RIT-P36-C-34 | P0-Core | 交易 gating/scoring | `eval.score_calibration_required_before_gating.v1` | `kt.llm_training.model_training_engineering` | OpenAI evals docs / ML evaluation papers | candidate_ready |
| RIT-P36-C-36 | P0-Core | 交易 gating/scoring | `governance.dataset_card_and_model_card_required.v1` | `kt.ai_governance_audit` | official_doc / paper | candidate_ready |
| RIT-P36-D-B02 | P0-Core | 业务闭环治理 | `business_objective.success_metric_not_only_pnl.v1` | `kt.ai_business_objective` | official_doc / paper | candidate_ready |
| RIT-P36-D-B08 | P0-Core | 业务闭环治理 | `data_asset.eval_pool_must_not_train.v1` | `kt.ai_data_asset_management` | official_doc / paper | candidate_ready |
| RIT-P36-D-B09 | P0-Core | 业务闭环治理 | `data_asset.gold_set_immutable_required.v1` | `kt.ai_data_asset_management` | official_doc / paper | candidate_ready |
| RIT-P36-D-B10 | P0-Core | 业务闭环治理 | `method_selection.rag_first_baseline_required.v1` | `kt.llm_training.training_method_selection` | official_doc / paper | candidate_ready |
| RIT-P36-D-B11 | P0-Core | 业务闭环治理 | `method_selection.no_finetune_before_eval_baseline.v1` | `kt.llm_training.training_method_selection` | official_doc / paper | candidate_ready |
| RIT-P36-D-B16 | P0-Core | 业务闭环治理 | `runtime.llm_gate_is_suggestion_not_final_authority.v1` | `kt.trading_ai_safety` | official_doc / paper | candidate_ready |
| RIT-P36-D-B17 | P0-Core | 业务闭环治理 | `runtime.final_gate_deterministic_engine_required.v1` | `kt.trading_ai_safety` | official_doc / paper | candidate_ready |
| RIT-P36-D-B25 | P0-Core | 业务闭环治理 | `feedback.model_output_cannot_label_itself.v1` | `kt.ai_feedback_governance` | official_doc / paper | candidate_ready |
| RIT-P36-N-01 | P0-Core | 新增安全启动硬门 | `eval.counterfactual_outcome_missing_for_blocked_trades.v1` | `kt.llm_training.model_training_engineering` | OpenAI evals docs / ML evaluation papers | candidate_ready |
| RIT-P36-N-02 | P0-Core | 新增安全启动硬门 | `eval.off_policy_evaluation_required_for_gate_policy.v1` | `kt.llm_training.model_training_engineering` | OpenAI evals docs / ML evaluation papers | candidate_ready |
| RIT-P36-N-03 | P0-Core | 新增安全启动硬门 | `eval.blocked_trade_cannot_be_labeled_as_loss.v1` | `kt.llm_training.model_training_engineering` | OpenAI evals docs / ML evaluation papers | candidate_ready |
| RIT-P36-N-04 | P0-Core | 新增安全启动硬门 | `security.rag_context_is_untrusted_input.v1` | `kt.ai_security_privacy_compliance` | OWASP LLM prompt injection cheat sheet / NIST AI RMF | candidate_ready |
| RIT-P36-N-05 | P0-Core | 新增安全启动硬门 | `security.prompt_injection_test_required_for_trade_context.v1` | `kt.ai_security_privacy_compliance` | OWASP LLM prompt injection cheat sheet / NIST AI RMF | candidate_ready |
| RIT-P36-N-06 | P0-Core | 新增安全启动硬门 | `data_privacy.no_secret_or_account_identifier_in_training.v1` | `kt.ai_security_privacy_compliance` | ISO/IEC 42001 / NIST AI RMF | candidate_ready |
| RIT-P36-N-07 | P0-Core | 新增安全启动硬门 | `data_license.market_data_license_check_required.v1` | `kt.ai_security_privacy_compliance` | market data vendor terms / exchange data policy docs | candidate_ready |
| RIT-P36-N-08 | P0-Core | 新增安全启动硬门 | `eval.deterministic_baseline_required_before_llm_gate.v1` | `kt.llm_training.model_training_engineering` | OpenAI evals docs / ML evaluation papers | candidate_ready |
| RIT-P36-N-09 | P0-Core | 新增安全启动硬门 | `eval.ablation_required_for_rag_prompt_model_components.v1` | `kt.llm_training.model_training_engineering` | OpenAI evals docs / ML evaluation papers | candidate_ready |
| RIT-P36-N-10 | P0-Core | 新增安全启动硬门 | `label_factory.inter_annotator_agreement_required.v1` | `kt.ai_label_factory` | official_doc / paper | candidate_ready |
| RIT-P36-N-11 | P0-Core | 新增安全启动硬门 | `feature_store.feature_schema_registry_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-N-12 | P0-Core | 新增安全启动硬门 | `serving_consistency.training_serving_parity_test_required.v1` | `kt.llm_training.model_training_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-A-T07 | P0-Extended | 通用模型训练工程 | `dataset.deduplication_required.v1` | `kt.llm_training.model_training_engineering` | Datasheets for Datasets paper / ML data validation docs | candidate_ready |
| RIT-P36-A-T11 | P0-Extended | 通用模型训练工程 | `sft.when_to_use_and_not_use.v1` | `kt.llm_training.model_training_engineering` | OpenAI fine-tuning docs / Hugging Face SFTTrainer docs | candidate_ready |
| RIT-P36-A-T12 | P0-Extended | 通用模型训练工程 | `sft.output_schema_consistency_required.v1` | `kt.llm_training.model_training_engineering` | OpenAI fine-tuning docs / Hugging Face SFTTrainer docs | candidate_ready |
| RIT-P36-A-T13 | P0-Extended | 通用模型训练工程 | `preference_training.preference_pair_schema_required.v1` | `kt.llm_training.model_training_engineering` | DPO paper / TRL DPOTrainer docs | candidate_ready |
| RIT-P36-A-T14 | P0-Extended | 通用模型训练工程 | `preference_training.chosen_rejected_reason_required.v1` | `kt.llm_training.model_training_engineering` | DPO paper / TRL DPOTrainer docs | candidate_ready |
| RIT-P36-A-T15 | P0-Extended | 通用模型训练工程 | `dpo.preference_data_quality_required.v1` | `kt.llm_training.model_training_engineering` | DPO paper / TRL docs | candidate_ready |
| RIT-P36-B-S01 | P0-Extended | 训练专属 schema 工程 | `trade_data.raw_trade_record_required_fields.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-B-S02 | P0-Extended | 训练专属 schema 工程 | `trade_data.strategy_id_and_version_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-B-S03 | P0-Extended | 训练专属 schema 工程 | `trade_data.source_mode_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-B-S04 | P0-Extended | 训练专属 schema 工程 | `trade_data.fee_slippage_execution_cost_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-B-S07 | P0-Extended | 训练专属 schema 工程 | `trade_candidate.market_risk_execution_context_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-B-S13 | P0-Extended | 训练专属 schema 工程 | `label_schema.good_loss_bad_win_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-B-S14 | P0-Extended | 训练专属 schema 工程 | `label_schema.multi_dimensional_trade_quality.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-B-S15 | P0-Extended | 训练专属 schema 工程 | `label_schema.label_reason_codes_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-B-S16 | P0-Extended | 训练专属 schema 工程 | `training_example.sft_schema_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-B-S17 | P0-Extended | 训练专属 schema 工程 | `training_example.input_target_separation.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-B-S18 | P0-Extended | 训练专属 schema 工程 | `preference_pair.not_based_on_pnl_only.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-B-S19 | P0-Extended | 训练专属 schema 工程 | `eval_case.time_strategy_regime_split_required.v1` | `kt.llm_training.training_dataset_schema_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-C-04 | P0-Extended | 交易 gating/scoring | `training_data.trade_sample_schema_required.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-05 | P0-Extended | 交易 gating/scoring | `training_data.strategy_version_required.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-06 | P0-Extended | 交易 gating/scoring | `training_data.decision_timestamp_required.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-07 | P0-Extended | 交易 gating/scoring | `training_data.feature_timestamp_cutoff_required.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-09 | P0-Extended | 交易 gating/scoring | `labeling.no_pnl_only_labeling.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-10 | P0-Extended | 交易 gating/scoring | `labeling.good_loss_bad_win_distinction.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-11 | P0-Extended | 交易 gating/scoring | `labeling.ambiguous_trade_needs_human_review.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-20 | P0-Extended | 交易 gating/scoring | `scoring_rubric.reason_code_required.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-21 | P0-Extended | 交易 gating/scoring | `gating.low_confidence_cannot_allow.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-22 | P0-Extended | 交易 gating/scoring | `gating.false_allow_more_dangerous_than_false_block.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-D-B01 | P0-Extended | 业务闭环治理 | `business_objective.llm_trader_acceptance_criteria_required.v1` | `kt.ai_business_objective` | official_doc / paper | candidate_ready |
| RIT-P36-D-B03 | P0-Extended | 业务闭环治理 | `task_taxonomy.pre_trade_post_trade_task_separation.v1` | `kt.llm_training.trading_llm_task_taxonomy` | official_doc / paper | candidate_ready |
| RIT-P36-D-B04 | P0-Extended | 业务闭环治理 | `task_taxonomy.each_task_requires_schema_and_eval.v1` | `kt.llm_training.trading_llm_task_taxonomy` | official_doc / paper | candidate_ready |
| RIT-P36-D-B05 | P0-Extended | 业务闭环治理 | `label_factory.label_guideline_required.v1` | `kt.ai_label_factory` | official_doc / paper | candidate_ready |
| RIT-P36-D-B06 | P0-Extended | 业务闭环治理 | `label_factory.gold_set_required.v1` | `kt.ai_label_factory` | official_doc / paper | candidate_ready |
| RIT-P36-D-B07 | P0-Extended | 业务闭环治理 | `label_factory.label_conflict_resolution_required.v1` | `kt.ai_label_factory` | official_doc / paper | candidate_ready |
| RIT-P36-D-B12 | P0-Extended | 业务闭环治理 | `capability_boundary.llm_not_primary_price_predictor.v1` | `kt.llm_training.trading_llm_task_taxonomy` | official_doc / paper | candidate_ready |
| RIT-P36-D-B13 | P0-Extended | 业务闭环治理 | `capability_boundary.numeric_model_vs_llm_role_split.v1` | `kt.llm_training.trading_llm_task_taxonomy` | official_doc / paper | candidate_ready |
| RIT-P36-D-B18 | P0-Extended | 业务闭环治理 | `calibration.llm_score_not_probability.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-D-B19 | P0-Extended | 业务闭环治理 | `calibration.threshold_requires_shadow_data.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-D-B21 | P0-Extended | 业务闭环治理 | `lineage.model_prompt_rag_data_strategy_bound_together.v1` | `kt.llmops_deployment.artifact_lineage` | official_doc / paper | candidate_ready |
| RIT-P36-D-B22 | P0-Extended | 业务闭环治理 | `redteam.hard_gate_override_attempt_test.v1` | `kt.trading_ai_safety` | official_doc / paper | candidate_ready |
| RIT-P36-D-B23 | P0-Extended | 业务闭环治理 | `approval.hard_gate_enable_requires_approval.v1` | `kt.ai_governance_audit` | official_doc / paper | candidate_ready |
| RIT-P36-D-B24 | P0-Extended | 业务闭环治理 | `readiness.offline_eval_pass_not_equal_live_ready.v1` | `kt.llmops_deployment` | official_doc / paper | candidate_ready |
| RIT-P36-C-15 | P1 | 交易 gating/scoring | `scoring_rubric.setup_quality.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-16 | P1 | 交易 gating/scoring | `scoring_rubric.risk_reward_quality.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-17 | P1 | 交易 gating/scoring | `scoring_rubric.market_regime_fit.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-18 | P1 | 交易 gating/scoring | `scoring_rubric.rule_compliance.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-19 | P1 | 交易 gating/scoring | `scoring_rubric.uncertainty_penalty.v1` | `kt.llm_training.trading_scoring_gating_training` | official_doc / paper | candidate_ready |
| RIT-P36-C-35 | P1 | 交易 gating/scoring | `llm_judge.position_and_format_bias_check_required.v1` | `kt.llm_training.model_training_engineering` | official_doc / paper | candidate_ready |
| RIT-P36-D-B14 | P1 | 业务闭环治理 | `research_feedback.llm_suggestion_is_hypothesis_only.v1` | `kt.ai_feedback_governance` | official_doc / paper | candidate_ready |
| RIT-P36-D-B15 | P1 | 业务闭环治理 | `research_feedback.no_auto_strategy_parameter_update.v1` | `kt.ai_feedback_governance` | official_doc / paper | candidate_ready |
| RIT-P36-D-B20 | P1 | 业务闭环治理 | `risk_ledger.false_allow_cost_record_required.v1` | `kt.trading_ai_safety.false_allow_block_policy` | official_doc / paper | candidate_ready |

## 采集验收门槛

```text
1. 每条知识至少 2 个可追溯来源，优先 official_doc、paper、framework_doc、standard_or_risk_framework。
2. 必须写明 applies_when、not_applicable_when、assumptions、risk_notes、source_quality、conflict_audit。
3. P0-Core 缺来源或冲突未消解时，不能进入 reviewed，更不能进入 approved。
4. RAG/MCP/Agent 安全类知识必须默认把 retrieved context 和 tool output 视为非可信输入。
5. 外部项目私有数据、策略参数、账户事实和密钥不得进入通用知识。
6. 所有候选先进入 candidate，不能直接成为 approved。
```

