# Phase 37 Data Engineering D11 契约内联三审补证记录

生成日期：2026-06-11

## 任务

`CEK-TA-392` 只处理 `P37-B-D11 raw_vs_adjusted_data_boundary`，目标是把 CEK-TA 内部数据层契约正文、机器可校验契约摘要和 lineage/feature-store 来源放入三审包。

## 外部来源

| 来源 | 用途 | 边界 |
| --- | --- | --- |
| OpenLineage Object Model | 支撑 Run / Job / Dataset 以及跨转换 lineage event | 不规定 CEK-TA 物理表名 |
| OpenLineage Facets / Dataset Facets | 支撑 schema、version、输入输出 metadata 等 transformation manifest 字段 | 需要映射到项目字段 |
| TensorFlow TFX ML Metadata | 支撑 Artifact / Execution / Context 与 ML workflow lineage | 不定义交易 raw/adjusted 语义 |
| Feast OpenLineage Integration | 支撑 feature engineering lineage 和 feature-ready 血缘 | Feast 不是强制依赖 |

## 内联契约

```text
docs/contracts/phase37_data_engineering_dataset_layers_contract.md
```

三审包内同时包含：

```text
contract_inline.full_text
contract_inline.schema_extract.layers
contract_inline.schema_extract.transformation_manifest_required_fields
contract_inline.schema_extract.hard_boundaries
```

## 审计边界

```text
1. candidate 不是正式知识。
2. 本包最多允许 accepted_for_reviewed_caveat_only。
3. 不允许 approved/default guidance/hard gate。
4. 不允许生成交易建议、买卖点、仓位、杠杆或实盘执行许可。
```
