# Phase 36 第九批 SFT / trade_data 候选补证采集记录

## 目标

处理第九批审计中 5 条 `needs_more_evidence` 候选。审计指出的问题是：`sft.output_schema_consistency_required` 的原 statement 与 ID 不对齐；`trade_candidate.market_risk_execution_context_required` 缺少明确 context refs；三条 `trade_data.*` 是元治理占位句，缺少真实 schema / cost / source_mode 内容。

本次补证只修正候选和导出二审包，不直接转 reviewed，不设置 approved。

## 补证来源

- OpenAI Structured Outputs：https://platform.openai.com/docs/guides/structured-outputs?api-mode=chat
- JSON Schema Specification：https://json-schema.org/specification
- JSON Schema Required Properties：https://tour.json-schema.org/content/01-Getting-Started/03-Required-Properties
- Hugging Face TRL SFTTrainer：https://huggingface.co/docs/trl/sft_trainer
- TensorFlow Data Validation：https://www.tensorflow.org/tfx/data_validation/get_started
- TensorFlow Data Validation capabilities：https://www.tensorflow.org/tfx/data_validation/install
- FINRA Regulatory Notice 15-09：https://www.finra.org/industry/notices/15-09
- QuantConnect Trading and Orders：https://www.quantconnect.com/docs/v2/writing-algorithms/live-trading/trading-and-orders
- QuantConnect Reality Modelling：https://www.quantconnect.com/docs/v1/algorithm-reference/reality-modelling
- QuantConnect Paper Trading：https://www.quantconnect.com/docs/live-trading/paper-trading
- QuantConnect Live Trading Overview：https://www.quantconnect.com/docs/v1/live-trading/overview
- Feast point-in-time correctness：https://docs.feast.dev/getting-started
- Datasheets for Datasets：https://arxiv.org/abs/1803.09010

## 候选处理结果

### cand_20260609_ai_engineering_sft_output_schema_consistency_required_v1_001

- 状态：`needs_more_evidence`
- statement：SFT 训练样本和模型输出必须绑定版本化 `output_schema_id`，并在 held-out eval 上通过 JSON Schema / structured-output conformance 检查；SFT 可以提升格式稳定性，但生产侧仍必须保留 schema validation、parser fallback 和失败样本记录。
- normalized_claim：`sft.output_schema_consistency_required.v1`
- source_refs：7
- 二审包：`docs/audit/phase36_batch09_sft_trade_data_supplemental_audit_package_20260609.json`

### cand_20260609_ai_engineering_trade_candidate_market_risk_execution_context_required_v1_001

- 状态：`needs_more_evidence`
- statement：交易候选进入 LLM scoring/gating 前必须携带决策时点的 `market_context_ref`、`risk_context_ref` 和 `execution_context_ref`，且这些引用必须来自 owner-defined schema；缺少、过期或冲突的 context 必须降级为 `needs_more_evidence` 或 `human_review`，不得由 LLM 自行补全。
- normalized_claim：`trade_candidate.market_risk_execution_context_required.v1`
- source_refs：7
- 二审包：`docs/audit/phase36_batch09_sft_trade_data_supplemental_audit_package_20260609.json`

### cand_20260609_ai_engineering_trade_data_fee_slippage_execution_cost_required_v1_001

- 状态：`needs_more_evidence`
- statement：用于 LLM scoring/gating 训练、评估或复盘的 trade data 必须记录 `fee_ref`、`slippage_ref`、`fill_ref`、`spread_or_liquidity_context_ref` 和 `execution_cost_status`；缺失执行成本上下文时，不得把 PnL 或 outcome 直接作为训练标签或 gate 评估依据。
- normalized_claim：`trade_data.fee_slippage_execution_cost_required.v1`
- source_refs：5
- 二审包：`docs/audit/phase36_batch09_sft_trade_data_supplemental_audit_package_20260609.json`

### cand_20260609_ai_engineering_trade_data_raw_trade_record_required_fields_v1_001

- 状态：`needs_more_evidence`
- statement：进入 LLM training/eval/review 链路的 raw trade record 必须具备最小 schema：`trade_record_id`、`trade_candidate_id`、`decision_timestamp`、`source_mode`、`snapshot_id`、`strategy_version_ref`、`instrument_ref`、`order_ref`、`fill_ref`、`fee_slippage_ref`、`outcome_context_ref`、`privacy_scan_status` 和 `license_status`；缺少核心字段时必须 `block_training` 或 `needs_more_evidence`。
- normalized_claim：`trade_data.raw_trade_record_required_fields.v1`
- source_refs：7
- 二审包：`docs/audit/phase36_batch09_sft_trade_data_supplemental_audit_package_20260609.json`

### cand_20260609_ai_engineering_trade_data_source_mode_required_v1_001

- 状态：`needs_more_evidence`
- statement：每个进入 LLM training/eval/RAG/preference/review 的 trade data sample 必须声明 `source_mode`，例如 `backtest`、`paper`、`shadow`、`live`、`synthetic` 或 `incident_replay`，并记录 `allowed_use`、`prohibited_use`、`pool_type` 和 `promotion_ticket_id`；缺少 source_mode 或混用未经审计的 source_mode 必须阻断训练或降级审计。
- normalized_claim：`trade_data.source_mode_required.v1`
- source_refs：7
- 二审包：`docs/audit/phase36_batch09_sft_trade_data_supplemental_audit_package_20260609.json`
