# Phase 41 ResearchIngestionTask 队列

生成日期：2026-06-10
状态：queue draft
对应任务：CEK-TA-322

## 队列契约

每个任务必须按以下结构执行：

```text
task_id
knowledge_topic_id
target_canonical_node_id
priority
claim_type
model_role
query_plan
required_source_types
minimum_source_count
acceptance_gate
boundary_check
downstream
```

默认门槛：

```text
P0-Core: 至少 3 个来源，其中至少 1 个 official_doc 或 research_paper。
P0-Extended: 至少 2 个来源，其中至少 1 个 official_doc、standard_doc、governance_framework 或 research_paper。
P1: 至少 2 个来源，可以包含 engineering_article，但不能只有博客或厂商营销页。
内部契约可以作为边界来源，但不能替代外部专业来源。
```

## P0-Core 队列

| task_id | knowledge_topic_id | target_canonical_node_id | claim_type | model_role | query_plan | required_source_types | minimum_source_count | acceptance_gate | boundary_check | downstream |
| --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- | --- |
| P41-RT-001 | P41-A01 | `kt.ai_engineering.numeric_scoring.model_family_selection` | model_selection_rule | tabular_scorer | 搜索 rule baseline、Logistic Regression、LightGBM、XGBoost 默认比较，以及 CatBoost 条件候选边界 | official_doc, research_paper | 3 | 必须证明默认比较集和 CatBoost 条件引入边界 | 不得声称某模型稳定提高 PnL | candidate |
| P41-RT-002 | P41-A02 | `kt.ai_engineering.numeric_scoring.model_family_selection` | model_selection_rule | tabular_scorer | 搜索 Logistic Regression baseline、可解释性、概率校准和线性模型边界 | official_doc, research_paper | 3 | 必须说明透明 baseline 价值和限制 | 不得把 LR 当最终交易 gate | candidate |
| P41-RT-003 | P41-A03 | `kt.ai_engineering.numeric_scoring.model_family_selection` | model_selection_rule | tabular_scorer | 搜索 LightGBM/XGBoost GBDT 文档、论文、时间切分和同指标比较 | official_doc, research_paper | 3 | 必须覆盖两类 GBDT 候选和同评估协议 | 不得预设 GBDT 胜出 | candidate |
| P41-RT-004 | P41-B01 | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | training_policy_rule | tabular_scorer | 搜索 class imbalance、sample_weight、class_weight、cost-sensitive false allow | official_doc, research_paper | 3 | 必须输出少数类和成本权重策略 | 不得用过采样污染时间切分 | candidate |
| P41-RT-005 | P41-B02 | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | leakage_boundary_rule | tabular_scorer | 搜索 HPO leakage、train validation holdout 隔离、model selection bias | official_doc, research_paper | 3 | 必须明确 HPO 不能碰 holdout/calibration/shadow | 不得允许 test set 调参 | candidate |
| P41-RT-006 | P41-B03 | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | leakage_boundary_rule | tabular_scorer | 搜索 time series split、walk-forward、random split leakage | official_doc, research_paper | 3 | 必须说明时间序列样本不可随机打散 | 不采集 K 线规则本体 | candidate |
| P41-RT-007 | P41-C01 | `kt.ai_engineering.calibration_threshold.uncertainty` | calibration_rule | calibrator | 搜索 raw score vs calibrated probability、probability calibration | official_doc, research_paper | 3 | 必须阻断 raw score 直接当概率 | 不允许 raw score 直接 final gate | candidate |
| P41-RT-008 | P41-C02 | `kt.ai_engineering.calibration_threshold.uncertainty` | leakage_boundary_rule | calibrator | 搜索 independent calibration set、calibration leakage | official_doc, research_paper | 3 | 必须要求独立 calibration set | 不得用训练集直接拟合校准器 | candidate |
| P41-RT-009 | P41-C03 | `kt.ai_engineering.calibration_threshold.uncertainty` | threshold_policy_rule | final_gate | 搜索 cost-sensitive threshold、false positive/false negative cost、review capacity | official_doc, governance_framework, research_paper | 3 | 必须绑定成本矩阵和复核容量 | 不允许固定 0.5 默认阈值 | candidate |
| P41-RT-010 | P41-D01 | `kt.ai_engineering.decision_time_feature_contract.feature_store` | leakage_boundary_rule | tabular_scorer | 搜索 point-in-time feature join、feature availability、feature store leakage | official_doc, research_paper | 3 | 必须阻断 feature_available_time > decision_time | 不采集交易数据本体 | candidate |
| P41-RT-011 | P41-D02 | `kt.ai_engineering.decision_time_feature_contract.feature_store` | serving_consistency_rule | tabular_scorer | 搜索 offline-online feature parity、training-serving skew | official_doc, research_paper | 3 | 必须说明 parity test 和差异记录 | 不强制引入 Feast | candidate |
| P41-RT-012 | P41-E01 | `kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant` | runtime_boundary_rule | llm_audit_assistant | 搜索 Qwen/Qwen3 使用文档、LLM-as-judge/audit assistant 边界、AI governance | official_doc, governance_framework | 3 | 必须说明 Qwen3 只做审计助手 | 不得作为 scorer/final gate | candidate |
| P41-RT-013 | P41-E02 | `kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant` | output_contract_rule | llm_audit_assistant | 搜索 JSON Schema、structured output、LLM strict JSON 输出实践 | standard_doc, official_doc | 3 | 必须定义 strict JSON 必填字段 | 不接受自然语言报告替代 JSON | candidate |
| P41-RT-014 | P41-E03 | `kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant` | citation_rule | llm_audit_assistant | 搜索 RAG citation、no-hit abstain、unsupported answer、source grounding | official_doc, research_paper, internal_contract | 3 | 必须要求 no-hit abstain 或人工复核 | 无来源不得默认指导 | candidate |
| P41-RT-015 | P41-E05 | `kt.ai_engineering.llm_audit_assistant.qwen3_training_recipe` | training_boundary_rule | llm_audit_assistant | 搜索 SFT 用于格式/指令跟随、reason code、schema stability 的边界 | official_doc, research_paper | 3 | 必须说明 SFT 不训练交易概率 | 不用 PnL 训练买卖建议 | candidate |
| P41-RT-016 | P41-F01 | `kt.ai_engineering.model_release_governance.hybrid_runtime_contract` | runtime_boundary_rule | final_gate | 搜索 deterministic final gate、policy-as-code、risk control precedence、AI governance | governance_framework, internal_contract | 3 | 必须说明 final gate 唯一交易权限来源 | 不接受模型自然语言放行 | candidate |
| P41-RT-017 | P41-F02 | `kt.ai_engineering.model_release_governance.hybrid_runtime_contract` | release_governance_rule | final_gate | 搜索 release manifest、model registry、data versioning、rollback target、artifact hash | official_doc, governance_framework | 3 | 必须绑定 scorer/calibrator/Qwen/prompt/RAG/threshold/rollback | 不允许无 rollback 发布 | candidate |
| P41-RT-019 | P41-A05 | `kt.ai_engineering.numeric_scoring.model_family_selection` | governance_rule | tabular_scorer | 搜索模型选择多目标评估：业务成本、延迟、解释、校准、治理复杂度 | governance_framework, official_doc | 3 | 必须有非纯指标选择规则 | 不只看 accuracy/AUC | candidate |
| P41-RT-021 | P41-B05 | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | lineage_rule | tabular_scorer | 搜索 dataset hash、split manifest、data lineage、experiment reproducibility | official_doc, governance_framework | 3 | 必须要求 hash/version 进入 registry | 不引入数据库依赖 | candidate |
| P41-RT-024 | P41-D03 | `kt.ai_engineering.decision_time_feature_contract.feature_store` | lineage_rule | tabular_scorer | 搜索 feature lineage、schema version、missing policy | official_doc, standard_doc | 3 | 必须要求 source_object_ref、lineage_ref 和缺失策略 | 不定义项目私有字段 | candidate |
| P41-RT-025 | P41-D04 | `kt.ai_engineering.decision_time_feature_contract.feature_store` | label_boundary_rule | tabular_scorer | 搜索 label observation window、target leakage、post-outcome leakage | official_doc, research_paper | 3 | 必须阻断标签反向进入 features | 不把 PnL 单独当唯一标签，不定义交易收益本体 | candidate |
| P41-RT-040 | P41-E09 | `kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant` | untrusted_context_guard_rule | llm_audit_assistant | 搜索 OWASP LLM01、RAG prompt injection、不可信检索上下文、schema validation 和 unsupported claim 检查 | security_standard, official_doc | 3 | 必须要求 prompt-injection guard、citation resolver、unsupported_claim detector 和 schema validation | 不把 RAG context 或用户输入当可信事实 | candidate |

