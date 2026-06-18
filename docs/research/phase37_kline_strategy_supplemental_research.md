# Phase 37 Kline / Strategy Engineering 补证研究记录

日期：2026-06-11

## 补证范围

本次只处理首轮严格审计中的 4 条 `needs_more_evidence`：P37-C-K04、P37-C-K05、P37-C-K10、P37-C-K12。

## 补证结果

| research_task_id | candidate_id | 新状态 | source_count | 关键补证方向 |
| --- | --- | --- | ---: | --- |
| P37-C-K04 | `cand_20260611_phase37_kline_strategy_stop_loss_requires_invalidation_logic_001` | `ready_for_reaudit` | 8 | 把原先较强的“必须绑定结构失效”收窄为“必须记录止损规则的风险目的、触发条件、执行假设和失效关系”。; 新增 FINRA、Investor.gov、IBKR 和 CFA 来源支撑 stop/stop-limit 执行不确定性、交易成本和执行风险。; Backtrader 仅保留为框架例子，不作为主来源。 |
| P37-C-K05 | `cand_20260611_phase37_kline_strategy_take_profit_requires_reachability_check_001` | `ready_for_reaudit` | 8 | 把止盈可达性从盈利主张收窄为执行/成交质量假设披露规则。; 新增 CFA TCA、QuantConnect fill/slippage 和 Investor.gov order-risk 来源。; 明确不生成止盈价格、R 倍数参数或实盘执行建议。 |
| P37-C-K10 | `cand_20260611_phase37_kline_strategy_volume_confirmation_boundary_001` | `ready_for_reaudit` | 8 | 新增 Databento OHLCV、trade resampling、official statistics 和 Binance Kline 字段来源支撑 volume 语义差异。; 把一般 TA 成交量确认收窄为数据口径/聚合/质量边界。; 明确成交量确认不是独立交易信号，也不证明突破、反转或方向预测有效。 |
| P37-C-K12 | `cand_20260611_phase37_kline_strategy_strategy_rule_version_required_001` | `ready_for_reaudit` | 7 | 新增 MLflow Tracking、MLflow Dataset Tracking 和 DVC pipeline 来源支撑参数、代码版本、数据版本、输出文件、lineage 和可复现工作流。; White Reality Check 继续作为多次规则搜索和数据复用风险来源，不再单独支撑版本字段本体。; 明确 CEK-TA 不强制 MLflow/DVC，只要求等价的版本追踪字段。 |

## 来源目录

| key | title | publisher | type | role |
| --- | --- | --- | --- | --- |
| `finra_stop_orders` | Stop Orders: Factors to Consider During Volatile Markets | FINRA | regulator_guidance | FINRA explains stop orders and stop-limit orders, including that stop-limit orders may not execute and that volatile markets require careful consideration. |
| `investor_gov_stop_orders` | Investor Bulletin: Stop, Stop-Limit, and Trailing Stop Orders | SEC Investor.gov | regulator_guidance | Investor.gov states that stop prices are not guaranteed execution prices and stop-limit orders may not execute if price moves away. |
| `ibkr_stop_order` | Stop Order | Interactive Brokers | broker_official_doc | Interactive Brokers defines stop orders as market orders triggered by a stop price and notes that a specific execution price is not guaranteed. |
| `cfa_trade_execution` | Trade Strategy and Execution | CFA Institute | professional_body_reference | CFA Institute discusses trade cost analysis, market impact, execution risk, trading policy documents, and execution-quality improvement. |
| `quantconnect_trade_fills` | Trade Fills - Key Concepts | QuantConnect | trading_engine_official_doc | QuantConnect states that fill models determine fill price and quantity, incorporate spread costs, and work with slippage models. |
| `quantconnect_slippage` | Slippage models - Key Concepts | QuantConnect | trading_engine_official_doc | QuantConnect defines slippage as the difference between expected and actual fill price and models it to make backtests more realistic. |
| `databento_ohlcv` | Aggregate bars (OHLCV) | Databento | market_data_vendor_official_doc | Databento defines OHLCV aggregate bars as prices and total volume aggregated from trades over intervals. |
| `databento_custom_ohlcv` | Resampling trades data at a fixed interval | Databento | market_data_vendor_official_doc | Databento explains OHLCV schemas are derived from trades and demonstrates constructing bars by resampling trade data. |
| `databento_statistics` | Statistics schema | Databento | market_data_vendor_official_doc | Databento distinguishes official venue summary statistics from Databento-computed OHLCV bars, including volume fields. |
| `binance_klines` | Kline/Candlestick Data | Binance | exchange_official_doc | Binance spot Kline data includes volume, quote asset volume, number of trades, taker buy base volume and taker buy quote volume. |
| `mlflow_tracking` | ML Experiment Tracking | MLflow | mlops_official_doc | MLflow Tracking logs parameters, code versions, metrics and output files for later visualization and comparison. |
| `mlflow_dataset` | MLflow Dataset Tracking | MLflow | mlops_official_doc | MLflow Dataset Tracking tracks and versions datasets used in training, validation and evaluation with lineage from raw data to predictions. |
| `dvc_pipelines` | Get Started: Data Pipelines | DVC | data_versioning_official_doc | DVC pipelines capture, organize, version and reproduce data science and ML workflows, including pipeline stages and parameters. |

## 质量门禁

```json
{
  "pass": true,
  "errors": []
}
```

## 边界

本次补证不创建 formal reviewed，不创建 approved，不启用 default guidance 或 hard gate，不输出买卖点、仓位、杠杆、止损止盈参数或实盘执行建议。
