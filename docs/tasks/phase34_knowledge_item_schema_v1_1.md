# Phase 34: 知识卡片 Schema v1.1 与默认指导门禁升级

## Phase 目标

把 CEK-TA 正式知识卡片从 `schema_version = 1.0.0` 升级到可审计、可检索、可治理、可被 MCP/RAG 安全调用的 `schema_version = 1.1.0`。

本 Phase 不改变当前文件化知识库存储形态，不引入数据库；重点是补强知识卡片字段、统一机器门控规则，并让 MCP、FastAPI、Vue3、SearchLab 和其他项目接入都能读取同一套默认指导边界。

## 背景

当前正式知识项已经具备：

```text
knowledge_id
metadata
applicability
content
assumptions
source_evidence
source_quality
conflict_audit
review
contribution
```

但随着知识库进入可复用阶段，还需要补齐：

```text
claim_type
classification_notes
llm_usage_policy
machine_gate
recommended_extra_sources
```

这些字段用于解决：

```text
1. AI 不知道知识是交易信号、方法论约束还是风险边界。
2. tree_node_id 与 canonical_node_id 不一致时缺少解释。
3. reviewed / approved / default guidance 的边界需要更明确。
4. MCP/SearchLab/RAG 需要一个直接可读的机器门控字段。
5. Vue3 审计界面需要展示 AI 能怎么用、不能怎么用。
6. 后续来源增强需要有队列，不应直接把未核验来源写进 source_evidence。
```

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-164 | P0 | done | 定义 KnowledgeItem Schema v1.1 补强契约 | `codex-expert-kit/rag/knowledge_item_schema.md`、`docs/contracts/knowledge_item_schema_v1_1_contract.md` | CEK-TA-163 |
| CEK-TA-165 | P0 | done | 增加 claim_type、classification_notes、llm_usage_policy、machine_gate 字段规范 | `codex-expert-kit/rag/knowledge_item_schema.md`、`codex-expert-kit/rag/metadata_schema.md` | CEK-TA-164 |
| CEK-TA-166 | P0 | done | 批量升级正式知识卡片并保持向后兼容 | `codex-expert-kit/rag/knowledge/**/*.json` | CEK-TA-165 |
| CEK-TA-167 | P0 | done | 增加 machine_gate 生成与验证脚本 | `codex-expert-kit/rag/scripts/build_machine_gate.py`、`codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py` | CEK-TA-166 |
| CEK-TA-168 | P0 | done | 更新 MCP/SearchLab 默认指导门禁 | `codex-expert-kit/mcp/`、`codex-expert-kit/rag/searchlab/`、相关测试 | CEK-TA-167 |
| CEK-TA-169 | P1 | done | 更新 FastAPI 知识读取接口契约和返回字段 | `codex-expert-kit/api/`、`docs/contracts/knowledge_tree_reading_api_contract.md` | CEK-TA-167 |
| CEK-TA-170 | P1 | done | 更新 Vue3 知识详情和知识树审计栏展示 | `ui/src/types.ts`、`ui/src/views/KnowledgeTreeView.vue`、`ui/src/views/KnowledgeDetail.vue` | CEK-TA-169 |
| CEK-TA-171 | P1 | done | 建立 recommended_extra_sources 来源增强队列 | `docs/research/`、正式知识 JSON、来源增强任务模板 | CEK-TA-165 |
| CEK-TA-172 | P1 | done | 重建索引、fixture，并跑 API/MCP/Vue3 验收 | `knowledge_items.json`、`formalKnowledgeItems.ts`、测试报告、Phase 34 验收报告 | CEK-TA-168、CEK-TA-170 |

## 上游输入

```text
1. Phase 21 正式 knowledge_items.json 聚合索引。
2. Phase 22 path_resolver 路径解析规范。
3. Phase 28 FastAPI 只读知识树接口契约。
4. Phase 31/32 候选到 reviewed 的审计回写流程。
5. Phase 33 知识污染清理与门禁。
6. 当前正式知识文件：codex-expert-kit/rag/knowledge/**/*.json。
7. 当前正式知识 schema：codex-expert-kit/rag/knowledge_item_schema.md。
8. MCP/SearchLab 当前默认指导与阻断逻辑。
9. Vue3 当前知识树、知识详情、审计摘要展示字段。
```

## 下游输出

```text
1. 所有正式知识卡片具备 schema v1.1 的关键字段。
2. knowledge_items.json 聚合索引包含 llm_usage_policy 和 machine_gate。
3. MCP 查询结果明确返回 machine_gate/default_guidance 边界。
4. SearchLab 能显示该知识是否可作为默认指导。
5. FastAPI 只读接口返回 v1.1 字段，且老字段向后兼容。
6. Vue3 知识树和详情页显示 AI 使用策略、默认指导状态、阻断原因和分类说明。
7. 其他项目通过 MCP 调用时不会把 reviewed 当 approved。
8. 推荐补充来源进入增强队列，而不是未经核验直接进入 source_evidence。
```

