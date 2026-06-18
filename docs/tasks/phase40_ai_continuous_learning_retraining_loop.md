# Phase 40: AI Continuous Learning 与再训练闭环

## Phase 目标

为外接交易 LLM gating/scoring 项目补齐 AI Engineering 的持续学习、反馈治理、再训练、再校准、champion/challenger、shadow/paper/canary 验证和可回滚上线知识体系。

本 Phase 以现有知识树节点 `kt.ai_feedback_governance` / `KB_AI_18_FEEDBACK_GOVERNANCE` 为主归属，不新增顶级主枝。它解决的不是第一版 POC 如何训练，而是模型进入长期使用后，如何持续采集反馈、持续评估、定期训练、严格审批、灰度发布和可靠回滚。

核心原则：

```text
持续学习不等于在线自动学习。
再训练不等于自动上线。
LLM 不作为最终交易 gate。
交易规则本体仍归 Trading Engineering。
AI Engineering 只沉淀学习闭环、数据版本、标签、漂移、校准、发布和治理知识。
```

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-298 | P0 | done | 创建 Phase 40 任务卡并登记任务索引 | `docs/tasks/phase40_ai_continuous_learning_retraining_loop.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | Phase 39 |
| CEK-TA-299 | P0 | done | 定义 Continuous Learning 知识范围和 L3 专题结构 | `docs/research/phase40_ai_continuous_learning_scope.md`、`codex-expert-kit/rag/knowledge_tree.md` | CEK-TA-298 |
| CEK-TA-300 | P0 | done | 定义反馈日志、标签更新、数据集版本和审计追踪数据契约 | `docs/contracts/phase40_feedback_dataset_contract.md` | CEK-TA-299 |
| CEK-TA-301 | P0 | done | 定义漂移检测、再训练触发、再校准和阈值稳定性契约 | `docs/contracts/phase40_drift_retraining_recalibration_contract.md` | CEK-TA-300 |
| CEK-TA-302 | P0 | done | 定义 champion/challenger、shadow/paper/canary 和 release/rollback 契约 | `docs/contracts/phase40_champion_challenger_release_contract.md` | CEK-TA-301 |
| CEK-TA-303 | P0 | done | 创建 36 条持续学习知识点采集矩阵和 ResearchIngestionTask 队列 | `docs/research/phase40_continuous_learning_collection_matrix.md`、`docs/research/phase40_research_task_queue.md` | CEK-TA-302 |
| CEK-TA-304 | P0 | done | 导出 Phase 40 知识范围审计 JSON，先审计边界、专题和知识点数量 | `docs/audit/phase40_continuous_learning_scope_for_audit.json` | CEK-TA-303 |
| CEK-TA-305 | P1 | done | 联网采集 P0-Core 持续学习知识来源，生成候选知识包 | `codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/`、`docs/research/phase40_*`、`docs/reports/phase40_candidate_generation_report.md` | CEK-TA-304 |
| CEK-TA-306 | P1 | done | 导出候选 AI 审计包并运行来源、冲突、乱码和污染门禁 | `docs/audit/phase40_candidate_audit_package_*.json`、`docs/reports/phase40_candidate_quality_gate.json` | CEK-TA-305 |
| CEK-TA-307 | P1 | done | 按审计结果补证、回写、沉淀 formal reviewed，并重建索引和 Vue3 fixture | `codex-expert-kit/rag/knowledge/KB_AI_18_FEEDBACK_GOVERNANCE/`、`knowledge_items.json`、`ui/src/data/` | CEK-TA-306 |
| CEK-TA-308 | P1 | done | 验证 MCP/SearchLab/KnowledgeTree 能按持续学习子板块检索、引用、阻断和降级 | `codex-expert-kit/rag/scripts/validate_phase40_runtime_linkage.py`、`docs/reports/phase40_runtime_linkage_validation_report.json`、`codex-expert-kit/mcp/tests/`、`codex-expert-kit/api/tests/` | CEK-TA-307 |
| CEK-TA-310 | P1 | done | 继续采集 Phase 40 Batch D/E 剩余 18 条持续学习知识点，生成候选知识包 | `codex-expert-kit/rag/scripts/generate_phase40_extended_p1_candidates.py`、`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/`、`docs/research/phase40_batch_d_e_research.md`、`docs/reports/phase40_extended_p1_candidate_generation_report.md` | CEK-TA-308 |
| CEK-TA-311 | P1 | done | 导出 Phase 40 Batch D/E 候选 AI 审计包并运行质量门禁 | `codex-expert-kit/rag/scripts/export_phase40_extended_p1_audit_package.py`、`docs/audit/phase40_extended_p1_candidate_audit_package_20260610.json`、`docs/reports/phase40_extended_p1_candidate_quality_gate.json` | CEK-TA-310 |
| CEK-TA-312 | P1 | done | 导入 Phase 40 Batch D/E 严格审计结果，回写 13 条 accepted_for_draft 与 5 条 needs_more_evidence 候选状态 | `codex-expert-kit/rag/scripts/apply_phase40_extended_p1_audit_result.py`、`docs/audit/audit_result_phase40_extended_p1_batch_de_20260610_strict_v1.json`、`docs/reports/phase40_extended_p1_audit_import_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-311 |
| CEK-TA-313 | P1 | done | 为 Phase 40 Batch D/E 的 5 条 needs_more_evidence 候选补充证据并导出二审 JSON | `codex-expert-kit/rag/scripts/supplement_phase40_extended_p1_needs_evidence.py`、`docs/contracts/phase40_decision_cost_dashboard_metric_contract.md`、`docs/contracts/phase40_composite_release_artifact_contract.md`、`docs/audit/phase40_extended_p1_supplemental_reaudit_package_20260610.json`、`docs/reports/phase40_extended_p1_supplemental_evidence_report.json` | CEK-TA-312 |
| CEK-TA-314 | P1 | done | 导入 Phase 40 Batch D/E 补证二审结果，沉淀 5 条 formal reviewed 知识并重建索引 | `codex-expert-kit/rag/scripts/apply_phase40_extended_p1_supplemental_reaudit_result.py`、`docs/audit/audit_result_phase40_extended_p1_supplemental_reaudit_20260610_strict_v2.json`、`docs/reports/phase40_extended_p1_supplemental_reaudit_to_reviewed_report.json`、`codex-expert-kit/rag/knowledge/KB_AI_18_FEEDBACK_GOVERNANCE/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-313 |
| CEK-TA-309 | P1 | done | 生成 Phase 40 验收报告并更新任务状态 | `docs/reports/phase40_ai_continuous_learning_retraining_loop_report.md` | CEK-TA-314 |
| CEK-TA-315 | P1 | done | 导出 Phase 40 23 条 ai_passed 候选的 reviewed preparation 二审包，解决 formal_knowledge_id 存在但未入正式索引的准入缺口 | `codex-expert-kit/rag/scripts/export_phase40_ai_passed_reviewed_preparation_package.py`、`docs/audit/phase40_ai_passed_reviewed_preparation_audit_package_20260610.json`、`docs/reports/phase40_ai_passed_reviewed_preparation_gap_report.json` | CEK-TA-309 |
| CEK-TA-316 | P1 | done | 导入 Phase 40 reviewed preparation 二审结果，将 reviewed_allowed=true 的候选沉淀为 formal reviewed 并验证 MCP/SearchLab/知识树联动 | `codex-expert-kit/rag/scripts/apply_phase40_ai_passed_reviewed_preparation_result.py`、`docs/audit/audit_result_phase40_ai_passed_reviewed_preparation_20260610_strict_v1.json`、`docs/reports/phase40_ai_passed_reviewed_preparation_import_report.json`、`codex-expert-kit/rag/knowledge/KB_AI_18_FEEDBACK_GOVERNANCE/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-315 |
| CEK-TA-317 | P1 | done | 为 Phase 40 reviewed preparation 二审后仍需补证的 5 条候选补充来源和契约，再导出三审 JSON | `codex-expert-kit/rag/scripts/supplement_phase40_reviewed_preparation_needs_evidence.py`、`docs/contracts/phase40_review_budget_threshold_policy_contract.md`、`docs/contracts/phase40_release_manifest_kill_switch_contract.md`、`docs/research/phase40_reviewed_preparation_supplemental_research.md`、`docs/audit/phase40_reviewed_preparation_supplemental_reaudit_package_20260610.json`、`docs/reports/phase40_reviewed_preparation_supplemental_evidence_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-316 |
| CEK-TA-328 | P1 | done | 导入 Phase 40 reviewed preparation 补证三审结果，沉淀 5 条 formal reviewed 知识并重建索引 | `codex-expert-kit/rag/scripts/apply_phase40_reviewed_preparation_supplemental_reaudit_result.py`、`docs/audit/audit_result_phase40_reviewed_preparation_supplemental_reaudit_20260610_strict_v1.json`、`docs/reports/phase40_reviewed_preparation_supplemental_reaudit_import_report.json`、`codex-expert-kit/rag/knowledge/KB_AI_18_FEEDBACK_GOVERNANCE/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-317 |

