# Phase 37 Backtest B10/B11/B12 Reviewed 阻断项补证研究

生成时间：2026-06-11

## 补证目标

B10/B11/B12 在 reviewed-preparation 审计中被判定为 `needs_more_evidence`。本轮补证使用 CEK-TA 内部 `backtest_run_manifest` 契约作为字段本体主来源，并用外部工具/平台文档作为实现语义示例。

## 补证边界

```text
不得 approved。
不得 default guidance。
不得 hard gate。
不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。
```

## 候选与来源

### P37-E-B10 / cand_20260611_phase37_backtest_profit_factor_drawdown_context_required_001

Profit factor、收益回撤比或类似汇总指标不能单独证明策略质量；必须同时报告 drawdown、交易次数、样本覆盖、成本、尾部亏损和参数选择过程。

- Phase 37 Backtest Run Manifest Contract：docs/contracts/phase37_backtest_run_manifest_contract.md，作用：定义 profit_factor、max_drawdown、return_over_max_drawdown 的 CEK-TA 内部 metric_report 字段和解释边界。
- Backtest Statistics：https://www.quantconnect.com/docs/v2/cloud-platform/api-reference/backtest-management/read-backtest/backtest-statistics，作用：列出 backtest statistics、drawdown、fees 等字段语义，可作为回测指标报告实现示例。
- What is Profit Factor：https://research.titanfx.com/glossary/what-is-profit-factor，作用：给出 profit factor 的定义、用途和局限，可作为 supporting source；不得单独支撑 reviewed。

### P37-E-B11 / cand_20260611_phase37_backtest_reproducibility_package_required_001

可用于审计的 backtest 必须保存代码版本、数据版本、参数、运行环境、随机种子、依赖、输出指标、日志和 artifact；缺失复现实验包时不得作为正式证据。

- Phase 37 Backtest Run Manifest Contract：docs/contracts/phase37_backtest_run_manifest_contract.md，作用：定义 reproducibility_package 必填字段，包括 code_commit、dependency lockfile、config hash、input/output artifacts、日志、lineage 和 replay job。
- MLflow Tracking：https://mlflow.org/docs/latest/ml/tracking/，作用：MLflow Tracking 支撑记录参数、代码版本、指标和输出文件。
- Get Started: Data Pipelines：https://doc.dvc.org/start/data-pipelines/data-pipelines，作用：DVC pipelines 支撑 versioned pipeline、dependencies、outputs 和 reproducible workflows。

### P37-E-B12 / cand_20260611_phase37_backtest_strategy_version_and_data_version_required_001

Backtest 结果必须绑定 strategy_rule_version、parameter_hash、data_version、calendar/session version、cost/fill model version 和 evaluation timestamp，不能只保存最终指标。

- Phase 37 Backtest Run Manifest Contract：docs/contracts/phase37_backtest_run_manifest_contract.md，作用：定义 strategy_rule_version、parameter_hash、dataset_version、calendar/session version、cost/fill/slippage/fee model version 等回测证据包字段。
- MLflow Dataset Tracking：https://mlflow.org/docs/latest/ml/dataset/，作用：MLflow Dataset Tracking 支撑 dataset、model、metrics 和 evaluation artifacts 的 tracking/versioning。
- MLflow Model Registry：https://mlflow.org/docs/latest/ml/model-registry/，作用：MLflow registry 支撑 model version、run linkage、lineage 和 rollback 语义，可作为版本追踪 supporting source。

