# Phase 36: AI Engineering 交易 LLM Gating/Scoring 知识扩展

## Phase 目标

为第一个外接项目“训练 LLM 进行交易 gating/scoring，提高交易质量（R/R、胜率、PnL、风险过滤质量等）”建立 AI Engineering 专业知识扩展任务。

本 Phase 只负责把 AI Engineering 知识树、采集队列、契约、上下游、MCP/FastAPI/Vue3 对齐任务拆清楚。后续每条知识必须经过联网采集、来源评分、冲突审计、候选审核、正式 reviewed/approved 治理流程，不能直接写成默认指导。

AI Engineering 必须分成两层：

```text
通用 LLM / ML Training Engineering
  -> 交易数据到训练数据的 schema 转换链路
  -> 交易 LLM 任务分类和训练方法选择
  -> 交易 gating / scoring 专用训练约束
  -> 合格 LLM 交易质量审计助手业务闭环
```

也就是说，CEK-TA 不仅要告诉外接项目“交易 LLM 不能越权”，还要告诉它“如何正确构造数据集、如何把交易记录转换成训练样本、如何选择训练方法、做 eval、管理训练运行、避免 training-serving skew，以及什么才算一个可上线、可审计、不会越权、能持续改进的 LLM 交易质量审计助手”。

交易数据不能直接变成训练数据，必须经过：

```text
Raw Trade Record
  -> Trade Candidate Snapshot
  -> Decision-Time Features
  -> Outcome / Post-Trade Record
  -> Labeling Record
  -> SFT Example / Preference Pair / Eval Case
```

核心定位：

