# Phase 36 能力边界候选补证采集记录

## 任务信息

```text
Phase: Phase 36 AI Engineering gating/scoring 知识扩充
任务 ID: CEK-TA-199
下游任务: CEK-TA-200
创建日期: 2026-06-09
状态: done
```

## 目标

为 Phase 36 第一批 AI 审计中被标记为 `needs_more_evidence` 的 2 条 AI Engineering 能力边界候选补充联网来源、收敛措辞，并导出二次审计包。

本任务不把候选转成正式知识，不设置 `reviewed`，不设置 `approved`，也不允许进入默认指导。

## 上游输入

```text
docs/audit/audit_result_phase36_ai_engineering_batch_01_of_10_20260609_gpt55_pro.json
codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260609_ai_engineering_capability_boundary_llm_not_primary_price_predictor_v1_001.json
codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260609_ai_engineering_capability_boundary_numeric_model_vs_llm_role_split_v1_001.json
```

## 下游输出

```text
docs/research/phase36_capability_boundary_supplemental_research.md
docs/audit/phase36_capability_boundary_supplemental_audit_package_20260609.json
2 条已补证但仍处于 needs_more_evidence 的 candidate JSON
ui/src/data/phase23Candidates.ts
```

## 输入契约

候选必须包含：

```text
candidate_id
status.review_status
classification
claim.statement
claim.normalized_claim
applicability
source_refs
source_quality
conflict_audit
review.ai_audit
workflow
```

## 输出契约

补证后的候选必须满足：

```text
1. 保持 status.review_status = needs_more_evidence。
2. 保持 workflow.stage = needs_more_evidence。
3. 增加可追踪 source_refs。
4. claim.statement 从强断言改为工程安全边界。
5. applicability 增加例外条件和非适用边界。
6. review.audit_log 记录 supplemental_research_added。
7. 二次审计包只要求 accepted_for_draft | needs_more_evidence | rejected，不允许 approved。
```

## 补证对象

| candidate_id | normalized_claim | 当前处理 |
| --- | --- | --- |
| `cand_20260609_ai_engineering_capability_boundary_llm_not_primary_price_predictor_v1_001` | `capability_boundary.llm_not_primary_price_predictor.v1` | 补充 LLM 金融幻觉、数值/时序推理、校准和高影响金融自动化治理证据 |
| `cand_20260609_ai_engineering_capability_boundary_numeric_model_vs_llm_role_split_v1_001` | `capability_boundary.numeric_model_vs_llm_role_split.v1` | 补充职责矩阵、算法交易监督测试、LLM 校准和金融推理限制证据 |

## 联网来源

| source_id | 来源 | 用途 |
| --- | --- | --- |
| `src_acl_2024_llm_confidence_calibration_survey` | A Survey of Confidence Estimation and Calibration in Large Language Models, ACL Anthology, 2024 | 支持 LLM 输出需要置信度估计、校准和不确定性治理，不能直接当作硬执行依据 |
| `src_arxiv_2023_llm_finance_hallucination` | Deficiency of Large Language Models in Finance: An Empirical Examination of Hallucination, arXiv, 2023 | 支持 LLM 在金融任务中存在幻觉风险，尤其历史价格、金融术语等任务需要外部校验 |
| `src_arxiv_2026_fintradebench` | FinTradeBench: A Financial Reasoning Benchmark for LLMs, arXiv, 2026 | 支持当前 LLM 在金融数值和时间序列推理方面仍有挑战，检索对交易信号推理帮助有限 |
| `src_openai_usage_policies_high_impact_finance` | OpenAI Usage Policies, OpenAI | 支持高影响金融活动自动化必须保留人工审查和治理边界 |
| `src_finra_regulatory_notice_15_09` | FINRA Regulatory Notice 15-09, FINRA, 2015 | 支持算法交易系统需要风险评估、软件测试、系统验证、交易系统控制和合规监督 |
| `src_hf_2023_financebench` | FinanceBench: A New Benchmark for Financial Question Answering, Hugging Face Papers, 2023 | 支持金融问答中仍存在错误、拒答和幻觉风险，即使使用检索也需要评估和治理 |

## 内容补丁原则

两条候选的强断言被改成工程安全边界：

```text
不说“LLM 永远不能做价格预测”。
改为“默认不得把 LLM 输出作为 primary numeric price forecasting 或 execution authority”。
```

允许例外必须同时具备：

```text
validated_numeric_model
independent_review
monitoring
rollback
human_approval
```

职责拆分建议：

| 角色 | 可由 LLM 承担 | 应由数值/确定性/人工治理承担 |
| --- | --- | --- |
| 检索 | 可以 | 需要来源门禁 |
| 解释 | 可以 | 需要人工或规则复核高风险结论 |
| 候选评分 | 可以提出建议 | 不得绕过最终 gate |
| reason code | 可以生成草案 | 需要审计追踪 |
| 价格预测 | 默认不作为主权威 | 需要经验证数值模型 |
| 风险阈值 | 不作为最终权威 | 需要确定性风控或人工审批 |
| 仓位与订单执行 | 不允许直接控制 | 需要执行系统、风控和权限控制 |

## 边界

本任务属于 AI Engineering：

```text
包含 LLM 能力边界、职责矩阵、评估、校准、审计和治理。
不包含 K 线规则、价格预测模型、仓位公式、实盘执行、交易风控本体。
```

交易本体仍应路由到 Trading Engineering：

```text
价格预测模型 -> Trading Engineering / Strategy or Quant Foundation
风控阈值和仓位 -> Trading Engineering / Risk Management
订单执行和状态机 -> Trading Engineering / Live Execution
回测和验证 -> Trading Engineering / Backtest
```

## 二次审计要求

二次审计只允许输出：

```text
accepted_for_draft
needs_more_evidence
rejected
```

不得输出：

```text
approved
default_guidance_allowed
machine_gate.allow
```

审计重点：

```text
1. 补证来源是否足以支持改写后的工程安全边界。
2. 是否仍存在过强或过泛化措辞。
3. 是否需要把两条候选合并为一条原则和一条职责矩阵。
4. AI Engineering 与 Trading Engineering 边界是否清楚。
5. 是否还需要内部架构图、模型卡、数据卡或评估报告。
```

## Definition of Done

```text
1. 补证来源已写入 2 条 candidate JSON。
2. 两条候选仍保持 needs_more_evidence。
3. 二次审计包已导出。
4. Vue3 候选 fixture 已重建。
5. 候选工作流校验通过。
6. 知识污染校验通过。
7. 中文文档 UTF-8 无乱码。
```

## 回滚

如二次审计认为证据仍不足：

```text
1. 保持候选 needs_more_evidence。
2. 不生成 formal reviewed 知识。
3. 将缺口追加到 review.open_questions 和下一轮补证任务。
```

如发现来源不适合：

```text
1. 从 candidate source_refs 移除对应 source_id。
2. 降低 source_quality.score。
3. 重新导出二次审计包。
```
