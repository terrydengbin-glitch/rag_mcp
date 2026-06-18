# Phase 41 P0-Core 候选知识来源采集记录

生成日期：2026-06-10

## 结论

本轮按 Phase 41 P0-Core 矩阵生成候选知识 22 条，跳过已存在候选 0 条；当前 P0-Core 规划总数为 22 条。

本轮只生成 candidate，不进入 formal reviewed，不进入 approved，也不会作为默认指导。

## 主要来源族

| 来源族 | 用途 |
| --- | --- |
| scikit-learn | Logistic Regression baseline、概率校准、class_weight、sample_weight、TimeSeriesSplit、数据泄漏边界 |
| LightGBM / XGBoost / CatBoost | GBDT 候选模型、类别特征条件候选和同场评估边界 |
| NIST AI RMF | AI 风险治理、度量、管理和人类监督边界 |
| MLflow / DVC | model registry、dataset lineage、split manifest、release manifest 和可复现性 |
| Feast / TFDV | feature store、online/offline parity、schema、skew 和数据验证 |
| Qwen / JSON Schema / Hugging Face TRL | Qwen3 审计助手、strict JSON、SFT 格式训练和 reason code 输出 |
| OWASP LLM01 | RAG context、用户摘要和检索文档的不可信输入与 prompt-injection 防护 |

## P0-Core 主题

| topic_id | canonical_node_id | claim_type | model_role | 来源数 |
| --- | --- | --- | --- | ---: |
| P41-A01 | `kt.ai_engineering.numeric_scoring.model_family_selection` | model_selection_rule | tabular_scorer | 4 |
| P41-A02 | `kt.ai_engineering.numeric_scoring.model_family_selection` | model_selection_rule | tabular_scorer | 3 |
| P41-A03 | `kt.ai_engineering.numeric_scoring.model_family_selection` | model_selection_rule | tabular_scorer | 4 |
| P41-A05 | `kt.ai_engineering.numeric_scoring.model_family_selection` | governance_rule | tabular_scorer | 3 |
| P41-B01 | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | training_policy_rule | tabular_scorer | 4 |
| P41-B02 | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | leakage_boundary_rule | tabular_scorer | 3 |
| P41-B03 | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | leakage_boundary_rule | tabular_scorer | 3 |
| P41-B05 | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | lineage_rule | tabular_scorer | 3 |
| P41-C01 | `kt.ai_engineering.calibration_threshold.uncertainty` | calibration_rule | calibrator | 3 |
| P41-C02 | `kt.ai_engineering.calibration_threshold.uncertainty` | leakage_boundary_rule | calibrator | 3 |
| P41-C03 | `kt.ai_engineering.calibration_threshold.uncertainty` | threshold_policy_rule | final_gate | 3 |
| P41-D01 | `kt.ai_engineering.decision_time_feature_contract.feature_store` | leakage_boundary_rule | tabular_scorer | 3 |
| P41-D02 | `kt.ai_engineering.decision_time_feature_contract.feature_store` | serving_consistency_rule | tabular_scorer | 3 |
| P41-D03 | `kt.ai_engineering.decision_time_feature_contract.feature_store` | lineage_rule | tabular_scorer | 3 |
| P41-D04 | `kt.ai_engineering.decision_time_feature_contract.feature_store` | label_boundary_rule | tabular_scorer | 3 |
| P41-E01 | `kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant` | runtime_boundary_rule | llm_audit_assistant | 3 |
| P41-E02 | `kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant` | output_contract_rule | llm_audit_assistant | 3 |
| P41-E03 | `kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant` | citation_rule | llm_audit_assistant | 3 |
| P41-E05 | `kt.ai_engineering.llm_audit_assistant.qwen3_training_recipe` | training_boundary_rule | llm_audit_assistant | 3 |
| P41-E09 | `kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant` | untrusted_context_guard_rule | llm_audit_assistant | 3 |
| P41-F01 | `kt.ai_engineering.model_release_governance.hybrid_runtime_contract` | runtime_boundary_rule | final_gate | 3 |
| P41-F02 | `kt.ai_engineering.model_release_governance.hybrid_runtime_contract` | release_governance_rule | final_gate | 3 |

## 边界

本轮没有采集 K 线、fill model、订单状态机、实盘风控阈值或交易所执行适配器本体知识。这些内容仍归 Phase 37 / Trading Engineering。

