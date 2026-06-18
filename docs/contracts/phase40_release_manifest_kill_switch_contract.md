# Phase 40 Release Manifest Kill Switch Contract

生成日期：2026-06-10
状态：contract draft
对应任务：CEK-TA-317

## 目标

本文定义交易 AI gating/scoring 发布清单中的 `secret_scan`、`rollback_drill_status`、`kill_switch_tested_at` 和回滚验证字段。

本契约补充：

```text
docs/contracts/phase40_champion_challenger_release_contract.md
docs/contracts/phase40_composite_release_artifact_contract.md
```

核心原则：

```text
发布清单必须能回答：发布了什么、谁批准、如何停、如何回滚、是否演练过。
kill switch 是发布控制，不是交易策略逻辑。
secret scan 是发布安全门禁，不得保存密钥正文。
rollback drill 是可恢复性证据，不等于自动上线许可。
```

## 上游输入

| 输入 | 来源 | 用途 |
| --- | --- | --- |
| `ReleaseManifest` | CEK-TA-302 | 发布对象、证据、范围和控制 |
| `RollbackPlan` | CEK-TA-302 | 回滚目标、触发器和恢复步骤 |
| `CompositeArtifactReleaseManifest` | CEK-TA-313 | 组合 artifact 版本绑定 |
| `HumanApprovalRecord` | CEK-TA-302 | 人工审批 |
| `SecurityPrivacyReview` | 外接项目/安全流程 | secret scan、权限和私有数据检查 |

## 下游输出

| 输出 | 消费者 |
| --- | --- |
| `ReleaseSafetyChecklist` | release review、Vue3 审计 |
| `KillSwitchPolicy` | 部署系统、incident response |
| `RollbackDrillRecord` | incident response、SearchLab |
| `SecretScanResult` | 安全审计、发布门禁 |

## ReleaseSafetyChecklist 契约

最小字段：

```yaml
release_safety_checklist_id: string
schema_version: phase40_release_safety_checklist_v1
created_at: iso8601
release_manifest_ref: string
composite_release_unit_ref: string | null

required_checks:
  rollback_target_present: true | false
  kill_switch_policy_present: true | false
  kill_switch_tested_at: iso8601 | null
  rollback_drill_status: pass | warning | fail | not_run
  secret_scan_status: pass | warning | fail | not_run
  human_approval_record_ref: string | null
  monitoring_plan_ref: string | null

decision:
  release_safety_status: pass | warning | block_release
  reason_codes: list[string]
```

硬门：

```text
rollback_target_present != true -> block_release
kill_switch_policy_present != true -> block_release
kill_switch_tested_at 缺失 -> block_release
rollback_drill_status=fail 或 not_run -> block_release
secret_scan_status=fail 或 not_run -> block_release
human_approval_record_ref 缺失 -> block_release
```

## KillSwitchPolicy 契约

最小字段：

```yaml
kill_switch_policy_id: string
schema_version: phase40_kill_switch_policy_v1
created_at: iso8601
policy_status: draft | reviewed | approved | retired

scope:
  release_manifest_ref: string
  affected_components: list[numeric_scorer | calibrator | threshold_policy | llm_prompt | rag_pack | llm_model | final_gate_policy]
  allowed_strategy_versions: list[string]
  allowed_symbols: list[string]

activation:
  manual_owner: string
  automated_triggers: list[string]
  activation_procedure_ref: string
  expected_effect: disable_candidate | revert_to_champion | freeze_final_gate | route_to_human_review

test:
  last_tested_at: iso8601 | null
  last_test_result: pass | fail | not_run
  test_evidence_ref: string | null
```

禁止：

```text
kill switch 直接下单。
kill switch 修改交易策略逻辑。
kill switch 由 LLM audit assistant 自动批准。
```

## RollbackDrillRecord 契约

最小字段：

```yaml
rollback_drill_record_id: string
schema_version: phase40_rollback_drill_record_v1
created_at: iso8601
release_manifest_ref: string
rollback_plan_ref: string
drill_status: pass | warning | fail
rollback_target_release_manifest_id: string
tested_components: list[string]
verification_checks:
  manifest_hash_restored: true | false
  prompt_or_rag_regression_passed: true | false | null
  threshold_policy_restored: true | false | null
  final_gate_policy_restored: true | false | null
  monitoring_signal_restored: true | false
owner: string
evidence_ref: string
```

## SecretScanResult 契约

最小字段：

```yaml
secret_scan_result_id: string
schema_version: phase40_secret_scan_result_v1
created_at: iso8601
release_manifest_ref: string
scanner: github_secret_scanning | custom_secret_scanner | external_security_review
scan_scope:
  code_version_hash: string
  prompt_registry_uri: string | null
  rag_index_uri: string | null
  config_refs: list[string]
result:
  status: pass | warning | fail
  alert_count: integer
  resolved_alert_refs: list[string]
  stores_secret_value: false
```

禁止：

```text
在 CEK-TA 知识库中保存密钥正文。
把扫描结果中的 token、账号、私有 URL 或交易密钥写入通用知识。
secret_scan fail 时继续 release。
```

## 与 MCP/SearchLab/Vue3 的关系

| 组件 | 使用方式 |
| --- | --- |
| MCP | 只读检索发布安全字段和阻断规则，不执行 kill switch |
| SearchLab | 验证缺少 rollback、kill switch、secret scan 时是否阻断 |
| Vue3 | 展示 release safety checklist、open gaps 和审计状态 |

## 与 Trading Engineering 的边界

本契约不定义订单撤单实现、交易所 API、实盘仓位同步和风控阈值本体。交易执行细节必须路由到 Trading Engineering 或外接项目事实层。

## DoD

```text
1. 已定义 ReleaseSafetyChecklist。
2. 已定义 KillSwitchPolicy。
3. 已定义 RollbackDrillRecord。
4. 已定义 SecretScanResult。
5. 已明确 secret scan 不保存密钥正文。
6. 已明确 kill switch 不执行交易策略逻辑。
7. 已明确缺少 rollback/kill switch/secret scan/审批必须阻断发布。
8. UTF-8 无乱码。
```
