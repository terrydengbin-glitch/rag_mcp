# Phase 58 回测 / 回放 / 模拟盘 / 实盘等效链条资料研究

## 研究目标

本研究用于支撑一条 Trading Engineering 候选知识：

```text
同一交易系统中，回测、回放、模拟盘和实盘只有走同一真实策略链条，或具备字段级等效链条映射和差异报告时，结果才可比较。
```

这里的“等效”不是指收益相同，也不是指环境名称相同，而是指信号生成、数据可用时间、事件时钟、风控检查、订单意图、成交模型、成本模型、状态机、仓位账户同步和审计日志在工程链路上可追踪、可比较、可解释。

## 来源摘要

| 来源 | 类型 | 关键结论 | 对候选知识的作用 |
| --- | --- | --- | --- |
| NautilusTrader Architecture | 开源交易系统文档 | 将环境分为 Backtest、Sandbox、Live；Backtest 使用历史数据和模拟场所，Sandbox 使用实时数据和模拟场所，Live 使用实时数据和真实或 paper 场所；平台设计目标是在三类系统之间共享尽可能多的共同代码。 | 支撑“环境不同，但应共享共同核心和端口适配层”的工程原则。 |
| NautilusTrader Live Trading | 开源交易系统文档 | backtested strategies 可无代码改动部署到 live；同一 actors、strategies、execution algorithms 可运行在 backtest engine 和 live node；live 前需要理解配置、运行、执行 reconciliation 和 backtest/live 差异。 | 支撑“同一策略链条/共同执行算法”是可比性的前提，同时必须保留 reconciliation 和差异审计。 |
| QuantConnect Paper Trading | 量化平台文档 | paper trading 使用实时市场数据运行算法，但用虚拟资金和模拟成交；paper trading 可用于测试算法并检查 backtest 是否过拟合；paper brokerage 与 backtesting brokerage 有不同实现。 | 支撑“paper/sandbox 不是 live truth，实时数据加模拟成交仍需模型边界”。 |
| QuantConnect Live Trading | 量化平台文档 | live algorithm 在实时市场数据下运行并接入 live trading 部署流程。 | 支撑 live 与 backtest/paper 的环境差异：实时数据、运行节点和交易链路不同。 |
| HftBacktest Order Fill | 回放/高频回测文档 | market-data replay 回测无法改变模拟市场，不考虑市场冲击；订单必须足够小的假设很关键；最终必须用 live market 测试并按 backtest 与 live 的差异调整。 | 支撑“回放/回测成交模型必须显式声明假设，并通过 live 差异报告校准”。 |
| QuantStart Backtesting Considerations | 专业量化文章 | 事件驱动回测可以让 backtest 与 live trading 的核心策略/组合代码更容易保持一致。 | 支撑“事件驱动架构更适合真实链条复用”，但只能作为 supporting source。 |
| Investopedia Backtesting / Forward Performance Testing | 金融教育资料 | forward performance testing 常称 paper trading，按系统逻辑在 live market 中模拟交易；backtest、out-of-sample 和 forward performance 的相关性对系统验证重要。 | 支撑“paper trading 是过渡验证，不是直接等于 live”的教育层解释。 |

## 业界定义归纳

### Backtest

```text
Backtest 通常使用历史数据、模拟交易场所、模拟成交和模拟账户状态来验证策略逻辑、研究假设和风险表现。
```

Backtest 的价值在于快速覆盖历史样本、测试策略逻辑和生成研究证据。它的限制是成交、滑点、延迟、订单排队、市场冲击、拒单、账户同步和实时故障通常被模型化或简化。

### Replay

```text
Replay 通常使用历史 tick / order book / event stream 重新播放市场数据，并在模拟交易所或成交模型中重演订单行为。
```

Replay 的价值是比普通 OHLC 回测更接近真实事件时钟和盘口路径。它的限制是历史市场不会因模拟订单而改变，尤其在吃流动性、大订单、排队和市场冲击场景下可能不真实。