```text
LLM 是交易候选解释器、质量评分器、风险门控辅助器、异常拦截器和审计助手。
LLM 不是最终交易执行者，不能直接下单，不能绕过 deterministic risk engine。
合格 LLM 交易质量审计助手的验收目标不是声称赚钱，而是在确定性风控约束下减少坏交易放行、识别风险、提升解释和复盘质量，并且保持可审计。
```

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-179 | P0 | done | 定义 AI Engineering 交易 gating/scoring 知识树扩展框架 | `codex-expert-kit/rag/knowledge_tree.md`、`docs/research/phase36_ai_engineering_knowledge_framework.md` | CEK-TA-178 |
| CEK-TA-180 | P0 | done | 定义外接 LLM gating/scoring 项目业务流和边界契约 | `docs/contracts/ai_engineering_gating_scoring_contract.md` | CEK-TA-179 |
| CEK-TA-181 | P0 | done | 创建分层知识点采集矩阵和 ResearchIngestionTask 队列，区分 P0-Core、P0-Extended、P1 | `docs/research/phase36_ai_engineering_p0_collection_matrix.md`、`docs/research/phase36_ai_engineering_research_task_queue.md` | CEK-TA-180 |
| CEK-TA-182 | P0 | done | 对齐知识卡 schema、machine_gate、llm_usage_policy 和默认指导门禁 | `codex-expert-kit/rag/knowledge_item_schema.md`、`docs/contracts/ai_engineering_knowledge_item_policy.md` | CEK-TA-181 |
| CEK-TA-183 | P0 | done | 对齐 MCP 主动检索、只读权限和外部 AI 调用模板 | `codex-expert-kit/templates/external_project_active_retrieval_AGENTS.md`、`docs/contracts/external_ai_active_retrieval_protocol.md` | CEK-TA-182 |
| CEK-TA-184 | P1 | done | 对齐 FastAPI/KnowledgeTree/SearchLab 对 AI Engineering 新节点的只读展示与检索契约 | `docs/contracts/knowledge_tree_reading_api_contract.md`、`ui/src/views/KnowledgeTreeView.vue`、`ui/src/views/SearchLab.vue` | CEK-TA-182 |
| CEK-TA-185 | P1 | done | 采集并生成首批 AI Engineering P0 候选知识包 | `codex-expert-kit/rag/candidates/`、`docs/research/`、`docs/reports/phase36_ai_engineering_collection_report.md` | CEK-TA-181 |
| CEK-TA-186 | P1 | done | 运行来源评分、冲突检测、污染门禁和候选审计导出 | `docs/audit/`、`docs/reports/`、验证脚本输出 | CEK-TA-185 |
| CEK-TA-187 | P1 | done | 将通过审计的候选沉淀为 formal reviewed 知识并重建索引 | `codex-expert-kit/rag/knowledge/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts` | CEK-TA-186 |
| CEK-TA-188 | P1 | done | 验证 MCP/SearchLab/KnowledgeTree 能命中、引用、阻断和降级 | `codex-expert-kit/mcp/tests/`、`codex-expert-kit/api/tests/`、`ui/tests/e2e/`、`docs/reports/phase36_ai_engineering_completion_audit_report.md` | CEK-TA-187 |
| CEK-TA-199 | P1 | done | 为第一批审计中 needs_more_evidence 的 2 条能力边界候选创建补证采集任务并联网补来源 | `docs/research/phase36_capability_boundary_supplemental_research.md`、2 条 candidate JSON | CEK-TA-186 |
| CEK-TA-200 | P1 | done | 导出 2 条能力边界候选的补证后二次审计包 | `docs/audit/phase36_capability_boundary_supplemental_audit_package_20260609.json` | CEK-TA-199 |
| CEK-TA-201 | P1 | done | 导入 Phase 36 第二批 AI 审计结果，按补丁点生成 10 条 formal reviewed 知识并保留 2 条 needs_more_evidence | `docs/audit/audit_result_phase36_ai_engineering_batch_02_of_10_20260609_gpt55_pro_strict_sources.json`、`docs/reports/phase36_batch_02_audit_import_report.json`、`codex-expert-kit/rag/knowledge/` | CEK-TA-186 |
| CEK-TA-202 | P1 | done | 重建第二批审计后的 MCP 正式知识索引、Vue3 formal/candidate fixture，并执行质量门禁 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-201 |
| CEK-TA-203 | P1 | done | 为第二批审计中 needs_more_evidence 的 2 条候选创建补证采集任务并联网补直接来源 | `docs/research/phase36_batch02_supplemental_research.md`、2 条 candidate JSON | CEK-TA-201 |
| CEK-TA-204 | P1 | done | 导出第二批 2 条 needs_more_evidence 候选的补证后二次审计包 | `docs/audit/phase36_batch02_supplemental_audit_package_20260609.json` | CEK-TA-203 |
| CEK-TA-205 | P1 | done | 导入第一批能力边界补证二次审计结果，将 2 条 accepted_for_draft 转 formal reviewed 并按审计补丁优化知识内容 | `docs/audit/audit_result_phase36_capability_boundary_supplemental_reaudit_20260609_gpt55_pro.json`、`docs/reports/audit_result_phase36_capability_boundary_supplemental_reaudit_20260609_gpt55_pro_import_report.json`、`codex-expert-kit/rag/knowledge/KB_09_LLM_TRAINING/` | CEK-TA-200 |
| CEK-TA-206 | P1 | done | 重建第一批补证二审后的 MCP 正式知识索引、Vue3 formal/candidate fixture，并执行质量门禁 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-205 |
| CEK-TA-207 | P1 | done | 修复 Vue3 前端运行时挂起体验：避免默认探测被其他服务占用的 8787 端口、补 `/searchlab` 兼容跳转和 FastAPI 本地 CORS | `ui/src/services/knowledgeTreeApi.ts`、`ui/src/router.ts`、`codex-expert-kit/api/codex_expert_kit_api/main.py` | CEK-TA-206 |
| CEK-TA-208 | P1 | done | 导入第二批补证二次审计结果，将 2 条 accepted_for_draft 转 formal reviewed，并按审计补丁优化知识内容、字段契约、来源摘要和边界说明 | `docs/audit/audit_result_phase36_batch02_supplemental_reaudit_20260609_gpt55_pro_strict_sources.json`、`docs/reports/audit_result_phase36_batch02_supplemental_reaudit_20260609_gpt55_pro_strict_sources_import_report.json`、`codex-expert-kit/rag/knowledge/KB_09_LLM_TRAINING/kb_ai_engineering.dataset.deduplication_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_AI_ENGINEERING/kb_ai_engineering.deployment.llm_timeout_or_mcp_failure_fallback_required.v1.json` | CEK-TA-204 |
| CEK-TA-209 | P1 | done | 重建第二批补证二审后的 MCP 正式知识索引、Vue3 formal/candidate fixture，并执行质量门禁 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-208 |
| CEK-TA-210 | P1 | done | 修复 Phase 36 AI Engineering 候选和 reviewed 知识中的 UTF-8 乱码，并新增 no-mojibake 门禁脚本防止前端继续显示问号占位 | `codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/`、`codex-expert-kit/rag/knowledge/KB_09_LLM_TRAINING/`、`codex-expert-kit/rag/knowledge/KB_AI_ENGINEERING/`、`codex-expert-kit/rag/scripts/validate_no_mojibake.py`、`ui/src/data/` | CEK-TA-209 |
| CEK-TA-211 | P1 | done | 导入第三批 AI Engineering 审计结果，将 7 条 accepted_for_draft 转 formal reviewed，保留 5 条 needs_more_evidence，并按审计补丁优化正式知识内容 | `docs/audit/audit_result_phase36_ai_engineering_batch_03_of_10_20260609_gpt55_pro_strict_sources.json`、`docs/reports/phase36_batch_03_audit_import_report.json`、`codex-expert-kit/rag/knowledge/KB_09_LLM_TRAINING/` | CEK-TA-186 |
| CEK-TA-212 | P1 | done | 重建第三批审计后的 MCP 正式知识索引、Vue3 formal/candidate fixture，并执行 schema、污染、状态机和乱码门禁 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-211 |
| CEK-TA-213 | P1 | done | 为第三批审计中 needs_more_evidence 的 5 条候选创建补证采集任务并联网补直接来源 | `docs/research/phase36_batch03_supplemental_research.md`、5 条 candidate JSON | CEK-TA-211 |
| CEK-TA-214 | P1 | done | 导出第三批 5 条 needs_more_evidence 候选的补证后二次审计包 | `docs/audit/phase36_batch03_supplemental_audit_package_20260609.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-213 |
| CEK-TA-215 | P1 | done | 导入第四批 AI Engineering 审计结果，将 10 条 accepted_for_draft 转 formal reviewed，保留 1 条 needs_more_evidence，并按审计补丁优化正式知识内容 | `docs/audit/audit_result_phase36_ai_engineering_batch_04_of_10_20260609_gpt55_pro_strict_sources.json`、`docs/reports/phase36_batch_04_audit_import_report.json`、`codex-expert-kit/rag/knowledge/` | CEK-TA-186 |
| CEK-TA-216 | P1 | done | 重建第四批审计后的 MCP 正式知识索引、Vue3 formal/candidate fixture，并执行 schema、污染、状态机和乱码门禁 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-215 |
| CEK-TA-217 | P1 | done | 为第四批审计中 false allow 成本排序 needs_more_evidence 候选创建补证采集任务并联网补 cost matrix、risk ledger 和 owner 边界来源 | `docs/research/phase36_batch04_false_allow_supplemental_research.md`、1 条 candidate JSON | CEK-TA-215 |
| CEK-TA-218 | P1 | done | 导出第四批 false allow 候选的补证后二次审计包，并重建 Vue3 候选 fixture | `docs/audit/phase36_batch04_false_allow_supplemental_audit_package_20260609.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-217 |
| CEK-TA-219 | P1 | done | 导入第三批 5 条 needs_more_evidence 候选的补证二审结果，将 accepted_for_draft 转 formal reviewed，并保留补丁说明和边界 | `docs/audit/audit_result_phase36_batch03_supplemental_reaudit_20260609_gpt55_pro_strict_sources.json`、`docs/reports/audit_result_phase36_batch03_supplemental_reaudit_20260609_gpt55_pro_strict_sources_import_report.json`、`codex-expert-kit/rag/knowledge/KB_09_LLM_TRAINING/` | CEK-TA-214 |
| CEK-TA-220 | P1 | done | 重建第三批补证二审后的 MCP 正式知识索引、Vue3 formal/candidate fixture，并执行质量门禁 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-219 |
| CEK-TA-221 | P0 | done | 修复 Phase 36 历史审计资产中的问号占位型乱码，并从干净候选源重建受污染的补证审计包 | `docs/audit/phase36_capability_boundary_supplemental_audit_package_20260609.json`、`docs/audit/phase36_batch02_supplemental_audit_package_20260609.json`、`docs/audit/audit_result_phase36_capability_boundary_supplemental_reaudit_20260609_gpt55_pro.json` | CEK-TA-220 |
| CEK-TA-222 | P0 | done | 升级 no-mojibake 门禁，覆盖候选、正式知识、索引、docs/audit、docs/reports、docs/research 和 Vue3 fixture，并使用 codepoint 检测防止误报 URL 问号 | `codex-expert-kit/rag/scripts/validate_no_mojibake.py` | CEK-TA-221 |
| CEK-TA-223 | P1 | done | 导入第四批 false allow 补证二审结果，将 1 条 accepted_for_draft 转 formal reviewed，并保留 cost matrix、risk ledger、owner override 边界 | `docs/audit/audit_result_phase36_batch04_false_allow_supplemental_reaudit_20260609_gpt55_pro_strict_sources.json`、`docs/reports/audit_result_phase36_batch04_false_allow_supplemental_reaudit_20260609_gpt55_pro_strict_sources_import_report.json`、`codex-expert-kit/rag/knowledge/KB_09_LLM_TRAINING/kb_ai_engineering.gating.false_allow_more_dangerous_than_false_block.v1.json` | CEK-TA-218 |
| CEK-TA-224 | P1 | done | 重建第四批 false allow 二审后的 MCP 正式知识索引、Vue3 formal/candidate fixture，并执行质量门禁 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-223 |
| CEK-TA-225 | P1 | done | 导入第五批 AI Engineering 审计结果，将 9 条 accepted_for_draft 转 formal reviewed，保留 2 条 good_loss/bad_win needs_more_evidence | `docs/audit/audit_result_phase36_ai_engineering_batch_05_of_10_20260609_gpt55_pro_strict_sources.json`、`docs/reports/phase36_batch_05_audit_import_report.json`、`codex-expert-kit/rag/knowledge/` | CEK-TA-186 |
| CEK-TA-226 | P1 | done | 重建第五批审计后的 MCP 正式知识索引、Vue3 formal/candidate fixture，并执行 schema、污染、状态机和乱码门禁 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-225 |
| CEK-TA-227 | P1 | done | 为第五批审计中 2 条 good_loss/bad_win needs_more_evidence 候选创建补证采集任务并联网补 outcome bias、FINRA、human consensus 和 schema validation 来源 | `docs/research/phase36_batch05_good_loss_bad_win_supplemental_research.md`、2 条 candidate JSON | CEK-TA-225 |
| CEK-TA-228 | P1 | done | 导出第五批 2 条 good_loss/bad_win 候选的补证后二次审计包，并重建 Vue3 候选 fixture | `docs/audit/phase36_batch05_good_loss_bad_win_supplemental_audit_package_20260609.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-227 |
| CEK-TA-229 | P1 | done | 导入第五批 good_loss/bad_win 补证二审结果，将 2 条 accepted_for_draft 转 formal reviewed，并保留 reason-code/review_category 与 Trading Engineering owner 边界 | `docs/audit/audit_result_phase36_batch05_good_loss_bad_win_supplemental_reaudit_20260609_gpt55_pro_strict_sources.json`、`docs/reports/audit_result_phase36_batch05_good_loss_bad_win_supplemental_reaudit_20260609_gpt55_pro_strict_sources_import_report.json`、`codex-expert-kit/rag/knowledge/KB_09_LLM_TRAINING/` | CEK-TA-228 |
| CEK-TA-230 | P1 | done | 重建第五批 good_loss/bad_win 二审后的 MCP 正式知识索引、Vue3 formal/candidate fixture，并执行质量门禁 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-229 |
| CEK-TA-231 | P1 | done | 导入第六批 AI Engineering 审计结果，将 9 条 accepted_for_draft 转 formal reviewed，保留 2 条 llm_judge/preference_pair needs_more_evidence | `docs/audit/audit_result_phase36_ai_engineering_batch_06_of_10_20260609_gpt55_pro_strict_sources.json`、`docs/reports/phase36_batch_06_audit_import_report.json`、`codex-expert-kit/rag/knowledge/` | CEK-TA-186 |
| CEK-TA-232 | P1 | done | 重建第六批审计后的 MCP 正式知识索引、Vue3 formal/candidate fixture，并执行 schema、污染、状态机和乱码门禁 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-231 |
| CEK-TA-233 | P1 | done | 为第六批审计中 2 条 llm_judge/preference_pair needs_more_evidence 候选创建补证采集任务并联网补 LLM judge bias、DPO/TRL pair schema 和数据集治理来源 | `docs/research/phase36_batch06_llm_judge_preference_pair_supplemental_research.md`、2 条 candidate JSON | CEK-TA-231 |
| CEK-TA-234 | P1 | done | 导出第六批 2 条 llm_judge/preference_pair 候选的补证后二次审计包，并重建 Vue3 候选 fixture | `docs/audit/phase36_batch06_llm_judge_preference_pair_supplemental_audit_package_20260609.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-233 |
| CEK-TA-235 | P1 | done | 导入第六批 llm_judge/preference_pair 补证二审结果，将 2 条 accepted_for_draft 转 formal reviewed，并保留 judge bias、vendor-neutral preference schema 和 Trading Engineering 边界 | `docs/audit/audit_result_phase36_batch06_llm_judge_preference_pair_supplemental_reaudit_20260609_gpt55_pro_strict_sources.json`、`docs/reports/audit_result_phase36_batch06_llm_judge_preference_pair_supplemental_reaudit_20260609_gpt55_pro_strict_sources_import_report.json`、`codex-expert-kit/rag/knowledge/KB_09_LLM_TRAINING/` | CEK-TA-234 |
| CEK-TA-236 | P1 | done | 重建第六批 llm_judge/preference_pair 二审后的 MCP 正式知识索引、Vue3 formal/candidate fixture，并执行质量门禁 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-235 |
| CEK-TA-237 | P1 | done | 导入第七批 AI Engineering 审计结果，将 8 条 accepted_for_draft 转 formal reviewed，保留 3 条 rag_no_hit/research_feedback/risk_ledger needs_more_evidence | `docs/audit/audit_result_phase36_ai_engineering_batch_07_of_10_20260609_gpt55_pro_strict_sources.json`、`docs/reports/phase36_batch_07_audit_import_report.json`、`codex-expert-kit/rag/knowledge/` | CEK-TA-186 |
| CEK-TA-238 | P1 | done | 重建第七批审计后的 MCP 正式知识索引、Vue3 formal/candidate fixture，并执行 schema、污染、状态机和乱码门禁 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-237 |
| CEK-TA-239 | P1 | done | 为第七批审计中 3 条 rag_no_hit/research_feedback/risk_ledger needs_more_evidence 候选创建补证采集任务并联网补 RAG no-hit fallback、MCP/OWASP tool permission、cost-sensitive cost matrix 和 risk manage 来源 | `docs/research/phase36_batch07_rag_parameter_risk_ledger_supplemental_research.md`、3 条 candidate JSON | CEK-TA-237 |
| CEK-TA-240 | P1 | done | 导出第七批 3 条 rag_no_hit/research_feedback/risk_ledger 候选的补证后二次审计包，并重建 Vue3 候选 fixture | `docs/audit/phase36_batch07_rag_parameter_risk_ledger_supplemental_audit_package_20260609.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-239 |
| CEK-TA-241 | P1 | done | 导入第七批 rag_no_hit/research_feedback/risk_ledger 补证二审结果，将 3 条 accepted_for_draft 转 formal reviewed，并保留 RAG fallback、tool permission、risk ledger 边界 | `docs/audit/audit_result_phase36_batch07_rag_parameter_risk_ledger_supplemental_reaudit_20260609_gpt55_pro_strict_sources.json`、`docs/reports/audit_result_phase36_batch07_rag_parameter_risk_ledger_supplemental_reaudit_20260609_gpt55_pro_strict_sources_import_report.json`、`codex-expert-kit/rag/knowledge/KB_AI_ENGINEERING/` | CEK-TA-240 |
| CEK-TA-242 | P1 | done | 重建第七批 rag_no_hit/research_feedback/risk_ledger 二审后的 MCP 正式知识索引、Vue3 formal/candidate fixture，并执行质量门禁 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-241 |
| CEK-TA-243 | P1 | done | 导入第八批 AI Engineering 审计结果，将 6 条 accepted_for_draft 转 formal reviewed，保留 5 条 scoring_rubric needs_more_evidence | `docs/audit/audit_result_phase36_ai_engineering_batch_08_of_10_20260609_gpt55_pro_strict_sources.json`、`docs/reports/phase36_batch_08_audit_import_report.json`、`codex-expert-kit/rag/knowledge/` | CEK-TA-186 |
| CEK-TA-244 | P1 | done | 重建第八批审计后的 MCP 正式知识索引、Vue3 formal/candidate fixture，并执行 schema、污染、状态机和乱码门禁 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-243 |
| CEK-TA-245 | P1 | done | 为第八批审计中 5 条 scoring_rubric needs_more_evidence 候选创建补证采集任务，重写维度 statement，并补 TimeSeriesSplit、GroupKFold、threshold/cost-sensitive、FINRA、NIST、calibration 和内部 rubric 维度契约来源 | `docs/contracts/ai_engineering_scoring_rubric_dimension_contract.md`、`docs/research/phase36_batch08_scoring_rubric_supplemental_research.md`、5 条 candidate JSON | CEK-TA-243 |
| CEK-TA-246 | P1 | done | 导出第八批 5 条 scoring_rubric 候选的补证后二次审计包，并重建 Vue3 候选 fixture | `docs/audit/phase36_batch08_scoring_rubric_supplemental_audit_package_20260609.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-245 |
| CEK-TA-247 | P1 | done | 导入第八批 scoring_rubric 补证二审结果，将 5 条 accepted_for_draft 转 formal reviewed，并补齐 uncertainty_penalty 的 NAACL 2024 LLM confidence calibration survey 来源 | `docs/audit/audit_result_phase36_batch08_scoring_rubric_supplemental_reaudit_20260609_gpt55_pro_strict_sources.json`、`docs/reports/audit_result_phase36_batch08_scoring_rubric_supplemental_reaudit_20260609_gpt55_pro_strict_sources_import_report.json`、`codex-expert-kit/rag/knowledge/KB_09_LLM_TRAINING/` | CEK-TA-246 |
| CEK-TA-248 | P1 | done | 重建第八批 scoring_rubric 二审后的 MCP 正式知识索引、Vue3 formal/candidate fixture，并执行质量门禁 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-247 |
| CEK-TA-249 | P1 | done | 导入第九批 AI Engineering 审计结果，将 6 条 accepted_for_draft 转 formal reviewed，保留 5 条 SFT/trade_data needs_more_evidence | `docs/audit/audit_result_phase36_ai_engineering_batch_09_of_10_20260609_gpt55_pro_strict_sources.json`、`docs/reports/phase36_batch_09_audit_import_report.json`、`codex-expert-kit/rag/knowledge/` | CEK-TA-186 |
| CEK-TA-250 | P1 | done | 重建第九批审计后的 MCP 正式知识索引、Vue3 formal/candidate fixture，并执行 schema、污染、状态机和乱码门禁 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-249 |
| CEK-TA-251 | P1 | done | 为第九批审计中 5 条 SFT/trade_candidate/trade_data needs_more_evidence 候选创建补证采集任务，重写 statement，并补 Structured Outputs、JSON Schema、TRL、TFDV、FINRA、QuantConnect、Feast 和 Datasheets 来源 | `docs/research/phase36_batch09_sft_trade_data_supplemental_research.md`、5 条 candidate JSON | CEK-TA-249 |
| CEK-TA-252 | P1 | done | 导出第九批 5 条 SFT/trade_candidate/trade_data 候选的补证后二次审计包，并重建 Vue3 候选 fixture | `docs/audit/phase36_batch09_sft_trade_data_supplemental_audit_package_20260609.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-251 |
| CEK-TA-253 | P1 | done | 导入第十批 AI Engineering 审计结果，将 7 条 accepted_for_draft 转 formal reviewed，保留 4 条 strategy_version/training_example needs_more_evidence | `docs/audit/audit_result_phase36_ai_engineering_batch_10_of_10_20260609_gpt55_pro_strict_sources.json`、`docs/reports/phase36_batch_10_audit_import_report.json`、`codex-expert-kit/rag/knowledge/` | CEK-TA-186 |
| CEK-TA-254 | P1 | done | 重建第十批审计后的 MCP 正式知识索引、Vue3 formal/candidate fixture，并执行 schema、污染、状态机和乱码门禁；修正污染门禁对专业 `training sample` 术语的误报 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts`、`codex-expert-kit/rag/scripts/validate_knowledge_pollution.py` | CEK-TA-253 |
| CEK-TA-255 | P1 | done | 为第十批审计中 4 条 strategy_version/training_example needs_more_evidence 候选创建补证采集任务，重写 statement，并补 MLflow、DVC、Datasheets、scikit-learn、TRL、Structured Outputs、JSON Schema 和 TFDV 来源 | `docs/research/phase36_batch10_strategy_training_example_supplemental_research.md`、4 条 candidate JSON、`codex-expert-kit/rag/scripts/phase36_batch10_supplement.py` | CEK-TA-253 |
| CEK-TA-256 | P1 | done | 导出第十批 4 条 strategy_version/training_example 候选的补证后二次审计包，并重建 Vue3 候选 fixture | `docs/audit/phase36_batch10_strategy_training_example_supplemental_audit_package_20260609.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-255 |
| CEK-TA-257 | P1 | done | 导入第九批 5 条 SFT/trade_candidate/trade_data 补证二审结果，将 accepted_for_draft 转 formal reviewed，并保留 output schema、context refs、execution cost、raw trade record 和 source_mode 边界 | `docs/audit/audit_result_phase36_batch09_sft_trade_data_supplemental_reaudit_20260609_gpt55_pro_strict_sources.json`、`docs/reports/audit_result_phase36_batch09_sft_trade_data_supplemental_reaudit_20260609_gpt55_pro_strict_sources_import_report.json`、`codex-expert-kit/rag/knowledge/KB_09_LLM_TRAINING/` | CEK-TA-252 |
| CEK-TA-258 | P1 | done | 重建第九批 SFT/trade_data 二审后的 MCP 正式知识索引、Vue3 formal/candidate fixture，并执行 schema、污染、状态机、乱码和前端构建门禁 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts`、`codex-expert-kit/rag/scripts/validate_knowledge_pollution.py` | CEK-TA-257 |
| CEK-TA-259 | P1 | done | 导入第十批 4 条 strategy_version/training_example 补证二审结果，将 accepted_for_draft 转 formal reviewed，并保留 strategy refs、lineage、input-target separation 和 SFT schema 边界 | `docs/audit/audit_result_phase36_batch10_strategy_training_example_supplemental_reaudit_20260609_gpt55_pro_strict_sources.json`、`docs/reports/audit_result_phase36_batch10_strategy_training_example_supplemental_reaudit_20260609_gpt55_pro_strict_sources_import_report.json`、`codex-expert-kit/rag/knowledge/KB_09_LLM_TRAINING/` | CEK-TA-256 |
| CEK-TA-260 | P1 | done | 重建第十批 strategy/training_example 二审后的 MCP 正式知识索引、Vue3 formal/candidate fixture，并执行 schema、污染、状态机、乱码和前端构建门禁 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-259 |
| CEK-TA-261 | P1 | done | 完成 Phase 36 AI Engineering 113 条知识点完整性复审，确认候选、正式知识、MCP/SearchLab、Vue3 fixture、schema、污染和乱码门禁均符合预期 | `docs/reports/phase36_ai_engineering_completion_audit_report.md` | CEK-TA-260 |
| CEK-TA-263 | P1 | done | 修复知识树页面中 formal knowledge、formalized candidate 和 open gap 的状态混排，清理已二审知识遗留 needs_more_evidence 文案 | `ui/src/views/KnowledgeTreeView.vue`、`codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py`、`codex-expert-kit/rag/knowledge/KB_09_LLM_TRAINING/`、`ui/src/data/` | CEK-TA-261 |
| CEK-TA-264 | P1 | done | 输出 AI Engineering 交易 gating/scoring 模型与训练平台选型审计方案，明确数值模型、LLM 和确定性风控的职责边界 | `docs/research/phase36_ai_engineering_model_platform_selection_proposal.md` | CEK-TA-261 |
| CEK-TA-265 | P1 | done | 融合外部审计意见优化模型与训练平台选型方案，补齐 Conditional Go、校准、反事实评估、LLM 严格输出和 Phase 38 拆分 | `docs/research/phase36_ai_engineering_model_platform_selection_proposal.md` | CEK-TA-264 |

