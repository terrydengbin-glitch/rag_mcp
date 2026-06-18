# CEK-TA 专业知识采集 Backlog

本文件是 Phase 12 的首批专业主题采集 backlog。它只定义待研究主题和验收口径，不代表这些主题已经入库或 approved。

## Backlog 使用规则

```text
1. 每个条目必须先生成 ResearchIngestionTask。
2. 每个条目必须输出 IngestionCandidate。
3. 候选知识必须绑定知识树节点。
4. 候选知识必须经过来源评分和冲突检测。
5. accepted 只表示候选通过审计，可转正式知识 draft；不得直接 approved。
6. 本 backlog 采集的是专业交易知识，不采集行情数据、K线数据或订单流原始数据。
```

## 状态定义

```text
todo: 未开始采集
researching: 正在搜索和阅读
candidate_ready: 候选包已生成
needs_review: 需要人工审计
accepted_for_draft: 可转换为正式知识 draft
rejected: 不适合入库
blocked: 缺少来源或存在未解决冲突
```

## 首批主题

| ID | 优先级 | 状态 | 主题 | 目标节点 | 预期产物 |
| --- | --- | --- | --- | --- | --- |
| KR-001 | P0 | todo | 回测前视偏差、数据泄漏和过拟合风险 | `kt.backtest.bias` | checklist、anti_pattern、eval_case |
| KR-002 | P0 | todo | 回测数据质量：缺失、重复、时区、样本边界 | `kt.backtest.data_quality` | procedure、checklist |
| KR-003 | P0 | todo | OHLC 同一根 K 线同时触发 TP/SL 的填充假设 | `kt.replay_simulation.fill_model` | principle、procedure、anti_pattern |
| KR-004 | P0 | todo | 实盘风控：kill switch、最大亏损、权限边界 | `kt.live_execution.risk_control` | procedure、checklist |
| KR-005 | P1 | todo | K 线交易知识：ATR、RSI、移动均线、成交量的使用边界 | `kt.kline_strategy.indicators` | principle、anti_pattern |
| KR-006 | P1 | todo | K 线交易知识：趋势、区间、突破、失效条件 | `kt.kline_strategy.market_structure` | definition、checklist |
| KR-007 | P1 | todo | 仓位管理：单笔风险、组合暴露、杠杆和回撤 | `kt.quant_foundation.position_sizing` | formula、principle、checklist |
| KR-008 | P1 | todo | 执行仿真：滑点、手续费、部分成交和延迟假设 | `kt.replay_simulation.fill_model` | schema、procedure、eval_case |
| KR-009 | P1 | todo | RAG 检索质量：引用、来源可靠性、冲突感知检索 | `kt.rag_engineering.retrieval_policy` | procedure、eval_case |
| KR-010 | P1 | todo | LLM 训练数据：数据集卡、泄漏控制、训练/评测切分 | `kt.llm_training.dataset_design` | checklist、anti_pattern |
| KR-011 | P2 | todo | LLM 评测：交易安全、幻觉、回归样例和通过标准 | `kt.llm_training.eval_design` | eval_case、procedure |
| KR-012 | P2 | todo | 外部项目接入：只读调用、健康检查和知识回灌边界 | `kt.project_integration.adapter` | adapter_rule、checklist |

## 主题详情

### KR-001: 回测前视偏差、数据泄漏和过拟合风险

```yaml
priority: P0
status: todo
target_node_id: kt.backtest.bias
partition_id: KB_04_BACKTEST
domain: backtest
subdomain: bias
questions:
  - 回测中常见 lookahead bias、data leakage、selection bias、overfitting 如何定义？
  - 哪些工程检查可以在代码审计中发现这些风险？
  - 哪些风险只能降低，不能完全消除？
preferred_source_types:
  - paper
  - book
  - framework_doc
freshness_requirement: stable
expected_outputs:
  - checklist
  - anti_pattern
  - eval_case
conflict_check_scope:
  - kt.backtest.bias
  - kt.backtest.data_quality
dod:
  - 至少一个 medium 或 high 来源支撑核心定义
  - 明确不等同于策略收益承诺
  - 写清训练集/测试集/时间切分边界
```

### KR-002: 回测数据质量

