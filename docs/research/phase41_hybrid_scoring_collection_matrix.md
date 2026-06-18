# Phase 41 Hybrid Scoring 与 Qwen3 审计助手知识采集矩阵

生成日期：2026-06-10
状态：collection matrix draft
对应任务：CEK-TA-322

## 采集原则

```text
1. Phase 41 只采集 AI Engineering 中 hybrid scoring / Qwen3 audit / deterministic final gate 的工程知识。
2. 表格/统计模型只作为 numeric scorer、risk ranking、review priority，不作为最终交易 gate。
3. Qwen3 只作为 audit assistant，不作为 numeric scorer、final gate 或事实来源。
4. final gate 只读取策略版本、阈值策略、风控规则命中、release manifest 和人工审批。
5. K 线、fill model、订单状态机、仓位和风控规则本体属于 Trading Engineering，只能作为 related_trading_refs 引用。
6. reviewed 不等于 approved；本轮输出先进候选审计，不直接进入默认强指导。
```

## 来源种子

| 来源 | URL | 类型 | 覆盖方向 |
| --- | --- | --- | --- |
| scikit-learn Logistic Regression | https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression | official_doc | 透明 baseline、线性分类器 |
| scikit-learn Probability Calibration | https://scikit-learn.org/stable/modules/calibration.html | official_doc | 概率校准、可靠性曲线 |
| scikit-learn Common Pitfalls | https://scikit-learn.org/stable/common_pitfalls.html | official_doc | 数据泄漏、评估陷阱 |
| scikit-learn TimeSeriesSplit | https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html | official_doc | 时间切分、未来信息泄漏 |
| scikit-learn compute_class_weight | https://scikit-learn.org/stable/modules/generated/sklearn.utils.class_weight.compute_class_weight.html | official_doc | 类别不平衡、class weight |
| LightGBM Documentation | https://lightgbm.readthedocs.io/ | official_doc | GBDT scorer |
| XGBoost Documentation | https://xgboost.readthedocs.io/ | official_doc | GBDT scorer |
| CatBoost Documentation | https://catboost.ai/docs/ | official_doc | 类别特征 GBDT |
| CatBoost paper | https://arxiv.org/abs/1810.11363 | research_paper | 类别特征和 ordered boosting |
| XGBoost paper | https://arxiv.org/abs/1603.02754 | research_paper | tree boosting |
| LightGBM paper | https://papers.nips.cc/paper_files/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html | research_paper | histogram GBDT、leaf-wise growth |
| SHAP paper | https://arxiv.org/abs/1705.07874 | research_paper | 模型解释 |
| NIST AI RMF | https://www.nist.gov/itl/ai-risk-management-framework | governance_framework | AI 风险治理 |
| MLflow Model Registry | https://mlflow.org/docs/latest/ml/model-registry/ | official_doc | registry、版本、stage/alias |
| DVC Data Versioning | https://dvc.org/doc | official_doc | 数据版本、pipeline、hash |
| Feast Documentation | https://docs.feast.dev/ | official_doc | feature store、offline/online parity |
| Kubeflow Pipelines | https://www.kubeflow.org/docs/components/pipelines/ | official_doc | 训练流水线治理 |
| Ray Documentation | https://docs.ray.io/ | official_doc | 分布式训练条件引入 |
| vLLM Documentation | https://docs.vllm.ai/ | official_doc | LLM serving 条件引入 |
| Hugging Face TRL | https://huggingface.co/docs/trl/ | official_doc | SFT/DPO/偏好训练 |
| Qwen Documentation | https://qwen.readthedocs.io/ | official_doc | Qwen/Qwen3 模型使用、推理模式、部署边界 |
| JSON Schema | https://json-schema.org/ | standard_doc | strict JSON 输出结构 |
| OWASP LLM01 Prompt Injection | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ | security_standard | prompt injection、不可信上下文 |
| SEC Knight Capital Release | https://www.sec.gov/newsroom/press-releases/2013-222 | regulator_release | 运行时控制、异常和市场接入风险 |
| FCA Algorithmic Trading Controls | https://www.fca.org.uk/publications/multi-firm-reviews/algorithmic-trading-controls-high-level-observations | regulator_review | 算法交易控制和治理 |
| CEK-TA Phase 41 Runtime Contract | `docs/contracts/phase41_hybrid_scoring_runtime_contract.md` | internal_contract | scorer / Qwen3 / final gate 权限边界 |
| CEK-TA Phase 41 Training Data Contract | `docs/contracts/phase41_tabular_llm_training_data_contract.md` | internal_contract | feature、label、dataset、registry 契约 |

## 采集矩阵

### A. Model Family Selection

