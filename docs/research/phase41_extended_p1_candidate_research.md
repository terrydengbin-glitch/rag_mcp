# Phase 41 P0-Extended/P1 候选知识来源采集记录

生成日期：2026-06-10

## 结论

本轮将 P0-Extended 12 条和 P1 7 条合并采集，计划 19 条，生成候选 `19` 条，跳过已存在 `0` 条。

本轮只生成 candidate，不进入 formal reviewed，不进入 approved，也不会作为默认指导。

## 主要来源族

| 来源族 | 用途 |
| --- | --- |
| CatBoost / scikit-learn / SHAP | 条件模型、ensemble、解释边界、group split 和校准增强 |
| MAPIE / modAL | conformal / abstain band、active learning 和 hard-example mining 增强边界 |
| Qwen / TRL / vLLM | Qwen3 thinking、DPO、RAG-first、服务化条件和延迟吞吐边界 |
| Feast / MLflow / Ray / Kubeflow | feature store、model registry、分布式训练和流水线平台条件引入 |
| NIST AI RMF / CEK-TA 内部契约 | AI 治理、只读 MCP、路径 resolver、final gate 和发布边界 |

## 本批主题

| topic_id | priority | canonical_node_id | claim_type | model_role | 来源数 |
| --- | --- | --- | --- | --- | ---: |
| P41-A04 | P0-Extended | `kt.ai_engineering.numeric_scoring.model_family_selection` | conditional_model_rule | tabular_scorer | 3 |
| P41-A06 | P0-Extended | `kt.ai_engineering.numeric_scoring.model_family_selection` | extension_rule | tabular_scorer | 3 |
| P41-A07 | P0-Extended | `kt.ai_engineering.numeric_scoring.scorer_explainability` | explainability_boundary_rule | tabular_scorer | 3 |
| P41-B04 | P0-Extended | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | leakage_boundary_rule | tabular_scorer | 3 |
| P41-B06 | P1 | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | extension_rule | tabular_scorer | 3 |
| P41-C04 | P0-Extended | `kt.ai_engineering.calibration_threshold.uncertainty` | calibration_method_rule | calibrator | 3 |
| P41-C05 | P0-Extended | `kt.ai_engineering.calibration_threshold.uncertainty` | monitoring_rule | calibrator | 3 |
| P41-C06 | P1 | `kt.ai_engineering.calibration_threshold.uncertainty` | extension_rule | calibrator | 3 |
| P41-D05 | P1 | `kt.ai_engineering.decision_time_feature_contract.feature_store` | platform_boundary_rule | platform_governance | 3 |
| P41-E04 | P0-Extended | `kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant` | usage_policy_rule | llm_audit_assistant | 3 |
| P41-E06 | P0-Extended | `kt.ai_engineering.llm_audit_assistant.qwen3_training_recipe` | preference_training_rule | llm_audit_assistant | 3 |
| P41-E07 | P0-Extended | `kt.ai_engineering.llm_audit_assistant.qwen3_training_recipe` | method_selection_rule | llm_audit_assistant | 3 |
| P41-E08 | P1 | `kt.ai_engineering.llm_audit_assistant.qwen3_training_recipe` | serving_boundary_rule | platform_governance | 3 |
| P41-F03 | P0-Extended | `kt.ai_engineering.model_release_governance.hybrid_runtime_contract` | observability_rule | final_gate | 3 |
| P41-F04 | P0-Extended | `kt.ai_engineering.model_release_governance.hybrid_runtime_contract` | promotion_gate_rule | final_gate | 3 |
| P41-F05 | P1 | `kt.ai_engineering.model_release_governance.training_platform_governance` | platform_boundary_rule | platform_governance | 3 |
| P41-F06 | P1 | `kt.ai_engineering.model_release_governance.training_platform_governance` | platform_boundary_rule | platform_governance | 3 |
| P41-F07 | P1 | `kt.ai_engineering.model_release_governance.training_platform_governance` | integration_boundary_rule | platform_governance | 3 |
| P41-F08 | P0-Extended | `kt.ai_engineering.model_release_governance.hybrid_runtime_contract` | runtime_fallback_rule | final_gate | 3 |

## 边界

本批 P0-Extended/P1 是增强能力采集，不改变 P0-Core 的基本运行链路；不得把平台工具、feature store、本地 serving 或分布式训练变成默认依赖。

