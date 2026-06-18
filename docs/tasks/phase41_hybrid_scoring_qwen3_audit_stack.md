# Phase 41: Hybrid Scoring 与 Qwen3 审计助手知识扩展

## Phase 目标

沿着 Phase 36、Phase 38 和 Phase 40 已确认的主线，补齐外接交易 LLM gating/scoring 项目真正落地所需的组合式 AI Engineering 知识：

```text
表格/统计模型负责数值 scoring、风险排序、review priority。
Qwen3/LLM 负责审计解释、reason code、RAG 引用、缺字段检查和人工复核摘要。
deterministic final gate 负责最终交易放行、阻断、仓位、安全停机和实盘权限。
```

本 Phase 的核心不是重新讨论“用不用 Qwen3”，而是把“LightGBM / XGBoost / Logistic Regression / CatBoost + Qwen3 Audit Assistant + deterministic final gate”拆成可采集、可审计、可检索、可被外部 AI IDE 主动调用的专业知识卡。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-318 | P0 | done | 创建 Phase 41 任务卡并登记任务索引 | `docs/tasks/phase41_hybrid_scoring_qwen3_audit_stack.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-317 |
| CEK-TA-319 | P0 | done | 定义 Hybrid Scoring Stack 知识范围、L3 专题和跨分支边界 | `docs/research/phase41_hybrid_scoring_qwen3_scope.md`、`codex-expert-kit/rag/knowledge_tree.md` | CEK-TA-318 |
| CEK-TA-320 | P0 | done | 定义表格模型、Qwen3 审计助手、final gate 的组合运行时契约 | `docs/contracts/phase41_hybrid_scoring_runtime_contract.md` | CEK-TA-319 |
| CEK-TA-321 | P0 | done | 定义训练数据、point-in-time feature、标签、校准、阈值和模型 registry 契约 | `docs/contracts/phase41_tabular_llm_training_data_contract.md` | CEK-TA-320 |
| CEK-TA-322 | P0 | done | 创建并按范围审计补丁修正 41 条 Phase 41 知识点采集矩阵和 ResearchIngestionTask 队列 | `docs/research/phase41_hybrid_scoring_collection_matrix.md`、`docs/research/phase41_research_task_queue.md` | CEK-TA-321 |
| CEK-TA-323 | P0 | done | 导出 Phase 41 知识范围审计 JSON，导入范围审计结果并回写补丁 | `docs/audit/phase41_hybrid_scoring_qwen3_scope_for_audit.json`、`docs/audit/audit_result_phase41_hybrid_scoring_qwen3_scope_20260610_strict_v1.json`、`docs/reports/phase41_scope_audit_patch_import_report.json` | CEK-TA-322 |
| CEK-TA-324 | P1 | done | 联网采集 P0-Core 来源，生成候选知识包 | `codex-expert-kit/rag/scripts/generate_phase41_p0_core_candidates.py`、`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase41_*.json`、`docs/research/phase41_p0_core_candidate_research.md`、`docs/reports/phase41_candidate_generation_report.md`、`docs/reports/phase41_candidate_quality_gate.json` | CEK-TA-323 |
| CEK-TA-325 | P1 | done | 导出 Phase 41 候选 AI 审计包并运行来源、冲突、乱码和污染门禁 | `codex-expert-kit/rag/scripts/export_phase41_candidate_audit_package.py`、`docs/audit/phase41_candidate_audit_package_20260610.json`、`docs/reports/phase41_candidate_quality_gate.json` | CEK-TA-324 |
| CEK-TA-326 | P1 | done | 按审计结果补证、回写、沉淀 formal reviewed，并重建索引和 Vue3 fixture；Phase 41 P0-Core 22 条已全部转 formal reviewed/caveat_only，P41-B05 与 P41-D03 二审通过并已入库；approved/default guidance/hard gate 均为 0 | `codex-expert-kit/rag/scripts/apply_phase41_candidate_audit_result.py`、`codex-expert-kit/rag/scripts/apply_phase41_candidate_supplemental_reaudit_result.py`、`codex-expert-kit/rag/scripts/prepare_phase41_a05_r1_third_audit_package.py`、`codex-expert-kit/rag/scripts/apply_phase41_a05_r1_third_audit_result.py`、`codex-expert-kit/rag/scripts/export_phase41_ai_passed_reviewed_preparation_package.py`、`codex-expert-kit/rag/scripts/apply_phase41_reviewed_preparation_result.py`、`codex-expert-kit/rag/scripts/supplement_phase41_reviewed_preparation_needs_evidence.py`、`codex-expert-kit/rag/scripts/apply_phase41_reviewed_preparation_supplemental_reaudit_result.py`、`docs/contracts/phase41_tabular_llm_training_data_contract.md`、`docs/audit/audit_result_phase41_candidate_audit_package_20260610_strict_v1.json`、`docs/audit/audit_result_phase41_candidate_supplemental_reaudit_20260610_strict_v2.json`、`docs/audit/phase41_a05_r1_third_audit_package_20260610.json`、`docs/audit/audit_result_phase41_a05_r1_third_audit_20260610_strict_v3.json`、`docs/audit/phase41_ai_passed_reviewed_preparation_audit_package_20260610.json`、`docs/audit/audit_result_phase41_ai_passed_reviewed_preparation_20260610_strict_v1.json`、`docs/audit/phase41_reviewed_preparation_supplemental_reaudit_package_20260610.json`、`docs/audit/audit_result_phase41_reviewed_preparation_supplemental_reaudit_20260610_strict_v1.json`、`docs/reports/phase41_candidate_audit_import_report.json`、`docs/reports/phase41_candidate_supplemental_reaudit_import_report.json`、`docs/reports/phase41_candidate_remaining_evidence_followups.json`、`docs/reports/phase41_a05_r1_third_audit_preparation_report.md`、`docs/reports/phase41_a05_r1_third_audit_import_report.json`、`docs/reports/phase41_ai_passed_reviewed_preparation_gap_report.json`、`docs/reports/phase41_reviewed_preparation_import_report.json`、`docs/reports/phase41_reviewed_preparation_supplemental_evidence_report.json`、`docs/reports/phase41_reviewed_preparation_supplemental_evidence_report.md`、`docs/reports/phase41_reviewed_preparation_supplemental_reaudit_import_report.json`、`docs/reports/phase41_reviewed_preparation_remaining_followups.json`、`codex-expert-kit/rag/knowledge/KB_AI_20_NUMERIC_SCORING/`、`codex-expert-kit/rag/knowledge/KB_AI_21_CALIBRATION_THRESHOLD/`、`codex-expert-kit/rag/knowledge/KB_AI_22_DECISION_TIME_FEATURES/`、`codex-expert-kit/rag/knowledge/KB_AI_23_LLM_AUDIT_ASSISTANT/`、`codex-expert-kit/rag/knowledge/KB_AI_25_MODEL_RELEASE_GOVERNANCE/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/phase23Candidates.ts`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/knowledgeTreeNodes.ts`、`ui/src/types.ts` | CEK-TA-325 |
| CEK-TA-327 | P1 | done | 验证 MCP/SearchLab/KnowledgeTree 能按 Phase 41 子板块检索、引用、阻断和降级；确认 22 条 Phase 41 formal reviewed 知识可检索、可引用，默认指导检索被 caveat_only 阻断，MCP 写权限被拒绝 | `codex-expert-kit/rag/scripts/validate_phase41_runtime_linkage.py`、`docs/reports/phase41_runtime_linkage_validation_report.json` | CEK-TA-326 |
| CEK-TA-329 | P1 | done | 重新核对 Phase 41 优先级覆盖，确认 P0-Core 22 条已完成，P0-Extended 12 条和 P1 7 条尚未采集，并修正 Phase 41 状态为 doing | `docs/reports/phase41_remaining_scope_alignment_report.json`、`docs/index_tasks.md`、`docs/tasks/README.md`、`docs/tasks/phase41_hybrid_scoring_qwen3_audit_stack.md` | CEK-TA-327 |
| CEK-TA-330 | P1 | done | 联网采集 Phase 41 P0-Extended/P1 剩余 19 条来源并生成候选知识包；本批 P0-Extended 12 条和 P1 7 条统一采集 | `codex-expert-kit/rag/scripts/generate_phase41_extended_p1_candidates.py`、`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/`、`docs/research/phase41_extended_p1_candidate_research.md`、`docs/reports/phase41_extended_p1_candidate_generation_report.md` | CEK-TA-329 |
| CEK-TA-331 | P1 | done | 导出 Phase 41 P0-Extended/P1 候选 AI 审计包并运行来源、冲突、乱码和污染门禁；联合审计包包含 19 条候选，质量门禁 pass | `codex-expert-kit/rag/scripts/export_phase41_extended_p1_audit_package.py`、`docs/audit/phase41_extended_p1_candidate_audit_package_20260610.json`、`docs/reports/phase41_extended_p1_candidate_quality_gate.json` | CEK-TA-330 |
| CEK-TA-332 | P1 | done | 导入 Phase 41 P0-Extended/P1 审计结果，按 Phase 32 工作流分流 accepted、needs_more_evidence、rejected 并完成 6 条补证与二审包导出；本轮不创建 reviewed/approved/default/hard gate | `codex-expert-kit/rag/scripts/apply_phase41_extended_p1_audit_result.py`、`codex-expert-kit/rag/scripts/supplement_phase41_extended_p1_needs_evidence.py`、`docs/audit/audit_result_phase41_extended_p1_candidate_audit_package_20260610_strict_v1.json`、`docs/reports/phase41_extended_p1_audit_import_report.json`、`docs/research/phase41_extended_p1_supplemental_research.md`、`docs/reports/phase41_extended_p1_supplemental_evidence_report.json`、`docs/audit/phase41_extended_p1_supplemental_reaudit_package_20260610.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-331 |
| CEK-TA-333 | P1 | done | 将二审允许的 6 条 Phase 41 P0-Extended/P1 候选沉淀为 formal reviewed/caveat_only，并重建索引、Vue3 fixture 和运行时联动验证；approved/default/hard gate 均保持 0 | `codex-expert-kit/rag/scripts/apply_phase41_extended_p1_supplemental_reaudit_result.py`、`docs/audit/audit_result_phase41_extended_p1_supplemental_reaudit_20260610_strict_v2.json`、`docs/reports/phase41_extended_p1_supplemental_reaudit_import_report.json`、`codex-expert-kit/rag/knowledge/KB_AI_20_NUMERIC_SCORING/`、`codex-expert-kit/rag/knowledge/KB_AI_23_LLM_AUDIT_ASSISTANT/`、`codex-expert-kit/rag/knowledge/KB_AI_25_MODEL_RELEASE_GOVERNANCE/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/`、`docs/reports/phase41_runtime_linkage_validation_report.json` | CEK-TA-332 |
| CEK-TA-335 | P1 | done | 导出 Phase 41 P0-Extended/P1 剩余 13 条 ai_passed 候选 reviewed-preparation 再审计包；本轮只请求 reviewed 许可，不创建 formal reviewed/approved/default/hard gate | `codex-expert-kit/rag/scripts/export_phase41_extended_p1_remaining_reviewed_preparation_package.py`、`docs/audit/phase41_extended_p1_remaining_reviewed_preparation_audit_package_20260610.json`、`docs/reports/phase41_extended_p1_remaining_reviewed_preparation_gap_report.json` | CEK-TA-333 |
| CEK-TA-336 | P1 | done | 导入 Phase 41 剩余 13 条 reviewed-preparation 再审计结果；12 条沉淀为 formal reviewed/caveat_only，P41-A06 修正 slug/formal_knowledge_id 后继续 needs_more_evidence；approved/default/hard gate 均保持 0 | `codex-expert-kit/rag/scripts/apply_phase41_extended_p1_remaining_reviewed_preparation_result.py`、`docs/audit/audit_result_phase41_extended_p1_remaining_reviewed_preparation_20260610_strict_v1.json`、`docs/reports/phase41_extended_p1_remaining_reviewed_preparation_import_report.json`、`docs/reports/phase41_a06_metadata_slug_followup_report.json`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-335 |
| CEK-TA-337 | P1 | done | 为 P41-A06 补充 single-model baseline comparison report 和 auditability impact report，并导出单条三审 JSON；本轮不创建 formal reviewed/approved/default/hard gate | `codex-expert-kit/rag/scripts/prepare_phase41_a06_single_model_baseline_third_audit_package.py`、`docs/research/phase41_a06_ensemble_baseline_auditability_supplemental_research.md`、`docs/audit/phase41_a06_single_model_baseline_third_audit_package_20260611.json`、`docs/reports/phase41_a06_single_model_baseline_third_audit_package_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-336 |
| CEK-TA-338 | P1 | done | 导入 P41-A06 三审结果，只升级候选为 accepted_for_draft，并保持 reviewed/approved/default/hard gate 全部关闭 | `codex-expert-kit/rag/scripts/apply_phase41_a06_third_audit_result.py`、`docs/audit/audit_result_phase41_a06_single_model_baseline_third_audit_20260611_strict_v3.json`、`docs/reports/phase41_a06_third_audit_import_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-337 |
| CEK-TA-339 | P1 | done | 为 P41-A06 生成 reviewed/caveat_only 准备审计包，只请求 formal reviewed 许可；不创建 formal knowledge/approved/default/hard gate | `codex-expert-kit/rag/scripts/export_phase41_a06_reviewed_preparation_package.py`、`docs/audit/phase41_a06_reviewed_preparation_audit_package_20260611.json`、`docs/reports/phase41_a06_reviewed_preparation_gap_report.json` | CEK-TA-338 |
| CEK-TA-340 | P1 | done | 导入 P41-A06 reviewed-preparation 审计结果，创建 formal reviewed/caveat_only 知识并重建索引和 Vue3 fixture；保持 approved/default/hard gate 全部关闭 | `codex-expert-kit/rag/scripts/apply_phase41_a06_reviewed_preparation_result.py`、`docs/audit/audit_result_phase41_a06_reviewed_preparation_20260611_strict_v1.json`、`docs/reports/phase41_a06_reviewed_preparation_import_report.json`、`codex-expert-kit/rag/knowledge/KB_AI_20_NUMERIC_SCORING/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-339 |
| CEK-TA-334 | P1 | done | 验证 Phase 41 全量 41 条目标的 MCP/SearchLab/KnowledgeTree 联动，生成最终验收报告并更新 Phase 状态 | `codex-expert-kit/rag/scripts/validate_phase41_runtime_linkage.py`、`docs/reports/phase41_final_acceptance_report.md` | CEK-TA-340 |

