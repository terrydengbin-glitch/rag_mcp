# Phase 38 AI 模型平台知识采集矩阵

生成日期：2026-06-10
状态：collection matrix draft
对应任务：CEK-TA-269

## 采集原则

```text
1. 每条知识必须有来源、适用边界、不适用场景和冲突审计。
2. Phase 38 只采集 AI Engineering 方法，不采集交易规则本体。
3. 交易规则只通过 related_trading_refs 引用 Phase 37。
4. reviewed 不等于 approved；本轮统一进入候选审计。
5. P0-Core 是 POC 前硬门；P0-Extended 是正式发布前硬门；P1 是增强项。
```

## 来源种子

| 来源 | URL | 类型 | 覆盖方向 |
| --- | --- | --- | --- |
| scikit-learn Probability Calibration | https://scikit-learn.org/stable/modules/calibration.html | official_doc | 概率校准、校准曲线 |
| scikit-learn Brier Score | https://scikit-learn.org/stable/modules/generated/sklearn.metrics.brier_score_loss.html | official_doc | Brier score |
| LightGBM Documentation | https://lightgbm.readthedocs.io/ | official_doc | GBDT scorer |
| XGBoost Documentation | https://xgboost.readthedocs.io/ | official_doc | GBDT scorer |
| CatBoost Documentation | https://catboost.ai/ | official_doc | 类别特征 GBDT |
| CatBoost paper | https://arxiv.org/abs/1810.11363 | research_paper | 类别特征、GBDT |
| Hugging Face TRL | https://huggingface.co/docs/trl/en/index | official_doc | SFT/DPO/偏好训练 |
| TRL SFT Trainer | https://huggingface.co/docs/trl/en/sft_trainer | official_doc | SFT |
| TRL DPO Trainer | https://huggingface.co/docs/trl/en/dpo_trainer | official_doc | DPO |
| MLflow Model Registry | https://mlflow.org/docs/latest/ml/model-registry/ | official_doc | model registry、alias、版本 |
| DVC Get Started | https://doc.dvc.org/start | official_doc | 数据版本 |
| DVC Pipelines | https://doc.dvc.org/start/data-pipelines/data-pipelines | official_doc | pipeline 复现 |
| TensorFlow Data Validation | https://www.tensorflow.org/tfx/data_validation/get_started | official_doc | schema、skew、drift |
| TFDV Guide | https://github.com/tensorflow/tfx/blob/master/docs/guide/tfdv.md | official_doc | training-serving skew、drift |
| NIST AI RMF | https://www.nist.gov/itl/ai-risk-management-framework | governance_framework | AI 风险治理 |
| Hudson & Thames Meta-Labeling | https://hudsonthames.org/meta-labeling-a-toy-example/ | engineering_article | 交易候选二层过滤 |
| XGBoost paper | https://arxiv.org/abs/1603.02754 | research_paper | 可扩展 tree boosting |

## 采集矩阵

### A. Numeric Scoring / Meta-Labeling

| ID | 优先级 | canonical_node_id | 知识点 | claim_type | 主要来源 |
| --- | --- | --- | --- | --- | --- |
| P38-A01 | P0-Core | `kt.ai_engineering.numeric_scoring` | scorer / soft gate / final gate 必须分权 | governance_rule | Phase 36 契约、NIST AI RMF |
| P38-A02 | P0-Core | `kt.ai_engineering.numeric_scoring` | deterministic rule baseline 必须先建立 | methodology_constraint | scikit-learn、Phase 36 |
| P38-A03 | P0-Core | `kt.ai_engineering.numeric_scoring` | Logistic Regression 作为透明 baseline | model_selection_rule | scikit-learn |
| P38-A04 | P0-Core | `kt.ai_engineering.numeric_scoring` | LightGBM 只能作为候选 scorer，不预设胜出 | model_selection_rule | LightGBM docs |
| P38-A05 | P0-Core | `kt.ai_engineering.numeric_scoring` | XGBoost 应作为 strong baseline 同场比较 | model_selection_rule | XGBoost docs |
| P38-A06 | P0-Core | `kt.ai_engineering.numeric_scoring` | meta-labeling 只能过滤候选，不能生成新交易机会 | risk_boundary_rule | Hudson & Thames、meta-labeling literature |
| P38-A07 | P0-Core | `kt.ai_engineering.numeric_scoring` | numeric scorer 输出必须是风险排序或质量评分，不是最终交易动作 | runtime_boundary_rule | Phase 38 runtime contract |
| P38-A08 | P0-Extended | `kt.ai_engineering.numeric_scoring` | CatBoost 仅在类别特征占比高时条件引入 | model_selection_rule | CatBoost docs |
| P38-A09 | P0-Extended | `kt.ai_engineering.numeric_scoring` | feature attribution 只能辅助调试，不等于因果解释 | caveat_rule | model explainability sources |
| P38-A10 | P1 | `kt.ai_engineering.numeric_scoring` | ranking model 可作为 review_priority 增强项 | extension_rule | ML ranking sources |

