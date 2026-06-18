# Phase 45 Market Data Ingestion Lineage Contract

## 目标

本契约用于支撑 `P45-G-DATA05 / vendor_schema_version_required` 的 reviewed 前补证。

它定义 CEK-TA 对市场数据 ingestion、解析、标准化和导出的最小血缘字段。该契约不替代供应商 schema，不替代市场数据授权合同，不产生训练授权、再分发许可、交易信号或实盘执行许可。

## 适用范围

```text
1. 市场数据 raw ingest。
2. vendor schema 解析。
3. reference data / market data 标准化。
4. 供回测、replay、TCA、AI 训练或 RAG 检索使用的数据快照。
```

## 字段契约

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `vendor_id` | yes | 数据供应商或交易所数据来源标识。 |
| `dataset_id` | yes | 供应商 dataset / feed / product 标识。 |
| `venue_id` | yes | 交易场所或市场标识。 |
| `schema_name` | yes | 供应商 schema 名称，如 trades、MBO、MBP、definitions、statistics。 |
| `schema_version` | yes | 供应商 schema 或字段版本；若供应商无显式版本，记录抓取日期和文档版本引用。 |
| `field_dictionary_ref` | yes | 字段字典、API 文档或 schema 文档引用。 |
| `parser_version` | yes | CEK-TA 或外接项目解析器版本。 |
| `parser_code_hash` | yes | 解析器代码 hash 或构建产物 digest。 |
| `normalization_version` | yes | 标准化逻辑版本。 |
| `normalization_code_hash` | yes | 标准化代码 hash 或构建产物 digest。 |
| `raw_snapshot_uri` | yes | 原始数据快照位置或对象标识。 |
| `raw_snapshot_digest` | yes | 原始快照 hash / digest，用于证明输入未静默变化。 |
| `source_file_count` | no | 输入文件或分片数量。 |
| `source_record_count` | no | 输入记录数量。 |
| `ingested_at` | yes | ingestion 完成时间。 |
| `source_available_time` | yes | 数据在供应商侧可用时间，若不可得需标记 unknown。 |
| `produced_at` | yes | 标准化输出产生时间。 |
| `lineage_id` | yes | 将 raw input、parser、normalizer、output dataset 关联的血缘 ID。 |
| `input_dataset_version` | yes | 输入数据版本。 |
| `output_dataset_version` | yes | 输出数据版本。 |
| `quality_report_id` | no | 关联数据质量报告。 |
| `contract_version` | yes | 本契约版本。 |

## 校验规则

```text
1. 缺少 `raw_snapshot_digest` 时，不得声称数据快照可复现。
2. 缺少 `parser_version` 或 `normalization_version` 时，不得声称解析/标准化语义可追踪。
3. 供应商字段、单位、枚举、schema 或数据类型发生变化时，必须产生新的 `schema_version` 或 `field_dictionary_ref`。
4. `raw_snapshot_uri` 不得被标准化输出覆盖。
5. 回测、replay、TCA、AI 训练和 RAG 索引只能引用已绑定 `lineage_id` 的输出。
6. 若外接项目无法保存原始数据，必须保存供应商请求参数、响应 digest、时间范围、dataset、schema 和授权边界。
```

## Owner 边界

```text
Data Engineering:
  拥有 ingestion、parser、normalization、schema version、raw snapshot 和 lineage contract。

Market Microstructure:
  拥有 session、market status、instrument metadata 的市场语义校验。

AI Engineering:
  只能消费已版本化、point-in-time、带 lineage 的训练/评估数据；不能修改市场数据事实。

Legal / Vendor Owner:
  拥有市场数据授权、training/evaluation permission、redistribution 和 retention 判断。
```

## Machine Gate

```json
{
  "review_mode": "caveat_only_candidate_support",
  "approved_allowed": false,
  "default_guidance_allowed": false,
  "hard_gate_allowed": false,
  "trade_execution_advice_allowed": false,
  "legal_license_conclusion_allowed": false
}
```

## 不做什么

```text
1. 不定义供应商商业授权。
2. 不定义法律结论。
3. 不定义交易信号。
4. 不输出买卖点、仓位、杠杆、止损止盈或实盘执行许可。
5. 不要求所有外接项目必须使用同一物理表名。
```
