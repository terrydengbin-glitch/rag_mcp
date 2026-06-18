# Phase 36 AI Engineering 知识卡策略

## 目标

本策略定义 AI Engineering 知识点进入 CEK-TA 知识卡时的 `claim_type`、`llm_usage_policy`、`machine_gate`、默认指导门禁和降级规则。它承接 Phase 34 的 KnowledgeItem Schema v1.1，不改变文件化存储方式，不引入数据库。

## 上游

```text
docs/contracts/knowledge_item_schema_v1_1_contract.md
codex-expert-kit/rag/knowledge_item_schema.md
docs/contracts/ai_engineering_gating_scoring_contract.md
docs/research/phase36_ai_engineering_p0_collection_matrix.md
docs/research/phase36_ai_engineering_research_task_queue.md
```

## 下游

```text
codex-expert-kit/rag/candidates/
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/indexes/knowledge_items.json
MCP search_expert_knowledge / get_knowledge_item
FastAPI KnowledgeTree 只读接口
Vue3 知识树、候选审计页、SearchLab
外部项目 AI 主动检索模板
```

## AI Engineering claim_type

| claim_type | 用途 | 典型节点 |
| --- | --- | --- |
| `llm_training_rule` | 训练目标、SFT/DPO/PEFT、训练运行和训练边界 | `kt.llm_training.model_training_engineering` |
| `llm_eval_rule` | eval、holdout、production-like eval、counterfactual/off-policy、baseline、ablation | `kt.llm_training.model_training_engineering` |
| `training_data_schema_rule` | Raw Trade -> Snapshot -> Feature -> Outcome -> Label -> Example 的 schema 边界 | `kt.llm_training.training_dataset_schema_engineering` |
| `ai_security_rule` | prompt injection、RAG 非可信上下文、tool output 非可信、密钥脱敏 | `kt.ai_security_privacy_compliance` |
| `ai_governance_rule` | dataset/model card、人工审核、审批、反馈治理、事故治理 | `kt.ai_governance_audit` |
| `llmops_release_rule` | shadow、paper、live rollout、artifact lineage、rollback、readiness gate | `kt.llmops_deployment` |

## claim_type 路由

```text
训练目标、SFT、DPO、PEFT、训练运行 -> llm_training_rule
holdout、eval、calibration、counterfactual、baseline、ablation -> llm_eval_rule
TradeCandidate、Decision-Time Feature、LabelingRecord、EvalCase -> training_data_schema_rule
RAG context untrusted、prompt injection、tool output untrusted、data privacy/license -> ai_security_rule
dataset card、model card、approval、feedback、human review -> ai_governance_rule
shadow mode、artifact lineage、release control、rollback -> llmops_release_rule
RAG metadata、citation、machine_gate filtering -> rag_governance_rule
MCP read-only、server-side permission -> mcp_contract_rule
```

## llm_usage_policy 模板

```json
{
  "allowed": [
    "用于审计外接项目的训练数据、RAG 检索、MCP 调用、eval、部署或治理流程。",
    "用于提醒开发 AI 检查来源、冲突、适用边界、数据泄漏和默认指导门禁。",
    "用于生成候选知识、测试计划、审计 checklist 或只读建议。"
  ],
  "not_allowed": [
    "不得据此生成具体买卖点。",
    "不得绕过 deterministic risk engine。",
    "不得直接下单、改策略参数、开启实盘权限或替代人工审批。",
    "不得把 reviewed/candidate 知识当成 approved 默认指导。"
  ],
  "required_context": [
    "task_type",
    "mode",
    "review_status",
    "machine_gate",
    "source_evidence",
    "conflict_status",
    "applicability"
  ],
  "fallback_behavior": "ask_for_context"
}
```

## machine_gate 策略

### allow

仅当全部满足：

```text
review.review_status = approved
review.default_guidance_allowed = true
source_evidence 至少 1 条，P0-Core 建议至少 2 条
source_quality.overall_reliability in [high, medium]
conflict_audit.conflict_status in [none, resolved]
contribution.private_data_removed = true
llm_usage_policy.not_allowed 明确禁止下单、绕过风控和默认指导误用
不包含项目私有事实、账户信息、密钥、未授权数据
```

### caveat_only

适用于：

```text
review.review_status = reviewed
来源、冲突、污染门禁通过
但未经过 approved 治理
或该知识只适合作为审计/研究/候选上下文
```

### deny

任一情况必须 deny：

```text
candidate / draft / rejected / deprecated
无来源
confirmed conflict 或 unresolved conflict
来源质量 low
包含私有数据、账户标识、密钥、未脱敏交易样本
RAG/MCP 安全规则被违反
把 LLM 说成最终交易裁决者
把 hard_block 写成最终执行裁决，而不是 hard_block_recommendation
```

## P0-Core 额外门禁

```text
1. 至少 2 个来源；其中至少 1 个应为 official_doc、paper、standard_or_risk_framework 或 framework_doc。
2. 明确 applies_when 和 not_applicable_when。
3. 明确与 Trading Engineering 的边界；不能写具体交易规则本体。
4. 明确缺上下文时的 fallback_behavior。
5. 明确默认指导阻断条件。
6. 明确 MCP/SearchLab/外部项目 AI 如何引用 source_evidence。
```

## AI Engineering 与 Trading Engineering 分界

AI Engineering 知识卡可以写：

```text
如何引用交易知识
如何把交易知识写入 retrieved_knowledge
如何用交易知识做训练数据 gate、eval gate、runtime gate
如何记录 knowledge_refs、reason_codes、audit_trace
如何阻断无来源、冲突、过期、未授权或低质量知识
```

AI Engineering 知识卡不能写：

```text
某个 K 线形态如何交易
具体入场、止损、止盈、仓位策略
回测 fill model 的交易规则本体
订单状态机、仓位同步、kill switch 的执行规则本体
交易复盘 bad trade taxonomy 的本体定义
```

这些内容应进入 Trading Engineering 分支，由 AI Engineering 通过 `knowledge_refs` 引用。

## 候选到正式知识状态

```text
candidate_ready -> reviewed_candidate -> formal_draft -> formal_reviewed -> formal_approved
```

硬规则：

```text
AI 审计通过不等于 approved。
formal reviewed 默认 machine_gate = caveat_only。
只有后续人工治理任务能把 reviewed 升为 approved。
```

## MCP/FastAPI/Vue3 展示要求

```text
claim_type
canonical_node_id
review_status
machine_gate.default_guidance
llm_usage_policy.allowed
llm_usage_policy.not_allowed
required_context
source_evidence count
conflict_status
blocking_reasons
recommended_next_action
```

## 测试与验收

```text
python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
```

通过条件：

```text
1. validator 支持 AI Engineering claim_type。
2. 既有正式知识不因 claim_type 扩展而失败。
3. 策略文档明确上游、下游、门禁、边界和状态流。
4. 中文 UTF-8 无乱码。
```
