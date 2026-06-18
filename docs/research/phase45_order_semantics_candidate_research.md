# Phase 45 Order Type / TIF / Venue Semantics 候选知识采集记录

## 范围

本批次对应 CEK-TA-467 / P45-F，目标是采集 6 条 Order Type / TIF / Venue Semantics P1 候选知识。

本批次只生成候选和审计支撑材料，不创建 reviewed、approved、default guidance 或 hard gate。

## 联网核验来源

| source_key | 来源 | 类型 | URL | 用途 |
| --- | --- | --- | --- | --- |
| `fix_protocol` | FIX Trading Community FIX Protocol | `official_protocol_doc` | https://fixtrading.org/standards/fix-protocol/ | FIX protocol provides standardized order-entry and execution-report message semantics used by many electronic trading integrations. |
| `fix_execution_report` | FIXimate FIX 4.4 Execution Report | `official_protocol_doc` | https://fiximate.fixtrading.org/legacy/en/FIX.4.4/body_5756.html | FIX Execution Report supports receipt, status, fill, cancel, replace and reject semantics for order-event lifecycle review. |
| `cme_order_types` | CME Group Futures Order Types | `official_exchange_doc` | https://www.cmegroup.com/education/courses/things-to-know-before-trading-cme-futures/futures-order-types | CME explains futures order types such as market, limit, stop and GTC-style validity and warns participants to understand available order conditions. |
| `cme_order_qualifiers` | CME Globex Order Qualifiers | `official_exchange_doc` | https://www.cmegroup.com/confluence/display/EPICSANDBOX/Order%2BQualifiers | CME order qualifiers describe duration, minimum execution quantity and display quantity attributes used with Globex orders. |
| `cme_smp` | CME Globex Self-Match Prevention FAQ | `official_exchange_doc` | https://www.cmegroup.com/solutions/market-access/globex/trade-on-globex/faq-self-match.html | CME describes self-match prevention as optional functionality to prevent matching orders for accounts with common ownership and notes activation/rejection caveats. |
| `nasdaq_order_types_pdf` | Nasdaq Order Types and Modifiers | `official_exchange_doc` | https://www.nasdaqtrader.com/content/productsservices/trading/ordertypesg.pdf | Nasdaq order type and modifier guide documents TIF behavior such as market-hours IOC, system-hours IOC and order-type availability caveats. |
| `binance_futures_order` | Binance USD-M Futures New Order API | `official_platform_doc` | https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api | Binance Futures order API documents order type, timeInForce, reduceOnly, selfTradePreventionMode and GTD goodTillDate behavior. |
| `binance_spot_order` | Binance Spot Trading Endpoints | `official_platform_doc` | https://developers.binance.com/docs/binance-spot-api-docs/rest-api/trading-endpoints | Binance Spot documents LIMIT_MAKER as a post-only limit order rejected if it immediately matches and trades as taker. |
| `kraken_futures_order` | Kraken Futures Send Order API | `official_platform_doc` | https://docs.kraken.com/api-reference/order-management/send-order | Kraken futures API documents limit, post-only, IOC, market, stop, take-profit, trailing-stop and FOK order types, plus reduceOnly behavior. |
| `coinbase_trading_rules` | Coinbase Markets Trading Rules | `official_platform_doc` | https://www.coinbase.com/legal/trading_rules | Coinbase trading rules define limit, market, stop, TWAP, TIF, post-only, maker/taker and fee behavior with platform caveats. |
| `coinbase_trading_concepts` | Coinbase Exchange Trading Concepts | `official_platform_doc` | https://docs.cdp.coinbase.com/exchange/concepts/trading | Coinbase developer documentation lists STP modes and TIF options such as GTC, GTT, IOC and FOK. |
| `coinbase_international_stp` | Coinbase International Exchange Trading Rules | `official_platform_doc` | https://www.coinbase.com/international-exchange/legal/trading-rules | Coinbase International rules describe self-trade prevention, including cancel/decrement behavior when self-execution would occur. |
| `cfa_trading_costs` | CFA Institute Trading Costs and Electronic Markets | `professional_body` | https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets | CFA describes explicit and implicit trading costs, including broker commissions, exchange fees, bid-ask spread, market impact, delay and unfilled trades. |
| `sec_maker_taker` | SEC EMSAC Memo: Maker-Taker Fees on Equities Exchanges | `regulatory_discussion` | https://www.sec.gov/spotlight/emsac/memo-maker-taker-fees-on-equities-exchanges.pdf | SEC EMSAC memo describes maker-taker pricing as exchanges charging to take liquidity and paying rebates to post liquidity. |
| `cme_clearing_fees` | CME Exchange Fees for Clearing and Trading | `official_exchange_doc` | https://www.cmegroup.com/company/clearing-fees.html | CME states exchange fees vary by membership, incentive program participant status, product, volume, venue and transaction type. |

## 候选列表

| ID | title | source_count | 状态 |
| --- | --- | ---: | --- |
| P45-F-ORD01 | 订单类型语义必须由 adapter 和 venue 明确声明 | 5 | candidate_ready |
| P45-F-ORD02 | Time In Force 必须绑定 session、venue 和过期语义 | 5 | candidate_ready |
| P45-F-ORD03 | post-only 和 reduce-only 是执行约束，不是盈利或安全保证 | 4 | candidate_ready |
| P45-F-ORD04 | 自成交防护必须声明模式、账户范围和事件处理 | 4 | candidate_ready |
| P45-F-ORD05 | 交易所特有订单类型不得泛化为通用语义 | 5 | candidate_ready |
| P45-F-ORD06 | maker/taker 费用必须和订单类型、成交结果分开审计 | 4 | candidate_ready |

## 边界

```text
1. 不输出买卖点、仓位、杠杆、止损止盈、路由建议、费用套利或实盘执行建议。
2. FIX 只作为协议语义来源，不能替代 broker/venue/order truth。
3. CME、Nasdaq、Coinbase、Binance、Kraken 等来源必须保留 venue、product、session、account mode 和 API version caveat。
4. 候选知识必须等待外部严格审计，不得直接进入 formal reviewed。
```