## 上游输入

```text
1. 用户确认的主线：表格/统计模型做 numeric scoring，Qwen3 做审计助手，deterministic final gate 做最终交易权限。
2. docs/research/phase36_ai_engineering_model_platform_selection_proposal.md
3. docs/tasks/phase36_ai_engineering_gating_scoring_knowledge.md
4. docs/tasks/phase38_ai_model_platform_poc_knowledge.md
5. docs/tasks/phase40_ai_continuous_learning_retraining_loop.md
6. docs/contracts/phase38_ai_scoring_gate_runtime_contract.md
7. docs/contracts/phase38_training_data_and_eval_contract.md
8. docs/contracts/phase40_feedback_dataset_contract.md
9. codex-expert-kit/rag/knowledge_tree.md
10. codex-expert-kit/rag/knowledge_item_schema.md
11. codex-expert-kit/rag/indexes/knowledge_items.json
```

## 下游输出

```text
1. AI Engineering 下 Hybrid Scoring Stack 的知识范围、专题和 canonical node。
2. LightGBM / XGBoost / Logistic Regression / CatBoost 的模型选择、比较、校准、阈值和解释知识。
3. Qwen3 Audit Assistant 的职责边界、thinking mode 策略、SFT/DPO 边界、strict JSON schema 和 citation 契约。
4. deterministic final gate 的输入、输出、审批、release manifest 和 rollback 知识。
5. 外接 LLM gating/scoring 项目的 AI IDE 主动检索模板和运行时验证样例。
6. MCP/SearchLab/KnowledgeTree/Vue3 可检索、可审计、可引用的 formal reviewed 知识。
```

