# Phase 42 Database / Data Contract / Storage Engineering 知识范围

## 范围结论

Phase 42 补齐交易 AI 项目在数据库、数据契约、审计日志、向量检索存储、迁移、备份恢复和数据生命周期上的专业知识。它服务外接 LLM gating/scoring 项目的开发 AI，让开发 AI 在设计数据层时能主动检索 CEK-TA，避免无审计、无版本、无时点边界、无迁移回滚、无来源追踪的存储设计。

本 Phase 不直接创建生产数据库，也不替外部项目写真实 schema。它先沉淀可复用知识和契约，后续真实落地必须另开实现任务并由开发者确认。

核心链路固定为：

```text
PostgreSQL/关系库负责 canonical records、ledger、manifest 和审计追踪。
Vector DB / pgvector / Qdrant 负责 retrieval index，不负责事实主库。
LLM audit 可以写审计结果，不可以写 final_gate 决策表。
deterministic final gate、score、feedback、outcome、label、dataset、model、prompt、RAG index 必须可追踪、可回放、可审计。
```

## 上游输入

| 上游 | 作用 |
| --- | --- |
| Phase 32 候选到 reviewed 知识工作流 | 约束 candidate、reviewed、approved 的状态边界 |
| Phase 38 AI 模型平台 POC | 提供 scorer、calibrator、LLM audit assistant、final gate 的运行时对象 |
| Phase 40 Continuous Learning | 提供反馈日志、标签刷新、漂移监控、再训练、发布和回滚治理对象 |
| Phase 41 Hybrid Scoring 与 Qwen3 审计助手 | 提供表格 scorer、Qwen3 audit、RAG、final gate 的组合边界 |
| Phase 37 Trading Engineering | 提供交易本体引用边界，K 线、fill model、风控、执行和回测规则不迁入 Phase 42 |
| `codex-expert-kit/rag/knowledge_tree.md` | 提供 AI Engineering L1/L2/L3 节点挂载位置 |

## 下游输出

| 下游 | 消费方式 |
| --- | --- |
| CEK-TA-344 数据库核心表契约 | 使用本范围定义核心表、主键、索引、时间字段、版本字段、审计字段和 append-only 边界 |
| CEK-TA-345 RAG/vector storage 契约 | 使用本范围定义文档、chunk、embedding、vector index、citation 和 source provenance |
| CEK-TA-346 采集矩阵 | 按本范围拆成 34 条知识点和 ResearchIngestionTask 队列 |
| CEK-TA-347 scope audit JSON | 把本范围、专题、表结构和知识点数量交给外部 AI/人工先审计 |
| MCP/SearchLab/KnowledgeTree/Vue3 | 按 canonical node 检索、展示和审计正式知识 |
| 外接交易 AI 项目 | 通过 MCP/RAG 主动检索数据库、迁移、审计日志、向量库和生命周期知识 |

## L2 到 L3 专题映射

Phase 42 新增一个 AI Engineering L2 节点：

```text
kt.ai_engineering.database_storage_engineering
```

对应分区：

```text
KB_AI_26_DATABASE_STORAGE
```

