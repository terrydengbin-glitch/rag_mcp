# Phase 41 Hybrid Scoring 与 Qwen3 审计助手知识范围

## 范围结论

Phase 41 只补齐 AI Engineering 中“组合式 scoring/audit/gate 架构”的专业知识，不采集交易规则本体。

核心链路固定为：

```text
表格/统计模型负责数值 scoring、风险排序和复核优先级。
Qwen3/LLM 负责审计解释、reason code、RAG 引用、缺字段检查和人工复核摘要。
deterministic final gate 负责最终交易权限、阻断、降级、回滚和审计追踪。
```

本 Phase 的知识必须服务外接 LLM gating/scoring 项目的 AI IDE，让开发 AI 能快速理解该用什么模型、模型输出如何校准、Qwen3 能做什么、不能做什么，以及最终交易放行为什么不能交给语言模型。

## 上游输入

| 上游 | 作用 |
| --- | --- |
| Phase 36 AI Engineering gating/scoring 知识 | 提供交易 LLM 项目、训练数据、审计状态和默认指导边界 |
| Phase 38 AI 模型平台与交易 Gating/Scoring POC | 提供 Numeric Scorer、LLM Audit Assistant、Final Gate 的基础运行时契约 |
| Phase 40 Continuous Learning | 提供反馈日志、漂移监控、再训练、再校准、发布和回滚治理 |
| Phase 37 Trading Engineering | 提供交易本体引用边界，K 线、fill model、风控、执行和回测规则不迁入 Phase 41 |
| `codex-expert-kit/rag/knowledge_tree.md` | 提供 AI Engineering L1/L2/L3 节点挂载位置 |

## 下游输出

| 下游 | 消费方式 |
| --- | --- |
| CEK-TA-320 runtime contract | 使用本范围定义 scorer、Qwen3、RAG、final gate 的职责边界 |
| CEK-TA-321 training data contract | 使用本范围定义 point-in-time feature、标签、校准、阈值和 registry 字段 |
| CEK-TA-322 collection matrix | 按本范围拆分并按审计补丁调整为 41 条知识点 |
| CEK-TA-323 scope audit JSON | 把本范围、专题和数量交给外部 AI/人工先审计 |
| MCP/SearchLab/KnowledgeTree/Vue3 | 按 canonical node 检索、展示和审计正式知识 |

## L2 到 L3 专题映射

| L2 节点 | L3 专题 | canonical node | 分区 |
| --- | --- | --- | --- |
| Numeric Scoring And Meta Labeling | Model Family Selection | `kt.ai_engineering.numeric_scoring.model_family_selection` | `KB_AI_20_NUMERIC_SCORING` |
| Numeric Scoring And Meta Labeling | Tabular Scorer Training | `kt.ai_engineering.numeric_scoring.tabular_scorer_training` | `KB_AI_20_NUMERIC_SCORING` |
| Numeric Scoring And Meta Labeling | Scorer Explainability | `kt.ai_engineering.numeric_scoring.scorer_explainability` | `KB_AI_20_NUMERIC_SCORING` |
| Calibration And Threshold Policy | Calibration Uncertainty | `kt.ai_engineering.calibration_threshold.uncertainty` | `KB_AI_21_CALIBRATION_THRESHOLD` |
| Decision-Time Feature And Leakage Gate | Decision-Time Feature Store | `kt.ai_engineering.decision_time_feature_contract.feature_store` | `KB_AI_22_DECISION_TIME_FEATURES` |
| LLM Audit Assistant | Qwen3 Audit Assistant | `kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant` | `KB_AI_23_LLM_AUDIT_ASSISTANT` |
| LLM Audit Assistant | Qwen3 Training Recipe | `kt.ai_engineering.llm_audit_assistant.qwen3_training_recipe` | `KB_AI_23_LLM_AUDIT_ASSISTANT` |
| Model Release Governance | Hybrid Runtime Contract | `kt.ai_engineering.model_release_governance.hybrid_runtime_contract` | `KB_AI_25_MODEL_RELEASE_GOVERNANCE` |
| Model Release Governance | Training Platform Governance | `kt.ai_engineering.model_release_governance.training_platform_governance` | `KB_AI_25_MODEL_RELEASE_GOVERNANCE` |

## L3 专题职责

### Model Family Selection

范围内：

```text
Rule baseline、Logistic Regression、LightGBM、XGBoost、CatBoost 的同场比较。
不同模型家族在交易 scoring 中的适用边界、数据要求、解释成本、延迟和治理成本。
不能预设某个模型必胜，必须用时间切分、校准和业务成本评估。
```

范围外：

```text
不做真实训练。
不声称某模型能稳定提升 PnL。
不把模型选择替代交易策略设计。
```

### Tabular Scorer Training

范围内：

```text
类别不平衡、class weight、sample weight、时间切分、HPO 防泄漏、类别特征处理。
训练集、验证集、校准集、shadow/paper/test 的边界。
numeric scorer 只输出风险排序、质量分和候选复核优先级。
```

范围外：

```text
不定义 K 线信号规则。
不定义订单执行、仓位或风控本体。
不允许 scorer 直接生成交易放行结论。
```

### Scorer Explainability

范围内：

```text
SHAP、feature importance、局部解释、全局解释和解释边界。
解释只能用于审计、debug、复核和监控，不等于因果证明。
feature attribution / top_features 不得作为交易规则证据或 final gate 决策依据。
```

范围外：

```text
不把解释结果当作买卖依据。
不把 feature importance 当作策略有效性证明。
```

### Calibration Uncertainty

范围内：

