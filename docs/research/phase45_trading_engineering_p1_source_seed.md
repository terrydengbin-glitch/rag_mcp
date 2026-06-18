# Phase 45 Trading Engineering P1/P2 来源种子库

## 目标

本文件为 Phase 45 47 条 Trading Engineering P1/P2 知识采集提供可信来源种子。后续候选知识必须优先使用监管、交易所、协议、专业协会、标准组织和官方文档；厂商博客和教育资料只能作为 supporting source。

## 来源等级

```text
P0: regulatory_doc、official_exchange_doc、official_protocol_doc、standard_doc、professional_body
P1: official_platform_doc、framework_doc、data_vendor_doc、public_technical_report
P2: vendor_blog、education_article、product_glossary，仅作 supporting
```

## P45-A Execution TCA

| source_id | source_type | 来源 | URL | 用途 |
| --- | --- | --- | --- | --- |
| p45_src_cfa_trading_costs | professional_body | CFA Institute Trading Costs and Electronic Markets | https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets | implementation shortfall、market impact、delay cost、opportunity cost、VWAP/TWAP 边界 |
| p45_src_cfa_trade_execution | professional_body | CFA Institute Trade Strategy and Execution | https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution | execution quality、benchmark、trade cost analysis、routing context |
| p45_src_fix_protocol | official_protocol_doc | FIX Trading Community FIX Protocol | https://fixtrading.org/standards/fix-protocol/ | execution report、订单事件和协议语义 supporting |

## P45-B Audit Trail / Clock Sync

| source_id | source_type | 来源 | URL | 用途 |
| --- | --- | --- | --- | --- |
| p45_src_sec_rule_613 | regulatory_doc | SEC Rule 613 Consolidated Audit Trail | https://www.sec.gov/about/divisions-offices/division-trading-markets/rule-613-consolidated-audit-trail | CAT、订单活动追踪、监管审计链 |
| p45_src_cfr_242_613 | regulatory_doc | 17 CFR 242.613 Consolidated audit trail | https://www.law.cornell.edu/cfr/text/17/242.613 | clock synchronization、timestamp、audit trail 字段语义 |
| p45_src_esma_rts25 | regulatory_doc | ESMA Article 22c / RTS 25 clock synchronisation | https://www.esma.europa.eu/publications-and-data/interactive-single-rulebook/mifir/article-22c-synchronisation-business-clocks | UTC、business clock、granularity、clock sync 监管边界 |

## P45-C Layered Risk / Credit / Margin

| source_id | source_type | 来源 | URL | 用途 |
| --- | --- | --- | --- | --- |
| p45_src_sec_15c3_5 | regulatory_doc | SEC Rule 15c3-5 Market Access Risk Controls | https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm | market access、pre-trade controls、financial/risk controls |
| p45_src_fia_risk_controls_2024 | professional_body | FIA Automated Trading Risk Controls and System Safeguards | https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf | pre-trade risk、message controls、post-trade analysis、conformance testing |
| p45_src_cme_credit_controls | official_exchange_doc | CME Globex Credit Controls | https://www.cmegroup.com/tools-information/webhelp/globex-credit-controls/Content/CME-Globex-Credit-Controls-Management.html | credit limit、max quantity、exposure controls、order blocking/cancel examples |

## P45-D Resilience / Incident / Log

| source_id | source_type | 来源 | URL | 用途 |
| --- | --- | --- | --- | --- |
| p45_src_sec_reg_sci | regulatory_doc | SEC Regulation Systems Compliance and Integrity | https://www.sec.gov/rules-regulations/2015/12/regulation-systems-compliance-integrity | systems compliance、incident、BCDR、regulated system resilience |
| p45_src_ecfr_reg_sci | regulatory_doc | eCFR Regulation SCI | https://www.ecfr.gov/current/title-17/chapter-II/part-242/subpart-ECFRe106e84e67e2bc9 | written policy、system operation、compliance and integrity |
| p45_src_nist_800_92 | standard_doc | NIST SP 800-92 Guide to Computer Security Log Management | https://csrc.nist.gov/pubs/sp/800/92/final | log management、retention、integrity、enterprise logging lifecycle |