## 输入契约

### 正式知识输入

每条正式知识仍然是一条独立 JSON 文件：

```text
codex-expert-kit/rag/knowledge/{partition_id}/{knowledge_id}.json
```

输入必须保留 v1.0 字段：

```text
schema_version
knowledge_id
title
metadata
applicability
content
assumptions
source_evidence
source_quality
conflict_audit
review
contribution
```

### v1.1 新增字段

新增字段必须兼容缺省值；旧知识在迁移前不能导致 API/MCP/Vue3 崩溃。

```json
{
  "metadata": {
    "claim_type": "risk_boundary_rule",
    "classification_notes": "string | null"
  },
  "llm_usage_policy": {
    "allowed": ["string"],
    "not_allowed": ["string"],
    "required_context": ["string"],
    "fallback_behavior": "deny | ask_for_context | cite_with_caveat"
  },
  "machine_gate": {
    "default_guidance": "allow | caveat_only | deny",
    "reason": "string",
    "requires_human_escalation": true,
    "blocking_reasons": ["string"],
    "checked_at": "YYYY-MM-DD",
    "gate_version": "1.0.0"
  },
  "recommended_extra_sources": [
    {
      "title": "string",
      "source_url": "string | null",
      "source_type": "paper | official_doc | exchange_rule | framework_doc | book | research_report | engineering_article",
      "purpose": "string",
      "status": "proposed | verified | rejected"
    }
  ]
}
```

## 输出契约

### machine_gate 判定规则

```text
allow:
  review.review_status = approved
  review.default_guidance_allowed = true
  conflict_audit.conflict_status in [none, resolved]
  source_evidence 至少 1 条
  source_quality.overall_reliability in [high, medium]
  freshness != deprecated
  contribution.private_data_removed = true
  未命中污染门禁

caveat_only:
  review.review_status = reviewed
  来源和冲突门禁通过
  但未经过 human approved 治理

deny:
  draft / rejected / deprecated
  无来源
  未解决冲突
  命中污染门禁
  私有数据未脱敏
  default_guidance_allowed = false
```

### MCP 输出

MCP 检索结果必须包含：

```text
knowledge_id
title
review_status
approval_status/default_guidance_allowed
machine_gate.default_guidance
machine_gate.reason
machine_gate.blocking_reasons
llm_usage_policy.allowed
llm_usage_policy.not_allowed
source_evidence/source_count
conflict_status
tree_node_id/canonical_node_id
```

MCP 默认指导模式只能返回 `machine_gate.default_guidance = allow` 的知识。`caveat_only` 可以在审计/研究模式返回，但必须带 caveat。

### SearchLab 输出

SearchLab 必须展示：

```text
default_guidance: allow | caveat_only | deny
why_allowed_or_blocked
required_context
not_allowed
source_count
conflict_status
```

### FastAPI 输出

FastAPI 只读接口必须在知识节点详情和知识条目列表中暴露：

```text
claim_type
classification_notes
llm_usage_policy
machine_gate
recommended_extra_sources_count
```

如果老知识暂缺 v1.1 字段，API 应返回兼容默认值，而不是返回 500。

### Vue3 输出

Vue3 至少显示：

```text
1. 知识类型 claim_type。
2. 默认指导状态 allow/caveat_only/deny。
3. AI 可以怎么用。
4. AI 不能怎么用。
5. 需要哪些上下文。
6. 分类说明 classification_notes。
7. 阻断原因 blocking_reasons。
8. 推荐补充来源数量和状态。
```

## 边界范围

### 本 Phase 做

```text
1. 升级知识 schema 到 v1.1。
2. 批量补齐正式知识字段。
3. 增加 machine_gate 生成和验证。
4. 更新索引生成和前端 fixture。
5. 更新 MCP/SearchLab/FastAPI/Vue3 读取和展示。
6. 增加测试和验收报告。
```

### 本 Phase 不做

```text
1. 不引入数据库。
2. 不把 reviewed 自动升级为 approved。
3. 不直接把 recommended_extra_sources 写成 source_evidence。
4. 不新增外部服务依赖。
5. 不改变候选知识到 reviewed 的状态语义。
6. 不删除历史审计记录。
7. 不改变 MCP tool 权限，只加强默认指导过滤。
```

## 涉及组件