## 上游输入

```text
1. 用户提供的持续学习建议。
2. docs/tasks/phase36_ai_engineering_gating_scoring_knowledge.md
3. docs/tasks/phase38_ai_model_platform_poc_knowledge.md
4. docs/tasks/phase39_knowledge_tree_single_source_stats_alignment.md
5. docs/research/phase36_ai_engineering_model_platform_selection_proposal.md
6. docs/contracts/phase38_ai_scoring_gate_runtime_contract.md
7. docs/contracts/phase38_training_data_and_eval_contract.md
8. codex-expert-kit/rag/knowledge_tree.md
9. codex-expert-kit/rag/knowledge_item_schema.md
10. codex-expert-kit/rag/indexes/knowledge_items.json
11. codex-expert-kit/rag/candidates/
```

## 下游输出

```text
1. AI Engineering 下 `kt.ai_feedback_governance` 的持续学习知识子体系。
2. 持续数据采集、标签刷新、漂移检测、再训练、再校准、发布回滚的数据契约。
3. 36 条可采集、可审计、可沉淀的专业知识点矩阵。
4. 外接 LLM gating/scoring 项目可复用的持续学习开发规则。
5. MCP/SearchLab/KnowledgeTree 可检索、可引用、可阻断的 formal reviewed 知识。
6. Vue3 知识树和候选审计页可展示持续学习板块覆盖情况。
```

## 建议 L3 专题

Phase 40 统一挂在 `kt.ai_feedback_governance` 下，建议新增或强化以下 L3 专题：

| L3 专题 | canonical node | 说明 |
| --- | --- | --- |
| Feedback Logging | `kt.ai_feedback_governance.feedback_logging` | 记录所有候选交易，不只记录已成交交易 |
| Label Refresh | `kt.ai_feedback_governance.label_refresh` | 多维标签更新、人工复核、good loss / bad win |
| Drift Monitoring | `kt.ai_feedback_governance.drift_monitoring` | feature、label、score、calibration、regime、strategy drift |
| Retraining Trigger | `kt.ai_feedback_governance.retraining_trigger` | 定期训练、漂移触发、样本阈值和禁止自动上线 |
| Recalibration Loop | `kt.ai_feedback_governance.recalibration_loop` | 再训练后概率校准、Brier、ECE、分组校准 |
| Champion Challenger | `kt.ai_feedback_governance.champion_challenger` | challenger 与 champion 的离线、shadow、paper 比较 |
| Shadow Paper Canary | `kt.ai_feedback_governance.shadow_paper_canary` | shadow、paper、soft gate、小流量 canary 阶段 |
| Rollback Governance | `kt.ai_feedback_governance.rollback_governance` | release manifest、rollback target、kill switch、审批记录 |
| LLM Prompt RAG SFT Loop | `kt.ai_feedback_governance.llm_prompt_rag_sft_loop` | LLM 优先 RAG/prompt，再考虑 SFT/LoRA |
| Feedback Loop Risk | `kt.ai_feedback_governance.feedback_loop_risk` | 自标注污染、反馈回路过拟合、自动化偏差 |

## 知识点规划

建议总量：36 条。

```text
P0-Core：18 条
P0-Extended：12 条
P1：6 条
```

### P0-Core 方向

```text
1. 所有 trade_candidate_snapshot 都必须记录，不只记录已成交交易。
2. 被 block、skip、human review 的候选也必须进入反馈池。
3. decision-time features、scorer output、LLM audit output、final gate decision 必须同链路保存。
4. 标签不能只使用 PnL，必须包含交易质量、规则违规、风控违规、执行质量和人工复核。
5. false allow cost 与 false block cost 必须进入标签和评估。
6. feature drift、label drift、score distribution drift、calibration drift 必须定期检查。
7. strategy version、symbol distribution、execution cost drift 必须进入交易 AI 的漂移监控。
8. 再训练只能产生 candidate_model，不得自动替换 champion_model。
9. 每次再训练后必须重新校准概率和阈值。
10. challenger 必须经过 offline、shadow、paper、soft-gate 验证。
11. hard gate 启用必须有人工审批和 release manifest。
12. 每次发布必须记录 dataset_hash、feature_schema_version、label_policy_version、model_version。
13. rollback_target 和 kill switch 必须在上线前存在。
14. LLM 持续改进优先 RAG 更新，其次 prompt 更新，最后才是 SFT/LoRA。
15. LLM SFT/LoRA 只在 eval 证明 schema、citation 或 reason-code 稳定失败时启用。
16. 人工复核修正必须进入 eval set，不得直接成为默认训练真值。
17. 自标注和模型反馈必须标注来源，避免反馈回路污染。
18. 持续学习指标不得只看 PnL，必须包含解释质量、引用完整率、坏交易拦截质量和人审成本。
```

## 输入契约

持续学习任务至少需要以下输入：

