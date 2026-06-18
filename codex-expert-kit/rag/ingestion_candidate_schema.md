# CEK-TA Ingestion Candidate Schema

本文件定义 Phase 12 的候选知识入库包结构。候选包是联网采集和正式知识库之间的审计缓冲层，不是 approved 知识。

## Schema Version

```text
schema_name: cek_ta_ingestion_candidate
schema_version: 1.0.0
encoding: UTF-8
```

## Required Object

```json
{
  "schema_version": "1.0.0",
  "candidate_id": "cand_20260608_backtest_same_candle_tp_sl_001",
  "research_task_id": "CEK-TA-RESEARCH-20260608-001",
  "status": {
    "review_status": "proposed | sourced | classified | conflict_checked | reviewed | accepted | rejected | needs_more_evidence",
    "ingestion_decision": "hold | needs_more_evidence | reject | convert_to_knowledge_item | convert_to_skill | convert_to_skill_and_knowledge | convert_to_eval_case",
    "decision_reason": "string",
    "created_at": "YYYY-MM-DD",
    "updated_at": "YYYY-MM-DD"
  },
  "classification": {
    "tree_node_id": "kt.replay_simulation.fill_model",
    "tree_path": "CEK-TA / Trading Engineering / Replay And Simulation / Fill Model",
    "related_nodes": [],
    "partition_id": "KB_05_REPLAY_SIMULATION",
    "domain": "replay_simulation",
    "subdomain": "fill_model",
    "rule_type": "definition | principle | procedure | formula | checklist | anti_pattern | adapter_rule | schema | incident | eval_case",
    "used_for": ["backtest_review", "replay", "simulation"]
  },
  "claim": {
    "claim_id": "claim_001",
    "statement": "single clear candidate rule",
    "normalized_claim": "canonical short form for conflict detection",
    "evidence_summary": "short source-backed summary",
    "interpretation_notes": "what Codex inferred from the evidence",
    "claim_strength": "strong | moderate | weak",
    "performance_claim": false
  },
  "applicability": {
    "market": "crypto | futures | spot | stock | general",
    "asset": "BTC | ETH | multi | general",
    "timeframe": "tick | 1s | 1m | 3m | 15m | 1h | 4h | 1d | general",
    "data_granularity": "tick | trade | order_book | second | kline | account_event | general",
    "project_type": "kline_trend_strategy | abnormal_move_strategy | high_fidelity_simulator | live_binance_futures | trading_llm_assistant | general",
    "applies_when": ["string"],
    "not_applicable_when": ["string"],
    "assumptions": ["string"],
    "limitations": ["string"]
  },
  "source_refs": [
    {
      "source_id": "src_001",
      "source_title": "string",
      "source_url": "string | null",
      "source_type": "official_doc | paper | exchange_rule | framework_doc | book | research_report | engineering_article | internal_report | task_card | code_doc | runbook",
      "publisher": "string | null",
      "published_at": "YYYY-MM-DD | null",
      "accessed_at": "YYYY-MM-DD",
      "version": "string | null",
      "reliability": "high | medium | low",
      "score": 0,
      "relevance": "high | medium | low",
      "freshness": "stable | time_sensitive | deprecated",
      "limitations": [],
      "evidence_summary": "string",
      "quoted_excerpt_allowed": false
    }
  ],
  "source_quality": {
    "overall_reliability": "high | medium | low",
    "score": 0,
    "score_version": "1.0.0",
    "primary_source_count": 0,
    "supporting_source_count": 0,
    "low_reliability_source_count": 0,
    "mandatory_downgrades": [],
    "limitations": []
  },
  "conflict_audit": {
    "conflict_status": "none | potential | confirmed | resolved | deprecated_by_conflict",
    "checked_against": [],
    "conflicts": [
      {
        "knowledge_id": "string",
        "conflict_type": "direct_conflict | scope_conflict | version_conflict | market_conflict | granularity_conflict | assumption_conflict",
        "severity": "blocking | warning | informational",
        "overlap_scope": {
          "domain": "string",
          "subdomain": "string",
          "market": "string",
          "timeframe": "string",
          "data_granularity": "string"
        },
        "candidate_claim": "string",
        "existing_claim": "string",
        "resolution": "string",
        "default_recommendation": "string | null",
        "requires_human_review": true
      }
    ],
    "resolution_summary": "string",
    "approval_allowed": false
  },
  "review": {
    "confidence": "high | medium | low",
    "freshness": "stable | time_sensitive | deprecated",
    "reviewer": "codex | human | mixed | null",
    "reviewed_at": "YYYY-MM-DD | null",
    "open_questions": [],
    "audit_log": [
      {
        "at": "YYYY-MM-DD",
        "actor": "codex | human",
        "action": "created | sourced | classified | conflict_checked | reviewed | accepted | rejected | requested_more_evidence",
        "reason": "string"
      }
    ]
  },
  "workflow": {
    "stage": "pending_review | ai_audited | needs_more_evidence | rejected | formalized_reviewed | approval_requested | approved",
    "queue_group": "pending | ai_passed | needs_more_evidence | formalized | rejected",
    "formal_knowledge_id": "string | null",
    "formal_review_status": "draft | reviewed | approved | rejected | deprecated | null",
    "ai_audit_result_id": "string | null",
    "hidden_from_default_queue": false,
    "next_action": "export_ai_audit | apply_ai_audit_patch | review_formal_knowledge | request_human_approval | none"
  },
  "copyright": {
    "stores_full_text": false,
    "stores_long_quote": false,
    "summary_only": true,
    "license_notes": "string | null",
    "reuse_risk": "low | medium | high"
  },
  "conversion_target": {
    "proposed_knowledge_id": "kb_05_replay_simulation.fill_model.same_candle_tp_sl.v1",
    "target_schema": "cek_ta_knowledge_item",
    "target_review_status": "draft",
    "skill_candidate": false,
    "eval_case_candidate": false
  }
}
```