```text
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/metadata_schema.md
codex-expert-kit/rag/knowledge/**/*.json
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/scripts/build_knowledge_items_index.py
codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py
codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
codex-expert-kit/mcp/
codex-expert-kit/api/
ui/src/types.ts
ui/src/data/formalKnowledgeItems.ts
ui/src/views/KnowledgeTreeView.vue
ui/src/views/KnowledgeDetail.vue
ui/tests/e2e/audit-workbench.spec.ts
```

## 涉及数据结构

```text
KnowledgeItem
KnowledgeItem.metadata
LlmUsagePolicy
MachineGate
RecommendedExtraSource
KnowledgeTreeNodeViewModel
McpKnowledgeSearchResult
FastApiKnowledgeItemResponse
Vue KnowledgeItem type
```

## 涉及数据库/存储

当前仍采用文件化存储：

```text
1. 单条正式知识：codex-expert-kit/rag/knowledge/**/*.json
2. 聚合索引：codex-expert-kit/rag/indexes/knowledge_items.json
3. 前端 fixture：ui/src/data/formalKnowledgeItems.ts
```

本 Phase 不引入数据库。如果后续要引入 SQLite/Postgres/向量库，必须另开 Phase 并先定义 schema、迁移和回滚。

## 实施步骤

```text
1. 定义 v1.1 契约文档。
2. 更新 knowledge_item_schema.md 和 metadata_schema.md。
3. 实现 machine_gate 生成规则。
4. 批量迁移正式知识 JSON。
5. 增加 v1.1 schema 验证脚本。
6. 更新 knowledge_items.json 构建脚本。
7. 更新 MCP/SearchLab 默认指导过滤和返回结构。
8. 更新 FastAPI response model 和测试。
9. 更新 Vue3 类型、知识树、详情页展示。
10. 重建索引和前端 fixture。
11. 运行污染门禁、candidate workflow 门禁、API/MCP/Vue3 测试。
12. 生成 Phase 34 验收报告。
13. 更新 docs/index_tasks.md 和 docs/tasks/README.md 状态。
```

## Definition of Done

```text
1. Phase 34 任务卡已登记到 docs/index_tasks.md 和 docs/tasks/README.md。
2. v1.1 契约文档存在并说明字段、枚举、默认值和兼容策略。
3. 所有正式知识卡片都能通过 v1.1 验证。
4. machine_gate 能稳定生成 allow/caveat_only/deny。
5. reviewed 不会被误判为 approved。
6. MCP 默认指导只返回 allow。
7. SearchLab 能展示 caveat 和 deny 原因。
8. FastAPI 对缺失 v1.1 字段有兼容默认值。
9. Vue3 能展示 AI 使用策略和默认指导门禁。
10. knowledge_items.json 和 formalKnowledgeItems.ts 已重建。
11. 污染门禁继续通过。
12. API/MCP/Vue3 测试通过。
13. Phase 34 验收报告存在。
```

## 测试与验收

### 文档与 schema

```text
1. UTF-8 读取 docs 和 schema 文档无乱码。
2. v1.1 字段契约完整。
3. 枚举值和默认值有说明。
```

### 知识数据

```text
python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
```

### 索引和 fixture

```text
python codex-expert-kit/rag/scripts/build_knowledge_items_index.py
python codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py
```

### API/MCP

```text
python -m pytest codex-expert-kit/api/tests codex-expert-kit/mcp/tests
```

### Vue3

```text
cd ui
npm run build
npm run test:e2e
```

## 风险与回滚

### 风险

```text
1. v1.1 字段补齐不完整导致 API 或 Vue3 空字段显示异常。
2. MCP 默认指导门禁过严，导致可用知识减少。
3. reviewed/approved 语义被误改，影响治理安全。
4. recommended_extra_sources 被误当成正式 source_evidence。
```

### 回滚

```text
1. 保留 v1.0 字段不删除，v1.1 为增量字段。
2. 若 v1.1 迁移失败，可回退到旧 knowledge_items.json 和 formalKnowledgeItems.ts。
3. machine_gate 脚本只生成字段，不删除 source/review/conflict 原始信息。
4. MCP/FastAPI/Vue3 必须支持缺省字段兼容。
```

## 需要开发者确认的问题

```text
1. 是否确认 reviewed 只能是 caveat_only，不能作为默认指导 allow？
2. 是否确认 approved 升级必须单独开人工治理任务？
3. 是否确认 recommended_extra_sources 只作为待核验来源增强队列，不进入正式 source_evidence？
4. 是否需要在 Vue3 中增加“申请 approved 治理”的人工动作入口？
```

## 状态更新要求

完成本 Phase 时必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase34_knowledge_item_schema_v1_1.md
docs/reports/phase34_knowledge_item_schema_v1_1_report.md
```