| L2 节点 | L3 专题 | canonical node | 分区 |
| --- | --- | --- | --- |
| Database / Data Contract / Storage Engineering | Relational Core Schema | `kt.ai_engineering.database_storage_engineering.relational_core_schema` | `KB_AI_26_DATABASE_STORAGE` |
| Database / Data Contract / Storage Engineering | Data Contract Lineage | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | `KB_AI_26_DATABASE_STORAGE` |
| Database / Data Contract / Storage Engineering | Migration Versioning | `kt.ai_engineering.database_storage_engineering.migration_versioning` | `KB_AI_26_DATABASE_STORAGE` |
| Database / Data Contract / Storage Engineering | Indexing Query Performance | `kt.ai_engineering.database_storage_engineering.indexing_query_performance` | `KB_AI_26_DATABASE_STORAGE` |
| Database / Data Contract / Storage Engineering | Audit Log Ledger | `kt.ai_engineering.database_storage_engineering.audit_log_ledger` | `KB_AI_26_DATABASE_STORAGE` |
| Database / Data Contract / Storage Engineering | Feature Store Storage | `kt.ai_engineering.database_storage_engineering.feature_store_storage` | `KB_AI_26_DATABASE_STORAGE` |
| Database / Data Contract / Storage Engineering | Vector Store Retrieval Storage | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | `KB_AI_26_DATABASE_STORAGE` |
| Database / Data Contract / Storage Engineering | Model Registry Release Storage | `kt.ai_engineering.database_storage_engineering.model_registry_release_storage` | `KB_AI_26_DATABASE_STORAGE` |
| Database / Data Contract / Storage Engineering | Runtime Observability Trace | `kt.ai_engineering.database_storage_engineering.runtime_observability_trace` | `KB_AI_26_DATABASE_STORAGE` |
| Database / Data Contract / Storage Engineering | Data Lifecycle Retention | `kt.ai_engineering.database_storage_engineering.data_lifecycle_retention` | `KB_AI_26_DATABASE_STORAGE` |
| Database / Data Contract / Storage Engineering | Security Privacy Access Control | `kt.ai_engineering.database_storage_engineering.security_privacy_access_control` | `KB_AI_26_DATABASE_STORAGE` |
| Database / Data Contract / Storage Engineering | Backup Restore Disaster Recovery | `kt.ai_engineering.database_storage_engineering.backup_restore_disaster_recovery` | `KB_AI_26_DATABASE_STORAGE` |

## L3 专题职责

### Relational Core Schema

范围内：

```text
交易 AI 核心关系表、主键、唯一键、外键、约束、JSONB 边界和 idempotency key。
trade_candidate、score_result、calibration_result、llm_audit_result、final_gate_ledger 的最小关系模型。
PostgreSQL constraints 用于保护高价值不变量。
```

范围外：

```text
不设计具体交易策略表。
不写外部项目生产数据库 DDL。
不允许无 migration 手改 schema。
```

### Data Contract Lineage

范围内：

```text
event_time、decision_time、ingestion_time、label_time 的分离。
schema_version、feature_schema_hash、dataset_hash、split_manifest_hash、label_policy_version。
训练样本、反馈、结果、标签和数据集 manifest 的 lineage。
```

范围外：

```text
不定义项目私有交易字段。
不把 outcome 或 label 反向写入 decision-time feature。
```

### Migration Versioning

范围内：

```text
Alembic migration review、reversible migration、rollback plan、schema compatibility check。
autogenerate 只能辅助生成，不得自动应用。
```

范围外：

```text
不执行真实迁移。
不做不可逆迁移。
不跳过人工审查。
```

### Indexing Query Performance

范围内：

```text
查询模式驱动索引、复合索引、唯一索引、分区、分页、慢查询记录。
score/final_gate/audit_trace/release_manifest 常见读取路径的索引边界。
```

范围外：

```text
不提前为未知查询创建复杂索引。
不为了性能牺牲审计追踪和版本一致性。
```

### Audit Log Ledger

范围内：

```text
append-only ledger、actor、reason、before_after、trace_id、row_hash/prev_hash。
final_gate、人工复核、权限变更、审计状态变更的证据链。
```

范围外：

```text
不允许 LLM 直接写 final_gate ledger。
不允许覆盖或删除审计事件。
```

### Feature Store Storage

范围内：

```text
offline/online feature parity、feature snapshot、feature manifest、point-in-time join。
Feast 只作为条件引入选项，不是 POC 默认依赖。
```

范围外：

```text
不定义 K 线指标本体。
不强制引入 Feast。
```

### Vector Store Retrieval Storage

范围内：

```text
pgvector/Qdrant 选型边界、embedding_model_version、chunk_version、payload metadata、source provenance。
vector search result 必须回链到 source document、formal knowledge id 和 citation。
```

范围外：

```text
Vector DB 不作为事实主库。
向量检索命中不等于知识已 approved。
```

### Model Registry Release Storage

范围内：

```text
model_release_manifest、scorer_version、calibrator_version、threshold_policy_version、prompt_version、rag_index_version、rollback_target。
MLflow 只在模型版本和 release manifest 复杂度上升后作为条件引入。
```

范围外：

```text
不直接部署 MLflow。
不允许无 rollback target 发布。
```

### Runtime Observability Trace

范围内：

