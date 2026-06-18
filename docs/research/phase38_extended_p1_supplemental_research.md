# Phase 38 P0-Extended / P1 补证采集记录

## 目标

根据 Phase 38 P0-Extended / P1 严格审计报告，为 13 条 needs_more_evidence 候选和 C10-R1 重建候选补充 claim-specific 来源。本记录只用于二审准备，不代表 reviewed、approved、default guidance 或 hard gate。

## 补证结果

### P38-A09 - cand_20260610_phase38_p38_a09_feature_attribution_001

- 补丁摘要：feature attribution 只能解释模型输出贡献或相关性模式，不能替代因果识别；若要写 causal explanation，必须另有 causal graph、干预或反事实设计。
- 来源数量：4
- 来源 ID：src_shap_causal_warning, src_pearl_causal_inference_primer
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_a09_feature_attribution_001.json`

### P38-A10 - cand_20260610_phase38_p38_a10_ranking_model_review_priority_001

- 补丁摘要：ranking model 可用于 review_priority 排序增强，但输出只决定人工复核优先级，不得作为交易 gate 或收益承诺；必须用 NDCG/MAP 等排序指标独立评估。
- 来源数量：4
- 来源 ID：src_sklearn_ndcg_score, src_lightgbm_lambdarank
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_a10_ranking_model_review_priority_001.json`

### P38-B10 - cand_20260610_phase38_p38_b10_conformal_bayesian_calibration_001

- 补丁摘要：conformal / Bayesian calibration 只能作为不确定性或校准增强层；必须声明假设、校准集和覆盖率/校准指标，不能替代 deterministic final gate。
- 来源数量：4
- 来源 ID：src_conformal_prediction_tutorial, src_sklearn_probability_calibration
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_b10_conformal_bayesian_calibration_001.json`

### P38-C10-R1 - cand_20260610_phase38_p38_c10_cross_market_feature_availability_recheck_001

- 补丁摘要：跨市场迁移必须重新检查 point-in-time 特征可用性、training-serving skew、target domain 分布差异和 feature store AS-OF join；通过前不得进入 formal draft。
- 来源数量：5
- 来源 ID：src_feast_point_in_time_joins, src_tfdv_training_serving_skew, src_domain_adaptation_transfer_learning_intro
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_c10_cross_market_feature_availability_recheck_001.json`

### P38-D07 - cand_20260610_phase38_p38_d07_rag_prompt_baseline_sft_001

- 补丁摘要：RAG/prompt baseline 应先建立可审计基线；只有当检索、提示和结构化输出仍无法稳定满足 schema/reason code 时，才考虑 SFT/LoRA。
- 来源数量：5
- 来源 ID：src_openai_model_optimization, src_rag_original_paper
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_d07_rag_prompt_baseline_sft_001.json`

### P38-D08 - cand_20260610_phase38_p38_d08_sft_lora_schema_reason_code_001

- 补丁摘要：SFT LoRA 仅用于稳定输出 schema、reason code 和审计格式；格式约束仍应由 JSON Schema/structured output 校验，LoRA 不提供事实来源。
- 来源数量：6
- 来源 ID：src_hf_peft_lora, src_hf_structured_output, src_json_schema_docs
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_d08_sft_lora_schema_reason_code_001.json`

### P38-D10 - cand_20260610_phase38_p38_d10_teacher_model_baseline_001

- 补丁摘要：teacher model 可作审计 baseline 或 judge 辅助，但事实必须来自 citation resolver 和 formal knowledge；teacher 输出不得作为无来源事实。
- 来源数量：5
- 来源 ID：src_ragas_faithfulness, src_langfuse_llm_as_judge, src_cek_ta_phase38_rag_citation_reason_contract
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_d10_teacher_model_baseline_001.json`

### P38-E07 - cand_20260610_phase38_p38_e07_rag_prompt_model_threshold_ablation_001

- 补丁摘要：RAG、prompt、model、threshold 的改动必须通过隔离 ablation 比较；每次只改变一个主要变量，并记录参数、指标、artifact 和版本。
- 来源数量：5
- 来源 ID：src_pykeen_ablation_study, src_mlflow_tracking
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_e07_rag_prompt_model_threshold_ablation_001.json`

### P38-E08 - cand_20260610_phase38_p38_e08_shadow_no_hit_conflict_citation_completeness_001

- 补丁摘要：shadow 记录必须包含 no-hit、conflict、citation completeness 和 faithfulness 相关字段，用于发现 RAG 覆盖缺口，不得自动放行交易。
- 来源数量：4
- 来源 ID：src_ragas_faithfulness, src_cek_ta_phase38_rag_citation_reason_contract
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_e08_shadow_no_hit_conflict_citation_completeness_001.json`

### P38-E09 - cand_20260610_phase38_p38_e09_false_block_opportunity_paper_replay_001

- 补丁摘要：false block opportunity 可用 paper/replay/OPE/人工复核估计，但 fill、slippage、fee、latency 和成本假设必须引用 Trading Engineering，不得由 AI Engineering 自行定义。
- 来源数量：4
- 来源 ID：src_open_bandit_pipeline, src_cek_ta_phase37_fill_cost_boundary
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_e09_false_block_opportunity_paper_replay_001.json`

### P38-E10 - cand_20260610_phase38_p38_e10_active_learning_review_sampling_001

- 补丁摘要：active learning review sampling 只能用于提高人工标注/复核效率；采样策略要平衡 uncertainty、diversity 和代表性，不能用作收益承诺或自动 gate。
- 来源数量：3
- 来源 ID：src_deep_active_learning_survey
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_e10_active_learning_review_sampling_001.json`

### P38-F10 - cand_20260610_phase38_p38_f10_model_compression_001

- 补丁摘要：model compression、quantization、distillation 只能在不破坏 schema、citation、校准、latency 和审计指标后考虑；压缩模型必须重新跑评估和回滚预案。
- 来源数量：4
- 来源 ID：src_llm_compression_survey, src_model_compression_survey_frontiers
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_f10_model_compression_001.json`

### P38-G05 - cand_20260610_phase38_p38_g05_citation_completeness_shadow_001

- 补丁摘要：citation completeness 应进入 shadow 指标，衡量每条审计结论是否能解析到正式知识和来源；低完整率必须触发 no-hit/补证/人工复核。
- 来源数量：4
- 来源 ID：src_ragas_faithfulness, src_cek_ta_phase38_rag_citation_reason_contract
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_g05_citation_completeness_shadow_001.json`

### P38-G06 - cand_20260610_phase38_p38_g06_no_hit_query_001

- 补丁摘要：no-hit query 必须进入知识缺口队列，并记录 query、scope、requested_decision、missing_node 和下游影响；不得由 AI 现场编造规则。
- 来源数量：4
- 来源 ID：src_cek_ta_phase35_active_retrieval_protocol, src_cek_ta_phase38_rag_citation_reason_contract
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_g06_no_hit_query_001.json`

## 边界

```text
1. 补证完成不等于审计通过。
2. 本批候选仍停留在 needs_more_evidence / ready_for_reaudit。
3. 二审通过后才允许进入 formal draft 队列。
4. 任何候选都不能直接进入 reviewed、approved、default guidance 或 hard gate。
5. fill、成本、风控、执行、K 线结构等交易规则本体继续路由到 Trading Engineering。
```
