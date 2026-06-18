# Phase 45 Resilience / Incident / Log Runtime Contract

## 目标

本契约用于支撑 Phase 45 / P45-D 中系统韧性、事故响应、降级模式、只读模式、恢复、replay 和日志治理知识。它只定义 CEK-TA 支持层的通用字段和边界，不创建实盘执行动作，不定义停机阈值，不定义风险阈值，不替代外接项目的 Live Execution / Risk Management owner。

## 适用范围

```text
适用：
1. 外接交易项目设计 runtime mode、degraded mode、read-only mode、recovery mode。
2. 外接交易项目设计 failover、state rebuild、audit replay、simulation replay 和 live order action 的边界。
3. AI IDE 检查交易系统方案是否把恢复回放误写成真实订单重发或修改。

不适用：
1. 不给出买卖点、仓位、杠杆、止损止盈。
2. 不给出停机阈值、恢复阈值、风险阈值。
3. 不替外接项目触发拒单、撤单、重发订单、停机、解锁。
4. 不替代 broker、exchange、venue 或账户事实来源。
```

## Runtime Mode Schema

```json
{
  "runtime_mode": {
    "mode": "normal | degraded | read_only | recovery | manual_intervention_required",
    "mode_reason": "string",
    "entered_at": "timestamp",
    "entered_by": "system | operator | risk_owner | live_execution_owner",
    "allowed_operations": [
      "query_status",
      "read_audit_log",
      "reconcile_state",
      "export_report"
    ],
    "forbidden_operations": [
      "new_order",
      "cancel_replace",
      "live_order_replay_write",
      "position_mutation",
      "risk_threshold_change"
    ],
    "data_freshness_policy": {
      "market_data_status": "fresh | stale | unknown",
      "account_state_status": "fresh | stale | unknown",
      "order_state_status": "fresh | stale | unknown",
      "freshness_evidence_id": "string"
    },
    "write_policy": {
      "order_write_enabled": false,
      "audit_write_enabled": true,
      "configuration_write_enabled": false,
      "reason": "string"
    },
    "exit_conditions": [
      {
        "condition_id": "string",
        "description": "string",
        "evidence_required": ["string"],
        "owner": "live_execution_owner | risk_owner | operations_owner"
      }
    ],
    "manual_approval_required": true,
    "audit_trace_id": "string"
  }
}
```

### Runtime Mode 边界

```text
1. degraded/read_only 只能说明系统能力受限，不等于自动停机或自动放行。
2. read_only 模式默认允许查询、审计、状态核对和报告导出，不允许新订单、cancel/replace、replay 写入或风险阈值修改。
3. recovery 模式允许状态重建和审计回放，但不允许通过回放直接写真实订单。
4. manual_intervention_required 表示需要人工/owner 复核，不代表 CEK-TA 已经定义执行动作。
```

## Replay Boundary Schema

```json
{
  "replay_boundary": {
    "replay_mode": "audit_replay | simulation_replay | state_rebuild | live_order_action",
    "source_of_truth": "broker_order_state | exchange_order_state | clearing_statement | internal_event_log",
    "client_order_id": "string",
    "venue_order_id": "string",
    "broker_order_id": "string",
    "idempotency_key": "string",
    "original_event_id": "string",
    "replay_event_id": "string",
    "state_snapshot_id": "string",
    "replay_reason": "string",
    "allowed_write_scope": "none | audit_log_only | simulation_store_only | external_owner_approved_live_action",
    "live_action_requires": [
      "order_source_of_truth_confirmed",
      "idempotency_key_present",
      "current_order_state_checked",
      "risk_owner_approval",
      "live_execution_owner_approval",
      "audit_trace_id"
    ],
    "forbidden_without_approval": [
      "new_order",
      "cancel_replace",
      "cancel_order",
      "modify_order",
      "resubmit_order"
    ]
  }
}
```

### Replay 边界

```text
1. audit_replay 只用于审计解释和事件链复现。
2. simulation_replay 只用于回测、回放或模拟证据。
3. state_rebuild 只用于恢复内部状态视图，不能自动写 broker/exchange。
4. live_order_action 必须由外接项目 Live Execution / Risk Management owner 明确授权。
5. 没有幂等键、订单真相源、当前订单状态快照、owner 审批和审计 trace 时，不得通过 replay 自动重发、修改或撤销真实订单。
```

## Owner 边界