| ID | 优先级 | canonical_node_id | 知识点 | claim_type | model_role | 主要来源 |
| --- | --- | --- | --- | --- | --- | --- |
| P41-A01 | P0-Core | `kt.ai_engineering.numeric_scoring.model_family_selection` | Rule baseline、Logistic Regression、LightGBM、XGBoost 必须同场比较；CatBoost 在类别变量丰富或类别处理成本较高时作为条件候选，不能预设胜出 | model_selection_rule | tabular_scorer | scikit-learn、LightGBM、XGBoost、CatBoost |
| P41-A02 | P0-Core | `kt.ai_engineering.numeric_scoring.model_family_selection` | Logistic Regression 必须作为透明 baseline，用于暴露线性可解释边界和校准难度 | model_selection_rule | tabular_scorer | scikit-learn、calibration docs |
| P41-A03 | P0-Core | `kt.ai_engineering.numeric_scoring.model_family_selection` | LightGBM 与 XGBoost 可作为强 GBDT 候选，但必须使用相同时间切分和指标评估 | model_selection_rule | tabular_scorer | LightGBM、XGBoost papers/docs |
| P41-A04 | P0-Extended | `kt.ai_engineering.numeric_scoring.model_family_selection` | CatBoost 只在类别变量丰富或类别处理成本较高时作为条件候选 | conditional_model_rule | tabular_scorer | CatBoost docs/paper |
| P41-A05 | P0-Core | `kt.ai_engineering.numeric_scoring.model_family_selection` | 模型选择必须同时比较业务成本、延迟、可解释性、校准质量和治理复杂度 | governance_rule | tabular_scorer | NIST AI RMF、MLflow、scikit-learn |
| P41-A06 | P0-Extended | `kt.ai_engineering.numeric_scoring.model_family_selection` | 模型集成只能作为增强项，必须先证明单模型 baseline 不足且不破坏可审计性 | extension_rule | tabular_scorer | scikit-learn、ML governance sources |
| P41-A07 | P0-Extended | `kt.ai_engineering.numeric_scoring.scorer_explainability` | feature attribution / top_features 只能辅助调试和审计，不等于因果解释、交易规则证据或 final gate 决策依据 | explainability_boundary_rule | tabular_scorer | SHAP、causal inference sources |

### B. Tabular Scorer Training

| ID | 优先级 | canonical_node_id | 知识点 | claim_type | model_role | 主要来源 |
| --- | --- | --- | --- | --- | --- | --- |
| P41-B01 | P0-Core | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | bad_trade / false_allow 少数类必须声明 class weight、sample weight 或采样策略，并在加权或采样后重新检查校准质量 | training_policy_rule | tabular_scorer | scikit-learn、LightGBM、XGBoost |
| P41-B02 | P0-Core | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | HPO 只能读取 train/validation，不得读取 holdout、calibration、shadow、paper 或 incident pool | leakage_boundary_rule | tabular_scorer | scikit-learn pitfalls、Phase 41 contract |
| P41-B03 | P0-Core | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | 时间序列交易样本必须使用时间感知切分，不能随机打散导致未来信息泄漏 | leakage_boundary_rule | tabular_scorer | scikit-learn pitfalls、time-series CV |
| P41-B04 | P0-Extended | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | entity group split 必须避免同一策略/品种/周期族跨 split 泄漏 | leakage_boundary_rule | tabular_scorer | ML validation practice |
| P41-B05 | P0-Core | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | 训练样本必须记录 dataset_hash、split_manifest_hash、feature_schema_version 和 label_policy_version | lineage_rule | tabular_scorer | DVC、MLflow |
| P41-B06 | P1 | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | active learning 或 hard-example mining 只能作为复核采样增强，不能绕过 gold/eval 隔离 | extension_rule | tabular_scorer | active learning sources |

### C. Calibration And Threshold

