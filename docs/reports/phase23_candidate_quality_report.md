# Phase 23 候选知识质量报告

本报告记录 Phase 23 全网专业知识采集候选包的来源质量、冲突审计、审计问题和后续处理建议。

## 报告状态

```text
phase: Phase 23
task_scope: CEK-TA-100 / CEK-TA-101
created_at: 2026-06-08
updated_at: 2026-06-08
status: in_progress
```

## 当前候选总览

| Candidate | Research Task | Partition | Status | Source Reliability | Conflict Status | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| `cand_20260608_backtest_bias_leakage_overfit_001` | `CEK-TA-RESEARCH-20260608-023-001` | `KB_04_BACKTEST` | `conflict_checked` | high / 89 | resolved | convert_to_knowledge_item |
| `cand_20260608_replay_simulation_ohlc_same_bar_fill_001` | `CEK-TA-RESEARCH-20260608-023-002` | `KB_05_REPLAY_SIMULATION` | `conflict_checked` | high / 84 | none | convert_to_knowledge_item |
| `cand_20260608_live_execution_order_state_reconciliation_001` | `CEK-TA-RESEARCH-20260608-023-003` | `KB_06_LIVE_EXECUTION` | `conflict_checked` | high / 91 | resolved | convert_to_knowledge_item |
| `cand_20260608_risk_management_pre_trade_risk_gates_001` | `CEK-TA-RESEARCH-20260608-023-004` | `KB_07_RISK_MANAGEMENT` | `conflict_checked` | high / 91 | resolved | convert_to_knowledge_item |
| `cand_20260608_rag_engineering_metadata_citation_freshness_policy_001` | `CEK-TA-RESEARCH-20260608-023-005` | `KB_10_RAG_ENGINEERING` | `conflict_checked` | high / 87 | resolved | convert_to_knowledge_item |
| `cand_20260608_mcp_engineering_tool_contract_readonly_errors_observability_001` | `CEK-TA-RESEARCH-20260608-023-006` | `KB_11_MCP_ENGINEERING` | `conflict_checked` | high / 90 | resolved | convert_to_knowledge_item |
| `cand_20260608_knowledge_governance_lifecycle_evidence_conflict_deprecation_001` | `CEK-TA-RESEARCH-20260608-023-007` | `KB_13_KNOWLEDGE_GOVERNANCE` | `conflict_checked` | high / 89 | resolved | convert_to_knowledge_item |

## 候选 001: 回测偏差、数据泄漏和过拟合审计门

### 目标

```text
补强 KB_04_BACKTEST / backtest.bias 知识：把数据泄漏、前视信息、测试集调参、多重试验选择拆成独立审计门。
```

### 来源记录

| Source | Type | Reliability | Score | Use |
| --- | --- | --- | ---: | --- |
| NBER: Backtesting Strategies Based on Multiple Signals | paper | high | 91 | 支撑多信号、多参数选择导致的过拟合和多重测试审计 |
| The Probability of Backtest Overfitting | paper | high | 88 | 支撑 PBO/样本内最佳模型与样本外表现差异审计 |
| scikit-learn Common pitfalls: Data leakage | official_doc | high | 89 | 支撑数据泄漏、预处理泄漏、fit/fit_transform 边界 |
| scikit-learn Cross-validation | official_doc | high | 84 | 支撑测试集调参导致评估指标不再代表泛化表现 |

### 来源结论

```text
overall_reliability: high
score: 89
primary_source_count: 4
supporting_source_count: 0
low_reliability_source_count: 0
mandatory_downgrades: none
```

### 冲突审计

已检查：

```text
kb_04_backtest.bias.multiple_testing_overfit.v1
```

结论：

```text
conflict_status: resolved
severity: informational
approval_allowed: true
```

说明：

```text
现有 approved 知识覆盖多重测试和过拟合默认审计；本候选补充数据泄漏、预处理泄漏、测试集调参和分层审计清单。两者不存在直接冲突，但正式 draft 需要关联 existing item，避免重复表述。
```

### 人工审计问题

