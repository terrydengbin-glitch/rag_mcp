# Phase 45 Audit Trail / Clock Sync 内部契约

## 契约目标

本契约服务 Phase 45 / P45-B Audit Trail / Clock Sync 知识候选，用于把外部监管、协议、日志管理、事件流和存储来源落到 CEK-TA 内部可审计字段。

本契约只定义知识库和外接项目设计时应检查的字段边界，不创建数据库表，不规定具体存储产品，不启用实盘 hard gate，不输出买卖点、仓位、杠杆、止损止盈或风险阈值。

## Owner 边界

| 范围 | Owner | 边界 |
| --- | --- | --- |
| 时钟同步和事件时间 | Data Engineering / Live Execution | 只记录事件时间、接收时间、日志时间、时区、精度、同步来源和漂移证据 |
| 订单事件因果链 | Live Execution | 只记录订单、路由、修改、撤单、拒单、成交和终态事件链 |
| 事件序列和幂等 | Live Execution / Data Engineering | 只定义 event_id、sequence、dedup_key、idempotency_key、replay_cursor 和 correction event |
| 审计日志 retention 与完整性 | Database / Storage Engineering | 只定义 retention、record class、完整性校验、修改/删除审计和归档恢复路径 |
| 合规解释 | 外接项目法律/合规 owner | CEK-TA 不给具体辖区合规结论 |
| 风控动作 | Risk Management / Live Execution | CEK-TA 不自动拒单、停机、撤单、解锁或放行 |

## 订单事件审计字段

| 字段 | 必填 | 类型 | 语义 |
| --- | --- | --- | --- |
| `event_id` | yes | string | CEK-TA 事件唯一 ID，不等于 broker/exchange ID |
| `source_system` | yes | string | 事件来源系统，例如 order_gateway、broker_adapter、exchange_feed、manual_ops |
| `event_type` | yes | enum | received、routed、replaced、canceled、rejected、partial_fill、fill、expired、terminal_state、correction |
| `event_time` | yes | timestamp | 事件在业务系统或外部系统中发生的时间 |
| `receive_time` | yes | timestamp | CEK-TA 或外接系统收到事件的时间 |
| `log_time` | yes | timestamp | 日志写入时间 |
| `timezone` | yes | string | 时间戳时区或 UTC 规范 |
| `timestamp_precision` | yes | string | 时间精度，例如 second、millisecond、microsecond、nanosecond |
| `clock_source` | yes | string | 时钟来源或同步服务引用 |
| `clock_drift_status` | yes | enum | within_policy、observed_drift、unknown、not_applicable |
| `prev_event_id` | optional | string | 前序事件 ID，用于因果链 |
| `parent_event_id` | optional | string | 上游父事件 ID，用于 cancel/replace、correction 或派生事件 |
| `client_order_id` | optional | string | 客户端订单 ID，由外接项目事实层提供 |
| `broker_order_id` | optional | string | broker 订单 ID，由外接项目事实层提供 |
| `exchange_order_id` | optional | string | 交易所订单 ID，由外接项目事实层提供 |
| `actor` | optional | string | human、system、broker、exchange、risk_engine、unknown |
| `reason_code` | optional | string | 修改、取消、拒单、校正或异常原因 |

## 事件序列和幂等字段

| 字段 | 必填 | 类型 | 语义 |
| --- | --- | --- | --- |
| `sequence` | yes | integer/string | 来源系统或 CEK-TA 分配的事件序列 |
| `dedup_key` | yes | string | 重复事件检测键 |
| `idempotency_key` | yes | string | 幂等处理键 |
| `replay_cursor` | optional | string | 重放或回灌游标 |
| `replay_reason` | optional | enum | recovery、backfill、migration、correction、audit_rebuild |
| `correction_event_id` | optional | string | 校正事件 ID；校正不得覆盖原始事件 |
| `original_event_id` | optional | string | 被校正的原始事件 ID |
| `ordering_status` | yes | enum | in_order、out_of_order、duplicate、missing_gap、late_arrival、unknown |
| `ingestion_status` | yes | enum | accepted、duplicate_ignored、correction_appended、quarantined、rejected |
| `raw_event_hash` | optional | string | 原始事件载荷摘要，用于完整性检查 |

规则：

```text
1. 乱序、重复、缺失和延迟事件必须显式标记。
2. replay/backfill/correction 不得静默覆盖原始真实事件。
3. Exactly-once、at-least-once、at-most-once 是工程语义，不得被写成监管或交易所统一保证。
4. 外接项目可用 Kafka、CDC、数据库唯一键、append-only event store 或等价机制实现，但必须保留可审计字段。
```

## 审计日志 retention 与完整性字段

| 字段 | 必填 | 类型 | 语义 |
| --- | --- | --- | --- |
| `audit_record_id` | yes | string | 审计记录 ID |
| `record_class` | yes | enum | order_event、execution_report、clock_sync、retention_policy、regulatory_report_intermediate、manual_entry |
| `retention_policy_id` | yes | string | 保留策略引用，不在 CEK-TA 通用知识中写死年限 |
| `jurisdiction_scope` | yes | string | 适用辖区或市场范围 |
| `storage_mode` | yes | enum | append_only、worm、audit_trail_alternative、object_lock、ledger_like、unknown |
| `integrity_check` | yes | enum | checksum、hash_chain、object_version_lock、audit_trail_reconstruction、none_declared |
| `checksum_or_hash` | optional | string | 记录或对象摘要 |
| `modification_audit_id` | optional | string | 修改审计记录 |
| `deletion_audit_id` | optional | string | 删除审计记录 |
| `access_audit_id` | optional | string | 访问审计记录 |
| `archive_restore_path` | optional | string | 归档恢复路径或过程引用 |
| `legal_hold_status` | optional | enum | none、active、unknown |
| `immutability_exception_reason` | optional | string | 不可变存储例外说明 |

规则：

```text
1. 普通应用日志不能在缺少 retention、完整性校验、修改/删除审计和恢复路径时被当作可审计 ledger。
2. WORM、audit-trail alternative、object lock 和 hash/checksum 是实现或合规模式，不是所有市场的统一强制方案。
3. CEK-TA 不输出具体 retention 年限；外接项目必须由法律/合规 owner 绑定 jurisdiction 和 record_class。
4. Database/Storage Engineering 只拥有存储完整性和生命周期，不拥有策略、订单执行或风险阈值。
```

## Reviewed/Caveat-Only 导入条件

P45-B 知识候选进入 formal reviewed/caveat_only 前必须满足：

```text
1. 候选已通过 accepted_for_draft 或 reviewed preparation 外部严格审计。
2. source_refs 至少包含可审计来源，且来源角色不能被夸大。
3. 本契约摘要、schema extract 或 contract hash 已进入 reviewed preparation 包。
4. machine_gate.default_guidance 只能是 caveat_only 或 deny，不能启用 default guidance。
5. approved_allowed、default_guidance_allowed、hard_gate_allowed、risk_threshold_advice_allowed 必须为 false。
6. 候选与 Phase 37/42/45 已有知识做冲突和重复检查。
```

## 不做什么

```text
1. 不创建数据库表或迁移。
2. 不指定 Kafka、Debezium、AWS S3、WORM 或任何供应商为唯一实现。
3. 不输出交易建议、风控阈值或法律合规结论。
4. 不把审计字段变成策略 alpha、胜率解释或交易放行条件。
5. 不把 reviewed/caveat_only 自动提升为 approved。
```