### B. Calibration & Threshold Policy

| ID | 优先级 | canonical_node_id | 知识点 | claim_type | 主要来源 |
| --- | --- | --- | --- | --- | --- |
| P38-B01 | P0-Core | `kt.ai_engineering.calibration_threshold` | scorer 概率必须经过独立校准检查 | calibration_rule | scikit-learn calibration |
| P38-B02 | P0-Core | `kt.ai_engineering.calibration_threshold` | calibrator 不得使用 scorer 训练集拟合 | leakage_boundary_rule | scikit-learn calibration |
| P38-B03 | P0-Core | `kt.ai_engineering.calibration_threshold` | Brier score 必须作为概率质量指标之一 | eval_rule | scikit-learn Brier |
| P38-B04 | P0-Core | `kt.ai_engineering.calibration_threshold` | reliability diagram / calibration curve 必须输出 | eval_rule | scikit-learn calibration |
| P38-B05 | P0-Core | `kt.ai_engineering.calibration_threshold` | threshold 不得固定 0.5，必须绑定成本策略 | governance_rule | cost-sensitive learning |
| P38-B06 | P0-Core | `kt.ai_engineering.calibration_threshold` | false allow / false block 必须进入 cost matrix | governance_rule | Phase 36 |
| P38-B07 | P0-Core | `kt.ai_engineering.calibration_threshold` | threshold_policy_version 必须进入 final gate trace | lineage_rule | MLflow / release manifest |
| P38-B08 | P0-Extended | `kt.ai_engineering.calibration_threshold` | 校准必须按 strategy/regime/horizon 切片检查 | eval_rule | model monitoring sources |
| P38-B09 | P0-Extended | `kt.ai_engineering.calibration_threshold` | calibration drift 必须进入 shadow 监控 | monitoring_rule | TFDV / drift docs |
| P38-B10 | P1 | `kt.ai_engineering.calibration_threshold` | conformal / Bayesian calibration 只能作为增强层 | extension_rule | conformal sources |

### C. Decision-Time Feature & Leakage Gate

| ID | 优先级 | canonical_node_id | 知识点 | claim_type | 主要来源 |
| --- | --- | --- | --- | --- | --- |
| P38-C01 | P0-Core | `kt.ai_engineering.decision_time_feature_contract` | 每个样本必须有 decision_time | schema_rule | Phase 38 data contract |
| P38-C02 | P0-Core | `kt.ai_engineering.decision_time_feature_contract` | 每个特征必须有 feature_available_time | schema_rule | TFDV / feature store practice |
| P38-C03 | P0-Core | `kt.ai_engineering.decision_time_feature_contract` | feature_available_time 晚于 decision_time 必须阻断 | leakage_boundary_rule | Phase 38 data contract |
| P38-C04 | P0-Core | `kt.ai_engineering.decision_time_feature_contract` | post-trade outcome 不得进入 scorer 输入 | leakage_boundary_rule | scikit-learn pitfalls / data leakage |
| P38-C05 | P0-Core | `kt.ai_engineering.decision_time_feature_contract` | label_observation_end_time 必须晚于真实可观察结果 | schema_rule | Phase 38 data contract |
| P38-C06 | P0-Core | `kt.ai_engineering.decision_time_feature_contract` | feature lineage 必须记录 source_object | lineage_rule | DVC / TFDV |
| P38-C07 | P0-Core | `kt.ai_engineering.decision_time_feature_contract` | training-serving parity test 必须存在 | serving_consistency_rule | TFDV guide |
| P38-C08 | P0-Extended | `kt.ai_engineering.decision_time_feature_contract` | feature schema registry 必须版本化 | governance_rule | TFDV / DVC |
| P38-C09 | P0-Extended | `kt.ai_engineering.decision_time_feature_contract` | data quality expectation suite 应覆盖核心字段 | data_quality_rule | TFDV / Great Expectations |
| P38-C10 | P1 | `kt.ai_engineering.decision_time_feature_contract` | 多市场迁移时必须重新检查特征可用性 | transfer_caveat | model transfer sources |

