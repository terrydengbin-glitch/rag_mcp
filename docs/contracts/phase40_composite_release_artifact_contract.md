# Phase 40 Composite Release Artifact Contract

生成日期：2026-06-10
状态：contract draft
对应任务：CEK-TA-313

## 目标

本文定义交易 AI gating/scoring 发布中的组合发布单元和组合回滚目标。它补充 `phase40_champion_challenger_release_contract.md`，用于约束模型、prompt、RAG 索引、校准器、阈值策略和 final gate policy 的版本绑定。

核心原则：

```text
组合发布必须有 manifest。
组合回滚必须能恢复到明确的上一组 artifact。
模型回滚不等于 prompt/RAG/threshold 已回滚。
阈值和 final gate policy 仍受确定性 owner 审批约束。
```

## 上游输入

| 输入 | 来源 | 用途 |
| --- | --- | --- |
| `ReleaseManifest` | `phase40_champion_challenger_release_contract.md` | 记录发布对象和证据 |
| `RollbackPlan` | `phase40_champion_challenger_release_contract.md` | 定义回滚触发和步骤 |
| `PromptRegressionReport` | Phase 38 / 外接项目 | 证明 prompt 变更不破坏 schema、citation、reason code |
| `RagRegressionReport` | Phase 38 / 外接项目 | 证明 RAG 索引变更不破坏检索命中和来源引用 |
| `ThresholdStabilityReport` | Phase 40 | 证明阈值策略稳定性 |

## 下游输出

| 输出 | 消费者 |
| --- | --- |
| `CompositeReleaseUnit` | release review、MCP、SearchLab、Vue3 审计 |
| `CompositeArtifactReleaseManifest` | 部署系统、审计、回滚治理 |
| `CompositeRollbackTarget` | incident response、kill switch、发布回滚 |

## CompositeReleaseUnit 契约

最小字段：

```yaml
composite_release_unit_id: string
schema_version: phase40_composite_release_unit_v1
created_at: iso8601
release_unit_status: draft | reviewed | approved_for_canary | deployed | frozen | rolled_back | rejected

components:
  numeric_model_version: string | null
  calibrator_version: string | null
  threshold_policy_version: string | null
  prompt_version: string | null
  rag_index_version: string | null
  rag_snapshot_hash: string | null
  llm_model_version: string | null
  final_gate_policy_version: string | null
  code_version_hash: string

evidence_refs:
  champion_challenger_review_ref: string
  prompt_regression_report_ref: string | null
  rag_regression_report_ref: string | null
  threshold_stability_report_ref: string | null
  shadow_paper_canary_report_refs: list[string]
  human_approval_record_ref: string | null

scope:
  allowed_strategy_versions: list[string]
  allowed_symbols: list[string]
  allowed_market_regimes: list[string]
  deployment_stage: shadow | paper | soft_gate | canary | production
```

硬门：

```text
缺少 code_version_hash -> block_release
release_unit_status=deployed 且缺少 human_approval_record_ref -> block_release
包含 prompt_version 但缺少 prompt_regression_report_ref -> block_release
包含 rag_index_version 但缺少 rag_regression_report_ref -> block_release
包含 threshold_policy_version 但缺少 threshold_stability_report_ref -> block_release
deployment_stage=production 且没有 rollback target -> block_release
```

## CompositeArtifactReleaseManifest 契约

最小字段：

```yaml
composite_artifact_release_manifest_id: string
schema_version: phase40_composite_artifact_release_manifest_v1
created_at: iso8601
composite_release_unit_ref: string
manifest_hash: string
artifact_storage_refs:
  model_artifact_uri: string | null
  calibrator_artifact_uri: string | null
  prompt_registry_uri: string | null
  rag_index_uri: string | null
  threshold_policy_uri: string | null
  final_gate_policy_uri: string | null
rollback:
  composite_rollback_target_ref: string
  kill_switch_policy_ref: string
  rollback_owner: string
```

## CompositeRollbackTarget 契约

最小字段：

```yaml
composite_rollback_target_id: string
schema_version: phase40_composite_rollback_target_v1
created_at: iso8601
current_release_unit_ref: string
target_release_unit_ref: string
rollback_components:
  numeric_model: true | false
  calibrator: true | false
  threshold_policy: true | false
  prompt: true | false
  rag_index: true | false
  llm_model: true | false
  final_gate_policy: true | false
verification_checks:
  manifest_hash_match: true | false
  prompt_regression_restored: true | false | null
  rag_index_restored: true | false | null
  threshold_policy_restored: true | false | null
  final_gate_policy_restored: true | false | null
```

回滚后要求：

```text
冻结 current_release_unit_ref。
记录 incident 或 rollback audit trace。
重跑 RAG/prompt/schema/threshold 最小回归检查。
禁止只回滚模型却继续使用事故版本 prompt、RAG 索引或阈值策略。
```

## 与 MCP/SearchLab/Vue3 的关系

| 组件 | 使用方式 |
| --- | --- |
| MCP | 只读返回组合发布单元、组件版本和回滚边界，不执行发布或回滚 |
| SearchLab | 验证“缺少 manifest/rollback target 是否阻断” |
| Vue3 | 展示发布单元的组件、证据、状态、回滚目标和缺口 |

## DoD

```text
1. 已定义 CompositeReleaseUnit。
2. 已定义 CompositeArtifactReleaseManifest。
3. 已定义 CompositeRollbackTarget。
4. 已明确 prompt/RAG/threshold/model 必须组合追踪。
5. 已明确回滚不是只回滚模型。
6. 已明确 final gate policy 仍需 owner 审批。
7. UTF-8 无乱码。
```
