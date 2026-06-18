# Phase 42 交易 AI 数据库与数据契约

## 契约目标

本契约定义外接交易 AI gating/scoring 项目在设计数据库、数据契约、审计日志和数据生命周期时必须遵守的最小工程边界。

本契约只定义知识库和外接项目开发 AI 的设计规范，不直接创建生产数据库，不执行迁移，不替外部项目写真实 DDL。

## 上游输入

```text
docs/research/phase42_database_storage_scope.md
docs/tasks/phase42_database_data_contract_storage_engineering.md
docs/contracts/phase41_hybrid_scoring_runtime_contract.md
docs/contracts/phase41_tabular_llm_training_data_contract.md
docs/contracts/phase40_feedback_dataset_contract.md
codex-expert-kit/rag/knowledge_tree.md
```

## 下游消费者

```text
1. Phase 42 采集矩阵和 ResearchIngestionTask 队列。
2. 外接交易 AI 项目的数据库/schema/migration 设计。
3. MCP/SearchLab 主动检索返回的数据库工程指导。
4. Vue3 知识树和候选审计页面。
5. 后续真实数据库落地 Phase。
```

## 总体原则

```text
1. canonical records 必须进入关系型事实存储，不能只存在向量库、日志或临时文件。
2. 所有 scoring/gating 决策必须有 audit_trace_id。
3. final_gate、score_result、llm_audit_result、feedback、outcome、label 默认 append-only。
4. decision_time、event_time、ingestion_time、label_time 必须分离。
5. feedback、outcome、label 必须分表或分对象，不能混成同一个“结果字段”。
6. LLM audit 只能写审计结果，不得写 final_gate 决策。
7. schema 变更必须有 migration、review、rollback 和兼容性检查。
8. 数据删除、归档、脱敏不能破坏审计回放。
```

## 核心表契约

### trade_candidate

用途：保存一次待评分/待审计/待 gate 的交易候选快照。

最小字段：

```text
trade_candidate_id
project_adapter_id
strategy_id
strategy_version
symbol_or_instrument_ref
timeframe_ref
decision_time
feature_snapshot_ref
feature_schema_version
candidate_payload_hash
created_at
audit_trace_id
```

硬规则：

```text
1. 只能包含 decision_time 当时可见字段。
2. 不得包含 outcome、label、未来 K 线、成交结果或人工复盘结论。
3. candidate_payload_hash 必须可用于回放时核对快照是否被篡改。
```

### score_result

用途：保存 scorer/calibrator 对 trade_candidate 的数值评分结果。

最小字段：

```text
score_result_id
trade_candidate_id
scorer_version
calibrator_version
threshold_policy_version
raw_score
calibrated_score
risk_bucket
uncertainty_bucket
top_feature_refs
score_payload_hash
created_at
audit_trace_id
```

硬规则：

```text
1. score_result 必须 append-only。
2. raw_score 不得直接作为交易概率或 final gate 决策。
3. calibrated_score 必须绑定 calibrator_version。
4. top_feature_refs 只能用于解释和审计，不能作为交易规则证据。
```

### calibration_result

用途：保存校准器输出、校准质量和阈值策略引用。

最小字段：

```text
calibration_result_id
model_version
calibrator_version
calibration_dataset_hash
calibration_method
brier_score
ece
slice_metrics_ref
created_at
audit_trace_id
```

硬规则：

```text
1. calibration_dataset_hash 必须独立于训练集。
2. 校准质量不足时不得进入默认放行链路。
3. slice_metrics_ref 可引用 regime、strategy family、timeframe 等切片，但不定义 Trading 本体。
```

### llm_audit_result

用途：保存 Qwen3/LLM 审计助手的结构化审计输出。

最小字段：

```text
llm_audit_result_id
trade_candidate_id
model_name
model_version
prompt_version
rag_index_version
reason_codes
risk_flags
missing_fields
unsupported_claims
knowledge_refs
citation_completeness_score
requires_human_review
audit_payload_hash
created_at
audit_trace_id
```

硬规则：

```text
1. llm_audit_result 必须 append-only。
2. LLM 输出不能写 final_gate 决策。
3. 无 RAG 命中、无来源、引用冲突未消解时必须 abstain 或 requires_human_review。
4. 不保存私有 chain-of-thought。
```

### final_gate_ledger

用途：保存 deterministic final gate 的最终放行、阻断、降级、复核或冻结决策。

最小字段：

```text
final_gate_event_id
trade_candidate_id
score_result_id
llm_audit_result_id
risk_policy_version
threshold_policy_version
release_manifest_version
gate_decision
deterministic_rule_hits
actor
reason
before_state
after_state
created_at
audit_trace_id
row_hash
prev_hash
```

