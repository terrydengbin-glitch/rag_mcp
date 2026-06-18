# Phase 58: 回测 / 回放 / 模拟盘 / 实盘等效链条知识补充

## Phase 目标

Phase 58 用于补齐 Trading Engineering 中“同一系统内回测、回放、模拟盘和实盘之间的关系与等效条件”知识。核心目标是明确：结果可比不来自环境名称相同，而来自策略真实链条或字段级等效链条一致，并且差异必须可审计。

本 Phase 先创建候选知识和审计包；在外部 reviewed-preparation 严格审计通过后，允许沉淀为 formal reviewed/caveat_only。全程不得创建 approved、default guidance 或 hard gate。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-553 | P0 | done | 创建 Phase 58 任务卡与索引入口 | `docs/tasks/phase58_backtest_sim_live_equivalence_chain.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-552 |
| CEK-TA-554 | P0 | done | 搜索专业资料并梳理业界对 backtest、replay、sandbox/paper、live 的定义和关系 | `docs/research/phase58_backtest_sim_live_equivalence_chain_research.md` | CEK-TA-553 |
| CEK-TA-555 | P0 | done | 创建“真实/等效策略链条”候选知识卡 | `codex-expert-kit/rag/candidates/KB_05_REPLAY_SIMULATION/cand_20260616_phase58_backtest_sim_live_equivalent_chain_001.json` | CEK-TA-554 |
| CEK-TA-556 | P0 | done | 导出候选 AI 审计包并运行 JSON/UTF-8/边界质量门禁 | `docs/audit/phase58_backtest_sim_live_equivalence_chain_candidate_audit_package_20260616.json`、`docs/reports/phase58_backtest_sim_live_equivalence_chain_quality_gate.json` | CEK-TA-555 |
| CEK-TA-557 | P0 | done | 导入外部严格审计结果，将候选升级为 accepted_for_draft 并保留非 reviewed 边界 | `docs/audit/audit_result_phase58_backtest_sim_live_equivalence_chain_20260616_strict_v1.json`、`codex-expert-kit/rag/candidates/KB_05_REPLAY_SIMULATION/cand_20260616_phase58_backtest_sim_live_equivalent_chain_001.json` | CEK-TA-556 |
| CEK-TA-558 | P0 | done | 按审计补丁扩展 environment_equivalence_manifest 字段契约并运行 JSON/UTF-8 门禁 | `docs/reports/phase58_backtest_sim_live_equivalence_chain_quality_gate.json` | CEK-TA-557 |
| CEK-TA-559 | P0 | done | 创建 environment_equivalence_manifest 契约，定义跨环境等效链条字段、owner 和缺失策略 | `docs/contracts/phase58_environment_equivalence_manifest_contract.md` | CEK-TA-558 |
| CEK-TA-560 | P0 | done | 导出 reviewed/caveat_only 准备审计包并运行 JSON/UTF-8 门禁 | `docs/audit/phase58_backtest_sim_live_equivalence_reviewed_preparation_audit_package_20260616.json`、`docs/reports/phase58_backtest_sim_live_equivalence_chain_quality_gate.json` | CEK-TA-559 |
| CEK-TA-561 | P0 | done | 导入 reviewed-preparation 严格审计结果，并补齐 data_quality_identity、venue_adapter_identity、promotion_decision_policy 契约补丁 | `docs/audit/audit_result_phase58_backtest_sim_live_equivalence_reviewed_preparation_20260616_strict_v1.json`、`docs/contracts/phase58_environment_equivalence_manifest_contract.md`、`codex-expert-kit/rag/candidates/KB_05_REPLAY_SIMULATION/cand_20260616_phase58_backtest_sim_live_equivalent_chain_001.json` | CEK-TA-560 |
| CEK-TA-562 | P0 | done | 将通过审计的候选沉淀为 formal reviewed/caveat_only 并重建正式知识索引 | `codex-expert-kit/rag/knowledge/KB_05_REPLAY_SIMULATION/kb_05_replay_simulation.execution_semantics.environment_equivalence_manifest_required.v1.json`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`docs/reports/phase58_reviewed_preparation_import_report.json` | CEK-TA-561 |

## 上游输入

```text
用户需求：创建“回测、模拟盘、实盘必须走真实或等效策略链条才能等效”的知识点
Phase 37 Trading Engineering 知识扩展
Phase 45 Trading Engineering P1 专业知识补全
已有 KB_04_BACKTEST、KB_05_REPLAY_SIMULATION、KB_06_LIVE_EXECUTION 正式知识
联网资料：QuantConnect、NautilusTrader、HftBacktest 等专业平台文档
```

## 下游输出

```text
1. 一条候选知识卡，进入候选审计队列。
2. 一份专业资料研究报告。
3. 一份 AI 审计包，可交给外部 AI/人工进行严格审计。
4. 一份质量门禁报告，说明候选未直接进入 reviewed/approved/default guidance/hard gate。
5. 一份外部严格审计结果归档，说明候选只允许 accepted_for_draft。
6. 一份 environment_equivalence_manifest 契约。
7. 一份 reviewed/caveat_only 准备审计包。
8. 一份 reviewed-preparation 严格审计结果归档。
9. 一条 formal reviewed/caveat_only 正式知识。
10. 重建后的 MCP/SearchLab/Vue3 正式知识索引。
```

## 输入契约

```text
1. 候选必须基于可追溯专业来源。
2. 候选必须区分 backtest、replay、sandbox/paper、live 的环境差异。
3. 候选必须明确“真实链条”或“等效链条”的字段范围。
4. 候选必须说明不等效时如何处理：只能做差异报告，不能声称结果等价。
5. 候选不得包含买卖点、仓位、杠杆、止损止盈或实盘执行建议。
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
source_refs
source_quality
conflict_audit
llm_usage_policy
machine_gate
review
```

### AI 审计包

必须包含：

```text
审计目标
硬边界
候选知识正文
来源列表
需要外部 AI 搜索核验的问题
输出 schema
```

## 边界范围

范围内：

```text
1. 定义 backtest、replay、sandbox/paper、live 的工程关系。
2. 定义策略真实链条或等效链条所需字段。
3. 定义等效性检查和 gap report。
4. 明确 paper/sandbox、replay、live 的不可替代边界。
```

范围外：

```text
1. 不创建 approved 知识。
2. 不修改 MCP / FastAPI / Vue3 运行时代码。
3. 不生成交易策略、买卖点、仓位、杠杆、止损止盈或实盘执行建议。
4. 不要求所有平台必须采用某一个框架或工具。
5. 不允许 reviewed/caveat_only 进入 default guidance queue 或 hard gate。
```

## 涉及组件

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase58_backtest_sim_live_equivalence_chain.md
docs/research/
docs/audit/
docs/reports/
codex-expert-kit/rag/candidates/KB_05_REPLAY_SIMULATION/
codex-expert-kit/rag/knowledge/KB_05_REPLAY_SIMULATION/
codex-expert-kit/rag/indexes/knowledge_items.json
ui/src/data/formalKnowledgeItems.ts
```

