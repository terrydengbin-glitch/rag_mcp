# Phase 38 AI 模型平台与交易 Gating/Scoring POC 知识范围

生成日期：2026-06-10
状态：scope draft
对应任务：CEK-TA-266

## 目标

本文定义 Phase 38 的知识范围、子板块、canonical node、知识点数量、上下游边界和跨分支路由，用于后续联网采集、候选知识生成、AI/人工审计和 formal reviewed 沉淀。

Phase 38 的核心目标是支持外接项目开发“交易质量 gating/scoring POC”：

```text
数值模型负责 scoring / risk ranking / review priority。
LLM 负责审计解释、reason code、RAG 引用和人工复核摘要。
确定性 final gate 负责最终 allow/block/size/kill switch。
```

本范围文档不是正式知识卡，不提供默认指导。所有具体知识点必须走：

```text
ResearchIngestionTask -> candidate -> AI/人工审计 -> formal reviewed -> 后续人工治理 approved
```

## 上游输入

```text
docs/research/phase36_ai_engineering_model_platform_selection_proposal.md
docs/research/phase36_ai_engineering_knowledge_framework.md
docs/contracts/ai_engineering_gating_scoring_contract.md
docs/tasks/phase38_ai_model_platform_poc_knowledge.md
codex-expert-kit/rag/knowledge_tree.md
```

## 下游输出

```text
docs/contracts/phase38_ai_scoring_gate_runtime_contract.md
docs/contracts/phase38_training_data_and_eval_contract.md
docs/research/phase38_ai_model_platform_collection_matrix.md
docs/research/phase38_ai_model_platform_research_task_queue.md
docs/audit/phase38_ai_model_platform_knowledge_scope_for_audit.json
codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/
codex-expert-kit/rag/knowledge/KB_AI_ENGINEERING/
codex-expert-kit/rag/indexes/knowledge_items.json
ui/src/data/formalKnowledgeItems.ts
```

## 子板块总览

Phase 38 不新增顶级主枝，统一挂载到现有 `kt.ai_engineering`。RAG 相关内容只放到 `kt.rag_engineering.trading_scoring_rag_pack`，交易规则本体继续归 Phase 37 / Trading Engineering。

| 子板块 | canonical node | 主分区 | 预计知识点 | 主要消费者 |
| --- | --- | --- | ---: | --- |
| Numeric Scoring / Meta-Labeling | `kt.ai_engineering.numeric_scoring` | `KB_AI_20_NUMERIC_SCORING` | 10 | 外接训练项目、MCP、SearchLab |
| Calibration & Threshold Policy | `kt.ai_engineering.calibration_threshold` | `KB_AI_21_CALIBRATION_THRESHOLD` | 10 | scorer service、final gate、审计 UI |
| Decision-Time Feature & Leakage Gate | `kt.ai_engineering.decision_time_feature_contract` | `KB_AI_22_DECISION_TIME_FEATURES` | 10 | 数据集生成器、训练脚本、质量门禁 |
| LLM Audit Assistant | `kt.ai_engineering.llm_audit_assistant` | `KB_AI_23_LLM_AUDIT_ASSISTANT` | 10 | LLM 审计服务、AI IDE、候选审核 |
| Shadow / Paper / OPE Evaluation | `kt.ai_engineering.shadow_paper_ope_eval` | `KB_AI_24_SHADOW_PAPER_OPE` | 10 | eval pipeline、上线审批、复盘 |
| Model Release / Lineage / Rollback | `kt.ai_engineering.model_release_governance` | `KB_AI_25_MODEL_RELEASE_GOVERNANCE` | 10 | LLMOps、发布治理、事故复盘 |
| Trading AI RAG Pack & Citation Governance | `kt.rag_engineering.trading_scoring_rag_pack` | `KB_10_RAG_ENGINEERING` | 6 | MCP/SearchLab/外部 AI 主动检索 |

建议总数：

```text
P0-Core：43 条
P0-Extended：16 条
P1：7 条
合计：66 条
```

## P0-Core 子范围

P0-Core 是训练、评估、上线前必须具备的硬门，缺失时不得进入 hard gate 或实盘自动化。

