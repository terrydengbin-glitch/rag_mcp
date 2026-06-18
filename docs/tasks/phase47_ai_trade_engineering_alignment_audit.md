# Phase 47: AI/Trading Engineering 双主线归类与运行时一致性审计

## Phase 目标

Phase 47 用于系统审计当前知识库中 `AI Engineering` 和 `Trading Engineering` 两条主线的 L1/L2/L3 知识树归类、正式知识条目挂载、候选知识状态、Vue3 前端展示和 MCP Server 检索调用是否一致。

本 Phase 的目标不是新增知识，而是确认：

```text
1. AI Engineering 和 Trading Engineering 两条主线边界清楚。
2. L2 分区、L3 专题和知识点挂载正确。
3. 知识点内容、review_status、machine_gate、source、conflict 状态符合预期。
4. Vue3 知识树、候选页、SearchLab 页能正确显示和过滤。
5. MCP Server 能按节点、关键词和默认指导边界正常调用。
```

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-479 | P0 | done | 创建 Phase 47 任务卡、索引入口和审计契约 | `docs/tasks/phase47_ai_trade_engineering_alignment_audit.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-478 |
| CEK-TA-480 | P0 | done | 建立 AI/Trading 双主线知识树归类审计脚本 | `codex-expert-kit/rag/scripts/audit_ai_trade_engineering_tree_alignment.py`、`docs/reports/phase47_tree_alignment_audit_report.json` | CEK-TA-479 |
| CEK-TA-481 | P0 | done | 审计正式知识条目的分类、状态、来源、冲突和机器门控 | `docs/reports/phase47_formal_knowledge_classification_audit.json` | CEK-TA-480 |
| CEK-TA-482 | P1 | done | 审计候选知识和正式知识的队列关系、回链和重复挂载 | `docs/reports/phase47_candidate_formal_linkage_audit.json` | CEK-TA-480 |
| CEK-TA-483 | P1 | done | 审计 Vue3 前端知识树、候选页、SearchLab 页显示是否对齐 | `docs/reports/phase47_vue3_display_alignment_report.json` | CEK-TA-480 |
| CEK-TA-484 | P1 | done | 审计 MCP Server 对 AI/Trading 两条主线的检索、引用和阻断是否正常 | `docs/reports/phase47_mcp_runtime_alignment_report.json` | CEK-TA-480 |
| CEK-TA-485 | P1 | done | 整理发现的问题、修复建议和后续任务拆分 | `docs/reports/phase47_alignment_findings_and_fix_plan.md` | CEK-TA-481、CEK-TA-482、CEK-TA-483、CEK-TA-484 |
| CEK-TA-486 | P1 | done | 生成 Phase 47 验收报告并更新状态 | `docs/reports/phase47_ai_trade_engineering_alignment_audit_report.md` | CEK-TA-485 |

## 上游输入

```text
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/candidates/
codex-expert-kit/mcp/search_expert_knowledge.py
codex-expert-kit/mcp/server.py
ui/src/data/formalKnowledgeItems.ts
ui/src/data/phase23Candidates.ts
ui/src/data/knowledgeTreeNodes.ts
ui/src/views/KnowledgeTreeView.vue
ui/src/views/CandidateAuditView.vue
ui/src/views/SearchLabView.vue
docs/reports/phase41_final_acceptance_report.md
docs/reports/phase43_external_project_ai_memory_layer_report.md
docs/reports/phase45_trading_engineering_p1_completion_report.md
docs/reports/phase46_trading_engineering_regression_eval_report.md
```

## 下游输出

```text
1. AI/Trading 双主线 L1/L2/L3 归类审计报告。
2. 正式知识条目分类、状态、来源和 machine_gate 审计报告。
3. 候选知识与正式知识回链审计报告。
4. Vue3 前端展示一致性审计报告。
5. MCP Server 运行时检索和阻断审计报告。
6. 问题清单、修复建议和 Phase 47 验收报告。
```

## 输入契约

正式知识索引必须读取：

```text
codex-expert-kit/rag/indexes/knowledge_items.json
```

每条正式知识至少需要审计：

```text
knowledge_id
title
metadata.domain
metadata.subdomain
metadata.partition_id
metadata.tree_node_id
metadata.canonical_node_id
metadata.phase
review.review_status
review.approved_allowed
review.default_guidance_allowed
review.hard_gate_allowed
machine_gate.default_guidance
source_evidence
source_quality
conflict_audit.conflict_status
contribution.source_candidate_id
```

知识树节点至少需要审计：

```text
node_id
parent_id
level
label
branch
partition_id
topic_id
knowledge_count
candidate_count
status_summary
```

Vue3 fixture 至少需要审计：

```text
formalKnowledgeItems
phase23Candidates
knowledgeTreeNodes
```

MCP 检索至少需要审计：

```text
query
filters.canonical_node_id
filters.partition_id
include.reviewed
include.default_guidance_only
results[].knowledge_id
results[].source_count
results[].review_status
results[].machine_gate
blocked_results[]
errors
```

## 输出契约

每份审计报告必须包含：

```text
report_id
generated_at
task_id
scope
input_files
summary
checks
findings
errors
status
```

`status` 只能是：

```text
pass
warning
fail
```

问题项必须包含：

```text
finding_id
severity
component
knowledge_id 或 node_id
expected
actual
impact
suggested_fix
owner_phase
```

## 边界范围

范围内：

```text
1. 审计 AI Engineering 和 Trading Engineering 的 L1/L2/L3 归类。
2. 审计知识点是否挂到正确 canonical_node_id。
3. 审计知识点是否符合 reviewed/caveat_only、approved、default guidance、hard gate 的治理预期。
4. 审计候选知识和正式知识是否有回链、重复或状态错位。
5. 审计 Vue3 知识树和候选页是否能显示正确统计和中文文案。
6. 审计 MCP Server 是否能检索、返回来源并阻断不安全默认指导。
```

范围外：

```text
1. 不新增专业知识。
2. 不直接修改知识点内容。
3. 不直接调整知识树信息架构。
4. 不把 reviewed 升级为 approved。
5. 不启用 default guidance。
6. 不启用 hard gate。
7. 不改变 MCP tool 权限。
8. 不引入数据库或新后端框架。
9. 不生成买卖点、仓位、杠杆、止损止盈、风险阈值或实盘执行建议。
```

## 涉及组件

```text
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/candidates/
codex-expert-kit/rag/scripts/
codex-expert-kit/mcp/search_expert_knowledge.py
codex-expert-kit/mcp/server.py
ui/src/data/
ui/src/views/
docs/reports/
```

## 涉及数据结构

```text
FormalKnowledgeItem
CandidateKnowledgeItem
KnowledgeTreeNode
MCPSearchRequest
MCPSearchResponse
AlignmentFinding
AlignmentAuditReport
```

## 涉及数据库/存储

不引入数据库，不迁移存储层。继续使用文件化正式知识、候选知识、聚合索引和 Vue3 fixture。

## 实施步骤

```text
1. 固定 AI Engineering 和 Trading Engineering 预期 L1/L2/L3 节点清单。
2. 扫描 knowledge_items.json，按 canonical_node_id、partition_id、phase 和 review_status 聚合。
3. 识别跨主线误挂、L2/L3 缺失、孤儿节点、重复节点、候选/正式状态错位。
4. 检查 source_evidence、conflict_audit、machine_gate 和 review 权限是否符合预期。
5. 检查 Vue3 fixture 是否包含对应节点和知识，统计数字是否一致。
6. 使用 MCP/SearchLab 路径验证代表性查询、节点过滤、来源返回和 default_guidance_only 阻断。
7. 输出发现清单和修复建议。
8. 生成 Phase 47 验收报告并更新索引状态。
```

## Definition of Done

```text
1. Phase 47 任务卡存在并已写入 docs/index_tasks.md 和 docs/tasks/README.md。
2. AI/Trading 双主线归类审计脚本存在。
3. L1/L2/L3 节点覆盖审计报告存在。
4. 正式知识分类和 machine_gate 审计报告存在。
5. 候选知识和正式知识回链审计报告存在。
6. Vue3 显示一致性审计报告存在。
7. MCP Server 运行时检索审计报告存在。
8. 问题清单和修复建议存在。
9. 测试已执行。
10. 文档 UTF-8 无乱码。
11. 任务状态已更新。
```

## 测试与验收

必须执行：

```text
python codex-expert-kit/rag/scripts/audit_ai_trade_engineering_tree_alignment.py
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
python codex-expert-kit/rag/scripts/validate_trading_engineering_regression.py
npm --prefix ui run build
```

如 MCP Server 需要实机验证，优先使用只读检索脚本验证，不改变 MCP 权限。

## 风险与回滚

风险：

```text
1. AI Engineering 和 Trading Engineering 历史阶段命名不完全统一，可能产生 alias 误报。
2. Vue3 fixture 可能滞后于 knowledge_items，需要先重建再审计。
3. MCP Server 如果未启动，需要使用同构脚本验证 search_expert_knowledge。
4. 已有 approved seed 知识可能与 reviewed/caveat_only 统计口径不同，需要单独标注。
```

回滚：

```text
1. 本 Phase 首轮只新增审计脚本和报告，不修改正式知识内容。
2. 若报告误报，回滚或修正审计脚本和 alias mapping。
3. 若发现真实归类错误，另开修复任务卡，不在本审计任务中直接批量迁移。
```

## 需要开发者确认的问题

```text
1. 若发现 L1/L2/L3 信息架构需要调整，是否另开 Phase 进行知识树迁移。
2. 若发现 reviewed/caveat_only 需要升级为 approved，是否进入单独人工治理任务。
3. 是否要求 MCP Server 做真实进程级启动验收，还是使用同构只读脚本验收即可。
```