## 建议 L3 专题

Phase 41 不新增顶级主枝，统一挂在 `kt.ai_engineering` 和少量现有相关分支下。

| L3 专题 | canonical node | 说明 |
| --- | --- | --- |
| Model Family Selection | `kt.ai_engineering.numeric_scoring.model_family_selection` | Rule baseline、Logistic Regression、LightGBM、XGBoost、CatBoost 同场比较 |
| Tabular Scorer Training | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | 类别特征、样本权重、类别不平衡、HPO、时间切分 |
| Scorer Explainability | `kt.ai_engineering.numeric_scoring.scorer_explainability` | SHAP、feature importance、解释边界和非因果声明 |
| Calibration Uncertainty | `kt.ai_engineering.calibration_threshold.uncertainty` | 独立校准集、Platt/isotonic、分层校准、conformal abstain |
| Decision-Time Feature Store | `kt.ai_engineering.decision_time_feature_contract.feature_store` | point-in-time join、线上线下一致性、feature lineage |
| Qwen3 Audit Assistant | `kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant` | Qwen3 角色边界、thinking mode、strict JSON、citation、no-hit abstain |
| Qwen3 Training Recipe | `kt.ai_engineering.llm_audit_assistant.qwen3_training_recipe` | SFT、DPO、LoRA、RAG-first、schema eval、reason code eval |
| Hybrid Runtime Contract | `kt.ai_engineering.model_release_governance.hybrid_runtime_contract` | scorer、calibrator、Qwen3、RAG、final gate 的组合 trace |
| Training Platform Governance | `kt.ai_engineering.model_release_governance.training_platform_governance` | MLflow、Ray、Kubeflow、Feast 的条件引入和治理边界 |

