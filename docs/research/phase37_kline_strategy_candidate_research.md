# Phase 37 Kline / Strategy Engineering 候选研究记录

生成日期：2026-06-11

## 范围

本批只覆盖 Phase 37 C 组 Kline / Strategy Engineering 12 条候选知识。候选归入运行时知识树和 schema 的 `KB_02_KLINE_STRATEGY`，不是正式知识，不进入默认指导。

历史范围文件中 `KB_03_STRATEGY_ENGINEERING` 属旧命名；当前 `knowledge_tree.md` 和 `metadata_schema.md` 的正式分区为 `KB_02_KLINE_STRATEGY`。

## 候选清单

| research_task_id | candidate_id | tree_node_id | source_count | statement |
| --- | --- | --- | ---: | --- |
| P37-C-K01 | `cand_20260611_phase37_kline_strategy_trend_structure_boundary_001` | `kt.kline_strategy.market_structure` | 4 | K线趋势结构不能只凭主观看图命名；必须声明 higher high/lower low、区间、突破、回撤、支撑阻力或失效条件的识别规则，并说明市场、周期和样本边界。 |
| P37-C-K02 | `cand_20260611_phase37_kline_strategy_market_structure_requires_timeframe_001` | `kt.kline_strategy.market_structure` | 4 | 市场结构、趋势、支撑阻力和突破判断必须绑定时间周期、bar start/end、bar confirmation 和数据可用时点；不得把未确认的高周期 K 线当成已知事实。 |
| P37-C-K03 | `cand_20260611_phase37_kline_strategy_entry_signal_not_equal_trade_decision_001` | `kt.kline_strategy.entry_exit` | 4 | K线形态、指标交叉或突破信号只能作为候选入场条件；完整交易决策还必须经过成本、滑点、风险、止损、止盈、仓位、样本外和执行边界检查。 |
| P37-C-K04 | `cand_20260611_phase37_kline_strategy_stop_loss_requires_invalidation_logic_001` | `kt.kline_strategy.entry_exit` | 4 | 止损不能只写成固定点数或随意百分比；必须说明其与入场假设、结构失效、波动范围、数据粒度和执行模型之间的关系。 |
| P37-C-K05 | `cand_20260611_phase37_kline_strategy_take_profit_requires_reachability_check_001` | `kt.kline_strategy.entry_exit` | 4 | 止盈目标不能只按理想 R 倍数或图形目标声明；必须检查目标在样本、波动、流动性、bar 粒度、fill model、滑点和成本下是否可达。 |
| P37-C-K06 | `cand_20260611_phase37_kline_strategy_multi_timeframe_context_required_001` | `kt.kline_strategy.market_structure` | 4 | 多周期 K 线策略必须说明高低周期数据如何同步、何时确认、是否可能 repaint、如何避免未来数据泄漏，以及每个周期在决策中的职责。 |
| P37-C-K07 | `cand_20260611_phase37_kline_strategy_indicator_lag_boundary_001` | `kt.kline_strategy.indicators` | 4 | 移动平均、振荡器、波动率和成交量类指标都必须声明输入窗口、计算时点、确认规则和滞后边界；不得把指标输出解释为实时无延迟事实。 |
| P37-C-K08 | `cand_20260611_phase37_kline_strategy_atr_volatility_context_required_001` | `kt.kline_strategy.indicators` | 4 | ATR 等波动率指标只能说明历史区间波动或止损/仓位/过滤的候选上下文；必须声明品种、周期、窗口和用途，不能直接声称价格方向或交易胜率。 |
| P37-C-K09 | `cand_20260611_phase37_kline_strategy_rsi_threshold_not_universal_001` | `kt.kline_strategy.indicators` | 4 | RSI 的超买/超卖阈值只能作为带市场、周期、窗口、趋势状态和验证边界的候选解释；不得把 70/30 等阈值写成跨市场通用买卖规则。 |
| P37-C-K10 | `cand_20260611_phase37_kline_strategy_volume_confirmation_boundary_001` | `kt.kline_strategy.indicators` | 4 | 成交量确认只能在声明市场机制、成交量定义、数据源、周期和验证样本后使用；不同交易所、现货/合约、聚合商和缺失数据会改变成交量含义。 |
| P37-C-K11 | `cand_20260611_phase37_kline_strategy_signal_generalization_forbidden_without_market_scope_001` | `kt.kline_strategy` | 4 | 任何 K 线形态、指标、结构或组合信号都不得被描述为跨市场、跨周期、跨样本的通用规律；必须声明训练/研究样本、样本外、成本和冲突边界。 |
| P37-C-K12 | `cand_20260611_phase37_kline_strategy_strategy_rule_version_required_001` | `kt.kline_strategy` | 4 | K线策略规则进入回测、模拟、AI 训练或实盘候选前，必须记录 strategy_rule_version、参数、数据版本、周期、信号计算版本和变更原因，避免复现实验和审计断链。 |

