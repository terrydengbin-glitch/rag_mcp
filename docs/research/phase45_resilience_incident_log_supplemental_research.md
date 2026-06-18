# Phase 45 Resilience / Incident / Log 补证记录

## 补证目标

首轮审计中 P45-D-OPS02 与 P45-D-OPS03 被判定为 needs_more_evidence。本文件记录 degraded/read-only mode 与 failover/recovery/replay 边界补证。

## 新增内部契约

- `docs/contracts/phase45_resilience_incident_log_runtime_contract.md`：定义 runtime_mode、allowed/forbidden operations、read-only 写入禁用、replay boundary、owner boundary 和 machine gate。

## P45-D-OPS02 补证来源

| source_id | 来源 | 类型 | URL | 用途 |
| --- | --- | --- | --- | --- |
| `google_sre_handling_overload` | Google SRE Book: Handling Overload | `engineering_practice` | https://sre.google/sre-book/handling-overload/ | Google SRE describes graceful handling of overload, including serving degraded responses that are easier to compute and may rely on cached/local data. |
| `aws_graceful_degradation` | AWS Well-Architected: Implement graceful degradation | `cloud_architecture_doc` | https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_mitigate_interaction_failure_graceful_degradation.html | AWS Reliability guidance states graceful degradation maintains important functionality during failures by reducing functionality rather than failing completely. |
| `postgres_hot_standby` | PostgreSQL Documentation: Hot Standby | `official_database_doc` | https://www.postgresql.org/docs/current/hot-standby.html | PostgreSQL Hot Standby allows connections and read-only queries while a server is in archive recovery or standby mode. |
| `phase45_runtime_contract` | Phase 45 Resilience / Incident / Log Runtime Contract | `internal_contract` | docs/contracts/phase45_resilience_incident_log_runtime_contract.md | CEK-TA contract defines runtime_mode, allowed/forbidden operations, read_only write policy, replay boundary, owner boundary and machine gate. |

修补后 OPS02 claim：degraded/read_only/recovery/manual_intervention_required 必须声明 mode_reason、允许/禁止操作、数据新鲜度、写入禁用语义、人工接管、退出条件和 audit trace。read_only 下默认禁止 new_order、cancel_replace、live_order_replay_write、position_mutation 和 risk_threshold_change。

## P45-D-OPS03 补证来源

| source_id | 来源 | 类型 | URL | 用途 |
| --- | --- | --- | --- | --- |
| `fix_cancel_replace` | FIX 4.4 Order Cancel/Replace Request | `official_protocol_reference` | https://www.b2bits.com/fixopaedia/fixdic44/message_Order_Cancel_Replace_Request_G.html | FIX Cancel/Replace uses ClOrdID and OrigClOrdID and may be rejected when a request cannot be processed, supporting order identifier and cancel/replace boundaries. |
| `fix_order_cancel_reject` | FIX Latest OrderCancelReject | `official_protocol_doc` | https://fiximate.fixtrading.org/en/FIX.Latest/msg10.html | FIX OrderCancelReject includes ClOrdID and OrigClOrdID semantics for cancel/replace requests that could not be processed. |
| `binance_futures_new_order` | Binance USDⓈ-M Futures New Order | `official_exchange_api_doc` | https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api | Binance Futures New Order documents newClientOrderId as a unique id among open orders, supporting client order id boundaries in one venue/API context. |
| `ibkr_order_ids` | IBKR TWS API Documentation | `official_broker_doc` | https://www.interactivebrokers.com/campus/ibkr-api-page/trader-workstation-api/ | IBKR documentation states requests should use unique identifiers and the same order identifier cannot be reused except to modify an existing order. |
| `ibkr_modifying_orders` | IBKR TWS API: Modifying Orders | `official_broker_doc` | https://interactivebrokers.github.io/tws-api/modifying_orders.html | IBKR modifying-orders documentation explains that manual orders must be bound before API modification/cancellation and that API order IDs depend on session/client binding. |
| `phase45_runtime_contract` | Phase 45 Resilience / Incident / Log Runtime Contract | `internal_contract` | docs/contracts/phase45_resilience_incident_log_runtime_contract.md | CEK-TA contract defines runtime_mode, allowed/forbidden operations, read_only write policy, replay boundary, owner boundary and machine gate. |

修补后 OPS03 claim：replay 必须区分 audit_replay、simulation_replay、state_rebuild 和 live_order_action。没有订单真相源、client/venue/broker order id、idempotency_key、当前订单状态快照、Risk/Live Execution owner 审批和 audit_trace_id 时，不得通过 replay 自动重发、修改或撤销真实订单。

## 硬边界

```text
1. 补证不创建 formal reviewed。
2. 补证不创建 approved、default guidance 或 hard gate。
3. 不生成买卖点、仓位、杠杆、止损止盈、实盘执行建议、停机阈值或风险阈值。
4. 不触发自动拒单、自动撤单、自动重发订单、自动恢复交易。
5. 外部来源均保留 implementation / venue / broker / protocol caveat。
```
