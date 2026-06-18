# CEK-TA Knowledge Leaf Package Template

本模板定义知识树 v2 叶子节点的内容包规范。叶子节点内容包用于把一个专业知识点沉淀成可审计、可检索、可验证、可复用的文件集合。

## Purpose

```text
1. 让 Codex 不只检索一段结论，而是拿到定义、规则、误用、验证和示例。
2. 让每个叶子知识点都能被 RAG/MCP/Vue3 审计。
3. 让专业交易知识有适用边界、证据、冲突状态和测试方法。
4. 防止无来源、无边界、冲突未消解的知识进入默认指导。
```

## Directory Contract

推荐目录：

```text
codex-expert-kit/rag/knowledge/<canonical_node_id_slug>/
├── README.md
├── definition.md
├── rules.md
├── pitfalls.md
├── validation.md
└── examples.md
```

示例：

```text
codex-expert-kit/rag/knowledge/kt.trading_engineering.backtest.fill_assumption.same_bar_tp_sl/
├── README.md
├── definition.md
├── rules.md
├── pitfalls.md
├── validation.md
└── examples.md
```

## Package Metadata

每个文件包必须在 `README.md` 中声明：

```yaml
package_id: kt.trading_engineering.backtest.fill_assumption.same_bar_tp_sl
canonical_node_id: kt.trading_engineering.backtest.fill_assumption
v1_node_id: kt.replay_simulation.fill_model
partition_id: KB_04_BACKTEST
domain: backtest
capability: fill_assumption
topic: same_bar_tp_sl
review_status: draft | reviewed | approved | rejected | deprecated
node_status: draft | candidate | reviewing | approved | conditional | potential_conflict | conflicted | deprecated | archived
conflict_status: none | potential | confirmed | resolved | unchecked
freshness: stable | time_sensitive | deprecated
confidence: high | medium | low
risk_level: low | medium | high | critical
project_binding: none | project_name | sanitized_project_case | governance_only
source_count: 0
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
```

## File Responsibilities

| File | Responsibility | Must Include |
| --- | --- | --- |
| `README.md` | Package overview and metadata | scope, out_of_scope, status, source summary |
| `definition.md` | Precise definitions | terms, assumptions, applicability |
| `rules.md` | Executable professional rules | default_policy, conditions, required evidence |
| `pitfalls.md` | Misuse and anti-patterns | common mistakes, conflict traps |
| `validation.md` | How to verify or test | checklist, test cases, audit assertions |
| `examples.md` | Generalized examples | positive examples, negative examples, non-private cases |

## README.md Contract

```markdown
# <Knowledge Point Title>

## Metadata

```yaml
package_id:
canonical_node_id:
v1_node_id:
partition_id:
domain:
capability:
topic:
review_status:
node_status:
conflict_status:
freshness:
confidence:
risk_level:
project_binding:
created_at:
updated_at:
```

## Scope

```text
This package applies when:
```

## Out Of Scope

```text
This package does not apply when:
```

## Source Summary

```text
source_count:
primary_source_count:
supporting_source_count:
source_quality:
```

## Status Notes

```text
review notes, open questions, and known caveats
```
```

## definition.md Contract

```markdown
# Definition

## Terms

| Term | Definition | Notes |
| --- | --- | --- |

## Assumptions

```text
List assumptions explicitly.
```

## Applicability

```yaml
market:
asset:
timeframe:
data_granularity:
project_type:
applies_when:
not_applicable_when:
```

## Evidence Boundary

```text
What the sources prove, and what they do not prove.
```
```

## rules.md Contract

```markdown
# Rules

## Default Policy

```text
The safe default policy under stated assumptions.
```

## Conditional Rules

| Condition | Rule | Required Evidence | Conflict Policy |
| --- | --- | --- | --- |

## Required Evidence

```text
market
timeframe
data_granularity
source_evidence
applicability_boundary
conflict_status
```

## Not Allowed

```text
Rules that must never be applied as default guidance.
```
```

## pitfalls.md Contract

```markdown
# Pitfalls

## Common Misuse

```text
List common mistakes.
```

## Anti-Patterns

| Anti-Pattern | Why It Is Dangerous | Safer Alternative |
| --- | --- | --- |

## Conflict Traps

```text
Where this topic often conflicts with other nodes.
```
```

## validation.md Contract

```markdown
# Validation

## Checklist

```text
1. Source evidence exists.
2. Applicability is explicit.
3. Not-applicable cases are explicit.
4. Conflict check is complete.
5. Review status allows the intended use.
```

## Test Cases

| Case ID | Input | Expected Result | Status |
| --- | --- | --- | --- |

## Audit Assertions

```text
Assertions Vue3, RAG, MCP, or tests can verify.
```
```

## examples.md Contract

```markdown
# Examples

## Positive Examples

```text
Generalized examples without private project data.
```

## Negative Examples

```text
Examples showing what not to do.
```

## Non-Examples

```text
Cases that look similar but belong to another node.
```
```

## Source Rules

```text
1. Every approved package needs at least one medium/high reliability source.
2. Low reliability sources can supplement but cannot independently approve.
3. Long copyrighted passages are not stored.
4. Source records must include source_type, publisher, accessed_at, reliability, and evidence_summary.
5. Time-sensitive topics must carry version or accessed_at freshness warning.
```

## RAG/MCP Rules

```text
1. RAG chunks must preserve package_id and canonical_node_id.
2. Rules and validation chunks are high priority for code review and task execution.
3. Examples are support context, not default policy.
4. Draft/rejected/deprecated packages must not be default guidance.
5. Conflicted packages require explicit conflict warnings.
```

## Vue3 Audit Rules

Vue3 should display:

```text
package_id
canonical_node_id
v1_node_id
review_status
node_status
conflict_status
freshness
confidence
risk_level
source_count
open_questions
validation checklist
```

## Forbidden Cases

```text
1. Package with no source evidence marked approved.
2. Package with no applicability boundary.
3. Package that mixes markets, timeframes, or data granularities without boundaries.
4. Project-private facts marked project_binding = none.
5. Confirmed unresolved conflict used as default guidance.
6. Raw行情数据、K线数据、订单流原始数据放入知识包。
```

## DoD

```text
1. All six files exist.
2. README metadata is complete.
3. Definitions and rules are separated.
4. Pitfalls and validation are present.
5. Examples are generalized and non-private.
6. Source evidence is traceable.
7. Conflict and review status are explicit.
8. UTF-8 Chinese display is readable.
```

