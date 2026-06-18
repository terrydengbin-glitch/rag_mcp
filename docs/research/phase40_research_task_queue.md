# Phase 40 ResearchIngestionTask 队列

生成日期：2026-06-10
状态：queue draft
对应任务：CEK-TA-303

## 队列目标

本队列承接 `docs/research/phase40_continuous_learning_collection_matrix.md`，用于后续 CEK-TA-305 联网采集 Phase 40 持续学习知识来源并生成候选知识包。

## 执行顺序

```text
Batch A: P0-Core / feedback logging + label refresh
Batch B: P0-Core / drift + retraining + recalibration
Batch C: P0-Core / champion/challenger + shadow/paper/canary + rollback + LLM loop + feedback risk
Batch D: P0-Extended
Batch E: P1
```

## 通用 ResearchIngestionTask 契约

```yaml
task_id: string
matrix_ids: list[string]
priority: P0 | P1
target_canonical_nodes: list[string]
objective: string
required_source_types: list[string]
search_queries: list[string]
expected_candidates: integer
acceptance_gate: string
blocked_if: list[string]
outputs:
  research_notes: string
  candidate_json: string
  quality_gate_report: string
```

## Batch A：反馈日志与标签刷新

```yaml
task_id: P40-RIT-A-feedback-label-core
matrix_ids: [P40-C01, P40-C02, P40-C03, P40-C04, P40-C05, P40-C06]
priority: P0
target_canonical_nodes:
  - kt.ai_feedback_governance.feedback_logging
  - kt.ai_feedback_governance.label_refresh
objective: 采集所有候选记录、决策日志、反事实/阻断候选边界、多维标签和 false allow/block 成本相关专业资料。
required_source_types: [official_doc, paper, framework_doc, engineering_article]
search_queries:
  - model monitoring log all predictions rejected decisions
  - prediction logging feature snapshot model output audit trail
  - logged bandit feedback rejected actions counterfactual evaluation
  - multi dimensional labels model quality human review labels
  - reward hacking noisy labels outcome bias trading review
  - false positive false negative cost sensitive threshold decision
expected_candidates: 6
acceptance_gate: 每条候选至少 2 个来源，必须阻断 PnL-only label 和 allow-only logging。
blocked_if:
  - 只记录成交交易
  - 把 post-trade outcome 当作 decision-time feature
  - 把 LLM 输出当作标签真值
outputs:
  research_notes: docs/research/phase40_batch_a_feedback_label_research.md
  candidate_json: codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/
  quality_gate_report: docs/reports/phase40_batch_a_quality_gate.json
```

## Batch B：漂移、再训练触发、再校准

```yaml
task_id: P40-RIT-B-drift-retraining-recalibration-core
matrix_ids: [P40-C07, P40-C08, P40-C09, P40-C10, P40-C11, P40-C12]
priority: P0
target_canonical_nodes:
  - kt.ai_feedback_governance.drift_monitoring
  - kt.ai_feedback_governance.retraining_trigger
  - kt.ai_feedback_governance.recalibration_loop
objective: 采集漂移类型分离、交易 AI 切片监控、retrain != promote、再校准、成本阈值和人工复核预算相关专业资料。
required_source_types: [official_doc, paper, framework_doc, engineering_article]
search_queries:
  - feature drift label drift prediction drift calibration drift
  - model monitoring segment drift regime drift execution cost drift
  - candidate model champion challenger model registry approval
  - retraining trigger dataset version approval audit
  - probability calibration after retraining brier ece reliability
  - decision threshold cost matrix review capacity
expected_candidates: 6
acceptance_gate: 必须明确漂移报警不等于自动再训练，再训练不等于上线，再训练后必须重新校准。
blocked_if:
  - 只有 drift 总分没有类型分离
  - 再训练后自动替换 champion
  - 阈值固定 0.5 且无成本策略
outputs:
  research_notes: docs/research/phase40_batch_b_drift_retraining_recalibration_research.md
  candidate_json: codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/
  quality_gate_report: docs/reports/phase40_batch_b_quality_gate.json
```

## Batch C：晋级、灰度、回滚、LLM 持续改进和反馈风险

```yaml
task_id: P40-RIT-C-release-llm-risk-core
matrix_ids: [P40-C13, P40-C14, P40-C15, P40-C16, P40-C17, P40-C18]
priority: P0
target_canonical_nodes:
  - kt.ai_feedback_governance.champion_challenger
  - kt.ai_feedback_governance.shadow_paper_canary
  - kt.ai_feedback_governance.rollback_governance
  - kt.ai_feedback_governance.llm_prompt_rag_sft_loop
  - kt.ai_feedback_governance.feedback_loop_risk
objective: 采集 challenger 晋级、shadow/paper/canary、release manifest、rollback、LLM RAG/prompt/SFT 顺序和反馈回路污染相关资料。
required_source_types: [official_doc, paper, framework_doc, engineering_article]
search_queries:
  - champion challenger shadow deployment model validation
  - canary release stop condition model deployment guardrail
  - release manifest rollback kill switch model deployment approval
  - RAG update prompt evaluation fine tuning trigger
  - when to fine tune LLM eval schema citation reason code
  - feedback loop bias self training selective labels model generated labels
expected_candidates: 6
acceptance_gate: 必须明确 challenger/shadow/paper/canary 都不是自动上线许可，LLM 不能成为 final gate。
blocked_if:
  - 缺少 rollback target
  - LLM 直接决定交易 allow/block
  - 用模型生成标签训练自身
outputs:
  research_notes: docs/research/phase40_batch_c_release_llm_risk_research.md
  candidate_json: codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/
  quality_gate_report: docs/reports/phase40_batch_c_quality_gate.json
```

