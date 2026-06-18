# Phase 53 AI/Trading 安全、市场行为与运行治理知识范围

创建日期：2026-06-13

## 范围结论

Phase 53 承接 Phase 52 的权威资料缺口复审，只补齐 AI Engineering 与 Trading Engineering 中“外接交易 AI 项目上线前必须具备，但当前知识库覆盖较弱”的治理型知识。

本 Phase 不补交易策略技巧，不生成交易建议，不输出法律意见，不创建 approved/default guidance/hard gate。

## 上下游链条

```text
Phase 52 缺口复审
-> Phase 53 范围与来源种子
-> Phase 53 候选采集
-> 外部 AI/人工严格审计
-> Codex 按补丁点补证或重建
-> formal reviewed/caveat_only
-> MCP/SearchLab/KnowledgeTree/Vue3 联动验证
```

## L1/L2/L3 归类方案

### AI Engineering

| L2 | L3 | canonical_node_id | 目标 |
| --- | --- | --- | --- |
| Security Governance | Agent Threat Model | `kt.ai_engineering.security_governance.agent_threat_model` | 将 OWASP/MITRE/NIST 的 LLM/Agent 风险映射到交易 AI IDE、MCP 工具、RAG、记忆层和 final gate 边界 |
| Supply Chain Governance | AI SBOM | `kt.ai_engineering.supply_chain_governance.ai_sbom` | 定义模型、adapter、数据集、依赖、容器、推理服务、许可证和来源透明度清单 |

### Trading Engineering

| L2 | L3 | canonical_node_id | 目标 |
| --- | --- | --- | --- |
| Market Conduct | Surveillance Taxonomy | `kt.trading_engineering.market_conduct.surveillance_taxonomy` | 定义 spoofing、layering、wash/self-trade、momentum ignition 等市场行为监控 taxonomy |
| Market Access | Regulatory Boundary | `kt.trading_engineering.market_access.regulatory_boundary` | 定义 Market Access、DEA、sponsored access、Reg NMS、MiFID II 算法交易接入控制边界 |
| Audit Trace | Time Synchronization | `kt.trading_engineering.audit_trace.time_synchronization` | 定义订单、行情、成交、风控、RAG 审计日志的 clock source、同步状态、精度和漂移策略 |

## P0 知识点范围

### GAP-AI-01 Trading AI Agent Threat Model

目标 statement：

```text
交易 AI Agent 必须把 prompt injection、tool misuse、memory poisoning、excessive agency、overreliance、sensitive information disclosure 和 supply chain compromise 作为独立威胁面建模；LLM/RAG/MCP 只能提供分析、审计、解释和检索辅助，不能绕过 deterministic final gate、Risk Management 或 Live Execution owner。
```

适用范围：

```text
AI IDE
RAG/MCP 检索
交易审计助手
外接项目 agent orchestration
项目记忆层
工具调用链路
```

不适用：

```text
普通离线文档阅读
没有工具权限的纯文本总结
人工自己判断的非自动化流程
```

边界：

```text
不得输出交易信号。
不得把 LLM 安全风险自动解释成交易 hard gate。
不得给出漏洞利用步骤。
```

### GAP-AI-02 AI SBOM / Model SBOM

目标 statement：

```text
外接交易 AI 项目在使用模型、LoRA/adapter、embedding model、RAG index、训练数据、容器、依赖和推理服务前，应维护 AI SBOM / Model SBOM，用于供应链透明度、许可证审计、漏洞影响分析、模型来源追踪和回滚。
```

适用范围：

```text
Qwen3 / LLM 审计助手
LightGBM / XGBoost / Logistic Regression scorer
embedding / reranker
RAG index
训练与推理容器
外部模型服务
```

不适用：

```text
一次性本地实验且不进入共享环境
没有外部依赖和没有复用价值的草稿脚本
```

边界：

```text
不强制具体 SBOM 工具。
不把 SBOM 当作安全通过证明。
不把供应链信息暴露给未授权用户。
```