```text
trade_candidate_snapshot_id
decision_time_feature_schema_version
scorer_version
llm_audit_version
final_gate_policy_version
execution_or_block_result
post_trade_outcome_ref
human_review_ref
label_policy_version
dataset_version
strategy_version
symbol
market_regime
```

## 输出契约

持续学习知识和外接项目开发模板至少输出：

```text
feedback_record
label_update_record
drift_report
retraining_trigger_decision
candidate_model_manifest
calibration_report
threshold_policy_report
champion_challenger_report
shadow_paper_eval_report
release_manifest
rollback_plan
human_approval_record
```

## 业务流契约

```text
Candidate Trade
  -> Rule Gate
  -> Numeric Scorer
  -> LLM Audit Assistant
  -> Deterministic Final Gate
  -> Execution / Block / Human Review
  -> Outcome Logger
  -> Labeling Queue
  -> Dataset Builder
  -> Drift Monitor
  -> Retraining Pipeline
  -> Calibration Pipeline
  -> Shadow / Paper Eval
  -> Champion-Challenger Review
  -> Human Approval
  -> Approved Model Registry
  -> Controlled Deployment
  -> Rollback / Incident Review
```

## ML 与 LLM 分流

### ML Continuous Learning

```text
new trade candidates
  -> label update
  -> dataset version
  -> retrain numeric scorer
  -> recalibrate
  -> shadow/paper eval
  -> champion/challenger review
  -> promote or reject
```

关注：

```text
feature drift
label drift
score distribution drift
calibration drift
threshold stability
false allow / false block cost
regime robustness
```

### LLM Continuous Learning

```text
new audit cases
  -> human correction
  -> prompt eval set
  -> RAG knowledge update
  -> prompt update
  -> optional SFT/LoRA only when eval proves persistent failure
  -> LLM audit eval
```

关注：

```text
strict schema validity
reason code consistency
citation completeness
unsupported claim detection
no-source abstain
permission boundary
human review acceptance
```

## 边界范围

范围内：

```text
1. 持续学习、反馈治理、再训练、再校准、发布回滚知识规划。
2. AI Engineering 知识树 L3 专题补强。
3. 36 条知识点矩阵和采集队列。
4. 联网采集、候选生成、审计包、补证和 reviewed 沉淀任务规划。
5. MCP/SearchLab/KnowledgeTree/Vue3 对持续学习知识的只读检索和审计展示。
```

范围外：

```text
1. 不训练真实模型。
2. 不引入在线自动学习实盘模型。
3. 不让再训练模型自动上线。
4. 不把 LLM 设置为最终交易 gate。
5. 不采集 K 线、fill model、订单状态机、风控规则本体；这些归 Phase 37 / Trading Engineering。
6. 不修改 approved 状态语义。
7. 不引入数据库或外部 MLOps 平台，除非开发者另行确认。
```

## 涉及组件

```text
codex-expert-kit/rag/knowledge_tree.md
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/scripts/
codex-expert-kit/rag/candidates/
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/mcp/
codex-expert-kit/api/
ui/src/data/
ui/src/views/KnowledgeTreeView.vue
ui/src/views/SearchLab.vue
docs/contracts/
docs/research/
docs/audit/
docs/reports/
```

## 涉及数据结构

```text
TradeCandidateSnapshot
DecisionTimeFeatureRecord
ScorerOutputRecord
LlmAuditOutputRecord
FinalGateDecisionRecord
ExecutionOrBlockOutcome
PostTradeOutcome
HumanReviewRecord
LabelUpdateRecord
DatasetVersionManifest
DriftReport
RetrainingRunManifest
CalibrationReport
ChampionChallengerReport
ReleaseManifest
RollbackPlan
KnowledgeItem v1.1
ResearchIngestionTask
CandidateKnowledge
AI audit package
```

## 涉及存储

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

不新增数据库。若后续需要模型实验库、向量库、特征库、label store 或 release registry，必须另开 Phase 并由开发者确认。

## 实施步骤

```text
1. 创建 Phase 40 任务卡并更新索引。
2. 定义 `kt.ai_feedback_governance` 下的 L3 专题。
3. 写持续学习知识范围文档。
4. 写 feedback/dataset/label 数据契约。
5. 写 drift/retraining/recalibration 契约。
6. 写 champion/challenger/release/rollback 契约。
7. 创建 36 条知识点采集矩阵和 ResearchIngestionTask 队列。
8. 导出范围审计 JSON。
9. 审计通过后开始联网采集 P0-Core。
10. 生成候选知识、审计包、补证和 formal reviewed。
11. 重建索引和 Vue3 fixture。
12. 验证 MCP/SearchLab/KnowledgeTree 可命中、引用、阻断和降级。
13. 生成 Phase 40 验收报告。
```

## Definition of Done

```text
1. Phase 40 已登记到 docs/index_tasks.md。
2. docs/tasks/README.md 已登记 Phase 40。
3. Phase 40 任务卡存在，且包含上下游、契约、边界、DoD、测试。
4. 持续学习不等于在线自动学习的边界写清楚。
5. ML continuous learning 与 LLM continuous learning 分流写清楚。
6. 与 Trading Engineering 的边界写清楚。
7. 36 条知识点矩阵包含 priority、target_canonical_node_id、source_types、acceptance_gate。
8. 审计 JSON 能让外部 AI/人工先审计范围和边界。
9. 后续采集任务不允许无来源入库。
10. 中文文档保持 UTF-8，无乱码。
```

## 测试与验收

文档阶段：

```text
1. 检查任务卡存在。
2. 检查 docs/index_tasks.md 包含 Phase 40。
3. 检查 docs/tasks/README.md 包含 Phase 40。
4. 检查任务卡包含上下游、契约、边界、DoD、测试。
5. 运行 UTF-8/乱码门禁。
```

后续采集与入库阶段：

```text
python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
python codex-expert-kit/rag/scripts/validate_knowledge_tree_alignment.py
python -m pytest codex-expert-kit/mcp/tests
python -m pytest codex-expert-kit/api/tests
cd ui && npm run build
```

## 风险与回滚

| 风险 | 处理 |
| --- | --- |
| 把持续学习误解成实时在线学习 | 任务卡和知识卡硬写“再训练不得自动上线” |
| 把 Trading 规则本体塞进 AI Engineering | 只存学习治理知识，交易规则引用到 Trading Engineering |
| PnL-only 标签污染模型 | 标签契约强制多维标签和人审结果 |
| 自标注造成反馈回路污染 | 知识点必须覆盖 self-labeling risk 和 feedback-loop overfitting |
| challenger 过早替换 champion | 必须 offline/shadow/paper/canary 通过并人工审批 |
| LLM 越权成为最终 gate | LLM 只做审计助手，final gate 由确定性规则执行 |

回滚方式：

