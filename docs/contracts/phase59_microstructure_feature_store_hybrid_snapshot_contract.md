# Phase 59 Microstructure Feature Store & Hybrid Snapshot Contract

生成日期：2026-06-17

## 1. 契约目标

本契约定义 CEK-TA 对外接 Trading AI 项目中 K 线 snapshot、microstructure 数据、feature store、training dataset snapshot 和 canonical registry / audit ledger 的最小工程边界。

目标不是指定唯一数据库或真实 DDL，而是约束 AI IDE / 外接项目在设计数据层时：

```text
1. 不默认把低频 K 线 snap 和高频 microstructure 原始数据强行塞进一个物理宽表。
2. 不默认按 AI Trader 物理分库；物理分库只能作为合规隔离、客户密钥、监管边界、地域隔离、超大规模或运维约束下的例外。
3. 通过 dataset snapshot manifest 做 point-in-time、版本绑定、审计可回放的逻辑组合。
4. 保留 canonical registry / audit ledger 作为事实索引和治理入口。
```

## 2. 强制边界

```text
1. 本契约不创建真实数据库。
2. 本契约不强制使用 ClickHouse、kdb+、Feast、Iceberg、DuckDB、SQLite、Parquet 或任何单一技术。
3. 本契约不允许把 microstructure 原始数据直接作为训练样本输入。
4. 本契约不允许向量库或临时文件替代 canonical registry / audit ledger。
5. 本契约不定义买卖点、仓位、杠杆、止损止盈或实盘执行建议。
6. 本契约不创建 approved、default guidance 或 hard gate。
```

## 3. 逻辑对象

```text
MicrostructureHybridSnapshotContract:
  canonical_registry_identity
  audit_ledger_identity
  kline_snapshot_identity
  microstructure_store_identity
  microstructure_feature_identity
  feature_store_identity
  hybrid_training_dataset_snapshot_manifest
  point_in_time_join_policy
  readiness_policy
  tenant_isolation_policy
  owner_mapping
  missing_field_policy
  audit_trace
```

## 4. 字段契约

### 4.1 canonical_registry_identity

```json
{
  "registry_id": "string, required",
  "registry_schema_version": "string, required",
  "unit_id": "string, required",
  "unit_version": "string, required",
  "strategy_id": "string, required",
  "strategy_version": "string, required",
  "dataset_manifest_ref": "string, required",
  "feature_schema_ref": "string, required",
  "audit_trace_id": "string, required"
}
```

规则：

```text
1. unit_id / unit_version 是逻辑隔离字段，不代表每个 AI Trader 必须物理分库。
2. canonical registry 保存事实索引、版本引用和治理入口，不保存所有高频明细。
3. registry 不得被向量库、临时文件或未审计 cache 替代。
```

### 4.2 audit_ledger_identity

```json
{
  "ledger_id": "string, required",
  "ledger_schema_version": "string, required",
  "actor": "string, required",
  "action": "string, required",
  "reason": "string, required",
  "before_state_hash": "string|null, required",
  "after_state_hash": "string, required",
  "row_hash": "string|null, required",
  "prev_hash": "string|null, required",
  "created_at": "ISO-8601 timestamp, required",
  "audit_trace_id": "string, required"
}
```

规则：

```text
1. 高价值 dataset、feature、snapshot、readiness 和 promotion 状态变更必须进入 audit ledger。
2. ledger 是 append-only 或等价可追溯结构。
3. row_hash/prev_hash 可以为空，但必须说明替代防篡改机制。
```

### 4.3 kline_snapshot_identity

```json
{
  "kline_snapshot_ref": "string, required",
  "symbol_or_instrument_ref": "string, required",
  "timeframe": "string, required",
  "bar_start_time": "ISO-8601 timestamp, required",
  "bar_end_time": "ISO-8601 timestamp, required",
  "feature_available_time": "ISO-8601 timestamp, required",
  "indicator_schema_version": "string|null, required",
  "entry_exit_snapshot_version": "string|null, required",
  "source_dataset_version": "string, required",
  "snapshot_hash": "string, required"
}
```

规则：

```text
1. Kline snapshot 适合保存低频 K 线、指标、entry/exit snap 和决策上下文。
2. Kline snapshot 不应承载 tick、order book、trade prints 等高频原始事件。
3. feature_available_time 必须不晚于 decision_time。
```

