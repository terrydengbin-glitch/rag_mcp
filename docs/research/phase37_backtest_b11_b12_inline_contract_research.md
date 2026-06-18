# Phase 37 Backtest B11/B12 内联契约补证记录

生成日期：2026-06-11

## 任务

`CEK-TA-422` 只处理：

```text
P37-E-B11 backtest.reproducibility_package_required
P37-E-B12 backtest.strategy_version_and_data_version_required
```

上一轮审计认为 B11/B12 的外部来源足以支持 MLflow/DVC 等实验追踪模式，但不足以支持 CEK-TA 内部字段本体，因为 `backtest_run_manifest_contract.md` 只被路径引用，没有内联正文、字段表、schema extract 或 hash。

## 本轮补丁

```text
contract_path: docs/contracts/phase37_backtest_run_manifest_contract.md
schema_extract_path: docs/contracts/phase37_backtest_run_manifest_schema_extract.json
contract_sha256: 6698c0b2ec18dc12ebd85f46ace4c021c6b6d84e162ff45773c9a9e253289574
schema_extract_id: phase37_backtest_run_manifest_schema_extract_v1
```

## 字段范围

本轮重点内联：

```text
reproducibility_package:
  code_repository, code_commit, dependency_lockfile_hash, container_image_digest,
  random_seed, config_file_hash, input_artifact_ids, output_artifact_ids,
  log_artifact_id, metric_report_id, lineage_id, replay_command_or_ci_job_id,
  known_non_determinism

strategy_identity:
  strategy_rule_version, strategy_code_commit, parameter_hash, signal_schema_version,
  decision_policy_version

data_identity:
  dataset_version, source_dataset_version, symbol_universe_version,
  corporate_action_version, adjustment_policy_id, data_quality_report_id,
  available_time_policy_id

market_calendar_identity:
  calendar_version, session_template_version, holiday_calendar_version,
  early_close_calendar_version

execution_assumption_identity:
  cost_model_version, fee_model_version, slippage_model_version,
  spread_model_version, fill_model_version, order_type_policy_id,
  liquidity_assumption_id
```

## 审计边界

```text
1. candidate 不是 formal knowledge。
2. 本包最多允许 accepted_for_reviewed_caveat_only。
3. 不允许 approved。
4. 不允许 default guidance。
5. 不允许 hard gate。
6. 不允许生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。
```