```text
1. 如果专题拆分过细，调整范围文档和任务卡，不删除已沉淀知识。
2. 如果候选分类错误，修正 candidate metadata 后重建 fixture。
3. 如果 formal reviewed 知识发现风险，降级 machine_gate 或 review_status，不直接删除。
4. 如果 MCP/Vue3 展示异常，回滚 fixture 或显示层，保留知识本体。
```

## 需要开发者确认的问题

```text
1. 是否确认 Phase 40 总量先按 36 条知识点规划？
2. 是否确认本 Phase 只规划和采集知识，不训练真实模型？
3. 是否确认不引入数据库、特征库、模型注册表等外部服务？
4. 是否确认 `kt.ai_feedback_governance` 是本 Phase 主归属节点？
```

当前用户已确认继续收集 Phase 40 尚未采集的知识点；CEK-TA-299 至 CEK-TA-317 已完成。CEK-TA-316 已将 18 条二审允许的候选沉淀为 formal reviewed；CEK-TA-317 已为 5 条仍需补证的候选补来源、补契约并导出三审 JSON。Phase 40 继续保持 `doing`，等待三审结果回写后再决定是否沉淀为 formal reviewed。

## CEK-TA-307 当前处理记录

2026-06-10 已导入外部严格审计结果：

```text
输入审计报告：C:\Users\dove\Downloads\phase40_candidate_audit_result_20260610_strict_v1.json
仓库审计副本：docs/audit/audit_result_phase40_p0_core_continuous_learning_20260610_strict_v1.json
导入报告：docs/reports/phase40_p0_core_audit_import_report.json
导入脚本：codex-expert-kit/rag/scripts/apply_phase40_p0_core_audit_result.py
前端候选 fixture：ui/src/data/phase23Candidates.ts
```

审计分流结果：

```text
accepted_for_draft：10
needs_more_evidence：5
rejected：3
rebuilt：3
```

重要边界：

```text
1. 本次审计结果所有条目 reviewed_allowed=false。
2. accepted_for_draft 只代表可进入 formal draft 准备队列，不等于 reviewed。
3. 本次未创建 formal reviewed 知识，未更新 approved，未允许 default guidance 或 hard gate。
4. 3 条 rejected 原候选因空 slug 污染风险保留为 rejected，并已重建为干净 ID 的补证候选。
5. 当时 CEK-TA-307 保持 doing，等待 needs_more_evidence 与 rebuilt 候选补证、二审通过后再沉淀 formal reviewed。
```

2026-06-10 已处理 8 条 needs_more_evidence 候选补证，并导出二审 JSON：

```text
补证脚本：codex-expert-kit/rag/scripts/supplement_phase40_p0_core_needs_evidence.py
补证报告：docs/reports/phase40_p0_core_supplemental_evidence_report.json
二审包：docs/audit/phase40_p0_core_supplemental_reaudit_package_20260610.json
前端候选 fixture：ui/src/data/phase23Candidates.ts
```

二审包范围：

```text
P40-C04
P40-C05
P40-C08
P40-C10-R1
P40-C11-R1
P40-C13
P40-C17
P40-C18-R1
```

补证后边界：

```text
1. 8 条仍然是 candidate，不是 formal reviewed。
2. 全部保持 default_guidance_allowed=false、hard_gate_allowed=false。
3. 二审可以返回 accepted_for_draft / needs_more_evidence / rejected，但不得直接 approved。
4. 只有二审明确 reviewed_allowed=true 后，才进入 formal reviewed draft 生成和索引重建。
```

2026-06-10 已处理 8 条补证候选的二审报告，并沉淀为 formal reviewed 知识：

```text
输入二审报告：C:\Users\dove\.codex\attachments\1f2219f5-6d04-44e5-9260-e7a30f472742\pasted-text.txt
仓库审计副本：docs/audit/audit_result_phase40_p0_core_supplemental_reaudit_20260610_v2.json
回写脚本：codex-expert-kit/rag/scripts/apply_phase40_supplemental_reaudit_result.py
回写报告：docs/reports/phase40_supplemental_reaudit_to_reviewed_report.json
正式知识目录：codex-expert-kit/rag/knowledge/KB_AI_18_FEEDBACK_GOVERNANCE/
正式知识索引：codex-expert-kit/rag/indexes/knowledge_items.json
前端正式知识 fixture：ui/src/data/formalKnowledgeItems.ts
前端候选 fixture：ui/src/data/phase23Candidates.ts
前端知识树 fixture：ui/src/data/knowledgeTreeNodes.ts
```

二审沉淀结果：

```text
formal reviewed：8
needs_more_evidence：0
rejected：0
approved：0
default_guidance_allowed：0
hard_gate_allowed：0
machine_gate：caveat_only
```

正式 reviewed 知识：

```text
kb_ai_feedback_governance.phase40.pnl.v1
kb_ai_feedback_governance.phase40.good_loss_bad_win.v1
kb_ai_feedback_governance.phase40.strategy_version_symbol_mix_market_regime_execution_cost_ai.v1
kb_ai_feedback_governance.phase40.retraining_trigger_audit_record.v1
kb_ai_feedback_governance.phase40.retrain_recalibration_threshold_reliability.v1
kb_ai_feedback_governance.phase40.challenger_offline_shadow_paper_soft_gate.v1
kb_ai_feedback_governance.phase40.sft_lora_eval_schema_citation_reason_code.v1
kb_ai_feedback_governance.phase40.feedback_loop_label_provenance.v1
```

验证结果：

```text
knowledge_items.json：181 条正式知识
formalKnowledgeItems.ts：181 条正式知识
phase23Candidates.ts：209 条候选
knowledgeTreeNodes.ts：69 个知识树节点
schema v1.1：pass
知识污染扫描：pass
candidate -> reviewed 工作流：pass
UTF-8/乱码门禁：pass
知识树对齐：pass
Vue3 build：pass
```

最终边界：

```text
1. 二审通过只允许沉淀 formal reviewed。
2. 8 条知识不得自动进入 approved。
3. 不允许 default guidance，也不允许 hard gate。
4. MCP/SearchLab/KnowledgeTree 后续只能按 reviewed + caveat_only 方式检索、引用和降级展示。
```

## CEK-TA-308 当前处理记录

2026-06-10 已完成 MCP/SearchLab/KnowledgeTree 联动验证：

```text
验证脚本：codex-expert-kit/rag/scripts/validate_phase40_runtime_linkage.py
验证报告：docs/reports/phase40_runtime_linkage_validation_report.json
验证范围：KB_AI_18_FEEDBACK_GOVERNANCE / kt.ai_feedback_governance
验证状态：pass
```

验证覆盖：

```text
1. 正式索引中 Phase 40 formal reviewed 知识数量为 8。
2. 8 条全部为 review_status=reviewed。
3. 8 条全部为 machine_gate.default_guidance=caveat_only。
4. 8 条全部归属 KB_AI_18_FEEDBACK_GOVERNANCE。
5. 知识树命中 kt.ai_feedback_governance 及 10 个 L3 专题节点。
6. API/SearchLab 风格 filter_items 可按持续学习子板块命中 reviewed 知识。
7. MCP search_expert_knowledge 可返回 reviewed/caveat_only 结果，并携带来源、引用、machine_gate 和 acceptance_level。
8. MCP default_guidance_only 会阻断 Phase 40 caveat_only 知识，不把 reviewed 当 approved。
9. MCP 写入或审批类权限请求会被拒绝。
```

