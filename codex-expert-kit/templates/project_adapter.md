# CEK-TA Project Adapter Template

Use this template inside a business project to map project-specific facts, runtime modes, field names, risk boundaries, and CEK-TA tool permissions to reusable CEK-TA contracts.

The adapter belongs to the business project. Do not store raw project-private facts in CEK-TA. When a project contributes knowledge back to CEK-TA, only sanitized and generalized content can enter the contribution queue.

## Adapter Identity

```yaml
project_id: ""
adapter_id: ""
adapter_version: 0.1.0
project_name: ""
project_type: "kline_trend_strategy | abnormal_move_strategy | high_fidelity_simulator | live_binance_futures | trading_llm_assistant | custom"
market: "crypto | futures | spot | stock | general"
asset_classes:
  - ""
owner: ""
updated_at: YYYY-MM-DD
```

## CEK-TA Reference

```yaml
cek_ta_path: "E:\\collector\\rag"
cek_ta_version: "local"
enabled_domains:
  - quant_trading
  - kline_strategy
  - backtest_replay_simulation
  - trade_analysis
enabled_skills:
  - strategy-auditor
  - backtest-reviewer
  - trade-quality-analyst
```

## Runtime Modes

Declare every mode the project supports. Keep `live` disabled unless the business project has its own approval process.

```yaml
runtime_modes:
  research:
    enabled: true
    command: ""
  backtest:
    enabled: true
    command: ""
  replay:
    enabled: false
    command: ""
  simulation:
    enabled: false
    command: ""
  paper:
    enabled: false
    command: ""
  live:
    enabled: false
    command: ""
    requires_human_approval: true
```

## Project Fact Sources

```yaml
project_facts:
  overview: docs/project_overview.md
  pipeline: docs/current_pipeline.md
  config: docs/current_config.md
  data_schema: docs/data_schema.md
  reason_codes: docs/reason_codes.md
  runbook: docs/runbook.md
  risk_limits: docs/risk_limits.md
  recent_audit: docs/recent_audit.md
```

Rules:

```text
1. Project facts stay in the business project.
2. Project facts override CEK-TA general knowledge for that project only.
3. Missing project facts must be reported as adapter gaps.
4. Project private fields must never be promoted to CEK-TA reusable knowledge.
```

## Field Mapping

Map project-specific fields to CEK-TA contracts:

```yaml
market_event:
  project_symbol_field: ""
  project_timestamp_field: ""
  project_timeframe_field: ""
  project_open_field: ""
  project_high_field: ""
  project_low_field: ""
  project_close_field: ""
  project_volume_field: ""

signal_frame:
  project_signal_id_field: ""
  project_direction_field: ""
  project_strength_field: ""
  project_reason_codes_field: ""

order_intent:
  project_intent_id_field: ""
  project_side_field: ""
  project_qty_field: ""
  project_order_type_field: ""
  project_stop_loss_field: ""
  project_take_profit_field: ""

execution_report:
  project_order_id_field: ""
  project_fill_id_field: ""
  project_fill_price_field: ""
  project_fee_field: ""
  project_order_state_field: ""

trade_result:
  project_trade_id_field: ""
  project_net_pnl_field: ""
  project_realized_r_field: ""
  project_mae_field: ""
  project_mfe_field: ""
  project_exit_reason_field: ""
```

## Data Source Contract

```yaml
data_sources:
  market_data:
    provider: ""
    storage: ""
    schema_ref: docs/data_schema.md
    freshness: ""
    known_gaps:
      - ""
  order_events:
    provider: ""
    storage: "project local only"
    schema_ref: ""
    contains_private_data: true
  account_events:
    provider: ""
    storage: "project local only"
    schema_ref: ""
    contains_private_data: true
```

## Reason Code Mapping

```yaml
reason_codes:
  project_code: generic_cek_ta_code
examples:
  "TREND_UP_FILTER": "direction.trend_up"
  "ENTRY_BREAKOUT": "entry.breakout"
  "RISK_DAILY_LOSS": "risk.daily_loss_limit"
```

Rules:

```text
1. Keep project private codes in the project.
2. Map to generic CEK-TA codes only when contributing or auditing.
3. Do not invent generic codes without documenting meaning.
```

## Run Commands

```yaml
commands:
  test: ""
  lint: ""
  backtest: ""
  replay: ""
  simulation: ""
  audit_report: ""
```