```text
1. 是否把本候选拆成两条正式知识：data leakage 与 test-set tuning / multiple testing checklist？
2. 是否需要补充金融时间序列专用来源，例如 purged/embargoed cross-validation 的原始出处或框架文档？
3. 正式 draft 是否应引用并关联 kb_04_backtest.bias.multiple_testing_overfit.v1？
```

### 建议

```text
当前候选可以进入 needs_review。人工审计通过后，建议转换为正式知识 draft:
kb_04_backtest.bias.leakage_overfit_audit_gates.v1
```

## 候选 002: OHLC 同根 TP/SL 与 fill model 歧义

### 目标

```text
建立 KB_05_REPLAY_SIMULATION / replay_simulation.fill_model 知识：当只有 OHLC bar 数据时，同根 TP/SL 或 stop/limit 多订单触发顺序不可从 bar 本身恢复，必须披露 fill 假设或使用更低粒度回放。
```

### 来源记录

| Source | Type | Reliability | Score | Use |
| --- | --- | --- | ---: | --- |
| LEAN FillModel Class Reference | framework_doc | high | 91 | 支撑 OHLC 下 limit/stop 和 H-L 顺序不可完全确定，需要成交假设 |
| Backtrader Orders - Creation/Execution | framework_doc | medium | 80 | 支撑 bar 级 limit/stop 执行逻辑和 OHLC 部分推断边界 |
| backtesting.py API documentation | framework_doc | medium | 79 | 支撑 market/条件单的 bar 执行时点审计 |
| backtesting.py GitHub discussion #242 | code_doc | medium | 76 | 支撑同根 SL/TP intrabar 顺序不可断言、保守/延迟处理边界 |

### 来源结论

```text
overall_reliability: high
score: 84
primary_source_count: 4
supporting_source_count: 0
low_reliability_source_count: 0
mandatory_downgrades: none
```

### 冲突审计

```text
conflict_status: none
approval_allowed: true
```

说明：

```text
未发现现有正式知识中有同主题 approved 规则。本候选不规定所有框架必须采用相同 TP/SL 先后顺序，而是要求披露 fill policy、数据粒度和成交假设，因此不会与框架默认行为差异冲突。
```

### 人工审计问题

```text
1. CEK-TA 是否需要指定默认保守策略：同根 TP/SL 歧义时优先止损，还是只要求披露项目 fill policy？
2. 是否需要补充 TradingView、Zipline、vectorbt 等更多框架来源来覆盖不同默认行为？
3. 正式 draft 是否拆成原则知识和 eval_case 两个资产？
```

### 建议

```text
当前候选可以进入 needs_review。人工审计通过后，建议转换为正式知识 draft:
kb_05_replay_simulation.fill_model.ohlc_same_bar_tp_sl_ambiguity.v1
```

## 候选 003: 实盘订单状态机与仓位同步闭环

### 目标

```text
建立 KB_06_LIVE_EXECUTION / live_trading.order_state_machine 知识：实盘系统不能只依赖下单响应，必须用订单事件流、REST 查询、累计成交字段、账户/仓位事件、仓位快照和撤单/急停机制构成闭环。
```

### 来源记录

| Source | Type | Reliability | Score | Use |
| --- | --- | --- | ---: | --- |
| Binance Query Order | official_doc | high | 91 | 支撑订单状态 REST 复核和状态字段 |
| Binance Event: Order Update | official_doc | high | 94 | 支撑 ORDER_TRADE_UPDATE、状态枚举、执行类型、累计成交字段 |
| Binance Event: Balance and Position Update | official_doc | high | 92 | 支撑 ACCOUNT_UPDATE、仓位/余额变化事件和未成交/撤单边界 |
| Binance Position Information V3 | official_doc | high | 90 | 支撑当前仓位快照和事件流配合使用 |
| Binance Cancel All Open Orders | official_doc | high | 86 | 支撑保护流程中的批量撤单动作 |
| Binance Auto-Cancel All Open Orders | official_doc | high | 88 | 支撑心跳式倒计时撤单和断线保护思路 |

### 来源结论

```text
overall_reliability: high
score: 91
primary_source_count: 6
supporting_source_count: 0
low_reliability_source_count: 0
mandatory_downgrades: none
```

### 冲突审计

已检查：

