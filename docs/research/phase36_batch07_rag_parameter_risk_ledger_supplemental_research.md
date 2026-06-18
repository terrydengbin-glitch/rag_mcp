# Phase 36 第七批 needs_more_evidence 补证采集记录

## 任务范围

```text
Phase: Phase 36 AI Engineering 交易 LLM Gating/Scoring 知识扩展
任务: CEK-TA-239
对象:
- cand_20260609_ai_engineering_rag_no_hit_requires_neutral_or_review_v1_001
- cand_20260609_ai_engineering_research_feedback_no_auto_strategy_parameter_update_v1_001
- cand_20260609_ai_engineering_risk_ledger_false_allow_cost_record_required_v1_001
日期: 2026-06-09
```

## 上下游

上游输入：

```text
docs/audit/audit_result_phase36_ai_engineering_batch_07_of_10_20260609_gpt55_pro_strict_sources.json
docs/reports/phase36_batch_07_audit_import_report.json
三条 needs_more_evidence candidate JSON
```

下游输出：

```text
补证后的 candidate JSON
docs/audit/phase36_batch07_rag_parameter_risk_ledger_supplemental_audit_package_20260609.json
ui/src/data/phase23Candidates.ts
```

边界：

```text
补证不等于通过。
candidate 仍是 needs_more_evidence。
二审 accepted_for_draft 后也只能转 formal reviewed，不能转 approved。
不写入项目私有交易数据、具体买卖点、仓位、止损止盈、订单或账户信息。
```

## 补证 1：RAG no-hit requires neutral or review

审计问题：

```text
原 statement 没有明确 no-hit fallback action，只表达默认指导准入条件。
```

新增来源：

| source_id | 来源 | 类型 | 支撑点 |
| --- | --- | --- | --- |
| src_sufficient_context_rag_2024 | Sufficient Context: A New Lens on RAG Systems | paper | 上下文不足时 RAG 容易错误，应支持 abstain / selective behavior |
| src_contextual_no_retrieval_system_prompt | No Retrieval System Prompt | official_doc | 检索、重排、过滤后无相关知识时需要显式定义 agent 行为 |

补强后的 statement：

```text
如果任务要求检索 CEK-TA，但没有命中、来源覆盖不足，或没有符合 machine_gate 的可用知识，系统必须返回 neutral_score、abstain、needs_review 或 block_default_guidance，不得编造默认指导。
```

## 补证 2：no auto strategy parameter update

审计问题：

```text
原 statement 与 hypothesis-only 父规则重复，没有明确禁止自动创建、修改或部署策略参数。
```

新增来源：

| source_id | 来源 | 类型 | 支撑点 |
| --- | --- | --- | --- |
| src_owasp_prompt_tool_least_privilege | OWASP LLM Prompt Injection Prevention | standard | 最小权限、工具访问限制、敏感动作人工审批 |
| src_mcp_security_best_practices | MCP Security Best Practices | official_doc | progressive least-privilege scope、限制工具/资源访问 |
| src_mcp_authorization_scopes | Understanding Authorization in MCP | official_doc | 按工具/能力拆分权限并在服务端验证 scope |

补强后的 statement：

```text
LLM 输出不得自动创建、修改或部署交易策略参数；任何参数变更建议都必须转成 research ticket，并经过 Trading Engineering owner 审查、验证证据和审批。
```

## 补证 3：risk ledger false allow cost record required

审计问题：

```text
原来源支持通用风险治理，但不能直接支撑 false allow / false block / opportunity cost / cost matrix 风险账本。
```

新增来源：

| source_id | 来源 | 类型 | 支撑点 |
| --- | --- | --- | --- |
| src_sklearn_cost_sensitive_threshold | scikit-learn cost-sensitive threshold | official_doc | misclassification cost matrix、false positive / false negative 成本和阈值调整 |
| src_nist_ai_rmf_core_manage | NIST AI RMF Core Manage | standard | 按 impact、likelihood 和资源优先处理已记录 AI 风险 |

补强后的 statement：

```text
在改变 hard-gate 成本假设、阈值或默认风险偏好前，必须把 false allow、false block、机会成本上下文、后续观测结果和 reviewer decision 记录到风险账本。
```

内部互链：

```text
kb_ai_engineering.gating.false_allow_more_dangerous_than_false_block.v1
kb_ai_engineering.calibration.threshold_requires_shadow_data.v1
kb_ai_engineering.audit.every_gate_decision_requires_trace.v1
```

## 二审建议

```text
如果二审通过，只能输出 accepted_for_draft。
Codex 导入后只能生成 formal reviewed + machine_gate=caveat_only。
不得输出 approved，不得允许默认指导。
```