## 上游输入

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase35_external_ai_active_retrieval_protocol.md
docs/contracts/external_ai_active_retrieval_protocol.md
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/metadata_schema.md
codex-expert-kit/rag/knowledge_tree.md
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/templates/external_project_active_retrieval_AGENTS.md
```

业务输入：

```text
第一个外接项目：训练 LLM 做交易 gating/scoring。
目标：提高交易质量，包括 R/R、胜率、PnL、风险拦截质量、坏交易过滤质量、复盘和回灌效率。
边界：外接项目提供项目事实和交易数据；CEK-TA 提供可复用专业知识、审计规则、RAG/MCP 调用契约和治理流程。
```

## 下游输出

```text
1. AI Engineering 新知识树框架。
2. 外接 LLM gating/scoring 项目业务流和接口契约。
3. 分层专业知识采集队列：保留原 101 条作为采集池，新增反事实评估、安全隐私、baseline、标注一致性和训练服务一致性等关键硬门，并拆成 P0-Core、P0-Extended、P1。
4. 可进入 Phase 23/32 工作流的候选知识包。
5. formal reviewed 知识沉淀路径。
6. MCP/SearchLab/KnowledgeTree 可检索、可引用、可阻断的运行时验证。
7. 外接项目 AGENTS 模板可直接指导开发 AI 主动检索 CEK-TA。
```

## AI Engineering 知识树框架

```text
AI Engineering

