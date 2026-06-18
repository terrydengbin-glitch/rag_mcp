# Phase 37 Quant Foundation 阻断项补证记录

生成日期：2026-06-11

## 任务边界

本记录属于 `CEK-TA-381`，只为 `P37-A-Q02/Q06/Q11` 补充 reviewed-preparation 阻断证据并导出再审包。

不做：

```text
不创建 formal reviewed
不创建 approved
不启用 default guidance
不启用 hard gate
不生成买卖点、仓位、杠杆、止损止盈或实盘执行建议
```

## 补证摘要

### P37-A-Q02 - R-multiple 页码级书籍证据补强

候选：`cand_20260611_phase37_r_multiple_definition_001`

文件：`codex-expert-kit/rag/candidates/KB_01_QUANT_FOUNDATION/cand_20260611_phase37_r_multiple_definition_001.json`

补证目标：

```text
reviewed/caveat_only 准备再审
```

补丁后 statement：

```text
R-multiple 将单笔交易盈亏表达为相对初始风险单位 R 的倍数；它是风险归一化的交易结果指标，可用于复盘、结果比较、标签候选和研究评估，但必须受成本、滑点、样本量、回撤和验证边界约束。
```

新增或强化证据：

- `src_phase37_q02_tharp_position_sizing_toc_page_refs`：Van Tharp's Definitive Guide to Position SizingSM - Table of Contents page references - https://nexusfi.com/attachments/893d1248578892
  - 用途：目录页明确列出 R、R-multiples、total risk tracking、initial risk、expectancy 和 variability 的页码区间，可作为 R-multiple 本体来源的页码级证据线索。
  - 页码线索：TOC: Chapter 2 Risk (R) and R-Multiples, p.11; TOC: Understanding R-Multiples, p.12; TOC: Using Your Total Risk to Keep Track of Your R-Multiples, p.14; TOC: What If You Don’t Know Your Initial Risk?, p.16; TOC: More Thoughts about Expectancy, p.18; TOC: What about the Variability?, p.19; TOC: So What’s the Downside?, p.21
- `src_phase37_q02_van_tharp_expectancy_r_distribution`：Tharp Think Trading Concepts - https://vantharpinstitute.com/tharp-think-trading-concepts/
  - 用途：网页说明交易系统可由其生成的 R-multiple distribution 表征，expectancy 是平均 R-multiple；同时给出按 R 记录交易结果的示例和样本量 caveat。

保留边界：

```text
candidate-only；等待外部严格再审；approved/default guidance/hard gate 全部禁用。
```

### P37-A-Q06 - 仓位 sizing 交易规则与 AI 治理边界拆分

候选：`cand_20260611_phase37_position_sizing_requires_risk_unit_001`

文件：`codex-expert-kit/rag/candidates/KB_01_QUANT_FOUNDATION/cand_20260611_phase37_position_sizing_requires_risk_unit_001.json`

补证目标：

```text
reviewed/caveat_only 准备再审
```

补丁后 statement：

```text
仓位 sizing 的交易规则本体应限定为：进入仓位计算前必须有账户风险预算、单笔风险单位、止损或失效边界、最大暴露和杠杆/保证金边界；AI/RAG 只能提示缺字段或路由人工复核，不能自行推导仓位。
```

新增或强化证据：

- `src_phase37_q06_investor_gov_margin_larger_losses`：Investor Bulletin: Understanding Margin Accounts - https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-29
  - 用途：Investor.gov 说明 margin 会提高购买力，同时暴露于更大损失风险。
- `src_phase37_q06_cek_ta_phase38_runtime_contract_missing_field`：CEK-TA Phase 38 AI scoring gate runtime contract - docs/contracts/phase38_ai_scoring_gate_runtime_contract.md
  - 用途：该契约定义 LLM audit 负责解释 scorer 输出、生成 reason code、missing field 与人工复核摘要；unsupported_claims 不为空时 final gate 不得因 LLM 输出而放行。
- `src_phase37_q06_crosstrade_position_sizing_risk_stop`：Position Sizing - https://crosstrade.io/learn/risk-management/position-sizing
  - 用途：支持按账户风险、止损距离和合约/资产波动来确定仓位 sizing，而不是 AI 自行推导。

保留边界：

```text
candidate-only；等待外部严格再审；approved/default guidance/hard gate 全部禁用。
```

### P37-A-Q11 - 样本量、regime 与 non-stationarity 泛化边界补证

候选：`cand_20260611_phase37_sample_size_and_regime_caveat_001`

文件：`codex-expert-kit/rag/candidates/KB_01_QUANT_FOUNDATION/cand_20260611_phase37_sample_size_and_regime_caveat_001.json`

补证目标：

```text
reviewed/caveat_only 准备再审
```

补丁后 statement：

```text
交易系统评价必须声明样本数量、样本时期、市场状态、资产范围和验证方式；样本过小、只覆盖单一 regime，或未处理金融市场 non-stationarity 时，不得泛化为跨市场、跨周期或跨状态规则。
```

新增或强化证据：

- `src_phase37_q11_lseg_market_regime_detection`：Market regime detection using Statistical and ML based approaches - https://developers.lseg.com/en/article-catalog/article/market-regime-detection
  - 用途：说明金融市场微观结构行为会随时间变化，并可形成连续相似条件的 market regimes，需要识别 regime 及其 shifts。
- `src_phase37_q11_ssga_decoding_market_regimes`：Decoding Market Regimes with Machine Learning - https://www.ssga.com/library-content/assets/pdf/global/pc/2025/decoding-market-regimes-with-machine-learning.pdf
  - 用途：该研究将 market-regime analysis 描述为金融研究的重要工具，识别 1995-2024 年多个市场 regime，并比较不同 regime 下资产表现，支撑按 market state 限定结论边界。
- `src_phase37_q11_ucl_nonstationarity_financial_timeseries`：Non Stationarity and Market Structure Dynamics in Financial Time Series - https://discovery.ucl.ac.uk/10165624/1/Procacci_Thesis.pdf
  - 用途：研究指出金融系统结构会随时间变化，non-stationarity 是金融系统关键特征，并挑战经典统计假设。

保留边界：

```text
candidate-only；等待外部严格再审；approved/default guidance/hard gate 全部禁用。
```

## 再审入口

`docs/audit/phase37_quant_foundation_blocked_supplemental_reaudit_package_20260611.json`
