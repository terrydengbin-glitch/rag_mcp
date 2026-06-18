# Phase 37 Backtest Run Manifest Contract

## 目标

本契约定义 CEK-TA 内部用于支撑 Backtest formal reviewed/caveat_only 知识的 `backtest_run_manifest` 和 `reproducibility_package` 字段。它只用于回测证据审计、复现、版本追踪和指标解释，不用于生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。

## 适用范围

```text
适用于：
- 回测结果是否可作为研究证据的审计。
- 回测运行复现包、策略版本、数据版本、参数和成本/fill 假设追踪。
- profit factor、drawdown、收益回撤比等指标的上下文解释。
- 外接项目将自身 backtest engine 结果映射到 CEK-TA RAG 知识库。

不适用于：
- 实盘下单、拒单、停机、自动风控 hard gate。
- 策略盈利保证。
- 替代交易所、broker、数据供应商或项目事实层。
- 默认 approved guidance。
```

## 逻辑对象

```text
BacktestRunManifest:
  run_identity
  strategy_identity
  data_identity
  market_calendar_identity
  execution_assumption_identity
  sample_split
  optimization_protocol
  metric_report
  reproducibility_package
  audit_trace
```

## 必填字段

### run_identity

```json
{
  "backtest_run_id": "string",
  "created_at": "ISO-8601 timestamp",
  "created_by": "human | system | ci",
  "project_id": "string",
  "environment": "research | validation | paper_precheck",
  "engine_name": "string",
  "engine_version": "string",
  "engine_config_hash": "string"
}
```

### strategy_identity

```json
{
  "strategy_id": "string",
  "strategy_rule_version": "string",
  "strategy_code_commit": "string",
  "parameter_set_id": "string",
  "parameter_hash": "string",
  "signal_schema_version": "string",
  "decision_policy_version": "string"
}
```

### data_identity

```json
{
  "dataset_id": "string",
  "dataset_version": "string",
  "source_dataset_version": "string",
  "symbol_universe_version": "string",
  "corporate_action_version": "string",
  "adjustment_policy_id": "string",
  "data_quality_report_id": "string",
  "available_time_policy_id": "string"
}
```

### market_calendar_identity

```json
{
  "market": "string",
  "venue": "string",
  "timezone": "IANA timezone",
  "calendar_version": "string",
  "session_template_version": "string",
  "holiday_calendar_version": "string",
  "early_close_calendar_version": "string"
}
```

### execution_assumption_identity

```json
{
  "cost_model_version": "string",
  "fee_model_version": "string",
  "slippage_model_version": "string",
  "spread_model_version": "string",
  "fill_model_version": "string",
  "order_type_policy_id": "string",
  "liquidity_assumption_id": "string"
}
```

### sample_split

```json
{
  "train_window": "time range or null",
  "validation_window": "time range or null",
  "test_window": "time range",
  "out_of_sample_window": "time range",
  "walk_forward_schedule_id": "string or null",
  "decision_timestamp_policy": "string",
  "feature_available_time_policy": "string"
}
```

### optimization_protocol

```json
{
  "parameter_search_id": "string or null",
  "search_space_hash": "string or null",
  "selection_metric": "string or null",
  "final_evaluation_run_id": "string",
  "search_and_final_eval_separated": true
}
```

## metric_report 字段契约

`metric_report` 必须区分 gross / net / research / validation 结果。所有指标都必须绑定样本窗口、成本假设和交易数量。

```json
{
  "metric_report_id": "string",
  "metric_schema_version": "string",
  "gross_metrics": {},
  "net_metrics": {},
  "research_metrics": {},
  "validation_metrics": {},
  "trade_count": 0,
  "gross_profit": 0.0,
  "gross_loss_abs": 0.0,
  "net_profit": 0.0,
  "profit_factor": 0.0,
  "max_drawdown": 0.0,
  "max_drawdown_pct": 0.0,
  "return_over_max_drawdown": 0.0,
  "win_rate": 0.0,
  "average_win": 0.0,
  "average_loss_abs": 0.0,
  "turnover": 0.0,
  "fees": 0.0,
  "estimated_slippage": 0.0,
  "metric_limitations": []
}
```

### 指标定义

```text
profit_factor:
  gross_profit / gross_loss_abs。
  gross_loss_abs 必须取亏损绝对值。
  如果 gross_loss_abs = 0，必须标记 undefined_or_infinite，不得静默写成极大优势。

max_drawdown:
  equity curve 从历史峰值到后续低点的最大回撤。
  必须说明使用 gross equity、net equity、closed equity 还是 mark-to-market equity。

return_over_max_drawdown:
  net_profit 或年化收益除以 max_drawdown 的比值。
  必须说明分子定义、分母定义、样本窗口和成本处理。
```

### 指标解释边界

```text
1. profit factor 不能单独证明策略质量。
2. drawdown 不能只看百分比，还要结合持续时间、恢复时间、样本窗口和成本。
3. return_over_max_drawdown 不能替代样本外验证、walk-forward、交易次数、尾部风险和执行成本审计。
4. 所有指标必须同时给出 gross 和 net 口径，且默认解释以 net 口径为优先。
5. 指标优秀不等于实盘许可。
```

## reproducibility_package

```json
{
  "package_id": "string",
  "code_repository": "string",
  "code_commit": "string",
  "dependency_lockfile_hash": "string",
  "container_image_digest": "string or null",
  "random_seed": "integer or null",
  "config_file_hash": "string",
  "input_artifact_ids": [],
  "output_artifact_ids": [],
  "log_artifact_id": "string",
  "metric_report_id": "string",
  "lineage_id": "string",
  "replay_command_or_ci_job_id": "string",
  "known_non_determinism": []
}
```

## audit_trace

```json
{
  "source_refs": [],
  "review_status": "candidate | accepted_for_draft | reviewed | approved",
  "approved_allowed": false,
  "default_guidance_allowed": false,
  "hard_gate_allowed": false,
  "reviewed_preparation_audit_result_id": "string",
  "patch_notes": [],
  "conflict_status": "none_known_in_visible_context | none | resolved | potential | confirmed"
}
```

## MCP/RAG 使用边界

```text
MCP/SearchLab 可以检索本契约来解释回测证据包应包含哪些字段。
MCP/SearchLab 不得据此创建订单、仓位、杠杆、止损止盈或实盘执行建议。
formal reviewed/caveat_only 可被检索用于审计提醒，但不得进入 default guidance queue。
approved 只能由后续人工治理任务另行决定。
```

## 与外部工具的关系

```text
MLflow、DVC、QuantConnect、Zipline、Backtrader、vectorbt 等工具可以作为等价实现来源或映射对象。
本契约不要求外接项目必须使用某个工具。
外接项目必须把自己的物理字段映射到 CEK-TA logical fields。
```

## DoD

```text
1. 回测结果可追踪到策略版本、数据版本、成本模型、fill model 和样本窗口。
2. 指标报告同时区分 gross/net/research/validation 口径。
3. 复现包包含代码、依赖、配置、输入、输出、日志和 lineage。
4. 所有 reviewed/caveat_only 知识保留 approved/default/hard gate 禁用状态。
```
