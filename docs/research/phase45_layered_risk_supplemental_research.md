# Phase 45 Layered Risk RISK05 补证记录

## 补证目标

首轮审计中 P45-C-RISK05 被判定为 needs_more_evidence。本文件记录 broker available funds、buying power、crypto venue balance 和 collateral/margin 字段边界补证。

## 补充来源

| source_id | 来源 | 类型 | URL | 用途 |
| --- | --- | --- | --- | --- |
| `ibkr_available_for_trading` | Available for Trading Values | `official_broker_doc` | https://www.ibkrguides.com/traderworkstation/available-for-trading.htm | IBKR distinguishes Available Funds, Excess Liquidity, Buying Power and related account values, explaining that each value has different trading or cushion semantics. |
| `ibkr_available_funds` | Current Available Funds | `official_broker_doc` | https://www.interactivebrokers.com/campus/glossary-terms/current-available-funds/ | IBKR defines Current Available Funds as equity available for trading, calculated from Equity with Loan Value minus Initial Margin. |
| `ibkr_margin_requirements` | Margin Requirements | `official_broker_doc` | https://www.ibkrguides.com/advisorportal/ug/marginrequirements.htm | IBKR margin documentation distinguishes margin requirement, available funds, excess liquidity and buying power. |
| `binance_futures_account_info` | USDⓈ-M Futures Account Information V3 | `official_platform_doc` | https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Account-Information-V3 | Binance Futures account information endpoint exposes account-level balance fields such as availableBalance, margin balances and wallet-related values depending on account mode. |
| `binance_futures_balances` | What Is the Available Balance, Margin Balance, and Total Balance on Binance Futures? | `official_platform_article` | https://www.binance.com/en/blog/futures/457299340443288694 | Binance explains that futures wallet balance, available balance, margin balance and total balance serve different purposes and reflect different funds/PnL views. |

## 修补后边界

```text
1. clearing margin / performance bond、broker available funds、buying power、excess liquidity、crypto futures wallet balance、available balance、margin balance 和 strategy capital budget 必须分开。
2. 任一字段都不能被默认为可交易现金。
3. 资金充足性判断必须依赖 point-in-time account/margin/collateral evidence、broker/venue/account-mode 语义和 owner 边界。
4. 本候选不输出保证金比例、信用额度、可用资金判断或下单许可。
```
