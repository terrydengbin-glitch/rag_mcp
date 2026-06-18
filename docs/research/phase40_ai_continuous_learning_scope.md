# Phase 40 AI Continuous Learning 知识范围与 L3 专题结构

## 文档目的

本文定义 Phase 40 的知识范围、知识树归属、上下游边界和首批 36 条知识点规划，用于支撑外接交易 LLM gating/scoring 项目的长期持续学习、再训练、再校准、发布与回滚治理。

本阶段只做知识库与工程契约准备，不训练真实模型，不引入在线自动学习，不改变 MCP、SearchLab、Vue3 的权限语义。

## 上游输入

| 上游 | 用途 |
| --- | --- |
| Phase 36 AI Engineering 知识扩展 | 提供交易 LLM gating/scoring 的基础知识、候选审计和 reviewed 沉淀流程 |
| Phase 38 AI 模型平台与 POC 知识扩展 | 提供 numeric scorer、LLM audit assistant、deterministic final gate、校准、shadow/paper/OPE、发布治理基础 |
| Phase 39 知识树单一数据源 | 确保新增节点由 `knowledge_tree.md` 驱动，并同步 FastAPI/Vue3/MCP |
| 用户持续学习建议 | 明确持续学习不是在线自动学习，必须采用反馈采集、定期训练、受控发布和回滚 |

## 下游消费者

| 下游 | 消费方式 |
| --- | --- |
| 外接 LLM gating/scoring 项目 | 读取持续学习、反馈治理、再训练、再校准、灰度发布和回滚规则 |
| MCP / SearchLab | 按 canonical node 检索 Phase 40 知识，并返回来源、边界和机器门控 |
| Vue3 知识树 | 展示 `kt.ai_feedback_governance` 下 L3 专题、知识覆盖、候选和缺口 |
| 候选审计页 | 承接 Phase 40 候选知识的来源审计、冲突审计和 reviewed 沉淀 |
| Phase 37 Trading Engineering | 接收交易规则本体、K 线、fill model、订单状态机、风控规则等非 AI Engineering 内容 |

## 总体边界

### 范围内

```text
1. 交易 AI 的反馈日志、标签刷新、数据集版本、漂移检测、再训练触发、再校准。
2. champion/challenger 对比、shadow/paper/canary 验证、发布审批、回滚和 kill switch 治理。
3. LLM 审计助手的 prompt/RAG/SFT 持续改进顺序。
4. 自标注、选择性日志、反馈回路过拟合和自动化偏差风险控制。
5. 知识树 L3 专题、采集矩阵、ResearchIngestionTask 和审计 JSON 的前置规划。
```

### 范围外

```text
1. 不训练真实模型。
2. 不引入线上自动学习或自动替换 champion model。
3. 不让 LLM 作为最终交易 gate。
4. 不采集 K 线形态、市场微观结构、fill model、订单状态机、实盘风控规则本体。
5. 不把交易项目私有字段提升为通用知识。
6. 不新增数据库、特征库、模型注册表或外部 MLOps 平台。
```

## 知识树归属

Phase 40 主归属节点：

```text
L1: kt.ai_engineering
L2: kt.ai_feedback_governance
partition_id: KB_AI_18_FEEDBACK_GOVERNANCE
```

该节点服务 AI Engineering 的持续学习治理，不替代以下分支：

| 相关分支 | 归属边界 |
| --- | --- |
| `kt.ai_engineering.numeric_scoring` | 数值 scorer、meta-labeling、模型选择和打分边界 |
| `kt.ai_engineering.calibration_threshold` | 首版校准和阈值策略，Phase 40 只处理持续再校准闭环 |
| `kt.ai_engineering.shadow_paper_ope_eval` | 首版 shadow/paper/OPE 方法，Phase 40 处理长期发布验证链路 |
| `kt.ai_engineering.model_release_governance` | 通用模型发布治理，Phase 40 处理持续学习后的发布和回滚 |
| `kt.trading_engineering.*` | 交易规则、K 线、回测、回放、执行、风控、交易分析本体 |

## L3 专题结构