## P45-E Stress Testing / Scenario Risk

| source_id | source_type | 来源 | URL | 用途 |
| --- | --- | --- | --- | --- |
| p45_src_cpmi_iosco_pfmi | professional_body | CPMI-IOSCO Principles for Financial Market Infrastructures | https://www.iosco.org/library/pubdocs/pdf/ioscopd377-pfmi.pdf | stress testing、liquidity stress、extreme scenarios、risk resources |
| p45_src_bis_pfmi | professional_body | BIS CPMI Principles for Financial Market Infrastructures | https://www.bis.org/cpmi/publ/d101a.pdf | stress testing frequency、scenario assumptions、liquidity risk |
| p45_src_fia_risk_controls_2024 | professional_body | FIA Automated Trading Risk Controls and System Safeguards | https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf | automated trading risk controls、post-trade analysis、system safeguards |

## P45-F Order Type / TIF / Venue Semantics

| source_id | source_type | 来源 | URL | 用途 |
| --- | --- | --- | --- | --- |
| p45_src_fix_protocol | official_protocol_doc | FIX Trading Community FIX Protocol | https://fixtrading.org/standards/fix-protocol/ | order message、execution report、TimeInForce supporting |
| p45_src_fix_exec_report | official_protocol_doc | FIX 4.4 Execution Report | https://fiximate.fixtrading.org/legacy/en/FIX.4.4/body_5756.html | execution report lifecycle、order status、fill status |
| p45_src_databento_status | data_vendor_doc | Databento Status schema | https://databento.com/docs/schemas-and-data-formats/status | market status、halt、auction、session state supporting |

## P45-G Market Data Entitlement / Reference Data

| source_id | source_type | 来源 | URL | 用途 |
| --- | --- | --- | --- | --- |
| p45_src_databento_instruments | data_vendor_doc | Databento Instrument definitions | https://databento.com/docs/schemas-and-data-formats/instrument-definitions | point-in-time instrument definitions、tick size、listing/expiration metadata |
| p45_src_databento_statistics | data_vendor_doc | Databento Statistics schema | https://databento.com/docs/schemas-and-data-formats/statistics | official settlement、open interest、daily summary supporting |
| p45_src_databento_schema_catalog | data_vendor_doc | Databento Schemas and data formats | https://databento.com/docs/schemas-and-data-formats | schema version、status、corporate actions、reference data categories |

## P45-H Crypto Perpetual

| source_id | source_type | 来源 | URL | 用途 |
| --- | --- | --- | --- | --- |
| p45_src_binance_mark_price | official_platform_doc | Binance Futures Mark Price and Price Index | https://www.binance.com/en/support/faq/detail/360033525071 | mark price、index price、last price、liquidation trigger caveat |
| p45_src_binance_funding | official_platform_doc | Binance Futures Funding Rates | https://www.binance.com/en/support/faq/detail/360033525031 | funding interval、funding fee accounting、long/short funding flow |
| p45_src_databento_status | data_vendor_doc | Databento Status schema | https://databento.com/docs/schemas-and-data-formats/status | outage/halt/status schema supporting，不替代 crypto venue 官方规则 |

## 使用规则

```text
1. 每条候选至少 2 个来源；reviewed/caveat_only 准备时优先 3 个以上来源。
2. 若 claim 依赖 CEK-TA 内部字段契约，必须内联 contract 摘要、schema extract 或 hash。
3. 交易所、broker、数据商、crypto venue 来源只能证明其自身市场或产品，不得泛化。
4. P2 来源不能作为 reviewed 主证据。
5. 所有来源引用必须写入 source_refs/source_evidence，并带 source_type、url、retrieved_at、适用边界。
```