## Required Fields

```text
schema_version
candidate_id
research_task_id
status.review_status
status.ingestion_decision
classification.tree_node_id
classification.tree_path
classification.partition_id
classification.domain
classification.subdomain
claim.statement
claim.normalized_claim
claim.evidence_summary
applicability.applies_when
applicability.not_applicable_when
applicability.assumptions
source_refs
source_quality
conflict_audit
review.confidence
review.freshness
workflow
copyright
conversion_target
```

## State Flow

```text
proposed
  -> sourced
  -> classified
  -> conflict_checked
  -> reviewed
  -> accepted

reviewed
  -> rejected

conflict_checked
  -> needs_more_evidence
  -> sourced
```

`accepted` 只表示候选包通过审计，可以转换为正式知识草稿；不表示正式知识已 approved。

## Candidate To Reviewed Workflow

Phase 32 起，候选知识必须通过 `workflow` 表达它在批量审计流水线中的位置。

```text
pending_review -> ai_audited -> formalized_reviewed -> approval_requested -> approved
pending_review -> needs_more_evidence
pending_review -> rejected
```

队列分组规则：

```text
workflow.queue_group = pending: 默认待审计队列。
workflow.queue_group = ai_passed: AI 审计已通过，但尚未完成正式 reviewed 知识回写。
workflow.queue_group = needs_more_evidence: 需要补来源、边界、分类或冲突审计。
workflow.queue_group = formalized: 已回链正式知识，正式知识至少为 reviewed。
workflow.queue_group = rejected: 不再进入沉淀流程。
```

边界：

```text
1. candidate accepted 或 accepted_for_draft 不等于 approved。
2. formal knowledge reviewed 不等于 approved。
3. Phase 32 回写脚本不得自动生成 approved。
4. Vue3 候选页默认只展示 pending 队列，但 tree-filter 可以展示已沉淀候选以便追踪。
5. MCP/SearchLab/知识树默认读取正式知识索引，不读取候选队列作为默认知识。
```

