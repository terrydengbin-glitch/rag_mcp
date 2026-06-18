# Phase 36 第十批 strategy/training example 补证采集记录

## 任务信息

```text
Phase: Phase 36 AI Engineering 交易 LLM Gating/Scoring 知识扩展
任务: CEK-TA-255 / CEK-TA-256
日期: 2026-06-09
来源审计结果: audit_result_phase36_ai_engineering_batch_10_of_10_20260609_gpt55_pro_strict_sources
二审包: phase36_batch10_strategy_training_example_supplemental_audit_package_20260609
```

## 上游输入

```text
docs/audit/audit_result_phase36_ai_engineering_batch_10_of_10_20260609_gpt55_pro_strict_sources.json
codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/
docs/tasks/phase36_ai_engineering_gating_scoring_knowledge.md
docs/contracts/ai_engineering_gating_scoring_contract.md
```

## 下游输出

```text
4 条候选仍保留 needs_more_evidence 状态，等待二次审计。
docs/audit/phase36_batch10_strategy_training_example_supplemental_audit_package_20260609.json
ui/src/data/phase23Candidates.ts
```

## 边界

```text
本次只补证和导出二审包。
不创建 formal reviewed 知识。
不设置 approved。
不设置 machine_gate allow。
不把策略本体、K 线规则、买卖条件、仓位、止损止盈或订单执行规则写入 AI Engineering。
```

## 补证来源摘要

```text
MLflow Tracking: 支持参数、代码版本、指标、artifacts、run metadata、dataset-linked metrics 和模型/数据追踪。
DVC .dvc files: 支持用 Git 版本化数据占位元数据并跟踪数据目标。
Datasheets for Datasets: 支持数据集动机、组成、采集过程、推荐用途、维护和限制的透明记录。
scikit-learn common pitfalls: 支持 data leakage 风险和先 split 后 fit 的训练/测试隔离。
Hugging Face TRL SFTTrainer: 支持 standard/conversational、language modeling 和 prompt-completion SFT 数据格式。
OpenAI Structured Outputs + JSON Schema: 支持结构化输出 schema、字段说明、解析和验证。
TensorFlow Data Validation: 支持基于 schema 和统计的异常检测、缺失类型、缺失值、版本/漂移比较。
```

## 候选补证清单

| candidate_id | normalized_claim | 来源数 | 主要来源 |
| --- | --- | --- | --- |
| `cand_20260609_ai_engineering_trade_data_strategy_id_and_version_required_v1_001` | `trade_data.strategy_id_and_version_required.v1` | 4 | MLflow Tracking；.dvc Files | Data Version Control；Datasheets for Datasets；Model optimization | OpenAI API |
| `cand_20260609_ai_engineering_training_data_strategy_version_required_v1_001` | `training_data.strategy_version_required.v1` | 4 | MLflow Tracking；.dvc Files | Data Version Control；Datasheets for Datasets；Common pitfalls and recommended practices | scikit-learn |
| `cand_20260609_ai_engineering_training_example_input_target_separation_v1_001` | `training_example.input_target_separation.v1` | 5 | Common pitfalls and recommended practices | scikit-learn；SFT Trainer | Hugging Face TRL；TensorFlow Data Validation Anomalies Reference；Structured model outputs | OpenAI API；JSON Schema Specification |
| `cand_20260609_ai_engineering_training_example_sft_schema_required_v1_001` | `training_example.sft_schema_required.v1` | 5 | SFT Trainer | Hugging Face TRL；Structured model outputs | OpenAI API；JSON Schema Specification；TensorFlow Data Validation Anomalies Reference；Model optimization | OpenAI API |

## 二次审计重点

```text
1. strategy_id / strategy_version_ref / strategy_owner_ref 是否应在 trade_data 层和 training_data 层分别保留，还是合并为父子规则。
2. training sample 的 strategy_version_ref 缺失时，是否统一 block_training / exclude_from_eval。
3. input / target / label / outcome_context 分离规则是否覆盖 SFT、DPO、preference pair 和 eval case。
4. SFT example schema 是否足够 vendor-neutral，并能支持 schema validation、split_id、source_ids 和 held-out eval。
5. 所有条目通过二审后也只能进入 accepted_for_draft -> formal reviewed，不得直接 approved。
```
