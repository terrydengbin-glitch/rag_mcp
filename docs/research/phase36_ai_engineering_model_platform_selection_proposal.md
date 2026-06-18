# Phase 36 AI Engineering 模型与训练平台选型审计方案

生成日期：2026-06-10
审计融合版本：v2

## 目标

本方案用于审计“外接交易 LLM gating/scoring 项目”应该采用什么模型和训练平台组合，避免把语言模型误用为交易核心打分器。

本项目目标不是训练一个直接交易的 LLM，而是构建一套可审计、可回测、可模拟盘验证、可实盘降级的交易质量提升系统：

```text
数值模型负责交易质量 scoring / gating 风险排序。
LLM 负责解释、审计、reason code、RAG 引用、人工复核摘要和治理报告。
确定性风控负责最终放行、阻断、仓位和实盘安全边界。
```

## 审计结论

```text
Decision: Conditional Go
```

允许进入：

```text
Phase 38 任务拆分。
离线回测、shadow、paper POC。
soft gate / human-review assistant。
数值 scorer、LLM audit assistant 和 deterministic final gate 的契约设计。
```

暂不允许进入：

```text
LLM 直接输出最终交易 allow/block。
未校准分数进入实盘 hard gate。
PnL-only 标签训练 primary scorer。
未做反事实评估、泄漏审计和 shadow 验证前宣称提升交易收益。
没有 release manifest、rollback 和 kill switch 的实盘自动化。
```

本方案当前只建议推进 POC，不建议直接进入 hard gate 或实盘自动放行阶段。

## 核心结论

```text
Qwen3 / Llama / Mistral 这类语言模型适合做“交易质量审计助手”，不适合单独作为 gating/scoring 的核心数值模型。
```

更合适的第一版架构是：

```text
Rule Gate
  -> 数据完整性、时间戳、风险硬门、泄漏硬门

Tabular / Statistical Scorer
  -> LightGBM / XGBoost / CatBoost / Logistic Regression
  -> 输出 bad_trade_risk、quality_score、false_allow_risk、review_priority

LLM Audit Assistant
  -> Qwen3 或同级语言模型
  -> 输入 scorer 输出、交易上下文、CEK-TA RAG 检索结果
  -> 输出 reason_codes、missing_fields、risk_flags、knowledge_refs、人工复核摘要

Deterministic Final Gate
  -> 最终放行、阻断、仓位、安全停机和实盘权限
```

必须严格区分三个概念：

```text
scoring:
  输出质量分、风险分、校准概率、review_priority。
  不产生最终交易动作。

soft gate:
  输出 allow_recommendation、soft_block_recommendation、hard_block_recommendation、needs_human_review。
  只能影响人工复核、降级、排序或建议。

final gate:
  输出最终 allow/block/size/kill switch。
  只能由 deterministic final gate 和项目 owner 授权规则执行。
```

## 为什么不能让 LLM 做核心交易分数

LLM 的强项：

```text
解释复杂上下文。
把交易记录转成结构化审计结论。
根据知识库生成 reason code。
发现缺字段、冲突、边界不清和规则越权。
辅助人工复核和复盘。
```

LLM 的弱项：

```text
概率未必校准。
对数值尺度、尾部风险和分布漂移不稳定。
容易把语言置信度误当成真实概率。
对时序泄漏、样本外、执行成本和反事实偏差需要外部规则约束。
无法替代 deterministic risk engine。
```

因此，LLM 不应该输出“最终交易允许”，只能输出：

```text
allow_recommendation
soft_block_recommendation
hard_block_recommendation
needs_human_review
neutral
```

最终动作必须由确定性风控和项目 owner 决定。

## 成功案例与可借鉴方向

### 1. 量化机构公开案例更偏向数值机器学习

