# Phase 60: Sandbox / Replay / Paper Trading 环境治理知识扩展

## Phase 目标

Phase 60 用于补齐“沙盒、测试网、历史回放、实时模拟执行、模拟盘 / paper trading、实盘 canary”之间的专业边界、证据契约和晋级治理知识。

核心目标不是证明策略有收益，而是让外接项目能够用一致的环境治理框架回答：

```text
1. 当前跑在哪一种环境？
2. 数据、时钟、撮合、成交、费用、延迟、风控和订单状态是否等效或已声明差异？
3. 从回测 / 回放 / 沙盒 / 模拟盘进入下一阶段需要哪些证据？
4. sandbox、testnet、paper trading、live canary 的结果各自能证明什么，不能证明什么？
5. 如何用 gap report、promotion decision 和 audit trace 管理测试到实盘的过渡？
```

本 Phase 只创建知识范围、契约、候选知识、审计包和后续 formal reviewed/caveat_only 沉淀任务。不得创建 approved、default guidance 或 hard gate。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-571 | P0 | done | 创建 Phase 60 任务卡与索引入口 | `docs/tasks/phase60_sandbox_replay_paper_environment_governance.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-570 |
| CEK-TA-572 | P0 | done | 搜索专业资料并梳理 sandbox、testnet、historical replay、paper trading、live canary 的环境语义和案例 | `docs/research/phase60_sandbox_replay_paper_environment_research.md` | CEK-TA-571 |
| CEK-TA-573 | P0 | done | 定义 Sandbox / Replay / Paper Environment Contract | `docs/contracts/phase60_sandbox_replay_paper_environment_contract.md` | CEK-TA-572 |
| CEK-TA-574 | P0 | done | 定义 Environment Promotion Decision 与 Sandbox/Paper/Live Gap Report 契约 | `docs/contracts/phase60_environment_promotion_gap_report_contract.md` | CEK-TA-573 |
| CEK-TA-575 | P0 | done | 创建 P0 候选知识卡：环境分类、sandbox 与 paper 边界、replay market impact、environment manifest、promotion gate、gap report、testnet 隔离、static sandbox 边界、paper trading 限制、统一订单生命周期 | `codex-expert-kit/rag/candidates/KB_05_REPLAY_SIMULATION/cand_20260617_phase60_environment_taxonomy_required_001.json`、`codex-expert-kit/rag/candidates/KB_06_LIVE_EXECUTION/cand_20260617_phase60_static_api_sandbox_contract_only_001.json`、`codex-expert-kit/rag/candidates/KB_06_LIVE_EXECUTION/cand_20260617_phase60_testnet_endpoint_isolation_required_001.json`、`codex-expert-kit/rag/candidates/KB_05_REPLAY_SIMULATION/cand_20260617_phase60_paper_trading_not_live_required_001.json`、`codex-expert-kit/rag/candidates/KB_05_REPLAY_SIMULATION/cand_20260617_phase60_replay_market_impact_assumption_required_001.json`、`codex-expert-kit/rag/candidates/KB_05_REPLAY_SIMULATION/cand_20260617_phase60_environment_manifest_required_001.json`、`codex-expert-kit/rag/candidates/KB_07_RISK_MANAGEMENT/cand_20260617_phase60_environment_promotion_evidence_required_001.json`、`codex-expert-kit/rag/candidates/KB_05_REPLAY_SIMULATION/cand_20260617_phase60_sandbox_paper_live_gap_report_required_001.json`、`codex-expert-kit/rag/candidates/KB_06_LIVE_EXECUTION/cand_20260617_phase60_order_lifecycle_mapping_required_001.json`、`codex-expert-kit/rag/candidates/KB_07_RISK_MANAGEMENT/cand_20260617_phase60_sandbox_risk_rehearsal_not_hard_gate_001.json` | CEK-TA-574 |
| CEK-TA-576 | P0 | done | 导出 Phase 60 候选 AI 审计包并运行 JSON/UTF-8/边界质量门禁 | `docs/audit/phase60_sandbox_replay_paper_candidate_audit_package_20260617.json`、`docs/reports/phase60_candidate_quality_gate.json`、`docs/reports/phase60_p0_candidate_generation_report.json` | CEK-TA-575 |
| CEK-TA-577 | P0 | done | 导入外部严格审计结果，按 accepted_for_draft / needs_more_evidence / rejected / blocked 回写候选状态和补丁点 | `docs/audit/audit_result_phase60_candidate_20260617_strict_v1.json`、`docs/reports/phase60_candidate_audit_import_report.json`、`codex-expert-kit/rag/scripts/apply_phase60_candidate_audit_result.py`、`ui/src/data/phase23Candidates.ts`、`ui/public/data/phase23Candidates.json` | CEK-TA-576 |
| CEK-TA-578 | P0 | done | 对 accepted_for_draft 候选导出 reviewed/caveat_only 准备审计包，阻止候选直接进入 formal reviewed | `docs/audit/phase60_reviewed_preparation_audit_package_20260617.json`、`docs/reports/phase60_reviewed_preparation_gap_report.json`、`docs/reports/phase60_reviewed_preparation_export_report.json`、`codex-expert-kit/rag/scripts/export_phase60_reviewed_preparation_audit_package.py`、`ui/src/data/phase23Candidates.ts`、`ui/public/data/phase23Candidates.json` | CEK-TA-577 |
| CEK-TA-579 | P0 | done | 导入 reviewed/caveat_only 审计结果；10 条 Phase 60 P0 候选均已沉淀为 formal reviewed/caveat_only，未进入 approved/default guidance/hard gate | `docs/audit/audit_result_phase60_reviewed_preparation_20260617_strict_v1.json`、`docs/reports/phase60_reviewed_preparation_import_report.json`、`docs/audit/phase60_a07_a10_supplemental_reaudit_package_20260617.json`、`docs/reports/phase60_a07_a10_supplemental_reaudit_report.json`、`docs/audit/audit_result_phase60_a07_a10_supplemental_reaudit_20260617_strict_v1.json`、`docs/reports/phase60_a07_a10_supplemental_reaudit_import_report.json`、`codex-expert-kit/rag/scripts/apply_phase60_reviewed_preparation_result.py`、`codex-expert-kit/rag/scripts/prepare_phase60_a07_a10_supplemental_reaudit.py`、`codex-expert-kit/rag/scripts/apply_phase60_a07_a10_supplemental_reaudit_result.py`、`codex-expert-kit/rag/knowledge/KB_05_REPLAY_SIMULATION/`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/`、`codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/public/data/formalKnowledgeItems.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-578 |
| CEK-TA-580 | P1 | done | 验证 MCP/SearchLab/KnowledgeTree/Vue3 能检索 Phase 60 知识，并生成验收报告 | `codex-expert-kit/rag/scripts/validate_phase60_runtime_linkage.py`、`docs/reports/phase60_runtime_linkage_validation_report.json`、`docs/reports/phase60_sandbox_replay_paper_environment_report.md` | CEK-TA-579 |
| CEK-TA-581 | P1 | done | 明确 Phase 60 P1 6 条增强知识范围：FIX/券商认证、场景回放库、paper account reset、实时模拟健康监控、live canary rollback、环境漂移监控 | `docs/research/phase60_p1_enhanced_environment_governance_scope.md`、`docs/tasks/phase60_sandbox_replay_paper_environment_governance.md` | CEK-TA-580 |
| CEK-TA-582 | P1 | done | 联网采集 Phase 60 P1 6 条增强知识来源，生成候选知识包并运行来源、冲突、边界、UTF-8 和污染门禁 | `codex-expert-kit/rag/scripts/generate_phase60_p1_candidates.py`、`codex-expert-kit/rag/candidates/KB_05_REPLAY_SIMULATION/`、`codex-expert-kit/rag/candidates/KB_06_LIVE_EXECUTION/`、`codex-expert-kit/rag/candidates/KB_07_RISK_MANAGEMENT/`、`docs/reports/phase60_p1_candidate_generation_report.json`、`docs/reports/phase60_p1_candidate_quality_gate.json` | CEK-TA-581 |
| CEK-TA-583 | P1 | done | 导出 Phase 60 P1 6 条候选 AI 审计包，等待外部 AI/人工严格审计 | `codex-expert-kit/rag/scripts/export_phase60_p1_candidate_audit_package.py`、`docs/audit/phase60_p1_candidate_audit_package_20260617.json`、`docs/reports/phase60_p1_candidate_audit_package_quality_gate.json`、`docs/reports/phase60_p1_candidate_audit_package_export_report.json`、`ui/src/data/phase23Candidates.ts`、`ui/public/data/phase23Candidates.json` | CEK-TA-582 |
| CEK-TA-584 | P1 | done | 按外部审计结果回写 P1 候选状态，处理 accepted_for_draft / needs_more_evidence / rejected / blocked，不创建 reviewed 或 approved | `docs/audit/audit_result_phase60_p1_candidate_20260617_strict_v1.json`、`codex-expert-kit/rag/scripts/apply_phase60_p1_candidate_audit_result.py`、`docs/reports/phase60_p1_candidate_audit_import_report.json`、`ui/src/data/phase23Candidates.ts`、`ui/public/data/phase23Candidates.json` | CEK-TA-583 |
| CEK-TA-585 | P1 | done | 对 accepted_for_draft 的 P1 候选导出 reviewed/caveat_only 准备审计包，阻止候选直接进入 formal reviewed | `codex-expert-kit/rag/scripts/export_phase60_p1_reviewed_preparation_audit_package.py`、`docs/audit/phase60_p1_reviewed_preparation_audit_package_20260617.json`、`docs/reports/phase60_p1_reviewed_preparation_gap_report.json`、`docs/reports/phase60_p1_reviewed_preparation_export_report.json` | CEK-TA-584 |
| CEK-TA-586 | P1 | done | 导入 P1 reviewed/caveat_only 审计结果；3 条已沉淀 formal reviewed/caveat_only，3 条保持 needs_more_evidence，不创建 approved、default guidance 或 hard gate | `docs/audit/audit_result_phase60_p1_reviewed_preparation_20260618_strict_v1.json`、`codex-expert-kit/rag/scripts/apply_phase60_p1_reviewed_preparation_result.py`、`docs/reports/phase60_p1_reviewed_preparation_import_report.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_phase60_live_execution.adapter_certification.fix_broker_certification_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_phase60_live_execution.paper_account_state.reset_trace_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_phase60_live_execution.environment_health.monitor_required.v1.json`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/public/data/formalKnowledgeItems.json`、`ui/src/data/phase23Candidates.ts`、`ui/public/data/phase23Candidates.json` | CEK-TA-585 |
| CEK-TA-587 | P1 | done | 为 P60-P1-02 / P60-P1-05 / P60-P1-06 补充来源证据并导出 reviewed/caveat_only 补证复审包 | `codex-expert-kit/rag/scripts/prepare_phase60_p1_supplemental_reaudit.py`、`docs/audit/phase60_p1_needs_evidence_supplemental_reaudit_package_20260618.json`、`docs/reports/phase60_p1_needs_evidence_supplemental_reaudit_report.json`、`docs/research/phase60_p1_needs_evidence_supplemental_research.md`、`ui/src/data/phase23Candidates.ts`、`ui/public/data/phase23Candidates.json` | CEK-TA-586 |
| CEK-TA-588 | P1 | done | 导入 P1 needs_more_evidence 补证复审结果，3 条剩余候选均沉淀为 formal reviewed/caveat_only，不创建 approved、default guidance 或 hard gate | `docs/audit/audit_result_phase60_p1_needs_evidence_supplemental_reaudit_20260618_strict_v1.json`、`codex-expert-kit/rag/scripts/apply_phase60_p1_supplemental_reaudit_result.py`、`docs/reports/phase60_p1_supplemental_reaudit_import_report.json`、`codex-expert-kit/rag/knowledge/KB_05_REPLAY_SIMULATION/kb_phase60_replay_simulation.scenario_library.versioned_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/kb_phase60_risk_management.live_canary.rollback_owner_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_05_REPLAY_SIMULATION/kb_phase60_replay_simulation.environment_drift.monitor_required.v1.json` | CEK-TA-587 |
| CEK-TA-589 | P1 | done | 验证 MCP/SearchLab/KnowledgeTree/Vue3 能检索 Phase 60 P1 全量知识并更新 Phase 60 最终报告 | `codex-expert-kit/rag/scripts/validate_phase60_runtime_linkage.py`、`docs/reports/phase60_runtime_linkage_validation_report.json`、`docs/reports/phase60_sandbox_replay_paper_environment_report.md`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/public/data/formalKnowledgeItems.json`、`ui/src/data/phase23Candidates.ts`、`ui/public/data/phase23Candidates.json`、`ui/public/data/knowledgeTreeScopeIndex.json` | CEK-TA-588 |

## 上游输入

```text
Phase 37 Trading Engineering 专业知识库扩展
Phase 45 Trading Engineering P1 专业知识补全
Phase 58 回测 / 回放 / 模拟盘 / 实盘等效链条知识补充
Phase 59 Microstructure Feature Store 与 Hybrid Snapshot Contract
docs/contracts/phase58_environment_equivalence_manifest_contract.md
docs/contracts/phase37_replay_simulation_execution_assumption_contract.md
docs/contracts/phase37_backtest_run_manifest_contract.md
NautilusTrader、QuantConnect、HftBacktest、IBKR、Alpaca、Binance Testnet、Coinbase Sandbox、FIX Execution Report 等专业资料
```

## 下游输出

```text
1. 一份 sandbox / replay / paper / live canary 环境治理研究报告。
2. 一份环境契约，定义 environment_id、environment_type、data_source、execution_adapter、clock、fill/latency/fee/risk policy 和 audit trace。
3. 一份 promotion / gap report 契约，定义从一个环境进入下一环境的证据、阻断原因和人工复核字段。
4. 一批候选知识，进入候选审计队列。
5. 一份 AI 审计包，供外部 AI / 人工严格审计。
6. reviewed/caveat_only 通过后，正式知识可被 MCP/SearchLab/KnowledgeTree/Vue3 检索。
```

## 输入契约

```text
1. 所有候选必须有来源、source_type、适用范围、不适用场景、confidence、freshness、review_status 和 conflict_audit。
2. 任何 sandbox、testnet、paper trading、replay 来源都必须标注具体平台、市场、账户模式、API 版本或数据类型边界。
3. 内部契约字段必须区分环境事实、模拟假设、真实订单事实、风控政策和 promotion decision。
4. 不得把某个平台的 sandbox/testnet/paper trading 行为泛化为所有交易所、券商或资产类别。
5. 不得把沙盒或模拟盘结果写成策略有效、实盘许可、风控阈值或 hard gate。
```

## 输出契约

### Environment Manifest

必须覆盖：

```text
environment_id
environment_type: static_api_sandbox | exchange_testnet | historical_replay | realtime_simulation | paper_trading | live_canary | live
data_source_type
market_data_realtime_or_historical
clock_policy
execution_adapter_type
venue_adapter_ref
account_scope
api_endpoint_scope
fill_model_ref
latency_model_ref
fee_model_ref
market_impact_assumption
order_state_mapping_ref
risk_policy_ref
audit_trace_id
not_valid_for
```

### Promotion Decision

必须覆盖：

```text
from_environment
to_environment
required_evidence
gap_report_id
open_blockers
manual_review_required
decision_owner
decision_timestamp
promotion_decision: promote | hold | block | needs_more_evidence
rollback_plan_ref
```

### Gap Report

必须覆盖：

```text
environment_pair
data_gap
clock_gap
fill_gap
fee_gap
latency_gap
order_state_gap
risk_policy_gap
account_or_margin_gap
unsupported_order_type
known_simulation_limitation
severity
owner
resolution_status
```

## 边界范围

范围内：

```text
1. 定义 sandbox、testnet、historical replay、real-time simulation、paper trading、live canary 的用途和边界。
2. 定义环境 manifest、promotion decision、gap report 的字段和 owner。
3. 定义如何用沙盒环节验证 API contract、订单生命周期、错误处理、重试、风控 rehearsal 和审计日志。
4. 定义如何把 Phase 58 的等效链条落实到环境晋级证据。
5. 创建候选知识和审计包，等待外部严格审计。
```

范围外：

```text
1. 不接入真实交易所、券商、testnet、paper account 或 API key。
2. 不启动真实订单、模拟订单或自动交易。
3. 不创建新的数据库、服务或外部依赖。
4. 不把任何候选直接写入 approved、default guidance 或 hard gate。
5. 不给出买卖点、仓位、杠杆、止损止盈、风险阈值或实盘执行建议。
6. 不把 sandbox/paper trading 盈亏解释为可复用策略优势。
```

## 涉及组件

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase60_sandbox_replay_paper_environment_governance.md
docs/research/
docs/contracts/
docs/audit/
docs/reports/
codex-expert-kit/rag/candidates/KB_05_REPLAY_SIMULATION/
codex-expert-kit/rag/candidates/KB_06_LIVE_EXECUTION/
codex-expert-kit/rag/candidates/KB_07_RISK_MANAGEMENT/
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/indexes/knowledge_items.json
ui/src/data/
ui/public/data/
```

