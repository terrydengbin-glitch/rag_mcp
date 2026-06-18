# Phase 36 AI Engineering 首批 P0-Core 候选采集报告

## 结果

本轮完成 `CEK-TA-185` 的首批 AI Engineering P0-Core 联网采集，生成 10 条候选知识。候选只进入 `codex-expert-kit/rag/candidates/`，未写入 formal knowledge，未标记 reviewed 或 approved，不能作为 MCP/SearchLab/外部项目默认指导。

## 候选范围

| ResearchTask | candidate_id | knowledge_id | 主题 |
| --- | --- | --- | --- |
| RIT-P36-A-T01 | `cand_20260609_ai_engineering_training_objective_task_definition_required_v1_001` | `training_objective.task_definition_required.v1` | 训练任务目标必须先定义 |
| RIT-P36-A-T02 | `cand_20260609_ai_engineering_training_objective_rag_vs_finetune_boundary_required_v1_001` | `training_objective.rag_vs_finetune_boundary_required.v1` | RAG-first / fine-tune 边界 |
| RIT-P36-A-T08 | `cand_20260609_ai_engineering_dataset_dataset_card_required_v1_001` | `dataset.dataset_card_required.v1` | dataset card / datasheet |
| RIT-P36-A-T09 | `cand_20260609_ai_engineering_leakage_train_test_contamination_block_v1_001` | `leakage.train_test_contamination_block.v1` | 训练/测试污染阻断 |
| RIT-P36-A-T16 | `cand_20260609_ai_engineering_eval_holdout_test_set_required_v1_001` | `eval.holdout_test_set_required.v1` | holdout eval |
| RIT-P36-C-36 | `cand_20260609_ai_engineering_governance_dataset_card_and_model_card_required_v1_001` | `governance.dataset_card_and_model_card_required.v1` | dataset card + model card |
| RIT-P36-N-01 | `cand_20260609_ai_engineering_eval_counterfactual_outcome_missing_for_blocked_trades_v1_001` | `eval.counterfactual_outcome_missing_for_blocked_trades.v1` | 被阻断交易反事实结果缺失 |
| RIT-P36-N-02 | `cand_20260609_ai_engineering_eval_off_policy_evaluation_required_for_gate_policy_v1_001` | `eval.off_policy_evaluation_required_for_gate_policy.v1` | gate policy 需要 off-policy / counterfactual eval |
| RIT-P36-N-04 | `cand_20260609_ai_engineering_security_rag_context_is_untrusted_input_v1_001` | `security.rag_context_is_untrusted_input.v1` | RAG context / tool output 非可信 |
| RIT-P36-N-05 | `cand_20260609_ai_engineering_security_prompt_injection_test_required_for_trade_context_v1_001` | `security.prompt_injection_test_required_for_trade_context.v1` | 交易上下文 prompt injection 测试 |

## 来源覆盖

本轮使用的来源类型：

```text
official_doc
framework_doc
paper
standard_or_risk_framework
```

关键来源：

| 来源 | URL | 用途 |
| --- | --- | --- |
| OpenAI Model Optimization | https://platform.openai.com/docs/guides/model-optimization | 支撑 eval / prompt / fine-tune / feedback loop 的训练方法边界 |
| OpenAI Fine-tuning Best Practices | https://platform.openai.com/docs/guides/fine-tuning-best-practices | 支撑训练数据、测试数据、eval 数据分离 |
| Hugging Face TRL | https://huggingface.co/docs/trl | 支撑 SFT/DPO 等训练方法分类 |
| Datasheets for Datasets | https://arxiv.org/abs/1803.09010 | 支撑 dataset card / datasheet |
| scikit-learn Common Pitfalls | https://scikit-learn.org/stable/common_pitfalls.html | 支撑 data leakage / train-test contamination |
| scikit-learn Cross-validation | https://scikit-learn.org/stable/modules/cross_validation.html | 支撑 holdout / CV / 测试集调参风险 |
| Model Cards for Model Reporting | https://arxiv.org/abs/1810.03993 | 支撑 model card |
| Hugging Face Model Cards | https://huggingface.co/docs/hub/model-cards | 支撑模型卡工程实践 |
| Counterfactual Risk Minimization | https://proceedings.mlr.press/v37/swaminathan15.html | 支撑 logged bandit feedback / off-policy 评估 |
| Counterfactual Risk Minimization arXiv | https://arxiv.org/abs/1502.02362 | 支撑反事实学习与评估 |
| OWASP LLM Prompt Injection | https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html | 支撑 prompt injection / untrusted context |
| OWASP RAG Security | https://cheatsheetseries.owasp.org/cheatsheets/RAG_Security_Cheat_Sheet.html | 支撑 RAG context 非可信、pipeline logging |
| NIST AI RMF | https://www.nist.gov/itl/ai-risk-management-framework | 支撑 AI risk management / governance |

## 边界

```text
1. 本轮候选只覆盖 AI Engineering，不覆盖 K 线、策略、回测、实盘执行、风控规则本体。
2. 候选中的 LLM gate 只能表示 gate_suggestion，不能表示最终交易裁决。
3. RAG context、tool output、free-text trade notes 默认视为非可信输入。
4. 被阻断交易不能直接标注为亏损或坏交易，必须记录反事实结果缺失。
5. 所有候选均为 candidate_ready，等待 AI/人工审计。
```

## 验证

```text
python codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py
结果：wrote ui/src/data/phase23Candidates.ts with 17 candidates

python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
结果：gate_status = pass, candidate_count = 17, failure_count = 0, warning_count = 0
```

## 剩余风险

```text
1. 候选仍需 AI/人工审计后才能进入 formal draft/reviewed。
2. 部分来源是 time_sensitive official docs，后续正式知识需要记录 version/freshness。
3. 反事实评估知识需要在正式 draft 中进一步说明与交易 blocked trade 的映射边界。
4. RAG security 知识需要与 MCP 只读权限、外部项目主动检索协议建立交叉引用。
```
