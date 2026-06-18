# Phase 53 ResearchIngestionTask 队列

创建日期：2026-06-13

## 队列原则

```text
1. 先 P0，后 P1。
2. 每条候选必须至少包含 2 个 A1/A2 来源。
3. 必须显式写出 jurisdiction、asset class、system scope、owner boundary。
4. 所有候选默认只能进入 accepted_for_draft 或 reviewed/caveat_only 准备，不得直接 approved/default/hard gate。
5. 审计包必须要求外部 AI/人工继续搜索专业资料、官方文档、案例和数据。
```

## P0 队列

| research_task_id | priority | target_node | candidate_slug | 任务目标 | 必备来源 | 初始状态 |
| --- | --- | --- | --- | --- | --- | --- |
| P53-AI-SEC01 | P0 | `kt.ai_engineering.security_governance.agent_threat_model` | `trading_ai_agent_threat_model_required` | 定义交易 AI Agent 必须覆盖的 prompt injection、tool misuse、memory poisoning、excessive agency、overreliance、sensitive information disclosure 风险 | NIST AI RMF、OWASP、MITRE ATLAS | ready_for_collection |
| P53-AI-SBOM01 | P0 | `kt.ai_engineering.supply_chain_governance.ai_sbom` | `ai_sbom_model_sbom_required` | 定义外接交易 AI 项目的模型、adapter、数据集、依赖、容器、推理服务和许可证清单 | CISA SBOM、CISA AI SBOM、OWASP supply chain | ready_for_collection |
| P53-TR-MC01 | P0 | `kt.trading_engineering.market_conduct.surveillance_taxonomy` | `market_conduct_surveillance_taxonomy_required` | 定义 spoofing、layering、wash/self-trade、momentum ignition、marking the close 等市场行为监控 taxonomy | FINRA Manipulative Trading、CFTC Disruptive Trading Practices | ready_for_collection |
| P53-TR-MA01 | P0 | `kt.trading_engineering.market_access.regulatory_boundary` | `market_access_dea_regulatory_boundary_required` | 定义 Market Access、DEA、sponsored access、pre-trade controls、recordkeeping 和 jurisdiction boundary | SEC Rule 15c3-5、SEC FAQ、ESMA MiFID II Article 17 | ready_for_collection |
| P53-TR-TS01 | P0 | `kt.trading_engineering.audit_trace.time_synchronization` | `trade_audit_time_synchronization_required` | 定义交易事件、行情、成交、风控、模型推理和 RAG/MCP 审计日志的 clock source、sync status、timestamp precision、drift policy | FINRA Rule 6820、CAT Clock Sync、EU RTS 25、OpenTelemetry | ready_for_collection |

## P1 候选池

| research_task_id | priority | target_node | 任务目标 | 依赖 |
| --- | --- | --- | --- | --- |
| P53-AI-SEC02 | P1 | `kt.ai_engineering.security_governance.adversarial_eval` | 定义交易 AI 的 prompt injection 回归集、工具越权测试、记忆污染测试和红队样例 | P53-AI-SEC01 |
| P53-AI-OBS01 | P1 | `kt.ai_engineering.runtime_observability.inference_trace` | 定义 AI inference、RAG retrieval、tool call、final gate 的 trace/span、latency budget、error taxonomy | P53-AI-SEC01 |
| P53-TR-MC02 | P1 | `kt.trading_engineering.market_conduct.alert_review_workflow` | 定义市场行为异常 alert 的人工复核、误报、证据包和升级流程 | P53-TR-MC01 |
| P53-TR-MA02 | P1 | `kt.trading_engineering.market_access.cross_jurisdiction_boundary` | 定义 SEC/FINRA、CFTC、ESMA/MiFID II、crypto venue 的跨监管适用边界 | P53-TR-MA01 |
| P53-TR-RISK01 | P1 | `kt.trading_engineering.portfolio_risk.tail_risk_scenario` | 强化 VaR/ES、流动性压力、相关性断裂和集中度风险知识 | Phase 45 Stress |

## 每条候选必须回答的问题

```text
1. 该知识属于 AI Engineering 还是 Trading Engineering？
2. 它的 owner 是谁？
3. 它支撑的是审计、解释、监控、合规边界，还是运行时执行？
4. 哪些来源直接支撑 statement？
5. 哪些来源只能做 supporting source？
6. 适用于哪些 jurisdiction、asset class、venue、system scope？
7. 不适用于哪些场景？
8. 是否可能被误读为交易建议、法律意见或 hard gate？
9. 是否需要内部 CEK-TA contract 才能进入 reviewed？
10. MCP/SearchLab/Vue3 应如何展示和阻断？
```

## 审计输出要求

外部审计结果必须包含：

```text
candidate_id
research_task_id
decision
confidence
reviewed_allowed
approved_allowed
default_guidance_allowed
hard_gate_allowed
reasons
required_followups
patch_notes.source
patch_notes.content
patch_notes.boundary
patch_notes.conflict
```