```text
1. scorer / soft gate / final gate 职责边界
2. deterministic rule baseline
3. Logistic Regression baseline
4. LightGBM / XGBoost 并行候选
5. meta-labeling 只能过滤候选，不生成交易机会
6. calibration holdout 独立于 scorer 训练集
7. Brier / reliability / ECE 校准检查
8. cost matrix threshold policy
9. decision_time / feature_available_time / label_observation_end_time
10. post-trade field forbidden in scorer input
11. leakage unit test
12. training-serving parity check
13. LLM strict schema output
14. citation resolver
15. no-source abstain
16. unsupported claim detector
17. offline eval 不能声称 blocked trade 真实收益
18. shadow eval before hard gate
19. paper/replay eval for false block opportunity
20. OPE caveat for policy change
21. release manifest
22. dataset/model/prompt/rag hash
23. rollback target
24. kill switch and approval workflow
25. RAG context is untrusted input
26. machine_gate and review_status filtering
27. top-k and field trimming for context budget
28. no-hit neutral or human review
29. PnL-only label forbidden
30. model output cannot label itself
31. human review queue and SLA
32. false allow / false block cost ledger
33. feature schema registry
34. data version and split manifest
35. model registry versioning
36. final gate deterministic authority
37. scoring/gating 任务必须主动检索 CEK-TA
38. RAG context 默认是不可信输入
39. machine_gate 和 review_status 必须过滤默认指导
40. 知识包必须裁剪字段，控制上下文预算
41. citation completeness 必须进入 shadow 指标
42. no-hit query 应进入知识缺口队列
43. hard gate 开启必须保留审批和回滚链路
```

## P0-Extended 子范围

P0-Extended 用于第一轮工程建设补强，不阻断范围定义，但阻断正式发布。

```text
1. CatBoost 条件引入规则
2. conformal uncertainty layer 条件引入
3. SHAP / feature attribution 用于调试，不等于因果解释
4. review_priority 排序策略
5. threshold policy by strategy / regime / horizon
6. calibration drift monitoring
7. data quality expectation suites
8. feature lineage manifest
9. prompt + RAG baseline before SFT
10. SFT LoRA 触发条件
11. DPO / preference data 边界
12. ablation for RAG / prompt / model / threshold
13. shadow human-review precision
14. paper execution cost consistency
15. incident freeze
16. model card and dataset card
```

## P1 子范围

P1 用于优化增强。

```text
1. Bayesian calibration layer
2. ranking model alternative
3. multi-market transfer caveat
4. teacher model audit baseline
5. active learning review sampling
6. model compression / latency tradeoff
7. no-hit query 缺口治理增强
```

## 跨分支路由

Phase 38 只保存 AI 工程方法，不保存交易规则本体。

必须路由到 Trading Engineering 的内容：

```text
K 线形态、指标阈值、入场、止损、止盈 -> Phase 37 / Kline Strategy
回测偏差、walk-forward、成本模型本体 -> Phase 37 / Backtest
同根 K TP/SL、fill model、滑点、延迟 -> Phase 37 / Replay Simulation
订单状态机、仓位同步、kill switch 执行规则 -> Phase 37 / Live Execution
风控闸门、单笔风险、日亏损、组合暴露 -> Phase 37 / Risk Management / Live Risk Control
交易复盘 taxonomy、R/R 分解、坏例分类 -> Phase 37 / Trade Analysis
```

Phase 38 可以引用这些交易知识，但只能作为：

```text
related_trading_refs
knowledge_refs
retrieved_knowledge
reason_codes
eval gate 的依赖项
training data schema 中的引用字段
```

## 来源策略

优先来源类型：

```text
official_doc
framework_doc
research_paper
engineering_article
book_reference
governance_framework
```

首批种子来源：

| 来源 | 类型 | 用途 |
| --- | --- | --- |
| scikit-learn probability calibration | official_doc | 校准、Brier、概率解释 |
| LightGBM documentation | official_doc | GBDT scorer 候选 |
| XGBoost documentation | official_doc | GBDT scorer 候选 |
| CatBoost documentation | official_doc | 类别特征条件候选 |
| Hugging Face TRL SFT/DPO docs | official_doc | LLM 审计助手后训练边界 |
| OpenAI Structured Outputs | official_doc | strict schema 输出机制参考 |
| MLflow Model Registry | official_doc | 模型版本、注册、发布治理 |
| DVC docs | official_doc | 数据版本、pipeline、复现 |
| TensorFlow Data Validation | official_doc | schema、skew、drift、训练服务一致性 |
| NIST AI RMF | governance_framework | AI 风险治理和可信性 |
| Hudson & Thames meta-labeling | engineering_article | 交易 meta-labeling 结构 |
| ICML / PMLR OPE papers | research_paper | off-policy evaluation 边界 |

## 非目标

```text
不训练真实模型。
不引入数据库。
不选择唯一云平台。
不把 LLM 设为最终交易决策器。
不采集交易规则本体。
不把 reviewed 自动升为 approved。
不把某个外接项目私有经验写入通用知识。
```

## 审计问题

```text
1. 66 条范围是否足以覆盖第一版 trading gating/scoring POC？
2. Numeric scorer 是否应独立于 LLM Training 成为 AI Engineering 下的二级子板块？
3. RAG Pack 是否继续挂在 kt.rag_engineering.trading_scoring_rag_pack？
4. Phase 38 是否只引用 Trading Engineering，不复制交易规则本体？
5. P0-Core 是否应作为外接项目进入 POC 前的硬门？
```

## 当前状态

```text
CEK-TA-266: doing
下一步：创建 Phase 38 运行时契约、数据契约、采集矩阵和审计 JSON。
```