## Batch D：P0-Extended

```yaml
task_id: P40-RIT-D-extended
matrix_ids: [P40-E01, P40-E02, P40-E03, P40-E04, P40-E05, P40-E06, P40-E07, P40-E08, P40-E09, P40-E10, P40-E11, P40-E12]
priority: P0
target_canonical_nodes:
  - kt.ai_feedback_governance.feedback_logging
  - kt.ai_feedback_governance.label_refresh
  - kt.ai_feedback_governance.drift_monitoring
  - kt.ai_feedback_governance.retraining_trigger
  - kt.ai_feedback_governance.recalibration_loop
  - kt.ai_feedback_governance.champion_challenger
  - kt.ai_feedback_governance.shadow_paper_canary
  - kt.ai_feedback_governance.rollback_governance
  - kt.ai_feedback_governance.llm_prompt_rag_sft_loop
  - kt.ai_feedback_governance.feedback_loop_risk
objective: 补齐 replayable audit trail、标签策略兼容、drift root cause、事故触发、可靠性分桶、风险指标、shadow/paper 限制、artifact freeze、RAG 回归评测、人审审计、confidence 边界和监控看板。
required_source_types: [official_doc, paper, framework_doc, engineering_article]
search_queries:
  - replayable audit trail prediction log lineage
  - label policy version dataset migration compatibility
  - drift root cause data quality concept drift version change
  - incident retraining approval model governance
  - reliability diagram calibration bins sample coverage
  - model validation risk metric challenger evaluation
  - shadow mode paper trading limitations execution difference
  - model rollback freeze artifact incident response
  - RAG evaluation regression retrieval test set
  - human label audit reviewer reason conflict
  - model confidence not evidence uncertainty audit
  - model monitoring dashboard calibration drift review cost
expected_candidates: 12
acceptance_gate: 每条必须能补强 P0-Core 的治理闭环，不能引入自动上线或 Trading 本体知识。
blocked_if:
  - 只提供产品营销材料
  - 没有可执行字段或门禁
  - 与 Phase 40 三份契约冲突
outputs:
  research_notes: docs/research/phase40_batch_d_extended_research.md
  candidate_json: codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/
  quality_gate_report: docs/reports/phase40_batch_d_quality_gate.json
```

## Batch E：P1 增强项

```yaml
task_id: P40-RIT-E-p1-enhancement
matrix_ids: [P40-P01, P40-P02, P40-P03, P40-P04, P40-P05, P40-P06]
priority: P1
target_canonical_nodes:
  - kt.ai_feedback_governance.feedback_logging
  - kt.ai_feedback_governance.label_refresh
  - kt.ai_feedback_governance.retraining_trigger
  - kt.ai_feedback_governance.champion_challenger
  - kt.ai_feedback_governance.rollback_governance
  - kt.ai_feedback_governance.llm_prompt_rag_sft_loop
objective: 采集长尾覆盖、标签仲裁、混合再训练触发、拒绝实验追踪、组合回滚和 LLM 三类回归评测增强知识。
required_source_types: [official_doc, paper, framework_doc, engineering_article]
search_queries:
  - long tail monitoring sampling low frequency class
  - label conflict adjudication gold set regression
  - scheduled retraining event driven retraining
  - experiment tracking rejected model reason
  - rollback model prompt RAG threshold composite release
  - prompt regression RAG regression model eval separation
expected_candidates: 6
acceptance_gate: P1 只做增强，不阻塞 P0-Core 采集和审计。
blocked_if:
  - 与 P0-Core 重复且无新增治理价值
  - 不能落到 Phase 40 L3 节点
outputs:
  research_notes: docs/research/phase40_batch_e_p1_research.md
  candidate_json: codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/
  quality_gate_report: docs/reports/phase40_batch_e_quality_gate.json
```

## 执行门禁

```text
1. 每个 Batch 执行前必须确认 matrix_ids 全部存在于采集矩阵。
2. 每个候选知识必须带 target_canonical_node_id。
3. 每个候选知识必须带 source_evidence。
4. 每个候选知识必须带 applies_when / not_applicable_when。
5. 每个候选知识必须通过 no-mojibake 和污染门禁。
6. 每个候选知识必须声明不是 approved，不得直接进入默认指导。
```

## CEK-TA-303 DoD

```text
1. 本队列文件存在。
2. 36 条知识点被拆成 5 个 Batch。
3. 每个 Batch 有 task_id、matrix_ids、priority、target_canonical_nodes、objective、search_queries、acceptance_gate 和 outputs。
4. 队列能被 CEK-TA-305 直接消费。
5. 队列不包含 Trading Engineering 本体采集。
```
