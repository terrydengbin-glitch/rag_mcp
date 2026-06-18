# Phase 45 P2 reviewed 阻断项补证记录

## P45-G-DATA04

- Databento Corporate Actions：补充 listed/delisted securities、corporate actions、PIT reference event 语境。
- Nasdaq Daily List：补充 Nasdaq-specific pending suspension / delisting event 语境。
- 边界：这些来源只支撑对应 vendor/venue，不代表所有市场。

## P45-H-CRYPTO03

- Binance Futures Leverage & Margin：补充 Binance-specific margin bracket / leverage / maintenance margin 语境。
- Bybit Risk Limit：补充 Bybit-specific risk limit、maintenance margin 与阶梯风险语境。
- 边界：不得输出仓位、杠杆、清算规避或止损参数。

## P45-H-CRYPTO05

- OKX Status：补充 exchange status / incident / maintenance 语境。
- Bybit Mark Price Calculation：补充 mark/index 异常处理或 fallback 语境。
- Binance Market Volatility Statement：补充 incident-style 官方公告语境。
- 边界：API/WebSocket 风险只能进入 observability / audit checklist，不得变成自动停机 hard gate。