| ID | 优先级 | canonical_node_id | 知识点 | claim_type | model_role | 主要来源 |
| --- | --- | --- | --- | --- | --- | --- |
| P41-C01 | P0-Core | `kt.ai_engineering.calibration_threshold.uncertainty` | raw score 不得直接作为交易概率或 final gate 输入，必须经过校准或声明只用于排序 | calibration_rule | calibrator | scikit-learn calibration |
| P41-C02 | P0-Core | `kt.ai_engineering.calibration_threshold.uncertainty` | 校准器必须使用独立 calibration set，不得使用 scorer 训练集直接拟合 | leakage_boundary_rule | calibrator | scikit-learn calibration |
| P41-C03 | P0-Core | `kt.ai_engineering.calibration_threshold.uncertainty` | threshold policy 必须绑定业务成本矩阵、false allow、false block 和 review capacity | threshold_policy_rule | final_gate | Phase 41 contract、NIST AI RMF |
| P41-C04 | P0-Extended | `kt.ai_engineering.calibration_threshold.uncertainty` | Platt 与 isotonic 的选择必须声明样本量、单调性假设和过拟合风险 | calibration_method_rule | calibrator | scikit-learn calibration |
| P41-C05 | P0-Extended | `kt.ai_engineering.calibration_threshold.uncertainty` | 校准应按 regime、strategy family、timeframe 切片检查，发现漂移时触发再校准审计；regime、strategy、timeframe 只能作为引用或 slice label，不在 AI Engineering 定义交易规则本体 | monitoring_rule | calibrator | calibration docs、Phase 40 drift |
| P41-C06 | P1 | `kt.ai_engineering.calibration_threshold.uncertainty` | conformal 或 abstain band 只能作为不确定性增强层，不能替代 deterministic final gate | extension_rule | calibrator | conformal prediction sources |

### D. Decision-Time Feature Store

| ID | 优先级 | canonical_node_id | 知识点 | claim_type | model_role | 主要来源 |
| --- | --- | --- | --- | --- | --- | --- |
| P41-D01 | P0-Core | `kt.ai_engineering.decision_time_feature_contract.feature_store` | 每个训练样本必须做 point-in-time feature join，feature_available_time 晚于 decision_time 必须阻断 | leakage_boundary_rule | tabular_scorer | Feast、scikit-learn pitfalls、Phase 41 contract |
| P41-D02 | P0-Core | `kt.ai_engineering.decision_time_feature_contract.feature_store` | 线上线下特征生成必须一致；不一致时必须记录差异并阻断默认指导 | serving_consistency_rule | tabular_scorer | Feast、TFDV/skew sources |
| P41-D03 | P0-Core | `kt.ai_engineering.decision_time_feature_contract.feature_store` | feature lineage 必须记录 source_object_ref、lineage_ref、schema_version 和缺失值策略 | lineage_rule | tabular_scorer | DVC、Feast |
| P41-D04 | P0-Core | `kt.ai_engineering.decision_time_feature_contract.feature_store` | label_observation_window 必须晚于 decision_time 且不能反向进入 scorer features；outcome 口径不得在 AI Engineering 定义交易收益本体 | label_boundary_rule | tabular_scorer | Phase 41 contract、scikit-learn pitfalls |
| P41-D05 | P1 | `kt.ai_engineering.decision_time_feature_contract.feature_store` | Feast 或正式 feature store 只在离线/在线一致性压力出现后引入，POC 阶段可用文件化 manifest | platform_boundary_rule | platform_governance | Feast docs、Phase 41 scope |

### E. Qwen3 Audit Assistant And Training Recipe

| ID | 优先级 | canonical_node_id | 知识点 | claim_type | model_role | 主要来源 |
| --- | --- | --- | --- | --- | --- | --- |
| P41-E01 | P0-Core | `kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant` | Qwen3 只能做审计助手，不做 numeric scorer、final gate 或事实来源 | runtime_boundary_rule | llm_audit_assistant | Qwen docs、Phase 41 runtime contract |
| P41-E02 | P0-Core | `kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant` | Qwen3 审计输出必须是 strict JSON，包含 recommendation、reason_codes、missing_fields、unsupported_claims 和 knowledge_refs | output_contract_rule | llm_audit_assistant | JSON Schema、Qwen docs、Phase 41 contract |
| P41-E03 | P0-Core | `kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant` | Qwen3 无 RAG 命中、无来源或引用冲突未消解时必须 abstain 或 needs_human_review | citation_rule | llm_audit_assistant | CEK-TA retrieval protocol、Phase 41 runtime |
| P41-E04 | P0-Extended | `kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant` | thinking mode 只用于复杂审计，低延迟结构化检查可使用 non-thinking mode；不得保存私有 chain-of-thought，最终只保存 strict JSON、reason code、citation 和 audit summary | usage_policy_rule | llm_audit_assistant | Qwen docs、Phase 41 runtime |
| P41-E05 | P0-Core | `kt.ai_engineering.llm_audit_assistant.qwen3_training_recipe` | Qwen3 SFT 只训练格式、reason code、引用习惯和审计流程，不训练交易概率 | training_boundary_rule | llm_audit_assistant | TRL SFT、Phase 41 data contract |
| P41-E06 | P0-Extended | `kt.ai_engineering.llm_audit_assistant.qwen3_training_recipe` | DPO/preference pair 只能优化审计质量，不得以 PnL 高低直接构造偏好 | preference_training_rule | llm_audit_assistant | TRL DPO、Phase 41 data contract |
| P41-E07 | P0-Extended | `kt.ai_engineering.llm_audit_assistant.qwen3_training_recipe` | RAG-first 和 prompt 修正必须先于 SFT/LoRA，只有格式或流程稳定性不足才训练权重 | method_selection_rule | llm_audit_assistant | TRL、CEK-TA protocol |
| P41-E08 | P1 | `kt.ai_engineering.llm_audit_assistant.qwen3_training_recipe` | vLLM 或本地 Qwen serving 只在延迟、吞吐或离线批量审计需求明确后引入 | serving_boundary_rule | platform_governance | vLLM docs、Qwen docs |
| P41-E09 | P0-Core | `kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant` | RAG context、用户交易摘要和检索文档必须视为不可信输入；Qwen3 输出进入审计链路前必须经过 prompt-injection guard、citation resolver、unsupported_claim detector 和 schema validation | untrusted_context_guard_rule | llm_audit_assistant | OWASP LLM01、CEK-TA retrieval protocol |