### D. LLM Audit Assistant

| ID | 优先级 | canonical_node_id | 知识点 | claim_type | 主要来源 |
| --- | --- | --- | --- | --- | --- |
| P38-D01 | P0-Core | `kt.ai_engineering.llm_audit_assistant` | LLM audit assistant 必须输出 strict JSON schema | output_contract_rule | OpenAI Structured Outputs、JSON Schema |
| P38-D02 | P0-Core | `kt.ai_engineering.llm_audit_assistant` | LLM recommendation 不能等于 final gate decision | runtime_boundary_rule | Phase 38 runtime contract |
| P38-D03 | P0-Core | `kt.ai_engineering.llm_audit_assistant` | knowledge_refs 必须能解析到 formal index | citation_rule | CEK-TA MCP |
| P38-D04 | P0-Core | `kt.ai_engineering.llm_audit_assistant` | 无来源或 no-hit 必须 abstain / neutral | safety_rule | CEK-TA retrieval protocol |
| P38-D05 | P0-Core | `kt.ai_engineering.llm_audit_assistant` | unsupported_claims 不为空时不得默认放行 | safety_rule | structured output governance |
| P38-D06 | P0-Core | `kt.ai_engineering.llm_audit_assistant` | reason_codes 必须来自受控 taxonomy | output_contract_rule | Phase 36 |
| P38-D07 | P0-Extended | `kt.ai_engineering.llm_audit_assistant` | RAG + prompt baseline 必须先于 SFT | method_selection_rule | TRL / Phase 36 |
| P38-D08 | P0-Extended | `kt.ai_engineering.llm_audit_assistant` | SFT LoRA 仅用于稳定输出 schema 和 reason code | training_boundary_rule | TRL SFT |
| P38-D09 | P0-Extended | `kt.ai_engineering.llm_audit_assistant` | DPO 只优化审计偏好，不优化交易收益承诺 | preference_training_rule | TRL DPO |
| P38-D10 | P1 | `kt.ai_engineering.llm_audit_assistant` | teacher model 只能作为审计 baseline，不作为事实来源 | governance_rule | AI governance sources |

### E. Shadow / Paper / OPE Evaluation

| ID | 优先级 | canonical_node_id | 知识点 | claim_type | 主要来源 |
| --- | --- | --- | --- | --- | --- |
| P38-E01 | P0-Core | `kt.ai_engineering.shadow_paper_ope_eval` | offline eval 只能评估已执行交易样本 | eval_boundary_rule | Phase 36 |
| P38-E02 | P0-Core | `kt.ai_engineering.shadow_paper_ope_eval` | blocked trade 不能直接标注为亏损 | counterfactual_rule | OPE literature |
| P38-E03 | P0-Core | `kt.ai_engineering.shadow_paper_ope_eval` | hard gate 前必须 shadow mode | release_gate_rule | LLMOps practice |
| P38-E04 | P0-Core | `kt.ai_engineering.shadow_paper_ope_eval` | paper/replay 评估必须声明 fill/cost 假设来自 Trading Engineering | cross_branch_rule | Phase 37 |
| P38-E05 | P0-Core | `kt.ai_engineering.shadow_paper_ope_eval` | OPE 必须声明 behavior policy 和目标策略假设 | eval_boundary_rule | OPE papers |
| P38-E06 | P0-Core | `kt.ai_engineering.shadow_paper_ope_eval` | human_review_precision 必须作为 POC 指标 | eval_rule | Phase 36 |
| P38-E07 | P0-Extended | `kt.ai_engineering.shadow_paper_ope_eval` | RAG/prompt/model/threshold 必须可 ablation | eval_rule | ML eval practice |
| P38-E08 | P0-Extended | `kt.ai_engineering.shadow_paper_ope_eval` | shadow 日志必须记录 no-hit/conflict/citation completeness | observability_rule | CEK-TA protocol |
| P38-E09 | P0-Extended | `kt.ai_engineering.shadow_paper_ope_eval` | false block opportunity 必须用 paper/replay 或人工复核估计 | counterfactual_rule | OPE / replay |
| P38-E10 | P1 | `kt.ai_engineering.shadow_paper_ope_eval` | active learning review sampling 只能作为增强 | extension_rule | active learning sources |

