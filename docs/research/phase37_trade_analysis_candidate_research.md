# Phase 37 Trade Analysis Candidate Research

- generated_at: 2026-06-12
- task_id: CEK-TA-442
- partition: KB_07_TRADE_ANALYSIS
- candidate_count: 12
- gate_status: pass

## 来源种子

- `cfa_trade_execution`: Trade Strategy and Execution (CFA Institute) - https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution
- `cfa_performance_attribution`: Return-Based, Holdings-Based and Transaction-Based Performance Attribution (AnalystPrep / CFA Level III study note) - https://analystprep.com/study-notes/cfa-level-iii/return-based-holdings-based-and-transaction-based-performance-attribution-2/
- `van_tharp_concepts`: Tharp Think Trading Concepts (Van Tharp Institute) - https://vantharpinstitute.com/tharp-think-trading-concepts/
- `trademetria_mae_mfe`: Understanding MAE and MFE Metrics (Trademetria) - https://trademetria.com/blog/understanding-mae-and-mfe-metrics-a-guide-for-traders/
- `tradersync_mae_mfe`: MFE and MAE Metrics (TraderSync) - https://tradersync.com/mfe-and-mae-metrics/
- `tradezella_rr`: Risk-Reward Ratio: How to Calculate and Use It (TradeZella) - https://www.tradezella.com/blog/risk-reward-ratio
- `tradesviz_trade_plan`: Mastering Your Trading with R-Value and Profit Factor in TradesViz (TradesViz) - https://www.tradesviz.com/blog/what-is-r-value-profit-factor/
- `quantconnect_results`: Backtesting Results (QuantConnect) - https://www.quantconnect.com/docs/v2/cloud-platform/backtesting/results
- `bailey_pbo`: The Probability of Backtest Overfitting (SSRN) - https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253
- `white_reality_check`: A Reality Check for Data Snooping (Econometrica / JSTOR) - https://www.jstor.org/stable/2669537
- `ssrn_execution_quality`: The Role of Trading in Portfolio Performance Attribution (SSRN) - https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2928963

## 候选知识点

- `P37-H-T01` `trade_analysis.planned_vs_realized_r_required.v1`: 交易复盘必须区分入场前计划的 risk/reward 或计划 R 与出场后的 realized R；不能只用最终 PnL 判断执行质量。
- `P37-H-T02` `trade_analysis.mae_mfe_for_post_trade_only.v1`: MAE/MFE 应作为 post-trade 复盘、止损止盈研究和执行质量分析指标；不能在事前被当作已知路径或直接生成入场/出场建议。
- `P37-H-T03` `trade_analysis.bad_trade_taxonomy_required.v1`: 交易复盘必须把坏交易按计划错误、规则破坏、入场质量、出场质量、风险质量、执行质量、市场状态不匹配和数据/系统问题分类，而不是只标记亏损。
- `P37-H-T04` `trade_analysis.good_loss_bad_win_distinction.v1`: 复盘必须区分遵守规则但亏损的 good loss 与违反计划但盈利的 bad win；不能把盈利自动标记为好交易，也不能把亏损自动标记为坏交易。
- `P37-H-T05` `trade_analysis.entry_quality_review_required.v1`: 入场质量复盘必须记录信号、触发条件、时间框架、市场状态、计划价差、延迟和是否按规则入场；不能由最终盈亏倒推出入场正确。
- `P37-H-T06` `trade_analysis.exit_quality_review_required.v1`: 出场质量复盘必须记录计划出场、实际出场、MAE/MFE、滑点、提前/延后出场原因和规则符合性；不能只用是否盈利判断出场质量。
- `P37-H-T07` `trade_analysis.risk_quality_review_required.v1`: 风险质量复盘必须记录初始风险 R、实际承担风险、仓位、止损执行、风险变更、规则是否被移动或放宽；不能只用收益覆盖风险问题。
- `P37-H-T08` `trade_analysis.execution_quality_review_required.v1`: 执行质量复盘必须记录订单、成交、滑点、费用、延迟、拒单、撤单、机会成本和 broker/venue/algorithm 表现；不能把策略信号质量和执行质量混在一起。
- `P37-H-T09` `trade_analysis.rule_compliance_review_required.v1`: 每笔交易必须记录策略规则、入场/出场规则、风控规则和人工 override 是否被遵守；rule compliance 不能由 PnL 替代。
- `P37-H-T10` `trade_analysis.regime_fit_review_required.v1`: 交易复盘必须记录市场状态、波动率、流动性、趋势/震荡、交易时段和策略适配情况；不能把单笔输赢直接归因于策略有效或无效。
- `P37-H-T11` `trade_analysis.reason_code_required.v1`: 交易复盘、LLM scoring 和坏例分析必须使用稳定 reason code 描述交易原因、错误类型、执行问题和风险问题；不能只保存自由文本评论。
- `P37-H-T12` `trade_analysis.research_hypothesis_requires_validation.v1`: 交易复盘中发现的 pattern、错误归因或改进假设只能作为 research hypothesis，必须经过样本外、参数稳定性、成本和市场状态验证后才能进入策略规则。

## 边界

- 本批候选只处理 Trade Analysis / 交易复盘规则本体，不处理实盘下单权限、账户事实、仓位建议或策略收益声明。
- AI Engineering 只能引用本批知识设计标签、reason code、eval case 和审计解释，不得复制改写交易规则本体。
- 候选不得直接进入 reviewed、approved、default guidance 或 hard gate。
