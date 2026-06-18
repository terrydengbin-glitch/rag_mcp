# Phase 45 STRESS04 保证金/融资变化补证记录

## 补证目标

补齐 STRESS04 在二审中指出的 margin / funding direct source 缺口。补证后仍只导出三审包，不创建 reviewed、approved、default guidance 或 hard gate。

## 新增直接来源

| 来源 | URL | 用途 | 边界 |
| --- | --- | --- | --- |
| CME Group Product Margins | https://www.cmegroup.com/solutions/risk-management/margin-services/product-margins.html | CME defines futures margins/performance bonds as deposits required to cover potential losses and notes margin requirements vary by product and market volatility. | CME futures/clearing context only; not universal broker or crypto venue margin semantics. |
| IBKR Available for Trading Values | https://www.ibkrguides.com/traderworkstation/available-for-trading.htm | IBKR distinguishes Available Funds, Excess Liquidity and Buying Power, supporting broker/account-specific margin and financing field boundaries. | IBKR-specific account field semantics; not universal across brokers or venues. |
| Binance USD-M Futures Account Balance | https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Futures-Account-Balance-V2 | Binance USD-M Futures account balance response exposes wallet balance, cross wallet balance, available balance and margin availability fields. | Binance USD-M Futures API/account-mode context only; not a general broker or exchange rule. |
| Binance USD-M Futures Get Funding Info | https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-Info | Binance funding-info endpoint returns symbols with funding-rate cap/floor or fundingIntervalHours adjustments, supporting venue-specific funding-change evidence. | Binance USD-M Futures funding semantics only; not universal crypto or traditional futures financing semantics. |
| Binance Futures Balance and Position Update Event | https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams/Event-Balance-and-Position-Update | Binance user data stream documents account updates for balance, position, margin type and funding-fee balance changes. | Binance USD-M Futures event semantics only; not universal account-event schema. |

## 候选状态

- candidate_id: `cand_20260612_phase45_stress_scenario_p45_e_stress04_001`
- research_task_id: `P45-E-STRESS04`
- source_count: `12`
- 当前状态：`needs_more_evidence_supplemented`，等待 STRESS04 单条三审。

## 保留边界

```text
1. margin / funding 只能作为 broker、venue、clearing、account-mode 或 funding-interval specific 的情景维度。
2. 不得输出隔夜持仓建议、止损止盈、仓位调整、session 风险阈值或 hard gate。
3. 不得把 Binance funding、IBKR buying power 或 CME performance bond 泛化成所有市场规则。
```
