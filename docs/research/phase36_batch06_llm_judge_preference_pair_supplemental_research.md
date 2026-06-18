# Phase 36 第六批 needs_more_evidence 补证采集记录

## 任务范围

```text
Phase: Phase 36 AI Engineering 交易 LLM Gating/Scoring 知识扩展
任务: CEK-TA-233
对象:
- cand_20260609_ai_engineering_llm_judge_position_and_format_bias_check_required_v1_001
- cand_20260609_ai_engineering_preference_pair_not_based_on_pnl_only_v1_001
日期: 2026-06-09
```

## 上下游

上游输入：

```text
docs/audit/audit_result_phase36_ai_engineering_batch_06_of_10_20260609_gpt55_pro_strict_sources.json
docs/reports/phase36_batch_06_audit_import_report.json
两条 needs_more_evidence candidate JSON
```

下游输出：

```text
补证后的 candidate JSON
docs/audit/phase36_batch06_llm_judge_preference_pair_supplemental_audit_package_20260609.json
ui/src/data/phase23Candidates.ts
```

边界：

```text
补证不等于通过。
candidate 仍是 needs_more_evidence。
二审 accepted_for_draft 后也只能转 formal reviewed，不能转 approved。
不写入项目私有交易数据、具体买卖点、仓位、止损止盈、订单或账户信息。
```

## 补证 1：LLM judge position / format bias

候选：

```text
cand_20260609_ai_engineering_llm_judge_position_and_format_bias_check_required_v1_001
```

审计问题：

```text
原来源只支持通用 eval workflow 和 model card 限制记录，不能直接支撑 position bias、format bias、judge prompt stability。
```

新增来源：

| source_id | 来源 | 类型 | 支撑点 |
| --- | --- | --- | --- |
| src_zheng_mt_bench_chatbot_arena_2023 | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | paper | LLM-as-judge 的 position、verbosity、self-enhancement bias |
| src_shi_position_bias_llm_judge_2024 | Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge | paper | repetition stability、position consistency、preference fairness |
| src_wang_output_format_bias_2024 | LLMs Are Biased Towards Output Formats | paper | 输出格式偏差，可支撑 format variant / style sensitivity 检查 |

补强后的 statement：

```text
LLM-as-judge 评估必须检查候选顺序/位置交换、输出格式变体、回答长度/冗余敏感性和裁判提示稳定性；单次裁判分数不得作为模型晋级、调参或交易 gating 证据。
```

## 补证 2：preference pair not based on PnL only

候选：

```text
cand_20260609_ai_engineering_preference_pair_not_based_on_pnl_only_v1_001
```

审计问题：

```text
原 statement 是元治理占位句，与 normalized_claim 不对齐；原来源不能直接支撑 preference pair schema 或 no-PnL-only preference label。
```

新增来源：

| source_id | 来源 | 类型 | 支撑点 |
| --- | --- | --- | --- |
| src_openai_dpo_data_format | Direct preference optimization | official_doc | DPO 样本包含 prompt、preferred output、non-preferred output |
| src_hf_trl_dpo_trainer_dataset_format | DPO Trainer - Hugging Face TRL | official_doc | preference dataset 使用 prompt、chosen、rejected |
| src_datasheets_for_datasets_2018 | Datasheets for Datasets | paper | 数据集动机、组成、采集过程、用途和限制治理 |

补强后的 statement：

```text
交易 LLM 偏好训练的 preference pair 不得只按 PnL 构造；每个 pair 必须在同一 prompt 下比较 chosen/rejected，并记录过程质量、风险合规、规则合规、证据质量和 reason_codes。
```

内部互链：

```text
kb_ai_engineering.label_schema.no_pnl_only_label.v1
kb_ai_engineering.label_schema.multi_dimensional_trade_quality.v1
kb_ai_engineering.label_schema.good_loss_bad_win_required.v1
kb_ai_engineering.preference_training.chosen_rejected_reason_required.v1
```

## 二审建议

```text
如果二审通过，只能输出 accepted_for_draft。
Codex 导入后只能生成 formal reviewed + machine_gate=caveat_only。
不得输出 approved，不得允许默认指导。
```
