# Phase 40 Continuous Learning 知识点采集矩阵

生成日期：2026-06-10
状态：collection matrix draft
对应任务：CEK-TA-303

## 目标

本文把 Phase 40 的 36 条持续学习知识点拆成可联网采集、可审计、可生成候选知识卡的矩阵。后续 CEK-TA-305 按本文执行联网采集，CEK-TA-306 导出 AI 审计包。

## 总量

```text
总计：36 条
P0-Core：18 条
P0-Extended：12 条
P1：6 条
主归属：kt.ai_feedback_governance / KB_AI_18_FEEDBACK_GOVERNANCE
```

## 通用采集门槛

每条候选知识必须满足：

```text
1. 至少 2 个来源，优先官方文档、论文、框架文档、工程案例。
2. 必须声明 applies_when 和 not_applicable_when。
3. 必须声明不能自动上线、不能让 LLM 作为最终交易 gate。
4. 必须能回链到 Phase 40 三份契约之一。
5. 涉及执行、风控、K 线、fill model 本体时只做引用，路由到 Trading Engineering。
6. 候选知识默认 candidate_ready，不直接 approved。
```

## P0-Core 采集矩阵

| ID | 优先级 | canonical node | 知识点 | 推荐来源类型 | 搜索方向 | 接受门槛 |
| --- | --- | --- | --- | --- | --- | --- |
| P40-C01 | P0 | `kt.ai_feedback_governance.feedback_logging` | 所有交易候选都必须记录，包括 allow、block、skip 和 human_review | MLOps official doc, model monitoring doc, engineering article | model monitoring log all predictions decision logs blocked decisions | 明确 all predictions / rejected decisions 也要记录 |
| P40-C02 | P0 | `kt.ai_feedback_governance.feedback_logging` | feedback record 必须保存决策时特征、scorer 输出、LLM 审计输出、final gate 决策和后验结果引用 | feature store doc, model monitoring doc, audit logging doc | prediction logging feature snapshot model output decision audit trail | 能支持可回放 audit trail |
| P40-C03 | P0 | `kt.ai_feedback_governance.feedback_logging` | 被阻断候选也必须保留 opportunity-cost 评估入口，避免只学习已成交样本 | off-policy evaluation paper, counterfactual logging doc | logged bandit feedback rejected actions counterfactual evaluation | 明确 blocked/skipped 样本的反事实边界 |
| P40-C04 | P0 | `kt.ai_feedback_governance.label_refresh` | 标签不能只用 PnL，必须覆盖交易质量、规则违规、风控违规、执行质量和人工复核 | model risk doc, labeling guideline, trading AI eval doc | multi dimensional labels model quality human review labels | 明确 PnL-only label 风险 |
| P40-C05 | P0 | `kt.ai_feedback_governance.label_refresh` | good loss 与 bad win 必须进入标签复核，防止模型学习错误激励 | trading evaluation article, reinforcement learning reward hacking, model risk doc | reward hacking noisy labels outcome bias trading review | 能解释结果好坏不等于决策质量 |
| P40-C06 | P0 | `kt.ai_feedback_governance.label_refresh` | false allow cost 与 false block cost 必须进入评估和阈值决策 | cost-sensitive learning paper, threshold policy doc | false positive false negative cost sensitive threshold decision | 明确 false allow/block 成本矩阵 |
| P40-C07 | P0 | `kt.ai_feedback_governance.drift_monitoring` | feature drift、label drift、score distribution drift 和 calibration drift 必须分开监控 | ML monitoring official doc, data drift paper, calibration doc | feature drift label drift prediction drift calibration drift | 不允许只用一个 drift 总分 |
| P40-C08 | P0 | `kt.ai_feedback_governance.drift_monitoring` | strategy version、symbol mix、market regime 和 execution cost 漂移必须纳入交易 AI 监控 | model monitoring doc, trading system doc, model risk doc | model monitoring segment drift regime drift execution cost drift | 能说明交易 AI 切片维度 |
| P40-C09 | P0 | `kt.ai_feedback_governance.retraining_trigger` | 再训练只能生成 candidate model，不得自动替换 champion model | MLOps release doc, model registry doc, champion challenger doc | candidate model champion challenger model registry approval | 明确 retrain != promote |
| P40-C10 | P0 | `kt.ai_feedback_governance.retraining_trigger` | 再训练触发必须记录触发原因、样本窗口、数据版本和审批状态 | ML pipeline doc, model card/dataset card doc | retraining trigger dataset version approval audit | 有 trigger decision 字段证据 |
| P40-C11 | P0 | `kt.ai_feedback_governance.recalibration_loop` | 每次再训练后必须重新校准概率、阈值和分组可靠性 | calibration paper, sklearn calibration doc, model monitoring doc | probability calibration after retraining brier ece reliability | 有 Brier/ECE/reliability 证据 |
| P40-C12 | P0 | `kt.ai_feedback_governance.recalibration_loop` | threshold policy 必须与成本矩阵和人工复核预算联动 | cost-sensitive learning doc, decision threshold doc | decision threshold cost matrix review capacity | 阈值不是固定 0.5 |
| P40-C13 | P0 | `kt.ai_feedback_governance.champion_challenger` | challenger 必须先通过 offline、shadow、paper 或 soft-gate 验证 | MLOps deployment doc, model validation doc | champion challenger shadow deployment model validation | 明确 challenger 晋级阶段 |
| P40-C14 | P0 | `kt.ai_feedback_governance.shadow_paper_canary` | hard gate 启用前必须经过受控 canary 和停止条件检查 | canary deployment doc, ML monitoring doc | canary release stop condition model deployment guardrail | 有 stop condition / rollback |
| P40-C15 | P0 | `kt.ai_feedback_governance.rollback_governance` | 每次发布必须有 release manifest、rollback target、kill switch 和审批记录 | model registry doc, release management doc, incident response doc | release manifest rollback kill switch model deployment approval | 缺 rollback 直接阻断 |
| P40-C16 | P0 | `kt.ai_feedback_governance.llm_prompt_rag_sft_loop` | LLM 持续改进优先 RAG 更新，其次 prompt 更新，最后才考虑 SFT/LoRA | LLM eval doc, RAG eval doc, fine-tuning doc | RAG update prompt evaluation fine tuning trigger | 明确 SFT 不是第一反应 |
| P40-C17 | P0 | `kt.ai_feedback_governance.llm_prompt_rag_sft_loop` | SFT/LoRA 只能在 eval 证明 schema、citation、reason-code 长期失败时触发 | fine-tuning official doc, eval framework doc | when to fine tune LLM eval schema citation reason code | 有 eval-based trigger |
| P40-C18 | P0 | `kt.ai_feedback_governance.feedback_loop_risk` | 自标注、模型生成标签和选择性日志必须标注来源，避免反馈回路污染 | ML bias paper, data leakage doc, feedback loop article | feedback loop bias self training selective labels model generated labels | 明确自标注污染风险 |