| L3 专题 | canonical node | 主要问题 | 输出形态 |
| --- | --- | --- | --- |
| Feedback Logging | `kt.ai_feedback_governance.feedback_logging` | 是否记录了所有候选交易，而不是只记录成交交易 | schema / checklist / anti-pattern |
| Label Refresh | `kt.ai_feedback_governance.label_refresh` | 标签是否只看 PnL，是否覆盖人工复核、坏赢好亏、false allow/block cost | schema / procedure / eval case |
| Drift Monitoring | `kt.ai_feedback_governance.drift_monitoring` | 特征、标签、分数、校准、策略和市场 regime 是否漂移 | checklist / eval case |
| Retraining Trigger | `kt.ai_feedback_governance.retraining_trigger` | 何时触发再训练，如何禁止再训练结果自动上线 | policy / procedure |
| Recalibration Loop | `kt.ai_feedback_governance.recalibration_loop` | 再训练后是否重新校准概率和阈值 | procedure / eval case |
| Champion Challenger | `kt.ai_feedback_governance.champion_challenger` | challenger 如何与 champion 比较和晋级 | procedure / checklist |
| Shadow Paper Canary | `kt.ai_feedback_governance.shadow_paper_canary` | 如何从 shadow 到 paper 再到 canary 受控推进 | procedure / eval case |
| Rollback Governance | `kt.ai_feedback_governance.rollback_governance` | 发布前是否有 rollback target、kill switch 和审批链 | schema / checklist |
| LLM Prompt RAG SFT Loop | `kt.ai_feedback_governance.llm_prompt_rag_sft_loop` | LLM 持续改进是否优先 RAG/prompt，而不是直接 SFT/LoRA | procedure / anti-pattern |
| Feedback Loop Risk | `kt.ai_feedback_governance.feedback_loop_risk` | 自标注、选择性日志和模型反馈是否污染训练闭环 | principle / anti-pattern |

## 36 条知识点规划

### P0-Core：18 条

| 编号 | canonical node | 知识点 |
| --- | --- | --- |
| P40-C01 | `kt.ai_feedback_governance.feedback_logging` | 所有交易候选都必须记录，包括 allow、block、skip 和 human_review |
| P40-C02 | `kt.ai_feedback_governance.feedback_logging` | feedback record 必须保存决策时特征、scorer 输出、LLM 审计输出、final gate 决策和后验结果引用 |
| P40-C03 | `kt.ai_feedback_governance.feedback_logging` | 被阻断候选也必须保留 opportunity-cost 评估入口，避免只学习已成交样本 |
| P40-C04 | `kt.ai_feedback_governance.label_refresh` | 标签不能只用 PnL，必须覆盖交易质量、规则违规、风控违规、执行质量和人工复核 |
| P40-C05 | `kt.ai_feedback_governance.label_refresh` | good loss 与 bad win 必须进入标签复核，防止模型学习错误激励 |
| P40-C06 | `kt.ai_feedback_governance.label_refresh` | false allow cost 与 false block cost 必须进入评估和阈值决策 |
| P40-C07 | `kt.ai_feedback_governance.drift_monitoring` | feature drift、label drift、score distribution drift 和 calibration drift 必须分开监控 |
| P40-C08 | `kt.ai_feedback_governance.drift_monitoring` | strategy version、symbol mix、market regime 和 execution cost 漂移必须纳入交易 AI 监控 |
| P40-C09 | `kt.ai_feedback_governance.retraining_trigger` | 再训练只能生成 candidate model，不得自动替换 champion model |
| P40-C10 | `kt.ai_feedback_governance.retraining_trigger` | 再训练触发必须记录触发原因、样本窗口、数据版本和审批状态 |
| P40-C11 | `kt.ai_feedback_governance.recalibration_loop` | 每次再训练后必须重新校准概率、阈值和分组可靠性 |
| P40-C12 | `kt.ai_feedback_governance.recalibration_loop` | threshold policy 必须与成本矩阵和人工复核预算联动 |
| P40-C13 | `kt.ai_feedback_governance.champion_challenger` | challenger 必须先通过 offline、shadow、paper 或 soft-gate 验证 |
| P40-C14 | `kt.ai_feedback_governance.shadow_paper_canary` | hard gate 启用前必须经过受控 canary 和停止条件检查 |
| P40-C15 | `kt.ai_feedback_governance.rollback_governance` | 每次发布必须有 release manifest、rollback target、kill switch 和审批记录 |
| P40-C16 | `kt.ai_feedback_governance.llm_prompt_rag_sft_loop` | LLM 持续改进优先 RAG 更新，其次 prompt 更新，最后才考虑 SFT/LoRA |
| P40-C17 | `kt.ai_feedback_governance.llm_prompt_rag_sft_loop` | SFT/LoRA 只能在 eval 证明 schema、citation、reason-code 长期失败时触发 |
| P40-C18 | `kt.ai_feedback_governance.feedback_loop_risk` | 自标注、模型生成标签和选择性日志必须标注来源，避免反馈回路污染 |

### P0-Extended：12 条