## 涉及数据结构

```text
CandidateKnowledgeItem schema v1.1 candidate
EnvironmentManifest
EnvironmentPromotionDecision
SandboxPaperLiveGapReport
AI audit package JSON
Quality gate JSON
Formal reviewed/caveat_only knowledge item
```

## 涉及数据库/存储

```text
本 Phase 不创建真实数据库、表、迁移或存储服务。
只定义环境治理、晋级决策和 gap report 的知识契约字段。
```

## 实施步骤

```text
1. 创建 Phase 60 任务卡和索引入口。
2. 搜索并归纳 sandbox / testnet / replay / paper trading / live canary 专业资料。
3. 对齐 Phase 37、Phase 45、Phase 58、Phase 59 现有知识和契约。
4. 定义 Environment Manifest、Promotion Decision 和 Gap Report 契约。
5. 创建 P0 候选知识卡。
6. 导出 AI 审计包。
7. 运行 JSON、UTF-8、候选边界、默认指导和 hard gate 门禁。
8. 根据外部审计结果回写候选并补证。
9. reviewed/caveat_only 审计通过后再沉淀正式知识。
10. 重建索引、Vue3 fixture，并验证 MCP/SearchLab/KnowledgeTree 可检索。
```

## Definition of Done

```text
1. Phase 60 任务卡存在。
2. docs/index_tasks.md 和 docs/tasks/README.md 已更新。
3. 研究报告存在并带来源链接、来源类型和适用边界。
4. 契约文档存在，字段、owner、状态流和不做什么清晰。
5. 候选知识卡存在，来源、适用范围、不适用场景、冲突状态和 machine gate 齐全。
6. AI 审计包存在，明确禁止 reviewed/approved/default guidance/hard gate 的越级授权。
7. reviewed/caveat_only 前必须经过单独准备审计。
8. JSON 可解析，中文 UTF-8 无乱码。
9. 正式知识沉淀后，knowledge_items.json、Vue3 fixture、MCP/SearchLab/KnowledgeTree 联动验证通过。
```

