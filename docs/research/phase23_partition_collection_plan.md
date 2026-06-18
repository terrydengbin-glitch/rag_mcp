# Phase 23 13 分区专业知识采集矩阵

本文件用于指导 Phase 23 全网专业知识采集。它定义每个 KB 分区优先采什么、从哪些类型来源采、产出什么候选知识，以及哪些内容绝对不能采。

## 全局采集规则

```text
1. 本系统采集专业交易知识、工程知识、AI/RAG/MCP 知识和治理知识，不采集行情数据、K线原始数据或订单流原始数据。
2. 所有采集结果先进入 IngestionCandidate，不直接进入 approved。
3. 每条候选知识必须有来源、适用边界、不适用场景、假设、来源评分、冲突审计和审计状态。
4. P3 来源只能用于发现问题和案例，不能单独支撑通用规则。
5. 涉及交易所、API、模型、框架、MCP、RAG 工具的知识属于 time_sensitive，必须记录 accessed_at、version 或文档日期。
6. 涉及策略、指标、K线结构、风控、仓位的知识必须写明 market、timeframe、data_granularity、成本和假设边界。
7. 禁止沉淀投资建议、推荐杠杆、收益承诺、私有账户配置、私有策略阈值。
```

## 采集优先级

```text
P0: 影响其他项目安全性、回测可信度、检索可信度和知识入库门槛的知识。
P1: 影响策略开发质量、模拟盘可信度、LLM/RAG 工程质量的知识。
P2: 优化体验、扩展覆盖、形成长期知识资产的知识。
```

## 13 分区采集矩阵