## Gate Rules

候选包进入 `accepted` 必须满足：

```text
1. source_refs 至少 1 条。
2. source_quality.overall_reliability 为 high 或 medium。
3. tree_node_id 在 knowledge_tree.md 中存在。
4. applies_when、not_applicable_when、assumptions 均非空。
5. conflict_audit.conflict_status 为 none 或 resolved。
6. conflict_audit.approval_allowed 为 true。
7. copyright.stores_full_text = false。
8. copyright.stores_long_quote = false。
9. reviewer 为 human 或 mixed。
10. audit_log 写明接受理由。
```

必须保持 `rejected` 或 `needs_more_evidence` 的情况：

```text
1. 无来源。
2. 只有 P3/low reliability 来源支撑核心规则。
3. 来源不能覆盖声明的 market/timeframe/data_granularity。
4. 有 blocking conflict 且未消解。
5. performance claim 缺少样本、成本、偏差控制或可复现条件。
6. 内容包含未脱敏项目私有数据。
7. 内容依赖时间敏感规则但 accessed_at 或 version 缺失。
```

## Mapping To Knowledge Item

候选包转正式知识时字段映射如下：

| Candidate Field | Knowledge Item Field |
| --- | --- |
| `conversion_target.proposed_knowledge_id` | `knowledge_id` |
| `classification.*` | `metadata.*` |
| `applicability.*` | `applicability.*` |
| `claim.statement` | `content.statement` |
| `claim.evidence_summary` | `content.citation_notes` |
| `source_refs` | `source_evidence` |
| `source_quality` | `source_quality` |
| `conflict_audit` | `conflict_audit` |
| `review.confidence` | `review.confidence` |
| `review.freshness` | `review.freshness` |
| `candidate_id` | `review.source_candidate_id` |
| `review.ai_audit.audit_result_id` | `review.ai_audit_result_id` |
| `status.created_at` | `review.created_at` |
| `status.updated_at` | `review.updated_at` |

转换后的 `review.review_status` 必须为 `draft`，然后走 `draft -> reviewed -> approved`。

Formal knowledge 进入 `reviewed` 时必须补齐：

```yaml
review:
  source_candidate_id: string | null
  ai_audit_result_id: string | null
  approval_status: not_requested | requested | approved | rejected
  default_guidance_allowed: false
```

`default_guidance_allowed` 只有在 `review.review_status = approved` 且 `review.approval_status = approved` 时才允许为 `true`。

## Vue3 Audit Minimum Fields

Vue3 候选审计队列至少展示和过滤：

```text
candidate_id
research_task_id
tree_node_id
tree_path
domain
subdomain
rule_type
claim.statement
source_count
overall_reliability
source_quality.score
conflict_status
approval_allowed
confidence
freshness
review_status
ingestion_decision
open_questions
updated_at
workflow.stage
workflow.queue_group
workflow.formal_knowledge_id
workflow.formal_review_status
workflow.ai_audit_result_id
workflow.next_action
```

## MCP / RAG Boundary

```text
1. MCP 默认检索正式知识，不默认返回候选包。
2. 候选包只能通过审计视图或显式 audit/candidate 查询暴露。
3. RAG 索引不得把 rejected 候选当成普通知识。
4. reviewed/accepted 候选如果参与审计检索，必须带 review_status、conflict_status、candidate_id 和非 approved 警告。
```

## Test Checklist

```text
1. JSON 字段能覆盖 research_task_card.md 的输出。
2. 字段能映射到 knowledge_item_schema.md。
3. source_refs 满足 source_quality_rules.md。
4. conflict_audit 满足 conflict_detection_rules.md。
5. tree_node_id 能在 knowledge_tree.md 找到。
6. 没有自动 approved 路径。
7. UTF-8 中文可读。
```
