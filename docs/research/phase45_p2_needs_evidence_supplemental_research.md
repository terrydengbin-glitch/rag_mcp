# Phase 45 P2 DATA05 / CRYPTO05 补证记录

## 补证目标

首轮审计中 P45-G-DATA05 与 P45-H-CRYPTO05 被判定为 `needs_more_evidence`。本文件记录补证来源和修补边界。

## 补充来源

| source_id | 来源 | 类型 | URL | 用途 |
| --- | --- | --- | --- | --- |
| `cek_ta_ingestion_lineage_contract` | Phase 45 Market Data Ingestion Lineage Contract | `internal_contract` | docs/contracts/phase45_market_data_ingestion_lineage_contract.md | CEK-TA internal contract defines vendor_id, dataset_id, schema_version, parser_version, normalization_version, raw_snapshot_uri, raw_snapshot_digest and lineage_id. |
| `openlineage_dataset_facets` | OpenLineage Dataset Facets | `official_spec` | https://openlineage.io/docs/spec/facets/dataset-facets/ | OpenLineage dataset facets support attaching common, input and output metadata to datasets for lineage events. |
| `openlineage_object_model` | OpenLineage Object Model | `official_spec` | https://openlineage.io/docs/spec/object-model/ | OpenLineage object model links jobs, runs and input/output datasets to create lineage graphs across platforms. |
| `mlflow_dataset_tracking` | MLflow Dataset Tracking | `official_framework_doc` | https://mlflow.org/docs/latest/ml/dataset/ | MLflow Dataset Tracking supports tracking, versioning and managing datasets for training, validation and evaluation with lineage from raw data to predictions. |
| `mlflow_dataset_api` | MLflow Dataset API | `official_framework_doc` | https://mlflow.org/docs/latest/python_api/mlflow.data.html | MLflow Dataset includes name, digest, schema, profile and source information for a dataset. |
| `iceberg_spec` | Apache Iceberg Specification | `official_spec` | https://iceberg.apache.org/spec/ | Iceberg snapshots and manifest lists record table state and metadata about manifests and data files. |
| `dvc_pipelines` | DVC Data Pipelines | `official_framework_doc` | https://doc.dvc.org/start/data-pipelines/data-pipelines | DVC pipelines capture, organize, version and reproduce data science and machine learning workflows. |
| `binance_ws_market_streams` | Binance USDⓈ-M Futures WebSocket Market Streams | `official_api_doc` | https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams | Binance WebSocket market streams document ping/pong, disconnect behavior, message limits and stream limits. |
| `binance_ws_api_general` | Binance Futures WebSocket API General Info | `official_api_doc` | https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-api-general-info | Binance WebSocket API notes that a single connection is valid for 24 hours and ping/pong failure leads to disconnection. |
| `binance_maintenance_updates` | Binance Maintenance Updates | `official_platform_doc` | https://www.binance.com/en/support/announcement/list/157 | Binance publishes scheduled maintenance and upgrade notices that can affect services. |
| `bybit_ws_connect` | Bybit WebSocket Connect | `official_api_doc` | https://bybit-exchange.github.io/docs/v5/ws/connect | Bybit recommends sending ping heartbeat packets every 20 seconds to maintain WebSocket connections. |
| `binance_mark_price` | Binance Mark Price API | `official_api_doc` | https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Mark-Price | Binance Mark Price API exposes markPrice, indexPrice, lastFundingRate, nextFundingTime and time, supporting mark-price monitoring fields. |
| `binance_adl` | Binance Auto-Deleveraging | `official_platform_doc` | https://www.binance.com/en/support/faq/detail/360033525471 | Binance states ADL is the final liquidation step if the futures insurance fund cannot accept a bankrupt position. |
| `binance_insurance_fund` | Binance Futures Insurance Funds | `official_platform_doc` | https://www.binance.com/en/support/faq/detail/360033525371 | Binance describes futures insurance funds as safety nets for liquidation and bankrupt positions. |

## 修补后边界

```text
1. DATA05：vendor schema 与 CEK-TA parser/normalizer lineage 分开；parser_version、normalization_version、raw_snapshot_digest 和 lineage_id 由内部契约支撑。
2. DATA05：OpenLineage、MLflow、Iceberg、DVC 只作为 lineage / digest / snapshot / reproducibility 模式来源，不作为强制技术栈。
3. CRYPTO05：exchange outage、maintenance、WebSocket disconnect、heartbeat、rate-limit、mark price monitoring、ADL/insurance-fund loss allocation 分开建模。
4. CRYPTO05：clawback 已收窄为 exchange-specific loss-allocation mechanism；若外接项目使用特定 clawback 术语，必须补对应 venue rulebook。
5. 两条均不输出法律授权结论、交易许可、仓位、杠杆、清算规避、实盘执行建议或 hard gate。
```