## CEK-TA Tool Permission Profile

Default profile is read-only. Do not enable write-like tools unless the CEK-TA task card explicitly allows them.

```yaml
allowed_cek_ta_tools:
  - search_expert_knowledge
  - get_knowledge_item
  - get_conflict_audit
  - get_source_profile
  - list_kb_partitions
blocked_cek_ta_tools:
  - submit_knowledge_contribution
  - approve_knowledge_item
  - write_approved_knowledge
  - read_project_secrets
  - read_account_data
  - place_order
  - modify_live_risk
tool_policy:
  default_permission: read_only
  contribution_submission: file_template_only
  approval_allowed: false
  secrets_allowed: false
  account_data_allowed: false
```

## Knowledge Query Scope

```yaml
knowledge_query_scope:
  allowed_domains:
    - quant_trading
    - kline_strategy
    - backtest_replay_simulation
    - trade_analysis
  allowed_markets:
    - ""
  allowed_runtime_modes:
    - research
    - backtest
  include_conflict_audit: true
  include_sources: true
  require_applicability_boundary: true
  reject_unreviewed_knowledge: true
```

## Validation Metrics

```yaml
metrics:
  strategy:
    - win_rate
    - average_r
    - profit_factor
    - max_drawdown
    - cost_impact
  execution:
    - fill_rate
    - partial_fill_rate
    - average_slippage
  trade_analysis:
    - bad_case_rate_by_label
    - tp_reach_rate
    - noise_stop_rate
```

## Risk Boundaries

```yaml
risk_scope:
  max_position_mode: "project_defined | not_applicable"
  max_daily_loss_mode: "project_defined | not_applicable"
  leverage_policy: "project_defined | not_applicable"
  human_approval_required_for_live: true
live_trading_enabled: false
requires_human_approval_for_live: true
secrets_location: "never expose to CEK-TA"
account_data_policy: "project local only"
raw_order_policy: "project local only"
private_fields:
  - api_key
  - secret
  - token
  - account_id
  - raw_order_id
  - customer_id
```

## Rollback Plan

```text
1. Restore previous strategy version:
2. Restore previous config:
3. Disable adapter:
4. Stop live/paper execution:
5. Rerun validation:
```

## Knowledge Contribution Policy

```yaml
contribution_allowed: true
contribution_entrypoint: "<cek_ta_path>/contributions/proposed/"
contribution_template: "<cek_ta_path>/codex-expert-kit/templates/contribution_from_project.md"
requires_sanitization: true
requires_source: true
requires_conflict_check: true
target_queue: "<cek_ta_path>/contributions/"
initial_status: proposed
direct_approved_write_allowed: false
```

Contribution checklist:

```text
1. Remove secrets and account data.
2. Replace project fields with generic concepts.
3. Preserve evidence and applicability.
4. Check conflict with CEK-TA.
5. Submit as proposed, not approved.
```

## Adapter Acceptance Checklist

```text
1. project_id, project_name, project_type, market, and asset_classes are documented.
2. Runtime modes are explicit and live is disabled unless the project has human approval.
3. Project facts are documented and missing facts are visible.
4. Field mapping covers MarketEvent, SignalFrame, OrderIntent, ExecutionReport, TradeResult.
5. Data sources declare storage, schema, freshness, and private-data risk.
6. Run commands are current.
7. Validation metrics are explicit.
8. Tool permission profile blocks secrets, account data, live trading, and approved knowledge writes.
9. Knowledge query scope requires sources, conflicts, and applicability boundaries.
10. Rollback path exists.
11. Contribution policy starts at proposed and direct approved writes are false.
```

## Adapter Runtime Output

Codex or a healthcheck script should be able to summarize this adapter as:

```yaml
adapter_status: pass | warn | fail
missing_fields:
  - ""
unsupported_modes:
  - ""
allowed_tools:
  - search_expert_knowledge
blocked_tools:
  - place_order
project_fact_boundary:
  project_facts_location: "business_project"
  cek_ta_general_knowledge_location: "CEK-TA"
  private_fields_policy: "never contribute raw private fields"
knowledge_query_scope:
  domains:
    - ""
  include_sources: true
  include_conflict_audit: true
contribution_entrypoint: "<cek_ta_path>/contributions/proposed/"
healthcheck_result: "not_run | pass | warn | fail"
```
