# Phase 45 Market Data Entitlement / Reference Data 候选知识采集记录

## 范围

本批次对应 CEK-TA-469 / P45-G，目标是采集 6 条 Market Data Entitlement / Reference Data P2 候选知识。

本批次只生成候选知识、研究记录和质量门禁，不创建 reviewed、approved、default guidance 或 hard gate。

## 联网核验来源

| source_key | 来源 | 类型 | URL | 用途 |
| --- | --- | --- | --- | --- |
| `nyse_market_data_policy` | NYSE Proprietary Market Data Comprehensive Policy Package | `official_exchange_policy` | https://www.nyse.com/publicdocs/nyse/data/NYSE_Proprietary_Market_Data_Comprehensive_Policy_Package.pdf | NYSE policy documents Non-Display Use categories, internal use, use on behalf of clients and derived data policy boundaries. |
| `nasdaq_data_policies` | Nasdaq U.S. Equities and Options Data Policies | `official_exchange_policy` | https://www.nasdaqtrader.com/content/AdministrationSupport/Policy/USEquitiesandOptionsDataPolicies.pdf | Nasdaq policies describe non-display applications, internal usage and market-data product usage constraints. |
| `nasdaq_non_display_clarification` | Nasdaq Clarification for U.S. Non-Display Policy | `official_exchange_policy` | https://nasdaqtrader.com/TraderNews.aspx?id=dn2015-09 | Nasdaq defines Non-Display as machine or automated-device access or use without a natural-person display. |
| `cme_derived_data` | CME Group Derived Data | `official_exchange_policy` | https://www.cmegroup.com/market-data/browse-data/derived-data.html | CME describes licensing for derived works and derived data use cases based on CME market data. |
| `cme_license_data` | CME Group License Data Products | `official_exchange_policy` | https://www.cmegroup.com/market-data/license-data.html | CME market-data licensing page directs firms to license market data and derived data products by use case. |
| `databento_definitions` | Databento Instrument Definitions | `official_vendor_doc` | https://databento.com/docs/schemas-and-data-formats/instrument-definitions | Databento instrument definitions provide point-in-time reference information including symbol, name, listing, expiration, tick size and strike price. |
| `databento_schemas` | Databento Schemas and Data Formats | `official_vendor_doc` | https://databento.com/docs/schemas-and-data-formats | Databento documents supported market-data schemas and field dictionaries such as MBO, MBP, trades, bars, definitions and statistics. |
| `databento_statistics` | Databento Statistics Schema | `official_vendor_doc` | https://databento.com/docs/schemas-and-data-formats/statistics | Databento statistics include session fields such as upper and lower price limits, settlement and venue-specific volume/price fields. |
| `databento_definitions_blog` | Databento: Evaluating Market Data APIs - Point-in-Time Definitions | `vendor_technical_article` | https://databento.com/blog/instrument-definitions | Databento explains why point-in-time instrument definitions matter for historical and real-time reference data and backtesting. |
| `databento_tick_sizes` | Databento: Getting Futures Tick Sizes and Notional Tick Values | `vendor_technical_article` | https://databento.com/blog/tick-sizes-and-values | Databento discusses futures variable tick sizes, contract multipliers and display styles that should not be hardcoded. |
| `nasdaq_symbol_directory` | Nasdaq Symbol Directory Data Fields and Definitions | `official_exchange_doc` | https://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs | Nasdaq Symbol Directory defines fields such as round lot size, test issue and symbol directory metadata. |
| `nasdaq_round_lot` | UTP Vendor Alert: Regulation NMS Round Lot Designations | `official_exchange_doc` | https://www.nasdaqtrader.com/TraderNews.aspx?id=UTP2025-10 | UTP vendor alert describes semiannual round-lot designations for NMS stocks based on price-based evaluation periods. |
| `cme_product_slate` | CME Group Product Slate | `official_exchange_doc` | https://www.cmegroup.com/markets/products | CME product slate links searchable product contract specifications and previous-day volume/open-interest data. |
| `cme_price_limits` | CME Group Daily Price Limits | `official_exchange_doc` | https://www.cmegroup.com/trading/price-limits.html | CME publishes daily price limits for multiple product groups, showing that price-limit metadata is product and session dependent. |

## 候选列表

| ID | title | source_count | 状态 |
| --- | --- | ---: | --- |
| P45-G-DATA01 | 市场数据授权必须声明展示、非展示、衍生和训练用途 | 5 | candidate_ready |
| P45-G-DATA02 | instrument definition 必须按 point-in-time 保存 | 4 | candidate_ready |
| P45-G-DATA03 | tick size、lot size 和 price limit 必须作为版本化元数据 | 6 | candidate_ready |
| P45-G-DATA04 | 数据集覆盖范围和 universe 必须显式声明 | 4 | candidate_ready |
| P45-G-DATA05 | 供应商 schema 和解析版本必须可追踪 | 4 | candidate_ready |
| P45-G-DATA06 | reference data 不是默认交易信号 | 5 | candidate_ready |

## 边界

```text
1. 不输出法律授权结论、买卖点、仓位、杠杆、止损止盈或实盘执行建议。
2. 交易所/供应商数据政策和 schema 文档必须保留 active agreement、venue、dataset、product、jurisdiction 和版本边界。
3. reference data 只做身份、覆盖、授权、元数据和时点一致性约束；若作为模型特征，必须转入特征工程/策略研究/AI Engineering 验证。
4. 候选知识必须等待外部严格审计，不得直接进入 formal reviewed。
```
