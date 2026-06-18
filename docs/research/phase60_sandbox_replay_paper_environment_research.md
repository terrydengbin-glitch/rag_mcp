# Phase 60 Sandbox / Replay / Paper Trading 环境治理研究报告

生成日期：2026-06-17

## 研究目标

本报告用于支撑 Phase 60 的 P0 候选知识采集：如何创建、使用和管理沙盒、测试网、历史回放、实时模拟执行、模拟盘 / paper trading 与 live canary，使它们服务于测试、回放和模拟盘治理。

本报告的结论不是交易策略建议，也不证明任何策略可以实盘。它只定义环境证据、模拟假设、订单生命周期、晋级决策和 gap report 的治理边界。

## 总体结论

更稳健的环境链条应分层管理：

```text
static API sandbox
  -> 用于验证 API contract、字段格式、鉴权、请求/响应和错误结构

exchange testnet / demo trading
  -> 用于验证 venue-specific endpoint、账户隔离、订单生命周期和 adapter 行为

historical replay
  -> 用历史市场数据验证事件时钟、fill model、latency model、费用和 market-impact 假设

realtime simulation / sandbox execution
  -> 用实时行情和模拟执行验证订单链条、风控 rehearsal、状态同步和错误恢复

paper trading
  -> 用实时行情和虚拟资金做端到端演练，但必须保留模拟成交、费用、队列、延迟和 market impact 限制

live canary
  -> 用小范围真实资金和真实订单验证模拟环境无法证明的 live gap，但仍不等于放大实盘许可
```

每一层都必须输出 `environment_manifest`，跨层推进必须输出 `promotion_decision` 和 `gap_report`。任何一层的盈利、胜率、PnL 或 R/R 都不能替代这些证据。

## 权威资料与证据

### NautilusTrader：同一架构下区分 backtest / sandbox / live

NautilusTrader 官方架构文档明确区分 environment contexts：Backtest 使用 Historical + Simulated，Sandbox 使用 Realtime + Simulated，Live 使用 Realtime + Live Venue。它强调同一系统边界和组件结构可跨环境复用，但环境上下文仍然不同。

来源：

```text
NautilusTrader Architecture
https://nautilustrader.io/docs/latest/concepts/architecture/
source_type: framework_doc
```

适用边界：

```text
可用于支撑 environment taxonomy、shared runtime、sandbox/live 区分。
不得写成所有外接项目必须使用 NautilusTrader。
```

### QuantConnect：paper trading 是实时数据 + 虚拟资金 + 模拟成交

QuantConnect Paper Trading 文档说明 paper trading 会把实时数据送入算法，但交易使用 fictional capital，订单不会路由到交易所，成交是模拟的。

来源：

```text
QuantConnect Paper Trading
https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/quantconnect-paper-trading
source_type: platform_doc
```

适用边界：

```text
可用于支撑 paper trading 与 live trading 的区分。
不得把 paper trading 盈亏写成 live-ready 或策略优势证明。
```

### HftBacktest：市场数据回放不能改变市场，必须声明 no-market-impact 假设

HftBacktest 文档和维护者说明强调其为 market-data replay-based backtesting，回放中的订单不能改变市场，no-market-impact 假设非常关键。

来源：

```text
HftBacktest order fill documentation
https://hftbacktest.readthedocs.io/en/latest/order_fill.html
source_type: framework_doc
```

适用边界：

```text
可用于支撑 replay/fill model/market impact caveat。
不得泛化为所有 replay 框架的唯一实现方式。
```

### Alpaca：paper trading 不包含 market impact、信息泄露、延迟滑点、队列位置等

Alpaca Paper Trading 文档列出 paper trading 不能覆盖的 live 差异，包括订单 market impact、信息泄露、延迟导致的价格滑点、非市价限价单队列位置、price improvement、监管费用和分红。

来源：

```text
Alpaca Paper Trading
https://docs.alpaca.markets/us/docs/paper-trading
source_type: broker_platform_doc
```

适用边界：

```text
可用于支撑 paper/live gap report 字段。
不得作为所有券商 paper trading 的完整差异清单。
```

### IBKR：paper account 是 simulator，存在生产账户差异

IBKR 文档说明 paper trading account 模拟大部分生产账户，但因其 simulator 构造会存在差异；paper trading 适合学习平台、工具和功能。

来源：

```text
IBKR About Paper Trading Accounts
https://www.ibkrguides.com/clientportal/aboutpapertradingaccounts.htm
source_type: broker_doc
```

适用边界：

```text
可用于支撑 broker-specific paper account caveat。
不得把 IBKR paper account 行为泛化为所有 broker。
```