### 4.4 microstructure_store_identity

```json
{
  "micro_snapshot_ref": "string, required",
  "store_type": "enum[tick, order_book, trade_prints, spread_depth, order_flow, mixed], required",
  "venue_id": "string, required",
  "instrument_id": "string, required",
  "event_time_start": "ISO-8601 timestamp, required",
  "event_time_end": "ISO-8601 timestamp, required",
  "ingestion_time_range": "string, required",
  "raw_data_ref": "string|null, required",
  "aggregation_ref": "string|null, required",
  "storage_layout_version": "string, required",
  "retention_policy_ref": "string, required",
  "quality_report_id": "string, required"
}
```

规则：

```text
1. 高频 microstructure 原始数据应按写入频率、事件类型、查询模式和保留策略物理分层。
2. microstructure raw store 可以由 ClickHouse、kdb+、Parquet/Iceberg、专用 time-series store 或其他实现承载，但契约不能绑定单一技术。
3. 原始 microstructure 数据不得直接进入 numeric scorer；必须先形成 decision-time micro feature。
```

### 4.5 microstructure_feature_identity

```json
{
  "micro_feature_ref": "string, required",
  "feature_names": "array[string], required",
  "feature_schema_hash": "string, required",
  "feature_available_time": "ISO-8601 timestamp, required",
  "source_micro_snapshot_ref": "string, required",
  "aggregation_window": "string, required",
  "aggregation_policy_version": "string, required",
  "lineage_id": "string, required",
  "known_at_pass": "boolean, required"
}
```

规则：

```text
1. OFI、CVD、spread、depth、trade imbalance 等 micro features 必须记录窗口、来源、schema 和 available_time。
2. known_at_pass=false 时，不得进入训练样本或在线 scoring 输入。
3. micro feature 只能表达决策时点可见信息，不得包含未来成交、未来盘口或标签结果。
```

### 4.6 feature_store_identity

```json
{
  "feature_store_ref": "string, required",
  "offline_store_ref": "string|null, required",
  "online_store_ref": "string|null, required",
  "feature_view_version": "string, required",
  "entity_keys": "array[string], required",
  "point_in_time_join_policy": "string, required",
  "feature_serving_sla_ref": "string|null, required"
}
```

规则：

```text
1. offline_store / online_store 是实现模式，不强制使用 Feast。
2. 训练和推理可以使用不同物理存储，但必须共享 feature definition、schema hash 和 point-in-time 语义。
3. feature store 不能替代 canonical registry / audit ledger。
```

### 4.7 hybrid_training_dataset_snapshot_manifest

```json
{
  "dataset_snapshot_id": "string, required",
  "dataset_hash": "string, required",
  "dataset_version": "string, required",
  "kline_snapshot_refs": "array[string], required",
  "micro_snapshot_refs": "array[string], required",
  "micro_feature_refs": "array[string], required",
  "feature_schema_hash": "string, required",
  "label_policy_version": "string, required",
  "split_manifest_ref": "string, required",
  "prediction_time": "ISO-8601 timestamp, required",
  "feature_event_time": "ISO-8601 timestamp, required",
  "feature_known_at": "ISO-8601 timestamp, required",
  "label_event_time": "ISO-8601 timestamp, required",
  "label_known_at": "ISO-8601 timestamp, required",
  "feature_materialization_version": "string, required",
  "feature_generation_code_hash": "string, required",
  "known_at_pass": "boolean, required",
  "readiness": "enum[draft, training_ready, blocked, needs_review], required",
  "audit_trace_id": "string, required"
}
```

规则：

```text
1. dataset snapshot 只保存可训练样本引用、固化后的 feature frame 和版本 hash，不复制全部 raw microstructure 明细。
2. kline_snapshot_refs 与 micro_snapshot_refs 必须能追溯到各自来源和质量报告。
3. known_at_pass=false 或 readiness=blocked 时，不得进入训练。
4. dataset_hash 必须随任意输入引用、feature schema、label policy、split manifest 改变而改变。
5. prediction_time、feature_known_at 和 label_known_at 必须能证明训练样本没有使用未来特征或未来标签。
6. feature_materialization_version 和 feature_generation_code_hash 必须记录特征生成链路版本。
```

