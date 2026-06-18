# Phase 47 AI/Trading Engineering 双主线归类与运行时一致性审计验收报告

## 结论

Phase 47 审计已完成，整体状态为 `warning`。

这表示当前系统没有发现 MCP 默认指导泄漏、无来源正式知识、候选回链断裂、Vue fixture 数量不同步等阻断性问题；但发现了需要后续修复的知识树节点/alias 与老知识卡 schema 显式性问题。

本 Phase 只做审计，不直接修改知识本体，不升级 `approved`，不启用 `default guidance`，不启用 `hard gate`。

## 交付物

```text
codex-expert-kit/rag/scripts/audit_ai_trade_engineering_tree_alignment.py
docs/reports/phase47_tree_alignment_audit_report.json
docs/reports/phase47_formal_knowledge_classification_audit.json
docs/reports/phase47_candidate_formal_linkage_audit.json
docs/reports/phase47_vue3_display_alignment_report.json
docs/reports/phase47_mcp_runtime_alignment_report.json
docs/reports/phase47_alignment_findings_and_fix_plan.md
docs/reports/phase47_ai_trade_engineering_alignment_audit_report.md
```

## 审计范围

```text
正式知识索引：codex-expert-kit/rag/indexes/knowledge_items.json
候选知识目录：codex-expert-kit/rag/candidates/
Vue3 正式知识 fixture：ui/src/data/formalKnowledgeItems.ts
Vue3 候选 fixture：ui/src/data/phase23Candidates.ts
Vue3 知识树 fixture：ui/src/data/knowledgeTreeNodes.ts
MCP 检索路径：codex-expert-kit/mcp/search_expert_knowledge.py
```

## 汇总结果

```text
正式知识总数：479
AI Engineering 相关正式知识：325
Trading Engineering 相关正式知识：152
其他支持层正式知识：2

候选知识文件：483
候选 fixture：483
正式知识 fixture：479
知识树节点 fixture：118
```

## 子报告状态

```text
phase47_tree_alignment_audit：warning
phase47_formal_knowledge_classification_audit：warning
phase47_candidate_formal_linkage_audit：pass
phase47_vue3_display_alignment：warning
phase47_mcp_runtime_alignment：pass
```

## 关键发现

### 1. AI/Trading 知识树节点存在缺口

审计发现 12 个预期 L2/L3 节点未在当前 `knowledgeTreeNodes.ts` 中直接出现，另有 19 个正式知识使用的 `canonical_node_id` 未直接出现在知识树 fixture。

影响：

```text
1. MCP 可以按正式知识检索到内容。
2. Vue3 可能无法按部分 canonical node 精准点击、统计或过滤。
3. 需要确认是应补知识树节点，还是应建立 alias 映射。
```

### 2. 正式知识 schema 显式性不足

一批历史 reviewed 知识虽然 `machine_gate.default_guidance = caveat_only`，运行时不会进入默认指导，但缺少显式的：

```text
review.approved_allowed = false
review.default_guidance_allowed = false
review.hard_gate_allowed = false
```

影响：

```text
1. 当前 MCP 运行时安全。
2. 迁移到其他 RAG 平台或外部索引时可能产生字段歧义。
3. 建议后续另开 schema backfill 修复任务，批量补齐显式字段。
```

### 3. 候选与正式知识回链正常

审计结果：

```text
formal_items_with_candidate_ref：469
missing_candidate_ref_count：0
duplicate_candidate_ref_count：0
```

说明候选到正式知识的回链没有发现断裂或重复沉淀问题。

### 4. Vue3 fixture 数量同步正常

审计结果：

```text
formal_index_count：479
formal_fixture_count：479
candidate_file_count：483
candidate_fixture_count：483
missing_formal_fixture_count：0
missing_candidate_fixture_count：0
```

说明正式知识和候选知识数据已经同步到前端 fixture。当前主要前端问题是部分 tree node / canonical node 不直接对应。

### 5. MCP Server 只读检索路径正常

审计验证了 AI 与 Trading 两条主线的代表性查询：

```text
AI numeric scoring
AI LLM audit assistant
Trading execution TCA
Trading order semantics
```

结果：

```text
empty_result_cases：0
source_failed_cases：0
default_guidance_leak_cases：0
```

说明 MCP/SearchLab 同构检索能返回结果、能带来源、能阻断 `caveat_only` 进入 `default_guidance_only`。

## 后续修复建议

建议拆成两个后续任务，不在 Phase 47 审计任务里直接修改：

```text
1. Phase 48：AI/Trading 知识树 canonical node 与 alias 对齐修复
   - 补齐缺失 L2/L3 节点
   - 或建立 explicit alias mapping
   - 重建 knowledgeTreeNodes.ts
   - 用 Playwright 检查前端点击/过滤/统计

2. Phase 49：正式知识 schema governance backfill
   - 为历史 reviewed 知识补齐 approved_allowed/default_guidance_allowed/hard_gate_allowed=false
   - 保持 machine_gate.default_guidance=caveat_only
   - 不升级 approved
   - 不启用 default guidance
```

## 测试

已执行或需执行的验收命令：

```text
python codex-expert-kit/rag/scripts/audit_ai_trade_engineering_tree_alignment.py
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
python codex-expert-kit/rag/scripts/validate_trading_engineering_regression.py
npm --prefix ui run build
```

## 边界

```text
本报告不是知识修复报告。
本报告不代表任何 reviewed 知识升级为 approved。
本报告不允许 default guidance。
本报告不允许 hard gate。
本报告不提供买卖点、仓位、杠杆、止损止盈、风险阈值或实盘执行建议。
```