硬规则：

```text
1. final_gate_ledger 必须 append-only。
2. gate_decision 只能由 deterministic policy 或人工审批动作写入。
3. LLM recommendation、raw_score、自然语言解释不能直接写 gate_decision。
4. row_hash/prev_hash 或等价机制用于提供防篡改证据。
```

### feedback_event / outcome_event / label_event

用途：分离反馈、真实结果观察和训练标签。

硬规则：

```text
1. feedback_event 保存人工复核、运营反馈、复盘备注和纠错事件。
2. outcome_event 保存后验观察结果，不得反向污染 trade_candidate。
3. label_event 保存标签，必须绑定 label_policy_version 和 label_source。
4. 三者不能合并成一个字段。
```

### manifest 表

必须覆盖：

```text
feature_snapshot_manifest
dataset_snapshot_manifest
model_release_manifest
vector_index_manifest
migration_history
incident_freeze
```

硬规则：

```text
1. feature_snapshot_manifest 必须记录 feature_schema_hash。
2. dataset_snapshot_manifest 必须记录 dataset_hash、split_manifest_hash 和 label_policy_version。
3. model_release_manifest 必须绑定 scorer、calibrator、threshold、prompt、RAG index 和 rollback target。
4. migration_history 必须记录 migration id、review 状态、rollback plan 和 compatibility check。
5. incident_freeze 必须记录冻结范围、原因、审批人和解冻条件。
```

## 时间字段契约

| 字段 | 含义 | 规则 |
| --- | --- | --- |
| `event_time` | 业务事件发生时间 | 不能等同于入库时间 |
| `decision_time` | AI 或 final gate 作出决策的时间 | feature 必须在此时点可见 |
| `ingestion_time` | 数据进入系统的时间 | 用于延迟和数据新鲜度审计 |
| `label_time` | 标签可被观察或确认的时间 | 必须晚于 decision_time |
| `created_at` | 记录创建时间 | 用于审计，不替代业务时间 |

## 版本字段契约

每次 scoring/gating 必须能追踪：

```text
feature_schema_version
dataset_hash
split_manifest_hash
label_policy_version
scorer_version
calibrator_version
threshold_policy_version
prompt_version
rag_index_version
risk_policy_version
release_manifest_version
```

## 索引和约束契约

必须优先考虑：

```text
1. `trade_candidate_id`、`audit_trace_id`、`decision_time` 的查询路径。
2. `project_adapter_id + strategy_id + strategy_version + decision_time` 的复合查询。
3. `idempotency_key` 或 payload hash 防重复写入。
4. 高价值不变量使用数据库 constraint，而不是只靠应用层 if。
5. append-only 表禁止业务 update/delete。
```

## 迁移契约

```text
1. 每个 schema 变更必须有 migration 文件。
2. migration 必须有 review 记录。
3. migration 必须说明 rollback plan；不可逆迁移必须单独审批。
4. autogenerate 只能辅助生成，不得自动应用。
5. schema_version 变更必须触发兼容性检查。
```

## 权限契约

```text
1. MCP/SearchLab 默认只读。
2. LLM audit 写入权限只能指向 llm_audit_result 或 proposed/review 队列。
3. final_gate_ledger 写入必须由 deterministic final gate 服务或人工审批动作完成。
4. 数据库账号、API key、交易账户密钥、私有账户字段不得写入业务表。
5. 写动作必须有 actor、reason、request_id 或 audit_trace_id。
```

## 生命周期契约

```text
1. retention policy 必须声明保留期、归档方式和删除条件。
2. 归档或删除不能破坏 audit replay。
3. incident 相关数据默认冻结，直到人工解除。
4. backup 不能只配置，必须定期 restore drill。
```

## 输出给 RAG/MCP 的最小建议字段

```text
table_role
primary_key
unique_key
required_time_fields
required_version_fields
audit_fields
append_only_required
allowed_writers
forbidden_writers
rollback_requirement
retention_requirement
```

## 不做什么

```text
1. 不创建真实数据库。
2. 不写生产 DDL。
3. 不执行迁移。
4. 不提供交易策略、买卖点、仓位、止损止盈建议。
5. 不允许 Vector DB 替代 canonical store。
6. 不允许 LLM audit 直接写 final_gate。
```

## 验收标准

```text
1. 覆盖核心表、时间字段、版本字段、审计字段、迁移、索引、权限和生命周期。
2. 明确 append-only 与可 update 范围。
3. 明确外接项目和 MCP/SearchLab 的只读/写权限边界。
4. 明确本契约不引入真实数据库实现。
5. UTF-8 无乱码。
```