## P0-Extended 采集矩阵

| ID | 优先级 | canonical node | 知识点 | 推荐来源类型 | 搜索方向 | 接受门槛 |
| --- | --- | --- | --- | --- | --- | --- |
| P40-E01 | P0 | `kt.ai_feedback_governance.feedback_logging` | feedback log 必须支持 replayable audit trail | audit logging doc, ML observability doc | replayable audit trail prediction log lineage | 可从 log 回放决策 |
| P40-E02 | P0 | `kt.ai_feedback_governance.label_refresh` | 标签策略版本变更必须触发历史样本兼容性说明 | dataset versioning doc, label schema doc | label policy version dataset migration compatibility | 有 label_policy_version |
| P40-E03 | P0 | `kt.ai_feedback_governance.drift_monitoring` | 漂移报警必须区分数据质量问题、市场变化和策略版本变化 | monitoring doc, data quality doc | drift root cause data quality concept drift version change | 有 root cause 分类 |
| P40-E04 | P0 | `kt.ai_feedback_governance.retraining_trigger` | 事故驱动再训练不能绕过常规评估和审批 | incident response doc, MLOps governance doc | incident retraining approval model governance | 事故触发也要审批 |
| P40-E05 | P0 | `kt.ai_feedback_governance.recalibration_loop` | 再校准报告必须包含分桶可靠性和样本覆盖边界 | calibration doc, reliability diagram paper | reliability diagram calibration bins sample coverage | 有分桶和覆盖边界 |
| P40-E06 | P0 | `kt.ai_feedback_governance.champion_challenger` | champion/challenger 比较必须包含风险指标，不得只看平均收益 | model validation doc, risk metric doc | model validation risk metric challenger evaluation | 包含风险切片 |
| P40-E07 | P0 | `kt.ai_feedback_governance.shadow_paper_canary` | shadow 和 paper 结果必须明确与真实执行环境的差异 | shadow deployment doc, paper trading limitation doc | shadow mode paper trading limitations execution difference | 声明非实盘等价 |
| P40-E08 | P0 | `kt.ai_feedback_governance.rollback_governance` | rollback 后必须冻结相关模型、prompt、RAG 包和阈值策略 | incident response doc, rollback doc | model rollback freeze artifact incident response | 明确冻结范围 |
| P40-E09 | P0 | `kt.ai_feedback_governance.llm_prompt_rag_sft_loop` | RAG 知识更新必须回写检索评测集，不能只修改文档 | RAG eval doc, retrieval evaluation doc | RAG evaluation regression retrieval test set | 有 retrieval regression |
| P40-E10 | P0 | `kt.ai_feedback_governance.feedback_loop_risk` | 人工复核样本不能直接作为默认真值，必须带 reviewer、reason 和冲突状态 | labeling guideline, human annotation doc | human label audit reviewer reason conflict | 人审也要审计 |
| P40-E11 | P0 | `kt.ai_feedback_governance.feedback_loop_risk` | 高置信模型输出不能替代来源证据 | model risk doc, AI governance doc | model confidence not evidence uncertainty audit | 明确 confidence 不等于 evidence |
| P40-E12 | P0 | `kt.ai_feedback_governance.drift_monitoring` | 持续学习看板必须显示 drift、calibration、false allow/block 和人审成本趋势 | ML monitoring dashboard doc | model monitoring dashboard calibration drift review cost | 有 dashboard 指标 |

