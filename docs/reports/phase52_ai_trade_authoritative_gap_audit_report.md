# Phase 52 AI/Trading Engineering 权威资料缺口复审报告

审计时间：2026-06-13

## 结论

当前 AI Engineering 与 Trading Engineering 两条主线已经具备可支撑外接交易 AI 项目的主体知识框架：AI 侧覆盖数值 scorer、校准、Qwen/LLM 审计助手、RAG/MCP、持续学习、模型发布、数据库、记忆层；Trade 侧覆盖数据工程、策略工程、回测、Replay/Simulation、Live Execution、Risk Management、Trade Analysis、TCA、订单语义、市场数据授权、系统韧性和 crypto perpetual 风险。

本次对照权威资料后，没有发现需要推翻现有知识树的大缺口。但建议新增一组 P0/P1 补充知识，重点不是“更多交易技巧”，而是补强外接项目真正上线前最容易出事故的治理边界：

```text
1. AI/LLM/Agent 安全与供应链：OWASP、MITRE ATLAS、NIST AI RMF、AI SBOM。
2. 交易监管与市场行为监控：Reg NMS / Market Access / DEA / Market Abuse / Spoofing / Layering。
3. 生产运行可观测与时钟一致性：OpenTelemetry、SLO、PTP/NTP、订单事件时间序。
4. 跨市场适用边界：美国证券、期货、欧盟 MiFID II、crypto venue 不能互相泛化。
```

这些建议都应先进入候选和 reviewed/caveat_only，不应直接进入 approved、default guidance 或 hard gate。

## 本地覆盖扫描

基于 `codex-expert-kit/rag/indexes/knowledge_items.json` 的关键词弱扫描：

| 主题 | 命中情况 | 判断 |
| --- | ---: | --- |
| market data entitlement / redistribution | 11 / 3 | 已覆盖，但可继续强化 license 与 redistribution 边界 |
| best execution | 3 | 已覆盖 TCA 和 routing context，够用 |
| Reg NMS | 0 | 建议补充，尤其是美国股票 best execution / order protection 边界 |
| spoofing / layering / market abuse | 0 / 0 / 0 | 建议补充，当前只有 self-trade prevention 相关弱覆盖 |
| SBOM / AI SBOM | 0 | 建议补充，外接 AI 项目部署依赖和模型供应链需要 |
| OWASP / prompt injection | 52 / 51 | 已有较强覆盖，但应做交易 AI 专用映射 |
| SLO / latency / incident | 4 / 多 | 已覆盖运行时延迟与事故，但 AI inference 可观测还可补细 |
| PTP / NTP / clock sync | 0 / 1 / 32 | 建议补充高频/交易事件审计的精确时间边界 |
| stress / Expected Shortfall | 18 / 1 | 压力测试已覆盖，但 ES/尾部风险可按组合风险扩展 |

说明：关键词命中不是最终证据，只用于发现潜在弱点。

## 权威资料对照

### AI Engineering

| 权威资料 | 关键启发 | 当前覆盖判断 | 建议 |
| --- | --- | --- | --- |
| NIST AI RMF 与 Generative AI Profile | AI 风险应贯穿设计、开发、使用、评估和治理，GenAI 有独特风险 | 已覆盖治理、评估、上线、回滚，但需要更明确映射到外接交易 AI 的 risk register | P1 增强 |
| OWASP Top 10 for LLM Applications | 包含 Prompt Injection、Training Data Poisoning、Supply Chain Vulnerabilities、Excessive Agency、Overreliance 等 | 已覆盖 prompt injection、只读 MCP、LLM 不执行交易，但缺少交易 AI agent 专用 threat model | P0 补充 |
| MITRE ATLAS | AI 对抗战术和技术知识库，强调真实攻击观察 | 当前有安全治理，但没有系统化 adversarial scenario taxonomy | P1 补充 |
| CISA SBOM / AI SBOM | SBOM 是软件供应链安全基础，AI SBOM 进一步覆盖模型、数据、组件和依赖透明性 | 当前 SBOM 命中为 0，模型/数据 lineage 已有但供应链清单不足 | P0 补充 |
| Model Cards / Dataset Cards | 模型和数据应声明用途、限制、评估条件和适用边界 | 已覆盖 dataset card/model card，保持即可 | 不急 |
| MLflow Model Registry / Dataset Tracking / OpenLineage | 支撑模型版本、数据血缘、训练/验证/生产追踪 | Phase 40/41/42 已覆盖较好 | 不急 |
| OpenTelemetry Observability | 生产系统应有 logs、metrics、traces 以定位未知问题 | 运行时延迟已有，但 AI inference、RAG、tool call 的 trace 预算可补 | P1 补充 |