测试结果：

```text
python codex-expert-kit/rag/scripts/validate_phase40_runtime_linkage.py：pass
python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py：pass
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py：pass
python codex-expert-kit/rag/scripts/validate_no_mojibake.py：pass
python codex-expert-kit/rag/scripts/validate_knowledge_tree_alignment.py：pass
python -m pytest codex-expert-kit/mcp/tests：27 passed
python -m pytest codex-expert-kit/api/tests：21 passed
cd ui && npm run build：pass
```

边界确认：

```text
1. 本任务只验证只读检索和审计展示链路。
2. 不开放 MCP 写知识、审批知识、交易、账户或密钥权限。
3. 不把 reviewed/caveat_only 结果提升为 approved/default guidance。
4. 不改变 SearchLab、MCP 或 KnowledgeTree 的权限语义。
```

## CEK-TA-310/311 当前处理记录

2026-06-10 已继续采集 Phase 40 尚未采集的 Batch D/E 知识点，并导出审计包：

```text
生成脚本：codex-expert-kit/rag/scripts/generate_phase40_extended_p1_candidates.py
导出脚本：codex-expert-kit/rag/scripts/export_phase40_extended_p1_audit_package.py
采集记录：docs/research/phase40_batch_d_e_research.md
生成报告：docs/reports/phase40_extended_p1_candidate_generation_report.md
生成质量门禁：docs/reports/phase40_extended_p1_generation_quality_gate.json
审计包：docs/audit/phase40_extended_p1_candidate_audit_package_20260610.json
审计质量门禁：docs/reports/phase40_extended_p1_candidate_quality_gate.json
候选目录：codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/
前端候选 fixture：ui/src/data/phase23Candidates.ts
前端知识树 fixture：ui/src/data/knowledgeTreeNodes.ts
```

采集结果：

```text
Batch D / P0-Extended：12 条
Batch E / P1：6 条
合计新增候选：18 条
当前候选总数：227 条
当前正式知识总数：181 条
```

新增候选范围：

```text
P40-E01 replayable audit trail
P40-E02 label policy version compatibility
P40-E03 drift root cause classification
P40-E04 incident retraining requires approval
P40-E05 calibration bins and coverage
P40-E06 challenger risk metrics
P40-E07 shadow/paper execution gap
P40-E08 rollback freezes artifacts
P40-E09 RAG update retrieval regression
P40-E10 human review audit trace
P40-E11 confidence is not evidence
P40-E12 continuous learning dashboard
P40-P01 long-tail feedback sampling
P40-P02 label conflict and gold set
P40-P03 scheduled and event retraining
P40-P04 rejected challenger reason tracking
P40-P05 composite artifact rollback
P40-P06 prompt/RAG/model eval separation
```

本轮来源族：

```text
Snowflake / MLflow / Google Data Cards
Fiddler / DataRobot / Arize
scikit-learn calibration / CalibrationDisplay
AWS SageMaker shadow tests / Microsoft shadow testing
Coalition for Secure AI / NIST AI RMF
Evidently / Google Cloud / Promptfoo / Arize RAG evaluation
Label Studio / IBM Watson Knowledge Studio
Long-tailed learning survey / tail sampling docs
```

测试结果：

```text
python codex-expert-kit/rag/scripts/generate_phase40_extended_p1_candidates.py：pass，18/18
python codex-expert-kit/rag/scripts/export_phase40_extended_p1_audit_package.py：pass，18/18
python codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py：pass，227 candidates
python codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py：pass，69 nodes
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py：pass
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py：pass
python codex-expert-kit/rag/scripts/validate_no_mojibake.py：pass
python codex-expert-kit/rag/scripts/validate_knowledge_tree_alignment.py：pass
cd ui && npm run build：pass
```

边界确认：

```text
1. 本轮 18 条全部是 candidate，不是 formal reviewed。
2. 不进入 approved，不允许 default guidance，不允许 hard gate。
3. 审计包要求外部 AI/人工只能返回 accepted_for_draft / needs_more_evidence / rejected。
4. 本轮没有采集 K 线、fill model、订单状态机、实盘风控阈值或交易所执行适配器本体知识。
5. 后续如果审计通过，仍需按 Phase 32 候选到 reviewed 工作流回写、补证、重建索引和运行时验证。
```

## CEK-TA-312 当前处理记录

2026-06-10 已导入 Phase 40 Batch D/E 严格审计结果：

```text
输入审计报告：C:\Users\dove\Downloads\phase40_extended_p1_batch_de_audit_result_20260610_strict_v1.json
仓库审计副本：docs/audit/audit_result_phase40_extended_p1_batch_de_20260610_strict_v1.json
导入脚本：codex-expert-kit/rag/scripts/apply_phase40_extended_p1_audit_result.py
导入报告：docs/reports/phase40_extended_p1_audit_import_report.json
前端候选 fixture：ui/src/data/phase23Candidates.ts
前端知识树 fixture：ui/src/data/knowledgeTreeNodes.ts
```

审计分流结果：

```text
accepted_for_draft：13
needs_more_evidence：5
rejected：0
formal reviewed created：0
approved created：0
default guidance allowed：0
hard gate allowed：0
```

已进入 needs_more_evidence 的 5 条：

```text
P40-E06 challenger risk metrics
P40-E07 shadow/paper execution gap
P40-E11 confidence is not evidence
P40-E12 continuous learning dashboard
P40-P05 composite artifact rollback
```

需要补证方向：

```text
1. P40-E06：补 false_allow_rate、false_block_cost、tail loss/drawdown、calibration、review load 和 execution-cost 引用字段；Trading 风险指标只引用 Phase 37，不在 AI Engineering 定义。
2. P40-E07：补 paper/replay 与真实执行差异来源，增加 fill_cost_assumption_ref、replay_engine_version、market_data_replay_policy_ref、execution_gap_report。
3. P40-E11：补 RAG faithfulness/groundedness、citation resolver、source attribution、hallucination/no-source abstain 来源。
4. P40-E12：补 false allow/block、human-review-cost、decision-cost monitoring 的 KPI/指标契约或专业来源。
5. P40-P05：补 model_version、prompt_version、rag_index_version、threshold_policy_version 组合 rollback unit 的 release manifest / composite artifact 来源或 CEK-TA 契约。
```

边界确认：

```text
1. accepted_for_draft 不是 reviewed，也不是 approved。
2. 本次审计报告全部 reviewed_allowed=false。
3. 13 条 accepted_for_draft 只进入 formal draft 准备队列。
4. 5 条 needs_more_evidence 需要补证后再次导出二审包。
5. 所有候选均设置 hidden_from_default_queue=true、visible_in_default_guidance_queue=false。
```

