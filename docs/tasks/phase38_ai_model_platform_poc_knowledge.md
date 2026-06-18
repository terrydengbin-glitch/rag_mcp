# Phase 38: AI 模型平台与交易 Gating/Scoring POC 知识扩展

## Phase 目标

Phase 38 承接 Phase 36 的模型与训练平台选型方案，把“交易 LLM gating/scoring 项目”继续拆成可采集、可审计、可检索、可被外部 AI IDE 复用的专业知识子板块。

本 Phase 的重点不是马上训练模型，而是补齐外接项目真正落地前必须掌握的 AI Engineering 知识：

```text
数值模型负责 scoring / risk ranking / review priority。
LLM 负责审计解释、reason code、RAG 引用和人工复核摘要。
确定性风控负责最终 gate、仓位、kill switch 和实盘安全边界。
```

Phase 38 必须把“RAG AI 板块”拆清楚：

```text
RAG Engineering 只负责检索、引用、machine gate、上下文预算和 no-hit 降级。
Numeric Scoring 负责数值打分、meta-labeling、模型比较、校准和阈值。
LLM Audit Assistant 负责结构化审计输出，不负责最终交易决策。
Trading Engineering 继续负责 K 线、回测、fill、风控、执行等交易规则本体。
```

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-266 | P0 | done | 定义 Phase 38 AI 模型平台与 POC 知识子板块、canonical node 和跨分支路由 | `codex-expert-kit/rag/knowledge_tree.md`、`docs/research/phase38_ai_model_platform_knowledge_scope.md` | CEK-TA-265 |
| CEK-TA-267 | P0 | done | 定义 Numeric Scorer、LLM Audit Assistant、Deterministic Final Gate 的职责与 API 契约 | `docs/contracts/phase38_ai_scoring_gate_runtime_contract.md` | CEK-TA-266 |
| CEK-TA-268 | P0 | done | 定义训练数据、决策时特征、标签、校准集和评估集的数据契约 | `docs/contracts/phase38_training_data_and_eval_contract.md` | CEK-TA-267 |
| CEK-TA-269 | P0 | done | 创建 60-66 条 Phase 38 知识点采集矩阵和 ResearchIngestionTask 队列 | `docs/research/phase38_ai_model_platform_collection_matrix.md`、`docs/research/phase38_ai_model_platform_research_task_queue.md` | CEK-TA-268 |
| CEK-TA-270 | P0 | done | 生成 Phase 38 知识范围审计 JSON，供外部 AI/人工先审计分支、边界和知识点数量 | `docs/audit/phase38_ai_model_platform_knowledge_scope_for_audit.json` | CEK-TA-269 |
| CEK-TA-271 | P1 | done | 联网采集 P0-Core 知识来源，生成候选知识包 | `codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/`、`docs/reports/phase38_p0_core_candidate_generation_report.md` | CEK-TA-270 |
| CEK-TA-272 | P1 | done | 导出 Phase 38 候选 AI 审计包并等待统一审计；needs_more_evidence 补证在审计结果返回后处理 | `docs/audit/phase38_p0_core_candidate_audit_package_20260610.json`、`docs/reports/phase38_p0_core_candidate_quality_gate.json` | CEK-TA-271 |
| CEK-TA-273 | P1 | done | 将通过审计的 Phase 38 候选沉淀为 formal reviewed 知识并重建索引 | `codex-expert-kit/rag/knowledge/KB_AI_20_NUMERIC_SCORING/`、`codex-expert-kit/rag/knowledge/KB_AI_21_CALIBRATION_THRESHOLD/`、`codex-expert-kit/rag/knowledge/KB_AI_22_DECISION_TIME_FEATURES/`、`codex-expert-kit/rag/knowledge/KB_AI_23_LLM_AUDIT_ASSISTANT/`、`codex-expert-kit/rag/knowledge/KB_AI_24_SHADOW_PAPER_OPE/`、`codex-expert-kit/rag/knowledge/KB_AI_25_MODEL_RELEASE_GOVERNANCE/`、`codex-expert-kit/rag/knowledge/KB_10_RAG_ENGINEERING/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts` | CEK-TA-272 |
| CEK-TA-274 | P1 | done | 验证 MCP/SearchLab/KnowledgeTree 能按 Phase 38 子板块检索、引用、阻断和降级 | `codex-expert-kit/rag/scripts/validate_phase38_runtime_linkage.py`、`docs/reports/phase38_runtime_linkage_validation_report.json`、`codex-expert-kit/mcp/tests/`、`codex-expert-kit/api/tests/`、`ui/tests/e2e/` | CEK-TA-273 |
| CEK-TA-275 | P1 | done | 生成 Phase 38 验收报告并更新任务索引 | `docs/reports/phase38_ai_model_platform_poc_knowledge_report.md` | CEK-TA-274 |
| CEK-TA-276 | P1 | done | 导入 Phase 38 P0-Core 严格审计结果，分流 draft、补证和拒绝重建候选 | `docs/audit/audit_result_phase38_p0_core_20260610_strict_v1.json`、`docs/reports/phase38_p0_core_audit_import_report.json` | CEK-TA-272 |
| CEK-TA-277 | P1 | done | 为 Phase 38 P0-Core 7 条 needs_more_evidence 候选补 claim-specific 来源和 CEK-TA 内部契约 | `docs/contracts/phase38_rag_citation_and_reason_taxonomy_contract.md`、`docs/research/phase38_p0_core_supplemental_research.md` | CEK-TA-276 |
| CEK-TA-278 | P1 | done | 导出 Phase 38 P0-Core 补证后二审包，供外部 AI/人工复审 | `docs/audit/phase38_p0_core_supplemental_audit_package_20260610.json` | CEK-TA-277 |
| CEK-TA-279 | P1 | done | 导入 Phase 38 P0-Core 补证二审结果，7 条进入 formal draft 队列，G04-R1 保留补证并修正默认指导元数据 | `docs/audit/audit_result_phase38_p0_core_supplemental_reaudit_20260610_strict_v2.json`、`docs/reports/phase38_p0_core_supplemental_reaudit_import_report.json` | CEK-TA-278 |
| CEK-TA-280 | P1 | done | 为 G04-R1 补充上下文预算、字段白名单、top-k 和显式展开策略证据，并导出三审包 | `docs/research/phase38_g04_context_budget_supplemental_research.md`、`docs/audit/phase38_g04_context_budget_third_audit_package_20260610.json` | CEK-TA-279 |
| CEK-TA-281 | P1 | done | 同步 Phase 38 AI Engineering 子板块到 FastAPI/Vue3 知识树节点，校验候选归类和 UI 可见性 | `codex-expert-kit/api/codex_expert_kit_api/services.py`、`codex-expert-kit/api/tests/`、`docs/reports/phase38_knowledge_tree_ui_node_sync_report.json` | CEK-TA-266 |
| CEK-TA-282 | P1 | done | 导入 G04-R1 三审结果，将其升级为 accepted_for_draft 但继续阻断 reviewed/approved/default guidance/hard gate | `docs/audit/audit_result_phase38_g04_context_budget_third_reaudit_20260610_strict_v3.json`、`docs/reports/phase38_g04_context_budget_third_reaudit_import_report.json`、`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_g04_context_budget_field_trimming_001.json` | CEK-TA-280 |
| CEK-TA-283 | P1 | done | 对齐 Phase 38 P0-Extended/P1 剩余采集范围，修正矩阵与队列优先级口径并确认 66 条总量 | `docs/research/phase38_ai_model_platform_collection_matrix.md`、`docs/research/phase38_ai_model_platform_research_task_queue.md`、`docs/reports/phase38_extended_p1_scope_alignment_report.json` | CEK-TA-275 |
| CEK-TA-284 | P1 | done | 联网采集 Phase 38 P0-Extended/P1 来源并生成剩余候选知识包 | `codex-expert-kit/rag/scripts/generate_phase38_extended_p1_candidates.py`、`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/`、`docs/reports/phase38_extended_p1_candidate_generation_report.md` | CEK-TA-283 |
| CEK-TA-285 | P1 | done | 导出 Phase 38 P0-Extended/P1 候选 AI 审计包并运行质量门禁 | `codex-expert-kit/rag/scripts/export_phase38_extended_p1_audit_package.py`、`docs/audit/phase38_extended_p1_candidate_audit_package_20260610.json`、`docs/reports/phase38_extended_p1_candidate_quality_gate.json` | CEK-TA-284 |
| CEK-TA-286 | P1 | done | 导入 Phase 38 P0-Extended/P1 审计结果并按 Phase 32 工作流分流补证、拒绝和 reviewed 沉淀 | `docs/audit/audit_result_phase38_extended_p1_20260610_strict_v1.json`、`docs/reports/phase38_extended_p1_audit_import_report.json`、`codex-expert-kit/rag/scripts/apply_phase38_extended_p1_audit_result.py`、`ui/src/data/phase23Candidates.ts` | CEK-TA-285 |
| CEK-TA-287 | P1 | done | 为 Phase 38 P0-Extended/P1 13 条 needs_more_evidence 和 C10-R1 补充 claim-specific 来源并导出二审包 | `codex-expert-kit/rag/scripts/apply_phase38_extended_p1_supplemental_evidence.py`、`docs/research/phase38_extended_p1_supplemental_research.md`、`docs/audit/phase38_extended_p1_supplemental_audit_package_20260610.json`、`docs/reports/phase38_extended_p1_supplemental_evidence_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-286 |
| CEK-TA-288 | P1 | done | 导入 Phase 38 P0-Extended/P1 补证二审结果，13 条进入 formal draft 队列，B10 保留补证 | `codex-expert-kit/rag/scripts/apply_phase38_extended_p1_supplemental_reaudit_result.py`、`docs/audit/audit_result_phase38_extended_p1_supplemental_reaudit_20260610_strict_v2.json`、`docs/reports/phase38_extended_p1_supplemental_reaudit_import_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-287 |
| CEK-TA-289 | P1 | done | 为 B10 单独补 Bayesian calibration / Bayesian uncertainty calibration 直接来源并导出三审包 | `codex-expert-kit/rag/scripts/apply_phase38_b10_bayesian_calibration_supplement.py`、`docs/research/phase38_b10_bayesian_calibration_supplemental_research.md`、`docs/audit/phase38_b10_bayesian_calibration_third_audit_package_20260610.json`、`docs/reports/phase38_b10_bayesian_calibration_supplement_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-288 |
| CEK-TA-290 | P1 | done | 导入 B10 三审结果，将其升级为 accepted_for_draft，并保留校准层边界、来源去重和治理来源降级说明 | `codex-expert-kit/rag/scripts/apply_phase38_b10_third_reaudit_result.py`、`docs/audit/audit_result_phase38_b10_bayesian_calibration_third_reaudit_20260610_strict_v3.json`、`docs/reports/phase38_b10_bayesian_calibration_third_reaudit_import_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-289 |
| CEK-TA-341 | P1 | done | 将 Phase 38 残留 23 条 ai_passed 候选沉淀为 formal reviewed/caveat_only 知识并重建索引 | `codex-expert-kit/rag/scripts/promote_phase38_ai_passed_candidates_to_reviewed.py`、`docs/reports/phase38_ai_passed_to_reviewed_promotion_report.json`、`codex-expert-kit/rag/knowledge/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-290 |

## 上游输入

```text
docs/research/phase36_ai_engineering_model_platform_selection_proposal.md
docs/reports/phase36_ai_engineering_completion_audit_report.md
docs/contracts/ai_engineering_gating_scoring_contract.md
docs/contracts/ai_engineering_knowledge_item_policy.md
docs/contracts/external_ai_active_retrieval_protocol.md
docs/tasks/phase36_ai_engineering_gating_scoring_knowledge.md
docs/tasks/phase37_trading_engineering_knowledge_expansion.md
codex-expert-kit/rag/knowledge_tree.md
codex-expert-kit/rag/knowledge_item_schema.md
```

## 下游输出

```text
1. AI Engineering 下新增或强化的模型平台 POC 子板块。
2. Phase 38 知识点范围、采集矩阵和审计 JSON。
3. Numeric scorer、LLM audit assistant、final gate 的职责契约。
4. 训练数据、校准、阈值、shadow/paper/OPE、发布治理的知识候选。
5. formal reviewed 知识、MCP/SearchLab/KnowledgeTree 可检索索引和 Vue3 审计展示。
6. 外接交易 LLM gating/scoring 项目可复用的 AI IDE 主动检索指导。
```

## 建议子板块

Phase 38 不新增顶级主枝，统一挂在现有 `kt.ai_engineering` 下，并对 Trading Engineering 只做引用。

| 子板块 | 建议 canonical node | 预计知识点 | 说明 |
| --- | --- | ---: | --- |
| Numeric Scoring / Meta-Labeling | `kt.ai_engineering.numeric_scoring` | 8-10 | Rule baseline、Logistic Regression、LightGBM、XGBoost、CatBoost、meta-labeling、review priority |
| Calibration & Threshold Policy | `kt.ai_engineering.calibration_threshold` | 8-10 | calibration holdout、Brier、ECE、cost matrix、threshold policy、false allow/false block |
| Decision-Time Feature & Leakage Gate | `kt.ai_engineering.decision_time_feature_contract` | 8-10 | event_time、feature_available_time、decision_time、label_observation_end_time、leakage unit test |
| LLM Audit Assistant | `kt.ai_engineering.llm_audit_assistant` | 8-10 | strict schema、reason code、citation resolver、unsupported claim detector、no-source abstain |
| Shadow / Paper / OPE Evaluation | `kt.ai_engineering.shadow_paper_ope_eval` | 8-10 | offline eval、shadow eval、paper/replay eval、OPE、human review precision |
| Model Release / Lineage / Rollback | `kt.ai_engineering.model_release_governance` | 8-10 | release manifest、dataset hash、model artifact、rollback、kill switch、approval |
| Trading AI RAG Pack & Citation Governance | `kt.rag_engineering.trading_ai_rag_pack` | 6-8 | 主动检索、引用完整率、machine gate、上下文预算、no-hit 降级 |

建议总量：

```text
P0-Core：36 条左右。
P0-Extended：18 条左右。
P1：12 条左右。
合计：60-66 条。
```

## 输入契约

Phase 38 的知识采集任务必须至少包含：

```text
knowledge_topic_id
target_canonical_node_id
priority: P0-Core | P0-Extended | P1
claim_type
expected_sources
source_types
applicability
not_applicable_when
related_phase36_items
related_phase37_trading_refs
runtime_consumer: MCP | SearchLab | external_ai_ide | Vue3 | training_project
acceptance_gate
```

外接项目调用 Phase 38 知识时，应至少提供：

```text
project_adapter_id
task_type
mode: research | backtest | replay | paper | live
requested_decision: score | gate | audit | train | evaluate | release
trade_candidate_snapshot_ref
feature_schema_version
label_policy_version
model_family
scorer_version
calibrator_version
threshold_policy_version
rag_index_version
risk_policy_version
```

## 输出契约

RAG/MCP 返回 Phase 38 知识时必须包含：

```text
knowledge_id
canonical_node_id
review_status
machine_gate.default_guidance
claim_type
llm_usage_policy
source_evidence
conflict_status
freshness
applicability
not_applicable_when
related_trading_refs
recommended_next_action
```

模型 POC 契约必须区分：

```text
scorer_output:
  quality_score
  bad_trade_risk
  calibrated_probability
  risk_bucket
  top_features
  model_version