## 知识点规划

审计后总量：41 条。

### P0-Core：22 条

```text
1. P41-A01：默认同场比较 Rule baseline、Logistic Regression、LightGBM、XGBoost；CatBoost 只作为条件候选。
2. P41-A02：Logistic Regression 必须作为透明 baseline。
3. P41-A03：LightGBM 与 XGBoost 必须使用相同时间切分和指标评估。
4. P41-A05：模型选择必须比较业务成本、延迟、可解释性、校准质量和治理复杂度。
5. P41-B01：bad_trade / false_allow 少数类必须声明 class weight、sample weight 或采样策略，并复核校准。
6. P41-B02：HPO 只能读取 train/validation，不得读取 holdout、calibration、shadow、paper 或 incident pool。
7. P41-B03：时间序列交易样本必须使用时间感知切分，不能随机打散。
8. P41-B05：训练样本必须记录 dataset_hash、split_manifest_hash、feature_schema_version 和 label_policy_version。
9. P41-C01：raw score 不得直接作为交易概率或 final gate 输入。
10. P41-C02：校准器必须使用独立 calibration set。
11. P41-C03：threshold policy 必须绑定业务成本矩阵、false allow、false block 和 review capacity。
12. P41-D01：每个训练样本必须做 point-in-time feature join。
13. P41-D02：线上线下特征生成必须一致；不一致时必须记录差异并阻断默认指导。
14. P41-D03：feature lineage 必须记录 source_object_ref、lineage_ref、schema_version 和缺失值策略。
15. P41-D04：label_observation_window 必须晚于 decision_time，outcome 口径不在 AI Engineering 定义交易收益本体。
16. P41-E01：Qwen3 只能做审计助手，不做 numeric scorer、final gate 或事实来源。
17. P41-E02：Qwen3 审计输出必须是 strict JSON。
18. P41-E03：Qwen3 无 RAG 命中、无来源或引用冲突未消解时必须 abstain 或 needs_human_review。
19. P41-E05：Qwen3 SFT 只训练格式、reason code、引用习惯和审计流程，不训练交易概率。
20. P41-E09：RAG context、用户交易摘要和检索文档必须视为不可信输入。
21. P41-F01：final gate 可以读取校准风险信号和 threshold policy，但不得服从 Qwen3 recommendation 或 raw model score。
22. P41-F02：composite release manifest 必须绑定 scorer、calibrator、threshold、Qwen3 prompt、RAG index、reason taxonomy 和 rollback target。
```

