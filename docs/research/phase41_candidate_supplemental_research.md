# Phase 41 候选审计补证记录

生成日期：2026-06-10

## 结论

本轮导入 Phase 41 严格审计结果后，5 条候选被标记为 needs_more_evidence，3 条空 slug 候选被拒绝并重建为 R1 候选。

本轮只补候选来源和契约，不生成 formal reviewed，不设置 approved/default guidance。

## 补证来源方向

| 方向 | 来源 |
| --- | --- |
| 校准与加权后复核 | scikit-learn probability calibration、CEK-TA recalibration_after_weighting_report |
| 成本敏感阈值与复核容量 | scikit-learn classification threshold、cost-sensitive threshold、CEK-TA review_capacity_policy |
| RAG faithfulness / citation resolver | Ragas、DeepEval、Promptfoo、CEK-TA citation resolver contract |
| point-in-time 与 offline/online parity | Feast point-in-time joins、Databricks point-in-time、TFDV training-serving skew |
| final gate 与发布治理 | SEC Knight、FCA algorithmic controls、CEK-TA composite release manifest |

## 二审候选

| research_task_id | candidate_id | source_count | queue_group |
| --- | --- | ---: | --- |
| P41-A05-R1 | cand_20260610_phase41_p41_a05_model_selection_business_cost_latency_explainability_calibration_governance_001 | 6 | pending |
| P41-B01 | cand_20260610_phase41_p41_b01_bad_trade_false_allow_class_weight_sample_weight_001 | 6 | needs_more_evidence |
| P41-B03-R1 | cand_20260610_phase41_p41_b03_time_aware_split_no_random_shuffle_001 | 4 | pending |
| P41-C03 | cand_20260610_phase41_p41_c03_threshold_policy_false_allow_false_block_review_capacity_001 | 6 | needs_more_evidence |
| P41-D02-R1 | cand_20260610_phase41_p41_d02_offline_online_feature_parity_default_guidance_block_001 | 5 | pending |
| P41-E03 | cand_20260610_phase41_p41_e03_qwen3_rag_abstain_needs_human_review_001 | 7 | needs_more_evidence |
| P41-E09 | cand_20260610_phase41_p41_e09_rag_context_qwen3_prompt_injection_guard_citation_resolver_unsupported_claim_detector_schema_validation_001 | 6 | needs_more_evidence |
| P41-F02 | cand_20260610_phase41_p41_f02_composite_release_manifest_scorer_calibrator_threshold_qwen3_prompt_rag_index_reason_taxonomy_rollback_target_001 | 4 | needs_more_evidence |