```yaml
priority: P0
status: todo
target_node_id: kt.backtest.data_quality
partition_id: KB_04_BACKTEST
domain: backtest
subdomain: data_quality
questions:
  - 缺失 bar、重复事件、时区错位、复权/合约连续性如何影响回测？
  - 数据质量检查应在采集、清洗、特征、回测哪个阶段执行？
preferred_source_types:
  - framework_doc
  - engineering_article
  - paper
freshness_requirement: stable
expected_outputs:
  - procedure
  - checklist
conflict_check_scope:
  - kt.backtest.data_quality
  - kt.backtest.bias
dod:
  - 不能把股票复权规则泛化到 crypto 永续合约
  - 必须区分 kline、trade、order_book 数据粒度
```

### KR-003: OHLC 同一根 K 线 TP/SL 填充假设

```yaml
priority: P0
status: todo
target_node_id: kt.replay_simulation.fill_model
partition_id: KB_05_REPLAY_SIMULATION
domain: replay_simulation
subdomain: fill_model
questions:
  - 只有 OHLC 时是否能知道 TP 与 SL 的真实先后？
  - conservative、optimistic、ambiguous、intrabar replay 各自适用什么场景？
  - 回测报告必须披露哪些填充假设？
preferred_source_types:
  - framework_doc
  - paper
  - engineering_article
freshness_requirement: stable
expected_outputs:
  - principle
  - procedure
  - anti_pattern
conflict_check_scope:
  - kt.replay_simulation.fill_model
dod:
  - 明确 OHLC 与 tick/order_book 的数据粒度边界
  - 不允许把某一种填充顺序写成通用真相
```

### KR-004: 实盘风控

```yaml
priority: P0
status: todo
target_node_id: kt.live_execution.risk_control
partition_id: KB_06_LIVE_EXECUTION
domain: live_trading
subdomain: risk_control
questions:
  - 实盘系统需要哪些 kill switch、max loss、permission gate？
  - 哪些风控规则必须由交易所或账户状态确认？
  - 断线、重复订单、未知订单状态时应如何进入安全状态？
preferred_source_types:
  - official_doc
  - exchange_rule
  - framework_doc
freshness_requirement: time_sensitive
expected_outputs:
  - procedure
  - checklist
conflict_check_scope:
  - kt.live_execution.risk_control
dod:
  - 不给任何实盘投资建议
  - time_sensitive 来源必须有 accessed_at 和 version
  - 默认采用更保守的安全边界
```

### KR-005: K 线交易知识：指标使用边界

```yaml
priority: P1
status: todo
target_node_id: kt.kline_strategy.indicators
partition_id: KB_02_KLINE_STRATEGY
domain: kline_strategy
subdomain: indicators
questions:
  - ATR、RSI、移动均线、成交量指标分别适合表达什么，不适合表达什么？
  - 指标阈值为什么不能跨市场、周期、样本无边界复用？
preferred_source_types:
  - paper
  - book
  - research_report
  - framework_doc
freshness_requirement: stable
expected_outputs:
  - principle
  - anti_pattern
conflict_check_scope:
  - kt.kline_strategy.indicators
  - kt.kline_strategy.market_structure
dod:
  - 必须写明指标滞后、参数敏感性和样本依赖
  - 禁止沉淀保证收益类结论
```

### KR-006: K 线交易知识：市场结构

```yaml
priority: P1
status: todo
target_node_id: kt.kline_strategy.market_structure
partition_id: KB_02_KLINE_STRATEGY
domain: kline_strategy
subdomain: market_structure
questions:
  - 趋势、区间、突破、假突破、失效条件如何结构化表达？
  - 多周期结构冲突时如何记录适用边界？
preferred_source_types:
  - book
  - research_report
  - engineering_article
freshness_requirement: stable
expected_outputs:
  - definition
  - checklist
conflict_check_scope:
  - kt.kline_strategy.market_structure
  - kt.kline_strategy.entry_exit
dod:
  - 区分描述性结构和交易决策
  - 明确不构成单独入场信号
```

### KR-007: 仓位管理

```yaml
priority: P1
status: todo
target_node_id: kt.quant_foundation.position_sizing
partition_id: KB_01_QUANT_FOUNDATION
domain: quant_trading
subdomain: position_sizing
questions:
  - 单笔风险、组合暴露、杠杆、回撤限制如何定义？
  - Kelly 等公式的前置假设和误用风险是什么？
preferred_source_types:
  - paper
  - book
  - research_report
freshness_requirement: stable
expected_outputs:
  - formula
  - principle
  - checklist
conflict_check_scope:
  - kt.quant_foundation.position_sizing
dod:
  - 必须写明公式假设和不可用场景
  - 不输出投资建议或推荐杠杆
```

### KR-008: 执行仿真

