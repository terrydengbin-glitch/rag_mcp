# Phase 59: Microstructure Feature Store & Hybrid Snapshot Contract

## Phase 目标

Phase 59 用于补齐 Trading AI 数据架构中“低频 K 线 snapshot、高频 microstructure 原始/聚合数据、训练 dataset snapshot manifest、中央 canonical registry / audit ledger”之间的边界。

核心结论：

```text
不要把 K 线 snap 和 microstructure 原始/高频数据强行混在一个物理表或一个宽表里；
也不要按 AI Trader 物理分库；
应按数据粒度、写入频率、查询模式和审计需求物理分层，
再通过 dataset snapshot manifest 做 point-in-time 逻辑组合。
```

本 Phase 先创建候选知识、契约和审计包；只有在 reviewed/caveat_only 准备审计通过后，才允许沉淀为 formal reviewed/caveat_only。全程不得创建 approved、default guidance 或 hard gate。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-563 | P0 | done | 创建 Phase 59 任务卡与索引入口 | `docs/tasks/phase59_microstructure_feature_store_hybrid_snapshot.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-562 |
| CEK-TA-564 | P0 | done | 搜索专业资料并梳理 feature store、partition evolution、高写入时序存储、kdb+ tick 架构案例 | `docs/research/phase59_microstructure_feature_store_hybrid_snapshot_research.md` | CEK-TA-563 |
| CEK-TA-565 | P0 | done | 定义 Microstructure Feature Store & Hybrid Snapshot Contract | `docs/contracts/phase59_microstructure_feature_store_hybrid_snapshot_contract.md` | CEK-TA-564 |
| CEK-TA-566 | P0 | done | 创建 3 条候选知识卡：物理分层、hybrid dataset manifest、canonical registry 不按 Trader 分库 | `codex-expert-kit/rag/candidates/KB_03_MARKET_MICROSTRUCTURE/`、`codex-expert-kit/rag/candidates/KB_AI_26_DATABASE_STORAGE/` | CEK-TA-565 |
| CEK-TA-567 | P0 | done | 导出 Phase 59 候选 AI 审计包并运行 JSON/UTF-8/边界质量门禁 | `docs/audit/phase59_microstructure_feature_store_candidate_audit_package_20260617.json`、`docs/reports/phase59_microstructure_feature_store_candidate_quality_gate.json` | CEK-TA-566 |
| CEK-TA-568 | P0 | done | 导入 Phase 59 严格审计结果，三条候选升级为 accepted_for_draft 并按补丁收窄边界 | `docs/audit/audit_result_phase59_microstructure_feature_store_candidate_20260617_strict_v1.json`、`docs/reports/phase59_candidate_audit_import_report.json`、3 条 Phase 59 candidate JSON | CEK-TA-567 |
| CEK-TA-569 | P0 | done | 导出 Phase 59 reviewed/caveat_only 准备审计包，阻止 accepted_for_draft 直接入 formal reviewed | `docs/audit/phase59_reviewed_preparation_audit_package_20260617.json`、`docs/reports/phase59_reviewed_preparation_gap_report.json` | CEK-TA-568 |
| CEK-TA-570 | P0 | done | 导入 Phase 59 reviewed/caveat_only 审计结果，三条候选沉淀为 formal reviewed/caveat_only 并重建索引 | `docs/audit/audit_result_phase59_reviewed_preparation_20260617_strict_v1.json`、`docs/reports/phase59_reviewed_preparation_import_report.json`、`codex-expert-kit/rag/knowledge/KB_03_MARKET_MICROSTRUCTURE/kb_phase59_market_microstructure.kline_microstructure_store_separation_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_AI_26_DATABASE_STORAGE/kb_phase59_database_storage.hybrid_training_dataset_snapshot_manifest_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_AI_26_DATABASE_STORAGE/kb_phase59_database_storage.canonical_registry_not_per_trader_db_required.v1.json` | CEK-TA-569 |

## 上游输入

```text
用户提出的 Kline Snapshot Store / Microstructure Store / Training Dataset Snapshot 架构建议
docs/contracts/phase42_database_storage_contract.md
docs/contracts/phase38_training_data_and_eval_contract.md
Phase 37 Market Microstructure formal reviewed 知识
Phase 42 Database / Storage Engineering formal reviewed 知识
Feast、Apache Iceberg、ClickHouse、KX/kdb+ 官方资料
```

## 下游输出

```text
1. 一份专业资料研究报告。
2. 一份 hybrid snapshot contract。
3. 三条候选知识卡，进入候选审计队列。
4. 一份 AI 审计包，可交给外部 AI/人工严格审计。
5. 一份质量门禁报告，确认候选阶段未直接创建 reviewed/approved/default guidance/hard gate。
6. reviewed/caveat_only 审计通过后，三条 formal reviewed/caveat_only 知识进入正式索引和 Vue3 知识树。
```

## 输入契约

```text
1. 所有候选必须有来源、适用范围、不适用范围、冲突审计和 machine gate。
2. 必须区分 Trading Engineering 本体知识与 AI/Database Engineering 存储契约知识。
3. 不得把 ClickHouse、kdb+、Feast、Iceberg 写成强制依赖。
4. 不得把 microstructure 原始数据直接写成训练样本输入。
5. 不得按 AI Trader 建议物理分库；只能保留 unit_id / unit_version 等逻辑隔离。
```

## 输出契约

### 候选知识卡

必须包含：

```text
candidate_id
research_task_id
status
classification
claim
applicability
contract_refs
source_refs
source_quality
conflict_audit
llm_usage_policy
machine_gate
review
```

### 审计包

必须包含：

```text
审计目标
硬边界
候选知识正文
来源列表
契约摘要
需要外部 AI 搜索核验的问题
输出 schema
```

## 边界范围

范围内：

```text
1. 定义 Kline Snapshot Store、Microstructure Store、Feature Store、Dataset Snapshot Manifest 和 Canonical Registry / Audit Ledger 的关系。
2. 定义按数据粒度、写入频率和审计需求物理分层的原则。
3. 定义训练时通过 point-in-time manifest 逻辑组合 kline + micro features。
4. 明确 micro 原始数据、micro 聚合特征、K 线 snap 和训练样本之间的边界。
```

范围外：

```text
1. 不创建真实数据库或迁移。
2. 不引入新的后端框架或数据库依赖。
3. 不创建 formal reviewed、approved、default guidance 或 hard gate。
4. 不生成交易策略、买卖点、仓位、杠杆、止损止盈或实盘执行建议。
5. 不要求所有项目必须使用 ClickHouse、kdb+、Feast、Iceberg、DuckDB、SQLite、Parquet 或任何单一技术。
```

## 涉及组件

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase59_microstructure_feature_store_hybrid_snapshot.md
docs/research/
docs/contracts/
docs/audit/
docs/reports/
codex-expert-kit/rag/candidates/KB_03_MARKET_MICROSTRUCTURE/
codex-expert-kit/rag/candidates/KB_AI_26_DATABASE_STORAGE/
ui/src/data/phase23Candidates.ts
ui/public/data/phase23Candidates.json
```