KB_09 LLM Training
  KB_09A Model Training Engineering
    1. Training Objective
    2. Dataset Construction
    3. Data Leakage / Contamination
    4. Supervised Fine-Tuning
    5. Preference Training / DPO / RLHF
    6. PEFT / LoRA / QLoRA
    7. Evaluation / Evals
    8. Training Run Management
    9. Safety / Alignment Boundary
    10. Training-Serving Consistency

  KB_09C Training Dataset Schema Engineering
    1. Raw Trade Data Normalization
    2. Trade Candidate Snapshot Schema
    3. Decision-Time Feature Schema
    4. Outcome / Post-Trade Schema
    5. Labeling Schema
    6. Training Example Schema
    7. Preference Pair Schema
    8. Eval Case Schema

  KB_09D Trading LLM Task Taxonomy
    1. Trade Candidate Scoring
    2. Trade Gate Decision
    3. Risk Violation Detection
    4. Data Quality Audit
    5. Strategy Rule Compliance Audit
    6. Post-Trade Review
    7. Incident Explanation
    8. Parameter / Rule Improvement Suggestion

  KB_09E Training Method Selection
    1. RAG First Baseline
    2. SFT Boundary
    3. Preference / DPO Boundary
    4. Eval Baseline Before Fine-Tune
    5. Do Not Train Around Data Problems

  KB_09B Trading Scoring / Gating Training
    1. Trading Role Boundary
    2. Trade Sample Schema
    3. Trading Labeling & Leakage
    4. Scoring / Gating Rubric
    5. Trading Eval & Calibration
    6. Trading Safety Gate

