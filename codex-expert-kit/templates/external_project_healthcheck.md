# CEK-TA External Project Healthcheck

Use this checklist inside a business project after adding CEK-TA `AGENTS.md`, `project_adapter.md`, and optional MCP configuration.

The healthcheck does not grant permissions. It only reports whether the project can safely consume CEK-TA knowledge and prepare sanitized contributions.

## Healthcheck Identity

```yaml
healthcheck_id: EPH-YYYYMMDD-001
project_id: ""
project_name: ""
adapter_ref: docs/project_adapter.md
checked_at: YYYY-MM-DD
checked_by: codex | human | mixed
result: not_run | pass | warn | fail
```

## Required Inputs

```yaml
required_files:
  agents_md: AGENTS.md
  project_adapter: docs/project_adapter.md
  project_overview: docs/project_overview.md
  current_pipeline: docs/current_pipeline.md
  current_config: docs/current_config.md
  data_schema: docs/data_schema.md
  reason_codes: docs/reason_codes.md
  runbook: docs/runbook.md
  risk_limits: docs/risk_limits.md
optional_files:
  recent_audit: docs/recent_audit.md
  codex_config: .codex/config.toml
```

## Check 1: CEK-TA Path

```yaml
cek_ta_path_declared: false
cek_ta_path_exists: false
required_cek_ta_files_exist:
  - AGENTS.md
  - docs/index_tasks.md
  - codex-expert-kit/core/AGENTS.md
result: pass | warn | fail
notes:
  - ""
```

## Check 2: Project Fact Boundary

```yaml
project_facts_declared: false
missing_project_fact_files:
  - ""
project_private_fields_declared: false
project_facts_override_general_knowledge: true
result: pass | warn | fail
notes:
  - ""
```

Pass criteria:

```text
1. Project facts are stored in the business project.
2. CEK-TA stores reusable knowledge only.
3. Missing project fact files are listed before implementation starts.
```

## Check 3: Runtime Modes

```yaml
runtime_modes_declared: false
enabled_modes:
  - ""
unsupported_modes:
  - ""
live_enabled: false
live_human_approval_required: true
result: pass | warn | fail
notes:
  - ""
```

Fail if:

```text
live is enabled without explicit human approval
runtime mode is used without command or runbook
```

## Check 4: Field Mapping

```yaml
market_event_mapping_complete: false
signal_frame_mapping_complete: false
order_intent_mapping_complete: false
execution_report_mapping_complete: false
trade_result_mapping_complete: false
missing_fields:
  - ""
result: pass | warn | fail
notes:
  - ""
```

## Check 5: CEK-TA Tool Permissions

```yaml
allowed_tools:
  - search_expert_knowledge
  - get_knowledge_item
  - get_conflict_audit
  - get_source_profile
  - list_kb_partitions
blocked_tools:
  - submit_knowledge_contribution
  - approve_knowledge_item
  - write_approved_knowledge
  - read_project_secrets
  - read_account_data
  - place_order
permission_profile: read_only
result: pass | warn | fail
notes:
  - ""
```

Fail if:

```text
CEK-TA can read secrets
CEK-TA can read account data
CEK-TA can place orders
CEK-TA can approve knowledge
CEK-TA can write approved knowledge
```

## Check 6: Knowledge Query Scope

```yaml
allowed_domains_declared: false
include_sources: true
include_conflict_audit: true
require_applicability_boundary: true
reject_unreviewed_knowledge: true
result: pass | warn | fail
notes:
  - ""
```

## Check 7: MCP Configuration

```yaml
mcp_config_present: false
mcp_enabled: false
mcp_server_path: ""
mcp_server_path_exists: false
mcp_read_only_tools_only: true
result: pass | warn | fail | not_applicable
notes:
  - ""
```

Pass criteria:

```text
MCP is optional.
If enabled, it must point to CEK-TA server.py after Phase 14 is complete.
Until Phase 14, MCP config should remain disabled or treated as draft.
```

## Check 8: Contribution Readiness

```yaml
contribution_allowed: false
contribution_template_exists: false
target_queue_declared: false
initial_status_is_proposed: true
direct_approved_write_allowed: false
sanitization_required: true
source_required: true
conflict_check_required: true
result: pass | warn | fail
notes:
  - ""
```

Fail if:

```text
contribution can skip proposed
contribution can write directly into approved knowledge
sanitization is optional
source is optional
conflict check is optional
```

## Check 9: Validation And Rollback

```yaml
test_command_declared: false
backtest_command_declared: false
validation_metrics_declared: false
rollback_plan_declared: false
result: pass | warn | fail
notes:
  - ""
```

## Final Output

```yaml
adapter_status: pass | warn | fail
missing_fields:
  - ""
unsupported_modes:
  - ""
allowed_tools:
  - ""
blocked_tools:
  - ""
project_fact_boundary: "clear | unclear"
knowledge_query_scope: "clear | unclear"
contribution_entrypoint: ""
healthcheck_result: pass | warn | fail
next_actions:
  - ""
```

## Result Rules

```text
pass: All required checks pass. MCP can still be disabled if Phase 14 is not ready.
warn: Missing optional files or incomplete non-live mode details.
fail: Secret/account/live/approved-write boundary is broken, or project facts are missing.
```