Man AHL 公开文章说明，AHL 从 2014 年开始在多策略客户组合中交易机器学习系统，机器学习也是其研究重点。这类案例支持“量化 ML 可用于交易系统”，但不等于“LLM 可直接做交易决策”。来源：[Man AHL - The Rise of Machine Learning at Man AHL](https://www.man.com/insights/the-rise-of-machine-learning)。

Two Sigma 公开分享过 deep learning for sequences in quantitative finance，重点是深度学习如何应用于金融序列。这支持“序列模型 / 数值深度学习可用于量化研究”，仍然不是让语言模型直接承担交易放行。来源：[Two Sigma - Deep Learning for Sequences in Quantitative Finance](https://www.twosigma.com/articles/webinar-deep-learning-for-sequences-in-quantitative-finance/)。

### 2. Meta-labeling 更贴合 gating/scoring

Meta-labeling 的思想是：主策略先生成交易候选，再用第二层模型过滤 false positives 或辅助 position sizing。这个结构非常贴合本项目：

```text
主策略产生 candidate trade。
第二层模型判断该候选是否值得执行、是否需要过滤、是否需要降权或人工复核。
```

公开介绍中也强调 meta-labeling 可用于过滤分类模型中的 false positives。来源：[Hudson & Thames - Meta Labeling](https://hudsonthames.org/meta-labeling-a-toy-example/)。

### 3. 概率校准是 gating/scoring 的硬要求

交易 gate 如果输出概率或风险分数，必须校准。scikit-learn 官方文档说明，分类模型输出的概率不一定可靠，calibration 模块用于校准分类器概率。来源：[scikit-learn Probability Calibration](https://scikit-learn.org/stable/modules/calibration.html)。

这说明 gating/scoring 不能只看模型分数排序，还要做：

```text
calibration curve
Brier score
isotonic regression
Platt scaling
threshold by cost matrix
shadow calibration
```

校准硬门：

```text
calibrator 必须使用独立于 scorer 训练数据的 calibration_holdout_set。
不得在 scorer 训练集上拟合 calibrator。
必须按 strategy / regime / horizon 检查分层校准。
必须输出 reliability_diagram、Brier score、ECE/MCE、calibration slope/intercept。
```

阈值不应使用固定 0.5，而应由成本矩阵决定：

```text
expected_cost =
  P(bad_trade) * false_allow_cost
  - P(good_trade) * false_block_cost
  + review_cost
```

final gate 读取的是 expected cost bucket 和 threshold_policy_version，不直接读取裸概率。

## 推荐模型组合

### P0 主路线：数值模型做 scorer

| 模型 | 适用场景 | 优点 | 风险 |
| --- | --- | --- | --- |
| Rule Baseline | 第一版确定性对照 | 可审计、可复现、能定位模型增益 | 覆盖不足 |
| Logistic Regression | 第一版透明 baseline | 可解释、易校准、低过拟合 | 非线性能力弱 |
| LightGBM | primary candidate | 高效、支持大规模、工程成熟 | 不能预设胜出，必须和 baseline 同场比较 |
| XGBoost | strong baseline | 成熟、可解释性工具丰富 | 训练和调参成本较高 |
| CatBoost | 类别变量多时的条件候选 | 原生处理类别特征 | 不是每个 POC 都必须引入 |
| Conformal / uncertainty layer | 不确定性与风险边界 | 可给出不确定区域 | P1，不应阻塞 P0 |

P0 建议：

```text
Rule baseline
Logistic Regression
LightGBM
XGBoost
```

P1 条件引入：

```text
CatBoost：当策略版本、市场状态、交易 venue、symbol group 等类别变量占比高时引入。
Conformal / uncertainty layer：当 P0 scorer 已稳定，需要更明确不确定性边界时引入。
Bayesian calibration layer：当项目需要概率解释和决策成本更透明时引入。
```

暂不建议 P0 引入：

```text
深度序列模型直接做 gate。
LLM logits 或文本置信度当概率。
端到端 LLM trade scorer。
```

参考来源：

```text
LightGBM 官方文档：LightGBM 是基于树学习算法的 gradient boosting framework。
XGBoost 官方文档：XGBoost 是高效、灵活、可移植的 gradient boosting library。
CatBoost 官方资料：CatBoost 是支持类别特征的 gradient boosting on decision trees。
```

来源：

- [LightGBM Documentation](https://lightgbm.readthedocs.io/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [CatBoost Documentation](https://catboost.ai/)

### P0 辅助路线：LLM 做审计助手

| 模型 | 角色 | 用法 |
| --- | --- | --- |
| Qwen3 Instruct / Thinking | 中文和中英混合审计助手 | reason code、RAG 引用、审计解释 |
| Llama open-weight instruct | 备选开源模型 | 英文生态、部署生态成熟 |
| Mistral open-weight instruct | 备选轻量模型 | 延迟和推理成本可控 |
| OpenAI / Gemini / Claude | teacher / judge / baseline | 不作为主训练依赖 |

LLM 训练方式：

```text
SFT：稳定输出 schema、reason code、missing_fields、knowledge_refs。
DPO / preference training：优化“哪种审计结论更安全、更完整、更符合知识库”。
RAG-first baseline：训练前必须先验证 prompt + RAG 是否已足够。
```

Hugging Face TRL 官方支持 SFTTrainer 和 DPOTrainer，可用于语言模型后训练和 PEFT adapter 训练。来源：

- [Hugging Face TRL](https://huggingface.co/docs/trl/en/index)
- [TRL SFT Trainer](https://huggingface.co/docs/trl/en/sft_trainer)
- [TRL DPO Trainer](https://huggingface.co/docs/trl/en/dpo_trainer)

LLM audit assistant 必须输出严格 schema，不允许只输出自然语言报告：

```json
{
  "schema_version": "llm_audit_v1",
  "recommendation": "allow_recommendation | soft_block_recommendation | hard_block_recommendation | needs_human_review | neutral",
  "reason_codes": [],
  "risk_flags": [],
  "missing_fields": [],
  "knowledge_refs": [],
  "unsupported_claims": [],
  "citation_completeness_score": 0.0,
  "requires_human_review": true,
  "llm_must_not_decide_final_gate": true
}
```

必须增加：

```text
JSON Schema validation
enum validation
citation resolver
unsupported_claim detector
no-source abstain
retry then abstain
```

即使最终不用 OpenAI，也应参考结构化输出机制实现同等约束。

## 推荐训练平台组合

### 主路线：开源可迁移训练栈

```text
数值模型：
  scikit-learn + LightGBM / XGBoost / CatBoost

LLM 后训练：
  Hugging Face Transformers + TRL + PEFT/LoRA
  可选 Unsloth / Axolotl / LLaMA-Factory 做加速和实验模板

实验追踪：
  MLflow 或 W&B

数据版本：
  DVC + dataset hash + split manifest

模型服务：
  scorer service + vLLM / llama.cpp / TGI

审计与知识：
  CEK-TA MCP / SearchLab / KnowledgeTree
```

优势：

```text
不锁死单一云厂商。
可本地跑小规模 POC。
可在云 GPU 扩展。
适合保存 adapter、dataset hash、eval report、release manifest。
与 CEK-TA 的审计和知识回灌机制容易对接。
```

平台选型原则应从“训练工具优先”改成“可复现优先”。每次实验必须生成：

```text
release_manifest:
  dataset_hash
  feature_schema_version
  split_manifest_hash
  label_policy_version
  model_code_hash
  model_artifact_hash
  calibrator_hash
  threshold_policy_version
  eval_report_hash
  prompt_version
  rag_index_version
  llm_model_version
  approval_record
  rollback_target
```

### 托管备选

```text
Google Vertex AI Gemini SFT：适合快速托管 POC，但闭源和云绑定较强。
Azure AI Foundry：适合企业 Azure 环境。
OpenAI：不建议作为主 fine-tuning 平台；更适合 eval、teacher、baseline、结构化输出和审计辅助。
```

## 交易 gating/scoring 数据链路

训练数据不能直接从交易日志来，必须分层：

```text
Raw Trade Record
  -> Trade Candidate Snapshot
  -> Decision-Time Features
  -> Outcome / Post-Trade Record
  -> Labeling Record
  -> Numeric Scorer Dataset
  -> LLM Audit SFT Example / Preference Pair / Eval Case
```

字段级时间硬门：

```text
event_time
feature_available_time
decision_time
ingestion_time
label_observation_end_time
```

每个特征必须能回答：

```text
这个字段在 decision_time 之前是否真实可见？
它是原始字段、派生字段，还是人工复盘字段？
它是否来自 post-trade outcome？
它是否可能间接泄漏 exit / realized_pnl / future_return？
```

数值模型输入：

```text
decision_time_features
market_context_ref
risk_context_ref
execution_context_ref
strategy_version_ref
cost/slippage context
rule compliance features
historical quality features
```

数值模型禁止输入：

```text
future_return
realized_pnl
exit_price
MFE / MAE
post_trade_human_review
label
任何决策时不可见字段
```

泄漏单元测试必须覆盖：

```text
禁止字段名命中。
禁止 lineage 命中 post_trade source。
禁止 feature_available_time > decision_time。
禁止 target-derived feature。
禁止 human_review_outcome 进入 scorer training features。
禁止 label_observation_end_time 早于真实可观察结果。
```

LLM 输入：

```text
交易候选摘要
数值模型输出
缺字段列表
规则命中列表
CEK-TA RAG 检索结果
允许公开的上下文引用
```

LLM 禁止输入：

```text
账户密钥
未脱敏账号
私有策略正文
可反推出策略参数的敏感字段
未来结果字段
未经许可的市场数据全文
```

## 标签与评估设计

### 数值 scorer 标签

建议不要只用 PnL 标签，而是多维标签：

```text
bad_trade_flag
good_loss / bad_win
rule_violation
risk_violation
execution_quality
setup_quality
market_regime_fit
false_allow_cost
false_block_cost
human_review_outcome
```

### Meta-labeling 结构

```text
primary_strategy_signal -> trade_candidate
meta_model -> execute_quality / block_quality / review_priority
```

第一版可先做二分类或三分类：

```text
execute_candidate
block_or_skip
needs_human_review
```

再升级到：

```text
quality_score
bad_trade_risk
false_allow_cost
false_block_cost
review_priority
```

### 评估指标

不能只看 PnL：

```text
bad trade false allow rate
risk violation detection rate
false block opportunity cost
precision / recall / F1
ROC-AUC / PR-AUC
Brier score
calibration error
reason_code consistency
human_review precision
knowledge citation completeness
shadow mode improvement over baseline
```

必须拆分三类评估：

```text
Offline historical eval:
  只能评估已执行交易上的 scorer 表现。
  不得声称准确知道 blocked trade 的真实收益。

Shadow eval:
  实盘旁路运行，只记录 scorer / LLM / final gate 建议，不改变真实交易。
  用于估计建议分布、命中率、延迟、告警质量、人工复核负载。

Paper / replay eval:
  对候选交易做模拟执行、成本、滑点、成交可得性估计。
  用于估计 false block opportunity cost 和 false allow cost。
```

## 上线流程

```text
1. 建立 deterministic rule baseline。
2. 建立 prompt + RAG baseline。
3. 建立 Logistic Regression baseline。
4. 训练 LightGBM / XGBoost / CatBoost scorer。
5. 做概率校准和 threshold by cost matrix。
6. 训练或提示 LLM audit assistant 输出结构化解释。
7. 离线 eval，不允许训练集重叠。
8. shadow / paper 模式运行，只记录建议。
9. 对比 deterministic baseline、RAG baseline、numeric scorer、LLM audit assistant。
10. 满足业务验收后，只允许进入 soft gate 或 human review assist。
11. hard gate 必须单独人工审批，并保留 rollback。
```

## 第一版 POC 推荐

### 模型

```text
Numeric scorer:
  Rule baseline
  Logistic Regression baseline
  LightGBM primary candidate
  XGBoost strong baseline
  CatBoost conditional candidate

LLM assistant:
  Qwen3 Instruct / Thinking small or medium model
  先 RAG + prompt，不急于 fine-tune
  若 schema 输出不稳定，再做 SFT LoRA
```

### 服务

```text
scorer_service:
  输入 trade_candidate_snapshot
  输出 score、calibrated_probability、risk_bucket、top_features

llm_audit_service:
  输入 scorer 输出、CEK-TA RAG 命中、交易上下文摘要
  输出 reason_codes、risk_flags、missing_fields、knowledge_refs、human_review_summary

final_gate_service:
  输入 scorer + LLM audit + deterministic risk
  输出最终 gate_decision
```

### POC 验收

```text
不要求马上提升 PnL。
要求先证明坏交易识别、风险问题发现、缺字段降级、人工复核命中率、引用完整率提升。
```

## 风险与防护

| 风险 | 防护 |
| --- | --- |
| LLM 被误用为最终交易决策者 | LLM 只能输出 recommendation，final gate 由 deterministic engine 执行 |
| 分数未校准 | 必须做 calibration、Brier score、shadow threshold |
| PnL-only 标签污染 | 必须引入 process/risk/rule/execution 多维标签 |
| 数据泄漏 | feature_timestamp、decision_timestamp、input/target separation gate |
| 反事实偏差 | blocked trade 不能直接标亏损，必须 shadow/replay/OPE |
| 过拟合 | walk-forward、purged/embargo split、strategy/regime split |
| 私有策略泄漏 | strategy_version_ref 只能是引用，不存策略正文 |
| RAG 误导 | RAG context 非可信，必须引用来源和 machine_gate |
| 模型不可复现 | release manifest、artifact hash、rollback target |
| 实盘延迟/降级 | latency budget、fail-closed/fail-open、kill switch |
| 人工复核负载爆炸 | review_priority、队列 SLA、抽样复核 |

## 需要审计的问题

请审计以下判断是否成立：

```text
1. 是否同意“数值模型负责核心 scoring/gating，LLM 负责审计解释”的架构？
2. 第一版 numeric scorer 是否应以 LightGBM 为主，Logistic Regression 为 baseline？
3. 是否需要把 XGBoost/CatBoost 作为并行候选？
4. Qwen3 是否只作为 LLM audit assistant，而不是 primary scorer？
5. 第一版是否先做 RAG + prompt，再决定是否 SFT LoRA？
6. POC 是否先以 bad_trade_filter、risk_hit_rate、human_review_precision、citation completeness 验收，而不是直接以 PnL 验收？
7. 是否需要新增 Phase 38：模型选型、训练平台、POC 训练闭环知识扩展？
```

## 进入 POC 前的 6 个硬条件

```text
1. 明确 scorer / soft gate / final gate 的权限边界。
2. 建立 decision-time feature contract 和 leakage unit test。
3. 建立独立 calibration set 与 cost-based threshold policy。
4. 建立 shadow / paper / replay / OPE 评估框架。
5. 建立 LLM strict schema、citation resolver、abstain 机制。
6. 建立 release manifest、rollback、kill switch 和人工审批链路。
```

未满足以上条件，不得进入 hard gate 或实盘自动放行。

## Phase 38 建议拆分

```text
Phase 38.1 数据契约与泄漏审计
  - trade_candidate_snapshot schema
  - decision_time / feature_available_time / label_observation_end_time
  - leakage_unit_test
  - split_manifest

Phase 38.2 Numeric Scorer POC
  - Rule baseline
  - Logistic Regression baseline
  - LightGBM primary candidate
  - XGBoost strong baseline
  - CatBoost conditional candidate

Phase 38.3 Calibration 与 threshold
  - calibration holdout
  - reliability diagram
  - Brier / ECE / calibration slope
  - cost matrix
  - threshold policy version

Phase 38.4 LLM Audit Assistant
  - RAG + prompt baseline
  - strict schema output
  - reason_code taxonomy
  - citation resolver
  - unsupported_claim detector
  - no-source abstain

Phase 38.5 Shadow / Paper / OPE
  - offline eval
  - shadow eval
  - replay eval
  - false allow / false block cost
  - human review precision

Phase 38.6 Governance / Release
  - model registry
  - dataset/model/prompt/rag hash
  - approval workflow
  - rollback
  - kill switch
  - audit report template
```

## 建议下一步

```text
1. 基于本方案创建 Phase 38 任务卡。
2. 为 numeric scorer、LLM audit assistant、final gate 分别定义 API 契约。
3. 建立训练数据 schema：numeric scorer dataset 与 LLM audit SFT example 分离。
4. 创建第一批知识采集任务：meta-labeling、GBDT、校准、conformal、shadow eval、OPE、LLM audit assistant。
5. 输出外接项目 POC 技术路线。
```