### Trading Engineering

| 权威资料 | 关键启发 | 当前覆盖判断 | 建议 |
| --- | --- | --- | --- |
| SEC Rule 15c3-5 Market Access | 直接市场接入需要金融、监管和其他风险控制；裸接入风险明确 | Phase 37/45 已有 pre-trade risk controls，但美国证券 market access 监管语义可补强 | P0 补充 |
| FINRA Manipulative Trading | 明确 manipulative trading 相关规则，覆盖不当交易行为 | 当前 spoofing/layering/market abuse 命中弱 | P0 补充 |
| CFTC Disruptive Trading Practices | Spoofing 等破坏性交易行为需要意图和市场行为边界 | 当前没有系统 taxonomy | P1 补充 |
| ESMA MiFID II Article 17 | 算法交易系统需要容量、韧性、阈值、错误订单防控、记录保存和 DEA 控制 | 当前已有韧性和风险控制，但 EU/DEA 语义未单独成知识 | P1 补充 |
| FIXatdl / FIX Trading | 算法订单参数、配置和身份应机器可读、可审计 | Phase 45 已补订单语义和 algo execution，保持即可 | 不急 |
| FIA Automated Trading Risk Controls | 自动化交易应有本地化 pre-trade controls、实时监控和后交易报告 | Phase 45 已覆盖，保持即可 | 不急 |
| CFA Trade Strategy and Execution | 执行质量、交易成本、TCA 和 benchmark 不能简化为单指标 | Phase 45/Trade Analysis 已覆盖，保持即可 | 不急 |

## 建议新增或强化的知识点

### P0：建议下一阶段优先补

| 建议 ID | 分支 | 建议知识点 | 理由 | 边界 |
| --- | --- | --- | --- | --- |
| GAP-AI-01 | AI Engineering / Security Governance | Trading AI Agent Threat Model 必须覆盖 prompt injection、tool misuse、memory poisoning、excessive agency、overreliance | OWASP 与 MITRE ATLAS 均支持把 LLM/Agent 安全作为独立治理面 | 不给交易信号，不启用 hard gate |
| GAP-AI-02 | AI Engineering / Supply Chain Governance | AI SBOM / Model SBOM 必须记录模型、权重、adapter、数据集、依赖、容器、推理服务和许可证 | CISA AI SBOM 与 OWASP supply chain 风险直接支持 | 不要求固定工具，只定义清单契约 |
| GAP-TR-01 | Trading Engineering / Market Conduct Surveillance | 交易系统必须区分合法流动性行为与 spoofing、layering、wash/self-trade、momentum ignition 等市场操纵风险 | FINRA/CFTC 明确市场操纵和破坏性交易实践 | 只做审计/监控 taxonomy，不生成法律结论 |
| GAP-TR-02 | Trading Engineering / Market Access Regulatory Boundary | Market Access / DEA / sponsored access 需要金融、监管、信用和错误订单控制证据 | SEC Rule 15c3-5 与 ESMA Article 17 都强调接入控制 | 不输出合规意见或阈值 |
| GAP-TR-03 | Trading Engineering / Time Synchronization | 订单、行情、成交、风控和审计日志必须声明 clock source、sync status、timestamp precision 和 drift policy | 现有 PTP/NTP 命中弱，高频/回放/审计都依赖时间序 | 不等于高频策略建议 |

### P1：可排期补充