```text
kb_06_live_execution.risk_control.kill_switch_no_new_orders.v1
```

结论：

```text
conflict_status: resolved
severity: informational
approval_allowed: true
```

说明：

```text
现有 kill switch 知识定义保护状态下禁止新开仓；本候选定义订单状态机和仓位同步如何发现异常并触发保护流程。两者是上下游互补，不是直接冲突。
```

### 人工审计问题

```text
1. 正式 draft 是否将 Binance USDⓈ-M Futures 作为具体适用边界，另建 general adapter 抽象？
2. 是否需要补充 Coinbase、OKX 或 Interactive Brokers 文档来形成跨交易所通用版本？
3. 未知订单状态时 CEK-TA 默认是否应触发 kill switch，还是只标记为 incident_response 候选？
```

### 建议

```text
当前候选可以进入 needs_review。人工审计通过后，建议转换为正式知识 draft:
kb_06_live_execution.order_state_machine.event_rest_position_reconciliation.v1
```

## 候选 004: 预交易风险闸门

### 目标

```text
建立 KB_07_RISK_MANAGEMENT / risk_management.risk_gate 知识：自动化交易系统必须在订单进入执行适配器或交易所前执行风险闸门检查，覆盖风险限额、财务暴露、订单大小、权限、异常订单、连接状态和保护动作。
```

### 来源记录

| Source | Type | Reliability | Score | Use |
| --- | --- | --- | ---: | --- |
| SEC Rule 15c3-5 Market Access Risk Controls | official_doc | high | 94 | 支撑财务暴露、信用/资本阈值、异常订单和市场接入风险控制 |
| CFTC Automated Trading Risk Controls Concept Release | official_doc | high | 92 | 支撑预交易风控、交易后报告、系统保障和自动化交易安全 |
| CME Group Pre-Trade Risk Management | official_doc | high | 90 | 支撑限额、订单、权限、dashboard、报告和审计轨迹 |
| CME Group Risk Management Tools Manual | official_doc | high | 88 | 支撑 Kill Switch、权限层级、阻断新订单和取消工作订单 |

### 来源结论

```text
overall_reliability: high
score: 91
primary_source_count: 4
supporting_source_count: 0
low_reliability_source_count: 0
mandatory_downgrades: none
```

### 冲突审计

已检查：

```text
kb_01_quant_foundation.risk_return.position_risk_budget_before_signal.v1
kb_06_live_execution.risk_control.kill_switch_no_new_orders.v1
cand_20260608_live_execution_order_state_reconciliation_001
```

结论：

```text
conflict_status: resolved
severity: informational
approval_allowed: true
```

说明：

```text
候选与现有仓位预算、kill switch 和订单状态机候选均为互补关系。建议正式 draft 明确执行链路顺序：risk budget -> pre-trade risk gate -> order state machine -> kill switch / incident response。
```

### 人工审计问题

```text
1. 正式 draft 是否拆成 risk_gate、exposure_control、daily_loss_limit 三个知识资产？
2. 是否需要补充 crypto 交易所自身的 pre-trade risk 或账户限额文档？
3. CEK-TA 是否要规定统一的风险链路顺序：risk budget -> risk gate -> order state machine -> kill switch？
```

### 建议

```text
当前候选可以进入 needs_review。人工审计通过后，建议转换为正式知识 draft:
kb_07_risk_management.risk_gate.pre_trade_order_risk_controls.v1
```

## 候选 005: RAG metadata、citation、freshness 与冲突阻断策略

### 目标

```text
建立 KB_10_RAG_ENGINEERING / rag_engineering.retrieval_policy 知识：专业 RAG 默认检索必须返回 metadata、source_refs/citation、review_status、conflict_status、freshness、适用边界和推荐动作，并阻断无来源、draft/rejected、过期、冲突未消解或项目不匹配结果。
```

### 来源记录