```text
独立校准集、Platt scaling、isotonic regression、Brier/ECE、分层校准、uncertainty bucket、abstain band。
阈值必须绑定业务成本、false allow、false block 和人工复核容量。
```

范围外：

```text
不把 raw score 当概率。
不允许未校准分数直接进入 final gate。
```

### Decision-Time Feature Store

范围内：

```text
point-in-time join、线上线下一致性、feature lineage、feature schema version、label observation window。
训练、回测、shadow、paper、live 的特征生成必须可追踪。
```

范围外：

```text
不采集具体市场数据。
不定义交易项目私有特征字段。
```

### Qwen3 Audit Assistant

范围内：

```text
Qwen3/LLM 只做审计助手：缺字段检查、reason code、RAG 引用、unsupported claim、人工复核摘要。
复杂审计可以使用 thinking mode，低延迟结构化输出可以使用 non-thinking mode。
输出必须符合 strict JSON schema。
RAG context、用户交易摘要和检索文档必须视为不可信输入，进入审计链路前必须经过 prompt-injection guard、citation resolver、unsupported_claim detector 和 schema validation。
thinking mode 不保存私有 chain-of-thought，只保存 strict JSON、reason code、citation 和 audit summary。
```

范围外：

```text
Qwen3 不能做核心 numeric scorer。
Qwen3 不能做最终交易 gate。
Qwen3 不能输出无来源的交易结论。
```

### Qwen3 Training Recipe

范围内：

```text
RAG-first、prompt 修正、SFT、LoRA、DPO/preference pair 的选择边界。
SFT 只训练格式、reason code、引用习惯和审计流程，不训练交易概率。
```

范围外：

```text
不把交易盈亏样本直接训练成买卖建议。
不训练模型绕过 final gate。
```

### Hybrid Runtime Contract

范围内：

```text
scorer_output、qwen_audit_output、final_gate_output 的组合 trace。
每次决策必须记录 scorer_version、calibrator_version、prompt_version、RAG index、threshold_policy_version 和 final_gate 规则命中。
final gate 可以读取校准后的 scorer 风险信号、risk_bucket 和 threshold policy，但不得直接服从 Qwen3 recommendation 或 raw model score。
hybrid scoring runtime 必须定义 scorer、calibrator、RAG、Qwen3 和 final gate 的 latency budget、timeout、fallback、fail-to-review / fail-closed 策略。
```

范围外：

```text
不部署真实服务。
不引入新数据库。
不改变 MCP 只读知识检索权限。
```

### Training Platform Governance

范围内：

```text
MLflow、Ray、Kubeflow、Feast、vLLM 等平台能力的条件引入边界。
POC 阶段优先文件化契约和轻量脚本；只有出现规模、复现、线上线下一致性或服务化压力时才引入平台。
```

范围外：

```text
不在 Phase 41 直接接入平台。
不新增外部服务依赖。
```

## 跨分支边界

| 问题 | Primary branch | Phase 41 处理方式 |
| --- | --- | --- |
| K 线形态、指标、信号有效性 | Trading Engineering / Strategy Engineering | 只引用，不归入 AI Engineering |
| 回测偏差、数据泄漏、walk-forward | Trading Engineering / Backtest | 只作为 scorer 评估的约束引用 |
| fill model、滑点、延迟 | Trading Engineering / Replay Simulation | 只作为特征或标签边界引用 |
| 实盘订单、仓位、风控、安全停机 | Trading Engineering / Live Execution / Risk Management | final gate 只读取规则命中，不定义规则本体 |
| 训练数据、标签、校准、审计解释 | AI Engineering | Phase 41 直接维护 |
| Qwen3 提示词、SFT、DPO、RAG 引用 | AI Engineering / LLM Audit Assistant | Phase 41 直接维护 |
| 发布、回滚、模型 registry、artifact hash | AI Engineering / Model Release Governance | Phase 41 直接维护 |

## 知识卡准入要求

Phase 41 知识卡必须包含：

```text
knowledge_id
canonical_node_id
domain/subdomain
claim_type
model_role
applicability
not_applicable_when
source_evidence
source_quality
conflict_audit
llm_usage_policy
machine_gate
review.review_status
```

最低来源要求：

```text
1. P0-Core 知识点至少 3 个来源或 2 个强来源。
2. Qwen3 相关知识优先引用官方模型文档、技术报告或权威部署文档。
3. 表格模型知识优先引用官方文档、论文、成熟库文档和可复现工程实践。
4. 交易边界知识只引用 Trading Engineering 正式节点，不把交易本体复制到 AI Engineering。
```

## 首轮知识点数量建议

```text
P0-Core: 22 条
P0-Extended: 12 条
P1: 6-10 条
总量: 41 条
```

## 审计重点

外部 AI/人工审计本范围时，优先检查：

```text
1. 是否把 Qwen3 错放成 numeric scorer 或 final gate。
2. 是否把 LightGBM/XGBoost/Logistic Regression 输出错放成交易放行权限。
3. 是否把 K 线、fill model、风控本体污染进 AI Engineering。
4. 是否缺少 point-in-time feature、校准集、阈值策略和 release manifest。
5. 是否遗漏 no-hit abstain、citation、strict JSON、unsupported claim 等 LLM 审计要求。
6. 是否过早引入 MLflow/Feast/Kubeflow/Ray/vLLM 等平台作为运行时依赖。
7. 是否缺少 scorer explainability 的 attribution-not-causality 边界。
8. 是否缺少 Qwen3 + RAG 的 prompt injection / untrusted context 防护。
9. 是否缺少 scorer、calibrator、RAG、Qwen3 和 final gate 的 latency / fallback / timeout 策略。
```