### P0-Extended：12 条

```text
23. P41-A04：CatBoost 只在类别变量丰富或类别处理成本较高时作为条件候选。
24. P41-A06：模型集成只能作为增强项。
25. P41-A07：feature attribution / top_features 只能辅助调试和审计，不等于因果解释或交易规则证据。
26. P41-B04：entity group split 必须避免同一策略/品种/周期族跨 split 泄漏。
27. P41-C04：Platt 与 isotonic 的选择必须声明样本量、单调性假设和过拟合风险。
28. P41-C05：校准应按 regime、strategy family、timeframe 切片检查，但不定义 Trading 本体。
29. P41-E04：thinking mode 不保存私有 chain-of-thought。
30. P41-E06：DPO/preference pair 只能优化审计质量，不得以 PnL 高低直接构造偏好。
31. P41-E07：RAG-first 和 prompt 修正必须先于 SFT/LoRA。
32. P41-F03：每次 hybrid scoring 必须记录 audit trace。
33. P41-F04：champion/challenger 晋级必须经过 offline、shadow、paper/soft gate 和人工批准。
34. P41-F08：hybrid runtime 必须定义 latency budget、timeout、fallback、fail-to-review / fail-closed。
```

### P1：7 条

```text
35. P41-B06：active learning 或 hard-example mining 只能作为复核采样增强。
36. P41-C06：conformal 或 abstain band 只能作为不确定性增强层。
37. P41-D05：Feast 或正式 feature store 只在离线/在线一致性压力出现后引入。
38. P41-E08：vLLM 或本地 Qwen serving 只在延迟、吞吐或离线批量审计需求明确后引入。
39. P41-F05：MLflow registry 只有在模型版本和 release manifest 复杂度上升时引入。
40. P41-F06：Ray/Kubeflow 只在分布式训练或流水线编排需求明确后引入。
41. P41-F07：任何平台接入都必须保留 CEK-TA 知识检索只读、路径 resolver 和可移植配置边界。
```