测试结果：

```text
python codex-expert-kit/rag/scripts/apply_phase40_extended_p1_audit_result.py：pass
python codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py：pass，227 candidates
python codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py：pass，69 nodes
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py：pass
python codex-expert-kit/rag/scripts/validate_no_mojibake.py：pass
python codex-expert-kit/rag/scripts/validate_knowledge_tree_alignment.py：pass
cd ui && npm run build：pass
```

## CEK-TA-313 当前处理记录

2026-06-10 已为 Phase 40 Batch D/E 的 5 条 `needs_more_evidence` 候选补充证据，并导出二审 JSON：

```text
补证脚本：codex-expert-kit/rag/scripts/supplement_phase40_extended_p1_needs_evidence.py
补证契约：docs/contracts/phase40_decision_cost_dashboard_metric_contract.md
补证契约：docs/contracts/phase40_composite_release_artifact_contract.md
补证报告：docs/reports/phase40_extended_p1_supplemental_evidence_report.json
二审包：docs/audit/phase40_extended_p1_supplemental_reaudit_package_20260610.json
前端候选 fixture：ui/src/data/phase23Candidates.ts
前端知识树 fixture：ui/src/data/knowledgeTreeNodes.ts
```

补证范围：

```text
P40-E06 challenger risk metrics：补 decision-cost、false allow/block、calibration、人审成本和 execution_cost_ref 证据。
P40-E07 shadow/paper execution gap：补 shadow testing、paper simulator、fill model、paper/live 差异和 release contract 证据。
P40-E11 confidence not evidence：补 RAG faithfulness、grounding、citation、unsupported claim 和 retrieval/generation eval 证据。
P40-E12 continuous learning dashboard：补 drift、calibration、decision cost、人审成本和 dashboard metric schema 证据。
P40-P05 composite artifact rollback：补 CompositeReleaseUnit、CompositeRollbackTarget、MLflow registry、RAG eval 和 AI RMF manage 证据。
```

补证结果：

```text
候选补证数量：5
质量门禁：pass
二审包候选数量：5
formal reviewed created：0
approved created：0
default guidance allowed：0
hard gate allowed：0
```

重要边界：

```text
1. 本次补证后 5 条仍然是 candidate，不是 formal reviewed。
2. 二审可以返回 accepted_for_draft / needs_more_evidence / rejected。
3. 二审不得直接写 approved、default guidance 或 hard gate。
4. AI Engineering 只记录 Trading Engineering 引用字段，不定义 K 线、fill model、订单状态机、实盘风控或交易执行本体。
5. 内部 CEK-TA 契约只补字段和工作流边界，外部来源仍用于支撑通用方法。
```

验证结果：

```text
python codex-expert-kit/rag/scripts/supplement_phase40_extended_p1_needs_evidence.py：pass，5/5
python codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py：pass，227 candidates
python codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py：pass，69 nodes
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py：pass
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py：pass
python codex-expert-kit/rag/scripts/validate_no_mojibake.py：pass，597 files
python codex-expert-kit/rag/scripts/validate_knowledge_tree_alignment.py：pass
cd ui && npm run build：pass，存在 Vite 大 chunk 警告，不影响本任务
```

## CEK-TA-314 当前处理记录

2026-06-10 已导入 Phase 40 Batch D/E 补证二审结果，并将 5 条候选沉淀为 formal reviewed 知识：

```text
输入二审报告：C:\Users\dove\.codex\attachments\cd7ce66f-d73d-45cd-919c-b62d9af72320\pasted-text.txt
仓库审计副本：docs/audit/audit_result_phase40_extended_p1_supplemental_reaudit_20260610_strict_v2.json
回写脚本：codex-expert-kit/rag/scripts/apply_phase40_extended_p1_supplemental_reaudit_result.py
回写报告：docs/reports/phase40_extended_p1_supplemental_reaudit_to_reviewed_report.json
正式知识目录：codex-expert-kit/rag/knowledge/KB_AI_18_FEEDBACK_GOVERNANCE/
正式知识索引：codex-expert-kit/rag/indexes/knowledge_items.json
前端正式知识 fixture：ui/src/data/formalKnowledgeItems.ts
前端候选 fixture：ui/src/data/phase23Candidates.ts
前端知识树 fixture：ui/src/data/knowledgeTreeNodes.ts
```

二审沉淀结果：

```text
formal reviewed：5
needs_more_evidence：0
rejected：0
approved：0
default_guidance_allowed：0
hard_gate_allowed：0
machine_gate：caveat_only
正式知识总数：186
候选总数：227
Phase 40 formal reviewed 总数：13
```

新增 formal reviewed 知识：

```text
kb_ai_feedback_governance.phase40.challenger_risk_metrics.v1
kb_ai_feedback_governance.phase40.shadow_paper_execution_gap.v1
kb_ai_feedback_governance.phase40.confidence_not_evidence.v1
kb_ai_feedback_governance.phase40.continuous_learning_dashboard.v1
kb_ai_feedback_governance.phase40.composite_artifact_rollback.v1
```

知识树归类：

```text
kt.ai_feedback_governance.champion_challenger：+1
kt.ai_feedback_governance.shadow_paper_canary：+1
kt.ai_feedback_governance.feedback_loop_risk：+1
kt.ai_feedback_governance.drift_monitoring：+1
kt.ai_feedback_governance.rollback_governance：+1
```

边界确认：

```text
1. 二审通过只允许沉淀 formal reviewed。
2. 5 条知识不得自动进入 approved。
3. 5 条知识不得进入 default guidance，也不得启用 hard gate。
4. MCP/SearchLab/KnowledgeTree 只能以 reviewed + caveat_only 方式检索、引用和降级展示。
5. AI Engineering 只保留 Trading Engineering 引用字段和治理规则，不定义 K 线、fill model、订单状态机、实盘风控或交易执行本体。
```

验证结果：

```text
python codex-expert-kit/rag/scripts/apply_phase40_extended_p1_supplemental_reaudit_result.py：pass，5/5
python codex-expert-kit/rag/scripts/build_knowledge_items_index.py：pass，186 items
python codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py：pass，186 formal knowledge items
python codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py：pass，227 candidates
python codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py：pass，69 nodes
python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py：pass
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py：pass
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py：pass
python codex-expert-kit/rag/scripts/validate_no_mojibake.py：pass
python codex-expert-kit/rag/scripts/validate_knowledge_tree_alignment.py：pass
python codex-expert-kit/rag/scripts/validate_phase40_runtime_linkage.py：pass，Phase 40 reviewed count 13
python -m pytest codex-expert-kit/mcp/tests：27 passed
python -m pytest codex-expert-kit/api/tests：21 passed
cd ui && npm run build：pass，存在 Vite 大 chunk 警告，不影响本任务
```

## CEK-TA-309 当前处理记录

