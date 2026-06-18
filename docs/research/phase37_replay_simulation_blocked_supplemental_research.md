# Phase 37 Replay / Simulation R02/R10/R12 阻断项补证研究

生成日期：2026-06-12

## 任务目标

`CEK-TA-432` 只为 R02/R10/R12 补充内部契约和 schema extract，并导出 reviewed/caveat_only 再审包。

## 内部契约

- 契约路径：`docs/contracts/phase37_replay_simulation_execution_assumption_contract.md`
- 契约 SHA256：`8594bfd05c0e59422602feaec68b73af3a584a278bbf784fe4ce0245d653357f`
- schema_extract_id：`phase37_replay_simulation_execution_assumption_schema_extract_v1`

## 补证对象

### P37-F-R02 / cand_20260611_phase37_replay_simulation_ohlc_same_bar_tp_sl_ordering_required_001

- schema object：`same_bar_fill_ordering`
- claim：仅有 OHLC bar 且同一根 K 内同时触达止盈和止损时，系统不能声称知道真实先后顺序；必须声明 tick_replay、conservative、optimistic、next_bar_only 或 unknown_ordering_blocked 处理假设。
- 补证重点：内联 same_bar_fill_ordering schema，定义 tick_replay、conservative、optimistic、next_bar_only、unknown_ordering_blocked 的字段和判定规则。

### P37-F-R10 / cand_20260611_phase37_replay_simulation_simulation_live_gap_report_required_001

- schema object：`simulation_live_gap_report`
- claim：从 simulation / paper 进入 live 前，必须生成 simulation_live_gap_report，记录模拟与真实订单、成交、费用、延迟、拒单、订单状态和风控触发差异；该报告用于审计模拟证据，不等于实盘许可。
- 补证重点：内联 simulation_live_gap_report schema，定义模拟/实盘成交价格、数量、延迟、拒单、费用、订单状态、风控触发、缺失字段和 owner 边界。

### P37-F-R12 / cand_20260611_phase37_replay_simulation_execution_cost_consistency_required_001

- schema object：`execution_cost_mapping`
- claim：Backtest、Replay、Paper 和 Live 的费用、spread、slippage、market impact 与 fill model 必须有 execution_cost_mapping 版本化映射；成本口径不一致时不能直接比较表现。
- 补证重点：内联 execution_cost_mapping schema，定义 Backtest、Replay、Paper、Live 之间费用、spread、slippage、market impact 和 fill model 的版本化映射与 owner 边界。

## 审计边界

```text
1. candidate 不是正式知识。
2. 本包最多允许 accepted_for_reviewed_caveat_only。
3. 不允许 approved。
4. 不允许 default guidance。
5. 不允许 hard gate。
6. 不允许生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。
```

## 来源使用边界

外部框架、平台、FIX 或 broker 文档只用于说明实现模式和字段方向；CEK-TA exact field、owner mapping、workflow gate 由内部契约支撑。