## 输入契约

Phase 41 的采集任务必须至少包含：

```text
knowledge_topic_id
target_canonical_node_id
priority: P0-Core | P0-Extended | P1
claim_type
model_role: rule_baseline | tabular_scorer | calibrator | llm_audit_assistant | final_gate | platform_governance
expected_sources
source_types
applicability
not_applicable_when
related_phase36_items
related_phase38_items
related_phase40_items
runtime_consumer: MCP | SearchLab | external_ai_ide | Vue3 | training_project
acceptance_gate
```

外接项目调用 Phase 41 知识时，应至少提供：

```text
project_adapter_id
task_type
mode: research | backtest | replay | paper | live
requested_decision: score | audit | train | calibrate | threshold | release
trade_candidate_snapshot_ref
feature_schema_version
label_policy_version
model_family
scorer_version
calibrator_version
qwen_model_version
prompt_version
rag_index_version
threshold_policy_version
risk_policy_version
```

## 输出契约

RAG/MCP 返回 Phase 41 知识时必须包含：

```text
knowledge_id
canonical_node_id
review_status
machine_gate.default_guidance
claim_type
model_role
llm_usage_policy
source_evidence
conflict_status
freshness
applicability
not_applicable_when
related_trading_refs
recommended_next_action
```

Hybrid runtime 推荐输出必须区分：

