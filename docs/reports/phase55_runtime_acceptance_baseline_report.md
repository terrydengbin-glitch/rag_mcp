# Phase 55 MCP/SearchLab/Vue3 全链路运行时验收与知识库基线报告

## 结论

Phase 55 验收通过。

本次只做只读运行时验收和基线统计，不新增知识、不修改知识语义、不升级 `approved`，也不启用 `default guidance` 或 `hard gate`。

## 当前知识库基线

| 指标 | 数量 |
| --- | ---: |
| 正式知识总数 | 484 |
| reviewed / caveat_only | 474 |
| approved / allow | 10 |
| 缺少来源的正式知识 | 0 |
| confirmed conflict 知识 | 0 |
| 候选总数 | 488 |
| 已沉淀候选 | 474 |
| 已重建归档候选 | 14 |

基线报告：

```text
docs/reports/phase55_knowledge_base_baseline_report.json
```

## 运行时验收

`phase55_runtime_acceptance_report.json` 的 `gate_status` 为 `pass`。

已验证：

```text
1. MCP get_knowledge_item 可读取正式 reviewed 知识，并返回 source_evidence 与 machine_gate。
2. MCP browse_knowledge_tree 可读取 131 个知识树节点，与 UI fixture 数量一致。
3. MCP search_expert_knowledge 对 write_knowledge 权限请求返回 permission_denied。
4. default_guidance_only 不会返回 reviewed/caveat_only 知识。
5. SearchLab 等价检索可命中 AI Engineering 数值打分、Trading 回测、Trade Analysis、RAG/MCP 关键知识，并返回来源。
6. Vue3 formal fixture 与正式知识索引数量一致，均为 484。
7. 已沉淀候选均有 formal_knowledge_id 回链。
8. reviewed 知识没有开启 approved_allowed、default_guidance_allowed 或 hard_gate_allowed。
9. approved 知识 machine_gate 为 allow。
```

运行时报告：

```text
docs/reports/phase55_runtime_acceptance_report.json
```

## 观察项

Phase 55 记录到知识树节点统计与直接路径前缀复算存在差异。原因是知识树存在 canonical node、alias 和聚合统计口径，不适合用简单字符串前缀复算作为阻断门禁。

本项不阻断 Phase 55，权威阻断口径使用：

```text
python codex-expert-kit/rag/scripts/validate_knowledge_tree_alignment.py
```

该专用门禁本次已通过。

## 执行的测试

```text
python codex-expert-kit/rag/scripts/validate_phase55_runtime_acceptance.py
python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
python codex-expert-kit/rag/scripts/validate_knowledge_tree_alignment.py
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
npm --prefix ui run build
npx playwright test tests/e2e/audit-workbench.spec.ts tests/e2e/knowledge-tree-performance.spec.ts
```

结果：

```text
schema v1.1: pass
candidate workflow: pass
no mojibake: pass
knowledge tree alignment: pass
knowledge pollution: pass
Vue3 build: pass
Playwright: 26 passed
```

## 下游影响

外接项目现在可以把以下文件作为当前正式知识库可用基线：

```text
codex-expert-kit/rag/indexes/knowledge_items.json
docs/reports/phase55_knowledge_base_baseline_report.json
docs/reports/phase55_runtime_acceptance_report.json
```

MCP/SearchLab 应继续读取正式知识索引，不从 candidate 队列当默认知识读取。候选队列仍保留审计追踪和回链。

## 后续建议

下一步可以进入“知识库规模化运营”方向：把 Phase 55 的基线报告作为固定验收项，后续每次大批量知识扩充后都跑同一套 MCP/SearchLab/Vue3 全链路检查，再决定是否继续扩 AI Engineering、Trading Engineering 或外部项目接入能力。