### F. Model Release / Lineage / Rollback

| ID | 优先级 | canonical_node_id | 知识点 | claim_type | 主要来源 |
| --- | --- | --- | --- | --- | --- |
| P38-F01 | P0-Core | `kt.ai_engineering.model_release_governance` | release_manifest 必须绑定数据、模型、prompt、RAG 和阈值版本 | lineage_rule | MLflow / DVC |
| P38-F02 | P0-Core | `kt.ai_engineering.model_release_governance` | model registry 必须记录 model_version 和别名/发布状态 | governance_rule | MLflow registry |
| P38-F03 | P0-Core | `kt.ai_engineering.model_release_governance` | dataset_hash 和 split_manifest_hash 必须进入发布记录 | lineage_rule | DVC |
| P38-F04 | P0-Core | `kt.ai_engineering.model_release_governance` | rollback_target 必须在上线前定义 | release_gate_rule | LLMOps practice |
| P38-F05 | P0-Core | `kt.ai_engineering.model_release_governance` | hard gate 开启必须有 owner approval | governance_rule | NIST AI RMF |
| P38-F06 | P0-Core | `kt.ai_engineering.model_release_governance` | kill switch policy 必须纳入 release_manifest | safety_rule | Phase 36 |
| P38-F07 | P0-Extended | `kt.ai_engineering.model_release_governance` | incident freeze 必须冻结模型、prompt、RAG index 和 threshold | incident_rule | AI governance |
| P38-F08 | P0-Extended | `kt.ai_engineering.model_release_governance` | model card / dataset card 必须描述 intended use 和 out-of-scope use | governance_rule | model card / dataset card sources |
| P38-F09 | P0-Extended | `kt.ai_engineering.model_release_governance` | latency budget 和 fallback 必须纳入发布验收 | release_gate_rule | service reliability |
| P38-F10 | P1 | `kt.ai_engineering.model_release_governance` | model compression 只能在不破坏审计和校准后考虑 | extension_rule | deployment sources |

### G. Trading AI RAG Pack & Citation Governance

| ID | 优先级 | canonical_node_id | 知识点 | claim_type | 主要来源 |
| --- | --- | --- | --- | --- | --- |
| P38-G01 | P0-Core | `kt.rag_engineering.trading_scoring_rag_pack` | scoring/gating 任务必须主动检索 CEK-TA | retrieval_policy_rule | Phase 35 |
| P38-G02 | P0-Core | `kt.rag_engineering.trading_scoring_rag_pack` | RAG context 默认是不可信输入 | security_rule | NIST AI RMF / prompt injection guidance |
| P38-G03 | P0-Core | `kt.rag_engineering.trading_scoring_rag_pack` | machine_gate 和 review_status 必须过滤默认指导 | governance_rule | Phase 34/35 |
| P38-G04 | P0-Core | `kt.rag_engineering.trading_scoring_rag_pack` | 知识包必须裁剪字段，控制上下文预算 | retrieval_quality_rule | RAG engineering practice |
| P38-G05 | P0-Extended | `kt.rag_engineering.trading_scoring_rag_pack` | citation completeness 必须进入 shadow 指标 | eval_rule | CEK-TA protocol |
| P38-G06 | P1 | `kt.rag_engineering.trading_scoring_rag_pack` | no-hit query 应进入知识缺口队列 | governance_rule | CEK-TA knowledge governance |

## 统计

```text
Numeric Scoring: 10
Calibration Threshold: 10
Decision-Time Feature: 10
LLM Audit Assistant: 10
Shadow / Paper / OPE: 10
Model Release Governance: 10
Trading AI RAG Pack: 6
合计: 66

P0-Core: 43
P0-Extended: 16
P1: 7
```

说明：任务卡原建议为 P0-Core 36、P0-Extended 18、P1 12。实际拆分时，将部分“RAG 安全、发布治理、final gate 权限”等内容上调为 P0-Core，因此 P0-Core 为 43。该调整不改变总量 66，但让 POC 前硬门更严格。
