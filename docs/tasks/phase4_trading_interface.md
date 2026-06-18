# Phase 4 统一交易接口任务卡

## Phase 目标

定义 CEK-TA 的统一交易接口契约，让回测、市场回放、模拟盘和实盘在同一套策略语义下运行，只替换数据源和执行适配器，避免同一策略在不同环境中出现隐性语义漂移。

核心原则：

```text
Strategy semantics stay stable.
DataSource and ExecutionAdapter are replaceable.
FillModel assumptions must be explicit.
Live trading safety boundaries must not be weakened by backtest convenience.
```

## 任务列表

| ID | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- |
| CEK-TA-013 | done | 定义核心数据契约 | `codex-expert-kit/templates/interface_contract.md` |
| CEK-TA-014 | done | 定义 ExecutionAdapter 契约 | `codex-expert-kit/templates/execution_adapter_spec.md` |
| CEK-TA-015 | done | 定义 FillModel 规则 | `codex-expert-kit/templates/fill_model_spec.md` |

## 上游输入

```text
codex-expert-kit/core/AGENTS.md
codex-expert-kit/templates/project_AGENTS.md
codex-expert-kit/domains/quant_trading/README.md
codex-expert-kit/domains/backtest_replay_simulation/README.md
codex-expert-kit/rag/retrieval_policy.md
codex-expert-kit/rag/knowledge_item_schema.md
```

## 下游输出

```text
Phase 5 交易分析闭环:
  使用 OrderIntent、OrderRequest、FillEvent、PositionSnapshot、TradeResult 作为交易分析输入基础。

Phase 8 其他项目接入:
  业务项目用 interface_contract.md 和 execution_adapter_spec.md 对齐本地字段和 CEK-TA 统一语义。

回测/回放/模拟盘/实盘项目:
  通过同一策略输出 OrderIntent，再由不同 ExecutionAdapter 转成环境内动作。

Codex 审计:
  检查策略修改是否改变了输入、输出、交易频率、风险、成本、持仓时间或回滚路径。
```

## 输入契约

策略层输入必须声明：

```text
MarketEvent
FeatureFrame
SignalFrame
PositionSnapshot
RiskState
StrategyConfig
ClockState
```

策略层输出必须声明：

```text
Decision
OrderIntent
RiskDecision
ReasonCode
AuditTrace
```

## 输出契约

ExecutionAdapter 输出必须能被交易分析和审计消费：

```text
OrderRequest
OrderAck
FillEvent
OrderState
PositionSnapshot
ExecutionReport
ErrorEvent
```

FillModel 输出必须能说明：

```text
fill_price
fill_qty
fee
slippage
latency
partial_fill
same_candle_ordering
assumption_id
```

## 边界范围

本 Phase 做：

```text
1. 定义交易系统核心数据结构。
2. 定义策略层和执行层边界。
3. 定义 ExecutionAdapter 输入、输出、状态机、错误处理和审计要求。
4. 定义 FillModel 假设、同 K 线 TP/SL、滑点、手续费、延迟、部分成交规则。
5. 更新任务索引和 README 入口。
```

本 Phase 不做：

```text
1. 不连接真实交易所。
2. 不实现下单。
3. 不读取账户、密钥或实盘配置。
4. 不定义某个项目的私有字段。
5. 不改变策略逻辑。
6. 不引入数据库或后端框架。
```

## 涉及组件

```text
docs/tasks/phase4_trading_interface.md
codex-expert-kit/templates/interface_contract.md
codex-expert-kit/templates/execution_adapter_spec.md
codex-expert-kit/templates/fill_model_spec.md
docs/index_tasks.md
docs/tasks/README.md
codex-expert-kit/README.md
```

## 涉及数据结构

```text
MarketEvent
Kline
TradePrint
OrderBookSnapshot
FeatureFrame
SignalFrame
Decision
OrderIntent
OrderRequest
OrderAck
FillEvent
OrderState
PositionSnapshot
RiskState
ExecutionReport
FillAssumption
```

## 涉及数据库/存储

当前 Phase 不引入数据库。所有结构先作为模板契约。后续业务项目如落数据库，必须在业务项目任务卡中定义主键、索引、状态字段、时间字段、审计字段、迁移和回滚。

## 实施步骤

```text
1. 创建 Phase 4 任务卡。
2. 创建 interface_contract.md。
3. 创建 execution_adapter_spec.md。
4. 创建 fill_model_spec.md。
5. 更新 docs/index_tasks.md。
6. 更新 docs/tasks/README.md。
7. 更新 codex-expert-kit/README.md。
8. 执行文件存在性、关键章节、索引状态、UTF-8 检查。
```

## Definition of Done

```text
1. Phase 4 任务卡存在，并包含上下游、契约、边界、DoD 和测试。
2. interface_contract.md 定义核心数据结构和策略语义边界。
3. execution_adapter_spec.md 定义 adapter 输入输出、状态机、错误处理、权限和测试。
4. fill_model_spec.md 定义成交假设、同 K 线 TP/SL、滑点、手续费、延迟、部分成交和审计字段。
5. docs/index_tasks.md、docs/tasks/README.md、Phase 任务卡状态一致。
6. codex-expert-kit/README.md 有 Phase 4 入口。
7. 中文文档 UTF-8 读取无乱码。
```

## 测试与验收

```text
1. Test-Path 检查全部交付物存在。
2. Select-String 检查关键章节存在。
3. 检查 Phase 4、CEK-TA-013、CEK-TA-014、CEK-TA-015 均为 done。
4. Get-Content -Encoding UTF8 检查中文文档无乱码。
5. 检查模板不包含真实交易所密钥、账户字段或下单实现。
```

## 风险与回滚

风险：

```text
1. 契约过宽会导致业务项目难以落地。
2. 契约过窄会导致回测和实盘语义不一致。
3. FillModel 假设如果默认化过强，会掩盖真实执行风险。
```

回滚：

```text
1. 文档变更可通过版本控制回退。
2. 后续新增字段必须保持向后兼容，优先增加 optional 字段和 schema_version。
3. 业务项目已经采用旧契约时，不直接删除字段，先 deprecated。
```

## 需要开发者确认的问题

当前 Phase 只定义文档契约，不引入数据库、后端框架、交易所接入、外部服务或不可逆迁移，因此无需确认。

后续如果要实现真实交易所 adapter、引入事件总线、数据库、队列或实盘权限，必须单独向开发者确认。

## 状态更新要求

完成后必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase4_trading_interface.md
codex-expert-kit/README.md
```
