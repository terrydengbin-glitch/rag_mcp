# Phase 41 P0-Extended/P1 补证采集记录

生成日期：2026-06-10
对应任务：CEK-TA-332

## 补证范围

本次只处理严格审计标记为 `needs_more_evidence` 的 6 条候选：P41-A07、P41-B06、P41-E07、P41-F04、P41-F07、P41-F08。

## 采集原则

1. 外部来源支撑通用方法、平台治理、安全或监管控制。
2. CEK-TA 内部契约只支撑字段、状态流、权限和 AI/Trading 分支边界。
3. 补证后仍保持 candidate 状态，不创建 reviewed、approved、default guidance 或 hard gate。

## 补证结果

### P41-A07

- 候选：`cand_20260610_phase41_p41_a07_feature_attribution_top_features_final_gate_001`
- 文件：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase41_p41_a07_feature_attribution_top_features_final_gate_001.json`
- 新增来源：src_shap_causal_warning, src_phase41_runtime_contract
- 当前来源数量：5

### P41-B06

- 候选：`cand_20260610_phase41_p41_b06_active_learning_hard_example_mining_gold_eval_001`
- 文件：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase41_p41_b06_active_learning_hard_example_mining_gold_eval_001.json`
- 新增来源：src_active_learning_survey, src_ohem_paper, src_phase41_training_data_contract
- 当前来源数量：6

### P41-E07

- 候选：`cand_20260610_phase41_p41_e07_rag_first_prompt_sft_lora_001`
- 文件：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase41_p41_e07_rag_first_prompt_sft_lora_001.json`
- 新增来源：src_google_rag_finetune_guide, src_promptfoo_rag_eval, src_phase41_runtime_contract
- 当前来源数量：6

### P41-F04

- 候选：`cand_20260610_phase41_p41_f04_champion_challenger_offline_shadow_paper_soft_gate_champion_paper_replay_fill_cost_execution_phase_37_ai_engineering_001`
- 文件：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase41_p41_f04_champion_challenger_offline_shadow_paper_soft_gate_champion_paper_replay_fill_cost_execution_phase_37_ai_engineering_001.json`
- 新增来源：src_aws_sagemaker_shadow_tests, src_microsoft_shadow_testing, src_quantconnect_paper_trading, src_quantconnect_trade_fills, src_phase41_runtime_contract
- 当前来源数量：8

### P41-F07

- 候选：`cand_20260610_phase41_p41_f07_cek_ta_resolver_001`
- 文件：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase41_p41_f07_cek_ta_resolver_001.json`
- 新增来源：src_nist_least_privilege, src_owasp_llm_top10, src_phase41_runtime_contract
- 当前来源数量：6

### P41-F08

- 候选：`cand_20260610_phase41_p41_f08_hybrid_scoring_runtime_scorer_calibrator_rag_qwen3_final_gate_latency_budget_timeout_fallback_fail_to_review_fail_closed_001`
- 文件：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase41_p41_f08_hybrid_scoring_runtime_scorer_calibrator_rag_qwen3_final_gate_latency_budget_timeout_fallback_fail_to_review_fail_closed_001.json`
- 新增来源：src_google_sre_slo, src_google_sre_overload, src_fca_algo_trading_review, src_sec_knight_capital, src_phase41_runtime_contract
- 当前来源数量：8

