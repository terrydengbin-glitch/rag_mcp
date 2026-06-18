# Phase 37 Trade Analysis Review Contract

```text
contract_id: phase37_trade_analysis_review_contract
version: 1.0.0
status: reviewed_preparation_evidence
owner: Trading Engineering / Trade Analysis
created_at: 2026-06-12
encoding: UTF-8
```

## 目标

本契约为 Phase 37 Trade Analysis 12 条候选提供 reviewed/caveat_only 所需的 CEK-TA 内部字段本体、owner 边界和校验规则。

本契约只服务：

```text
post_trade_review
trade_quality_attribution
label_design
reason_code
bad_case_taxonomy
research_hypothesis_generation
```

本契约不服务：

```text
买卖点生成
仓位建议
杠杆建议
止损止盈参数建议
实盘执行许可
风险阈值数值
default guidance
hard gate
```

## Owner 边界

```text
Quant Foundation:
  负责 R、R-multiple、EV、R/R、成本调整期望值等本体定义。

Trade Analysis:
  负责交易完成后的复盘记录、质量归因、reason code、坏例分类、标签候选和研究假设。

Strategy Engineering:
  负责策略规则、信号、入场/出场规则版本和策略假设。

Data Engineering:
  负责行情、交易日志、订单日志、数据版本、时间戳、数据质量报告。

Replay / Simulation:
  负责模拟成交、fill model、MAE/MFE 路径证据、paper/live gap 的模拟侧解释。

Live Execution:
  负责真实订单、成交、费用、延迟、拒单、撤单、账户/经纪商事实和执行日志。

Risk Management:
  负责风险政策、仓位限制、暴露、亏损限制、最终风控动作和 hard gate。

AI Engineering:
  只能引用 Trade Analysis 字段作为 label、eval case、reason code、RAG 检索或 scoring 解释上下文。
```

Trade Analysis 不得接管 Strategy、Replay、Live Execution 或 Risk Management 的 owner 字段，只能通过 `*_ref`、`*_version`、`*_trace_id` 记录引用关系。

## 通用记录：TradeReviewRecord

每一条交易复盘记录必须包含以下字段。

| 字段 | 必填 | 类型 | 说明 | owner |
| --- | --- | --- | --- | --- |
| review_id | 是 | string | 复盘记录唯一 ID | Trade Analysis |
| trade_id | 是 | string | 交易记录 ID | Trade Analysis |
| trade_plan_id | 是 | string | 入场前交易计划 ID | Strategy / Trade Analysis |
| strategy_id | 是 | string | 策略 ID | Strategy Engineering |
| strategy_rule_version | 是 | string | 策略规则版本 | Strategy Engineering |
| data_version | 是 | string | 复盘使用的数据版本 | Data Engineering |
| market_context_id | 是 | string | 市场上下文引用 | Data / Microstructure |
| market_regime_id | 否 | string | 市场状态/流动性状态引用 | Market Microstructure |
| risk_policy_id | 是 | string | 风险政策引用 | Risk Management |
| order_trace_id | 否 | string | 订单链路追踪 ID | Live Execution |
| fill_trace_id | 否 | string | 成交链路追踪 ID | Live Execution |
| replay_trace_id | 否 | string | 回放/模拟链路 ID | Replay / Simulation |
| reviewer_id | 是 | string | 复盘人或复盘系统 ID | Trade Analysis |
| reviewed_at | 是 | datetime | 复盘时间 | Trade Analysis |
| audit_trace_id | 是 | string | 审计链路 ID | Trade Analysis |
| schema_version | 是 | string | 本记录 schema 版本 | Trade Analysis |

校验规则：

```text
1. trade_plan_id 必须早于真实入场或模拟入场产生。
2. strategy_rule_version、data_version、risk_policy_id 不允许为空。
3. order_trace_id、fill_trace_id 如不存在，必须声明 missing_reason。
4. audit_trace_id 必须可追踪到来源、计算、人工/系统复盘动作。
5. 不得只保存 PnL 而不保存计划、实际、风险、执行、市场状态和规则符合性上下文。
```

## T01：Planned vs Realized R Decomposition

字段表：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| planned_initial_risk_amount | 是 | decimal | 入场前计划的初始风险金额 |
| planned_initial_risk_unit | 是 | string | 初始风险单位，如 account_currency、quote_currency |
| planned_reward_r | 否 | decimal | 入场前计划收益目标的 R 倍数 |
| planned_risk_reward_ratio | 否 | decimal | 入场前计划 R/R |
| actual_gross_pnl | 是 | decimal | 未扣成本前盈亏 |
| actual_net_pnl | 是 | decimal | 扣除费用、滑点、资金费等后的净盈亏 |
| realized_r | 是 | decimal | actual_net_pnl / planned_initial_risk_amount |
| fee_amount | 否 | decimal | 费用 |
| slippage_amount | 否 | decimal | 滑点或成交偏离 |
| risk_basis | 是 | enum | initial_stop / policy_risk / manual_declared_r |
| cost_basis | 是 | enum | net_of_fees / gross_only / partial_cost |
| exit_basis | 是 | enum | planned_exit / stop / target / manual_exit / risk_exit / system_exit |
| calculation_currency | 是 | string | 计算币种 |
| calculation_trace_id | 是 | string | 计算链路 |