## 测试与验收

```text
1. python -m json.tool 校验候选 JSON。
2. python -m json.tool 校验审计包 JSON。
3. python -m json.tool 校验质量门禁 JSON。
4. 运行 no_mojibake 校验，确认中文 UTF-8 无乱码。
5. 检查候选 machine_gate.default_guidance=deny。
6. 检查候选阶段不进入正式 knowledge_items.json。
7. formal reviewed/caveat_only 通过后运行知识索引、Vue3 fixture、MCP/SearchLab/KnowledgeTree 联动验证。
```

## 风险与回滚

风险：

```text
1. sandbox、testnet、paper trading、live canary 容易被误读为同一种模拟环境。
2. 平台文档往往只适用于特定 broker、exchange、asset class 或 API 版本。
3. paper trading 盈亏容易被错误解释成策略可实盘。
4. replay 的成交、队列位置、market impact、延迟模型容易被过度泛化。
```

回滚：

```text
1. 删除 Phase 60 新增候选、研究报告、契约、审计包和报告。
2. 从 docs/index_tasks.md 和 docs/tasks/README.md 移除 Phase 60 入口。
3. 重建候选或正式 fixture。
4. 如果尚未创建 formal reviewed 知识，不影响正式 knowledge_items.json。
```

## 需要开发者确认的问题

```text
1. Phase 60 P0 候选数量是否先控制在 10 条，还是同时扩展 P1 的 6 条。
2. reviewed/caveat_only 通过后，是否需要额外创建 Vue3 环境治理筛选标签。
3. 是否需要后续单独开 Phase，将 Environment Manifest 落成外部项目可用的 JSON schema 模板。
```

## 状态更新要求

```text
完成每个任务后更新 docs/index_tasks.md、docs/tasks/README.md 和本任务卡状态。
不得在未完成 DoD 和测试前把任务标记为 done。
```
