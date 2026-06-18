# Phase 45 Stress Scenario 首轮审计补证记录

## 补证范围

本文件记录 P45-E-STRESS03、P45-E-STRESS04、P45-E-STRESS05 的首轮审计补证。补证后仍只进入再审包，不创建 reviewed、approved、default guidance 或 hard gate。

## 新增来源

| key | 来源 | URL | 用途 |
| --- | --- | --- | --- |
| `bcbs155_stress` | Principles for sound stress testing practices and supervision | https://www.bis.org/publ/bcbs155.pdf | BCBS stress-testing guidance includes stress testing of credit-risk concentrations and wrong-way risk considerations, supporting concentration/correlation stress caveats. |
| `bis_correlation_breakdown` | Evaluating correlation breakdowns during periods of market volatility | https://www.bis.org/publ/confer08k.pdf | BIS conference paper discusses correlation breakdown during volatile markets and the problem that correlations may change dramatically during major market events. |
| `fdic_ccr_concentration` | Interagency Supervisory Guidance on Counterparty Credit Risk Management | https://www.fdic.gov/news/financial-institution-letters/2011/fil11053a.pdf | Interagency guidance supports concentration analysis and counterparty credit-risk stress testing as part of risk reporting and governance. |
| `nasdaq_halt_orders` | Nasdaq Equity 4 Rules: Trading halt and pause order handling | https://listingcenter.nasdaq.com/rulebook/nasdaq/rules/Nasdaq%20Equity%204 | Nasdaq rules include halt/pause order handling, including cases where orders entered during a halt or pause will not be accepted unless directed elsewhere. |
| `nyse_mwcb_faq` | NYSE Market-Wide Circuit Breakers FAQ | https://www.nyse.com/publicdocs/nyse/NYSE_MWCB_FAQ.pdf | NYSE FAQ supports market-wide circuit breaker halt durations and reopening-auction processing after halts. |
| `cme_trading_hours` | CME Group Holiday and Trading Hours | https://www.cmegroup.com/trading-hours.html | CME trading-hours and holiday schedules support session, holiday, early-close and product-specific trading-hour boundaries. |
| `investopedia_gap_risk` | Gap Risk Explained | https://www.investopedia.com/terms/g/gaprisk.asp | Supporting source describing gap risk as price movement while markets are closed, with greater risk over weekends or longer closures. |
| `bis_market_risk_d457` | Minimum capital requirements for market risk | https://www.bis.org/bcbs/publ/d457.htm | BCBS market-risk standard supports the revised market-risk framework and Expected Shortfall as a market-risk measure. |
| `bis_mar33_liquidity_horizon` | Basel Framework MAR33 Internal models approach | https://www.bis.org/basel_framework/chapter/MAR/33.htm | Basel MAR33 supports liquidity horizons and stressed expected shortfall calculations in the market-risk internal models approach. |
| `acerbi_tasche_es` | Expected Shortfall: a natural coherent alternative to Value at Risk | https://faculty.washington.edu/ezivot/econ589/acertasc.pdf | Acerbi and Tasche discuss Expected Shortfall as a coherent alternative to Value at Risk and as an average of worst-tail losses. |

## 补证候选

| ID | source_count | 状态 |
| --- | ---: | --- |
| P45-E-STRESS03 | 6 | needs_more_evidence |
| P45-E-STRESS04 | 7 | needs_more_evidence |
| P45-E-STRESS05 | 6 | needs_more_evidence |

## 边界

```text
1. STRESS03 不输出相关性阈值、降仓、拒单或 hard gate。
2. STRESS04 不输出隔夜持仓建议、止损止盈、仓位调整、session 风险阈值或 hard gate。
3. STRESS05 不输出 VaR/ES 阈值、交易许可、降仓、停机或 hard gate。
```