```text
scorer_output:
  quality_score
  bad_trade_risk
  calibrated_probability
  risk_bucket
  uncertainty_bucket
  top_features
  model_version

qwen_audit_output:
  recommendation
  reason_codes
  risk_flags
  missing_fields
  knowledge_refs
  unsupported_claims
  citation_completeness_score
  requires_human_review

final_gate_output:
  gate_decision
  deterministic_rule_hits
  risk_policy_version
  threshold_policy_version
  release_manifest_version
  audit_trace_id
```

## 边界范围

本 Phase 包含：

```text
1. Hybrid Scoring Stack 专业知识范围和任务拆分。
2. 表格/统计模型、Qwen3 审计助手、deterministic final gate 的职责边界。
3. 特征时点一致性、标签观察窗口、校准、阈值、HPO、解释、发布治理知识。
4. 联网采集、候选生成、AI/人工审计、formal reviewed 沉淀和运行时验证任务。
5. MCP/SearchLab/KnowledgeTree/Vue3 对新知识的只读检索和审计展示对齐。
```

本 Phase 不包含：

```text
1. 不训练真实模型。
2. 不部署 Qwen3 服务。
3. 不把 Qwen3、LightGBM、XGBoost、CatBoost 或任何模型设为最终交易 gate。
4. 不生成买卖建议。
5. 不操作真实交易账户或密钥。
6. 不采集 K 线、回测、fill model、仓位、风控、执行规则本体；这些归 Phase 37 / Trading Engineering。
7. 不把 candidate/reviewed 自动升级为 approved。
8. 不引入新数据库或外部服务依赖，除非开发者另行确认。
```

## 涉及组件

```text
docs/research/
docs/contracts/
docs/audit/
docs/reports/
codex-expert-kit/rag/knowledge_tree.md
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/scripts/
codex-expert-kit/mcp/
codex-expert-kit/api/
ui/src/data/formalKnowledgeItems.ts
ui/src/data/phase23Candidates.ts
ui/src/views/KnowledgeTreeView.vue
ui/src/views/SearchLab.vue
```

## 涉及数据结构

```text
KnowledgeItem v1.1
ResearchIngestionTask
CandidateKnowledge
AI audit package
AI audit result
knowledge_items.json
trade_candidate_snapshot
feature_schema
label_policy
scorer_output
qwen_audit_output
final_gate_output
release_manifest
```

## 涉及数据库/存储

```text
1. 本 Phase 默认不引入数据库。
2. 正式知识继续使用文件化 JSON knowledge item 和 knowledge_items.json 聚合索引。
3. 候选知识继续存放在 codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/。
4. 后续如需 MLflow、Feast、Kubeflow、Ray 真实接入，必须另起实现 Phase 并由开发者确认。
```

## 实施步骤