## P0-Extended 队列

| task_id | knowledge_topic_id | target_canonical_node_id | claim_type | model_role | query_plan | required_source_types | minimum_source_count | acceptance_gate | boundary_check | downstream |
| --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- | --- |
| P41-RT-018 | P41-A04 | `kt.ai_engineering.numeric_scoring.model_family_selection` | conditional_model_rule | tabular_scorer | 搜索 CatBoost 类别特征、ordered boosting、适用边界 | official_doc, research_paper | 2 | 必须说明类别变量丰富时条件引入 | 不设为默认必选 | candidate |
| P41-RT-020 | P41-B04 | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | leakage_boundary_rule | tabular_scorer | 搜索 group split、entity split、leakage through repeated entities | official_doc, research_paper | 2 | 必须说明策略/品种/周期族隔离 | 不强制某一唯一 split 方法 | candidate |
| P41-RT-022 | P41-C04 | `kt.ai_engineering.calibration_threshold.uncertainty` | calibration_method_rule | calibrator | 搜索 Platt scaling、isotonic regression、样本量和过拟合风险 | official_doc, research_paper | 2 | 必须说明选择边界 | 不预设某校准方法必胜 | candidate |
| P41-RT-023 | P41-C05 | `kt.ai_engineering.calibration_threshold.uncertainty` | monitoring_rule | calibrator | 搜索 calibration drift、regime-specific calibration、monitoring | official_doc, research_paper | 2 | 必须连接 Phase 40 漂移治理 | regime、strategy、timeframe 只能作为 ref 或 slice label，不定义 Trading 本体 | candidate |
| P41-RT-026 | P41-E04 | `kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant` | usage_policy_rule | llm_audit_assistant | 搜索 Qwen thinking/non-thinking、推理模式、低延迟结构化输出 | official_doc | 2 | 必须定义 thinking mode 使用边界 | 不保存思维链为审计事实 | candidate |
| P41-RT-027 | P41-E06 | `kt.ai_engineering.llm_audit_assistant.qwen3_training_recipe` | preference_training_rule | llm_audit_assistant | 搜索 DPO/preference training、审计输出质量偏好 | official_doc, research_paper | 2 | 必须说明 DPO 只优化审计质量 | 不以 PnL 直接构造偏好 | candidate |
| P41-RT-028 | P41-E07 | `kt.ai_engineering.llm_audit_assistant.qwen3_training_recipe` | method_selection_rule | llm_audit_assistant | 搜索 RAG-first、prompt baseline、SFT/LoRA 触发条件 | official_doc, internal_contract | 2 | 必须先 RAG/prompt 后训练权重 | 不用训练替代知识补充 | candidate |
| P41-RT-029 | P41-F03 | `kt.ai_engineering.model_release_governance.hybrid_runtime_contract` | observability_rule | final_gate | 搜索 audit trace、model observability、decision logging | governance_framework, official_doc | 2 | 必须串联全链路 refs | 不记录密钥或账户私密字段 | candidate |
| P41-RT-030 | P41-F04 | `kt.ai_engineering.model_release_governance.hybrid_runtime_contract` | promotion_gate_rule | final_gate | 搜索 champion/challenger、shadow、canary、approval workflow、paper/replay 证据边界 | official_doc, governance_framework | 2 | 必须要求人工批准和 staged rollout | 不自动替换 champion；paper/replay/fill/cost 必须引用 Phase 37 | candidate |
| P41-RT-031 | P41-A06 | `kt.ai_engineering.numeric_scoring.model_family_selection` | extension_rule | tabular_scorer | 搜索 model ensemble governance、stacking 风险、可审计性 | official_doc, research_paper | 2 | 必须定义增强层和回滚边界 | 不作为 P0 默认方案 | candidate |
| P41-RT-039 | P41-A07 | `kt.ai_engineering.numeric_scoring.scorer_explainability` | explainability_boundary_rule | tabular_scorer | 搜索 SHAP、feature attribution、causal inference warning、top_features 审计边界 | research_paper, official_doc | 2 | 必须说明 attribution/top_features 只能调试和审计 | 不作为因果解释、交易规则证据或 final gate 决策依据 | candidate |
| P41-RT-041 | P41-F08 | `kt.ai_engineering.model_release_governance.hybrid_runtime_contract` | runtime_fallback_rule | final_gate | 搜索 latency budget、timeout、fallback、fail-closed、fail-to-review、算法交易事故控制 | regulator_release, regulator_review, engineering_article | 2 | 必须定义 scorer/calibrator/RAG/Qwen3/final gate 超时和降级 | 不允许故障时默认放行 | candidate |

