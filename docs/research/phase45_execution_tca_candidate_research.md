# Phase 45 Execution TCA 候选知识采集记录

## 目标

本批为 Phase 45 / P45-A / Execution TCA 6 条候选知识。所有条目只进入 candidate，不创建正式 reviewed、approved、default guidance 或 hard gate。

## 来源摘要

| source_id | 来源 | 类型 | URL | 用途 |
| --- | --- | --- | --- | --- |
| `cfa_trading_costs` | Trading Costs and Electronic Markets | `professional_body_reading` | https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets | CFA explains implementation shortfall, explicit and implicit trading costs, market impact, delay cost, opportunity cost, and benchmark limitations in electronic markets. |
| `cfa_trade_strategy_execution` | Trade Strategy and Execution | `professional_body_reading` | https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution | CFA describes trade cost analysis, execution quality, trading policies, escalation procedures, venue/partner selection, and post-trade evaluation. |
| `finra_5310` | FINRA Rule 5310: Best Execution and Interpositioning | `regulatory_rule` | https://www.finra.org/rules-guidance/rulebooks/finra-rules/5310 | FINRA Rule 5310 requires reasonable diligence to ascertain the best market and obtain favorable execution under prevailing market conditions. |
| `sec_rule_606_faq` | SEC FAQ: Rule 606 of Regulation NMS | `regulatory_guidance` | https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions/faq-rule-606-regulation | SEC Rule 606 guidance supports order routing disclosure and execution-quality transparency for routing services. |
| `fix_execution_report` | FIX 4.4 Execution Report | `official_protocol_doc` | https://fiximate.fixtrading.org/legacy/en/FIX.4.4/body_5756.html | FIX Execution Report supports order/execution event semantics and the separation of order state, fills, and post-trade reports. |
| `quantconnect_fills` | QuantConnect Reality Modeling: Trade Fills Key Concepts | `platform_doc` | https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts | QuantConnect fill modeling docs support the boundary that execution assumptions, fills, slippage, and fees are modeled components rather than strategy edge. |

## 候选条目

| research_task_id | candidate_id | partition | canonical_node_id | 来源数 |
| --- | --- | --- | --- | --- |
| P45-A-TCA01 | `cand_20260612_phase45_execution_tca_p45_a_tca01_001` | `KB_07_TRADE_ANALYSIS` | `kt.trade_analysis.execution_tca_review` | 3 |
| P45-A-TCA02 | `cand_20260612_phase45_execution_tca_p45_a_tca02_001` | `KB_07_TRADE_ANALYSIS` | `kt.trade_analysis.execution_tca_review` | 3 |
| P45-A-TCA03 | `cand_20260612_phase45_execution_tca_p45_a_tca03_001` | `KB_06_LIVE_EXECUTION` | `kt.live_execution.execution_tca` | 3 |
| P45-A-TCA04 | `cand_20260612_phase45_execution_tca_p45_a_tca04_001` | `KB_07_TRADE_ANALYSIS` | `kt.trade_analysis.execution_tca_review` | 3 |
| P45-A-TCA05 | `cand_20260612_phase45_execution_tca_p45_a_tca05_001` | `KB_06_LIVE_EXECUTION` | `kt.live_execution.execution_tca` | 3 |
| P45-A-TCA06 | `cand_20260612_phase45_execution_tca_p45_a_tca06_001` | `KB_06_LIVE_EXECUTION` | `kt.live_execution.execution_tca` | 4 |

## 边界

```text
1. Execution TCA 只解释执行成本、执行质量、benchmark、routing context 和算法执行边界。
2. 不生成买卖点、仓位、杠杆、止损止盈、风险阈值或实盘许可。
3. 不把 VWAP/TWAP/POV/arrival-price 算法写成策略 edge。
4. FINRA/SEC 来源只约束对应辖区和场景，不泛化到所有市场。
5. 候选必须等待外部 AI/人工审计。
```
