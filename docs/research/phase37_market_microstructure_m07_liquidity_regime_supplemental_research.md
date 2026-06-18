# Phase 37 Market Microstructure M07 补证研究

## 任务

CEK-TA-410 为 `P37-D-M07 microstructure.liquidity_regime_required.v1` 补充 reviewed/caveat_only 阻断项证据。

## 审计阻断点

上一轮 reviewed-preparation 审计认为：ECB/NBER/CFA 足以支持 liquidity stress caveat，但不足以支持 `rollover`、`session-specific`、休市前后、`halts/auction` 等完整 regime 边界。因此本轮只补这些直接证据，不把候选升级为正式知识。

## 补证来源

### src_m07_nyse_trading_information_sessions_auctions

- 标题：Trading Information
- 链接：https://www.nyse.com/trade/trading-information
- 类型：official_exchange_trading_rules
- 发布方：NYSE
- 证据作用：NYSE documents pre-opening, early, core and late trading sessions, plus core open and closing auction timing. This supports session-specific liquidity regime boundaries.
- 使用边界：NYSE-specific; external projects must map their own venue sessions and auctions.；Supports session and auction taxonomy, not a profitable signal.

### src_m07_nyse_hours_calendars_holidays

- 标题：Holidays & Trading Hours
- 链接：https://www.nyse.com/markets/hours-calendars
- 类型：official_exchange_calendar
- 发布方：NYSE
- 证据作用：NYSE publishes holiday and early-close schedules. This supports treating holiday and early-close periods as separate liquidity regime contexts.
- 使用边界：NYSE equity-market calendar only; not universal across futures, crypto or non-US markets.

### src_m07_nasdaq_trade_halt_codes

- 标题：Trading Halts Code
- 链接：https://nasdaqtrader.com/Trader.aspx?id=TradeHaltCodes
- 类型：official_exchange_halt_status_doc
- 发布方：Nasdaq Trader
- 证据作用：Nasdaq publishes halt code categories such as news pending, news released, single-stock trading pause and extraordinary market activity. This supports explicit halt/pause regime labels.
- 使用边界：Nasdaq equity halt-code semantics; other venues may use different status codes.

### src_m07_nasdaq_halt_cross_rule

- 标题：Nasdaq Equity Trading Rules
- 链接：https://listingcenter.nasdaq.com/rulebook/nasdaq/rules/Nasdaq%20Equity%204
- 类型：official_exchange_rulebook
- 发布方：Nasdaq
- 证据作用：Nasdaq rules reference halt/pause handling and re-opening through a Halt Cross process. This supports auction/reopen specific regime boundaries after halts.
- 使用边界：Rulebook source supports venue process boundaries, not a trading edge or execution permission.

### src_m07_cme_holiday_trading_hours

- 标题：CME Group Holiday and Trading Hours
- 链接：https://www.cmegroup.com/trading-hours.html
- 类型：official_exchange_calendar
- 发布方：CME Group
- 证据作用：CME Group provides holiday schedules and product-filtered trading hours. This supports futures-specific holiday/session regime mapping.
- 使用边界：CME-specific; products may have different holiday hours and trading sessions.

### src_m07_cme_expiration_calendar

- 标题：Expirations Calendar
- 链接：https://www.cmegroup.com/tools-information/calendars/expiration-calendar.html
- 类型：official_exchange_contract_calendar
- 发布方：CME Group
- 证据作用：CME provides important dates for futures and options expirations, deliveries, settlements and other key trading events. This supports expiration-event regime boundaries.
- 使用边界：Calendar source; product-specific contract specs still need to be mapped by the external project.

### src_m07_cme_equity_index_roll_dates

- 标题：Equity Index Roll Dates
- 链接：https://www.cmegroup.com/trading/equity-index/rolldates.html
- 类型：official_exchange_roll_calendar
- 发布方：CME Group
- 证据作用：CME explains roll dates for equity index futures and notes that the lead month can change because the near expiring contract will terminate soon and may become less liquid. This directly supports rollover liquidity regime tagging.
- 使用边界：Equity-index futures specific; other futures families need their own roll rules.

### src_m07_databento_status_schema

- 标题：Status schema
- 链接：https://databento.com/docs/schemas-and-data-formats/status
- 类型：vendor_schema_doc
- 发布方：Databento
- 证据作用：Databento status schema provides updates about trading sessions, halts, pauses, auction starts and matching engine statuses. This supports using vendor market-status data to label liquidity regimes.
- 使用边界：Vendor schema; availability and granularity vary by publisher and dataset.

## CEK-TA liquidity regime taxonomy v1

本 taxonomy 是 CEK-TA 内部标签契约，不是外部交易所、监管或行业通用标准。外接项目必须把自己的交易日历、market status、合约规格和数据供应商字段映射到这些逻辑标签。

| 标签 | 含义 | 必需证据 |
| --- | --- | --- |
| `normal_continuous` | 交易所正常连续交易时段，且无已知 halt、auction、holiday、rollover 或异常状态。 | venue_session_calendar, market_status_or_no_halt_evidence |
| `pre_open_or_open_auction` | 开盘前、开盘集合竞价或 opening cross 周边。 | exchange_auction_rules, session_time_boundary |
| `closing_auction_or_close` | 收盘集合竞价、收盘失衡冻结期或 close 周边。 | exchange_auction_rules, session_time_boundary |
| `holiday_or_early_close` | 交易所假日、节假日前后、提前收盘或节假日修改交易时段。 | exchange_holiday_calendar, early_close_schedule |
| `halt_pause_reopen` | 交易暂停、halt、pause、re-open 或 halt cross/reopen auction 周边。 | halt_code_or_market_status, reopen_or_cross_rule_if_applicable |
| `rollover_or_expiry` | 期货/期权合约换月、临近 last trading day、expiration、delivery 或 settlement 事件周边。 | contract_expiration_calendar, roll_schedule_or_product_contract_spec |
| `stressed_liquidity` | 市场/资金流动性压力、波动异常、成交与报价质量恶化或风控复核触发状态。 | liquidity_stress_source, project_defined_detection_rule |
| `thin_or_off_hours` | 盘前、盘后、隔夜、低成交、低深度或非核心交易时段。 | session_calendar, volume_depth_or_spread_threshold_policy |

## 仍然禁止

```text
1. 不得创建 approved。
2. 不得开启 default guidance。
3. 不得开启 hard gate。
4. 不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。
5. 不得把 CEK-TA 内部 regime 标签说成外部通用标准。
```