校验规则：

```text
1. realized_r 必须使用入场前计划的 initial risk 作为分母。
2. 若 planned_initial_risk_amount 缺失，不得计算 realized_r，只能标记 insufficient_plan.
3. actual_net_pnl 必须声明成本范围；不能只用最终 PnL 判断执行质量。
4. 本分解只能用于复盘和标签，不能推导下一笔交易的买卖点、仓位或止损止盈。
```

## T02：MAE / MFE Calculation Contract

字段表：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| price_path_source_id | 是 | string | 价格路径来源 |
| path_granularity | 是 | enum | tick / quote / order_book / bar |
| path_start_time | 是 | datetime | 路径开始时间 |
| path_end_time | 是 | datetime | 路径结束时间 |
| entry_price | 是 | decimal | 入场价格 |
| exit_price | 是 | decimal | 出场价格 |
| mae_price | 否 | decimal | 持仓期间最大不利价格 |
| mfe_price | 否 | decimal | 持仓期间最大有利价格 |
| mae_r | 否 | decimal | MAE 折算成 R |
| mfe_r | 否 | decimal | MFE 折算成 R |
| missing_path_policy | 是 | enum | block_metric / approximate_with_bar / unknown |
| path_quality_flag | 是 | enum | complete / partial / missing / approximated |

校验规则：

```text
1. MAE/MFE 只能在交易结束后计算。
2. path_granularity 为 bar 时必须声明无法证明 bar 内真实路径。
3. 缺失 tick/quote/order path 时不得声称真实 MAE/MFE。
4. MAE/MFE 不得作为事前已知路径或实盘许可。
```

## T03：Bad Trade Taxonomy

基础分类：

```text
plan_violation
risk_violation
execution_error
data_quality_issue
regime_mismatch
cost_or_slippage_mismatch
rule_ambiguity
manual_override
insufficient_context
good_process_bad_outcome
bad_process_good_outcome
```

字段表：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| taxonomy_version | 是 | string | 分类版本 |
| labels | 是 | array[string] | 可多标签 |
| primary_label | 是 | string | 主分类 |
| severity | 是 | enum | low / medium / high |
| evidence_refs | 是 | array[string] | 证据引用 |
| owner | 是 | enum | trade_analysis / strategy / data / replay / live_execution / risk |
| reviewer_note | 否 | string | 复盘说明 |

校验规则：

```text
1. bad trade 标签必须基于证据，不得只根据亏损判定。
2. 多标签允许，但必须指定 primary_label。
3. owner 指向其他分支时，Trade Analysis 只记录引用，不接管本体修复。
```

## T04：Good Loss / Bad Win Policy

字段表：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| outcome_class | 是 | enum | good_loss / bad_win / good_win / bad_loss / inconclusive |
| plan_compliance | 是 | enum | compliant / violated / ambiguous |
| risk_compliance | 是 | enum | compliant / violated / ambiguous |
| execution_quality | 是 | enum | good / degraded / failed / unknown |
| market_context_fit | 是 | enum | fit / mismatch / unknown |
| evidence_refs | 是 | array[string] | 支撑证据 |

校验规则：

```text
1. good_loss 不能等于可复制亏损，bad_win 不能等于必须禁止盈利交易。
2. outcome_class 只用于复盘和训练标签，不得直接改变实时交易规则。
```

## T05-T08：Entry / Exit / Risk / Execution Quality Review

四类质量复盘共享以下结构。

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| quality_dimension | 是 | enum | entry / exit / risk / execution |
| planned_ref | 是 | string | 计划引用 |
| actual_ref | 是 | string | 实际执行引用 |
| rule_ref | 是 | string | 策略或风险规则引用 |
| compliance_status | 是 | enum | compliant / violated / ambiguous / not_applicable |
| deviation_type | 否 | string | 偏离类型 |
| deviation_magnitude | 否 | decimal | 偏离幅度，必须有单位 |
| evidence_refs | 是 | array[string] | 证据引用 |
| owner_ref | 是 | enum | strategy / risk / live_execution / replay / trade_analysis |

额外要求：

```text
entry:
  必须记录 signal_ref、trigger_condition、timeframe、regime、planned_entry、actual_entry。

exit:
  必须记录 planned_exit、actual_exit、exit_reason、path_evidence、MAE/MFE window。

risk:
  必须记录 initial_R、actual_R、position_ref、stop_execution、risk_change_log、risk_policy_ref。

execution:
  必须引用 Live Execution order/fill/audit log，不重复定义真实执行 owner。
```

校验规则：

```text
1. quality review 不得只看 PnL。
2. execution_quality 涉及真实订单或成交时，必须引用 Live Execution owner 产物。
3. risk_quality 涉及风险政策或 hard gate 时，必须引用 Risk Management owner 产物。
```

