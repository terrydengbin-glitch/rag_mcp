# Phase 37 Data Engineering 候选研究记录

生成日期：2026-06-11

## 范围

本文件记录 Phase 37 `P37-B` Data Engineering 12 条候选知识的来源选择、分类和边界。所有条目仍是 candidate，不是 formal reviewed，不是 approved，不进入默认指导。

## 来源原则

```text
1. 优先使用数据供应商官方文档、数据库官方文档、数据质量框架、特征存储文档、交易所/指数/参考数据资料。
2. vendor/framework 文档只能支撑通用工程边界，不能替代外接项目自己的数据契约。
3. 时间戳、时区、schema、缺失、重复、异常值、版本、复权/换月必须写明适用边界和不适用场景。
4. 不输出买卖点、仓位、杠杆、止损止盈或实盘执行建议。
```

## 候选清单

| 任务 | 候选 | 子域 | 来源数 | 主来源数 | 状态 |
| --- | --- | --- | ---: | ---: | --- |
| P37-B-D01 | `kb_02_data_engineering.timestamp_alignment_required.v1` | timestamp_alignment | 4 | 3 | candidate_ready |
| P37-B-D02 | `kb_02_data_engineering.timezone_policy_required.v1` | timezone_policy | 4 | 3 | candidate_ready |
| P37-B-D03 | `kb_02_data_engineering.missing_bar_detection_required.v1` | data_quality | 4 | 3 | candidate_ready |
| P37-B-D04 | `kb_02_data_engineering.duplicate_event_detection_required.v1` | data_quality | 4 | 4 | candidate_ready |
| P37-B-D05 | `kb_02_data_engineering.ohlcv_schema_required.v1` | ohlcv_schema | 4 | 4 | candidate_ready |
| P37-B-D06 | `kb_02_data_engineering.feature_timestamp_required.v1` | feature_timestamp | 4 | 3 | candidate_ready |
| P37-B-D07 | `kb_02_data_engineering.data_versioning_required.v1` | data_versioning | 4 | 1 | candidate_ready |
| P37-B-D08 | `kb_02_data_engineering.symbol_contract_normalization_required.v1` | symbology | 4 | 4 | candidate_ready |
| P37-B-D09 | `kb_02_data_engineering.corporate_action_or_contract_rollover_policy.v1` | adjustment_rollover | 4 | 3 | candidate_ready |
| P37-B-D10 | `kb_02_data_engineering.outlier_detection_required.v1` | data_quality | 4 | 3 | candidate_ready |
| P37-B-D11 | `kb_02_data_engineering.raw_vs_adjusted_data_boundary.v1` | raw_adjusted_boundary | 4 | 3 | candidate_ready |
| P37-B-D12 | `kb_02_data_engineering.data_quality_report_required.v1` | data_quality_report | 4 | 2 | candidate_ready |

## 下游

```text
docs/audit/phase37_data_engineering_candidate_audit_package_20260611.json
```
