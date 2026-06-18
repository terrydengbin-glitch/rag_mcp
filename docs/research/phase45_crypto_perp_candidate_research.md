# Phase 45 Crypto Perpetual 候选知识采集记录

## 范围

本批次对应 CEK-TA-470 / P45-H，目标是采集 5 条 Crypto Perpetual P2 候选知识。

本批次只生成候选知识、研究记录和质量门禁，不创建 reviewed、approved、default guidance 或 hard gate。

## 联网核验来源

| source_key | 来源 | 类型 | URL | 用途 |
| --- | --- | --- | --- | --- |
| `binance_mark_index` | Binance Futures: What Are Mark Price and Price Index in USDⓈ-Margined Futures? | `official_platform_doc` | https://www.binance.com/en/support/faq/detail/360033525071 | Binance explains Mark Price and Price Index in futures and states that the Price Index mitigates manipulation risk by using multiple exchanges. |
| `binance_mark_api` | Binance Open Platform Mark Price API | `official_api_doc` | https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Mark-Price | Binance Mark Price API exposes markPrice, indexPrice, estimatedSettlePrice, lastFundingRate, interestRate, nextFundingTime and time fields. |
| `binance_funding` | Binance Futures Funding Rates | `official_platform_doc` | https://www.binance.com/en/support/faq/detail/360033525031 | Binance explains that funding payments are periodic cash flows exchanged between long and short holders of perpetual contracts. |
| `binance_funding_api` | Binance Funding Rate History API | `official_api_doc` | https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History | Binance funding history API returns fundingRate and markPrice associated with a funding-fee charge over time. |
| `binance_liquidation` | Binance Futures Liquidation Protocols | `official_platform_doc` | https://www.binance.com/en/support/faq/detail/360033525271 | Binance explains liquidation protocols, bankruptcy price and insurance fund takeover in volatile conditions. |
| `binance_liquidation_how` | Binance: How Liquidation Works in Futures Trading | `official_platform_doc` | https://www.binance.com/en/support/faq/detail/7ba80e1b406f40a0a140a84b3a10c387 | Binance describes liquidation as a risk-control feature intended to prevent negative equity when leveraged positions suffer gaps. |
| `binance_insurance_fund` | Binance Futures Insurance Funds | `official_platform_doc` | https://www.binance.com/en/support/faq/detail/360033525371 | Binance describes futures insurance funds as safety nets that limit the impact of liquidations and bankrupt positions. |
| `binance_adl` | Binance Auto-Deleveraging (ADL) | `official_platform_doc` | https://www.binance.com/en/support/faq/detail/360033525471 | Binance states ADL is the final step in liquidation and occurs if futures insurance funds cannot accept a bankrupt position. |
| `binance_adl_api` | Binance ADL Risk API | `official_api_doc` | https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/ADL-Risk | Binance ADL risk rating uses insurance fund balance, concentration, order book depth, volatility, leverage, unrealized PnL and margin utilization. |
| `binance_agg_trade` | Binance Futures Aggregate Trade Streams | `official_api_doc` | https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Aggregate-Trade-Streams | Binance states aggregate trade streams include only market trades and exclude insurance fund and ADL trades. |
| `bybit_mark_price` | Bybit Mark Price Calculation for Perpetual and Expiry Contracts | `official_platform_doc` | https://www.bybit.com/en/help-center/article/Mark-Price-Calculation-Perpetual-Expiry-Contracts | Bybit says mark price is used as a liquidation trigger and for unrealized PnL measurement in perpetual contracts. |
| `bybit_funding` | Bybit Introduction to Funding Rate | `official_platform_doc` | https://www.bybit.com/en/help-center/article/Introduction-to-Funding-Rate | Bybit explains funding rates, funding timestamp and interval behavior for futures/perpetual trading. |
| `bybit_insurance_fund` | Bybit Insurance Fund | `official_platform_doc` | https://www.bybit.com/en/help-center/article/Insurance-Fund | Bybit describes its insurance fund as a reserve pool used to protect traders from excessive losses in futures trading. |
| `bybit_adl` | Bybit Auto-Deleveraging (ADL) Mechanism | `official_platform_doc` | https://www.bybit.com/en/help-center/article/Auto-Deleveraging-ADL | Bybit explains ADL as a mechanism tied to insurance-fund drawdown and liquidation conditions. |
| `okx_funding` | OKX Perpetual Funding Fee Mechanism | `official_platform_doc` | https://www.okx.com/en-us/help/perps-funding-fee-mechanism | OKX explains funding fee mechanism for perpetual futures and notes product/feature/rule applicability caveats. |
| `okx_premarket_perp` | OKX Pre-market Product Rule | `official_platform_doc` | https://www.okx.com/help/pre-market-product-rule | OKX describes pre-market perpetuals, no expiration/delivery and early trading before official listing or spot launch. |
| `databento_status` | Databento Status Schema | `official_vendor_doc` | https://databento.com/docs/schemas-and-data-formats/status | Databento status schema covers trading status, halt, pause, auction, matching-engine status and instrument expiration events. |

## 候选列表

| ID | title | partition | source_count | 状态 |
| --- | --- | --- | ---: | --- |
| P45-H-CRYPTO01 | mark price、index price 和 last price 必须分开建模 | KB_03_MARKET_MICROSTRUCTURE | 3 | candidate_ready |
| P45-H-CRYPTO02 | funding interval 和 funding fee 必须独立记账 | KB_03_MARKET_MICROSTRUCTURE | 4 | candidate_ready |
| P45-H-CRYPTO03 | maintenance margin 和 liquidation 不能等同普通止损 | KB_07_RISK_MANAGEMENT | 4 | candidate_ready |
| P45-H-CRYPTO04 | ADL 和 insurance fund 只能作为 venue-specific 风险机制 | KB_07_RISK_MANAGEMENT | 5 | candidate_ready |
| P45-H-CRYPTO05 | crypto venue outage、pre-market 和 clawback 风险必须单独审计 | KB_07_RISK_MANAGEMENT | 5 | candidate_ready |

## 边界

```text
1. 不输出仓位、杠杆、买卖点、止损止盈、清算规避或实盘执行建议。
2. Binance、Bybit、OKX 等来源只能证明各自 venue/product/account mode 规则，不得泛化。
3. Crypto perpetual 相关 mark/index/last price、funding、liquidation、ADL、insurance fund、outage/clawback 必须绑定交易所、产品、抵押资产、保证金模式和规则版本。
4. 候选知识必须等待外部严格审计，不得直接进入 formal reviewed。
```
