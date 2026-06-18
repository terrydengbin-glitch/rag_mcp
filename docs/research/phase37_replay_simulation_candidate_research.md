# Phase 37 Replay / Simulation Candidate Research

- generated_at: 2026-06-11
- task_id: CEK-TA-424
- partition: KB_05_REPLAY_SIMULATION
- candidate_count: 12
- gate_status: pass

## 来源种子

- `quantconnect_fills`: Trade Fills - Key Concepts (QuantConnect) - https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts
- `quantconnect_slippage`: Slippage Models - Key Concepts (QuantConnect) - https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/slippage/key-concepts
- `quantconnect_fees`: Transaction Fees - Key Concepts (QuantConnect) - https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/transaction-fees/key-concepts
- `quantconnect_brokerage`: Reality Modelling - Brokerage Models (QuantConnect) - https://www.quantconnect.com/docs/v1/algorithm-reference/reality-modelling
- `backtrader_order_execution`: Orders - Creation/Execution (Backtrader) - https://www.backtrader.com/docu/order-creation-execution/order-creation-execution/
- `backtrader_slippage`: Broker - Slippage (Backtrader) - https://www.backtrader.com/docu/slippage/slippage/
- `backtrader_cheat_open`: Broker - Cheat-On-Open (Backtrader) - https://www.backtrader.com/docu/cerebro/cheat-on-open/cheat-on-open/
- `hftbacktest_order_fill`: Order Fill (HftBacktest) - https://hftbacktest.readthedocs.io/en/latest/order_fill.html
- `hftbacktest_latency`: Latency Models (HftBacktest) - https://hftbacktest.readthedocs.io/en/latest/latency_models.html
- `hftbacktest_project`: hftbacktest project (HftBacktest) - https://github.com/nkaz001/hftbacktest
- `ibkr_tws_api`: TWS API Documentation (Interactive Brokers) - https://www.interactivebrokers.com/campus/ibkr-api-page/trader-workstation-api/
- `ibkr_order_types`: Order Types (Interactive Brokers) - https://www.interactivebrokers.com/campus/ibkr-api-page/order-types/
- `fix_execution_report`: Execution Report <8> message - FIX 4.4 (OnixS FIX Dictionary) - https://www.onixs.biz/fix-dictionary/4.4/msgtype_8_8.html
- `fix_ordstatus`: OrdStatus <39> field - FIX 4.4 (OnixS FIX Dictionary) - https://www.onixs.biz/fix-dictionary/4.4/tagnum_39.html
- `binance_filters`: Filters (Binance Open Platform) - https://developers.binance.com/docs/binance-spot-api-docs/filters
- `cme_matching`: Matching Algorithm Overview (CME Group) - https://www.cmegroup.com/education/matching-algorithm-overview

## 候选知识点

- `P37-F-R01` `replay.event_clock_required.v1`: Replay / Simulation 必须声明事件时钟、撮合时点、信号生成时点和订单提交时点；未声明事件顺序的模拟结果不能作为执行质量或策略可交易性的证据。
- `P37-F-R02` `replay.ohlc_same_bar_tp_sl_ordering_required.v1`: 仅有 OHLC bar 时，同一根 K 内同时触达止盈和止损不能声称真实先后顺序；系统必须显式声明 conservative、optimistic、next-bar 或 tick-replay 等处理假设。
- `P37-F-R03` `replay.fill_model_assumption_required.v1`: Simulation 中的 market、limit、stop、stop-limit 和 auction 成交必须绑定 fill model 假设，包括价格来源、数量可得性、spread、滑点、队列/流动性限制和适用市场。
- `P37-F-R04` `replay.partial_fill_policy_required.v1`: Replay / Simulation 必须定义 partial fill、no fill、残量、超时、取消和后续状态更新策略；不能默认所有订单都完整成交。
- `P37-F-R05` `replay.latency_model_required.v1`: Simulation 必须声明行情延迟、决策延迟、订单发送延迟、交易所确认延迟和回报延迟；没有延迟模型的高频或盘中执行模拟只能作为粗略研究。
- `P37-F-R06` `replay.paper_trading_not_equal_live.v1`: Paper trading、模拟盘或沙盒执行只能验证系统流程和部分执行假设，不能等同于真实成交、真实滑点、真实拒单、真实延迟或真实风控表现。
- `P37-F-R07` `replay.exchange_rule_simulation_required.v1`: Replay / Simulation 若声称接近实盘，必须按市场和品种映射交易所/经纪商规则，包括交易时段、撮合算法、订单类型、最小数量、价格步长、涨跌停/暂停和拒单条件。
- `P37-F-R08` `replay.minimum_order_size_required.v1`: Simulation 必须校验交易所或经纪商的最小数量、步长、最小名义金额、价格精度和订单类型限制；未通过约束的订单应被模拟为拒单或不可提交。
- `P37-F-R09` `replay.order_reject_and_cancel_policy_required.v1`: Replay / Simulation 必须定义订单拒绝、撤单、撤改单、过期、pending 状态和回报缺失的处理；不能只模拟 filled 状态。
- `P37-F-R10` `replay.simulation_live_gap_report_required.v1`: 从 simulation / paper 进入 live 前，必须记录成交价格、成交数量、延迟、拒单、滑点、费用、订单状态和风控触发的模拟-实盘差异报告。
- `P37-F-R11` `replay.tick_replay_vs_ohlc_boundary.v1`: Tick/order-book replay 可以提供比 OHLC replay 更细的路径和队列信息，但仍不能改变历史市场；OHLC replay 不能伪装成 tick 级成交真实性。
- `P37-F-R12` `replay.execution_cost_consistency_required.v1`: Backtest、Replay、Paper 和 Live 的费用、spread、滑点、market impact 与 fill 假设必须有版本化映射；成本口径不一致时不能直接比较表现。

## 边界

- 本批候选只处理 replay/simulation 规则本体，不处理实盘下单权限、账户事实、仓位建议或策略收益声明。
- 候选不得直接进入 reviewed、approved、default guidance 或 hard gate。
