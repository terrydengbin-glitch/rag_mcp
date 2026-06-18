# Phase 38 P0-Core 补证采集记录

## 目标

根据 Phase 38 P0-Core 严格审计报告，为 7 条 needs_more_evidence 候选和 1 条重建 G04 补充 claim-specific 外部来源与 CEK-TA 内部契约。本记录只用于二审准备，不代表 reviewed、approved 或 default guidance。

## 补证结果

### P38-D03 - cand_20260610_phase38_p38_d03_knowledge_refs_formal_index_001

- 补丁摘要：knowledge_refs 必须解析到 formal index；解析失败时 recommendation 必须降级为 abstain/neutral，并触发人工复核。
- 来源数量：6
- 来源 ID：src_cek_ta_phase38_rag_citation_reason_contract, src_cek_ta_phase35_active_retrieval_protocol, src_json_schema_docs
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_d03_knowledge_refs_formal_index_001.json`

### P38-D04 - cand_20260610_phase38_p38_d04_no_hit_abstain_neutral_001

- 补丁摘要：no-hit 或无来源时不得默认生成指导；应输出 neutral/abstain，并记录缺口和查询上下文。
- 来源数量：7
- 来源 ID：src_cek_ta_phase38_rag_citation_reason_contract, src_ragas_faithfulness, src_deepeval_faithfulness, src_owasp_prompt_injection
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_d04_no_hit_abstain_neutral_001.json`

### P38-D05 - cand_20260610_phase38_p38_d05_unsupported_claims_001

- 补丁摘要：unsupported_claims 非空时不得默认 allow；应进入补证、人工复核或阻断队列。
- 来源数量：6
- 来源 ID：src_cek_ta_phase38_rag_citation_reason_contract, src_ragas_faithfulness, src_owasp_prompt_injection
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_d05_unsupported_claims_001.json`

### P38-D06 - cand_20260610_phase38_p38_d06_reason_codes_taxonomy_001

- 补丁摘要：reason_codes 必须来自受控 taxonomy v1，并通过 schema enum 校验；未知 code 必须降级和人工复核。
- 来源数量：6
- 来源 ID：src_cek_ta_phase38_rag_citation_reason_contract, src_json_schema_docs, src_openai_structured_outputs
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_d06_reason_codes_taxonomy_001.json`

### P38-E01 - cand_20260610_phase38_p38_e01_offline_eval_001

- 补丁摘要：historical offline eval 只能可靠评估已执行交易真实结果；未执行、blocked、skipped candidate 属于反事实，除非存在 shadow、paper、replay、OPE 或其他可观测/可估计机制。
- 来源数量：6
- 来源 ID：src_open_bandit_pipeline, src_sklearn_threshold_tuning, src_cek_ta_phase38_runtime_contract
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_e01_offline_eval_001.json`

### P38-G01 - cand_20260610_phase38_p38_g01_scoring_gating_cek_ta_001

- 补丁摘要：scoring/gating 任务属于必须主动检索 CEK-TA 的高风险任务；无命中时必须声明 no-hit，不得凭空补规则。
- 来源数量：6
- 来源 ID：src_cek_ta_phase35_active_retrieval_protocol, src_cek_ta_phase38_rag_citation_reason_contract, src_cek_ta_phase38_runtime_contract
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_g01_scoring_gating_cek_ta_001.json`

### P38-G03 - cand_20260610_phase38_p38_g03_machine_gate_review_status_001

- 补丁摘要：默认指导必须同时满足 approved、approval_status approved、machine_gate allow、无冲突和有来源；reviewed 只能 caveat 或审计参考。
- 来源数量：6
- 来源 ID：src_cek_ta_phase38_rag_citation_reason_contract, src_cek_ta_phase35_active_retrieval_protocol, src_json_schema_docs
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_g03_machine_gate_review_status_001.json`

### P38-G04-R1 - cand_20260610_phase38_p38_g04_context_budget_field_trimming_001

- 补丁摘要：知识包默认只返回最小必要字段；详细审计必须显式请求，并保留 top-k、字段白名单和 token budget。
- 来源数量：6
- 来源 ID：src_cek_ta_phase38_rag_citation_reason_contract, src_cek_ta_phase35_active_retrieval_protocol, src_owasp_prompt_injection
- 候选路径：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_g04_context_budget_field_trimming_001.json`

## 边界

```text
1. 补证完成不等于审计通过。
2. 本批候选仍停留在 needs_more_evidence / ready_for_reaudit。
3. 二审通过后才允许进入 formal draft 队列。
4. 任何候选都不能直接进入 reviewed、approved 或 default guidance。
```