## P1 队列

| task_id | knowledge_topic_id | target_canonical_node_id | claim_type | model_role | query_plan | required_source_types | minimum_source_count | acceptance_gate | boundary_check | downstream |
| --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- | --- |
| P41-RT-032 | P41-B06 | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | extension_rule | tabular_scorer | 搜索 active learning、hard-example mining、review sampling governance | research_paper, engineering_article | 2 | 必须只作为复核采样增强 | 不污染 gold/eval | candidate |
| P41-RT-033 | P41-C06 | `kt.ai_engineering.calibration_threshold.uncertainty` | extension_rule | calibrator | 搜索 conformal prediction、abstain band、不确定性分层 | research_paper, official_doc | 2 | 必须说明只能增强不确定性处理 | 不替代 final gate | candidate |
| P41-RT-034 | P41-D05 | `kt.ai_engineering.decision_time_feature_contract.feature_store` | platform_boundary_rule | platform_governance | 搜索 Feast feature store 引入条件、offline/online parity | official_doc | 2 | 必须给出 POC 文件化优先边界 | 不强制平台依赖 | candidate |
| P41-RT-035 | P41-E08 | `kt.ai_engineering.llm_audit_assistant.qwen3_training_recipe` | serving_boundary_rule | platform_governance | 搜索 vLLM、Qwen serving、吞吐和延迟边界 | official_doc | 2 | 必须定义引入条件和 fallback | 不部署真实服务 | candidate |
| P41-RT-036 | P41-F05 | `kt.ai_engineering.model_release_governance.training_platform_governance` | platform_boundary_rule | platform_governance | 搜索 MLflow registry、model version、artifact lineage | official_doc | 2 | 必须说明文件化 registry 到 MLflow 的升级条件 | 不引入运行时依赖 | candidate |
| P41-RT-037 | P41-F06 | `kt.ai_engineering.model_release_governance.training_platform_governance` | platform_boundary_rule | platform_governance | 搜索 Ray/Kubeflow 引入条件、分布式训练和 pipeline 编排治理 | official_doc | 2 | 必须说明非默认依赖 | 不改变 Phase 41 POC 边界 | candidate |
| P41-RT-038 | P41-F07 | `kt.ai_engineering.model_release_governance.training_platform_governance` | integration_boundary_rule | platform_governance | 搜索工具集成权限、路径 resolver、可移植配置、只读知识检索 | internal_contract, official_doc | 2 | 必须保留 CEK-TA resolver 和 MCP 只读边界 | 不硬编码本机路径 | candidate |

## 执行顺序

```text
1. 先执行 P0-Core：P41-RT-001 至 P41-RT-017，加 P41-RT-019、P41-RT-021、P41-RT-024、P41-RT-025、P41-RT-040。
2. P0-Core 全部形成候选后，导出范围审计 JSON 做边界审计。
3. P0-Extended：P41-RT-018、P41-RT-020、P41-RT-022、P41-RT-023、P41-RT-026 至 P41-RT-031、P41-RT-039、P41-RT-041 作为第二批。
4. P1 的 P41-RT-032 至 P41-RT-038 作为增强批。
5. 任一任务发现主要内容属于 Trading Engineering 本体，必须转入 Phase 37，不得强塞到 Phase 41。
```

## DoD

```text
1. 队列覆盖 41 条知识点。
2. 每条任务都有 canonical node、priority、claim_type、model_role、query_plan、source gate 和 boundary_check。
3. P0-Core 来源门槛不低于 3 个来源。
4. P0-Extended/P1 来源门槛不低于 2 个来源。
5. 明确 Qwen3、tabular scorer 和 final gate 的权限边界。
6. 明确不采集 Trading Engineering 本体。
```