## 涉及数据结构

```text
CandidateKnowledgeItem schema v1.1 candidate
AI audit package JSON
Quality gate JSON
```

## 涉及数据库/存储

```text
无数据库迁移。
仅新增文件化候选知识、研究报告、审计包和质量报告。
```

## 实施步骤

```text
1. 创建 Phase 58 任务卡和索引入口。
2. 搜索并归纳专业平台对 backtest、replay、sandbox/paper、live 的定义。
3. 对齐已有 Trading Engineering 知识树，确定主归属 KB_05_REPLAY_SIMULATION。
4. 创建候选知识卡。
5. 导出 AI 审计包。
6. 运行 JSON、UTF-8、候选边界和默认指导门禁。
7. 导入外部审计结果，更新候选状态和 patch notes。
8. 创建 environment_equivalence_manifest 字段契约。
9. 导出 reviewed/caveat_only 准备审计包，等待外部 AI/人工审计。
```

## Definition of Done

```text
1. Phase 58 任务卡存在。
2. docs/index_tasks.md 和 docs/tasks/README.md 已更新。
3. 研究报告存在并包含来源链接。
4. 候选知识卡存在，来源、适用范围、不适用范围、冲突状态、review 状态齐全。
5. 审计包存在，明确不得直接 reviewed/approved/default guidance/hard gate。
6. JSON 可解析，中文 UTF-8 无乱码。
7. 候选未进入正式知识索引。
8. 外部审计结果已归档，候选状态为 accepted_for_draft，仍禁止 reviewed/approved/default guidance/hard gate。
9. environment_equivalence_manifest 契约存在，字段、owner、缺失策略和 machine gate 边界清晰。
10. reviewed/caveat_only 准备审计包存在。
11. reviewed-preparation 审计结果已归档，结论为 accepted_for_reviewed_caveat_only。
12. formal reviewed/caveat_only 知识已创建，并明确 approved_allowed=false、default_guidance_allowed=false、hard_gate_allowed=false。
13. 正式知识索引和 Vue3 fixture 已重建。
```

## 测试与验收

```text
1. python -m json.tool 校验候选 JSON。
2. python -m json.tool 校验审计包 JSON。
3. python -m json.tool 校验质量门禁 JSON。
4. UTF-8 读取关键中文文档。
5. 检查候选 machine_gate.default_guidance=deny。
6. 检查 formal knowledge review_status=reviewed 且 reviewed_mode=caveat_only。
7. 检查 knowledge_items.json 可以命中新知识 ID。
```

## 风险与回滚

风险：

```text
1. 候选跨 Backtest / Replay / Live Execution 多分支，可能与已有知识重叠。
2. 外部来源主要是平台文档，正式 reviewed 前仍需外部 AI/人工审计。
3. 如果 source 只支持某平台语义，不能泛化到所有市场。
```

回滚：

```text
1. 删除 Phase 58 新增候选、研究报告、审计包和质量报告。
2. 从 docs/index_tasks.md 和 docs/tasks/README.md 移除 Phase 58 入口。
3. 不影响正式 knowledge_items.json，因为本 Phase 不写正式知识索引。
```

## 需要开发者确认的问题

```text
1. 外部审计通过后，是否将本知识沉淀为 formal reviewed/caveat_only。
2. 是否需要拆出更细的后续知识：策略链条字段契约、环境 gap report schema、回测到实盘 promotion checklist。
```

## 状态更新要求

```text
完成后更新 docs/index_tasks.md、docs/tasks/README.md 和本任务卡状态。
```