## 来源矩阵

| source_key | title | publisher | type | reliability | role |
| --- | --- | --- | --- | --- | --- |
| `lo_mamaysky_wang` | Foundations of Technical Analysis: Computational Algorithms, Statistical Inference, and Empirical Implementation | SSRN / Journal of Finance | peer_reviewed_paper | high | Lo, Mamaysky and Wang formalize technical pattern recognition and emphasize statistical inference and empirical implementation for technical-analysis claims. |
| `sullivan_timmermann_white` | Data-Snooping, Technical Trading Rule Performance, and the Bootstrap | SSRN / Journal of Finance | peer_reviewed_paper | high | The paper evaluates technical trading rules while accounting for data-snooping bias across a universe of rules. |
| `white_reality_check` | A Reality Check for Data Snooping | Econometrica / Wiley | peer_reviewed_paper | high | White defines data snooping as reusing the same data for inference or model selection and provides a reality-check framework. |
| `cfa_technical_analysis` | Technical Analysis | CFA Institute Research Foundation | professional_literature_review | high | CFA Institute discusses technical analysis, trend, support/resistance, indicators, oscillators, volume and risk-management context. |
| `fidelity_indicators` | Understanding Indicators in Technical Analysis | Fidelity Investments | brokerage_education_reference | medium_high | Fidelity categorizes trend, momentum, volume and volatility indicators and frames them as tools requiring context and risk management. |
| `ta_lib_home` | TA-Lib Technical Analysis Library | TA-Lib | technical_library_official_doc | medium_high | TA-Lib documents a large catalog of technical indicators, including RSI, ATR, moving averages and candlestick pattern recognition. |
| `ta_lib_python` | TA-Lib Python wrapper documentation | TA-Lib Python | technical_library_doc | medium_high | TA-Lib Python documents common indicators and market-data inputs used by trading software developers. |
| `tradingview_other_timeframes` | Other timeframes and data | TradingView | trading_platform_official_doc | medium_high | TradingView documents higher/lower timeframe data requests and behavior differences between historical and realtime bars. |
| `tradingview_repainting` | Repainting | TradingView | trading_platform_official_doc | medium_high | TradingView explains repainting and historical versus realtime behavior for script calculations. |
| `quantconnect_periods` | Periods | QuantConnect | trading_engine_official_doc | medium_high | QuantConnect states that bars have start and end times and are passed to algorithms at end time to avoid unavailable-bar lookahead. |
| `quantconnect_consolidators` | Time Period Consolidators | QuantConnect | trading_engine_official_doc | medium_high | QuantConnect documents time-period consolidators for aggregating data into multiple resolutions. |
| `backtrader_brackets` | Orders - Brackets | Backtrader | backtesting_framework_doc | medium | Backtrader describes bracket orders with main order, stop-side order and limit-side order submitted together. |
| `backtrader_stop` | Stop Trading | Backtrader | backtesting_framework_doc | medium | Backtrader discusses stop-based strategy mechanisms for limiting losses or securing profits. |

## 边界

1. 本批不生成买卖点、仓位、杠杆、止损止盈参数或实盘执行建议。
2. 本批不创建 reviewed、approved、default guidance 或 hard gate。
3. 平台/框架文档只作为工程语义和例子，不作为交易有效性证明。
4. AI Engineering 只能通过 `knowledge_refs` 引用本批规则，不得复制为模型训练或 RAG/MCP 本体规则。

## 质量门禁摘要

```json
{
  "quality_gate": {
    "pass": true,
    "errors": []
  },
  "phase": "37",
  "task_id": "CEK-TA-394",
  "generated_at": "2026-06-11",
  "partition_id": "KB_02_KLINE_STRATEGY",
  "candidate_count": 12,
  "candidate_ready_count": 12,
  "source_count_min": 4,
  "source_count_max": 4,
  "default_guidance_denied_count": 12,
  "tree_nodes": [
    "kt.kline_strategy",
    "kt.kline_strategy.entry_exit",
    "kt.kline_strategy.indicators",
    "kt.kline_strategy.market_structure"
  ],
  "outputs": {
    "candidate_dir": "E:\\collector\\rag\\codex-expert-kit\\rag\\candidates\\KB_02_KLINE_STRATEGY",
    "research_report": "E:\\collector\\rag\\docs\\research\\phase37_kline_strategy_candidate_research.md",
    "generation_report": "E:\\collector\\rag\\docs\\reports\\phase37_kline_strategy_candidate_generation_report.md",
    "quality_gate": "E:\\collector\\rag\\docs\\reports\\phase37_kline_strategy_candidate_quality_gate.json"
  }
}
```