### F. Hybrid Runtime, Release And Platform Governance

| ID | 优先级 | canonical_node_id | 知识点 | claim_type | model_role | 主要来源 |
| --- | --- | --- | --- | --- | --- | --- |
| P41-F01 | P0-Core | `kt.ai_engineering.model_release_governance.hybrid_runtime_contract` | final gate 可以读取校准后的 scorer 风险信号、risk_bucket 和 threshold policy，但最终 allow/block/reduce_size 必须由 deterministic final gate 执行，不得直接服从 Qwen3 recommendation 或 raw model score | runtime_boundary_rule | final_gate | Phase 41 runtime contract、scikit-learn calibration |
| P41-F02 | P0-Core | `kt.ai_engineering.model_release_governance.hybrid_runtime_contract` | composite release manifest 必须绑定 scorer、calibrator、threshold、Qwen3 prompt、RAG index、reason taxonomy 和 rollback target | release_governance_rule | final_gate | MLflow、DVC、Phase 41 data contract |
| P41-F03 | P0-Extended | `kt.ai_engineering.model_release_governance.hybrid_runtime_contract` | 每次 hybrid scoring 必须记录 audit trace，串联输入、scorer、calibrator、RAG、Qwen3 和 final gate 输出 | observability_rule | final_gate | Phase 41 runtime contract |
| P41-F04 | P0-Extended | `kt.ai_engineering.model_release_governance.hybrid_runtime_contract` | champion/challenger 晋级必须经过 offline、shadow、paper/soft gate 和人工批准，不得自动替换 champion；paper/replay/fill/cost/execution 假设必须引用 Phase 37，不在 AI Engineering 定义 | promotion_gate_rule | final_gate | Phase 40、ML governance、Phase 37 refs |
| P41-F05 | P1 | `kt.ai_engineering.model_release_governance.training_platform_governance` | MLflow registry 只有在模型版本和 release manifest 复杂度上升时引入，POC 可先用文件化 registry | platform_boundary_rule | platform_governance | MLflow docs |
| P41-F06 | P1 | `kt.ai_engineering.model_release_governance.training_platform_governance` | Ray/Kubeflow 只在分布式训练或流水线编排需求明确后引入，不作为 Phase 41 默认依赖 | platform_boundary_rule | platform_governance | Ray、Kubeflow docs |
| P41-F07 | P1 | `kt.ai_engineering.model_release_governance.training_platform_governance` | 任何平台接入都必须保留 CEK-TA 知识检索只读、路径 resolver 和可移植配置边界 | integration_boundary_rule | platform_governance | CEK-TA AGENTS、Phase 22 resolver |
| P41-F08 | P0-Extended | `kt.ai_engineering.model_release_governance.hybrid_runtime_contract` | hybrid scoring runtime 必须定义 scorer、calibrator、RAG、Qwen3 和 final gate 的 latency budget、timeout、fallback、fail-to-review / fail-closed 策略 | runtime_fallback_rule | final_gate | SEC Knight、FCA algorithmic controls、SRE sources |

## 数量统计

| 优先级 | 数量 |
| --- | ---: |
| P0-Core | 22 |
| P0-Extended | 12 |
| P1 | 7 |
| 合计 | 41 |

## 覆盖检查

```text
Model Family Selection: 6 条
Tabular Scorer Training: 6 条
Calibration Uncertainty: 6 条
Decision-Time Feature Store: 5 条
Scorer Explainability: 1 条
Qwen3 Audit Assistant / Training Recipe: 9 条
Hybrid Runtime / Release / Platform Governance: 8 条
```