## P1 采集矩阵

| ID | 优先级 | canonical node | 知识点 | 推荐来源类型 | 搜索方向 | 接受门槛 |
| --- | --- | --- | --- | --- | --- | --- |
| P40-P01 | P1 | `kt.ai_feedback_governance.feedback_logging` | feedback 采样策略必须说明长尾市场和低频策略覆盖 | sampling doc, model monitoring doc | long tail monitoring sampling low frequency class | 有长尾覆盖说明 |
| P40-P02 | P1 | `kt.ai_feedback_governance.label_refresh` | 标签冲突需要仲裁策略和 gold set 回归测试 | annotation guideline, gold set doc | label conflict adjudication gold set regression | 有仲裁机制 |
| P40-P03 | P1 | `kt.ai_feedback_governance.retraining_trigger` | 再训练计划应支持固定节奏与事件触发混合 | MLOps retraining doc | scheduled retraining event driven retraining | 明确混合触发 |
| P40-P04 | P1 | `kt.ai_feedback_governance.champion_challenger` | challenger 拒绝也要记录原因，进入后续实验知识库 | experiment tracking doc | experiment tracking rejected model reason | 保留拒绝原因 |
| P40-P05 | P1 | `kt.ai_feedback_governance.rollback_governance` | 发布治理要支持模型、prompt、RAG 包、阈值的组合回滚 | release management doc, LLMOps doc | rollback model prompt RAG threshold composite release | 支持组合 artifact |
| P40-P06 | P1 | `kt.ai_feedback_governance.llm_prompt_rag_sft_loop` | LLM 改动必须分离 prompt regression、RAG retrieval regression 和 model eval | LLM eval doc, prompt regression doc | prompt regression RAG regression model eval separation | 三类评测分开 |

## 知识卡片字段要求

后续生成候选知识卡时，每条至少包含：

```text
knowledge_id
candidate_id
target_canonical_node_id
claim_type
content.statement
applies_when
not_applicable_when
llm_usage_policy
machine_gate
source_evidence
source_quality
conflict_audit
review.review_status = candidate_ready
contribution.private_data_removed = true
```

## CEK-TA-303 DoD

```text
1. 本矩阵文件存在。
2. 共 36 条知识点，P0-Core 18 条、P0-Extended 12 条、P1 6 条。
3. 每条都有 canonical node、推荐来源类型、搜索方向和接受门槛。
4. 矩阵不包含 Trading Engineering 本体知识。
5. 后续 ResearchIngestionTask 队列可以逐条引用本矩阵 ID。
```