### GAP-TR-01 Market Conduct Surveillance Taxonomy

目标 statement：

```text
交易系统应将 spoofing、layering、wash/self-trade、momentum ignition、marking the close、front-running 等市场行为风险作为监控 taxonomy 和审计上下文；该 taxonomy 只用于合规/审计/人工复核，不得替代法律结论或自动交易许可。
```

适用范围：

```text
订单事件审计
交易后复盘
异常行为监控
broker/venue adapter 风险说明
AI 审计助手 reason code
```

不适用：

```text
判断某个用户是否违法
替代合规负责人或律师结论
无订单簿/订单事件证据的纯 K 线分析
```

边界：

```text
不得输出法律意见。
不得把异常标签直接变成硬阻断。
不得把正常做市/撤单泛化为市场操纵。
```

### GAP-TR-02 Market Access / DEA / Reg NMS Boundary

目标 statement：

```text
外接项目若连接 broker、交易所、ATS、DEA 或 sponsored access，应明确 market access owner、预交易金融/监管/错误订单控制、接入权限、年度/周期性 review、venue jurisdiction 和 recordkeeping；CEK-TA 只能沉淀证据契约和边界，不能输出合规意见或具体阈值。
```

适用范围：

```text
Live Execution
Risk Management
broker adapter
venue adapter
direct electronic access
algorithmic trading system governance
```

不适用：

```text
离线回测
没有下单权限的模拟分析
纯 RAG 问答
```

边界：

```text
不得输出信用额度、保证金比例、订单规模阈值。
不得声明项目已经满足某监管要求。
不得把美国 SEC/FINRA 规则泛化到 EU、crypto 或期货市场。
```

### GAP-TR-03 Time Synchronization Audit

目标 statement：

```text
交易事件、行情事件、订单状态、成交、风控动作、RAG 审计和模型推理日志必须声明 clock source、sync status、timestamp precision、timezone、drift policy 和 time-ordering caveat；没有可信时间同步证据时，不得声称事件先后顺序可用于执行质量或合规审计结论。
```

适用范围：

```text
market data ingestion
order/fill audit
replay/simulation gap report
live execution reconciliation
risk gate audit trace
model inference trace
RAG/MCP audit trace
```

不适用：

```text
不要求事件先后证明的静态知识文档
人工备注的非证据时间
```

边界：

```text
不得作为高频策略建议。
不得给出具体硬件采购建议。
不得把 clock sync 状态直接等同于交易许可。
```

## 跨分支 owner 边界

| 主题 | Owner | 只能引用的分支 |
| --- | --- | --- |
| LLM/Agent 安全 | AI Engineering | MCP、RAG、Memory、Final Gate、Project Integration |
| AI SBOM | AI Engineering + Database/Storage | Model Registry、Dataset Registry、Artifact Store |
| 市场行为监控 | Trading Engineering / Trade Analysis / Live Execution | Order Semantics、Audit Trail、Market Microstructure |
| Market Access | Trading Engineering / Live Execution / Risk Management | Broker/Venue Adapter、Risk Gate、Execution Log |
| 时间同步 | Trading Engineering / Data Engineering / Live Execution / Audit Trace | Market Data、Replay、Live Execution、MCP Audit |

## 不做什么

```text
1. 不创建新数据库。
2. 不修改 MCP tool 权限。
3. 不修改 Vue3 信息架构。
4. 不直接生成候选之外的正式知识。
5. 不升级 approved。
6. 不新增默认指导。
7. 不输出任何实盘执行建议。
```

## 审计要求

外部审计必须执行：

```text
1. 搜索相关专业网站、官方资料、案例和数据。
2. 区分官方监管/标准来源与 vendor/博客来源。
3. 检查来源是否直接支撑 statement。
4. 检查 jurisdiction、venue、asset class、system scope。
5. 检查是否有法律意见、交易建议、阈值建议越界。
6. 输出 decision、confidence、patch_notes、required_followups。
```