```text
1. 建立 Phase 41 任务卡和索引。
2. 输出知识范围、L3 专题和跨分支边界。
3. 输出 hybrid runtime、training data、feature、label、calibration、Qwen3 audit、final gate 契约。
4. 创建并按范围审计补丁修正 41 条知识点采集矩阵和 ResearchIngestionTask 队列。
5. 导出知识范围审计 JSON，由外部 AI/人工先审计边界和数量。
6. 联网采集 P0-Core 来源，生成候选知识包。
7. 导出候选 AI 审计包并运行质量门禁。
8. 按审计结果补证、回写、沉淀 formal reviewed。
9. 重建 knowledge_items.json 和 Vue3 fixture。
10. 验证 MCP/SearchLab/KnowledgeTree 检索、引用、阻断和降级。
```

## Definition of Done

```text
1. Phase 41 任务卡存在并登记到 docs/index_tasks.md 和 docs/tasks/README.md。
2. 上游 Phase 36/38/40 的边界已引用。
3. 任务卡明确输入、输出、契约、边界、存储、DoD 和测试。
4. 知识点规划明确 P0-Core、P0-Extended、P1。
5. 明确 Qwen3 只做 audit assistant，不做 numeric scorer 或 final gate。
6. 明确表格模型只做 scorer / risk ranking，不直接执行交易。
7. 明确 deterministic final gate 是最终交易权限来源。
8. 涉及中文文档时以 UTF-8 读取和写入，无乱码。
```

## 测试与验收

```text
文档验收：
  - docs/index_tasks.md 能找到 Phase 41 和 CEK-TA-318 至 CEK-TA-327。
  - docs/tasks/README.md 能找到 Phase 41 任务卡。
  - docs/tasks/phase41_hybrid_scoring_qwen3_audit_stack.md 包含任务卡必备章节。

知识验收：
  - 后续知识候选必须有来源、适用范围、不适用场景、冲突状态和 review_status。
  - 不允许无来源或未消解冲突知识进入 reviewed。
  - 不允许 candidate/reviewed 自动升级 approved。

运行时验收：
  - 后续 formal reviewed 入库后，MCP/SearchLab/KnowledgeTree 能按 canonical node 检索。
  - no-hit、无来源、冲突未消解时必须降级或阻断默认指导。

编码验收：
  - PowerShell 使用 UTF-8 读取检查。
  - 运行乱码门禁脚本或等效 UTF-8 检查。
```

## 风险与回滚

| 风险 | 影响 | 处理 |
| --- | --- | --- |
| 把 Qwen3 误当核心 scorer | 可能让语言置信度替代概率校准 | 在任务卡和知识卡中强制 role boundary |
| 把表格模型输出直接作为 final gate | 可能绕过风控和审批 | final gate 必须只读 policy/version/rule hits |
| 知识与 Phase 37 Trading 本体混杂 | 知识树分类污染 | 交易规则本体只引用，不归入 Phase 41 |
| 过早引入平台复杂度 | POC 被 MLflow/Feast/Kubeflow 复杂度拖慢 | 平台知识先做治理卡，真实接入另开 Phase |
| 来源不足或过期 | 知识无法 reviewed | 保持 candidate 或 needs_more_evidence，不入正式索引 |

回滚方式：

```text
1. 若任务卡分类不合适，回滚 docs/index_tasks.md、docs/tasks/README.md 和本任务卡新增内容。
2. 若后续候选生成有误，只回滚候选和审计包，不删除已审计正式知识。
3. 若 knowledge_tree 节点错误，先恢复上一个 knowledge_tree 版本并重建索引。
```

## 需要开发者确认的问题

```text
1. Phase 41 是否确认作为 Phase 38 的后续扩展，而不是并入 Phase 38。
2. 是否接受审计后 41 条作为本轮补充知识点范围。
3. 是否把 CatBoost 作为 P0-Extended 条件候选，而不是 P0 必选模型。
4. 是否后续需要单独创建“Qwen3 本地部署与训练平台实作 Phase”。
```

## 状态更新要求

完成每个任务后必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase41_hybrid_scoring_qwen3_audit_stack.md
```

如果新增契约、研究、审计或报告文档，还必须更新：

```text
docs/index_tasks.md 的文档入口
相关 Phase 报告
```