```yaml
priority: P1
status: todo
target_node_id: kt.replay_simulation.fill_model
partition_id: KB_05_REPLAY_SIMULATION
domain: replay_simulation
subdomain: fill_model
questions:
  - 滑点、手续费、部分成交、延迟如何在回测/回放/模拟盘里建模？
  - 哪些模型适合低保真筛选，哪些适合实盘前验证？
preferred_source_types:
  - framework_doc
  - paper
  - engineering_article
freshness_requirement: stable
expected_outputs:
  - schema
  - procedure
  - eval_case
conflict_check_scope:
  - kt.replay_simulation.fill_model
  - kt.market_microstructure.order_flow
dod:
  - 明确低保真与高保真边界
  - 明确成本模型会改变策略评价
```

### KR-009: RAG 检索质量

```yaml
priority: P1
status: todo
target_node_id: kt.rag_engineering.retrieval_policy
partition_id: KB_09_RAG_ENGINEERING
domain: rag_engineering
subdomain: retrieval_policy
questions:
  - RAG 检索结果需要哪些 citation、metadata、confidence、conflict warning？
  - 如何设计检索质量评测集和失败样例？
preferred_source_types:
  - official_doc
  - framework_doc
  - paper
freshness_requirement: time_sensitive
expected_outputs:
  - procedure
  - eval_case
conflict_check_scope:
  - kt.rag_engineering.retrieval_policy
  - kt.rag_engineering.source_quality
dod:
  - 不能依赖无引用回答
  - 与 Phase 13 search_result_contract.md 字段一致
```

### KR-010: LLM 训练数据

```yaml
priority: P1
status: todo
target_node_id: kt.llm_training.dataset_design
partition_id: KB_08_LLM_TRAINING
domain: llm_training
subdomain: dataset_design
questions:
  - 交易工程任务数据集如何写 dataset card？
  - 如何避免训练/评测泄漏、版权风险和私有项目污染？
preferred_source_types:
  - official_doc
  - paper
  - framework_doc
freshness_requirement: time_sensitive
expected_outputs:
  - checklist
  - anti_pattern
conflict_check_scope:
  - kt.llm_training.dataset_design
  - kt.llm_training.eval_design
dod:
  - 必须区分 RAG、SFT、eval 数据用途
  - 必须包含 license/source/split/leakage 字段
```

### KR-011: LLM 评测

```yaml
priority: P2
status: todo
target_node_id: kt.llm_training.eval_design
partition_id: KB_08_LLM_TRAINING
domain: llm_training
subdomain: eval_design
questions:
  - 如何评测交易工程助手的幻觉、引用、边界和安全性？
  - 如何把 bad case 变成 regression eval？
preferred_source_types:
  - official_doc
  - paper
  - framework_doc
freshness_requirement: time_sensitive
expected_outputs:
  - eval_case
  - procedure
conflict_check_scope:
  - kt.llm_training.eval_design
  - kt.trade_analysis.bad_case_taxonomy
dod:
  - 评测项必须有 pass/fail 或评分标准
  - 不把模型主观偏好当成专业真相
```

### KR-012: 外部项目接入边界

```yaml
priority: P2
status: todo
target_node_id: kt.project_integration.adapter
partition_id: KB_10_PROJECT_RUNBOOKS
domain: project_runbooks
subdomain: project_adapter
questions:
  - 外部项目如何只读调用 CEK-TA？
  - 项目事实、私有字段、贡献回灌如何隔离？
  - 健康检查应覆盖哪些失败模式？
preferred_source_types:
  - runbook
  - task_card
  - code_doc
freshness_requirement: stable
expected_outputs:
  - adapter_rule
  - checklist
conflict_check_scope:
  - kt.project_integration.adapter
  - kt.project_integration.healthcheck
  - kt.project_integration.contribution
dod:
  - 不把业务项目事实写入通用知识
  - 与 contribution_schema.md 和 sanitization_rules.md 一致
```

## 本轮不做

```text
1. 不实际执行联网采集。
2. 不创建 accepted 或 approved 知识。
3. 不改变 MCP 权限。
4. 不引入数据库或外部服务。
5. 不把 backlog 主题视作投资建议。
6. 不采集行情数据、K线数据或订单流原始数据。
```

## Phase 12 DoD

```text
1. backlog 覆盖回测知识、K线交易知识、风控知识、执行知识、LLM/RAG 知识。
2. 每个主题都有目标知识树节点。
3. 每个主题都有来源类型偏好。
4. 每个主题都有冲突检查范围。
5. 每个主题都有验收条件。
6. UTF-8 中文可读。
```
