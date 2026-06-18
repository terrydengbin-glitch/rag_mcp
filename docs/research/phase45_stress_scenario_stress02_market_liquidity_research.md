# Phase 45 STRESS02 market/execution liquidity 补证记录

## 补证目标

STRESS02 首轮 reviewed-preparation 审计认为 PFMI、CCP、CME、DTCC 来源足以支撑 clearing/funding liquidity，但不足以直接支撑 market depth、bid-ask spread、market impact 和 time-to-liquidation。本文补入 market/execution liquidity 直接来源。

## 来源分组

| 分组 | 来源 | URL | 用途 |
| --- | --- | --- | --- |
| clearing/funding liquidity | CPMI-IOSCO PFMI | https://www.iosco.org/library/pubdocs/pdf/IOSCOPD377.pdf | FMI/CCP liquidity risk、liquid resources、stress testing 语境 |
| clearing/funding liquidity | CPMI-IOSCO CCP Resilience | https://www.bis.org/cpmi/publ/d163.pdf | CCP credit/liquidity exposure 和 multiday liquidity stress 语境 |
| clearing/funding liquidity | CME Liquidity Risk Management | https://www.cmegroup.com/articles/brochures-and-handbooks/101-overview-cme-clearing-liquidity-risk-management-practices.html | CME Clearing liquidity stress 语境 |
| clearing/funding liquidity | DTCC Stress Testing | https://www.dtcc.com/managing-risk/financial-risk-management/stress-testing | clearing agency credit/liquidity exposure 和 financial resources 语境 |
| market/execution liquidity | ESMA Liquidity Stress Testing Guidelines | https://www.esma.europa.eu/sites/default/files/library/esma34-39-897_guidelines_on_liquidity_stress_testing_in_ucits_and_aifs_en.pdf | liquidation cost、time to liquidation、trade/order size、higher bid-ask spread、lower liquidity、longer time to liquidate |
| market/execution liquidity | eCFR Rule 22e-4 | https://www.ecfr.gov/current/title-17/chapter-II/part-270/section-270.22e-4 | liquidity classification 的 time-to-convert/sell/dispose-of 边界 |
| market/execution liquidity | CFA Institute Liquidity in Equity Markets | https://www.cfainstitute.org/sites/default/files/-/media/documents/article/position-paper/liquidity-in-equity-markets-characteristics-dynamics-implications-for-market-quality.pdf | bid-ask spread、price impact、block order execution cost |
| market/execution liquidity | NY Fed Measuring Treasury Market Depth | https://libertystreeteconomics.newyorkfed.org/2024/02/measuring-treasury-market-depth/ | market depth 作为特定价格上可买卖数量的市场流动性维度 |

## 必须保留的边界

1. clearing/funding liquidity 不得被外推为 market/execution liquidity。
2. market_depth_source_id、spread_source_id、market_impact_source_id、time_to_liquidate_source_id 缺失时必须标记 unknown，不得当作 normal、zero 或 safe。
3. 本条不得输出可成交数量、滑点阈值、liquidation horizon 数值、交易许可、仓位建议或 hard gate。
4. ESMA/SEC/CFA/NY Fed 来源具有基金、权益市场或美国国债市场等语境边界，外接项目必须按自身市场、venue、asset、data vendor 补事实来源。