### Binance：testnet / demo endpoint 必须与生产 endpoint 区分

Binance USDⓈ-M Futures General Info 文档提供 testnet REST 与 WebSocket base URL，说明多数 endpoint 可用于 testnet platform。

来源：

```text
Binance USD-M Futures General Info
https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info
source_type: exchange_api_doc
```

适用边界：

```text
可用于支撑 testnet endpoint isolation、API endpoint scope 和环境隔离。
不得写成所有交易所都有同样 testnet 语义。
```

### Coinbase：static sandbox 只返回 mocked response，不能证明市场行为

Coinbase Advanced Trade API Sandbox 文档说明 sandbox 目前只支持 Accounts 和 Orders 相关 endpoint，所有响应是 mocked，但格式与生产一致。

来源：

```text
Coinbase Advanced Trade API Sandbox
https://docs.cdp.coinbase.com/coinbase-app/advanced-trade-apis/sandbox
source_type: exchange_api_doc
```

适用边界：

```text
可用于支撑 static API sandbox 只能验证接口格式和字段契约。
不得把 mocked response 写成真实市场、真实成交或真实账户行为。
```

### FIX Execution Report：订单状态、成交、拒单和费用报告需要统一生命周期映射

FIX Execution Report 文档说明该消息用于确认订单接收、修改、订单状态、成交、拒单和交易后费用计算。

来源：

```text
FIX 4.4 Execution Report
https://www.onixs.biz/fix-dictionary/4.4/msgtype_8_8.html
source_type: standard_doc
```

适用边界：

```text
可用于支撑统一 order lifecycle / order state mapping。
不得把 FIX 状态直接写成所有 REST/WebSocket API 的原生状态。
```

## Phase 60 P0 知识范围

| ID | 知识点 | 主分支 | 目的 |
| --- | --- | --- | --- |
| P60-A01 | 环境类型必须显式声明 | Replay / Simulation | 防止 backtest、sandbox、paper、live 混用 |
| P60-A02 | static API sandbox 只能验证 API contract | Live Execution | 防止 mocked response 被误认为市场行为 |
| P60-A03 | testnet/demo endpoint 与生产 endpoint 必须隔离 | Live Execution | 防止 testnet key、endpoint、账户状态污染生产 |
| P60-A04 | paper trading 不等于 live trading | Replay / Simulation | 防止 paper 盈亏被当成 live-ready |
| P60-A05 | historical replay 必须声明 no-market-impact 与 fill 假设 | Replay / Simulation | 防止回放成交被当成真实成交能力 |
| P60-A06 | environment manifest 必须存在 | Replay / Simulation | 统一记录数据、时钟、adapter、fill、latency、fee、risk |
| P60-A07 | environment promotion 必须有证据门槛 | Risk Management | 防止从 sandbox/paper 直接跳到 live |
| P60-A08 | sandbox / paper / live gap report 必须标准化 | Replay / Simulation | 记录数据、成交、费用、延迟、订单状态和风控差异 |
| P60-A09 | 订单生命周期必须跨环境统一映射 | Live Execution | 防止订单状态、拒单、部分成交和费用语义混乱 |
| P60-A10 | sandbox risk rehearsal 不等于 live hard gate | Risk Management | 防止模拟风控演练被当作真实拒单/停机权限 |

## Phase 60 P1 后续范围

```text
1. sandbox seed data / fixture governance
2. replay clock vs wall-clock sandbox clock
3. network disconnect / retry / idempotency simulation
4. paper statement / audit report retention
5. live canary 小资金边界和回滚计划
6. sandbox 环境权限、密钥、账户和 endpoint 隔离审计
```

## 关键边界

```text
1. sandbox pass 不等于策略有效。
2. testnet order accepted 不等于 live exchange 会接受同样订单。
3. paper profit 不等于 live-ready。
4. replay fill 不等于真实队列位置、真实 market impact 或真实成交能力。
5. promotion decision 不是实盘许可，只是环境推进评审证据。
6. gap report 不能直接触发自动下单、自动拒单、自动停机或 hard gate。
```

## 对齐现有知识库

```text
Phase 58:
  提供环境等效链条和 environment_equivalence_manifest 的基础。

Phase 37 Replay / Simulation:
  提供 event clock、fill model、simulation-live gap、execution cost consistency 等知识。

Phase 45 Execution / Risk:
  提供订单语义、审计追踪、系统韧性和风险边界。

Phase 60:
  在以上基础上补齐 sandbox / testnet / paper / live canary 的环境治理和晋级证据。
```
