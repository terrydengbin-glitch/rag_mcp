# Phase 42 RAG / Vector Storage 契约

## 契约目标

本契约定义 CEK-TA 和外接交易 AI 项目在存储 RAG 文档、chunk、embedding、vector index、citation、source provenance 时必须遵守的边界。

核心判断：

```text
Vector DB 是 retrieval index，不是 canonical store。
RAG 命中是检索证据，不等于知识已 approved。
任何检索结果必须能回链到 source document、chunk、formal knowledge id、source_uri、license 和版本。
```

## 上游输入

```text
docs/research/phase42_database_storage_scope.md
docs/contracts/phase42_database_storage_contract.md
docs/contracts/phase38_rag_citation_and_reason_taxonomy_contract.md
docs/contracts/external_ai_active_retrieval_protocol.md
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/indexes/knowledge_items.json
```

## 下游消费者

```text
1. Phase 42 采集矩阵和候选知识卡。
2. MCP/SearchLab 检索工具。
3. 外接项目 AI IDE 主动检索协议。
4. Vue3 SearchLab 和知识树审计界面。
5. 后续 pgvector/Qdrant 实现任务。
```

## 存储角色分离

| 存储角色 | 允许保存 | 不允许保存 |
| --- | --- | --- |
| canonical store | 正式知识、来源文档、审计状态、版本、引用、人工结论 | 不应只保存 embedding 后丢失原文来源 |
| vector index | embedding、chunk_id、payload metadata、index_version、filter 字段 | 不作为唯一事实来源，不保存未脱敏私有全文 |
| object/file store | 原始文档快照、审计包、候选包、报告 | 不绕过 metadata 和审计状态 |
| runtime cache | 短期检索缓存、召回结果、排序结果 | 不作为长期事实或审计证据 |

## rag_document 契约

最小字段：

```text
document_id
source_uri
source_type
source_title
publisher_or_author
published_at
retrieved_at
license
copyright_policy
content_hash
language
domain
subdomain
review_status
source_quality_score
created_at
updated_at
```

硬规则：

```text
1. source_uri 和 content_hash 必须可用于来源追踪。
2. license 或 copyright_policy 必须存在。
3. retrieved_at 必须存在，用于 freshness 判断。
4. 文档不等于知识卡；进入默认指导前必须转为 source-backed knowledge item。
```

## rag_chunk 契约

最小字段：

```text
chunk_id
document_id
chunk_index
chunk_text_hash
chunk_version
section_path
start_offset
end_offset
summary
language
metadata
created_at
```

硬规则：

```text
1. chunk 必须能回链 document_id。
2. chunk_version 必须随切分策略或原文版本变化而变化。
3. chunk 不得保存超版权限制的长原文摘录。
4. chunk metadata 必须包含 domain、subdomain、source_type 和 freshness。
```

## embedding_record 契约

最小字段：

```text
embedding_id
chunk_id
embedding_model_name
embedding_model_version
embedding_dimension
embedding_created_at
normalization_policy
vector_hash
index_backend
index_version
payload_metadata_hash
```

硬规则：

```text
1. embedding_model_version 必须保存。
2. embedding 只能引用 chunk，不能替代 chunk/source。
3. embedding 模型更换必须触发 index_version 变化或重建计划。
```

## vector_index_manifest 契约

最小字段：

```text
vector_index_id
backend: pgvector | qdrant | other
index_name
index_version
embedding_model_name
embedding_model_version
distance_metric
index_type
payload_schema_version
filterable_fields
source_collection_hash
created_at
rebuild_reason
rollback_target
```

硬规则：

```text
1. index_version 必须绑定 embedding_model_version 和 payload_schema_version。
2. rebuild_reason 必须说明是模型变更、chunk 变更、来源变更还是 schema 变更。
3. rollback_target 必须可追踪。
```

## citation_result 契约

每次 MCP/SearchLab/RAG 返回知识时，citation 最少包含：

```text
knowledge_id
review_status
machine_gate.default_guidance
document_id
chunk_id
source_uri
source_type
retrieved_at
published_at
license
confidence
freshness_status
conflict_status
unsupported_claims
```

硬规则：

```text
1. 无 source_uri 或 chunk_id 的检索结果不得作为默认指导。
2. reviewed/caveat_only 不等于 approved。
3. conflict_status 为 unresolved 时必须阻断默认指导。
4. source_quality_score 低于门槛时必须降级为 needs_review 或 human_review。
```

## pgvector 与 Qdrant 边界

```text
1. pgvector 适合 PostgreSQL 已是主事实库、规模较小、运维希望简单、metadata filtering 较轻的阶段。
2. Qdrant 适合向量规模、payload filter、召回性能、独立扩展和向量索引治理压力明显增加的阶段。
3. 选型不能只看“流行度”，必须基于数据规模、filter 复杂度、延迟、运维、备份、权限、回滚和审计需求。
4. 无论选哪种，canonical records 仍应保留在事实存储中。
```

## HNSW 与 IVFFlat 边界

```text
1. HNSW 适合低延迟、高召回、内存可接受且索引构建成本可管理的场景。
2. IVFFlat 适合更可控的分桶近似搜索，但需要训练/聚类和 probe 参数治理。
3. index_type 必须写入 vector_index_manifest。
4. 召回质量、延迟、内存、重建时间必须被评估并记录。
```

## Payload Metadata 规则

filterable_fields 建议包含：

```text
knowledge_id
canonical_node_id
review_status
machine_gate
domain
subdomain
source_type
freshness_status
conflict_status
license
published_at
retrieved_at
```

硬规则：

```text
1. payload metadata 不得包含密钥、账户、未脱敏私有字段。
2. metadata filter 必须能过滤 review_status、machine_gate、conflict_status。
3. 外接项目私有字段必须先脱敏或只保存引用。
```

## RAG 与正式知识关系

```text
1. rag_document/rag_chunk 是来源材料。
2. CandidateKnowledge 是待审计候选。
3. formal KnowledgeItem 是可被 MCP/SearchLab/KnowledgeTree 消费的正式知识。
4. reviewed KnowledgeItem 只能 caveat_only，不能自动 approved。
5. approved/default guidance 必须经过后续人工治理任务。
```

## 错误和降级契约

| 场景 | 动作 |
| --- | --- |
| 无检索命中 | 返回 no_hit，建议人工补充资料 |
| 命中无来源 | 阻断默认指导，标记 source_missing |
| 命中冲突未消解 | 阻断默认指导，返回 conflict_unresolved |
| 命中过期来源 | 降级 freshness_stale，建议重新采集 |
| embedding/index 版本不匹配 | 阻断高置信引用，要求重建或回滚 |
| payload metadata 不完整 | 降级为 needs_review |

## 输出给 RAG/MCP 的最小建议字段

```text
document_contract
chunk_contract
embedding_contract
vector_index_manifest_contract
citation_contract
backend_selection_boundary
metadata_filter_requirement
default_guidance_block_rule
```

## 不做什么

```text
1. 不把向量命中当 approved 知识。
2. 不保存无来源长文本作为默认指导。
3. 不绕过 formal knowledge index。
4. 不让外部项目私有数据污染通用向量库。
5. 不创建真实 pgvector/Qdrant 服务。
```

## 验收标准

```text
1. 明确 document、chunk、embedding、vector index、citation 的字段契约。
2. 明确 Vector DB 不是 canonical store。
3. 明确 pgvector/Qdrant、HNSW/IVFFlat 的选型边界。
4. 明确 review_status、machine_gate、conflict_status 必须进入 metadata filter。
5. UTF-8 无乱码。
```