llm_audit_output:
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
  risk_policy_version
  threshold_policy_version
  deterministic_rule_hits
  audit_trace_id
```

## 边界范围

本 Phase 包含：

```text
AI 模型平台与 POC 知识子板块规划。
数值 scorer、LLM 审计助手、确定性 final gate 的职责分离。
训练数据、特征、标签、校准、阈值、评估和发布治理知识。
联网采集、候选生成、AI/人工审计、formal reviewed 沉淀和运行时验证任务。
MCP/SearchLab/KnowledgeTree/Vue3 对新子板块的只读检索和审计展示对齐。
```

本 Phase 不包含：

```text
不训练真实模型。
不选择或绑定单一云厂商作为唯一平台。
不把 Qwen3、Llama、Mistral 或任何 LLM 设为最终交易 gate。
不生成买卖建议。
不操作真实交易账户或密钥。
不采集 K 线、回测、fill model、风控、执行等交易规则本体；这些属于 Phase 37 / Trading Engineering。
不把 candidate/reviewed 自动升级为 approved。
不引入新数据库，除非开发者另行确认。
```

## 涉及组件

```text
codex-expert-kit/rag/knowledge_tree.md
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/scripts/
codex-expert-kit/mcp/
codex-expert-kit/api/
ui/src/views/KnowledgeTreeView.vue
ui/src/views/SearchLab.vue
ui/src/data/formalKnowledgeItems.ts
ui/src/data/phase23Candidates.ts
docs/contracts/
docs/research/
docs/audit/
docs/reports/
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
decision_time_feature_schema
numeric_scorer_dataset
llm_audit_example
calibration_manifest
threshold_policy_manifest
release_manifest
```

## 涉及数据库/存储

本 Phase 默认继续使用文件化知识库和索引：

```text
codex-expert-kit/rag/candidates/
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/indexes/knowledge_items.json
docs/audit/
docs/research/
docs/reports/
ui/src/data/
```

不新增数据库。若后续需要模型实验库、向量库或审计数据库，必须先创建新任务卡并向开发者确认。

## 实施步骤

```text
1. 根据 Phase 36 选型方案确认 Phase 38 子板块和 canonical node。
2. 写出 Numeric Scorer / LLM Audit Assistant / Final Gate 契约。
3. 写出训练数据、特征、标签、校准、阈值、评估和发布治理契约。
4. 创建 60-66 条知识点采集矩阵，分 P0-Core、P0-Extended、P1。
5. 生成知识范围审计 JSON，先审计分支和知识点范围。
6. 按 P0-Core 联网采集权威来源和实例，生成候选知识。
7. 导出候选审计包，按外部审计结果补证、优化、回写。
8. 通过质量门禁后转 formal reviewed，重建 knowledge_items.json 和 Vue3 fixture。
9. 验证 MCP/SearchLab/KnowledgeTree 能按新子板块检索、引用、阻断和降级。
10. 生成 Phase 38 验收报告。
11. 同步 FastAPI 知识树静态节点和别名，确保 Vue3 知识树能显示 Phase 38 AI Engineering 二级板块，并能按节点筛选候选。
```

## CEK-TA-281 子板块 UI 同步契约

上游输入：

```text
codex-expert-kit/rag/knowledge_tree.md
codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/
ui/src/data/phase23Candidates.ts
```

下游输出：

```text
FastAPI /api/knowledge-tree/nodes/kt.ai_engineering/children
FastAPI /api/candidates?tree_node_id=...
Vue3 KnowledgeTreeView 左侧知识树和候选联动筛选
```

输入契约：

```text
tree_node_id 和 canonical_node_id 必须保留候选原始归类。
Phase 38 的六个 AI Engineering 子板块挂在 kt.ai_engineering 下作为 Level 2。
Trading AI RAG Pack 保持原始 kt.rag_engineering.trading_scoring_rag_pack 归类，同时在 FastAPI 层通过别名挂到 kt.ai_engineering.rag_engineering.trading_scoring_rag_pack 展示，避免破坏历史候选 ID。
```

输出契约：

```text
children 接口必须返回 Phase 38 新增 Level 2 子板块。
候选筛选必须支持原始节点 ID 和展示别名节点 ID。
知识树节点同步不得改变 candidate/reviewed/approved 状态。
正式知识数量仍以 knowledge_items.json 为准，未转 formal reviewed 的候选不计入 formal knowledge。
```

边界范围：

```text
本任务只修复知识树节点展示和候选筛选归类。
不执行候选转 formal reviewed。
不修改 Phase 38 候选审计结论。
不把 reviewed/accepted_for_draft 自动升级为 approved。
```

## CEK-TA-282 G04-R1 三审结果导入契约

上游输入：

```text
docs/audit/phase38_g04_context_budget_third_audit_package_20260610.json
外部三审报告：G04-R1 accepted_for_draft
codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_g04_context_budget_field_trimming_001.json
```

下游输出：

```text
docs/audit/audit_result_phase38_g04_context_budget_third_reaudit_20260610_strict_v3.json
docs/reports/phase38_g04_context_budget_third_reaudit_import_report.json
ui/src/data/phase23Candidates.ts
```

输入契约：

```text
三审只允许 accepted_for_draft / needs_more_evidence / rejected。
accepted_for_draft 只表示进入 formal draft queue。
三审不得直接输出 reviewed、approved、default guidance 或 hard gate。
```

输出契约：

```text
candidate.status.review_status = accepted
candidate.status.ingestion_decision = accepted_for_draft
candidate.workflow.stage = ai_audited
candidate.workflow.queue_group = ai_passed
candidate.workflow.formal_review_status = draft
candidate.review.ai_audit.decision = accepted_for_draft
candidate.review.ai_audit.reviewed_allowed = false
candidate.review.ai_audit.approved_allowed = false
candidate.review.ai_audit.default_guidance_allowed = false
candidate.review.ai_audit.hard_gate_allowed = false
candidate.conversion_target.target_review_status = draft
candidate.conversion_target.default_guidance_allowed = false
candidate.conversion_target.hard_gate_allowed = false
```

边界范围：

```text
本任务不创建 formal reviewed 知识。
本任务不修改知识库 approved 规则。
本任务不改变 G04-R1 的 RAG Engineering 分类。
本任务不把 top_k=5 或 token_budget=4000 写成全局最优，只作为 P0 policy default。
```

## CEK-TA-341 残留 ai_passed 候选沉淀契约

任务目标：

```text
将 Phase 38 中仍停留在 workflow.queue_group=ai_passed 的 23 条 accepted_for_draft 候选，按 Phase 32 工作流沉淀为 formal reviewed/caveat_only 知识，清空待转正队列，并重建正式知识索引和 Vue3 fixture。
```

上游输入：

```text
1. Phase 38 已通过外部审计或补证审计的候选 JSON。
2. candidate.status.review_status=accepted。
3. candidate.status.ingestion_decision=accepted_for_draft。
4. candidate.workflow.queue_group=ai_passed。
5. candidate.conversion_target.proposed_knowledge_id。
6. candidate.source_refs、source_quality、conflict_audit 和 copyright 字段。
```

下游输出：

```text
1. formal knowledge JSON：review.review_status=reviewed。
2. machine_gate.default_guidance=caveat_only。
3. candidate.workflow.queue_group=formalized。
4. candidate.workflow.formal_knowledge_id 回链正式知识。
5. knowledge_items.json、formalKnowledgeItems.ts、phase23Candidates.ts、knowledgeTreeNodes.ts 重建。
6. Phase 38 runtime linkage、知识树统计、候选状态机、schema、污染和乱码门禁通过。
```

输入契约：

```text
只处理 candidate_id 以 cand_20260610_phase38_ 开头且 workflow.queue_group=ai_passed 的候选。
必须有 proposed_knowledge_id。
必须有 source_refs。
conflict_status 必须为 none 或 resolved。
copyright.stores_full_text=false。
copyright.stores_long_quote=false。
```

输出契约：

```text
formal.review.review_status=reviewed。
formal.review.default_guidance_allowed=false。
formal.review.approval_status=not_requested。
formal.machine_gate.default_guidance=caveat_only。
formal.review.ai_audit.approved_allowed=false。
formal.review.ai_audit.default_guidance_allowed=false。
formal.review.ai_audit.hard_gate_allowed=false。
candidate.workflow.stage=formalized_reviewed。
candidate.workflow.queue_group=formalized。
candidate.workflow.formal_review_status=reviewed。
```

边界范围：

```text
不创建 approved。
不进入 default guidance queue。
不启用 hard gate。
不删除 candidate 源文件。
不修改 Trading Engineering 本体规则。
不把 AI Engineering reviewed 知识当作实盘交易决策。
```

涉及组件：

```text
codex-expert-kit/rag/scripts/promote_phase38_ai_passed_candidates_to_reviewed.py
codex-expert-kit/rag/scripts/promote_phase38_accepted_candidates_to_reviewed.py
codex-expert-kit/rag/scripts/build_knowledge_items_index.py
codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py
codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py
codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py
codex-expert-kit/rag/scripts/validate_phase38_runtime_linkage.py
codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
```

Definition of Done：

```text
1. 23 条 ai_passed 候选全部转 formalized。
2. 正式知识总数从 250 增至 273。
3. 候选总数仍为 271，且保留审计追踪。
4. Phase 38 formal reviewed 数量为 66。
5. 所有新增 formal knowledge 均为 reviewed/caveat_only。
6. 无 approved/default guidance/hard gate 自动升级。
7. 索引和 Vue3 fixture 已重建。
8. 门禁和前端构建通过。
```

测试与验收：

```text
python codex-expert-kit/rag/scripts/promote_phase38_ai_passed_candidates_to_reviewed.py
python codex-expert-kit/rag/scripts/build_knowledge_items_index.py
python codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py
python codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py
python codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
python codex-expert-kit/rag/scripts/validate_knowledge_tree_alignment.py
python codex-expert-kit/rag/scripts/validate_phase38_runtime_linkage.py
npm --prefix ui run build
```

风险与回滚：

```text
风险：候选源文件仍存在，用户可能误以为还待审计；通过候选队列分组和 formal_knowledge_id 回链消解。
回滚：删除本任务新增的 23 条 formal knowledge 文件，恢复对应 candidate.workflow 为 ai_passed，重建 knowledge_items.json 和 Vue3 fixture。
```

## 审计结果导入补充契约

CEK-TA-276 到 CEK-TA-278 处理 Phase 38 P0-Core 严格审计结果，必须遵循：

```text
1. accepted_for_draft 只表示可以进入 formal draft 队列，不等于 reviewed、approved 或 default guidance。
2. needs_more_evidence 必须保留在补证队列，补充 claim-specific 来源和内部 CEK-TA 契约后才能重新审计。
3. rejected 候选不得删除，必须保留审计追踪；若知识方向仍有效，必须用新 candidate_id、normalized_claim 和 proposed_knowledge_id 重建。
4. G04 的空 slug 候选必须阻断，重建后的 ID 为 cand_20260610_phase38_p38_g04_context_budget_field_trimming_001。
5. Vue3 候选页读取候选 workflow 分组；MCP/SearchLab/知识树仍只读取 formal knowledge 索引。
6. 本轮不把任何 Phase 38 候选直接转为 formal reviewed 或 approved。
```

审计导入输出字段：

```text
audit_result_id
source_package_id
decision_summary
decisions[].candidate_id
decisions[].research_task_id
decisions[].decision
decisions[].allowed_next_stage
decisions[].blocking_reasons
decisions[].required_patches
decisions[].source_requirements
```

## Definition of Done

```text
1. Phase 38 任务卡存在并被 docs/index_tasks.md、docs/tasks/README.md 索引。
2. Phase 38 子板块、canonical node、知识点数量和优先级写清楚。
3. 上游 Phase 36 与 Phase 37 边界写清楚。
4. Numeric scorer、LLM audit assistant、final gate 的职责契约写清楚。
5. 训练数据、特征、标签、校准、阈值、评估和发布治理契约写清楚。
6. 每条知识采集任务都有来源要求、适用范围、不适用场景和审计门槛。
7. AI Engineering 与 Trading Engineering 没有规则本体重复收录。
8. candidate、reviewed、approved 状态语义没有被改变。
9. MCP/SearchLab/KnowledgeTree/Vue3 的读取边界明确。
10. 中文文档 UTF-8 无乱码。
```

## 测试与验收

文档与索引任务需要执行：

```text
文档存在性检查
索引一致性检查
UTF-8 乱码检查
```

后续采集与入库任务需要执行：

```text
python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
python -m pytest codex-expert-kit/mcp/tests
python -m pytest codex-expert-kit/api/tests
cd ui && npm run build
```

如测试脚本尚未覆盖 Phase 38 新契约，必须在验收报告中记录缺口并创建补测任务。

## 风险与回滚

| 风险 | 处理 |
| --- | --- |
| 把 RAG、LLM、数值模型混成一个大板块 | 子板块和 canonical node 拆分，RAG 只负责检索引用 |
| LLM 被误用为最终交易 gate | 契约中强制 LLM 只能输出 recommendation，final gate 由确定性规则执行 |
| 交易规则本体误收进 AI Engineering | 通过 Phase 37 跨分支引用契约路由回 Trading Engineering |
| PnL-only 标签污染 scorer | 标签知识必须包含过程质量、风险质量、执行质量和人工复核边界 |
| 数据泄漏进入训练特征 | decision-time feature contract 和 leakage unit test 必须作为 P0-Core |
| 未校准分数进入 hard gate | calibration / threshold policy 必须阻断 |
| candidate/reviewed 被当成 approved | 保持 Phase 32 状态机，不自动升级 approved |
| 上下文膨胀导致 AI IDE 调用慢 | RAG Pack 知识必须包含检索触发、top-k、字段裁剪和 no-hit 降级 |

回滚方式：

```text
1. 如果子板块过宽，调整 Phase 38 范围文档和任务卡，不删除已有正式知识。
2. 如果候选知识分支错误，修正 canonical_node_id 或移动候选，不直接复制。
3. 如果 formal reviewed 知识发现问题，降级 machine_gate 或 review_status，不直接删除 approved 规则。
4. 如果 MCP/Vue3 展示异常，回滚 fixture 或显示层改动，保留正式知识索引。
```

## 需要开发者确认的问题

```text
1. Phase 38 是否按 60-66 条知识点作为推荐范围推进？
2. 是否同意 P0 先覆盖 Numeric Scoring、Calibration、Decision-Time Feature、LLM Audit、Shadow/Paper/OPE、Release Governance？
3. 是否同意 Qwen3 只作为 LLM Audit Assistant 候选，不作为 primary numeric scorer？
4. 是否同意第一轮只做知识库与 POC 契约，不训练真实模型？
```

## 状态更新要求

完成任一任务后必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase38_ai_model_platform_poc_knowledge.md
相关 contracts/research/audit/reports 文档
```

不得只更新任务卡而不更新项目级索引。
