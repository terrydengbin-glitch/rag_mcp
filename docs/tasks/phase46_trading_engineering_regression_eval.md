# Phase 46: Trading Engineering 知识回归评测

## Phase 目标

Phase 46 用来把 Phase 37 和 Phase 45 已沉淀的 Trading Engineering 知识变成可持续回归评测对象，验证知识库在 MCP/SearchLab/KnowledgeTree/Vue3 中是否能稳定命中、返回来源、保持分支边界，并阻断 `approved/default guidance/hard gate` 误用。

本 Phase 不新增交易知识，不升级 `approved`，不启用默认指导，只做检索质量、引用完整性、边界阻断和跨分支归类回归。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-474 | P0 | done | 创建 Phase 46 任务卡、索引入口和评测契约 | `docs/tasks/phase46_trading_engineering_regression_eval.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-473 |
| CEK-TA-475 | P0 | done | 建立 Trading Engineering 回归评测集和验证脚本 | `codex-expert-kit/rag/scripts/validate_trading_engineering_regression.py`、`docs/reports/phase46_trading_engineering_regression_report.json` | CEK-TA-474 |
| CEK-TA-476 | P1 | done | 扩展 SearchLab/MCP 检索案例，覆盖 13 个 Trading 分区和 Phase 45 扩展节点 | `docs/reports/phase46_searchlab_case_matrix.json` | CEK-TA-475 |
| CEK-TA-477 | P1 | done | 增加 Vue3 知识树与候选队列一致性验收 | `docs/reports/phase46_vue_tree_candidate_consistency_report.json` | CEK-TA-475 |
| CEK-TA-478 | P1 | done | 生成 Phase 46 验收报告并更新状态 | `docs/reports/phase46_trading_engineering_regression_eval_report.md` | CEK-TA-476、CEK-TA-477 |

## 上游输入

```text
docs/reports/phase37_trading_engineering_knowledge_expansion_report.md
docs/reports/phase45_trading_engineering_p1_completion_report.md
docs/reports/phase45_runtime_linkage_report.json
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/mcp/search_expert_knowledge.py
ui/src/data/formalKnowledgeItems.ts
ui/src/data/knowledgeTreeNodes.ts
ui/src/data/phase23Candidates.ts
```

## 下游输出

```text
1. Trading Engineering 回归评测脚本。
2. MCP/SearchLab 检索案例矩阵。
3. 知识树、候选队列、正式知识索引一致性报告。
4. Phase 46 验收报告。
```

## 输入契约

评测脚本必须读取正式知识聚合索引：

```text
codex-expert-kit/rag/indexes/knowledge_items.json
```

每条正式知识至少需要：

```text
knowledge_id
title
metadata.canonical_node_id
metadata.phase
review.review_status
machine_gate.default_guidance
source_evidence
conflict_audit.conflict_status
```

## 输出契约

回归报告必须包含：

```text
report_id
generated_at
task_id
inventory
search_cases
default_guidance_block
boundary_checks
vue_fixture_checks
errors
status
```

`status` 只能是：

```text
pass
fail
```

## 边界范围

范围内：

```text
1. 验证正式知识是否可检索、可引用、可阻断。
2. 验证 Trading Engineering 节点覆盖是否可见。
3. 验证 reviewed/caveat_only 不会进入 default guidance。
4. 验证中文、来源、冲突、污染和索引一致性。
```

范围外：

```text
1. 不新增专业知识。
2. 不把 reviewed 升级为 approved。
3. 不启用 default guidance。
4. 不启用 hard gate。
5. 不生成交易建议、仓位、杠杆、止损止盈或风险阈值。
6. 不改变 MCP 权限。
```

## 涉及组件

```text
codex-expert-kit/rag/scripts/
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/mcp/search_expert_knowledge.py
docs/reports/
ui/src/data/
```

## 涉及数据结构

```text
FormalKnowledgeItem
knowledge_items index
MCP search request
MCP search response
RegressionCase
RegressionReport
```

## 涉及数据库/存储

不引入数据库，不迁移存储层。继续使用文件化索引和 Vue3 fixture。

## 实施步骤

```text
1. 创建 Phase 46 任务卡和索引入口。
2. 建立第一版 Trading Engineering 回归评测脚本。
3. 运行 MCP/SearchLab 检索案例，检查命中、来源、review_status 和 machine_gate。
4. 检查 default_guidance_only 是否阻断 reviewed/caveat_only。
5. 检查 Vue3 fixture 是否包含代表性知识和知识树节点。
6. 输出报告。
7. 后续扩展 13 分区完整 case matrix。
```

## Definition of Done

```text
1. Phase 46 任务卡存在并已写入索引。
2. 回归评测脚本存在。
3. 回归报告存在。
4. 至少覆盖 Quant Foundation、Data Engineering、Market Microstructure、Backtest、Replay、Live Execution、Risk、Trade Analysis、Phase 45 扩展节点。
5. 每个检索结果必须返回来源。
6. reviewed/caveat_only 不得进入 default guidance。
7. 文档和报告 UTF-8 无乱码。
8. 任务状态已更新。
```

## 测试与验收

必须执行：

```text
python codex-expert-kit/rag/scripts/validate_trading_engineering_regression.py
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
```

如涉及前端变更，再执行：

```text
npm --prefix ui run build
```

## 风险与回滚

风险：

```text
1. 检索 case 太少，不能代表所有 Trading Engineering 分支。
2. 关键词过窄导致误判检索失败。
3. 旧 Phase 的节点命名不完全统一。
```

回滚：

```text
1. 不修改正式知识内容。
2. 只回滚评测脚本和报告。
3. 保留失败报告，用于后续补 case 或修索引。
```

## 需要开发者确认的问题

```text
1. 是否要把 Phase 46 回归评测接入 CI。
2. 是否要把 SearchLab UI 加入人工可视化评测面板。
3. 是否要把失败 case 自动生成候选修复任务。
```