2026-06-10 已生成 Phase 40 验收与缺口报告：

```text
验收报告：docs/reports/phase40_ai_continuous_learning_retraining_loop_report.md
验收结论：阶段能力已跑通，但 Phase 40 不能标记为完全完成，需继续处理 CEK-TA-315。
```

验收通过部分：

```text
正式知识总数：186
Phase 40 formal reviewed：13
Phase 40 machine_gate=caveat_only：13
MCP/SearchLab/KnowledgeTree 联动验证：pass
候选到 reviewed 工作流门禁：pass
知识污染扫描：pass
UTF-8/乱码门禁：pass
API/MCP 测试：pass
Vue3 build：pass
```

验收发现的缺口：

```text
23 条 Phase 40 候选处于 ai_passed / accepted_for_draft。
这 23 条候选有 proposed formal_knowledge_id。
knowledge_items.json 中不存在对应 knowledge_id。
它们的 review.ai_audit.reviewed_allowed=false。
因此不能直接沉淀 formal reviewed。
```

后续处理：

```text
新增 CEK-TA-315：导出 23 条 ai_passed 候选的 reviewed preparation 二审包。
只有二审明确 reviewed_allowed=true 后，才能生成 formal reviewed 并重建索引。
Phase 40 在 CEK-TA-315 处理前继续保持 doing。
```

## CEK-TA-315 当前处理记录

2026-06-10 已导出 Phase 40 `ai_passed` 候选的 reviewed preparation 二审包：

```text
导出脚本：codex-expert-kit/rag/scripts/export_phase40_ai_passed_reviewed_preparation_package.py
二审包：docs/audit/phase40_ai_passed_reviewed_preparation_audit_package_20260610.json
缺口报告：docs/reports/phase40_ai_passed_reviewed_preparation_gap_report.json
```

导出范围：

```text
候选数量：23
queue_group：ai_passed
ingestion_decision：accepted_for_draft
review.ai_audit.reviewed_allowed：false
proposed formal_knowledge_id：存在
knowledge_items.json 对应 knowledge_id：不存在
```

质量门禁：

```text
candidate_count：23 / 23
queue_group_ai_passed：pass
accepted_for_draft_only：pass
reviewed_allowed_false_before_reaudit：pass
source_refs_min_2：pass
conflict_status_safe：pass
canonical_nodes_under_feedback_governance：pass
failure_count：0
gate_status：pass
```

知识树分布：

```text
kt.ai_feedback_governance.feedback_logging：5
kt.ai_feedback_governance.label_refresh：3
kt.ai_feedback_governance.retraining_trigger：3
kt.ai_feedback_governance.llm_prompt_rag_sft_loop：3
kt.ai_feedback_governance.drift_monitoring：2
kt.ai_feedback_governance.recalibration_loop：2
kt.ai_feedback_governance.rollback_governance：2
kt.ai_feedback_governance.champion_challenger：1
kt.ai_feedback_governance.shadow_paper_canary：1
kt.ai_feedback_governance.feedback_loop_risk：1
```

边界确认：

```text
1. 本任务只导出二审包和缺口报告。
2. 本任务不修改候选状态，不创建 formal reviewed，不重建正式知识索引。
3. accepted_for_draft 仍不等于 reviewed。
4. 外部二审必须显式返回 reviewed_allowed=true，Codex 才能继续执行候选到 formal reviewed 的沉淀任务。
5. 二审通过后也只能进入 reviewed + caveat_only，不得自动 approved、default guidance 或 hard gate。
```

## CEK-TA-316 当前处理记录

2026-06-10 已导入 Phase 40 reviewed preparation 二审结果：

```text
输入审计报告：C:\Users\dove\Downloads\audit_result_phase40_ai_passed_reviewed_preparation_20260610_strict_v1.json
仓库审计副本：docs/audit/audit_result_phase40_ai_passed_reviewed_preparation_20260610_strict_v1.json
导入脚本：codex-expert-kit/rag/scripts/apply_phase40_ai_passed_reviewed_preparation_result.py
导入报告：docs/reports/phase40_ai_passed_reviewed_preparation_import_report.json
正式知识目录：codex-expert-kit/rag/knowledge/KB_AI_18_FEEDBACK_GOVERNANCE/
正式知识索引：codex-expert-kit/rag/indexes/knowledge_items.json
前端正式知识 fixture：ui/src/data/formalKnowledgeItems.ts
前端候选 fixture：ui/src/data/phase23Candidates.ts
前端知识树 fixture：ui/src/data/knowledgeTreeNodes.ts
```

二审处理结果：

```text
reviewed_allowed=true：18
needs_more_evidence：5
rejected：0
approved：0
default_guidance_allowed：0
hard_gate_allowed：0
正式知识总数：204
Phase 40 formal reviewed 总数：31
候选总数：227
```

新增 formal reviewed 知识：

```text
kb_ai_feedback_governance.phase40.opportunity_cost.v1
kb_ai_feedback_governance.phase40.false_allow_cost_false_block_cost.v1
kb_ai_feedback_governance.phase40.candidate_model_champion_model.v1
kb_ai_feedback_governance.phase40.hard_gate_canary.v1
kb_ai_feedback_governance.phase40.llm_rag_prompt_sft_lora.v1
kb_ai_feedback_governance.phase40.replayable_audit_trail.v1
kb_ai_feedback_governance.phase40.label_policy_version_compatibility.v1
kb_ai_feedback_governance.phase40.drift_root_cause_classification.v1
kb_ai_feedback_governance.phase40.incident_retraining_requires_approval.v1
kb_ai_feedback_governance.phase40.calibration_bins_coverage.v1
kb_ai_feedback_governance.phase40.rollback_freezes_artifacts.v1
kb_ai_feedback_governance.phase40.rag_update_retrieval_regression.v1
kb_ai_feedback_governance.phase40.human_review_audit_trace.v1
kb_ai_feedback_governance.phase40.long_tail_feedback_sampling.v1
kb_ai_feedback_governance.phase40.label_conflict_gold_set.v1
kb_ai_feedback_governance.phase40.scheduled_event_retraining.v1
kb_ai_feedback_governance.phase40.rejected_challenger_reason_tracking.v1
kb_ai_feedback_governance.phase40.prompt_rag_model_eval_separation.v1
```

仍需补证的 5 条：

```text
P40-C01 allow_block_skip_human_review：补 logged bandit / OPE source 或 Phase40 feedback dataset contract。
P40-C02 feedback_record_scorer_llm_final_gate：补 point-in-time / decision-time feature contract 或 FeedbackRecord schema contract。
P40-C07 feature_drift_label_drift_score_distribution_drift_calibration_drift：补 calibration curve / reliability diagram / probability calibration 来源。
P40-C12 threshold_policy：补 review budget / queue capacity / human review load policy contract。
P40-C15 release_manifest_rollback_target_kill_switch：补 kill switch、rollback drill、secret scan、SRE 或 trading-control 来源/契约。
```

验证结果：

