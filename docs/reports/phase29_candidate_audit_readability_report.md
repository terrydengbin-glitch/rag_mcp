# Phase 29 候选知识人工审核阅读体验优化验收报告

## 验收结论

Phase 29 已完成。候选知识审计页已从原有“队列 + 详情”升级为更适合人工审核的三栏工作台：

```text
左侧：候选队列、风险标签、筛选、分页
中间：候选正文、适用边界、来源证据、冲突审计、draft 转换预览
右侧：人工审核 checklist、风险摘要、治理门、CEK-TA-102 handoff
```

本 Phase 没有改变候选知识生命周期，没有开放写入正式知识库，没有开放 MCP 写权限，也没有引入数据库。

## 完成任务

| ID | 状态 | 交付物 |
| --- | --- | --- |
| CEK-TA-134 | done | `docs/tasks/phase29_candidate_audit_readability_workbench.md` |
| CEK-TA-135 | done | `docs/contracts/candidate_audit_readability_contract.md` |
| CEK-TA-136 | done | `ui/src/views/IngestionReview.vue`、`ui/src/styles.css` |
| CEK-TA-137 | done | `ui/src/components/CandidateAuditChecklistPanel.vue`、`ui/src/views/IngestionReview.vue` |
| CEK-TA-138 | done | `ui/src/views/IngestionReview.vue`、`ui/src/styles.css` |
| CEK-TA-139 | done | `codex-expert-kit/api/`、`codex-expert-kit/api/tests/test_candidate_audit_api_contract.py` |
| CEK-TA-140 | done | `ui/tests/e2e/audit-workbench.spec.ts`、本报告 |

## 前端变更

```text
1. 候选页采用三栏审核工作台。
2. 候选队列增加 risk_low/risk_medium/risk_high/risk_blocked 标签。
3. 候选队列增加 risk filter、page size 和分页控件。
4. 中间正文区展示 claim、evidence summary、tree/canonical/source/target 和适用边界。
5. 右侧增加人工审核 checklist、阻断/缺口、下一步动作和 CEK-TA-102 handoff。
6. candidate/draft 仍只作为审核对象，不作为 approved 或默认指导。
```

## API 变更

新增只读候选 API：

```text
GET /api/candidates
GET /api/candidates/{candidate_id}
```

能力：

```text
1. 通过 path resolver 读取 codex-expert-kit/rag/candidates/**/*.json。
2. 支持 q、partition_id、tree_node_id、candidate_status、conflict_status、risk_level、limit、offset。
3. 返回归一化 CandidateReadableViewModel、source_refs 和 checklist。
4. 错误响应保留 error_code，并补齐 code/retryable 字段。
5. 不提供 POST/PUT/PATCH/DELETE。
```

## 边界确认

```text
1. 不直接写 codex-expert-kit/rag/knowledge/。
2. 不把 candidate、proposed、draft 显示为 approved。
3. 不绕过 CEK-TA-102。
4. 不开放 MCP 写权限。
5. 不引入数据库。
6. 不采集行情、K 线、订单簿或交易原始数据。
```

## 测试结果

```text
npm run build
结果：通过

python -m pytest codex-expert-kit\api\tests
结果：15 passed

npm run test:e2e
结果：18 passed
```

Playwright 覆盖：

```text
1. 候选页、知识树页、SearchLab 页桌面/移动端渲染。
2. 候选页 checklist、风险过滤、分页和 handoff 区域。
3. 知识树跳转候选页 tree_node_id 过滤。
4. 知识树三级浏览、13 分区一致性和阅读布局。
5. 无空白页、无横向溢出。
```

## 风险与回滚

风险：

```text
1. 候选 API 当前读取文件化候选包，不做持久化审核动作。
2. 浏览器端审核动作仍以 handoff 导出为主，尚未实现审核历史写入。
3. Phase 29 仅完成只读候选入口，未将 Vue3 候选页切换为 API-first 数据源。
```

回滚：

```text
1. 前端可回退 IngestionReview.vue 到 Phase 24 版本。
2. 删除 CandidateAuditChecklistPanel.vue 引用即可移除 checklist 面板。
3. 候选 API 为只读新增路由，移除 /api/candidates 路由不影响知识树 API。
4. 所有候选源文件和正式知识目录未被修改。
```

## 后续建议

```text
1. 下一 Phase 可把 Vue3 候选页数据源从 fixture 切到 FastAPI + fixture fallback。
2. 再后续可增加本地审核记录文件，但必须先定义写入契约和权限边界。
3. 可把候选 checklist 结果纳入 SearchLab 阻断审计展示。
```
