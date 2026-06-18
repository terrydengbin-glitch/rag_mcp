# Phase 33: 知识库污染清理与门禁

## Phase 目标

清理正式知识库中由 mock、demo、test、fixture、内部占位文档或项目开发规则污染形成的知识点，确保 `codex-expert-kit/rag/knowledge/**/*.json`、`knowledge_items.json`、MCP/SearchLab 和 Vue3 知识树只默认暴露可复用、可审计、来源可靠的专业知识。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-158 | P0 | done | 定义知识污染判定契约 | `docs/contracts/knowledge_pollution_cleanup_contract.md` |
| CEK-TA-159 | P0 | done | 扫描正式知识库污染候选并生成报告 | `docs/reports/phase33_knowledge_pollution_scan_report.json` |
| CEK-TA-160 | P0 | done | 从正式知识库移除 mock/test/internal-only 污染知识点 | `codex-expert-kit/rag/knowledge/` |
| CEK-TA-161 | P0 | done | 增加知识污染质量门禁 | `codex-expert-kit/rag/scripts/validate_knowledge_pollution.py` |
| CEK-TA-162 | P1 | done | 重建索引、Vue3 fixture 并验证知识树/MCP/SearchLab | `knowledge_items.json`、`formalKnowledgeItems.ts`、测试报告 |
| CEK-TA-163 | P1 | done | 生成 Phase 33 验收报告并更新索引 | `docs/reports/phase33_knowledge_pollution_cleanup_report.md` |

## 上游输入

```text
1. Phase 21 正式知识聚合索引。
2. Phase 32 候选到 reviewed 知识回写结果。
3. Vue3 知识树正式知识 fixture。
4. MCP/SearchLab 默认检索正式知识索引。
```

## 下游输出

```text
1. 正式知识库不再包含 mock/demo/test/fixture/internal-only 污染知识点。
2. Vue3 知识树只读取正式知识 fixture，不把 mockData 当成知识库事实。
3. MCP/SearchLab 不返回被污染条目。
4. 后续知识沉淀会被污染门禁阻断。
```

## 输入契约

正式知识输入：

```yaml
knowledge_id: string
metadata.domain: string
metadata.subdomain: string
source_evidence: array
source_evidence[].source_type: string
source_evidence[].publisher: string
source_evidence[].source_url: string | null
review.review_status: draft | reviewed | approved | rejected | deprecated
```

污染判定关键词：

```text
mock, demo, fixture, sample, test-only, placeholder, internal-only, fake, synthetic
```

## 输出契约

扫描报告：

```yaml
report_id: phase33_knowledge_pollution_scan
scanned_count: number
polluted_count: number
polluted_items:
  - knowledge_id: string
    path: string
    reasons: string[]
    action: remove_from_formal_knowledge | keep
```

## 边界范围

范围内：

```text
1. 清理正式知识 JSON。
2. 重建正式知识索引。
3. 重建 Vue3 正式知识 fixture。
4. 增加污染检测脚本。
5. 验证 MCP/API/Vue3 不受污染。
```

范围外：

```text
1. 不删除候选审计源文件。
2. 不删除 UI mockData fallback，除非它进入正式索引。
3. 不把 reviewed 自动提升 approved。
4. 不联网补新知识。
5. 不重构知识树信息架构。
```

## 涉及组件

```text
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/scripts/build_knowledge_items_index.py
codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py
codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
ui/src/data/formalKnowledgeItems.ts
ui/src/data/mockData.ts
ui/src/stores/auditStore.ts
codex-expert-kit/mcp/tests/
codex-expert-kit/api/tests/
ui/tests/e2e/
```

## Definition of Done

```text
1. 污染判定契约存在。
2. 扫描报告存在。
3. 污染知识点已从正式知识库移除或明确保留原因。
4. 正式索引和 Vue3 fixture 已重建。
5. 污染门禁脚本通过。
6. Phase 32 candidate/reviewed/approved 边界仍通过。
7. API、MCP、Vue3 build、Playwright 通过。
8. Phase 33 验收报告存在。
9. docs/index_tasks.md 和 docs/tasks/README.md 已更新。
```

## 测试与验收

```text
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
python codex-expert-kit/rag/scripts/build_knowledge_items_index.py
python codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py
python -m pytest codex-expert-kit/api/tests codex-expert-kit/mcp/tests
npm run build
npm run test:e2e
```

## 风险与回滚

风险：

```text
1. 误删项目治理类知识，导致 Project Support 分支覆盖率下降。
2. 旧测试期望依赖被清理条目。
3. 知识树节点计数需要同步重建。
```

回滚：

```text
1. 从删除记录恢复对应 JSON。
2. 重建 knowledge_items.json 和 formalKnowledgeItems.ts。
3. 重新运行污染门禁和 MCP/API/Vue3 测试。
```

