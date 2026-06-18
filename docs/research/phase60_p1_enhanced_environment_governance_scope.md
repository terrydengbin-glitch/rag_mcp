# Phase 60 P1 增强环境治理知识范围

生成日期：2026-06-17

## 目标

Phase 60 P0 已完成 sandbox、testnet、historical replay、paper trading、live canary 的基础边界、manifest、promotion decision 和 gap report。

P1 继续补 6 条增强知识，覆盖测试环境从“能跑”到“可审计、可复现、可回滚、可监控”的治理层。它们仍只允许进入候选审计，不直接创建 reviewed、approved、default guidance 或 hard gate。

## P1 6 条知识范围

| ID | 目标分支 | 主题 | 主要边界 |
| --- | --- | --- | --- |
| P60-P1-01 | KB_06_LIVE_EXECUTION | FIX / broker certification sandbox 必须作为 adapter 上线前的契约测试证据 | 只验证消息、字段、场景和 adapter 行为，不证明策略收益或真实流动性 |
| P60-P1-02 | KB_05_REPLAY_SIMULATION | replay / simulation scenario library 必须版本化 | 场景库用于复现异常、波动、停牌、撮合和错误恢复，不得当作未来收益证据 |
| P60-P1-03 | KB_06_LIVE_EXECUTION | paper account reset、初始资金和账户状态必须可追踪 | paper 账户重置或虚拟资金会改变评估语义，不能与 live 账户事实混用 |
| P60-P1-04 | KB_06_LIVE_EXECUTION | realtime simulation 必须记录心跳、断线、延迟和数据 stale 状态 | 只证明环境健康与 adapter 稳定性，不等于交易许可 |
| P60-P1-05 | KB_07_RISK_MANAGEMENT | live canary 必须有 rollback / stop condition / owner | canary 是小范围真实环境观察，不得自动扩大为 full live |
| P60-P1-06 | KB_05_REPLAY_SIMULATION | environment drift monitor 必须比较 replay、paper、canary 与 live 的差异趋势 | drift report 是治理和人工复核材料，不是 hard gate 或收益证明 |

## 来源种子

```text
TT FIX Certification
https://library.tradingtechnologies.com/tt-fix/general/Certification.html

FIXSIM
https://www.fixsim.com/

Paxos FIX Certification
https://docs.paxos.com/guides/crypto-brokerage/fix/certify

J.P. Morgan AI Research: Single Agent Market Replay or Multi-Agent Simulation
https://www.jpmorgan.com/content/dam/jpm/cib/complex/content/technology/ai-research-publications/pdf-12.pdf

QuantConnect Paper Trading
https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/quantconnect-paper-trading

Alpaca Paper Trading
https://docs.alpaca.markets/us/docs/paper-trading

NautilusTrader Architecture
https://nautilustrader.io/docs/latest/concepts/architecture/

FIX Trading Community Execution Report
https://www.fixtrading.org/online-specification/order-state-changes/

LaunchDarkly Canary Deployments
https://launchdarkly.com/docs/home/releases/canary

Google SRE Book: Monitoring Distributed Systems
https://sre.google/sre-book/monitoring-distributed-systems/
```

## 不做什么

```text
1. 不创建 approved。
2. 不进入 default guidance。
3. 不创建 hard gate。
4. 不输出买卖点、仓位、杠杆、止损止盈、风控阈值或实盘执行建议。
5. 不把 FIX / broker / exchange / vendor 的测试工具写成 CEK-TA 强制依赖。
6. 不把 paper / replay / canary 的表现写成策略有效或实盘许可。
```

## 下游

```text
1. CEK-TA-582 生成 6 条候选知识。
2. CEK-TA-583 导出候选审计包。
3. 外部 AI/人工审计后，CEK-TA-584 回写 accepted_for_draft / needs_more_evidence / rejected / blocked。
4. 只有 reviewed-preparation 审计通过后，CEK-TA-585 才能沉淀 formal reviewed/caveat_only。
```