```text
python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py：pass，204 items
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py：pass
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py：pass
python codex-expert-kit/rag/scripts/validate_no_mojibake.py：pass
python codex-expert-kit/rag/scripts/validate_knowledge_tree_alignment.py：pass
python codex-expert-kit/rag/scripts/validate_phase40_runtime_linkage.py：pass，Phase 40 reviewed count 31
python -m pytest codex-expert-kit/mcp/tests：27 passed
python -m pytest codex-expert-kit/api/tests：21 passed
cd ui && npm run build：pass，存在 Vite 大 chunk 警告，不影响本任务
```

边界确认：

```text
1. 二审通过的 18 条只进入 formal reviewed + caveat_only。
2. 18 条知识不得自动进入 approved。
3. 18 条知识不得进入 default guidance，也不得启用 hard gate。
4. 5 条 needs_more_evidence 仍然是 candidate，不进入正式知识索引。
5. AI Engineering 仍只保留学习治理、证据链、评估、发布和回滚边界；Trading Engineering 本体保持跨分支引用。
```

## CEK-TA-317 当前处理记录

2026-06-10 已为 reviewed preparation 二审后仍需补证的 5 条候选完成补证并导出三审包。

输入范围：

```text
P40-C01 allow_block_skip_human_review
P40-C02 feedback_record_scorer_llm_final_gate
P40-C07 feature_drift_label_drift_score_distribution_drift_calibration_drift
P40-C12 threshold_policy
P40-C15 release_manifest_rollback_target_kill_switch
```

新增契约：

```text
docs/contracts/phase40_review_budget_threshold_policy_contract.md
docs/contracts/phase40_release_manifest_kill_switch_contract.md
```

交付物：

```text
codex-expert-kit/rag/scripts/supplement_phase40_reviewed_preparation_needs_evidence.py
docs/research/phase40_reviewed_preparation_supplemental_research.md
docs/reports/phase40_reviewed_preparation_supplemental_evidence_report.json
docs/audit/phase40_reviewed_preparation_supplemental_reaudit_package_20260610.json
ui/src/data/phase23Candidates.ts
ui/src/data/knowledgeTreeNodes.ts
```

补证结果：

```text
P40-C01：补 Vowpal Wabbit contextual bandit、Open Bandit Pipeline、Doubly Robust Policy Evaluation、CEK-TA Feedback Dataset Contract。
P40-C02：补 Feast point-in-time joins、Tecton training data、Databricks point-in-time feature joins、CEK-TA Feedback Dataset Contract。
P40-C07：补 scikit-learn Probability calibration、Calibration curves、CalibrationDisplay、CEK-TA Drift Retraining Recalibration Contract。
P40-C12：补 Amazon A2I human review workflow、Review Budget Threshold Policy Contract、ThresholdStabilityReport 契约。
P40-C15：补 Google SRE canarying、GitHub secret scanning、NIST AI RMF Manage、FCA algorithmic trading controls、Release Manifest Kill Switch Contract。
```

质量门禁：

```text
补证候选数：5
三审包候选数：5
source_refs 下限：>= 6
formal reviewed 创建数：0
approved 创建数：0
default_guidance_allowed：false
hard_gate_allowed：false
gate_status：pass
```

边界确认：

```text
1. CEK-TA-317 只补 candidate 来源和契约，不创建 formal reviewed。
2. 三审可以返回 accepted_for_draft / needs_more_evidence / rejected。
3. 即使三审通过，后续也只能由 Codex 生成 formal reviewed + caveat_only，不得直接 approved。
4. Trading Engineering 的 K 线、fill model、订单状态机、实盘风控和交易执行本体不得混入 AI Engineering。
```

## CEK-TA-328 当前处理记录

2026-06-10 已导入 Phase 40 reviewed preparation 补证三审结果，并将 5 条三审通过候选沉淀为 formal reviewed 知识。

输入范围：

```text
P40-C01 allow_block_skip_human_review
P40-C02 feedback_record_scorer_llm_final_gate
P40-C07 feature_drift_label_drift_score_distribution_drift_calibration_drift
P40-C12 threshold_policy
P40-C15 release_manifest_rollback_target_kill_switch
```

交付物：

```text
codex-expert-kit/rag/scripts/apply_phase40_reviewed_preparation_supplemental_reaudit_result.py
docs/audit/audit_result_phase40_reviewed_preparation_supplemental_reaudit_20260610_strict_v1.json
docs/reports/phase40_reviewed_preparation_supplemental_reaudit_import_report.json
codex-expert-kit/rag/knowledge/KB_AI_18_FEEDBACK_GOVERNANCE/
codex-expert-kit/rag/indexes/knowledge_items.json
ui/src/data/phase23Candidates.ts
ui/src/data/formalKnowledgeItems.ts
ui/src/data/knowledgeTreeNodes.ts
docs/reports/phase40_runtime_linkage_validation_report.json
```

沉淀结果：

```text
新增 formal reviewed：5
Phase 40 formal reviewed 总数：36
正式知识总数：209
needs_more_evidence：0
rejected：0
approved：0
default_guidance_allowed：0
hard_gate_allowed：0
machine_gate：全部 caveat_only
```

新增 formal reviewed 知识：

```text
kb_ai_feedback_governance.phase40.allow_block_skip_human_review.v1
kb_ai_feedback_governance.phase40.feedback_record_scorer_llm_final_gate.v1
kb_ai_feedback_governance.phase40.feature_drift_label_drift_score_distribution_drift_calibration_drift.v1
kb_ai_feedback_governance.phase40.threshold_policy.v1
kb_ai_feedback_governance.phase40.release_manifest_rollback_target_kill_switch.v1
```

质量门禁：

```text
python codex-expert-kit/rag/scripts/build_knowledge_items_index.py：pass，209 items
python codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py：pass，227 candidates
python codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py：pass，209 formal knowledge items
python codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py：pass，69 knowledge tree nodes
python codex-expert-kit/rag/scripts/validate_phase40_runtime_linkage.py：pass，Phase 40 reviewed count 36
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py：pass
python codex-expert-kit/rag/scripts/validate_no_mojibake.py：pass
python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py：pass，209 items
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py：pass
python -m pytest codex-expert-kit/mcp/tests：27 passed
python -m pytest codex-expert-kit/api/tests：21 passed
cd ui && npm run build：pass，存在 Vite 大 chunk 警告，不影响本任务
```

边界确认：

```text
1. 三审通过的 5 条只进入 formal reviewed + caveat_only。
2. 5 条知识不得自动进入 approved。
3. 5 条知识不得进入 default guidance，也不得启用 hard gate。
4. 候选源文件保留审计追踪，并回链 formal knowledge。
5. AI Engineering 只记录持续学习、反馈、漂移、阈值和发布治理；Trading Engineering 本体保持跨分支引用。
```

## 状态更新要求

完成任一任务后必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase40_ai_continuous_learning_retraining_loop.md
相关 contracts/research/audit/reports 文档
```