KB_10 RAG Engineering
  1. Retrieval Decision Policy
  2. Metadata / Machine Gate Filtering
  3. Token & Context Budget
  4. Trading Scoring RAG Pack
  5. Citation / Evidence Contract
  6. Retrieval Quality Evaluation

KB_11 MCP / Agent Engineering
  1. MCP Tool Contract
  2. Tool Permission Enforcement
  3. External AI Calling Protocol
  4. Gating / Scoring Agent Flow
  5. Error / No-hit / Conflict Degradation
  6. Agent Non-Delegation Boundary

KB_AI_12 LLMOps / Deployment
  1. Offline Evaluation
  2. Shadow / Paper / Live Rollout
  3. Artifact Lineage
  4. Release Control
  5. Monitoring & Drift
  6. Rollback & Incident Response
  7. Deployment Readiness Gate

KB_AI_13 AI Governance / Audit
  1. Training Data Governance
  2. Knowledge Usage Permission
  3. Human Review Workflow
  4. External Contribution Backflow
  5. Model Output Audit
  6. Dataset Card / Model Card
  7. Incident Governance
  8. Approval / Ownership Workflow

KB_AI_14 Trading AI Safety / Risk Control
  1. Deterministic Risk Gate Precedence
  2. False Allow / False Block Cost Policy
  3. Kill Switch / Emergency Disable
  4. Human Escalation Boundary
  5. Live Trading Permission Boundary
  6. Trading LLM Red Team

