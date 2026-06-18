# Phase 45 Execution TCA 补证记录

## 补证目标

首轮审计中 P45-A-TCA03 与 P45-A-TCA06 被判定为 needs_more_evidence。本文件记录补证来源、claim 收窄和边界修补。

## P45-A-TCA03 补证

| source_id | 来源 | 类型 | URL | 用途 |
| --- | --- | --- | --- | --- |
| `fixatdl` | FIX Algorithmic Trading Definition Language | `official_protocol_doc` | https://fixtrading.org/standards/fix-algorithmic-trading-definition-language/ | FIXatdl is a vendor-neutral standard for describing algorithmic trading strategy user interfaces and parameters across order/execution management systems. |
| `ibkr_algos` | IBKR Order Types, Algos and Tools | `broker_official_doc` | https://www.interactivebrokers.com/en/trading/ordertypes.php | IBKR lists broker order types and algos as execution tools used to limit risks, speed execution, support price improvement and simplify trading process. |
| `ibkr_vwap` | IBKR VWAP Best Efforts Order | `broker_official_doc` | https://www.interactivebrokers.com/campus/trading-lessons/vwap-best-efforts-order-in-ibkr-desktop/ | IBKR describes VWAP as an algo seeking to achieve the volume-weighted average price over a defined interval. |
| `ibkr_twap` | IBKR Time-Weighted Average Price (TWAP) | `broker_official_doc` | https://www.interactivebrokers.com/campus/trading-lessons/time-weighted-average-price-twap/ | IBKR describes TWAP as an algo designed to attain time-weighted average price during a specified period. |

修补后 claim：VWAP/TWAP/POV 或 participation 类算法应被描述为 execution scheduling / participation algorithm；它们不是策略 alpha。CEK-TA 内部边界要求它们不得绕过订单、风控、流动性、市场状态和 venue-specific 约束。

## P45-A-TCA06 补证

| source_id | 来源 | 类型 | URL | 用途 |
| --- | --- | --- | --- | --- |
| `bailey_pbo` | The Probability of Backtest Overfitting | `paper` | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253 | Bailey et al. propose a framework to estimate probability of backtest overfitting in investment simulations, supporting independent validation before promoting claims. |
| `white_reality_check` | A Reality Check for Data Snooping | `paper` | https://www.jstor.org/stable/2999444 | White's Reality Check addresses data-snooping risk when the same data is reused for inference or model selection. |

修补后 claim：execution optimization 默认只能改善或解释 implementation cost；如果要把 execution-derived feature、低滑点或 benchmark outperform 写成 alpha，必须转入独立策略研究验证流程，并接受样本外、data snooping、过拟合和 leakage 审计。

## 硬边界

```text
1. 补证不创建 formal reviewed。
2. 补证不创建 approved、default guidance 或 hard gate。
3. 不生成买卖点、仓位、杠杆、止损止盈、实盘执行建议或风险阈值。
4. broker-specific algorithm docs 只能作为算法执行语义示例。
5. strategy validation papers 只支撑转入策略研究验证流程，不证明执行特征有 alpha。
```
