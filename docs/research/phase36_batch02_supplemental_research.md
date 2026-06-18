# Phase 36 第二批 needs_more_evidence 补证采集记录

## 任务信息

```text
Phase: Phase 36 AI Engineering gating/scoring 知识扩充
任务 ID: CEK-TA-203
下游任务: CEK-TA-204
创建日期: 2026-06-09
状态: done
```

## 目标

为 Phase 36 第二批 AI 审计中被标记为 `needs_more_evidence` 的 2 条候选补充直接来源、重写 statement，并导出二次审计包。

本任务只处理候选补证，不把候选转成正式知识，不设置 `reviewed`，不设置 `approved`，也不允许进入默认指导。

## 上游输入

```text
docs/audit/audit_result_phase36_ai_engineering_batch_02_of_10_20260609_gpt55_pro_strict_sources.json
codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260609_ai_engineering_dataset_deduplication_required_v1_001.json
codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260609_ai_engineering_deployment_llm_timeout_or_mcp_failure_fallback_required_v1_001.json
```

## 下游输出

```text
docs/research/phase36_batch02_supplemental_research.md
docs/audit/phase36_batch02_supplemental_audit_package_20260609.json
2 条已补证但仍处于 needs_more_evidence 的 candidate JSON
ui/src/data/phase23Candidates.ts
```

## 补证对象

| candidate_id | normalized_claim | 补证目标 |
| --- | --- | --- |
| `cand_20260609_ai_engineering_dataset_deduplication_required_v1_001` | `dataset.deduplication_required.v1` | 从泛化 dataset governance 改为 exact/near duplicate、train/eval contamination 和 split overlap 检查 |
| `cand_20260609_ai_engineering_deployment_llm_timeout_or_mcp_failure_fallback_required_v1_001` | `deployment.llm_timeout_or_mcp_failure_fallback_required.v1` | 从 shadow/paper readiness 改为 LLM/MCP timeout、tool error、permission failure、RAG no-hit、source conflict 和 schema validation failure 的 safe fallback |

## 联网来源

### dataset.deduplication_required.v1

| source_id | 来源 | 用途 |
| --- | --- | --- |
| `src_acl_2022_deduplicating_training_data` | Deduplicating Training Data Makes Language Models Better, ACL/arXiv | 支持 LLM 数据集 exact/near duplicate、记忆化、train-test overlap 和评估污染风险 |
| `src_bigcode_dataset_decontamination_deduplication` | BigCode Dataset GitHub repository | 支持 benchmark decontamination 和 near_deduplication 作为训练数据准备工程步骤 |
| `src_sklearn_common_pitfalls_data_leakage` | scikit-learn Common pitfalls / data leakage | 支持训练、验证、测试之间的数据泄漏和隔离原则 |
| `src_datasheets` | Datasheets for Datasets | 作为 supporting source，支持记录数据组成、来源、用途、限制和维护信息 |
| `src_openai_ft` | OpenAI Fine-tuning best practices | 作为 supporting source，支持数据质量和 held-out eval |
| `src_tfdv` | TensorFlow Data Validation | 作为 supporting source，支持 schema validation、异常检测、train/serve skew |

### deployment.llm_timeout_or_mcp_failure_fallback_required.v1

| source_id | 来源 | 用途 |
| --- | --- | --- |
| `src_openai_rate_limits_exponential_backoff` | OpenAI Rate limits | 支持 LLM API rate limit、随机指数退避、最大重试和失败请求限额成本 |
| `src_aws_retry_with_backoff_pattern` | AWS Retry with backoff pattern | 支持临时故障、429、网络故障、非幂等操作和 fail-fast |
| `src_aws_circuit_breaker_pattern` | AWS Circuit breaker pattern | 支持反复 timeout/failure 时快速失败、停止持续重试和服务恢复探测 |
| `src_mcp_tools_error_handling` | Model Context Protocol tools specification | 支持 protocol errors 与 tool execution errors 区分，以及 `isError: true` 的可操作错误反馈 |
| `src_arxiv_2026_mcp_runtime_fault_taxonomy` | A Taxonomy of Runtime Faults in MCP Servers | 支持 MCP runtime fault taxonomy，包括工具调用、schema enforcement、状态管理、模型供应商集成、timeout 和取消 |

## 内容补丁

### dataset.deduplication_required.v1

补证后 statement：

```text
Training、eval、gold、shadow 和 preference datasets 在进入训练、评估或 promotion 前，必须执行 exact duplicate、near-duplicate 和 train/eval contamination 检查；发现重叠或近重复时必须记录处理动作，不能静默进入训练或最终评估。
```

建议字段：

```text
dedupe_run_id
dedupe_method
exact_hash_match_count
near_duplicate_threshold
near_duplicate_group_id
train_eval_overlap_count
gold_overlap_count
action_taken
reason
weighting_policy
split_isolation
reviewer
```

边界：

```text
AI Engineering 定义重复检测、污染检测、审计字段和 promotion gate。
原始交易文本、截图、订单记录或策略样本不进入通用知识库。
具体业务重复判断由外接项目 data owner 或 Trading Engineering 提供。
```

### deployment.llm_timeout_or_mcp_failure_fallback_required.v1

补证后 statement：

```text
LLM/MCP timeout、tool error、permission failure、RAG no-hit、source conflict 或 schema validation failure 必须降级到 neutral、abstain、needs_review、block_default_guidance 或 degraded_read_only_response，绝不能因为故障默认 hard allow 或绕过 deterministic risk gate。
```

建议字段：

```text
failure_type
timeout_ms
mcp_server_id
tool_name
error_code
retry_policy_id
retry_budget
circuit_breaker_state
fallback_action
safe_default
review_queue_id
audit_event_id
```

边界：

```text
AI Engineering 定义 LLM/MCP failure 的安全降级、审计字段和 retry/fail-fast/circuit-breaker 策略。
不定义实盘订单处理、仓位调整、止损止盈或交易执行规则。
如果故障影响订单状态、交易风控或执行引擎，应路由 Trading Engineering。
```

## 二次审计要求

二次审计只允许输出：

```text
accepted_for_draft
needs_more_evidence
rejected
```

不得输出：

```text
approved
default_guidance_allowed
machine_gate.allow
```

审计重点：

```text
1. 补证来源是否直接支撑 rewritten statement。
2. candidate_id、normalized_claim、statement、source_refs 是否已经一致。
3. 是否仍与已 reviewed 知识重复。
4. AI Engineering 与 Trading Engineering 边界是否清楚。
5. 是否可进入 accepted_for_draft，还是继续 needs_more_evidence。
```

## Definition of Done

```text
1. 补证来源已写入 2 条 candidate JSON。
2. 两条候选仍保持 needs_more_evidence。
3. 二次审计包已导出。
4. Vue3 候选 fixture 已重建。
5. 候选工作流校验通过。
6. 知识污染校验通过。
7. 中文文档 UTF-8 无乱码。
```

## 回滚

如二次审计认为证据仍不足：

```text
1. 保持候选 needs_more_evidence。
2. 不生成 formal reviewed 知识。
3. 将缺口追加到 review.open_questions 和下一轮补证任务。
```

如发现来源不适合：

```text
1. 从 candidate source_refs 移除对应 source_id。
2. 降低 source_quality.score。
3. 重新导出二次审计包。
```