## T09：Rule Compliance Schema

字段表：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| strategy_rule_version | 是 | string | 策略规则版本 |
| entry_rule_ref | 否 | string | 入场规则 |
| exit_rule_ref | 否 | string | 出场规则 |
| risk_rule_ref | 否 | string | 风险规则 |
| manual_override | 是 | boolean | 是否人工覆盖 |
| violation_type | 否 | enum | missing_plan / early_entry / late_entry / stop_violation / target_violation / size_violation / rule_ambiguity |
| reviewer_id | 是 | string | 复盘人 |
| evidence_refs | 是 | array[string] | 证据引用 |

校验规则：

```text
1. 规则符合性必须绑定 strategy_rule_version。
2. rule_ambiguity 不能自动归咎为违规，必须进入规则修订或研究假设。
```

## T10：Regime Fit Review Contract

字段表：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| market_regime_id | 是 | string | 市场状态引用 |
| liquidity_regime_id | 否 | string | 流动性状态引用 |
| volatility_regime_id | 否 | string | 波动状态引用 |
| session_context_id | 否 | string | 交易时段上下文 |
| strategy_regime_assumption | 是 | string | 策略预期状态 |
| observed_regime | 是 | string | 观测状态 |
| fit_status | 是 | enum | fit / mismatch / unknown |
| mismatch_reason | 否 | string | 不匹配原因 |

校验规则：

```text
1. regime_fit 只能描述交易发生时的上下文匹配，不预测未来状态。
2. 市场状态本体归 Market Microstructure / Data Engineering，Trade Analysis 只记录引用。
```

## T11：Reason Code Taxonomy

字段表：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| reason_code_id | 是 | string | reason code 唯一 ID |
| taxonomy_version | 是 | string | taxonomy 版本 |
| category | 是 | enum | plan / risk / execution / market_regime / data_quality / psychology_or_manual / research |
| severity | 是 | enum | info / low / medium / high |
| owner | 是 | enum | trade_analysis / strategy / risk / live_execution / replay / data / ai |
| multi_label_allowed | 是 | boolean | 是否允许多标签 |
| migration_rule | 否 | string | 版本迁移规则 |

校验规则：

```text
1. reason code 必须有版本。
2. reason code 不等于交易执行动作。
3. category=ai 只能表示 AI 解释或标签问题，不得控制交易。
```

## T12：Research Hypothesis Lifecycle

字段表：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| hypothesis_id | 是 | string | 研究假设 ID |
| source_trade_set_id | 是 | string | 来源交易集合 |
| hypothesis_statement | 是 | string | 假设描述 |
| validation_protocol_id | 是 | string | 验证协议 |
| oos_required | 是 | boolean | 是否需要样本外 |
| cost_check_required | 是 | boolean | 是否需要成本检查 |
| regime_check_required | 是 | boolean | 是否需要分状态检查 |
| promotion_criteria | 是 | string | 进入策略规则修订的条件 |
| status | 是 | enum | proposed / testing / rejected / validated / promoted |
| promoted_strategy_rule_version | 否 | string | 若提升为策略规则，记录版本 |

校验规则：

```text
1. 复盘发现必须先进入 hypothesis，再由 Strategy / Backtest / Replay / Risk 等分支验证。
2. status=validated 不等于可实盘。
3. promoted 前必须有独立验证、成本、样本、状态和 owner 审计。
```

## 跨分支冲突处理

```text
1. 如果 trade_analysis 字段与 Quant Foundation 的 R 定义冲突，以 Quant Foundation 为准。
2. 如果 trade_analysis 字段与 Live Execution 的真实订单/成交冲突，以 Live Execution 事实层为准。
3. 如果 trade_analysis 字段与 Risk Management 的风控状态冲突，以 Risk Management policy/audit 为准。
4. 如果 trade_analysis 复盘结论与 Strategy 规则冲突，生成 research_hypothesis，不直接改策略。
5. 如果 AI Engineering 使用 Trade Analysis 标签，必须引用 reason_code_id、taxonomy_version 和 review_id。
```

## Machine Gate

```json
{
  "default_guidance": "caveat_only",
  "approved_allowed": false,
  "default_guidance_allowed": false,
  "hard_gate_allowed": false,
  "risk_threshold_advice_allowed": false,
  "trade_execution_advice_allowed": false,
  "requires_human_escalation": true
}
```

## Reviewed/Caveat 允许条件

候选知识进入 formal reviewed/caveat_only 前必须满足：

```text
1. 至少 3 个来源或 1 个 CEK-TA 内部字段契约 + 2 个外部支撑来源。
2. source_evidence 不为空。
3. conflict_status 不得为 unresolved。
4. 字段 owner 清晰。
5. 不输出交易建议、风险阈值或 hard gate。
6. machine_gate.default_guidance 只能是 caveat_only。
7. approved_allowed/default_guidance_allowed/hard_gate_allowed 必须全部为 false。
```