| 编号 | canonical node | 知识点 |
| --- | --- | --- |
| P40-E01 | `kt.ai_feedback_governance.feedback_logging` | feedback log 必须支持 replayable audit trail |
| P40-E02 | `kt.ai_feedback_governance.label_refresh` | 标签策略版本变更必须触发历史样本兼容性说明 |
| P40-E03 | `kt.ai_feedback_governance.drift_monitoring` | 漂移报警必须区分数据质量问题、市场变化和策略版本变化 |
| P40-E04 | `kt.ai_feedback_governance.retraining_trigger` | 事故驱动再训练不能绕过常规评估和审批 |
| P40-E05 | `kt.ai_feedback_governance.recalibration_loop` | 再校准报告必须包含分桶可靠性和样本覆盖边界 |
| P40-E06 | `kt.ai_feedback_governance.champion_challenger` | champion/challenger 比较必须包含风险指标，不得只看平均收益 |
| P40-E07 | `kt.ai_feedback_governance.shadow_paper_canary` | shadow 和 paper 结果必须明确与真实执行环境的差异 |
| P40-E08 | `kt.ai_feedback_governance.rollback_governance` | rollback 后必须冻结相关模型、prompt、RAG 包和阈值策略 |
| P40-E09 | `kt.ai_feedback_governance.llm_prompt_rag_sft_loop` | RAG 知识更新必须回写检索评测集，不能只修改文档 |
| P40-E10 | `kt.ai_feedback_governance.feedback_loop_risk` | 人工复核样本不能直接作为默认真值，必须带 reviewer、reason 和冲突状态 |
| P40-E11 | `kt.ai_feedback_governance.feedback_loop_risk` | 高置信模型输出不能替代来源证据 |
| P40-E12 | `kt.ai_feedback_governance.drift_monitoring` | 持续学习看板必须显示 drift、calibration、false allow/block 和人审成本趋势 |

### P1：6 条

| 编号 | canonical node | 知识点 |
| --- | --- | --- |
| P40-P01 | `kt.ai_feedback_governance.feedback_logging` | feedback 采样策略必须说明长尾市场和低频策略覆盖 |
| P40-P02 | `kt.ai_feedback_governance.label_refresh` | 标签冲突需要仲裁策略和 gold set 回归测试 |
| P40-P03 | `kt.ai_feedback_governance.retraining_trigger` | 再训练计划应支持固定节奏与事件触发混合 |
| P40-P04 | `kt.ai_feedback_governance.champion_challenger` | challenger 拒绝也要记录原因，进入后续实验知识库 |
| P40-P05 | `kt.ai_feedback_governance.rollback_governance` | 发布治理要支持模型、prompt、RAG 包、阈值的组合回滚 |
| P40-P06 | `kt.ai_feedback_governance.llm_prompt_rag_sft_loop` | LLM 改动必须分离 prompt regression、RAG retrieval regression 和 model eval |

## 采集来源类型要求

| 知识方向 | 优先来源 |
| --- | --- |
| 持续训练与 MLOps | 官方文档、工程白皮书、权威技术博客、学术论文 |
| 数据漂移与校准 | 学术论文、机器学习官方文档、统计学习资料 |
| champion/challenger 与灰度发布 | MLOps 平台文档、工程案例、生产发布实践 |
| LLM prompt/RAG/SFT 闭环 | 官方文档、RAG 评测资料、LLM 训练评估资料 |
| 交易 AI 风险边界 | 交易系统工程资料、模型风险管理资料、CEK-TA 内部契约 |

## 接受门槛

后续候选知识必须满足：

```text
1. 每条至少有 source_evidence。
2. 不能只引用普通博客，必须尽量使用官方文档、论文、框架文档或工程案例。
3. 必须明确 applies_when 和 not_applicable_when。
4. 必须明确 LLM 是否可作为默认指导。
5. 不能把 LLM 设为最终交易 gate。
6. 不能把再训练结果自动升级为 champion。
7. 不能与 Phase 36/38 reviewed 知识冲突。
8. 不能把 Trading Engineering 本体知识塞进 AI Engineering。
```

## CEK-TA-299 DoD 对照

```text
1. `docs/research/phase40_ai_continuous_learning_scope.md` 已创建。
2. `codex-expert-kit/rag/knowledge_tree.md` 已补齐 `kt.ai_feedback_governance` 的 L3 专题。
3. L3 专题不新增顶级主枝，仍归 AI Engineering / Feedback Governance。
4. 36 条知识点范围已按 P0-Core、P0-Extended、P1 拆分。
5. 已写清与 Trading Engineering、Phase 36、Phase 38 的边界。
6. 后续 CEK-TA-300 至 CEK-TA-304 可直接消费本文档。
```