### 4.8 point_in_time_join_policy

```json
{
  "policy_id": "string, required",
  "entity_time_field": "string, required",
  "feature_available_time_field": "string, required",
  "max_staleness_policy": "string|null, required",
  "future_feature_block": "boolean, required",
  "join_tolerance_policy": "string, required",
  "feature_ttl_policy": "string, required",
  "asof_join_direction": "enum[backward, exact, forbidden_forward], required",
  "null_feature_policy": "string, required",
  "late_arrival_policy": "string, required",
  "calendar_policy": "string, required",
  "timezone_policy": "string, required"
}
```

规则：

```text
1. future_feature_block 必须为 true。
2. feature_available_time > decision_time 时必须 block_sample。
3. late_arrival_policy 必须说明迟到事件如何影响训练样本 readiness。
4. asof_join_direction 不得允许 forward join。
5. null_feature_policy 必须说明缺失 micro feature 时是阻断、填充、降级还是人工复核。
```

### 4.9 readiness_policy

```json
{
  "readiness_policy_id": "string, required",
  "required_quality_reports": "array[string], required",
  "required_manifest_refs": "array[string], required",
  "blockers": "array[string], required",
  "human_review_required": "boolean, required",
  "not_live_permission": "boolean, required"
}
```

规则：

```text
1. readiness 只表示训练数据准备状态，不表示交易许可。
2. human_review_required 默认 true，除非外接项目有独立治理契约。
3. not_live_permission 必须为 true。
```

### 4.10 tenant_isolation_policy

```json
{
  "tenant_isolation_policy_id": "string, required",
  "default_isolation_model": "enum[logical_unit_fields, pool, silo, bridge], required",
  "physical_split_allowed": "boolean, required",
  "physical_split_reason": "array[compliance_isolation_required, customer_key_required, regulatory_boundary_required, geo_boundary_required, scale_sharding_required, operational_safety_required], required",
  "cross_database_lineage_reconciliation": "string|null, required",
  "global_registry_ref": "string, required",
  "global_audit_trace_policy": "string, required"
}
```

规则：

```text
1. 默认隔离模型是 unit_id / unit_version / strategy_id / strategy_version 等逻辑字段。
2. 物理分库、schema 隔离或 hybrid pool/silo/bridge 架构只能作为有证据的例外。
3. 任何物理拆分都必须保留 global registry、cross-database lineage reconciliation 和 audit trace。
4. 向量库、cache、日志片段或临时文件不得替代 canonical registry / audit ledger。
```

## 5. Owner Mapping

```text
Market Microstructure owner:
  microstructure 原始数据、本体语义、盘口/成交/订单流解释边界。

Data Engineering owner:
  raw/cleaned/adjusted/feature_ready/label_ready 数据层、available_time、质量报告、lineage。

AI Engineering owner:
  feature store、training dataset snapshot、numeric scorer dataset、LLM audit dataset、dataset hash、schema hash。

Database / Storage owner:
  canonical registry、audit ledger、storage layout、retention、migration、backup。

Risk / Live Execution owner:
  真实订单、成交、拒单、账户、风控事实；不由本契约接管。
```

## 6. Machine Gate

```json
{
  "default_guidance": "deny",
  "reviewed_allowed": false,
  "approved_allowed": false,
  "default_guidance_allowed": false,
  "hard_gate_allowed": false,
  "trade_execution_advice_allowed": false,
  "requires_human_escalation": true
}
```

规则：

```text
1. Phase 59 候选进入外部审计前不得作为 formal reviewed 使用。
2. 即使后续 reviewed/caveat_only，也只能作为数据架构审计和 RAG 检索上下文。
3. 不允许进入 default guidance queue。
```

## 7. 不做什么

```text
1. 不定义真实数据库 DDL。
2. 不定义任何交易信号或执行规则。
3. 不规定必须使用某个数据库或 feature store。
4. 不把 K 线 snap、microstructure raw、label、outcome 混成一个宽表。
5. 不默认按 AI Trader 物理分库；物理分库必须有 tenant isolation policy 和 lineage reconciliation。
6. 不让向量库、cache 或临时文件成为事实主库。
```