| 建议 ID | 分支 | 建议知识点 | 理由 | 边界 |
| --- | --- | --- | --- | --- |
| GAP-AI-03 | AI Engineering / Observability | AI inference、RAG retrieval、tool call、final gate 需要 trace/span、latency budget、error taxonomy 和 sampling policy | OpenTelemetry 支持 logs/metrics/traces 的统一可观测模型 | 不绑定单一厂商 |
| GAP-AI-04 | AI Engineering / Adversarial Evaluation | 外接 AI 项目应有红队样例、prompt injection 回归集、工具越权测试和记忆污染测试 | OWASP/MITRE ATLAS 支持对抗测试 | 不能替代人工安全审核 |
| GAP-TR-04 | Trading Engineering / Cross-Jurisdiction Boundary | US SEC/FINRA、CFTC、EU MiFID II、crypto venue 的规则不能互相泛化 | 多监管来源语义差异明显 | 不给法律意见 |
| GAP-TR-05 | Trading Engineering / Portfolio Tail Risk | 组合风险除普通 loss limit 外，应补 VaR/ES、流动性压力、相关性断裂和集中度场景 | 当前 Expected Shortfall 命中弱 | 不输出风控阈值 |
| GAP-TR-06 | Trading Engineering / Market Data Licensing | Market data license、derived data、redistribution、delayed/realtime entitlement 需要更细证据链 | 当前 entitlement 有覆盖，但 redistribution 较弱 | 不解释具体商业合同 |

## 不建议现在新增的主题

| 主题 | 原因 |
| --- | --- |
| 具体策略信号百科 | 与 CEK-TA 支持层定位不符，容易污染交易建议边界 |
| 单一经纪商实盘教程 | 会变成项目私有接入知识，应该放外接项目 adapter |
| 具体仓位/风控数值模板 | 会越过 reviewed/caveat_only，进入风险阈值建议 |
| 法律合规结论 | CEK-TA 可沉淀监管边界和证据契约，但不能代替律师或合规负责人 |
| 某个观测平台的完整接入方案 | 应定义 OpenTelemetry/trace 契约，不绑定单一 vendor |

## 后续 Phase 建议

建议开一个新 Phase，而不是把这些缺口塞进 Phase 37/45：

```text
Phase 53: AI/Trading Security, Market Conduct and Runtime Governance Knowledge Extension
```

建议任务顺序：

```text
1. 定义新增知识范围和 L3 节点：AI Agent Security、AI SBOM、Market Conduct Surveillance、Market Access Boundary、Time Sync Audit。
2. 创建 ResearchIngestionTask 队列和权威来源种子库。
3. 先采集 5 条 P0 候选：GAP-AI-01、GAP-AI-02、GAP-TR-01、GAP-TR-02、GAP-TR-03。
4. 导出 AI 审计包，要求审计方必须搜索权威资料、官方文档、案例和边界。
5. 通过后只允许进入 reviewed/caveat_only，禁止 approved/default/hard gate。
6. 重建索引并跑 MCP/SearchLab/KnowledgeTree 回归验证。
```

## 来源

AI 与安全：

```text
NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/
MITRE ATLAS: https://atlas.mitre.org/
CISA SBOM: https://www.cisa.gov/topics/information-communications-technology-supply-chain-security/sbom
CISA AI SBOM minimum elements: https://www.cisa.gov/resources-tools/resources/software-bill-materials-ai-minimum-elements
Google Model Cards: https://research.google/pubs/model-cards-for-model-reporting/
MLflow Model Registry: https://mlflow.org/docs/latest/ml/model-registry/
MLflow Dataset Tracking: https://mlflow.org/docs/latest/ml/dataset/
OpenLineage Object Model: https://openlineage.io/docs/spec/object-model/
OpenTelemetry Observability Primer: https://opentelemetry.io/docs/concepts/observability-primer/
```

Trading 与监管：

```text
SEC Rule 15c3-5 Market Access: https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm
FINRA Manipulative Trading: https://www.finra.org/rules-guidance/guidance/reports/2025-finra-annual-regulatory-oversight-report/manipulative-trading
CFTC Disruptive Trading Practices: https://www.cftc.gov/LawRegulation/DoddFrankAct/Rulemakings/DF_24_DisruptiveTrading/index.htm
ESMA MiFID II Article 17 Algorithmic Trading: https://www.esma.europa.eu/publications-and-data/interactive-single-rulebook/mifid-ii/article-17-algorithmic-trading
FIXatdl: https://fixtrading.org/standards/fix-algorithmic-trading-definition-language/
FIA Automated Trading Risk Controls: https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf
```

## DoD 验收

```text
1. Phase 52 任务卡已创建。
2. docs/index_tasks.md 与 docs/tasks/README.md 已更新。
3. 已进行本地关键词覆盖扫描。
4. 已联网检索权威资料并给出来源链接。
5. 已输出 P0/P1 建议补充知识点。
6. 未直接修改正式知识状态。
7. 未输出交易执行建议、阈值建议或合规结论。
8. UTF-8 与乱码检查通过。
```
