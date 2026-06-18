# Phase 37 Data Engineering D10/D11 补证研究记录

生成日期：2026-06-11

## 范围

本文件只记录 `P37-B-D10` 与 `P37-B-D11` reviewed-preparation 阻断项的补证。它不创建 formal reviewed、不创建 approved、不进入默认指导，也不改变 MCP/SearchLab 正式知识索引。

## 补证清单

| 任务 | 候选 | 补证重点 | 来源数 |
| --- | --- | --- | ---: |
| P37-B-D10 | `cand_20260611_phase37_data_engineering_outlier_detection_required_001` | 将 outlier 明确限定为需要标记、隔离、解释、保留或修复的审计对象，不能等同于自动删除。；补充 market-data cleaning、trade correction、trade reporting、market data flags 和 order book event 来源。；保留 candidate-only 边界；外部二审前不得 formal reviewed、approved、default guidance 或 hard gate。 | 8 |
| P37-B-D11 | `cand_20260611_phase37_data_engineering_raw_vs_adjusted_data_boundary_001` | 明确 raw、cleaned、adjusted、feature-ready、label-ready 是 CEK-TA 数据契约层名。；补充 medallion architecture、feature store point-in-time join、MLflow dataset lineage、Delta Lake time travel 和内部层级契约。；强调 downstream layer 不能回写 raw；raw 修正必须以 correction record 或新 dataset version 表达。 | 11 |

## 来源使用边界

```text
1. Databento、CME、Nasdaq 资料用于支撑 market-data anomaly、flags、trade correction、cancel/re-entry 和 correction record 边界。
2. Databricks、Feast、MLflow、Delta Lake 资料用于支撑数据分层、点时正确特征、数据集血缘和版本边界。
3. CEK-TA 内部数据层契约用于定义 feature-ready / label-ready / raw write-protection 的本项目知识库语义。
4. 所有候选仍需外部二审，不得直接作为 reviewed/approved/default guidance。
```

## 再审入口

```text
docs/audit/phase37_data_engineering_blocked_supplemental_reaudit_package_20260611.json
```
