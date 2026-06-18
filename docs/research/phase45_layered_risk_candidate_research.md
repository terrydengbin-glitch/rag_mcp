# Phase 45 Layered Risk / Credit / Margin 候选知识采集记录

## 范围

本批次对应 CEK-TA-461 / P45-C，目标是采集 6 条 Layered Risk / Credit / Margin P1 候选知识。

本批次只生成候选和审计包，不创建 reviewed、approved、default guidance 或 hard gate。

## 来源记录

| source_key | 来源 | 类型 | URL | 用途 |
| --- | --- | --- | --- | --- |
| `sec_15c3_5_final` | Risk Management Controls for Brokers or Dealers with Market Access | `regulatory_rule` | https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm | SEC Rule 15c3-5 requires market-access broker-dealers to maintain financial and regulatory risk-management controls, including pre-set credit/capital thresholds and erroneous-order controls. |
| `sec_15c3_5_faq` | SEC Market Access Rule FAQ | `regulatory_guidance` | https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions/divisionsmarketregfaq-0 | SEC FAQ explains that controls should systematically limit financial exposure, prevent orders beyond credit/capital thresholds, reject orders beyond price/size parameters, and keep financial controls under broker-dealer control. |
| `fia_automated_controls_2024` | Best Practices for Automated Trading Risk Controls and System Safeguards | `professional_body` | https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf | FIA best-practice paper covers pre-trade risk management, exchange volatility controls, post-trade analysis, testing, conformance, and system safeguards for automated trading. |
| `cme_pre_trade` | CME Globex Pre-Trade Risk Management | `official_exchange_doc` | https://www.cmegroup.com/solutions/market-access/globex/trade-on-globex/pre-trade-risk-management.html | CME describes pre-trade risk tools including order blocking, cancel open orders, cancel-on-disconnect, self-match prevention, duplicate order checks, and real-time activity monitoring. |
| `cme_credit_controls` | CME Globex Credit Controls | `official_exchange_doc` | https://www.cmegroup.com/tools-information/webhelp/globex-credit-controls/Content/CME-Globex-Credit-Controls-Management.html | CME Globex Credit Controls provide pre-execution controls for clearing-firm risk administrators to set exposure and maximum quantity limits for Globex order/trade activity. |
| `cme_account_credit` | CME Account Manager Credit Controls | `official_exchange_doc` | https://www.cmegroup.com/tools-information/webhelp/account-manager-service/Content/credit-controls.html | CME account-level controls include credit, long/short quantity limits and order-submission controls by product group and product. |
| `cme_price_banding` | CME Globex Price Banding | `official_exchange_doc` | https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457317722/Limits%2Band%2BBanding | CME price banding subjects orders to price validation and rejects orders outside the given band to prevent erroneous or market-moving orders. |
| `cme_messaging_controls` | CME Globex Messaging Controls | `official_exchange_doc` | https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457317540/Messaging%2BControls | CME messaging controls are designed to protect participants from excessive messaging in iLink order entry. |
| `cme_span` | CME SPAN Methodology Overview | `official_exchange_doc` | https://www.cmegroup.com/solutions/risk-management/performance-bonds-margins/span-methodology-overview.html | CME SPAN is a portfolio-risk methodology for calculating performance bond requirements using risk arrays and scenario-based portfolio loss estimates. |
| `cme_margins_faq` | CME Performance Bonds/Margins FAQ | `official_exchange_doc` | https://www.cmegroup.com/solutions/risk-management/performance-bonds-margins/faq-performance-bonds-margins.html | CME explains performance bonds/margins as deposits held at CME Clearing to ensure clearing members meet obligations; requirements vary by product and volatility. |

## 候选列表

| ID | title | source_count | 状态 |
| --- | --- | ---: | --- |
| P45-C-RISK01 | pre-trade controls 必须分层声明 | 4 | candidate_ready |
| P45-C-RISK02 | credit limit 不是策略风险限额 | 3 | candidate_ready |
| P45-C-RISK03 | 最大订单量和价格 collar 必须独立于策略信号 | 4 | candidate_ready |
| P45-C-RISK04 | 消息节流和 cancel-rate controls 必须可审计 | 3 | candidate_ready |
| P45-C-RISK05 | margin、collateral 和 available funds 必须分开 | 3 | candidate_ready |
| P45-C-RISK06 | post-trade surveillance 不能替代 pre-trade gate | 3 | candidate_ready |

## 边界

```text
1. 不输出风险阈值、信用额度、保证金比例、买卖点、仓位、杠杆、止损止盈或实盘执行建议。
2. SEC、FIA、CME 来源必须保留辖区、venue、产品、broker/clearing 和 implementation caveat。
3. 候选知识必须等待外部严格审计，不得直接进入 formal reviewed。
```