| 分区 | 名称 | 优先级 | 首批采集主题 | 首选来源 | 预期候选类型 | 禁止内容 |
| --- | --- | --- | --- | --- | --- | --- |
| `KB_01_QUANT_FOUNDATION` | 量化基础 | P0 | 期望值、风险收益比、成本、Kelly/仓位公式前置假设、交易生命周期 | paper、book、research_report、framework_doc | definition、formula、principle、checklist、anti_pattern | 推荐杠杆、收益承诺、账户级仓位建议 |
| `KB_02_DATA_ENGINEERING` | 数据工程 | P0 | 数据契约、时间对齐、缺失/重复/时区/复权、特征泄漏、数据版本 | official_doc、exchange_rule、framework_doc、engineering_article | schema、procedure、checklist、eval_case | 原始行情数据、私有 vendor key、未映射的项目私有字段 |
| `KB_03_STRATEGY_ENGINEERING` | 策略工程 | P1 | 信号设计、方向/入场/出场、K线结构、指标边界、微观结构、衍生品流 | book、paper、research_report、framework_doc、engineering_article | definition、principle、procedure、anti_pattern、eval_case | 保证盈利、万能指标阈值、无来源交易口诀、原始 K线数据 |
| `KB_04_BACKTEST` | 回测 | P0 | lookahead bias、data leakage、selection bias、overfitting、成本、walk-forward、可复现 | paper、book、framework_doc、engineering_article | checklist、procedure、anti_pattern、eval_case | 只展示收益不披露样本/成本/参数搜索的结论 |
| `KB_05_REPLAY_SIMULATION` | 回放与模拟盘 | P0 | replay clock、事件回放、OHLC 同根 TP/SL、fill model、slippage、latency、fidelity level | framework_doc、paper、engineering_article、official_doc | principle、schema、procedure、eval_case | 未披露成交顺序假设、把低保真模拟等同实盘 |
| `KB_06_LIVE_EXECUTION` | 实盘执行 | P0 | 交易所 adapter、订单状态机、仓位同步、异常订单、安全停机、incident response | official_doc、exchange_rule、framework_doc、engineering_article | official_rule_summary、procedure、checklist、incident | API key、账户配置、过期交易所规则、危险快捷实现 |
| `KB_07_RISK_MANAGEMENT` | 风险管理 | P0 | 风控闸门、单笔风险、组合暴露、回撤控制、日亏损限制、ruin risk | paper、book、exchange_rule、official_doc、engineering_article | principle、formula、procedure、checklist、anti_pattern | 投资建议、推荐杠杆、账户专属限制 |
| `KB_08_TRADE_ANALYSIS` | 交易分析 | P1 | trade quality、bad-case taxonomy、R/R 分解、成本分解、setup/time bucket、迭代闭环 | internal_report、research_report、engineering_article、runbook | taxonomy、definition、procedure、checklist、eval_case | 原始私有交易、账户 PnL 当通用证据、项目私有标签 |
| `KB_09_LLM_TRAINING` | LLM 训练 | P1 | RAG vs finetune、dataset card、SFT/LoRA/QLoRA、偏好训练、评测集、泄漏控制 | official_doc、framework_doc、paper、engineering_article | schema、procedure、checklist、eval_case、anti_pattern | 未授权数据、私有 prompt、把市场事实灌入模型当长期真相 |
| `KB_10_RAG_ENGINEERING` | RAG 工程 | P0 | metadata、chunking、retrieval、rerank、citation、source quality、conflict-aware retrieval、freshness | official_doc、framework_doc、paper、engineering_article | schema、procedure、checklist、eval_case、anti_pattern | 无来源片段、丢 citation、未审计写入工具 |
| `KB_11_MCP_ENGINEERING` | MCP 与 Agent 工程 | P0 | MCP tool contract、权限边界、runtime config、error schema、observability、只读策略、Agent tool-use policy | official_doc、framework_doc、code_doc、runbook | schema、procedure、checklist、anti_pattern、runbook | 隐式写权限、隐藏副作用工具、密钥和危险命令 |
| `KB_12_PROJECT_INTEGRATION` | 其他项目接入 | P1 | adapter、truth boundary、field mapping、healthcheck、贡献回灌、脱敏 | runbook、task_card、code_doc、internal_report | schema、procedure、adapter_rule、checklist、runbook | 原始密钥、未脱敏账户数据、私有字段字典直接通用化 |
| `KB_13_KNOWLEDGE_GOVERNANCE` | 知识治理 | P0 | 状态生命周期、证据政策、冲突消解、来源质量、版本、废弃、贡献审查 | runbook、task_card、official_doc、framework_doc、code_doc | schema、procedure、checklist、anti_pattern、audit_rule | 无来源政策变更、未审计冲突规则、私有经验直接通用化 |

## 每个分区首批验收门槛

```text
1. 至少形成 1 个 ResearchIngestionTask。
2. 每个 P0 分区至少沉淀 1 个候选知识包。
3. 每个候选包至少 1 个 medium/high 来源。
4. 每个候选包必须绑定 canonical_root 或更具体 target_node_id。
5. 每个候选包必须记录 not_applicable_when 和 assumptions。
6. P0 分区候选必须执行冲突检测。
7. time_sensitive 候选必须记录 accessed_at。
8. accepted 候选只能转换为正式知识 draft。
```

## 首批推进顺序

```text
第一批 P0:
1. KB_04_BACKTEST
2. KB_05_REPLAY_SIMULATION
3. KB_06_LIVE_EXECUTION
4. KB_07_RISK_MANAGEMENT
5. KB_10_RAG_ENGINEERING
6. KB_11_MCP_ENGINEERING
7. KB_13_KNOWLEDGE_GOVERNANCE

第二批 P1:
1. KB_01_QUANT_FOUNDATION
2. KB_02_DATA_ENGINEERING
3. KB_03_STRATEGY_ENGINEERING
4. KB_08_TRADE_ANALYSIS
5. KB_09_LLM_TRAINING
6. KB_12_PROJECT_INTEGRATION
```

## 不做什么

```text
1. 不执行自动大规模爬取。
2. 不保存大段版权原文。
3. 不采集 raw market data。
4. 不把候选知识放进 MCP 默认检索。
5. 不改变已有正式知识的 approved 状态。
6. 不引入外部数据库或新服务。
```