```text
request_id、audit_trace_id、latency、timeout、fallback、error record、retrieval_hit、citation_completeness。
scorer、calibrator、RAG、Qwen3 audit、final gate 的链路追踪。
```

范围外：

```text
不记录密钥、账户私密字段或未脱敏交易项目私有数据。
```

### Data Lifecycle Retention

范围内：

```text
保留、归档、删除、冷存储、数据集冻结、incident freeze 和不破坏审计回放的 lifecycle policy。
```

范围外：

```text
不把删除策略写成绕过审计追踪。
不因归档导致 replay 和 audit 断链。
```

### Security Privacy Access Control

范围内：

```text
数据库权限、最小权限、RLS/pgAudit 条件引入、secret 不入业务表、PII/private field 脱敏。
```

范围外：

```text
不保存 API key、交易账户密钥、私有账户字段。
不让 MCP 默认获得写权限。
```

### Backup Restore Disaster Recovery

范围内：

```text
backup、restore drill、RPO/RTO、恢复演练报告、灾备状态和演练失败处理。
```

范围外：

```text
不把“配置了备份”等同于“可恢复”。
不在未验证恢复前宣称数据安全。
```

## 跨分支边界

| 主题 | Phase 42 可以做 | 必须引用或交给其他分支 |
| --- | --- | --- |
| K 线和交易信号 | 保存字段版本、来源、schema、decision_time 可见性 | K 线结构、指标边界、setup 规则归 Phase 37 / Trading Engineering |
| 回测和 replay | 记录 dataset_hash、feature_schema_hash、simulation/ref refs | 回测偏差、fill model、slippage 规则归 Trading Engineering |
| 风控和 final gate | 保存 deterministic gate ledger、policy version、actor/reason | 具体风控规则、仓位、止损止盈归 Trading Engineering |
| LLM 审计 | 保存 llm_audit_result、citation、missing_fields、unsupported_claims | Qwen3 训练、reason code 细节归 Phase 41 |
| RAG 检索 | 保存 document/chunk/vector index/citation metadata | 检索排序、machine gate 和冲突感知策略归 RAG Engineering |
| 持续学习 | 保存 feedback/outcome/label/dataset/model manifest | 漂移触发、再训练、晋级回滚策略归 Phase 40 |

## 核心表骨架范围

Phase 42 后续契约会覆盖以下最小表骨架：

```text
trade_candidate
score_result
calibration_result
llm_audit_result
final_gate_ledger
feedback_event
outcome_event
label_event
feature_snapshot_manifest
dataset_snapshot_manifest
rag_document
rag_chunk
vector_index_manifest
model_release_manifest
audit_trace
migration_history
incident_freeze
```

append-only 默认候选：

```text
final_gate_ledger
score_result
llm_audit_result
feedback_event
outcome_event
label_event
```

## 采集优先级

P0 优先覆盖：

```text
canonical store vs vector index
audit_trace_id
append-only final gate and score ledger
decision-time visibility
feedback/outcome/label separation
version binding
RAG source provenance
PostgreSQL constraints and idempotency
Alembic migration review
time fields separation
point-in-time correctness
manifest hash
audit ledger tamper evidence
retention without audit breakage
secret/privacy boundary
backup restore drill
permission audit
```

P1 延后覆盖：

```text
pgvector vs Qdrant
HNSW vs IVFFlat
Qdrant payload index
Feast adoption boundary
MLflow registry adoption boundary
RLS/pgAudit adoption boundary
```

## 审计问题

本范围提交外部 AI/人工审计时重点检查：

```text
1. 是否错误引入真实数据库实施。
2. 是否把 Vector DB 当事实主库。
3. 是否让 LLM audit 绕过 deterministic final gate。
4. 是否混入 K 线、fill model、仓位、止损止盈、实盘执行本体。
5. 是否缺少 decision_time、event_time、label_time、ingestion_time 分离。
6. 是否缺少 source provenance、version binding、audit_trace_id 或 rollback target。
7. 是否把 reviewed/caveat_only 自动当 approved/default guidance。
```

## 状态

```text
scope_status: ready_for_contract
task_id: CEK-TA-343
review_status: draft
default_guidance_allowed: false
hard_gate_allowed: false
```