```text
Live Execution owner：
1. 拥有真实订单、成交、取消、修改、broker/venue 状态事实。
2. 拥有 order state machine 和 source-of-truth 查询。

Risk Management owner：
1. 拥有风险政策、人工复核、解锁、恢复放行和 hard gate。
2. 拥有停机/恢复阈值，但 CEK-TA 不提供这些数值。

Operations owner：
1. 拥有 runtime mode、incident response、BC/DR、恢复演练和 post-incident review。

Database / Storage owner：
1. 拥有 audit log、telemetry、correlation id、hash/checksum、retention 和 archive restore。

AI Engineering owner：
1. 只能引用 mode、incident、replay 和 reason code 做审计解释或 RAG 检索。
2. 不能发起 live order action。
```

## Incident Taxonomy Schema

```json
{
  "incident_taxonomy": {
    "taxonomy_scope": "CEK-TA internal taxonomy",
    "taxonomy_version": "string",
    "category": [
      "system_availability",
      "data_quality",
      "order_and_fill",
      "risk_policy",
      "account_and_funding",
      "external_dependency",
      "market_state",
      "human_action"
    ],
    "impact_area": ["runtime", "data", "execution", "risk", "storage", "operations"],
    "affected_system": "string",
    "market_impact": "none | delayed | degraded | unknown",
    "data_quality": "valid | stale | missing | corrupted | unknown",
    "order_state": "not_applicable | pending | partially_filled | filled | canceled | rejected | unknown",
    "human_action": "none | manual_override | manual_recovery | manual_review_required",
    "audit_trace_id": "string",
    "owner": "operations_owner | live_execution_owner | risk_owner | data_owner | storage_owner"
  }
}
```

### Incident Taxonomy 边界

```text
1. 以上 taxonomy 是 CEK-TA internal taxonomy，不是外部监管机构或交易所发布的通用事故分类标准。
2. taxonomy label 只能进入 audit、review、priority queue、post-incident review 或 RAG 检索上下文。
3. taxonomy label 不得自动触发交易动作、风控阈值、停机阈值、拒单、撤单、重发订单或 hard gate。
```

## Audit Ledger Schema

```json
{
  "audit_ledger_event": {
    "ledger_id": "string",
    "event_id": "string",
    "correlation_id": "string",
    "source_event_id": "string",
    "source_ts": "timestamp",
    "ingest_ts": "timestamp",
    "event_type": "runtime_mode_change | order_event | incident_event | replay_event | access_event | delete_event | correction_event",
    "actor": "system | operator | live_execution_owner | risk_owner | storage_owner",
    "source_system": "string",
    "hash": "string",
    "prev_hash": "string",
    "integrity_check": "hash_chain | immutable_storage | external_audit_trail | unknown",
    "access_log_id": "string",
    "delete_log_id": "string",
    "retention_policy_ref": "string",
    "jurisdiction_scope": "string",
    "order_truth_source_ref": "string",
    "archive_restore_path": "string"
  }
}
```

### Log 层级边界

```text
1. debug_log：用于开发和排错，不等于正式 audit ledger。
2. telemetry_log：用于观测 traces、metrics、logs，不等于订单事实来源。
3. incident_log：用于事故响应和复盘，不等于 order truth source。
4. audit_ledger：用于审计追踪、完整性校验、访问/删除审计和保留策略证明。
5. order_truth_source：真实订单、成交、撤单、拒单、费用和账户事实仍归 Live Execution / broker / venue / clearing source。
6. audit ledger 不能替代 broker/venue/order source of truth，也不能推导交易许可或 hard gate。
```

## Machine Gate

```json
{
  "default_guidance": "deny",
  "approved_allowed": false,
  "default_guidance_allowed": false,
  "hard_gate_allowed": false,
  "risk_threshold_advice_allowed": false,
  "trade_execution_advice_allowed": false
}
```

## 测试要求

```text
1. 缺少 idempotency_key 的 live_order_action 必须被标记为 invalid_for_live_action。
2. read_only 模式下 new_order、cancel_replace、live_order_replay_write 必须被标记为 forbidden_operation。
3. recovery 模式下 audit_replay 和 state_rebuild 允许写审计/状态存储，但不得写 broker/exchange。
4. 所有 mode change 和 replay request 必须有 audit_trace_id。
5. 所有输出不得包含买卖点、仓位、杠杆、止损止盈、风险阈值或实盘执行建议。
```
