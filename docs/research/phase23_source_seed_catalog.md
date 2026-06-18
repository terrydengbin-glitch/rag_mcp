# Phase 23 可信来源种子库

本文件记录 Phase 23 初始可信来源种子。种子库不是知识结论，只是后续 ResearchIngestionTask 的来源入口。每次真正生成候选知识时，仍必须重新读取来源、记录 accessed_at、抽取 claim、评分并执行冲突检测。

## 来源分级

```text
P0: 官方文档、交易所规则、标准/协议文档、原始论文、权威数据/框架文档。
P1: 开源框架官方文档、工程白皮书、权威教程。
P2: 书籍、课程、研究报告、专业工程文章。
P3: 博客、论坛、经验帖。只能用于发现问题，不能单独支撑 approved。
```

## 交易工程来源种子

| 适用分区 | 来源 | 类型 | 可靠性 | 用途 | URL |
| --- | --- | --- | --- | --- | --- |
| `KB_04_BACKTEST` | Backtest Overfitting in Financial Markets | paper | high | 回测过拟合、multiple testing、PBO | https://papers.ssrn.com/abstract=2731886 |
| `KB_04_BACKTEST` | Backtesting Strategies Based on Multiple Signals | paper | high | 多信号回测、选择偏差、过拟合风险 | https://www.nber.org/papers/w21329 |
| `KB_04_BACKTEST` | QuantConnect LEAN trade fills docs | framework_doc | high | fill model、slippage、成交假设 | https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts |
| `KB_05_REPLAY_SIMULATION` | QuantConnect reality modeling docs | framework_doc | high | fill、fee、slippage、margin model | https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling |
| `KB_06_LIVE_EXECUTION` | Binance API order status guide | official_doc | medium | 订单状态、REST/WebSocket 监控 | https://academy.binance.com/lt/articles/binance-api-understanding-order-status |
| `KB_06_LIVE_EXECUTION` | Binance official API docs | official_doc | high | 交易所 API、订单、账户、风险字段 | https://developers.binance.com/docs |
| `KB_07_RISK_MANAGEMENT` | Kelly criterion and position sizing literature | paper/book | medium | 仓位理论、公式前提、误用风险 | 待具体任务检索确认 |
| `KB_02_DATA_ENGINEERING` | Exchange API docs and framework data docs | official_doc/framework_doc | high | 数据 schema、时间戳、事件字段、版本 | 待具体交易所/框架任务确认 |
| `KB_03_STRATEGY_ENGINEERING` | Technical analysis and market microstructure literature | book/paper | medium | 指标边界、微观结构、策略解释边界 | 待具体任务检索确认 |

## AI/RAG/MCP 来源种子

| 适用分区 | 来源 | 类型 | 可靠性 | 用途 | URL |
| --- | --- | --- | --- | --- | --- |
| `KB_09_LLM_TRAINING` | Hugging Face Dataset Card docs | official_doc | high | dataset card、数据集说明、license/metadata | https://huggingface.co/docs/datasets/v2.7.1/dataset_card |
| `KB_09_LLM_TRAINING` | OpenAI evaluation best practices | official_doc | high | eval 设计、评测标准、回归评测 | https://platform.openai.com/docs/guides/evaluation-best-practices |
| `KB_10_RAG_ENGINEERING` | OpenAI Knowledge Retrieval blueprint | official_doc | high | cited answers、retrieval、evals | https://openai.com/solutions/blueprints/knowledge-retrieval/ |
| `KB_10_RAG_ENGINEERING` | OpenAI RAG and semantic search help | official_doc | medium | RAG 基本定义、语义检索适用场景 | https://help.openai.com/en/articles/8868588-retrieval-augmented-generation-rag-and-semantic-search-for-gpts |
| `KB_10_RAG_ENGINEERING` | Qdrant hybrid search and reranking docs | framework_doc | high | hybrid search、metadata filtering、rerank | https://qdrant.tech/documentation/advanced-tutorials/reranking-hybrid-search/ |
| `KB_10_RAG_ENGINEERING` | LangChain retrieval docs | framework_doc | medium | retrieval pipeline、document loaders、text splitters | https://docs.langchain.com/oss/python/langchain/retrieval |
| `KB_11_MCP_ENGINEERING` | Model Context Protocol official docs repository | official_doc | high | MCP spec、tools、resources、server contracts | https://github.com/modelcontextprotocol/modelcontextprotocol |
| `KB_11_MCP_ENGINEERING` | Model Context Protocol servers repository | code_doc | medium | reference server patterns、security/quality signals | https://github.com/modelcontextprotocol/servers |

## 项目接入与知识治理来源种子

| 适用分区 | 来源 | 类型 | 可靠性 | 用途 | URL |
| --- | --- | --- | --- | --- | --- |
| `KB_12_PROJECT_INTEGRATION` | CEK-TA external project integration guide | runbook | high | 外部项目接入、健康检查、回灌边界 | `docs/其他项目接入指南.md` |
| `KB_12_PROJECT_INTEGRATION` | CEK-TA contribution schema and sanitization rules | runbook/schema | high | 倒灌、脱敏、项目事实边界 | `codex-expert-kit/rag/contribution_schema.md`、`codex-expert-kit/rag/sanitization_rules.md` |
| `KB_13_KNOWLEDGE_GOVERNANCE` | CEK-TA source quality rules | runbook | high | 来源评分、强制降级、质量门槛 | `codex-expert-kit/rag/source_quality_rules.md` |
| `KB_13_KNOWLEDGE_GOVERNANCE` | CEK-TA conflict detection rules | runbook | high | 冲突类型、阻断规则、审计状态 | `codex-expert-kit/rag/conflict_detection_rules.md` |
| `KB_13_KNOWLEDGE_GOVERNANCE` | CEK-TA quality metrics | runbook | high | 知识质量、检索质量、回归指标 | `codex-expert-kit/rag/quality_metrics.md` |

## 使用规则

```text
1. 种子库只提供起点，不代表 claim 已经被确认。
2. 每个候选包必须重新记录 SourceRef，不能只引用本种子库。
3. time_sensitive 来源必须在采集当天重新访问。
4. 如果来源内容与既有知识冲突，候选状态必须停在 conflict_checked 或 needs_more_evidence。
5. 如果来源只支持特定框架或交易所，不能泛化为通用交易规则。
6. 不保存大段原文，只保存摘要、字段化证据和链接。
```

## 待补强来源

```text
1. KB_01_QUANT_FOUNDATION 需要补充仓位管理、期望值、风险收益比的权威书籍/论文。
2. KB_02_DATA_ENGINEERING 需要按交易所、数据供应商、框架分别补充数据契约来源。
3. KB_03_STRATEGY_ENGINEERING 需要按 K 线结构、指标、微观结构、衍生品流拆分来源。
4. KB_08_TRADE_ANALYSIS 需要补充可脱敏的交易分析 taxonomy 和工程实践来源。
5. KB_12_PROJECT_INTEGRATION 主要由 CEK-TA runbook 和下游项目脱敏贡献补强。
```
