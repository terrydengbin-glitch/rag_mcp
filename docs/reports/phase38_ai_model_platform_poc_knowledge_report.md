# Phase 38 AI 模型平台与交易 Gating/Scoring POC 知识扩展验收报告

## 验收范围

本报告验收 CEK-TA-273、CEK-TA-274、CEK-TA-275：

1. 将 Phase 38 已审计通过的候选知识沉淀为 formal reviewed 知识。
2. 重建正式知识索引和 Vue3 fixture。
3. 验证 KnowledgeTree、SearchLab/API、MCP 能按 Phase 38 子板块检索、引用、阻断和降级。

边界：本轮只进入 `reviewed` 与 `caveat_only`，不进入 `approved`，不打开默认指导，不作为 hard gate。

## 交付物

| 类型 | 路径 | 说明 |
| --- | --- | --- |
| 候选转 reviewed 脚本 | `codex-expert-kit/rag/scripts/promote_phase38_accepted_candidates_to_reviewed.py` | 只处理 Phase 38 accepted_for_draft 候选 |
| 运行时联动验证脚本 | `codex-expert-kit/rag/scripts/validate_phase38_runtime_linkage.py` | 覆盖索引、知识树、API/SearchLab 风格过滤和 MCP |
| 候选转 reviewed 报告 | `docs/reports/phase38_candidates_to_reviewed_promotion_report.json` | 记录 43 条正式知识沉淀结果 |
| 运行时联动报告 | `docs/reports/phase38_runtime_linkage_validation_report.json` | CEK-TA-274 验证报告，状态为 pass |
| 正式知识索引 | `codex-expert-kit/rag/indexes/knowledge_items.json` | 当前共 173 条正式知识 |
| Vue3 正式知识 fixture | `ui/src/data/formalKnowledgeItems.ts` | 当前共 173 条正式知识 |
| Vue3 候选 fixture | `ui/src/data/phase23Candidates.ts` | 当前共 164 条候选审计记录 |

## 知识沉淀结果

Phase 38 本轮共沉淀 43 条 formal reviewed 知识：

| 节点 | 数量 |
| --- | ---: |
| `kt.ai_engineering.numeric_scoring` | 7 |
| `kt.ai_engineering.calibration_threshold` | 7 |
| `kt.ai_engineering.decision_time_feature_contract` | 7 |
| `kt.ai_engineering.llm_audit_assistant` | 6 |
| `kt.ai_engineering.shadow_paper_ope_eval` | 6 |
| `kt.ai_engineering.model_release_governance` | 6 |
| `kt.rag_engineering.trading_scoring_rag_pack` | 4 |

全部 43 条均为：

```text
review_status = reviewed
machine_gate.default_guidance = caveat_only
review.default_guidance_allowed = false
```

原始被拒绝的 G04 空 slug 候选没有进入 formal knowledge；G04-R1 三审通过后作为正式 reviewed 知识进入 `kt.rag_engineering.trading_scoring_rag_pack`。

## 运行时验证

CEK-TA-274 验证结论：

```text
docs/reports/phase38_runtime_linkage_validation_report.json: pass
```

验证覆盖：

1. `knowledge_items.json` 中 Phase 38 正式知识数量为 43。
2. KnowledgeTree 中 Phase 38 新增 AI Engineering 子节点存在。
3. FastAPI/SearchLab 风格过滤能按节点返回 reviewed 知识。
4. MCP `search_expert_knowledge` 能返回来源、引用、review_status、machine_gate。
5. MCP `default_guidance_only=true` 会阻断 Phase 38 `caveat_only` 知识。
6. MCP 写入或审批权限请求会被拒绝。

## 测试结果

| 测试 | 结果 |
| --- | --- |
| `python codex-expert-kit/rag/scripts/validate_phase38_runtime_linkage.py` | pass |
| `python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py` | pass，173 条 |
| `python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py` | pass，0 污染 |
| `python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py` | pass |
| `python codex-expert-kit/rag/scripts/validate_no_mojibake.py` | pass，0 乱码 |
| `python -m pytest codex-expert-kit/api/tests` | 21 passed |
| `python -m pytest codex-expert-kit/mcp/tests` | 27 passed |
| `npm run build` | pass，存在 Vite chunk size 警告 |
| `npm run test:e2e` | 18 passed |

## 前端调整

验收过程中同步修复了 Vue3 审计工作台的用户可见英文：

1. KnowledgeTree e2e 从旧英文 `OPEN GAPS` 改为中文 `待补缺口`。
2. SearchLab 页面将 `Matches`、`Blocked`、`Warnings`、`score`、`sources` 等展示文案改为中文。
3. 候选跳转 e2e 改为直接访问目标知识树节点，避免与三级浏览点击测试重复和并发初始化抖动。

## 风险与后续

当前风险：

1. Phase 38 知识还不是 `approved`，只能作为可引用 reviewed 参考，不能作为默认指导。
2. Vite 构建存在 chunk size 警告，后续可单独拆分懒加载。
3. Phase 38 目前完成 P0-Core，P0-Extended / P1 仍需继续采集。
4. Trading Engineering 相关知识应继续走 Phase 37，不能混入 AI Engineering。

建议下一步：

1. 继续 Phase 38 P0-Extended / P1，补齐模型发布、监控、校准漂移、LLM 审计助手失败模式等知识。
2. 或进入 Phase 37，补 Trading Engineering 的 K 线、回测、fill model、风控和实盘执行本体知识。