KB_AI_15 Business Objective / Acceptance Criteria
  1. LLM Trader Role Definition
  2. Quality Improvement Metrics
  3. Business Cost Metrics
  4. Live Readiness Criteria

KB_AI_16 Label Factory / Annotation Workflow
  1. Auto Label
  2. Human Label
  3. Label Conflict Resolution
  4. Gold Set
  5. Label Quality Score

KB_AI_17 Data Asset Management
  1. Research Pool
  2. Training Pool
  3. Eval Pool
  4. Gold Pool
  5. Shadow Pool
  6. Incident Pool

KB_AI_18 Continuous Learning / Feedback Governance
  1. Live Feedback Boundary
  2. Retraining Dataset Release
  3. Knowledge Backfill
  4. Feedback Loop Risk

KB_AI_19 AI Security / Privacy / Compliance
  1. Prompt Injection / RAG Security
  2. Tool Output Untrusted Boundary
  3. Secret / Account Identifier Redaction
  4. Trade Data Sanitization
  5. Market Data License / Permission
  6. Training Export Approval
```

## 知识点采集范围

审计融合后，原 101 条不再全部视为同等 P0。它们保留为第一批采集池，并按下列规则重新分层：

```text
P0-Core：安全启动硬门；缺失或违反时，训练、评估、上线或默认指导必须阻断。
P0-Extended：第一轮工程建设必需；用于补齐上线前的评估、治理、追踪和审计能力。
P1：优化增强项；包括更细的 scoring rubric 维度、更多 drift 指标、更多 risk ledger 细项和方法深挖。
```

原始采集池仍分为四组：

```text
A. 通用模型训练工程：20 条
B. 训练专属 schema 工程：20 条
C. 交易 gating/scoring：36 条
D. 业务闭环治理：25 条
```

新增关键硬门 12 条：

```text
N01. eval.counterfactual_outcome_missing_for_blocked_trades.v1
N02. eval.off_policy_evaluation_required_for_gate_policy.v1
N03. eval.blocked_trade_cannot_be_labeled_as_loss.v1
N04. security.rag_context_is_untrusted_input.v1
N05. security.prompt_injection_test_required_for_trade_context.v1
N06. data_privacy.no_secret_or_account_identifier_in_training.v1
N07. data_license.market_data_license_check_required.v1
N08. eval.deterministic_baseline_required_before_llm_gate.v1
N09. eval.ablation_required_for_rag_prompt_model_components.v1
N10. label_factory.inter_annotator_agreement_required.v1
N11. feature_store.feature_schema_registry_required.v1
N12. serving_consistency.training_serving_parity_test_required.v1
```

降级为 P1 的典型条目：

```text
scoring_rubric.setup_quality.v1
scoring_rubric.risk_reward_quality.v1
scoring_rubric.market_regime_fit.v1
scoring_rubric.rule_compliance.v1
scoring_rubric.uncertainty_penalty.v1
部分 risk_ledger、monitoring drift、research_feedback 细项
```

重复项处理规则：

```text
schema 组负责字段定义，例如 trade_candidate.decision_timestamp_required.v1。
gating 组负责缺字段时的阻断或降级，例如 training_gate.block_if_missing_decision_timestamp.v1。
dataset / eval / eval_case / time_split 可以共存，但必须建立 depends_on，不得重复表达同一规则。
```

### A. 通用模型训练工程采集池

这些知识点用于建立训练系统地基，不绑定某个交易策略或外接项目事实：

```text
T01. training_objective.task_definition_required.v1
T02. training_objective.rag_vs_finetune_boundary_required.v1
T03. dataset.schema_required.v1
T04. dataset.source_lineage_required.v1
T05. dataset.version_and_hash_required.v1
T06. dataset.train_validation_test_split_required.v1
T07. dataset.deduplication_required.v1
T08. dataset.dataset_card_required.v1
T09. leakage.train_test_contamination_block.v1
T10. leakage.label_in_input_forbidden.v1
T11. sft.when_to_use_and_not_use.v1
T12. sft.output_schema_consistency_required.v1
T13. preference_training.preference_pair_schema_required.v1
T14. preference_training.chosen_rejected_reason_required.v1
T15. dpo.preference_data_quality_required.v1
T16. eval.holdout_test_set_required.v1
T17. eval.production_like_eval_required.v1
T18. training_run.config_and_hyperparameter_snapshot_required.v1
T19. serving_consistency.train_like_serve_required.v1
T20. safety.no_tool_permission_escalation.v1
```

### B. 训练专属 schema 工程采集池

这些知识点用于把交易记录转换为 LLM 训练、偏好训练和评估可用的结构化样本：

```text
S01. trade_data.raw_trade_record_required_fields.v1
S02. trade_data.strategy_id_and_version_required.v1
S03. trade_data.source_mode_required.v1
S04. trade_data.fee_slippage_execution_cost_required.v1
S05. trade_candidate.snapshot_required_before_scoring.v1
S06. trade_candidate.decision_timestamp_required.v1
S07. trade_candidate.market_risk_execution_context_required.v1
S08. feature_schema.decision_time_only.v1
S09. feature_schema.feature_timestamp_cutoff_required.v1
S10. feature_schema.post_trade_fields_forbidden_in_input.v1
S11. outcome_schema.post_trade_fields_separated.v1
S12. label_schema.no_pnl_only_label.v1
S13. label_schema.good_loss_bad_win_required.v1
S14. label_schema.multi_dimensional_trade_quality.v1
S15. label_schema.label_reason_codes_required.v1
S16. training_example.sft_schema_required.v1
S17. training_example.input_target_separation.v1
S18. preference_pair.not_based_on_pnl_only.v1
S19. eval_case.time_strategy_regime_split_required.v1
S20. eval_case.no_training_overlap_required.v1
```

### C. 交易 gating/scoring 采集池

这些知识点用于外接交易 LLM scoring/gating 项目，必须继承 A 组训练工程地基和 B 组训练数据 schema 转换链路：

```text
01. llm_role_boundary.scorer_not_executor.v1
02. llm_role_boundary.no_direct_order_execution.v1
03. llm_role_boundary.cannot_override_hard_risk_gate.v1
04. training_data.trade_sample_schema_required.v1
05. training_data.strategy_version_required.v1
06. training_data.decision_timestamp_required.v1
07. training_data.feature_timestamp_cutoff_required.v1
08. labeling.no_future_information.v1
09. labeling.no_pnl_only_labeling.v1
10. labeling.good_loss_bad_win_distinction.v1
11. labeling.ambiguous_trade_needs_human_review.v1
12. data_quality.backtest_paper_live_separation.v1
13. data_quality.execution_cost_required.v1
14. data_quality.missing_core_fields_block_training.v1
15. scoring_rubric.setup_quality.v1
16. scoring_rubric.risk_reward_quality.v1
17. scoring_rubric.market_regime_fit.v1
18. scoring_rubric.rule_compliance.v1
19. scoring_rubric.uncertainty_penalty.v1
20. scoring_rubric.reason_code_required.v1
21. gating.low_confidence_cannot_allow.v1
22. gating.false_allow_more_dangerous_than_false_block.v1
23. rag.retrieval_required_before_trade_scoring.v1
24. rag.approved_machine_gate_allow_only_default_guidance.v1
25. rag.no_source_or_conflict_blocks_default_guidance.v1
26. rag.no_hit_requires_neutral_or_review.v1
27. mcp.read_only_knowledge_access.v1
28. mcp.server_side_permission_enforcement_required.v1
29. deployment.shadow_mode_before_live.v1
30. deployment.llm_timeout_or_mcp_failure_fallback_required.v1
31. versioning.model_prompt_rag_strategy_snapshot_required.v1
32. audit.every_gate_decision_requires_trace.v1
33. eval.time_split_walk_forward_required.v1
34. eval.score_calibration_required_before_gating.v1
35. llm_judge.position_and_format_bias_check_required.v1
36. governance.dataset_card_and_model_card_required.v1
```

### D. 业务闭环治理采集池

这些知识点用于补齐“合格 LLM 交易质量审计助手”的业务验收、任务边界、标签工厂、数据资产、上线决策、风险账本和反馈治理：

```text
B01. business_objective.llm_trader_acceptance_criteria_required.v1
B02. business_objective.success_metric_not_only_pnl.v1
B03. task_taxonomy.pre_trade_post_trade_task_separation.v1
B04. task_taxonomy.each_task_requires_schema_and_eval.v1
B05. label_factory.label_guideline_required.v1
B06. label_factory.gold_set_required.v1
B07. label_factory.label_conflict_resolution_required.v1
B08. data_asset.eval_pool_must_not_train.v1
B09. data_asset.gold_set_immutable_required.v1
B10. method_selection.rag_first_baseline_required.v1
B11. method_selection.no_finetune_before_eval_baseline.v1
B12. capability_boundary.llm_not_primary_price_predictor.v1
B13. capability_boundary.numeric_model_vs_llm_role_split.v1
B14. research_feedback.llm_suggestion_is_hypothesis_only.v1
B15. research_feedback.no_auto_strategy_parameter_update.v1
B16. runtime.llm_gate_is_suggestion_not_final_authority.v1
B17. runtime.final_gate_deterministic_engine_required.v1
B18. calibration.llm_score_not_probability.v1
B19. calibration.threshold_requires_shadow_data.v1
B20. risk_ledger.false_allow_cost_record_required.v1
B21. lineage.model_prompt_rag_data_strategy_bound_together.v1
B22. redteam.hard_gate_override_attempt_test.v1
B23. approval.hard_gate_enable_requires_approval.v1
B24. readiness.offline_eval_pass_not_equal_live_ready.v1
B25. feedback.model_output_cannot_label_itself.v1
```

## 契约

### 外接项目输入契约

外接项目调用 AI Engineering 知识时，应至少提供：

```text
project_adapter_id
task_type
strategy_id
strategy_version
raw_trade_record
trade_candidate
decision_timestamp
feature_timestamp_cutoff
market_context
risk_context
execution_context
outcome_record
labeling_record
training_example_type: sft | preference_pair | eval_case | scoring_runtime
mode: backtest | replay | paper | live
requested_decision: score | gate | audit | dataset_review | incident_review
task_taxonomy: pre_trade_scoring | pre_trade_gating | risk_violation_detection | data_quality_audit | strategy_rule_audit | post_trade_review | incident_explanation | research_suggestion
business_acceptance_target
```

### RAG/MCP 输出契约

CEK-TA 返回给外接项目的知识必须带：

```text
knowledge_id
canonical_node_id
review_status
machine_gate.default_guidance
llm_usage_policy
source_evidence
conflict_status
freshness
applicability
not_applicable_when
reason_codes
recommended_next_action
```

### Gating/Scoring 输出契约

外接项目 AI 不应输出模糊结论，必须结构化：

```text
score
gate_suggestion: allow_recommendation | soft_block_recommendation | hard_block_recommendation | needs_human_review | neutral
confidence
reason_codes
knowledge_refs
source_refs
assumptions
missing_fields
fallback_action
audit_trace_id
```

### 交易数据到训练数据转换契约

训练数据生成链路必须显式区分：

```text
raw_trade_record: 原始交易记录，可包含完整事后结果。
trade_candidate_snapshot: 决策时快照，只能包含 decision_timestamp 当时可见的信息。
decision_time_features: 每个特征必须有 feature_timestamp 和 available_at_decision。
outcome_record: 事后结果，只能进入 label、eval、复盘，不得进入模型输入。
labeling_record: 过程质量、结果质量、人工/规则来源和 reason_codes。
sft_example: input 和 target_output 必须分离。
preference_pair: chosen/rejected 必须基于同一 prompt，不能只按 PnL 选择。
eval_case: 必须和训练集隔离，声明 time/strategy/regime split。
```

阻断规则：

```text
feature_timestamp > decision_timestamp -> block sample
input contains pnl / exit_price / MFE / MAE / final outcome -> block sample
missing strategy_version -> block sample
missing source_mode -> block sample
missing label_reason_codes for supervised labels -> needs_review
preference pair based only on PnL -> block sample
eval case overlaps training example -> block eval
missing task_taxonomy or output_schema -> block training task
offline eval passed but no shadow report -> block live/paper hard gate promotion
LLM suggestion attempts direct strategy parameter update -> block and route to research hypothesis
model output used as its own label -> block feedback sample
```

### 业务闭环契约

合格 LLM 交易质量审计助手必须显式定义：

```text
business_objective: 该模型服务的交易质量目标。
task_taxonomy: 当前样本或调用属于哪类任务。
acceptance_criteria: 上线前必须满足的业务指标和安全指标。
data_asset_pool: research_pool | training_pool | eval_pool | gold_pool | shadow_pool | incident_pool。
label_factory_stage: auto_label | rule_label | human_review | conflict_resolution | gold_set_release。
runtime_position: deterministic_pre_risk_gate 之后、deterministic_final_gate 之前。
calibration_policy: 分数阈值来源、shadow 数据要求、按策略/市场状态校准要求。
risk_ledger: false_allow、false_block、hard_block_recommendation、opportunity_cost 和事后结果关联记录。
approval_owner: 模型上线、阈值调整、hard gating 开启和事故处理责任人。
feedback_boundary: live result 不能自动成为训练标签；模型输出不能给自己贴标签。
```

### 状态契约

```text
candidate: 候选知识，不能作为默认指导。
reviewed: 可用于审计/检索，但不能自动作为 approved 默认指导。
approved: 经过后续人工治理任务确认后，才能成为默认指导。
machine_gate.allow: MCP/SearchLab 默认指导可使用。
machine_gate.caveat_only: 只能带警告引用。
machine_gate.deny: 阻断默认使用。
```

## 边界

本 Phase 包含：

```text
AI Engineering 知识树扩展框架。
分层知识点采集矩阵，包括通用模型训练工程、交易数据到训练数据 schema 工程、交易 gating/scoring 专用训练约束、业务闭环治理，以及反事实评估、安全隐私、baseline、标注一致性和训练服务一致性硬门。
外接项目 gating/scoring 业务流契约。
RAG/MCP/FastAPI/Vue3 对齐任务。
候选知识采集、审计、沉淀路径。
运行时验证任务。
```

跨分支边界：

```text
AI Engineering 只沉淀 AI/LLM/RAG/MCP/训练数据 schema/评估/部署/治理知识。
K 线、策略、回测、回放、模拟盘、实盘执行、交易风控、交易复盘等交易专业规则本体必须进入 Trading Engineering 对应分支。
AI Engineering 可以引用 Trading Engineering 知识，但不能重写交易规则本体。
```

分支路由：

```text
K 线结构、指标、入场、止损、止盈 -> KB_02_KLINE_STRATEGY
市场微观结构、盘口、流动性、订单流 -> KB_03_MARKET_MICROSTRUCTURE
回测偏差、过拟合、成本模型、指标解释 -> KB_04_BACKTEST
回放、模拟盘、fill model、滑点延迟 -> KB_05_REPLAY_SIMULATION
实盘订单、执行适配器、仓位同步、kill switch -> KB_06_LIVE_EXECUTION
交易复盘、坏例 taxonomy、R/R 分解 -> KB_07_TRADE_ANALYSIS
LLM 训练、RAG、MCP、训练数据 schema、eval、部署、治理 -> AI Engineering
```

本 Phase 不包含：

```text
不训练实际 LLM。
不接入真实交易账户。
不生成买卖建议。
不采集 K 线、交易策略、回测、实盘执行、风控规则本体。
不允许 LLM 直接下单。
不把外接项目私有交易数据写入 CEK-TA 通用知识。
不把 candidate/reviewed 直接升级为 approved。
不引入新数据库，除非开发者明确确认。
```

## 实施步骤

```text
1. 更新 AI Engineering 知识树和分区说明。
2. 写出 gating/scoring 外接业务流契约。
3. 建立分层知识点采集矩阵，覆盖原 101 条采集池和新增 12 条关键硬门。
4. 为每条知识点创建 ResearchIngestionTask。
5. 联网采集权威来源，至少覆盖官方文档、研究论文、主流工程文档和安全治理资料。
6. 对来源做评分、去重和冲突检查。
7. 生成候选知识包，不直接进入正式知识。
8. 通过候选审核页/AI 审计包完成人工或 AI 辅助审计。
9. 将通过审计的候选转成 formal reviewed 知识。
10. 重建 knowledge_items.json 和 Vue3 fixture。
11. 验证 MCP/SearchLab/KnowledgeTree 能检索、引用、阻断和降级。
12. 生成 Phase 36 验收报告。
```

## Definition of Done

```text
1. Phase 36 任务卡存在并被 docs/index_tasks.md、docs/tasks/README.md 索引。
2. AI Engineering L2 分区、KB_09A/KB_09C/KB_09D/KB_09E/KB_09B 子层和业务闭环专题被写入知识树规划文档。
3. 分层知识点都有采集任务、来源要求、优先级、验收门槛和降级规则。
4. 外接 LLM gating/scoring 业务流契约、交易数据到训练数据转换契约和业务闭环契约存在。
5. RAG/MCP/FastAPI/Vue3 的读取和展示边界明确。
6. AI Engineering 和 Trading Engineering 的知识边界明确，交易规则本体不会被误收进 AI Engineering。
7. 所有候选知识均保留来源、适用边界、冲突状态、review_status、machine_gate。
8. 没有无来源、冲突未消解、过期或 candidate 状态知识进入默认指导。
9. MCP/SearchLab/KnowledgeTree 验证通过。
10. 测试或验收报告记录真实命令、结果和剩余风险。
11. 中文文档 UTF-8 无乱码。
```

## 测试与验收

需要运行或补充：

```text
python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
python -m pytest codex-expert-kit/mcp/tests
python -m pytest codex-expert-kit/api/tests
cd ui && npm run build
cd ui && npm run test:e2e
```

如果某项测试尚未具备对应实现，必须在验收报告中说明缺口和补测任务。

## 风险与回滚

| 风险 | 处理 |
| --- | --- |
| 外部项目私有经验污染通用知识库 | 只允许进入 contributions/proposed 或 candidates；必须脱敏和抽象成通用规则 |
| LLM 被误用为交易执行器 | 知识卡、MCP 模板和外接 AGENTS 明确禁止直接下单 |
| candidate/reviewed 被当成 approved | machine_gate、review_status、MCP 默认指导门禁必须阻断 |
| 检索上下文膨胀 | 使用 Retrieval Decision Policy、top-k、machine_gate、字段裁剪 |
| 来源质量不足 | 标记 needs_more_evidence，不进入 reviewed/approved |
| 理论冲突未消解 | 标记 conflict_status，不允许默认指导 |
| 交易结果混入训练输入 | 通过 decision-time feature gate 和 outcome separation 阻断样本 |
| PnL 被误当成唯一标签 | 必须使用多维标签、过程质量和 reason_codes |
| 交易规则本体误塞进 AI Engineering | 拆分知识点，交易规则回 Trading Engineering，AI Engineering 只保留引用、schema、eval 或治理部分 |
| 没有合格标准就训练模型 | 必须先定义 business acceptance criteria 和 task taxonomy |
| LLM 建议直接改策略 | 只能进入 research hypothesis，必须经过回测、样本外、模拟盘和人工审核 |
| live 结果自动回灌训练 | live result 必须先进入反馈治理和人工/规则审核，不可自动贴标签 |

回滚方式：

```text
1. 若知识树扩展不合适，回滚 Phase 36 知识树规划文档，不删除已有正式知识。
2. 若候选知识污染，移出 candidates 或标记 rejected，不进入 formal knowledge。
3. 若正式 reviewed 知识发现问题，降级 review_status 或 machine_gate，不直接删除 approved 规则。
4. 若 MCP/FastAPI/Vue3 对齐出错，回滚对应展示或读取契约，保留原 formal knowledge index。
```

## 状态更新要求

完成任一任务后必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase36_ai_engineering_gating_scoring_knowledge.md
相关 contracts/research/reports 文档
```

不得只更新任务卡而不更新项目级索引。