### Sandbox / Paper Trading

```text
Sandbox / Paper Trading 通常使用实时市场数据和模拟成交或模拟账户，让策略在当前市场条件下运行，但不承担真实资金风险。
```

Paper 的价值是检验实时数据、调度、消息、日志、风险检查和运维链路。它的限制是成交、资金、保证金、费用、拒单和账户同步仍可能不等于真实经纪商或交易所。

### Live Trading

```text
Live Trading 使用实时数据、真实或 paper 交易场所、真实订单状态和真实运行风险。
```

Live 的关键不是收益本身，而是订单生命周期、风控、账户同步、执行报告、异常处理和审计链路都必须按真实环境处理。

## 等效链条判断

一个策略从 backtest 推进到 replay、paper/sandbox、live，至少需要以下链路一致或可映射：

```text
1. strategy_code_version：策略代码版本一致，或差异有审计记录。
2. strategy_config_hash：参数、开关、资产池、时间框架、特征开关一致。
3. data_available_time：信号只能使用当时可见数据。
4. event_clock：历史事件、回放事件、实时事件的时间语义可比较。
5. signal_output_schema：信号、目标、订单意图字段一致。
6. risk_check_chain：事前风控检查在各环境中一致或有等效映射。
7. order_intent_schema：订单方向、数量、订单类型、时效、路由上下文一致。
8. fill_cost_latency_model：回测/回放/模拟成交模型和实盘成交差异可解释。
9. order_state_machine：提交、确认、部分成交、拒单、撤单、超时、未知状态可映射。
10. position_account_truth：仓位、现金、保证金、费用和账户事实有来源优先级。
11. audit_trace：每个环境都能追踪策略版本、数据版本、订单事件和差异报告。
```

如果这些字段缺失，系统可以说“在某环境下运行过”，但不能说“回测、模拟盘、实盘等效”。

## 需要进入候选知识的核心规则

```text
同一系统内，回测、回放、模拟盘和实盘之间的结果不能因为策略名称相同就被视为可比或等效。只有当信号、数据时间、事件时钟、风控、订单意图、成交成本延迟模型、订单状态、仓位账户同步和审计日志走同一真实链条，或提供字段级等效映射与 gap report 时，才可以比较结果、推进环境或用于 AI 训练标签。
```

## 边界

```text
1. 该知识不生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。
2. 该知识不要求所有项目使用 NautilusTrader、QuantConnect 或 HftBacktest。
3. 该知识不声称 paper trading 等于 live trading。
4. 该知识不声称 backtest 结果可以证明策略可实盘。
5. 该知识只用于工程等效性审计、项目方案审查、候选知识检索和 AI IDE 设计提醒。
```

## 后续建议

```text
1. 外部 AI/人工审计本候选是否足以 accepted_for_draft。
2. 审计通过后，可拆出三条 reviewed/caveat_only 知识：
   - strategy_chain_equivalence_required
   - environment_gap_report_required
   - paper_replay_live_promotion_checklist
3. 后续可以为 DogSignal Gate 的外接交易项目生成“环境推进清单”模板。
```

## 来源链接

```text
NautilusTrader Architecture:
https://nautilustrader.io/docs/latest/concepts/architecture/

NautilusTrader Live Trading:
https://nautilustrader.io/docs/latest/concepts/live/

QuantConnect Paper Trading:
https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/quantconnect-paper-trading

QuantConnect Live Trading:
https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/getting-started

HftBacktest Order Fill:
https://hftbacktest.readthedocs.io/en/latest/order_fill.html

QuantStart Backtesting Considerations:
https://www.quantstart.com/articles/backtesting-systematic-trading-strategies-in-python-considerations-and-open-source-frameworks/

Investopedia Backtesting:
https://www.investopedia.com/articles/trading/05/030205.asp
```