| Source | Type | Reliability | Score | Use |
| --- | --- | --- | ---: | --- |
| OpenAI File Search | official_doc | high | 93 | 支撑 file citations、include search results、metadata filtering |
| OpenAI Retrieval | official_doc | high | 92 | 支撑 vector stores、attributes、semantic search 和 filtering |
| Qdrant Documentation | framework_doc | high | 88 | 支撑 payload metadata、filtering、hybrid search、reranking |
| LangChain Retrieval | framework_doc | medium | 80 | 支撑 retrieval/RAG 基本架构和知识库检索 |
| LlamaIndex Citation Query Engine | framework_doc | medium | 78 | 支撑 citation source nodes |
| Ragas Available Metrics | framework_doc | medium | 81 | 支撑 context precision、context recall、faithfulness 等 RAG 评测指标 |
| CEK-TA Search Result Contract | internal_report | medium | 86 | 支撑 CEK-TA source_refs、conflict_status、freshness、recommended_next_action 和阻断规则 |

### 来源结论

```text
overall_reliability: high
score: 87
primary_source_count: 6
supporting_source_count: 1
low_reliability_source_count: 0
mandatory_downgrades: none
```

### 冲突审计

已检查：

```text
kb_09_rag_engineering.source_quality.unsourced_default_block.v1
kb_08_llm_training.eval_and_risk.source_boundary_human_escalation.v1
```

结论：

```text
conflict_status: resolved
severity: informational
approval_allowed: true
```

说明：

```text
现有无来源阻断知识是单项 gate；本候选是完整检索结果契约和阻断策略。现有 LLM source boundary 知识定义回答层的人类升级/刷新来源边界；本候选定义检索层需要提供的字段。三者为上下游互补。
```

### 人工审计问题

```text
1. 正式 draft 是否拆成 metadata/citation policy、conflict-aware retrieval、freshness policy 三条知识？
2. CEK-TA 是否需要把 OpenAI File Search 作为一种实现来源，而不是默认依赖？
3. 是否要补充一个 eval_case，验证无来源、draft、rejected、confirmed conflict、deprecated 均被阻断？
```

### 建议

```text
当前候选可以进入 needs_review。人工审计通过后，建议转换为正式知识 draft:
kb_10_rag_engineering.retrieval_policy.metadata_citation_freshness_conflict_gate.v1
```

## 候选 006: MCP tool contract、只读权限、错误结构和观测性

### 目标

```text
建立 KB_11_MCP_ENGINEERING / mcp_engineering.tool_contract 知识：Knowledge MCP 工具必须声明 name、purpose、input_schema、output_schema、error_schema、permission boundary、rate/size limits、audit fields 和测试用例；CEK-TA 默认 MCP 工具必须只读。
```

### 来源记录

| Source | Type | Reliability | Score | Use |
| --- | --- | --- | ---: | --- |
| MCP Specification | official_doc | high | 94 | 支撑 MCP 协议、server/client、tools/resources/prompts 基础能力 |
| MCP Tools Concept | official_doc | high | 93 | 支撑 tool name、description、inputSchema 作为工具契约核心 |
| MCP Basic Protocol | official_doc | high | 90 | 支撑 JSON-RPC 请求/响应/通知和标准错误响应 |
| MCP Security Best Practices | official_doc | high | 95 | 支撑用户同意、权限控制、输入验证、避免 token passthrough/confused deputy |
| MCP Python SDK | framework_doc | medium | 82 | 支撑 MCP server/tool 实现和测试映射 |
| CEK-TA MCP Server Spec | internal_report | medium | 88 | 支撑 CEK-TA read-only、source/conflict/freshness 输出和禁止交易/密钥/写入 |

### 来源结论

```text
overall_reliability: high
score: 90
primary_source_count: 5
supporting_source_count: 1
low_reliability_source_count: 0
mandatory_downgrades: none
```

### 冲突审计

已检查：

```text
cand_20260608_rag_engineering_metadata_citation_freshness_policy_001
kb_09_rag_engineering.source_quality.unsourced_default_block.v1
kb_10_project_runbooks.path_resolver.portable_paths.v1
```

结论：

```text
conflict_status: resolved
severity: informational
approval_allowed: true
```

说明：

```text
候选与 RAG 检索候选、无来源阻断知识和 path resolver 知识均为互补关系。建议正式 draft 明确层级：runtime config/path resolver -> MCP tool contract -> RAG retrieval result contract -> LLM answer boundary。
```

