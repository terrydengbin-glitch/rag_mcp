# Phase 34 Knowledge Item Schema v1.1 Report

## 结果

Phase 34 已完成。正式知识卡片已从 `schema_version = 1.0.0` 升级到 `1.1.0`，并补齐 AI 使用策略与机器门控字段。

## 交付物

```text
docs/contracts/knowledge_item_schema_v1_1_contract.md
docs/research/phase34_recommended_extra_sources_queue.md
codex-expert-kit/rag/scripts/build_machine_gate.py
codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py
docs/reports/phase34_schema_v1_1_validation_report.json
codex-expert-kit/rag/indexes/knowledge_items.json
ui/src/data/formalKnowledgeItems.ts
```

## 数据结果

```text
正式知识总数: 17
machine_gate.allow: 10
machine_gate.caveat_only: 7
machine_gate.deny: 0
```

说明：

```text
1. approved + default_guidance_allowed=true 的正式知识进入 allow。
2. reviewed 知识进入 caveat_only，不作为默认指导。
3. recommended_extra_sources 只作为待核验来源增强队列，不计入 source_evidence。
```

## 上下游对齐

### 上游

```text
codex-expert-kit/rag/knowledge/**/*.json
Phase 31/32 candidate-to-reviewed workflow
Phase 33 knowledge pollution gate
```

### 下游

```text
knowledge_items.json
MCP search_expert_knowledge / get_knowledge_item
FastAPI knowledge tree read-only endpoints
Vue3 KnowledgeTreeView / KnowledgeDetail / SearchLab
其他项目 MCP 调用方
```

## 契约变更

新增字段：

```text
metadata.claim_type
metadata.classification_notes
llm_usage_policy
machine_gate
recommended_extra_sources
```

MCP 默认安全策略：

```text
默认只返回 machine_gate.default_guidance = allow。
caveat_only 需要显式审计模式 include.default_guidance_only=false。
```

## 测试

```text
python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py
结果: pass

python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
结果: pass

python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
结果: pass

python codex-expert-kit/rag/scripts/build_knowledge_items_index.py
结果: pass, 17 items

python codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py
结果: pass, 17 items

python -m pytest codex-expert-kit/api/tests codex-expert-kit/mcp/tests
结果: 38 passed

cd ui && npm run build
结果: pass

cd ui && npm run test:e2e
结果: 18 passed
```

## 风险与回滚

```text
1. v1.1 是增量字段，未删除 v1.0 字段。
2. MCP 对旧 sample fixture 做兼容推断，避免旧样例因缺 machine_gate 失效。
3. reviewed 不会被误判为 approved。
4. 如需回滚，可恢复 knowledge_items.json、formalKnowledgeItems.ts 和正式知识 JSON 的 v1.0 版本。
```

## 结论

Phase 34 DoD 已满足。CEK-TA 知识卡片现在具备可审计、可检索、可治理、可被 MCP/RAG 安全调用的 v1.1 字段。
