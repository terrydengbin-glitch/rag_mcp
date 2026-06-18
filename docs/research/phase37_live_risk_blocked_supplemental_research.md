# Phase 37 Live/Risk L03/L10/L11 阻断项补证研究

生成日期：2026-06-12

## 任务目标

`CEK-TA-440` 只为 L03/L10/L11 补充内部契约和 schema extract，并导出 reviewed/caveat_only 再审包。

## 内部契约

- 契约路径：`docs/contracts/phase37_live_risk_reconciliation_exposure_loss_policy_contract.md`
- 契约 SHA256：`16b28ab273acb96d90b1bb05221fe3f85b3f5b37942aaa997b6d673d5559a892`
- schema_extract_id：`phase37_live_risk_reconciliation_exposure_loss_policy_schema_extract_v1`

## 补证对象

### P37-G-L03 / cand_20260612_phase37_live_risk_position_reconciliation_required_001

- schema object：`position_reconciliation`
- claim：实盘系统必须把本地订单、成交和仓位与 broker、exchange、account statement 或 clearing source 对账；发现差异时必须进入 reconciliation_required 或等价审计状态，而不是继续按未核验的本地状态下单。
- 补证重点：内联 position_reconciliation schema，定义 local_position_ref、broker_position_ref、account_statement_ref、discrepancy_type、mismatch_qty、mismatch_notional、stale_source、unknown_source、reconciliation_action、owner 和 audit_trace 字段。

### P37-G-L10 / cand_20260612_phase37_live_risk_portfolio_exposure_limit_required_001

- schema object：`portfolio_exposure_limit`
- claim：组合暴露治理必须定义账户、策略、品种、venue、相关资产、行业/主题、方向、gross/net exposure、价格源、聚合规则、stale pricing 处理、owner 和 audit trace；阈值只引用外接项目 policy，不由 CEK-TA 推荐。
- 补证重点：内联 portfolio_exposure_limit schema，定义 exposure taxonomy、aggregation_rule、price_source、gross/net/directional exposure、correlated_group、policy_threshold_ref、owner 和 audit_trace 字段。

### P37-G-L11 / cand_20260612_phase37_live_risk_consecutive_loss_stop_required_001

- schema object：`consecutive_loss_stop_policy`
- claim：若交易系统使用连续亏损停止规则，必须定义亏损事件口径、时间窗口政策引用、计数来源、重置条件、冻结动作、人工复核、解锁流程，以及与单笔风险、日亏损和组合暴露规则的优先级；不得写入 CEK-TA 推荐阈值。
- 补证重点：内联 consecutive_loss_stop_policy schema，定义 loss_event_basis、time_window_policy_ref、streak_count_source、reset_condition、freeze_action、manual_review_required、unlock_process_ref、priority_order_ref 和 audit_trace 字段。

## 审计边界

```text
1. candidate 不是正式知识。
2. 本包最多允许 accepted_for_reviewed_caveat_only。
3. 不允许 approved。
4. 不允许 default guidance。
5. 不允许 hard gate。
6. 不允许风险阈值建议。
7. 不允许生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。
```

## 来源使用边界

外部监管、broker、venue 和 platform 文档只用于说明原则和实现模式；CEK-TA exact field、owner mapping、workflow gate 由内部契约支撑。
