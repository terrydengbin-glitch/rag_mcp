# Phase 37: Trading Engineering 专业知识库扩展

## Phase 目标

Phase 37 用于承接 Phase 36 划出的跨分支边界：K 线、策略、数据工程、回测、回放、模拟盘、实盘执行、风控、交易复盘等交易专业规则本体，必须进入 Trading Engineering 对应分支，不能一股脑塞进 AI Engineering。

本 Phase 先固化 Trading Engineering 需要完善的知识库分区、知识点清单、上下游契约、边界和审计要求。后续每条知识点必须经过联网采集、来源评分、冲突审计、候选审核、formal reviewed/approved 治理流程，不能直接写成默认指导。

核心定位：

```text
Trading Engineering 负责交易专业规则本体。
AI Engineering 负责如何引用、训练、检索、评估和治理这些交易规则。
```

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-189 | P0 | done | 定义 Trading Engineering 知识分支边界和 P0 知识点范围 | `docs/research/phase37_trading_engineering_knowledge_scope.md` | CEK-TA-179 |
| CEK-TA-190 | P0 | done | 生成 Trading Engineering 知识范围审计 JSON | `docs/audit/phase37_trading_engineering_knowledge_scope_for_audit.json` | CEK-TA-189 |
| CEK-TA-191 | P0 | done | 对齐 Trading Engineering 与 AI Engineering 的跨分支引用契约 | `docs/contracts/trading_ai_cross_branch_knowledge_contract.md` | CEK-TA-189 |
| CEK-TA-192 | P0 | done | 创建 Trading Engineering P0 ResearchIngestionTask 队列 | `docs/research/phase37_trading_engineering_research_task_queue.md` | CEK-TA-190 |
| CEK-TA-193 | P1 | done | 检查并修正知识树 Trading 分支与 13 分区命名映射 | `codex-expert-kit/rag/knowledge_tree.md`、`docs/reports/phase37_trading_tree_mapping_report.md` | CEK-TA-191 |
| CEK-TA-194 | P1 | done | 采集并生成首批 Trading Engineering P0 候选知识包 | `codex-expert-kit/rag/candidates/KB_01_QUANT_FOUNDATION/`、`docs/reports/phase37_trading_collection_report.md` | CEK-TA-192 |
| CEK-TA-195 | P1 | done | 运行来源评分、冲突检测、污染门禁和候选审计导出 | `docs/audit/phase37_quant_foundation_candidate_audit_package_20260611.json`、`docs/reports/phase37_quant_foundation_candidate_quality_gate.json`、验证脚本输出 | CEK-TA-194 |
| CEK-TA-196 | P1 | done | 将通过 reviewed-preparation 审计的候选沉淀为 formal reviewed 知识并重建索引 | `codex-expert-kit/rag/knowledge/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts` | CEK-TA-380 |
| CEK-TA-197 | P1 | done | 验证 MCP/SearchLab/KnowledgeTree 能按 Trading 分支命中、引用、阻断和降级 | `codex-expert-kit/rag/scripts/validate_phase37_runtime_linkage.py`、`docs/reports/phase37_runtime_linkage_validation_report.json` | CEK-TA-196 |
| CEK-TA-198 | P1 | done | 生成 Phase 37 验收报告并更新索引 | `docs/reports/phase37_trading_engineering_knowledge_expansion_report.md` | CEK-TA-197 |
| CEK-TA-375 | P1 | done | 处理 Quant Foundation 首轮审计结果，回写 accepted/needs_more_evidence，并为 3 条补证生成二审包 | `docs/audit/audit_result_phase37_quant_foundation_candidate_audit_20260611_strict_v1.json`、`docs/reports/phase37_quant_foundation_audit_import_report.json`、`docs/audit/phase37_quant_foundation_supplemental_reaudit_package_20260611.json` | CEK-TA-195 |
| CEK-TA-376 | P1 | done | 处理 Quant Foundation 二审结果，回写 2 条 accepted_for_draft 和 1 条继续 needs_more_evidence | `docs/audit/audit_result_phase37_quant_foundation_supplemental_reaudit_20260611_strict_v1.json`、`docs/reports/phase37_quant_foundation_supplemental_reaudit_import_report.json` | CEK-TA-375 |
| CEK-TA-377 | P1 | done | 为 P37-A-Q02 R-multiple 定义补强专业来源、修正 risk-normalized metrics 主分类并导出三审包 | `codex-expert-kit/rag/knowledge_tree.md`、`docs/research/phase37_q02_r_multiple_third_audit_research.md`、`docs/audit/phase37_q02_r_multiple_third_audit_package_20260611.json`、`docs/reports/phase37_q02_r_multiple_third_audit_package_report.json` | CEK-TA-376 |
| CEK-TA-378 | P1 | done | 导入 P37-A-Q02 三审结果，将候选升级为 accepted_for_draft 并保留 reviewed/approved/default/hard gate 阻断 | `docs/audit/phase37_q02_r_multiple_third_audit_result_20260611_strict_v1.json`、`docs/reports/phase37_q02_r_multiple_third_audit_import_report.json` | CEK-TA-377 |
| CEK-TA-379 | P1 | done | 导出 Quant Foundation reviewed/caveat_only 准备审计包，阻止 accepted_for_draft 直接入 reviewed | `docs/audit/phase37_quant_foundation_reviewed_preparation_audit_package_20260611.json`、`docs/reports/phase37_quant_foundation_reviewed_preparation_gap_report.json`、`codex-expert-kit/rag/scripts/export_phase37_quant_foundation_reviewed_preparation_package.py` | CEK-TA-378 |
| CEK-TA-380 | P1 | done | 导入 Quant Foundation reviewed-preparation 审计结果，9 条沉淀为 formal reviewed/caveat_only，3 条回到补证队列 | `docs/audit/phase37_quant_foundation_reviewed_preparation_audit_result_20260611_strict_v2.json`、`docs/reports/phase37_quant_foundation_reviewed_preparation_import_report.json`、`codex-expert-kit/rag/knowledge/KB_01_QUANT_FOUNDATION/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts` | CEK-TA-379 |
| CEK-TA-381 | P1 | done | 为 P37-A-Q02/Q06/Q11 补充 reviewed 阻断证据并导出再审包 | `docs/research/phase37_quant_foundation_blocked_supplemental_research.md`、`docs/audit/phase37_quant_foundation_blocked_supplemental_reaudit_package_20260611.json`、`docs/reports/phase37_quant_foundation_blocked_supplemental_reaudit_report.json` | CEK-TA-380 |
| CEK-TA-382 | P1 | done | 导入 P37-A-Q02/Q06/Q11 阻断项再审结果，3 条转 formal reviewed/caveat_only 并重建索引 | `docs/audit/audit_result_phase37_quant_foundation_blocked_supplemental_reaudit_20260611_strict_v3.json`、`docs/reports/phase37_quant_foundation_blocked_supplemental_reaudit_import_report.json`、`codex-expert-kit/rag/knowledge/KB_01_QUANT_FOUNDATION/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts` | CEK-TA-381 |
| CEK-TA-383 | P1 | done | 采集并生成 Trading Engineering Data Engineering 12 条候选知识 | `codex-expert-kit/rag/scripts/generate_phase37_data_engineering_candidates.py`、`codex-expert-kit/rag/candidates/KB_02_DATA_ENGINEERING/`、`docs/research/phase37_data_engineering_candidate_research.md`、`docs/reports/phase37_data_engineering_candidate_generation_report.md` | CEK-TA-198 |
| CEK-TA-384 | P1 | done | 导出 Data Engineering 候选 AI 审计包 | `codex-expert-kit/rag/scripts/export_phase37_data_engineering_candidate_audit_package.py`、`docs/audit/phase37_data_engineering_candidate_audit_package_20260611.json` | CEK-TA-383 |
| CEK-TA-385 | P1 | done | 运行 Data Engineering 来源、冲突、乱码和污染质量门禁 | `docs/reports/phase37_data_engineering_candidate_quality_gate.json`、`docs/reports/phase37_data_engineering_candidate_audit_package_quality_gate.json`、`ui/src/data/phase23Candidates.ts`、`ui/src/types.ts`、`ui/src/stores/auditStore.ts`、`codex-expert-kit/api/codex_expert_kit_api/services.py` | CEK-TA-384 |
| CEK-TA-386 | P1 | done | 导入 Data Engineering 首轮严格审计结果，12 条回写为 accepted_for_draft 并保持 reviewed/approved/default/hard gate 阻断 | `codex-expert-kit/rag/scripts/apply_phase37_data_engineering_audit_result.py`、`docs/audit/audit_result_phase37_data_engineering_candidate_audit_20260611_strict_v1.json`、`docs/reports/phase37_data_engineering_audit_import_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-385 |
| CEK-TA-387 | P1 | done | 导出 Data Engineering reviewed/caveat_only 准备审计包，阻止 accepted_for_draft 直接入 formal reviewed | `codex-expert-kit/rag/scripts/export_phase37_data_engineering_reviewed_preparation_package.py`、`docs/audit/phase37_data_engineering_reviewed_preparation_audit_package_20260611.json`、`docs/reports/phase37_data_engineering_reviewed_preparation_gap_report.json` | CEK-TA-386 |
| CEK-TA-388 | P1 | done | 处理 Data Engineering 首轮审计结果 meta-audit，归档 schema_patched 版本并修正 confidence 枚举 | `docs/audit/meta_audit_result_phase37_data_engineering_candidate_audit_20260611_strict_v1.json`、`docs/audit/audit_result_phase37_data_engineering_candidate_audit_20260611_strict_v1_schema_patched.json`、`docs/reports/phase37_data_engineering_audit_import_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-386 |
| CEK-TA-389 | P1 | done | 导入 Data Engineering reviewed-preparation 审计结果，10 条沉淀为 formal reviewed/caveat_only，2 条回到补证队列 | `codex-expert-kit/rag/scripts/apply_phase37_data_engineering_reviewed_preparation_result.py`、`docs/audit/audit_result_phase37_data_engineering_reviewed_preparation_20260611_strict_v1.json`、`docs/reports/phase37_data_engineering_reviewed_preparation_import_report.json`、`codex-expert-kit/rag/knowledge/KB_02_DATA_ENGINEERING/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-387 |
| CEK-TA-390 | P1 | done | 为 P37-B-D10/D11 补充 reviewed 阻断证据并导出再审包 | `codex-expert-kit/rag/scripts/supplement_phase37_data_engineering_blocked_candidates.py`、`docs/contracts/phase37_data_engineering_dataset_layers_contract.md`、`docs/research/phase37_data_engineering_blocked_supplemental_research.md`、`docs/audit/phase37_data_engineering_blocked_supplemental_reaudit_package_20260611.json`、`docs/reports/phase37_data_engineering_blocked_supplemental_reaudit_report.json` | CEK-TA-389 |
| CEK-TA-391 | P1 | done | 导入 P37-B-D10/D11 阻断项再审结果，D10 沉淀 formal reviewed/caveat_only，D11 继续补证 | `codex-expert-kit/rag/scripts/apply_phase37_data_engineering_blocked_supplemental_reaudit_result.py`、`docs/audit/audit_result_phase37_data_engineering_blocked_supplemental_reaudit_20260611_strict_v1.json`、`docs/reports/phase37_data_engineering_blocked_supplemental_reaudit_import_report.json`、`codex-expert-kit/rag/knowledge/KB_02_DATA_ENGINEERING/kb_02_data_engineering.outlier_detection_required.v1.json`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-390 |
| CEK-TA-392 | P1 | done | 为 P37-B-D11 内联 CEK-TA 数据层契约正文并补 lineage 标准来源，导出三审包 | `codex-expert-kit/rag/scripts/supplement_phase37_data_engineering_d11_contract_inline_third_audit.py`、`docs/research/phase37_data_engineering_d11_contract_inline_third_audit_research.md`、`docs/audit/phase37_data_engineering_d11_contract_inline_third_audit_package_20260611.json`、`docs/reports/phase37_data_engineering_d11_contract_inline_third_audit_report.json`、`codex-expert-kit/rag/candidates/KB_02_DATA_ENGINEERING/cand_20260611_phase37_data_engineering_raw_vs_adjusted_data_boundary_001.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-391 |
| CEK-TA-393 | P1 | done | 导入 P37-B-D11 契约内联三审结果，沉淀 formal reviewed/caveat_only 并重建索引 | `codex-expert-kit/rag/scripts/apply_phase37_data_engineering_d11_contract_inline_third_audit_result.py`、`docs/audit/audit_result_phase37_data_engineering_d11_contract_inline_third_audit_20260611_strict_v1.json`、`docs/reports/phase37_data_engineering_d11_contract_inline_third_audit_import_report.json`、`codex-expert-kit/rag/knowledge/KB_02_DATA_ENGINEERING/kb_02_data_engineering.raw_vs_adjusted_data_boundary.v1.json`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts`、`docs/reports/phase37_runtime_linkage_validation_report.json` | CEK-TA-392 |
| CEK-TA-394 | P1 | done | 采集并生成 Trading Engineering Kline / Strategy Engineering 12 条候选知识 | `codex-expert-kit/rag/scripts/generate_phase37_kline_strategy_candidates.py`、`codex-expert-kit/rag/candidates/KB_02_KLINE_STRATEGY/`、`docs/research/phase37_kline_strategy_candidate_research.md`、`docs/reports/phase37_kline_strategy_candidate_generation_report.md`、`docs/reports/phase37_kline_strategy_candidate_quality_gate.json` | CEK-TA-393 |
| CEK-TA-395 | P1 | done | 导出 Kline / Strategy Engineering 候选 AI 审计包 | `codex-expert-kit/rag/scripts/export_phase37_kline_strategy_candidate_audit_package.py`、`docs/audit/phase37_kline_strategy_candidate_audit_package_20260611.json`、`docs/reports/phase37_kline_strategy_candidate_audit_package_quality_gate.json` | CEK-TA-394 |
| CEK-TA-396 | P1 | done | 导入 Kline / Strategy Engineering 首轮严格审计结果并分流 accepted/needs_more_evidence/rejected | `codex-expert-kit/rag/scripts/apply_phase37_kline_strategy_audit_result.py`、`docs/audit/audit_result_phase37_kline_strategy_candidate_audit_20260611_strict_v1.json`、`docs/reports/phase37_kline_strategy_audit_import_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-395 |
| CEK-TA-397 | P1 | done | 为 P37-C-K04/K05/K10/K12 补充止损、止盈可达性、成交量语义和策略规则版本证据并导出二审包 | `codex-expert-kit/rag/scripts/supplement_phase37_kline_strategy_needs_evidence.py`、`docs/research/phase37_kline_strategy_supplemental_research.md`、`docs/audit/phase37_kline_strategy_supplemental_reaudit_package_20260611.json`、`docs/reports/phase37_kline_strategy_supplemental_reaudit_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-396 |
| CEK-TA-398 | P1 | done | 导入 Kline / Strategy Engineering 补证二审结果，将 4 条候选置为 accepted_for_draft 并保持 reviewed/approved/default/hard gate 阻断 | `codex-expert-kit/rag/scripts/apply_phase37_kline_strategy_supplemental_reaudit_result.py`、`docs/audit/audit_result_phase37_kline_strategy_supplemental_reaudit_20260611_strict_v1.json`、`docs/reports/phase37_kline_strategy_supplemental_reaudit_import_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-397 |
| CEK-TA-399 | P1 | done | 导出 Kline / Strategy Engineering 12 条 accepted_for_draft 候选 reviewed/caveat_only 准备审计包 | `codex-expert-kit/rag/scripts/export_phase37_kline_strategy_reviewed_preparation_package.py`、`docs/audit/phase37_kline_strategy_reviewed_preparation_audit_package_20260611.json`、`docs/reports/phase37_kline_strategy_reviewed_preparation_gap_report.json` | CEK-TA-398 |
| CEK-TA-400 | P1 | done | 导入 Kline / Strategy Engineering reviewed-preparation 审计结果，12 条沉淀为 formal reviewed/caveat_only 并重建索引 | `codex-expert-kit/rag/scripts/apply_phase37_kline_strategy_reviewed_preparation_result.py`、`docs/audit/audit_result_phase37_kline_strategy_reviewed_preparation_20260611_strict_v1.json`、`docs/reports/phase37_kline_strategy_reviewed_preparation_import_report.json`、`codex-expert-kit/rag/knowledge/KB_02_KLINE_STRATEGY/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-399 |
| CEK-TA-402 | P1 | done | 采集并生成 Trading Engineering Market Microstructure 12 条候选知识 | `codex-expert-kit/rag/scripts/generate_phase37_market_microstructure_candidates.py`、`codex-expert-kit/rag/candidates/KB_03_MARKET_MICROSTRUCTURE/`、`docs/research/phase37_market_microstructure_candidate_research.md`、`docs/reports/phase37_market_microstructure_candidate_generation_report.md`、`docs/reports/phase37_market_microstructure_candidate_quality_gate.json` | CEK-TA-400 |
| CEK-TA-403 | P1 | done | 导出 Market Microstructure 候选 AI 审计包 | `codex-expert-kit/rag/scripts/export_phase37_market_microstructure_candidate_audit_package.py`、`docs/audit/phase37_market_microstructure_candidate_audit_package_20260611.json`、`docs/reports/phase37_market_microstructure_candidate_audit_package_quality_gate.json` | CEK-TA-402 |
| CEK-TA-404 | P1 | done | 导入 Market Microstructure 首轮严格审计结果并分流 accepted/needs_more_evidence/rejected | `codex-expert-kit/rag/scripts/apply_phase37_market_microstructure_audit_result.py`、`docs/audit/audit_result_phase37_market_microstructure_candidate_audit_20260611_strict_v1.json`、`docs/reports/phase37_market_microstructure_audit_import_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-403 |
| CEK-TA-405 | P1 | done | 确认 Market Microstructure 无 needs_more_evidence 候选，补证流程无需执行 | `docs/reports/phase37_market_microstructure_no_supplement_needed_report.json` | CEK-TA-404 |
| CEK-TA-406 | P1 | done | 确认 Market Microstructure 无补证二审结果需要导入 | `docs/reports/phase37_market_microstructure_no_supplement_needed_report.json` | CEK-TA-405 |
| CEK-TA-407 | P1 | done | 导出 Market Microstructure accepted_for_draft 候选 reviewed/caveat_only 准备审计包 | `codex-expert-kit/rag/scripts/export_phase37_market_microstructure_reviewed_preparation_package.py`、`docs/audit/phase37_market_microstructure_reviewed_preparation_audit_package_20260611.json`、`docs/reports/phase37_market_microstructure_reviewed_preparation_gap_report.json` | CEK-TA-406 |
| CEK-TA-408 | P1 | done | 导入 Market Microstructure reviewed-preparation 审计结果并沉淀 11 条 formal reviewed/caveat_only，M07 回到补证队列 | `codex-expert-kit/rag/scripts/apply_phase37_market_microstructure_reviewed_preparation_result.py`、`docs/audit/audit_result_phase37_market_microstructure_reviewed_preparation_20260611_strict_v1.json`、`docs/reports/phase37_market_microstructure_reviewed_preparation_import_report.json`、`codex-expert-kit/rag/knowledge/KB_03_MARKET_MICROSTRUCTURE/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-407 |
| CEK-TA-410 | P1 | done | 为 P37-D-M07 补充交易日历、session、auction/halt、holiday、rollover/expiry 或 vendor market status 证据并导出再审包 | `codex-expert-kit/rag/scripts/supplement_phase37_market_microstructure_m07_liquidity_regime.py`、`docs/research/phase37_market_microstructure_m07_liquidity_regime_supplemental_research.md`、`docs/audit/phase37_market_microstructure_m07_liquidity_regime_reaudit_package_20260611.json`、`docs/reports/phase37_market_microstructure_m07_liquidity_regime_supplemental_report.json` | CEK-TA-408 |
| CEK-TA-411 | P1 | done | 导入 P37-D-M07 补证再审结果，沉淀 formal reviewed/caveat_only 并重建索引 | `codex-expert-kit/rag/scripts/apply_phase37_market_microstructure_m07_liquidity_regime_reaudit_result.py`、`docs/audit/audit_result_phase37_market_microstructure_m07_liquidity_regime_reaudit_20260611_strict_v1.json`、`docs/reports/phase37_market_microstructure_m07_liquidity_regime_reaudit_import_report.json`、`codex-expert-kit/rag/knowledge/KB_03_MARKET_MICROSTRUCTURE/kb_03_market_microstructure.liquidity_regime_required.v1.json`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-410 |
| CEK-TA-409 | P1 | done | 验证 Market Microstructure 在 MCP/SearchLab/KnowledgeTree/Vue3 的联动命中、引用和阻断 | `codex-expert-kit/rag/scripts/validate_phase37_runtime_linkage.py`、`docs/reports/phase37_runtime_linkage_validation_report.json` | CEK-TA-411 |
| CEK-TA-412 | P1 | done | 采集并生成 Trading Engineering Backtest 12 条候选知识 | `codex-expert-kit/rag/scripts/generate_phase37_backtest_candidates.py`、`codex-expert-kit/rag/candidates/KB_04_BACKTEST/`、`docs/research/phase37_backtest_candidate_research.md`、`docs/reports/phase37_backtest_candidate_generation_report.md`、`docs/reports/phase37_backtest_candidate_quality_gate.json` | CEK-TA-409 |
| CEK-TA-413 | P1 | done | 导出 Backtest 候选 AI 审计包 | `codex-expert-kit/rag/scripts/export_phase37_backtest_candidate_audit_package.py`、`docs/audit/phase37_backtest_candidate_audit_package_20260611.json`、`docs/reports/phase37_backtest_candidate_audit_package_quality_gate.json` | CEK-TA-412 |
| CEK-TA-414 | P1 | done | 导入 Backtest 首轮严格审计结果并分流 accepted/needs_more_evidence/rejected | `codex-expert-kit/rag/scripts/apply_phase37_backtest_audit_result.py`、`docs/audit/audit_result_phase37_backtest_candidate_audit_20260611_strict_v1.json`、`docs/reports/phase37_backtest_audit_import_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-413 |
| CEK-TA-415 | P1 | done | 确认 Backtest 无 needs_more_evidence 候选，补证流程无需执行 | `docs/reports/phase37_backtest_no_supplement_needed_report.json` | CEK-TA-414 |
| CEK-TA-416 | P1 | done | 确认 Backtest 无补证二审结果需要导入 | `docs/reports/phase37_backtest_no_supplement_needed_report.json` | CEK-TA-415 |
| CEK-TA-417 | P1 | done | 导出 Backtest accepted_for_draft 候选 reviewed/caveat_only 准备审计包 | `codex-expert-kit/rag/scripts/export_phase37_backtest_reviewed_preparation_package.py`、`docs/audit/phase37_backtest_reviewed_preparation_audit_package_20260611.json`、`docs/reports/phase37_backtest_reviewed_preparation_gap_report.json` | CEK-TA-416 |
| CEK-TA-418 | P1 | done | 导入 Backtest reviewed-preparation 审计结果，9 条沉淀 formal reviewed/caveat_only，B10/B11/B12 回到补证队列 | `codex-expert-kit/rag/scripts/apply_phase37_backtest_reviewed_preparation_result.py`、`docs/audit/audit_result_phase37_backtest_reviewed_preparation_20260611_strict_v1.json`、`docs/reports/phase37_backtest_reviewed_preparation_import_report.json`、`codex-expert-kit/rag/knowledge/KB_04_BACKTEST/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-417 |
| CEK-TA-420 | P1 | done | 为 Backtest B10/B11/B12 补充 profit factor/drawdown 专业来源与 CEK-TA backtest_run_manifest/versioning schema，并导出再审包 | `codex-expert-kit/rag/scripts/supplement_phase37_backtest_reviewed_blocked_candidates.py`、`docs/contracts/phase37_backtest_run_manifest_contract.md`、`docs/research/phase37_backtest_reviewed_blocked_supplemental_research.md`、`docs/audit/phase37_backtest_reviewed_blocked_supplemental_reaudit_package_20260611.json`、`docs/reports/phase37_backtest_reviewed_blocked_supplemental_report.json` | CEK-TA-418 |
| CEK-TA-421 | P1 | done | 导入 Backtest B10/B11/B12 补证再审结果，B10 沉淀 formal reviewed/caveat_only，B11/B12 继续补证 | `codex-expert-kit/rag/scripts/create_phase37_backtest_blocked_supplemental_reaudit_result_from_report.py`、`codex-expert-kit/rag/scripts/apply_phase37_backtest_reviewed_blocked_supplemental_result.py`、`docs/audit/audit_result_phase37_backtest_reviewed_blocked_supplemental_reaudit_20260611_strict_v1.json`、`docs/reports/phase37_backtest_reviewed_blocked_supplemental_import_report.json`、`codex-expert-kit/rag/knowledge/KB_04_BACKTEST/kb_04_backtest.profit_factor_drawdown_context_required.v1.json`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-420 |
| CEK-TA-422 | P1 | done | 为 Backtest B11/B12 内联完整 backtest_run_manifest contract/schema extract/字段表/schema hash，并导出下一轮再审包 | `codex-expert-kit/rag/scripts/supplement_phase37_backtest_b11_b12_inline_contract.py`、`docs/contracts/phase37_backtest_run_manifest_schema_extract.json`、`docs/research/phase37_backtest_b11_b12_inline_contract_research.md`、`docs/audit/phase37_backtest_b11_b12_inline_contract_reaudit_package_20260611.json`、`docs/reports/phase37_backtest_b11_b12_inline_contract_report.json`、`ui/src/components/StatusBadge.vue`、`ui/src/types.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-421 |
| CEK-TA-423 | P1 | done | 导入 Backtest B11/B12 内联契约再审结果并沉淀剩余 formal reviewed/caveat_only | `codex-expert-kit/rag/scripts/create_phase37_backtest_b11_b12_inline_contract_reaudit_result_from_report.py`、`codex-expert-kit/rag/scripts/apply_phase37_backtest_b11_b12_inline_contract_result.py`、`docs/audit/audit_result_phase37_backtest_b11_b12_inline_contract_reaudit_20260611_strict_v1.json`、`docs/reports/phase37_backtest_b11_b12_inline_contract_import_report.json`、`codex-expert-kit/rag/knowledge/KB_04_BACKTEST/kb_04_backtest.reproducibility_package_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_04_BACKTEST/kb_04_backtest.strategy_version_and_data_version_required.v1.json`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-422 |
| CEK-TA-419 | P1 | done | 验证 Backtest 在 MCP/SearchLab/KnowledgeTree/Vue3 的联动命中、引用和阻断 | `codex-expert-kit/rag/scripts/validate_phase37_runtime_linkage.py`、`docs/reports/phase37_runtime_linkage_validation_report.json` | CEK-TA-423 |
| CEK-TA-424 | P1 | done | 采集并生成 Trading Engineering Replay / Simulation 12 条候选知识 | `codex-expert-kit/rag/scripts/generate_phase37_replay_simulation_candidates.py`、`codex-expert-kit/rag/candidates/KB_05_REPLAY_SIMULATION/`、`docs/research/phase37_replay_simulation_candidate_research.md`、`docs/reports/phase37_replay_simulation_candidate_generation_report.md`、`docs/reports/phase37_replay_simulation_candidate_quality_gate.json` | CEK-TA-419 |
| CEK-TA-425 | P1 | done | 导出 Replay / Simulation 候选 AI 审计包 | `codex-expert-kit/rag/scripts/export_phase37_replay_simulation_candidate_audit_package.py`、`docs/audit/phase37_replay_simulation_candidate_audit_package_20260611.json`、`docs/reports/phase37_replay_simulation_candidate_audit_package_quality_gate.json` | CEK-TA-424 |
| CEK-TA-426 | P1 | done | 导入 Replay / Simulation 首轮严格审计结果并分流 accepted/needs_more_evidence/rejected | `codex-expert-kit/rag/scripts/apply_phase37_replay_simulation_audit_result.py`、`docs/audit/audit_result_phase37_replay_simulation_candidate_audit_20260611_strict_v1.json`、`docs/reports/phase37_replay_simulation_audit_import_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-425 |
| CEK-TA-427 | P1 | done | 确认 Replay / Simulation 无 needs_more_evidence 候选，补证流程无需执行 | `docs/reports/phase37_replay_simulation_no_supplement_needed_report.json` | CEK-TA-426 |
| CEK-TA-428 | P1 | done | 确认 Replay / Simulation 无补证二审结果需要导入 | `docs/reports/phase37_replay_simulation_no_supplement_needed_report.json` | CEK-TA-427 |
| CEK-TA-429 | P1 | done | 导出 Replay / Simulation accepted_for_draft 候选 reviewed/caveat_only 准备审计包 | `codex-expert-kit/rag/scripts/export_phase37_replay_simulation_reviewed_preparation_package.py`、`docs/audit/phase37_replay_simulation_reviewed_preparation_audit_package_20260612.json`、`docs/reports/phase37_replay_simulation_reviewed_preparation_gap_report.json` | CEK-TA-428 |
| CEK-TA-430 | P1 | done | 导入 Replay / Simulation reviewed-preparation 审计结果，9 条沉淀 formal reviewed/caveat_only，R02/R10/R12 回到补证队列 | `codex-expert-kit/rag/scripts/apply_phase37_replay_simulation_reviewed_preparation_result.py`、`docs/audit/audit_result_phase37_replay_simulation_reviewed_preparation_20260612_strict_v1.json`、`docs/reports/phase37_replay_simulation_reviewed_preparation_import_report.json`、`codex-expert-kit/rag/knowledge/KB_05_REPLAY_SIMULATION/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-429 |
| CEK-TA-432 | P1 | done | 为 Replay / Simulation R02/R10/R12 补充 same_bar_fill_ordering、simulation_live_gap_report、execution_cost_mapping 内部契约/schema 并导出再审包 | `docs/contracts/phase37_replay_simulation_execution_assumption_contract.md`、`docs/research/phase37_replay_simulation_blocked_supplemental_research.md`、`docs/audit/phase37_replay_simulation_blocked_supplemental_reaudit_package_20260612.json`、`docs/reports/phase37_replay_simulation_blocked_supplemental_report.json` | CEK-TA-430 |
| CEK-TA-433 | P1 | done | 导入 Replay / Simulation R02/R10/R12 补证再审结果并沉淀剩余 formal reviewed/caveat_only | `codex-expert-kit/rag/scripts/apply_phase37_replay_simulation_blocked_supplemental_result.py`、`docs/audit/audit_result_phase37_replay_simulation_blocked_supplemental_reaudit_20260612_strict_v1.json`、`docs/reports/phase37_replay_simulation_blocked_supplemental_import_report.json`、`codex-expert-kit/rag/knowledge/KB_05_REPLAY_SIMULATION/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-432 |
| CEK-TA-431 | P1 | done | 验证 Replay / Simulation 在 MCP/SearchLab/KnowledgeTree/Vue3 的联动命中、引用和阻断 | `codex-expert-kit/rag/scripts/validate_phase37_runtime_linkage.py`、`docs/reports/phase37_runtime_linkage_validation_report.json` | CEK-TA-433 |
| CEK-TA-434 | P1 | done | 对齐 Live Execution / Risk Management 知识树节点、分区和候选归类契约 | `codex-expert-kit/rag/knowledge_tree.md`、`ui/src/data/knowledgeTreeNodes.ts`、`docs/reports/phase37_live_risk_tree_mapping_report.json` | CEK-TA-431 |
| CEK-TA-435 | P1 | done | 采集并生成 Trading Engineering Live Execution / Risk Management 12 条候选知识 | `codex-expert-kit/rag/scripts/generate_phase37_live_risk_candidates.py`、`codex-expert-kit/rag/candidates/KB_06_LIVE_EXECUTION/`、`codex-expert-kit/rag/candidates/KB_07_RISK_MANAGEMENT/`、`docs/research/phase37_live_risk_candidate_research.md`、`docs/reports/phase37_live_risk_candidate_generation_report.md`、`docs/reports/phase37_live_risk_candidate_quality_gate.json` | CEK-TA-434 |
| CEK-TA-436 | P1 | done | 导出 Live Execution / Risk Management 候选 AI 审计包并运行候选质量门禁 | `codex-expert-kit/rag/scripts/export_phase37_live_risk_candidate_audit_package.py`、`docs/audit/phase37_live_risk_candidate_audit_package_20260612.json`、`docs/reports/phase37_live_risk_candidate_audit_package_quality_gate.json` | CEK-TA-435 |
| CEK-TA-437 | P1 | done | 导入 Live Execution / Risk Management 首轮严格审计结果，12 条回写为 accepted_for_draft 并保持 reviewed/approved/default/hard gate 阻断 | `codex-expert-kit/rag/scripts/apply_phase37_live_risk_audit_result.py`、`docs/audit/audit_result_phase37_live_risk_candidate_audit_20260612_strict_v1.json`、`docs/reports/phase37_live_risk_audit_import_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-436 |
| CEK-TA-438 | P1 | done | 导出 Live Execution / Risk Management reviewed/caveat_only 准备审计包，阻止 accepted_for_draft 直接入 formal reviewed | `codex-expert-kit/rag/scripts/export_phase37_live_risk_reviewed_preparation_package.py`、`docs/audit/phase37_live_risk_reviewed_preparation_audit_package_20260612.json`、`docs/reports/phase37_live_risk_reviewed_preparation_gap_report.json` | CEK-TA-437 |
| CEK-TA-439 | P1 | done | 导入 Live Execution / Risk Management reviewed-preparation 审计结果，9 条沉淀 formal reviewed/caveat_only，L03/L10/L11 回到补证队列 | `codex-expert-kit/rag/scripts/apply_phase37_live_risk_reviewed_preparation_result.py`、`docs/audit/audit_result_phase37_live_risk_reviewed_preparation_20260612_strict_v1.json`、`docs/reports/phase37_live_risk_reviewed_preparation_import_report.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/`、`codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-438 |
| CEK-TA-440 | P1 | done | 为 Live/Risk L03/L10/L11 补充 position_reconciliation、portfolio_exposure_limit、consecutive_loss_stop_policy 内部契约/schema 并导出再审包 | `docs/contracts/phase37_live_risk_reconciliation_exposure_loss_policy_contract.md`、`docs/research/phase37_live_risk_blocked_supplemental_research.md`、`docs/audit/phase37_live_risk_blocked_supplemental_reaudit_package_20260612.json`、`docs/reports/phase37_live_risk_blocked_supplemental_report.json` | CEK-TA-439 |
| CEK-TA-441 | P1 | done | 导入 Live/Risk L03/L10/L11 补证再审结果并沉淀剩余 formal reviewed/caveat_only | `codex-expert-kit/rag/scripts/apply_phase37_live_risk_blocked_supplemental_result.py`、`docs/audit/audit_result_phase37_live_risk_blocked_supplemental_reaudit_20260612_strict_v1.json`、`docs/reports/phase37_live_risk_blocked_supplemental_import_report.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/`、`codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-440 |
| CEK-TA-442 | P1 | done | 采集并生成 Trading Engineering Trade Analysis 12 条候选知识 | `codex-expert-kit/rag/scripts/generate_phase37_trade_analysis_candidates.py`、`codex-expert-kit/rag/candidates/KB_07_TRADE_ANALYSIS/`、`docs/research/phase37_trade_analysis_candidate_research.md`、`docs/reports/phase37_trade_analysis_candidate_generation_report.md`、`docs/reports/phase37_trade_analysis_candidate_quality_gate.json` | CEK-TA-441 |
| CEK-TA-443 | P1 | done | 导出 Trade Analysis 候选 AI 审计包并运行候选质量门禁 | `codex-expert-kit/rag/scripts/export_phase37_trade_analysis_candidate_audit_package.py`、`docs/audit/phase37_trade_analysis_candidate_audit_package_20260612.json`、`docs/reports/phase37_trade_analysis_candidate_audit_package_quality_gate.json` | CEK-TA-442 |
| CEK-TA-444 | P1 | done | 导入 Trade Analysis 首轮严格审计结果，12 条回写为 accepted_for_draft 并保持 reviewed/approved/default/hard gate 阻断 | `codex-expert-kit/rag/scripts/apply_phase37_trade_analysis_audit_result.py`、`docs/audit/audit_result_phase37_trade_analysis_candidate_audit_20260612_strict_v1.json`、`docs/reports/phase37_trade_analysis_audit_import_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-443 |
| CEK-TA-445 | P1 | done | 导出 Trade Analysis accepted_for_draft 候选 reviewed/caveat_only 准备审计包，阻止 draft 直接入 formal reviewed | `codex-expert-kit/rag/scripts/export_phase37_trade_analysis_reviewed_preparation_package.py`、`docs/audit/phase37_trade_analysis_reviewed_preparation_audit_package_20260612.json`、`docs/reports/phase37_trade_analysis_reviewed_preparation_gap_report.json` | CEK-TA-444 |
| CEK-TA-446 | P1 | done | 导入 Trade Analysis reviewed-preparation 审计结果，12 条回写为 needs_more_evidence，阻止 formal reviewed | `codex-expert-kit/rag/scripts/apply_phase37_trade_analysis_reviewed_preparation_result.py`、`docs/audit/audit_result_phase37_trade_analysis_reviewed_preparation_20260612_strict_v1.json`、`docs/reports/phase37_trade_analysis_reviewed_preparation_import_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-445 |
| CEK-TA-447 | P1 | done | 为 Trade Analysis 12 条补充 trade_review、R 分解、MAE/MFE、taxonomy、quality review、reason code 和 hypothesis lifecycle 内部契约/schema 并导出再审包 | `docs/contracts/phase37_trade_analysis_review_contract.md`、`docs/research/phase37_trade_analysis_blocked_supplemental_research.md`、`docs/audit/phase37_trade_analysis_blocked_supplemental_reaudit_package_20260612.json`、`docs/reports/phase37_trade_analysis_blocked_supplemental_report.json` | CEK-TA-446 |
| CEK-TA-448 | P1 | done | 导入 Trade Analysis 补证再审结果并沉淀 12 条 formal reviewed/caveat_only | `codex-expert-kit/rag/scripts/apply_phase37_trade_analysis_blocked_supplemental_result.py`、`docs/audit/audit_result_phase37_trade_analysis_blocked_supplemental_reaudit_20260612_strict_v1.json`、`docs/reports/phase37_trade_analysis_blocked_supplemental_import_report.json`、`codex-expert-kit/rag/knowledge/KB_07_TRADE_ANALYSIS/` | CEK-TA-447 |
| CEK-TA-449 | P1 | done | 验证 Trade Analysis 在 knowledge_items、Vue3、MCP/SearchLab/KnowledgeTree 的联动命中和阻断 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/`、`docs/reports/phase37_trade_analysis_runtime_linkage_report.json`、`codex-expert-kit/rag/scripts/validate_phase37_trade_analysis_runtime_linkage.py` | CEK-TA-448 |
| CEK-TA-450 | P1 | done | Phase 37 全量 96 条 Trading Engineering formal reviewed/caveat_only 知识收口验收，修正队列状态并生成总报告 | `codex-expert-kit/rag/scripts/validate_phase37_full_runtime_linkage.py`、`docs/reports/phase37_full_runtime_linkage_report.json`、`docs/reports/phase37_trading_engineering_knowledge_expansion_report.md`、`docs/research/phase37_trading_engineering_research_task_queue.md` | CEK-TA-449 |
| CEK-TA-451 | P1 | done | 对 Phase 37 Trading Engineering P0 进行外部专业资料对照审计，识别 P1/P2 遗漏知识点 | `docs/reports/phase37_trading_engineering_post_completion_gap_audit_report.md` | CEK-TA-450 |

## 上游输入

```text
docs/tasks/phase36_ai_engineering_gating_scoring_knowledge.md
docs/audit/phase36_ai_engineering_knowledge_scope_for_audit.json
docs/research/phase36_ai_engineering_knowledge_framework.md
codex-expert-kit/rag/knowledge_tree.md
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/metadata_schema.md
docs/contracts/knowledge_item_schema_v1_1_contract.md
```

## 下游输出

```text
1. Trading Engineering 需要完善的知识点清单。
2. Trading Engineering 知识范围审计 JSON。
3. Trading 与 AI 的跨分支引用契约。
4. Trading Engineering ResearchIngestionTask 队列。
5. 后续候选知识、formal reviewed 知识、索引和 Vue3 知识树展示。
```

## 分支边界

Trading Engineering 包含交易专业规则本体：

```text
量化基础、EV、R/R、成本、仓位、交易决策流
市场数据工程、时间对齐、缺失重复、时区、数据版本
K 线结构、指标边界、多周期、入场、止损、止盈
市场微观结构、盘口、流动性、订单流
回测可信度、数据泄漏、过拟合、样本外、成本模型
回放、模拟盘、fill model、同根 K TP/SL、滑点、延迟
实盘执行、订单状态机、仓位同步、kill switch、事故恢复
风险管理、单笔风险、日亏损、组合暴露、风控闸门
交易复盘、坏例 taxonomy、R/R 分解、交易质量归因
```

Trading Engineering 不包含：

```text
LLM/SFT/DPO/PEFT 训练方法本体。
RAG/MCP tool contract 本体。
模型部署、LLMOps、AI governance 本体。
外部项目私有策略参数、账户事实、密钥、实盘配置。
```

AI Engineering 可以引用 Trading Engineering，但只能引用：

```text
knowledge_refs
retrieved_knowledge
reason_codes
TradeCandidate / LabelingRecord / EvalCase 中的交易上下文字段
训练、eval、runtime gate 所需的交易规则引用
```

## P0 知识点范围

第一批 Trading Engineering P0 暂定 96 条，分为 8 组。

### A. Quant Foundation / 量化基础 P0

```text
Q01. quant_foundation.expected_value_definition.v1
Q02. quant_foundation.r_multiple_definition.v1
Q03. quant_foundation.risk_reward_boundary.v1
Q04. quant_foundation.cost_adjusted_expectancy_required.v1
Q05. quant_foundation.win_rate_not_enough.v1
Q06. quant_foundation.position_sizing_requires_risk_unit.v1
Q07. quant_foundation.leverage_amplifies_drawdown.v1
Q08. quant_foundation.signal_decision_execution_separation.v1
Q09. quant_foundation.trade_frequency_vs_quality_boundary.v1
Q10. quant_foundation.edge_requires_out_of_sample_evidence.v1
Q11. quant_foundation.sample_size_and_regime_caveat.v1
Q12. quant_foundation.no_profit_claim_without_costs.v1
```

### B. Data Engineering / 市场数据工程 P0

```text
D01. data_engineering.timestamp_alignment_required.v1
D02. data_engineering.timezone_policy_required.v1
D03. data_engineering.missing_bar_detection_required.v1
D04. data_engineering.duplicate_event_detection_required.v1
D05. data_engineering.ohlcv_schema_required.v1
D06. data_engineering.feature_timestamp_required.v1
D07. data_engineering.data_versioning_required.v1
D08. data_engineering.symbol_contract_normalization_required.v1
D09. data_engineering.corporate_action_or_contract_rollover_policy.v1
D10. data_engineering.outlier_detection_required.v1
D11. data_engineering.raw_vs_adjusted_data_boundary.v1
D12. data_engineering.data_quality_report_required.v1
```

### C. Kline / Strategy Engineering / K 线与策略工程 P0

```text
K01. kline_strategy.trend_structure_boundary.v1
K02. kline_strategy.market_structure_requires_timeframe.v1
K03. kline_strategy.entry_signal_not_equal_trade_decision.v1
K04. kline_strategy.stop_loss_requires_invalidation_logic.v1
K05. kline_strategy.take_profit_requires_reachability_check.v1
K06. kline_strategy.multi_timeframe_context_required.v1
K07. kline_strategy.indicator_lag_boundary.v1
K08. kline_strategy.atr_volatility_context_required.v1
K09. kline_strategy.rsi_threshold_not_universal.v1
K10. kline_strategy.volume_confirmation_boundary.v1
K11. kline_strategy.signal_generalization_forbidden_without_market_scope.v1
K12. kline_strategy.strategy_rule_version_required.v1
```

### D. Market Microstructure / 市场微观结构 P0

```text
M01. microstructure.spread_liquidity_context_required.v1
M02. microstructure.order_book_depth_boundary.v1
M03. microstructure.trade_prints_aggressor_caveat.v1
M04. microstructure.order_flow_proxy_boundary.v1
M05. microstructure.cvd_interpretation_caveat.v1
M06. microstructure.funding_open_interest_context_required.v1
M07. microstructure.liquidity_regime_required.v1
M08. microstructure.market_impact_cost_required.v1
M09. microstructure.high_frequency_signal_latency_boundary.v1
M10. microstructure.slippage_regime_caveat.v1
M11. microstructure.thin_market_execution_risk.v1
M12. microstructure.microstructure_feature_not_universal.v1
```

### E. Backtest / 回测可信度 P0

```text
B01. backtest.lookahead_bias_block.v1
B02. backtest.data_leakage_block.v1
B03. backtest.survivorship_selection_bias_check.v1
B04. backtest.parameter_search_separate_from_final_eval.v1
B05. backtest.walk_forward_validation_required.v1
B06. backtest.out_of_sample_required.v1
B07. backtest.cost_model_required.v1
B08. backtest.slippage_fee_spread_required.v1
B09. backtest.metric_interpretation_boundary.v1
B10. backtest.profit_factor_drawdown_context_required.v1
B11. backtest.reproducibility_package_required.v1
B12. backtest.strategy_version_and_data_version_required.v1
```

### F. Replay / Simulation / 回放与模拟 P0

```text
R01. replay.event_clock_required.v1
R02. replay.ohlc_same_bar_tp_sl_ordering_required.v1
R03. replay.fill_model_assumption_required.v1
R04. replay.partial_fill_policy_required.v1
R05. replay.latency_model_required.v1
R06. replay.paper_trading_not_equal_live.v1
R07. replay.exchange_rule_simulation_required.v1
R08. replay.minimum_order_size_required.v1
R09. replay.order_reject_and_cancel_policy_required.v1
R10. replay.simulation_live_gap_report_required.v1
R11. replay.tick_replay_vs_ohlc_boundary.v1
R12. replay.execution_cost_consistency_required.v1
```

### G. Live Execution / Risk Management / 实盘执行与风控 P0

```text
L01. live_execution.least_privilege_api_required.v1
L02. live_execution.order_state_machine_required.v1
L03. live_execution.position_reconciliation_required.v1
L04. live_execution.kill_switch_required.v1
L05. live_execution.exchange_adapter_error_contract_required.v1
L06. live_execution.order_fill_trade_log_required.v1
L07. risk_management.single_trade_risk_limit_required.v1
L08. risk_management.daily_loss_limit_required.v1
L09. risk_management.max_open_positions_required.v1
L10. risk_management.portfolio_exposure_limit_required.v1
L11. risk_management.consecutive_loss_stop_required.v1
L12. risk_management.hard_risk_gate_precedes_execution.v1
```

### H. Trade Analysis / 交易复盘 P0

```text
T01. trade_analysis.planned_vs_realized_r_required.v1
T02. trade_analysis.mae_mfe_for_post_trade_only.v1
T03. trade_analysis.bad_trade_taxonomy_required.v1
T04. trade_analysis.good_loss_bad_win_distinction.v1
T05. trade_analysis.entry_quality_review_required.v1
T06. trade_analysis.exit_quality_review_required.v1
T07. trade_analysis.risk_quality_review_required.v1
T08. trade_analysis.execution_quality_review_required.v1
T09. trade_analysis.rule_compliance_review_required.v1
T10. trade_analysis.regime_fit_review_required.v1
T11. trade_analysis.reason_code_required.v1
T12. trade_analysis.research_hypothesis_requires_validation.v1
```

## 契约

每个 Trading Engineering 知识项必须包含：

```text
primary_branch
primary_partition
canonical_node_id
claim_type
applicability
not_applicable_when
assumptions
source_evidence
source_quality
conflict_audit
llm_usage_policy
machine_gate
related_ai_engineering_nodes
```

跨分支引用契约：

```text
Trading Engineering 是交易规则本体的 primary owner。
AI Engineering 只能通过 knowledge_refs 引用 Trading Engineering。
如果 AI Engineering 需要某条交易规则，必须引用 canonical_node_id，不得复制改写规则本体。
如果交易规则被修订，AI Engineering 的相关 eval/rubric/gate 必须重新验证。
```

## Definition of Done

```text
1. Phase 37 任务卡存在并被 docs/index_tasks.md、docs/tasks/README.md 索引。
2. Trading Engineering P0 范围文档存在。
3. Trading Engineering 审计 JSON 存在并可被 JSON parser 读取。
4. Trading 与 AI 的跨分支边界写清楚。
5. 96 条 P0 知识点都有分组、命名和目标分支。
6. 不把 AI 训练、RAG、MCP、LLMOps 知识误放入 Trading Engineering。
7. 不把项目私有策略参数、账户事实、密钥或实盘配置写入通用知识。
8. 中文文档 UTF-8 无乱码。
```

## 测试与验收

```text
文档存在性检查
JSON 格式检查
P0 条目计数检查
索引一致性检查
UTF-8 乱码检查
```

## 风险与回滚

| 风险 | 处理 |
| --- | --- |
| Trading 与 AI 分支重复收录同一规则 | Trading 保存规则本体，AI 只保存引用和治理规则 |
| K 线/策略知识被误写成投资建议 | 必须声明适用边界、非建议属性和验证要求 |
| 项目私有策略污染通用知识 | 只允许脱敏后的通用规则进入候选 |
| 理论冲突未消解 | 标记 conflict_status，不允许默认指导 |

回滚方式：

```text
1. 若范围过宽，调整 Phase 37 范围文档和审计 JSON，不删除已有正式知识。
2. 若发现错误分支，更新 primary_branch / related_nodes，不直接复制知识。
3. 若候选知识污染，标记 rejected 或 needs_more_evidence。
```

## 状态更新要求

完成任一任务后必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase37_trading_engineering_knowledge_expansion.md
相关 contracts/research/audit/reports 文档
```
