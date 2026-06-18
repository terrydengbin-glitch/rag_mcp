# Phase 59 Microstructure Feature Store & Hybrid Snapshot Research

生成日期：2026-06-17

## 研究问题

用户提出的知识点：

```text
K 线 snap 和 microstructure 原始/高频数据不应强行混在一个物理表或一个宽表里；
也不应按 AI Trader 物理分库；
更合理的是中央 canonical registry / audit ledger + 按数据粒度和写入特征物理分层 + 训练时通过 dataset snapshot manifest 逻辑组合。
```

本报告核验该方向是否值得进入 CEK-TA 候选知识库。

## 本地契约对齐

### Phase 42 Database / Storage Contract

`docs/contracts/phase42_database_storage_contract.md` 已定义：

```text
1. canonical records 必须进入关系型事实存储，不能只存在向量库、日志或临时文件。
2. 所有 scoring/gating 决策必须有 audit_trace_id。
3. decision_time、event_time、ingestion_time、label_time 必须分离。
4. feature_snapshot_manifest 和 dataset_snapshot_manifest 是正式存储契约对象。
5. point-in-time correctness 是训练数据硬边界。
```

该契约支持“中央 canonical registry / audit ledger + dataset snapshot manifest”的方向。

### Phase 38 Training Data And Evaluation Contract

`docs/contracts/phase38_training_data_and_eval_contract.md` 已定义：

```text
1. 交易日志不能直接变成训练输入。
2. 决策时可见信息和事后结果必须物理或逻辑隔离。
3. Decision-Time Feature Frame 必须保留 feature_timestamp、feature_available_time、source_object、lineage 和 feature_schema_version。
4. Numeric Scorer Dataset 只允许 decision_time_features，不允许 future market movement、post_trade outcome 或 LLM explanation as numeric feature。
```

该契约支持“microstructure 原始数据不能直接进入训练样本，必须通过决策时可见聚合特征和 manifest 进入训练集”的方向。

## 外部来源核验

### Feast：point-in-time feature retrieval 和 feature store 分层

来源：

```text
https://docs.feast.dev/
https://docs.feast.dev/getting-started/concepts/point-in-time-joins
https://docs.feast.dev/getting-started/concepts/feature-retrieval
```

可支持的结论：

```text
1. 训练数据应通过 point-in-time correct feature sets 生成，避免未来特征泄漏。
2. Feature store 提供统一访问层，抽象底层数据基础设施。
3. 离线训练和在线推理可以通过不同存储服务，但通过统一特征定义和检索语义消费。
```

不能支持的结论：

```text
1. 不强制使用 Feast。
2. 不证明所有 microstructure 数据都必须进入 feature store。
3. 不定义交易领域的 K 线、盘口、订单簿或成交打印本体。
```

### Apache Iceberg：逻辑表与物理分区解耦

来源：

```text
https://iceberg.apache.org/
https://iceberg.apache.org/docs/latest/partitioning/
https://iceberg.apache.org/spec/
```

可支持的结论：

```text
1. 表的逻辑 schema 不应暴露或绑定全部物理分区细节。
2. Hidden partitioning 和 partition evolution 支持数据布局随查询模式或数据规模演进。
3. 适合支持“不要把物理布局绑死到一张宽表或固定分区列”的方法边界。
```

不能支持的结论：

```text
1. 不强制使用 Iceberg。
2. 不证明 SQLite/DuckDB/Parquet/ClickHouse/kdb+ 哪个是唯一正确实现。
```

### ClickHouse MergeTree：高写入和大数据量事件存储模式

来源：

```text
https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree
https://clickhouse.com/docs/engines/table-engines/mergetree-family
```

可支持的结论：

```text
1. MergeTree family 面向高数据写入率和巨大数据量。
2. 适合作为高频事件、时间序列或分析型存储的实现模式之一。
3. 支持把 microstructure 高频事件与低频 K 线 snap 在物理存储层分开。
```

不能支持的结论：

```text
1. 不强制使用 ClickHouse。
2. 不把 ClickHouse 文档写成交易系统通用法规或唯一数据库选择。
```

### KX/kdb+ tick：实时和历史市场数据分层案例

来源：

```text
https://code.kx.com/q/architecture/
https://code.kx.com/q/learn/startingkdb/tick/
```

可支持的结论：

```text
1. kdb+ tick 架构常用于捕获、处理和分析大量实时与历史数据。
2. 典型架构包含 tickerplant、RDB 和 HDB，用于区分实时数据、当日内存数据和历史数据库。
3. 这是高频 market data 常见物理分层案例，可作为 microstructure store 的参考模式。
```

不能支持的结论：

```text
1. 不强制使用 kdb+。
2. 不证明所有项目都需要完整 tick 架构。
```

## 候选知识拆分

建议拆成 3 条候选：

| 研究任务 | 候选主题 | 主归属 | 说明 |
| --- | --- | --- | --- |
| P59-MFS-001 | Kline Snapshot 与 Microstructure Store 不应混成一个宽表 | `KB_03_MARKET_MICROSTRUCTURE` / `kt.market_microstructure.order_flow` | Trading 本体边界：K 线低频 snap 与 tick/order book/trade prints 高频事件的物理层分离 |
| P59-MFS-002 | Hybrid Training Dataset Snapshot Manifest 逻辑组合 kline/micro features | `KB_AI_26_DATABASE_STORAGE` / `kt.ai_engineering.database_storage_engineering.feature_store_storage` | AI/DB 契约：训练样本通过 manifest 绑定 kline_snapshot_ref、micro_snapshot_ref、feature_schema_hash、dataset_hash、known_at_pass |
| P59-MFS-003 | 中央 canonical registry / audit ledger 不应按 AI Trader 物理分库 | `KB_AI_26_DATABASE_STORAGE` / `kt.ai_engineering.database_storage_engineering.relational_core_schema` | AI/DB 契约：按 unit_id/unit_version 逻辑隔离，不按 Trader 物理分库 |

## 推荐架构表达

```text
Canonical Registry / Audit Ledger
  保存 unit、dataset、manifest、audit_trace、feature_schema、ledger、lineage、readiness。

Kline Snapshot Store
  保存 1m/5m/15m K 线、指标、entry/exit snap、低频决策上下文。

Microstructure Store
  保存 tick、order book、trade prints、spread、depth、OFI、CVD 等高频原始或聚合数据。

Feature Store / Feature Manifest
  保存 decision-time 可见的聚合特征定义、schema hash、lineage、available_time。

Training Dataset Snapshot
  通过 kline_snapshot_ref + micro_snapshot_ref + feature_schema_hash + dataset_hash + known_at_pass + readiness 逻辑组合训练样本。
```

## 入库边界

必须写清：

```text
1. 物理分层按数据粒度、写入频率、查询模式和审计需求，不按 AI Trader 物理分库。
2. microstructure 原始数据不能直接成为 numeric scorer 输入，必须经过 decision-time feature frame 和 point-in-time 检查。
3. Vector DB 或临时文件不能替代 canonical registry / audit ledger。
4. ClickHouse/kdb+/Feast/Iceberg 只能作为 implementation pattern 或 supporting source。
5. 不生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。
```

## 初步结论

该知识点值得入库，且应进入候选审计流程。它不是单纯数据库实现建议，而是 Trading AI 数据架构边界规则，可为后续 AI Trader 项目的数据采集、训练样本生成、特征存储和审计回放提供基础约束。