## 涉及数据结构

```text
CandidateKnowledgeItem schema v1.1 candidate
MicrostructureFeatureStoreContract
HybridTrainingDatasetSnapshotManifest
AI audit package JSON
Quality gate JSON
```

## 涉及数据库/存储

```text
本 Phase 不创建真实数据库。
只定义候选知识中的存储设计契约：canonical registry / audit ledger、kline snapshot store、microstructure store、feature store、dataset snapshot manifest。
```

## 实施步骤

```text
1. 创建 Phase 59 任务卡和索引入口。
2. 搜索并归纳 Feast、Iceberg、ClickHouse、KX/kdb+ 等官方/专业资料。
3. 对齐 Phase 38 / Phase 42 现有契约，避免重复和越界。
4. 创建 Microstructure Feature Store & Hybrid Snapshot Contract。
5. 创建 3 条候选知识卡。
6. 导出 AI 审计包。
7. 运行 JSON、UTF-8、候选边界和默认指导门禁。
8. 重建候选 Vue3 fixture，让候选页可见。
```

## Definition of Done

```text
1. Phase 59 任务卡存在。
2. docs/index_tasks.md 和 docs/tasks/README.md 已更新。
3. 研究报告存在并包含来源链接。
4. 契约文档存在，字段、owner、边界和不做什么清晰。
5. 三条候选知识卡存在，来源、适用范围、不适用范围、冲突状态和 review 状态齐全。
6. 审计包存在，明确不得直接 reviewed/approved/default guidance/hard gate。
7. JSON 可解析，中文 UTF-8 无乱码。
8. 候选进入 Vue3 候选 fixture，但未进入正式 knowledge_items.json。
```

## 测试与验收

```text
1. python -m json.tool 校验候选 JSON。
2. python -m json.tool 校验审计包 JSON。
3. python -m json.tool 校验质量门禁 JSON。
4. UTF-8 读取关键中文文档。
5. 检查候选 machine_gate.default_guidance=deny。
6. 检查正式知识索引不包含 Phase 59 候选。
```

## 风险与回滚

风险：

```text
1. 该主题跨 Trading Engineering 与 AI/Database Engineering，归类不当会污染分支边界。
2. 官方资料是平台/技术实现模式，不应被写成 CEK-TA 强制技术栈。
3. 如果外部 AI 审计认为来源不足，需要补 venue-specific microstructure 数据案例。
```

回滚：

```text
1. 删除 Phase 59 新增候选、研究报告、契约、审计包和质量报告。
2. 从 docs/index_tasks.md 和 docs/tasks/README.md 移除 Phase 59 入口。
3. 重建 ui 候选 fixture。
4. 不影响正式 knowledge_items.json，因为本 Phase 不写正式知识索引。
```

## 需要开发者确认的问题

```text
1. 外部审计通过后，是否将三条候选沉淀为 formal reviewed/caveat_only。
2. 是否需要为 ClickHouse/kdb+/Feast/Iceberg 分别创建 implementation pattern 示例知识。
3. 是否需要后续扩展真实 DDL / migration phase。
```

## 状态更新要求

```text
完成后更新 docs/index_tasks.md、docs/tasks/README.md 和本任务卡状态。
```
