# Phase 54 历史 reviewed schema 与候选回链全量回填验收报告

## 结论

Phase 54 已完成。历史 formal reviewed/caveat_only 知识卡的 schema v1.1 治理字段已补齐，候选到正式知识的 workflow 回链字段已补齐，正式知识索引和 Vue3 fixture 已重建。

本次只修治理字段和回链字段：

```text
不修改知识 claim
不修改 source_evidence 语义
不把 reviewed 升级为 approved
不启用 default guidance
不启用 hard gate
```

## 回填结果

| 项目 | 结果 |
| --- | --- |
| formal knowledge 扫描 | 484 |
| schema v1.1 回填文件 | 467 |
| schema unsafe | 0 |
| candidate 扫描 | 488 |
| formal knowledge 扫描 | 484 |
| candidate workflow 回填 | 424 |
| formal review 回链回填 | 68 |
| manual_required | 0 |

## 交付物

```text
docs/tasks/phase54_historical_reviewed_schema_workflow_backfill.md
codex-expert-kit/rag/scripts/build_phase54_backfill_precheck_report.py
codex-expert-kit/rag/scripts/backfill_phase54_reviewed_schema_v1_1.py
codex-expert-kit/rag/scripts/backfill_phase54_candidate_workflow_links.py
docs/reports/phase54_backfill_precheck_report.json
docs/reports/phase54_reviewed_schema_backfill_report.json
docs/reports/phase54_candidate_workflow_backfill_report.json
docs/reports/phase54_validation_report.json
codex-expert-kit/rag/indexes/knowledge_items.json
ui/public/data/formalKnowledgeItems.json
ui/public/data/phase23Candidates.json
ui/public/data/knowledgeTreeScopeIndex.json
ui/src/data/formalKnowledgeItems.ts
ui/src/data/phase23Candidates.ts
```

## 验收

| 门禁 | 结果 |
| --- | --- |
| `validate_knowledge_item_schema_v1_1.py` | pass，failure_count=0 |
| `validate_candidate_to_reviewed_workflow.py` | pass，failure_count=0 |
| `validate_no_mojibake.py` | pass，failure_count=0 |
| `validate_knowledge_tree_alignment.py` | pass |
| `validate_knowledge_pollution.py` | pass，polluted_count=0 |
| `npm --prefix ui run build` | pass |

## 风险与回滚

所有被修改的知识卡和候选文件都记录在：

```text
docs/reports/phase54_reviewed_schema_backfill_report.json
docs/reports/phase54_candidate_workflow_backfill_report.json
```

如果后续发现某条历史知识卡的 `claim_type` 推断需要人工细分，可以按报告中的 `knowledge_id` 和 `source_path` 定点修正，不需要回滚整个 Phase。

## 下一步

后续新增知识沉淀脚本应在写入 formal reviewed 时直接补齐 schema v1.1、candidate workflow 和 formal review 回链字段，避免再次积累历史欠账。
