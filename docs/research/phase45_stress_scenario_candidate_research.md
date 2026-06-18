# Phase 45 Stress Testing / Scenario Risk 候选知识采集记录

## 范围

本批次对应 CEK-TA-465 / P45-E，目标是采集 6 条 Stress Testing / Scenario Risk P1 候选知识。

本批次只生成候选和审计包，不创建 reviewed、approved、default guidance 或 hard gate。

## 联网核验来源

| source_key | 来源 | 类型 | URL | 用途 |
| --- | --- | --- | --- | --- |
| `cpmi_iosco_pfmi` | CPMI-IOSCO Principles for Financial Market Infrastructures | `professional_body` | https://www.iosco.org/library/pubdocs/pdf/IOSCOPD377.pdf | PFMI supports stress testing, liquidity-risk management and extreme-but-plausible scenario analysis for financial market infrastructures. |
| `bis_stress_testing_principles` | Basel Committee Stress Testing Principles | `professional_body` | https://www.bis.org/bcbs/publ/d450.htm | BCBS stress testing principles cover objectives, governance, policies, processes, methodology, resources and documentation for stress-testing frameworks. |
| `bis_ccp_resilience` | CPMI-IOSCO Resilience of Central Counterparties: Further Guidance on the PFMI | `professional_body` | https://www.bis.org/cpmi/publ/d163.pdf | The CCP resilience guidance discusses stress-testing frameworks, credit and liquidity risk exposure, extreme but plausible market conditions, and multiday liquidity stress considerations. |
| `cme_clearing_stress` | CME Clearing Stress Testing Practices | `official_exchange_doc` | https://www.cmegroup.com/articles/brochures-and-handbooks/101-overview-cme-clearing-stress-testing-practices.html | CME describes scenario-based clearing stress testing using historical and hypothetical scenarios across price and volatility risk factors. |
| `cme_liquidity_stress` | CME Clearing Liquidity Risk Management Practices | `official_exchange_doc` | https://www.cmegroup.com/articles/brochures-and-handbooks/101-overview-cme-clearing-liquidity-risk-management-practices.html | CME describes liquidity stress testing with historical and hypothetical scenarios for clearing liquidity-risk management. |
| `dtcc_stress_testing` | DTCC Stress Testing | `official_platform_doc` | https://www.dtcc.com/managing-risk/financial-risk-management/stress-testing | DTCC states stress testing measures stress-scenario impact on credit and liquidity exposures and financial resources for each clearing agency. |
| `fia_automated_controls_2024` | Best Practices for Automated Trading Risk Controls and System Safeguards | `professional_body` | https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf | FIA covers automated trading risk controls, exchange volatility controls, post-trade analysis, testing and system safeguards. |

## 候选列表

| ID | title | source_count | 状态 |
| --- | --- | ---: | --- |
| P45-E-STRESS01 | 场景压力测试必须声明场景、假设和 owner | 3 | candidate_ready |
| P45-E-STRESS02 | 流动性压力必须和价格 PnL 压力分开 | 4 | candidate_ready |
| P45-E-STRESS03 | 相关性在压力下可能失效 | 3 | candidate_ready |
| P45-E-STRESS04 | 跳空和隔夜风险必须独立审计 | 3 | candidate_ready |
| P45-E-STRESS05 | 尾部亏损必须配合压力场景复核 | 3 | candidate_ready |
| P45-E-STRESS06 | 压力测试通过不等于交易许可 | 3 | candidate_ready |

## 边界

```text
1. 不输出风险阈值、仓位、杠杆、买卖点、止损止盈或实盘执行建议。
2. PFMI、BCBS、CCP、CME、DTCC、FIA 来源必须保留机构、清算、venue、产品和治理语境边界。
3. 候选知识必须等待外部严格审计，不得直接进入 formal reviewed。
```