### 人工审计问题

```text
1. 正式 draft 是否拆成 tool_contract、permission_boundary、error_schema、observability 四条知识资产？
2. CEK-TA 是否需要补一个 MCP tool contract JSON schema 模板，供后续工具新增时强制使用？
3. 是否要把 MCP 官方 spec 版本写入 MCP runtime healthcheck 输出？
```

### 建议

```text
当前候选可以进入 needs_review。人工审计通过后，建议转换为正式知识 draft:
kb_11_mcp_engineering.tool_contract.readonly_errors_observability.v1
```

## 候选 007: 知识状态生命周期、证据门槛、冲突阻断和废弃策略

### 目标

```text
建立 KB_13_KNOWLEDGE_GOVERNANCE / knowledge_governance.status_lifecycle 知识：CEK-TA 知识必须按状态生命周期治理，进入默认指导前必须满足来源证据、适用边界、冲突状态、freshness、审计日志和可回滚记录。
```

### 来源记录

| Source | Type | Reliability | Score | Use |
| --- | --- | --- | ---: | --- |
| NIST AI RMF | official_doc | high | 94 | 支撑 AI 系统风险治理、可信性、设计/开发/使用/评估生命周期 |
| NIST AI RMF Core | official_doc | high | 95 | 支撑 Govern/Map/Measure/Manage、全生命周期、文档化、透明度、问责 |
| OWASP AISVS | official_doc | high | 88 | 支撑 AI 应用数据、训练、部署、监控、退役的安全验证生命周期 |
| OWASP LLMSVS | official_doc | high | 86 | 支撑 LLM 应用架构、生命周期、训练、运行、集成、存储和监控安全 |
| CEK-TA Knowledge Item Schema | internal_report | medium | 88 | 支撑 CEK-TA draft/reviewed/approved/deprecated/rejected 状态流和 approval gate |
| CEK-TA Source Quality Rules | internal_report | medium | 87 | 支撑来源可靠性、评分维度、强制降级和 approved 来源要求 |
| CEK-TA Conflict Detection Rules | internal_report | medium | 89 | 支撑冲突类型、阻断条件、消解顺序和输出契约 |

### 来源结论

```text
overall_reliability: high
score: 89
primary_source_count: 4
supporting_source_count: 3
low_reliability_source_count: 0
mandatory_downgrades: none
```

### 冲突审计

已检查：

```text
kb_09_rag_engineering.source_quality.unsourced_default_block.v1
cand_20260608_rag_engineering_metadata_citation_freshness_policy_001
cand_20260608_mcp_engineering_tool_contract_readonly_errors_observability_001
```

结论：

```text
conflict_status: resolved
severity: informational
approval_allowed: true
```

说明：

```text
候选是 KB_13 治理父规则，与现有无来源阻断、RAG 检索候选和 MCP 工具候选是上下游关系。正式 draft 应作为状态生命周期和默认指导 gate 的总规则。
```

### 人工审计问题

```text
1. 正式 draft 是否要同步更新 knowledge_item_schema.md，把 candidate/reviewed/accepted 等候选状态和正式状态更清晰分层？
2. 是否需要把 KB_13 作为所有候选转 draft 的强制评审清单？
3. 是否要在 MCP/SearchLab 增加治理状态过滤的专门回归用例？
```

### 建议

```text
当前候选可以进入 needs_review。人工审计通过后，建议转换为正式知识 draft:
kb_13_knowledge_governance.status_lifecycle.evidence_conflict_deprecation_gate.v1
```

## 本轮不做

```text
1. 不把候选包直接标记 approved。
2. 不把候选包加入 MCP 默认检索。
3. 不生成投资建议或策略收益判断。
4. 不保存来源长段原文。
```

## 后续动作

```text
1. 将 CEK-TA-RESEARCH-20260608-023-001 到 023-007 状态更新为 candidate_ready。
2. 对七个 P0 候选进入人工审计，决定是否转正式知识 draft。
3. 下一步可进入 CEK-TA-102，把 accepted 候选转正式知识 draft 并重建索引；或继续执行 P1：KB_01_QUANT_FOUNDATION。
```
