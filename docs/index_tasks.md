# CEK-TA 项目管理规范与任务索引

本文是本项目的任务管理总入口，用于把《需求框架.md》《任务需求清单.md》《知识库采集与审计规范.md》《Vue3知识审计界面需求.md》拆成可执行 Phase，并统一任务状态、交付路径、验收规则和推进顺序。

## 项目定位

```text
项目名称：Codex Expert Kit for Trading & AI
简称：CEK-TA
项目性质：支持层项目
核心目标：为其他交易、回测、模拟盘、实盘、LLM、RAG 项目提供专业知识库和专家能力复用层
```

本项目不直接承载某个交易策略的项目事实，而是沉淀可复用的专业知识、审计规则、Skill 工作流、RAG/MCP 检索能力和 Vue3 知识审计界面。

## 管理原则

```text
1. 先契约，后实现。
2. 先 P0，后 P1/P2。
3. 每个任务必须有交付物路径。
4. 每个知识条目必须有来源和适用边界。
5. 理论冲突必须被标注、消解或阻断。
6. Vue3 界面只做审计工作台，不做营销页。
7. 任何实现任务完成后都必须更新本索引状态。
```

## 状态定义

```text
todo: 未开始
doing: 正在进行
blocked: 被阻塞，需要外部输入或前置任务
review: 已完成实现，等待审计
done: 已验收
deprecated: 已废弃
```

## 优先级定义

```text
P0: 必须先完成，否则后续无法稳定展开
P1: 第一版能力包需要具备
P2: 第一版跑通后增强
```

## Phase 总览

| Phase | 名称 | 目标 | 状态 |
| --- | --- | --- | --- |
| Phase 0 | 项目管理与规范入口 | 建立任务索引、管理规范、状态流 | done |
| Phase 1 | Codex Expert Kit 骨架 | 让任何项目都能继承交易工程规则 | done |
| Phase 2 | RAGFlow 知识库接入 | 让 Codex 可以查专业知识 | done |
| Phase 2.5 | 知识采集与冲突审计 | 保证知识有来源、有分类、无未消解冲突 | done |
| Phase 3 | Knowledge MCP | 让 Codex 跨项目通过 MCP 查知识 | done |
| Phase 4 | 统一交易接口 | 统一回测、回放、模拟盘、实盘策略语义 | done |
| Phase 5 | 交易分析闭环 | 每笔交易都能变成策略优化样本 | done |
| Phase 6 | LLM 训练闭环 | 把审计与分析能力训练成稳定模型能力 | done |
| Phase 7 | Vue3 知识审计界面 | 提供可视化知识审计工作台 | done |
| Phase 8 | 其他项目接入 | 定义其他项目如何调用 CEK-TA | done |
| Phase 9 | 知识倒灌与反哺 | 定义其他项目如何向 CEK-TA 贡献知识 | done |
| Phase 10 | 外部项目运行时接入增强 | 让其他项目稳定调用、健康检查和回灌 CEK-TA | done |
| Phase 11 | 知识树体系 | 让知识库按专业知识树组织、浏览和审计 | done |
| Phase 12 | 专业知识采集流水线 | 让 Codex 联网搜索、分析、归类并生成候选知识 | done |
| Phase 13 | RAG 数据层与检索质量 | 让知识可索引、可检索、可追踪和可测试 | done |
| Phase 14 | Knowledge MCP 运行时服务 | 把 MCP 草案升级为可运行服务 | done |
| Phase 15 | Vue3 审计工作台升级 | 增加知识树、候选审计、检索测试和接入审计 | done |
| Phase 16 | 知识质量与评测体系 | 用指标和评测集持续优化知识库质量 | done |
| Phase 17 | 首批真实知识资产沉淀 | 沉淀第一批可复用、可审计、可检索专业知识 | done |
| Phase 18 | 知识树 v2 治理升级 | 让知识树支持 canonical path、alias 兼容、状态治理和安全检索路由 | done |
| Phase 19 | Seed 知识运行时验证 | 验证首批知识能被 MCP/SearchLab 命中、返回来源并阻断不安全默认指导 | done |
| Phase 20 | SearchLab MCP 真实运行时与检索质量闭环 | 把 SearchLab 接到 MCP 同构运行时，并补齐 canonical 过滤、排名质量和阻断审计 | done |
| Phase 21 | MCP 正式知识聚合索引 | 生成正式 knowledge_items.json，让其他项目 MCP 默认查询正式知识库 | done |
| Phase 22 | Path Resolver 移植复用地基 | 用 resolver 统一路径解析，避免硬编码绝对路径影响项目移植复用 | done |
| Phase 23 | 13 分区全网专业知识采集 | 围绕 13 个 KB 分区建立全网专业知识采集矩阵、来源种子库和候选任务队列 | done |
| Phase 24 | Vue3 候选知识审计工作台 v2 | 让前端承接候选知识查看、来源审计、冲突审计、转换预览和 CEK-TA-102 交接 | done |
| Phase 25 | Vue3 审计界面实机验收 | 用 Playwright 跑桌面/移动端截图、无空白/溢出检查和知识树过滤跳转验收 | done |
| Phase 26 | 知识树 3 级目录 UI | 让用户按“主枝 -> 分区 -> 专题”浏览知识树，并联动节点知识、候选、缺口和审计状态 | done |
| Phase 27 | 知识树阅读体验优化 | 先产出阅读型 HTML 原型，再把知识树页面升级为左树、中阅读、右审计的文档站式体验 | done |
| Phase 28 | 知识树阅读 UI Vue3 与 FastAPI 落地 | 对齐 HTML 原型、目标截图和文档，把知识树阅读体验落到 Vue3 页面与 FastAPI 只读契约 | done |
| Phase 29 | 候选知识人工审核阅读体验优化 | 把候选页升级为更适合人工阅读、风险判断、来源核查和 CEK-TA-102 交接的审核工作台 | done |
| Phase 30 | 候选知识 AI 审计包导出 | 一键导出带审计说明、检查项、输出 schema 和候选数据的 JSON 审计包 | done |
| Phase 31 | 候选知识 AI 审计结果回写 | 将外部 AI 审计结果回写到候选和正式 draft，修正补丁点并标记 reviewed | done |
| Phase 32 | 候选到 reviewed 知识的批量审计工作流 | 建立候选分组、AI 审计回写、正式 reviewed 知识回链和批量质量门禁 | done |
| Phase 33 | 知识库污染清理与门禁 | 清理 mock/test/internal-only 污染知识并增加正式知识污染门禁 | done |
| Phase 34 | 知识卡片 Schema v1.1 与默认指导门禁升级 | 补强知识卡片字段、机器门控、LLM 使用策略，并对齐 MCP/FastAPI/Vue3 | done |
| Phase 35 | 外部项目 AI 主动检索协议 | 定义外部项目 AI 什么时候必须搜、怎么搜、怎么引用、没搜到怎么办 | done |
| Phase 36 | AI Engineering 交易 LLM Gating/Scoring 知识扩展 | 为外接 LLM 训练项目扩展 AI Engineering 知识树、采集队列、契约和运行时验证 | done |
| Phase 37 | Trading Engineering 专业知识库扩展 | 固化 Trading 分支需要完善的交易专业知识点、跨分支边界和采集审计范围 | done |
| Phase 38 | AI 模型平台与交易 Gating/Scoring POC 知识扩展 | 拆分 AI 数值打分、校准、LLM 审计助手、shadow/paper/OPE 和发布治理知识子板块 | done |
| Phase 39 | 知识树单一数据源与统计对齐 | 统一 MCP/FastAPI/Vue3 知识树节点源和正式知识、候选知识统计口径 | done |
| Phase 40 | AI Continuous Learning 与再训练闭环 | 补齐 AI Engineering 持续反馈、标签刷新、漂移监控、周期再训练、再校准、灰度发布和回滚治理知识 | done |
| Phase 41 | Hybrid Scoring 与 Qwen3 审计助手知识扩展 | 补齐表格/统计 scorer、Qwen3 审计助手和 deterministic final gate 的组合落地知识 | done |
| Phase 42 | Database / Data Contract / Storage Engineering for Trading AI | 补齐交易 AI 数据库、数据契约、审计日志、向量库、迁移、备份恢复和数据生命周期治理知识 | done |
| Phase 43 | External Project AI Memory Layer | 为使用 CEK-TA 的外接 AI 项目定义项目记忆层、Memory Contract、MCP/API 契约、写入门禁、检索预算、安全治理和 adapter 选型知识 | done |
| Phase 44 | AI Trader Project Gap Audit | 使用当前正式知识库推演 AI 交易者项目理论方案，识别数据、交易、AI 训练、持续学习和实盘治理知识断层 | done |
| Phase 45 | Trading Engineering P1 专业知识补全 | 基于 Phase 37 完成后缺口审计，补齐 TCA、审计追踪、分层风控、系统韧性、压力测试、订单语义、数据授权和 crypto perpetual 特有风险知识 | done |
| Phase 46 | Trading Engineering 知识回归评测 | 将 Phase 37/45 Trading Engineering 知识变成 MCP/SearchLab/KnowledgeTree 可持续回归评测集 | done |
| Phase 47 | AI/Trading Engineering 双主线归类与运行时一致性审计 | 审计 AI Engineering 与 Trading Engineering 的 L1/L2/L3、知识点归类、Vue3 展示和 MCP Server 调用是否一致 | done |
| Phase 48 | 知识树 canonical alias 与 reviewed schema backfill 修复 | 先修 AI/Trading 知识树 canonical node / alias，再补历史 reviewed/caveat_only 显式权限字段 | done |
| Phase 49 | Vue3 前端白屏与 Dev Server 稳定性修复 | 修复大 fixture 重写导致 Vite 缓存空模块、刷新白屏的问题 | done |
| Phase 50 | Vue3 大 Fixture 拆包与懒加载 | 将候选、正式知识和知识树大 fixture 从首包拆出，改为可分页、可缓存、可按需加载的数据访问层 | done |
| Phase 51 | Vue3 KnowledgeTree 大分支性能优化 | 给知识树增加范围索引、分页摘要、详情懒加载、虚拟滚动和大分支性能验收 | done |
| Phase 52 | AI/Trading Engineering 权威资料缺口复审 | 对照全网权威资料、标准和案例，复审 AI 与 Trading 两条主线是否还有应补知识点 | done |
| Phase 53 | AI/Trading 安全、市场行为与运行治理知识扩展 | 补齐 AI Agent 安全、AI SBOM、市场行为监控、Market Access 和时间同步审计知识 | done |
| Phase 54 | 历史 reviewed schema 与候选回链全量回填 | 补齐历史 formal reviewed 知识 schema v1.1 治理字段和候选到正式知识回链字段 | done |
| Phase 55 | MCP/SearchLab/Vue3 全链路运行时验收与知识库基线 | 固化当前正式知识库统计基线，验证 MCP、SearchLab、Vue3、权限和治理语义全链路可用 | done |
| Phase 56 | 外部调用 README 与 MCP 接入文档清晰化 | 让外部项目从 README、快速手册、MCP spec 和配置模板中直接看懂如何调用 CEK-TA 知识库 | done |
| Phase 57 | DogSignal Gate 开源品牌 UI 方案与 HTML 原型 | 明确 DogSignal Gate 是整体项目品牌，产出开源审计工作台 UI 优化方案和 HTML 原型 | done |
| Phase 58 | 回测 / 回放 / 模拟盘 / 实盘等效链条知识补充 | 明确同一交易系统只有走真实或字段级等效策略链条时，回测、回放、模拟盘和实盘结果才可比较 | done |
| Phase 59 | Microstructure Feature Store 与 Hybrid Snapshot Contract | 定义 Kline Snapshot Store、Microstructure Store、Feature Store、Training Dataset Snapshot 和 canonical registry / audit ledger 的边界并创建候选知识 | done |
| Phase 60 | Sandbox / Replay / Paper Trading 环境治理知识扩展 | 定义沙盒、测试网、历史回放、实时模拟执行、模拟盘和 live canary 的环境边界、晋级证据和 gap report 契约 | done |

## Phase 任务卡

所有 Phase 的详细任务卡统一放在：

```text
docs/tasks/
```

任务卡目录：

[tasks/README.md](./tasks/README.md)

| Phase | 任务卡 | 状态 |
| --- | --- | --- |
| Phase 0 | [tasks/phase0_project_management.md](./tasks/phase0_project_management.md) | done |
| Phase 1 | [tasks/phase1_expert_kit_skeleton.md](./tasks/phase1_expert_kit_skeleton.md) | done |
| Phase 2 | [tasks/phase2_ragflow_knowledge_base.md](./tasks/phase2_ragflow_knowledge_base.md) | done |
| Phase 2.5 | [tasks/phase2_5_knowledge_audit.md](./tasks/phase2_5_knowledge_audit.md) | done |
| Phase 3 | [tasks/phase3_knowledge_mcp.md](./tasks/phase3_knowledge_mcp.md) | done |
| Phase 4 | [tasks/phase4_trading_interface.md](./tasks/phase4_trading_interface.md) | done |
| Phase 5 | [tasks/phase5_trade_analysis_loop.md](./tasks/phase5_trade_analysis_loop.md) | done |
| Phase 6 | [tasks/phase6_llm_training_loop.md](./tasks/phase6_llm_training_loop.md) | done |
| Phase 7 | [tasks/phase7_vue3_audit_ui.md](./tasks/phase7_vue3_audit_ui.md) | done |
| Phase 8 | [tasks/phase8_external_project_integration.md](./tasks/phase8_external_project_integration.md) | done |
| Phase 9 | [tasks/phase9_knowledge_contribution.md](./tasks/phase9_knowledge_contribution.md) | done |
| Phase 10 | [tasks/phase10_external_project_runtime_integration.md](./tasks/phase10_external_project_runtime_integration.md) | done |
| Phase 11 | [tasks/phase11_knowledge_tree.md](./tasks/phase11_knowledge_tree.md) | done |
| Phase 12 | [tasks/phase12_research_ingestion_pipeline.md](./tasks/phase12_research_ingestion_pipeline.md) | done |
| Phase 13 | [tasks/phase13_rag_data_layer.md](./tasks/phase13_rag_data_layer.md) | done |
| Phase 14 | [tasks/phase14_mcp_runtime_server.md](./tasks/phase14_mcp_runtime_server.md) | done |
| Phase 15 | [tasks/phase15_vue3_audit_workbench_upgrade.md](./tasks/phase15_vue3_audit_workbench_upgrade.md) | done |
| Phase 16 | [tasks/phase16_knowledge_quality_eval.md](./tasks/phase16_knowledge_quality_eval.md) | done |
| Phase 17 | [tasks/phase17_seed_knowledge_assets.md](./tasks/phase17_seed_knowledge_assets.md) | done |
| Phase 18 | [tasks/phase18_knowledge_tree_v2_governance.md](./tasks/phase18_knowledge_tree_v2_governance.md) | done |
| Phase 19 | [tasks/phase19_seed_runtime_validation.md](./tasks/phase19_seed_runtime_validation.md) | done |
| Phase 20 | [tasks/phase20_searchlab_mcp_runtime_quality.md](./tasks/phase20_searchlab_mcp_runtime_quality.md) | done |
| Phase 21 | [tasks/phase21_formal_mcp_knowledge_index.md](./tasks/phase21_formal_mcp_knowledge_index.md) | done |
| Phase 22 | [tasks/phase22_path_resolver_foundation.md](./tasks/phase22_path_resolver_foundation.md) | done |
| Phase 23 | [tasks/phase23_partition_wide_research_ingestion.md](./tasks/phase23_partition_wide_research_ingestion.md) | done |
| Phase 24 | [tasks/phase24_vue3_candidate_audit_workbench_v2.md](./tasks/phase24_vue3_candidate_audit_workbench_v2.md) | done |
| Phase 25 | [tasks/phase25_vue3_playwright_visual_acceptance.md](./tasks/phase25_vue3_playwright_visual_acceptance.md) | done |
| Phase 26 | [tasks/phase26_knowledge_tree_hierarchical_ui.md](./tasks/phase26_knowledge_tree_hierarchical_ui.md) | done |
| Phase 27 | [tasks/phase27_knowledge_tree_reading_ui.md](./tasks/phase27_knowledge_tree_reading_ui.md) | done |
| Phase 28 | [tasks/phase28_knowledge_tree_vue_fastapi_delivery.md](./tasks/phase28_knowledge_tree_vue_fastapi_delivery.md) | done |
| Phase 29 | [tasks/phase29_candidate_audit_readability_workbench.md](./tasks/phase29_candidate_audit_readability_workbench.md) | done |
| Phase 30 | [tasks/phase30_candidate_ai_audit_package_export.md](./tasks/phase30_candidate_ai_audit_package_export.md) | done |
| Phase 31 | [tasks/phase31_candidate_ai_audit_result_backwrite.md](./tasks/phase31_candidate_ai_audit_result_backwrite.md) | done |
| Phase 32 | [tasks/phase32_candidate_to_reviewed_workflow.md](./tasks/phase32_candidate_to_reviewed_workflow.md) | done |
| Phase 33 | [tasks/phase33_knowledge_pollution_cleanup.md](./tasks/phase33_knowledge_pollution_cleanup.md) | done |
| Phase 34 | [tasks/phase34_knowledge_item_schema_v1_1.md](./tasks/phase34_knowledge_item_schema_v1_1.md) | done |
| Phase 35 | [tasks/phase35_external_ai_active_retrieval_protocol.md](./tasks/phase35_external_ai_active_retrieval_protocol.md) | done |
| Phase 36 | [tasks/phase36_ai_engineering_gating_scoring_knowledge.md](./tasks/phase36_ai_engineering_gating_scoring_knowledge.md) | done |
| Phase 37 | [tasks/phase37_trading_engineering_knowledge_expansion.md](./tasks/phase37_trading_engineering_knowledge_expansion.md) | done |
| Phase 38 | [tasks/phase38_ai_model_platform_poc_knowledge.md](./tasks/phase38_ai_model_platform_poc_knowledge.md) | done |
| Phase 39 | [tasks/phase39_knowledge_tree_single_source_stats_alignment.md](./tasks/phase39_knowledge_tree_single_source_stats_alignment.md) | done |
| Phase 40 | [tasks/phase40_ai_continuous_learning_retraining_loop.md](./tasks/phase40_ai_continuous_learning_retraining_loop.md) | done |
| Phase 41 | [tasks/phase41_hybrid_scoring_qwen3_audit_stack.md](./tasks/phase41_hybrid_scoring_qwen3_audit_stack.md) | done |
| Phase 42 | [tasks/phase42_database_data_contract_storage_engineering.md](./tasks/phase42_database_data_contract_storage_engineering.md) | done |
| Phase 43 | [tasks/phase43_external_project_ai_memory_layer.md](./tasks/phase43_external_project_ai_memory_layer.md) | done |
| Phase 44 | [tasks/phase44_ai_trader_project_gap_audit.md](./tasks/phase44_ai_trader_project_gap_audit.md) | done |
| Phase 45 | [tasks/phase45_trading_engineering_p1_completion.md](./tasks/phase45_trading_engineering_p1_completion.md) | done |
| Phase 46 | [tasks/phase46_trading_engineering_regression_eval.md](./tasks/phase46_trading_engineering_regression_eval.md) | done |
| Phase 47 | [tasks/phase47_ai_trade_engineering_alignment_audit.md](./tasks/phase47_ai_trade_engineering_alignment_audit.md) | done |
| Phase 48 | [tasks/phase48_tree_alias_schema_backfill.md](./tasks/phase48_tree_alias_schema_backfill.md) | done |
| Phase 49 | [tasks/phase49_vue3_dev_server_stability.md](./tasks/phase49_vue3_dev_server_stability.md) | done |
| Phase 50 | [tasks/phase50_vue3_fixture_lazy_loading.md](./tasks/phase50_vue3_fixture_lazy_loading.md) | done |
| Phase 51 | [tasks/phase51_knowledge_tree_large_scope_performance.md](./tasks/phase51_knowledge_tree_large_scope_performance.md) | done |
| Phase 52 | [tasks/phase52_ai_trade_authoritative_gap_audit.md](./tasks/phase52_ai_trade_authoritative_gap_audit.md) | done |
| Phase 53 | [tasks/phase53_ai_trade_security_market_conduct_extension.md](./tasks/phase53_ai_trade_security_market_conduct_extension.md) | done |
| Phase 54 | [tasks/phase54_historical_reviewed_schema_workflow_backfill.md](./tasks/phase54_historical_reviewed_schema_workflow_backfill.md) | done |
| Phase 55 | [tasks/phase55_runtime_acceptance_baseline.md](./tasks/phase55_runtime_acceptance_baseline.md) | done |
| Phase 56 | [tasks/phase56_external_call_readme_mcp_docs.md](./tasks/phase56_external_call_readme_mcp_docs.md) | done |
| Phase 57 | [tasks/phase57_dogsignal_gate_open_source_ui_concept.md](./tasks/phase57_dogsignal_gate_open_source_ui_concept.md) | done |
| Phase 58 | [tasks/phase58_backtest_sim_live_equivalence_chain.md](./tasks/phase58_backtest_sim_live_equivalence_chain.md) | done |
| Phase 59 | [tasks/phase59_microstructure_feature_store_hybrid_snapshot.md](./tasks/phase59_microstructure_feature_store_hybrid_snapshot.md) | done |
| Phase 60 | [tasks/phase60_sandbox_replay_paper_environment_governance.md](./tasks/phase60_sandbox_replay_paper_environment_governance.md) | done |

## Phase 0: 项目管理与规范入口

目标：建立项目任务管理入口，确保后续所有 Phase 都能被追踪、验收和回溯。

| ID | 优先级 | 状态 | 任务 | 交付物 | 任务卡 | 验收标准 |
| --- | --- | --- | --- | --- | --- | --- |
| CEK-TA-000 | P0 | done | 创建项目管理任务索引 | `docs/index_tasks.md` | [tasks/phase0_project_management.md](./tasks/phase0_project_management.md) | 包含 Phase 拆分、任务状态、依赖、验收规则、DoD、测试 |
| CEK-TA-043 | P0 | done | 创建项目级开发规范与开发 Skill | `AGENTS.md`、`.agents/skills/cek-ta-development-workflow/SKILL.md` | [tasks/phase0_project_management.md](./tasks/phase0_project_management.md) | 开发规范覆盖 tasks_index、上下游、契约、边界、DoD、测试、重大决策提问；Skill 验证通过 |

## Phase 1: Codex Expert Kit 骨架

目标：让任何项目都能继承交易工程规则。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-001 | P0 | done | 创建 `codex-expert-kit/` 基础目录 | `codex-expert-kit/` | CEK-TA-000 |
| CEK-TA-002 | P0 | done | 编写全局 `AGENTS.md` | `codex-expert-kit/core/AGENTS.md` | CEK-TA-001 |
| CEK-TA-003 | P0 | done | 编写项目接入模板 | `codex-expert-kit/templates/project_AGENTS.md` | CEK-TA-001 |
| CEK-TA-004 | P1 | done | 创建首批领域包 | `codex-expert-kit/domains/quant_trading/` 等 | CEK-TA-001 |
| CEK-TA-005 | P1 | done | 创建首批 Skill | `codex-expert-kit/skills/*/SKILL.md` | CEK-TA-002 |

## Phase 2: RAGFlow 知识库接入

目标：让 Codex 可以查专业知识，不靠上下文硬塞。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-006 | P0 | done | 定义知识库分区 | `codex-expert-kit/rag/kb_partitions.md` | CEK-TA-001 |
| CEK-TA-007 | P0 | done | 定义 metadata schema | `codex-expert-kit/rag/metadata_schema.md` | CEK-TA-006 |
| CEK-TA-008 | P1 | done | 定义 chunking rules | `codex-expert-kit/rag/chunking_rules.md` | CEK-TA-007 |
| CEK-TA-009 | P1 | done | 定义 retrieval policy | `codex-expert-kit/rag/retrieval_policy.md` | CEK-TA-007 |

## Phase 2.5: 知识采集与冲突审计

目标：保证每条专业知识都有来源、有分类、有适用边界，并且理论规则不互相矛盾。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-022 | P0 | done | 建立知识采集与审计规范 | `知识库采集与审计规范.md` | CEK-TA-000 |
| CEK-TA-023 | P0 | done | 定义知识条目结构化 schema | `codex-expert-kit/rag/knowledge_item_schema.md` | CEK-TA-022 |
| CEK-TA-024 | P0 | done | 定义冲突检测规则 | `codex-expert-kit/rag/conflict_detection_rules.md` | CEK-TA-023 |
| CEK-TA-025 | P1 | done | 定义来源质量评分 | `codex-expert-kit/rag/source_quality_rules.md` | CEK-TA-022 |
| CEK-TA-026 | P1 | done | 定义 Codex 联网采集任务模板 | `codex-expert-kit/templates/research_task_card.md` | CEK-TA-022 |

## Phase 3: Knowledge MCP

目标：让 Codex 在任何项目里通过 MCP 查知识。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-010 | P0 | done | 编写 MCP server 规格 | `codex-expert-kit/mcp/mcp_server_spec.md` | CEK-TA-007 |
| CEK-TA-011 | P1 | done | 实现 `search_expert_knowledge` 草案 | `codex-expert-kit/mcp/search_expert_knowledge.py` | CEK-TA-010 |
| CEK-TA-012 | P1 | done | 实现 adapter/reason_code 查询草案 | `codex-expert-kit/mcp/get_*.py` | CEK-TA-010 |

## Phase 4: 统一交易接口

目标：让回测、回放、模拟盘、实盘使用同一套策略语义。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-013 | P0 | done | 定义核心数据契约 | `codex-expert-kit/templates/interface_contract.md` | CEK-TA-002 |
| CEK-TA-014 | P0 | done | 定义 ExecutionAdapter 契约 | `codex-expert-kit/templates/execution_adapter_spec.md` | CEK-TA-013 |
| CEK-TA-015 | P1 | done | 定义 FillModel 规则 | `codex-expert-kit/templates/fill_model_spec.md` | CEK-TA-014 |

## Phase 5: 交易分析闭环

目标：每笔交易都能变成策略优化样本。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-016 | P0 | done | 定义 trade result schema | `codex-expert-kit/templates/trade_result_schema.md` | CEK-TA-013 |
| CEK-TA-017 | P1 | done | 定义 bad case taxonomy | `codex-expert-kit/domains/trade_analysis/knowledge/bad_trade_taxonomy.md` | CEK-TA-016 |
| CEK-TA-018 | P1 | done | 创建 trade-quality-analyst Skill | `codex-expert-kit/skills/trade-quality-analyst/SKILL.md` | CEK-TA-017 |

## Phase 6: LLM 训练闭环

目标：把策略审计、交易分析、任务卡写法训练成稳定能力。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-019 | P1 | done | 创建 LLM training domain | `codex-expert-kit/domains/llm_training/` | CEK-TA-001 |
| CEK-TA-020 | P1 | done | 创建数据集与评测模板 | `codex-expert-kit/templates/dataset_card.md`、`eval_report.md` | CEK-TA-019 |
| CEK-TA-021 | P2 | done | 创建训练相关 Skills | `llm-data-curator`、`sft-engineer`、`eval-engineer` | CEK-TA-020 |

## Phase 7: Vue3 知识审计界面

目标：提供可视化工作台，方便审计知识、来源、冲突、版本和 Codex 任务记录。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-027 | P0 | done | 编写 Vue3 审计界面需求 | `Vue3知识审计界面需求.md` | CEK-TA-000 |
| CEK-TA-028 | P1 | done | 创建 Vue3 项目骨架 | `ui/` | CEK-TA-027 |
| CEK-TA-029 | P1 | done | 实现知识列表与过滤 | `ui/src/views/KnowledgeList.vue` | CEK-TA-028 |
| CEK-TA-030 | P1 | done | 实现知识详情页 | `ui/src/views/KnowledgeDetail.vue` | CEK-TA-028 |
| CEK-TA-031 | P1 | done | 实现冲突审计页 | `ui/src/views/ConflictReview.vue` | CEK-TA-028 |
| CEK-TA-032 | P2 | done | 实现 Codex 采集任务记录页 | `ui/src/views/TaskLog.vue` | CEK-TA-028 |

## Phase 8: 其他项目接入

目标：让其他交易、回测、模拟盘、实盘、LLM、RAG 项目能够稳定调用 CEK-TA 支持层。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-033 | P0 | done | 编写其他项目接入指南 | `docs/其他项目接入指南.md` | CEK-TA-000 |
| CEK-TA-034 | P1 | done | 创建业务项目 `AGENTS.md` 模板 | `codex-expert-kit/templates/external_project_AGENTS.md` | CEK-TA-033 |
| CEK-TA-035 | P1 | done | 创建 Project Adapter 模板 | `codex-expert-kit/templates/project_adapter.md` | CEK-TA-033 |
| CEK-TA-036 | P1 | done | 创建 MCP 接入示例配置 | `codex-expert-kit/templates/codex_config_mcp.toml` | CEK-TA-010 |

## Phase 9: 知识倒灌与反哺

目标：允许其他项目把专业经验、安全脱敏后的案例、审计结论和规则更新反哺到 CEK-TA，同时避免污染通用知识库。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-037 | P0 | done | 编写知识倒灌与反哺规范 | `docs/知识倒灌与反哺规范.md` | CEK-TA-033 |
| CEK-TA-038 | P0 | done | 创建倒灌任务卡模板 | `codex-expert-kit/templates/knowledge_contribution_task.md` | CEK-TA-037 |
| CEK-TA-039 | P0 | done | 定义倒灌知识 schema | `codex-expert-kit/rag/contribution_schema.md` | CEK-TA-037 |
| CEK-TA-040 | P1 | done | 定义脱敏与去项目私有化规则 | `codex-expert-kit/rag/sanitization_rules.md` | CEK-TA-037 |
| CEK-TA-041 | P1 | done | 实现倒灌队列目录 | `contributions/` | CEK-TA-038 |
| CEK-TA-042 | P1 | done | Vue3 增加倒灌队列视图 | `ui/src/views/ContributionQueue.vue` | CEK-TA-028 |

## Phase 10: 外部项目运行时接入增强

目标：让其他项目稳定调用、健康检查和回灌 CEK-TA。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-044 | P0 | done | 定义外部项目运行时接入协议 | `docs/其他项目接入指南.md`、`codex-expert-kit/templates/project_adapter.md` | CEK-TA-033 |
| CEK-TA-045 | P0 | done | 定义外部项目接入健康检查 | `codex-expert-kit/templates/external_project_healthcheck.md` | CEK-TA-044 |
| CEK-TA-046 | P1 | done | 定义外部项目知识调用与回灌流程 | `codex-expert-kit/templates/contribution_from_project.md` | CEK-TA-037 |

## Phase 11: 知识树体系

目标：让知识库按专业知识树组织、浏览和审计。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-047 | P0 | done | 定义知识树节点 schema | `codex-expert-kit/rag/knowledge_tree_schema.md` | CEK-TA-023 |
| CEK-TA-048 | P0 | done | 创建交易与 AI 专业知识树主干 | `codex-expert-kit/rag/knowledge_tree.md` | CEK-TA-047 |
| CEK-TA-049 | P1 | done | 定义知识树覆盖率与审计规则 | `codex-expert-kit/rag/knowledge_tree_audit_rules.md` | CEK-TA-048 |

## Phase 12: 专业知识采集流水线

目标：让 Codex 联网搜索、分析、归类并生成候选知识。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-050 | P0 | done | 定义研究采集任务运行规范 | `codex-expert-kit/templates/research_ingestion_runbook.md` | CEK-TA-026 |
| CEK-TA-051 | P0 | done | 定义候选知识入库包结构 | `codex-expert-kit/rag/ingestion_candidate_schema.md` | CEK-TA-050 |
| CEK-TA-052 | P1 | done | 创建首批专业主题采集 backlog | `docs/knowledge_research_backlog.md` | CEK-TA-048 |

## Phase 13: RAG 数据层与检索质量

目标：让知识可索引、可检索、可追踪和可测试。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-053 | P0 | done | 定义正式知识存储目录与索引格式 | `codex-expert-kit/rag/storage_layout.md` | CEK-TA-047 |
| CEK-TA-054 | P0 | done | 定义检索结果契约 | `codex-expert-kit/rag/search_result_contract.md` | CEK-TA-053 |
| CEK-TA-055 | P1 | done | 创建样例知识数据与检索测试集 | `codex-expert-kit/rag/examples/` | CEK-TA-054 |

## Phase 14: Knowledge MCP 运行时服务

目标：把 MCP 草案升级为可运行服务。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-056 | P0 | done | 实现 MCP server 入口 | `codex-expert-kit/mcp/server.py` | CEK-TA-054 |
| CEK-TA-057 | P0 | done | 对齐 MCP tools 与 RAG 数据层 | `codex-expert-kit/mcp/*.py` | CEK-TA-056 |
| CEK-TA-058 | P1 | done | 增加 MCP 运行时测试与示例配置 | `codex-expert-kit/mcp/tests/`、`codex-expert-kit/templates/codex_config_mcp.toml` | CEK-TA-057 |

## Phase 15: Vue3 审计工作台升级

目标：增加知识树、候选审计、检索测试和接入审计。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-059 | P0 | done | 增加知识树视图 | `ui/src/views/KnowledgeTreeView.vue` | CEK-TA-048 |
| CEK-TA-060 | P1 | done | 增加候选知识审计与检索测试台 | `ui/src/views/IngestionReview.vue`、`ui/src/views/SearchLab.vue` | CEK-TA-051 |
| CEK-TA-061 | P1 | done | 增加外部项目接入审计视图 | `ui/src/views/ProjectIntegrationAudit.vue` | CEK-TA-045 |

## Phase 16: 知识质量与评测体系

目标：用指标和评测集持续优化知识库质量。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-062 | P0 | done | 定义知识质量指标体系 | `codex-expert-kit/rag/quality_metrics.md` | CEK-TA-049 |
| CEK-TA-063 | P1 | done | 定义检索与问答评测集 | `codex-expert-kit/rag/eval_sets/` | CEK-TA-055 |
| CEK-TA-064 | P1 | done | 定义质量报告模板 | `codex-expert-kit/templates/knowledge_quality_report.md` | CEK-TA-062 |

## Phase 17: 首批真实知识资产沉淀

目标：沉淀第一批可复用、可审计、可检索专业知识。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-065 | P0 | done | 定义首批知识资产范围与验收标准 | `docs/seed_knowledge_assets_plan.md` | CEK-TA-062 |
| CEK-TA-066 | P1 | done | 创建首批 accepted 知识样例 | `codex-expert-kit/rag/knowledge/` | CEK-TA-065 |
| CEK-TA-067 | P1 | done | 对首批知识执行质量评测 | `docs/reports/seed_knowledge_quality_report.md` | CEK-TA-064 |

## Phase 18: 知识树 v2 治理升级

目标：在不破坏现有 v1 `tree_node_id`、RAG 数据层、MCP 查询和 Vue3 审计界面的前提下，让知识树支持 canonical path、alias 兼容、节点状态治理、冲突策略和安全检索路由。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-068 | P0 | done | 定义知识树 v2 迁移与兼容策略 | `codex-expert-kit/rag/knowledge_tree_v2_migration.md` | CEK-TA-048 |
| CEK-TA-069 | P0 | done | 定义知识树 v2 节点治理 schema | `codex-expert-kit/rag/knowledge_tree_node_v2_schema.md` | CEK-TA-047 |
| CEK-TA-070 | P0 | done | 定义 v1 到 v2 的 alias 映射表 | `codex-expert-kit/rag/knowledge_tree_aliases.md` | CEK-TA-068 |
| CEK-TA-071 | P1 | done | 创建知识树 v2 主干草案 | `codex-expert-kit/rag/knowledge_tree_v2.md` | CEK-TA-069 |
| CEK-TA-072 | P1 | done | 定义 v2 KB 分区与路由策略 | `codex-expert-kit/rag/kb_partitions_v2.md`、`codex-expert-kit/rag/tree_routing_policy.md` | CEK-TA-071 |
| CEK-TA-073 | P2 | done | 定义叶子知识内容包模板 | `codex-expert-kit/templates/knowledge_leaf_package_template.md` | CEK-TA-071 |
| CEK-TA-074 | P2 | done | 定义 RAG/MCP/Vue3 兼容改造清单 | `docs/knowledge_tree_v2_integration_plan.md` | CEK-TA-072 |

## Phase 19: Seed 知识运行时验证

目标：验证 Phase 17 首批 10 条 accepted seed 知识能通过 MCP/SearchLab 运行时查询命中，能返回来源、适用边界、冲突状态和推荐动作，并能阻断无来源、冲突、过期、draft/rejected 等不安全默认指导。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-075 | P0 | done | 定义 seed 运行时验证计划与查询用例 | `docs/seed_runtime_validation_plan.md` | CEK-TA-067 |
| CEK-TA-076 | P0 | done | 增加 MCP seed 知识 runtime 查询测试 | `codex-expert-kit/mcp/tests/test_seed_runtime_validation.py` | CEK-TA-075 |
| CEK-TA-077 | P0 | done | 增加阻断回归测试：无来源、冲突、过期、draft/rejected | `codex-expert-kit/mcp/tests/test_seed_runtime_blocking.py` | CEK-TA-076 |
| CEK-TA-078 | P1 | done | 对齐 SearchLab seed 查询用例展示 | `ui/src/data/*`、`ui/src/views/SearchLab.vue` | CEK-TA-075 |
| CEK-TA-079 | P1 | done | 生成 seed 运行时验证报告 | `docs/reports/seed_runtime_validation_report.md` | CEK-TA-077、CEK-TA-078 |

## Phase 20: SearchLab MCP 真实运行时与检索质量闭环

目标：把 Phase 19 的运行时验证结果接入 SearchLab 可审计链路，并补齐 canonical 过滤、alias 兼容、tree path 过滤、检索排序质量回归和阻断原因展示。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-080 | P0 | done | 定义 SearchLab 调用 MCP runtime 的本地契约 | `docs/searchlab_mcp_runtime_contract.md` | CEK-TA-079 |
| CEK-TA-081 | P0 | done | 补齐 MCP `canonical_node_id` / alias / tree path 过滤能力 | `codex-expert-kit/mcp/search_expert_knowledge.py`、`codex-expert-kit/mcp/common.py`、`codex-expert-kit/mcp/tests/` | CEK-TA-080 |
| CEK-TA-082 | P0 | done | 建立检索排序质量回归集与指标报告 | `codex-expert-kit/rag/eval_sets/runtime_ranking_eval_cases.json`、`docs/reports/runtime_ranking_quality_report.md` | CEK-TA-080 |
| CEK-TA-083 | P1 | done | 让 SearchLab 使用真实 runtime fixture/adapter 展示查询结果 | `ui/src/data/`、`ui/src/stores/`、`ui/src/views/SearchLab.vue` | CEK-TA-081、CEK-TA-082 |
| CEK-TA-084 | P1 | done | 增加 SearchLab 阻断审计展示与测试 | `ui/src/views/SearchLab.vue`、`ui/src/types.ts`、`ui/src/data/` | CEK-TA-083 |
| CEK-TA-085 | P1 | done | 生成 Phase 20 运行时质量验收报告 | `docs/reports/searchlab_mcp_runtime_quality_report.md` | CEK-TA-081、CEK-TA-082、CEK-TA-084 |

## Phase 21: MCP 正式知识聚合索引

目标：生成正式 `knowledge_items.json` 聚合索引，并让其他项目通过 MCP 默认读取正式知识库，而不是 sample fixture。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-086 | P0 | done | 创建正式知识聚合索引生成脚本 | `codex-expert-kit/rag/scripts/build_knowledge_items_index.py` | CEK-TA-066 |
| CEK-TA-087 | P0 | done | 生成正式 `knowledge_items.json` | `codex-expert-kit/rag/indexes/knowledge_items.json` | CEK-TA-086 |
| CEK-TA-088 | P0 | done | 更新 MCP 默认路径测试 | `codex-expert-kit/mcp/tests/test_server_runtime.py` | CEK-TA-087 |
| CEK-TA-089 | P1 | done | 更新 MCP 示例配置和外部接入说明 | `codex-expert-kit/templates/codex_config_mcp.toml`、`docs/其他项目接入指南.md` | CEK-TA-087 |
| CEK-TA-090 | P1 | done | 生成 Phase 21 验收报告 | `docs/reports/formal_mcp_knowledge_index_report.md` | CEK-TA-088、CEK-TA-089 |

## Phase 22: Path Resolver 移植复用地基

目标：建立统一路径 resolver，让 MCP、索引脚本、外部接入和后续开发规则不依赖硬编码绝对路径。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-091 | P0 | done | 定义并实现 CEK-TA path resolver | `codex-expert-kit/core/path_resolver.py` | CEK-TA-043 |
| CEK-TA-092 | P0 | done | 让 MCP server 使用 resolver 定位根目录和正式知识索引 | `codex-expert-kit/mcp/server.py` | CEK-TA-091 |
| CEK-TA-093 | P0 | done | 让正式知识索引生成脚本使用 resolver | `codex-expert-kit/rag/scripts/build_knowledge_items_index.py` | CEK-TA-091 |
| CEK-TA-094 | P0 | done | 把路径 resolver 规则写入 AGENTS.md 和知识库 | `AGENTS.md`、`codex-expert-kit/rag/knowledge/KB_10_PROJECT_RUNBOOKS/*.json` | CEK-TA-091 |
| CEK-TA-095 | P1 | done | 更新外部接入说明、MCP 配置和测试 | `docs/其他项目接入指南.md`、`codex-expert-kit/templates/codex_config_mcp.toml`、`codex-expert-kit/core/tests/`、`codex-expert-kit/mcp/tests/` | CEK-TA-092、CEK-TA-093 |
| CEK-TA-096 | P1 | done | 生成 Phase 22 验收报告并重建正式知识索引 | `docs/reports/path_resolver_foundation_report.md`、`codex-expert-kit/rag/indexes/knowledge_items.json` | CEK-TA-094、CEK-TA-095 |

## Phase 23: 13 分区全网专业知识采集

目标：围绕 `kb_partitions_v2.md` 的 13 个正式分区，建立可持续的全网专业知识采集矩阵、可信来源种子库、ResearchIngestionTask 队列和候选知识审计流程。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-097 | P0 | done | 定义 13 分区采集矩阵 | `docs/research/phase23_partition_collection_plan.md` | CEK-TA-072、CEK-TA-050 |
| CEK-TA-098 | P0 | done | 建立首批可信来源种子库 | `docs/research/phase23_source_seed_catalog.md` | CEK-TA-025、CEK-TA-050 |
| CEK-TA-099 | P0 | done | 为 13 分区生成 ResearchIngestionTask 队列 | `docs/research/phase23_research_task_queue.md` | CEK-TA-097、CEK-TA-098 |
| CEK-TA-100 | P1 | done | 按队列执行首批联网采集并生成候选包 | `codex-expert-kit/rag/candidates/` | CEK-TA-099 |
| CEK-TA-101 | P1 | done | 执行来源评分、冲突检测和人工审计问题整理 | `docs/reports/phase23_candidate_quality_report.md` | CEK-TA-100 |
| CEK-TA-102 | P1 | done | accepted 候选转正式知识 draft 并重建索引 | `codex-expert-kit/rag/knowledge/`、`codex-expert-kit/rag/indexes/knowledge_items.json` | CEK-TA-101 |

## Phase 24: Vue3 候选知识审计工作台 v2

目标：让 Vue3 前端承接 Phase 23 候选知识审计，支持候选查看、来源核查、冲突审计、知识树覆盖联动、候选转正式知识 draft 预览、审计决策导出和 CEK-TA-102 交接。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-103 | P0 | done | 定义 Vue3 候选审计数据契约与字段映射 | `ui/src/types.ts`、`docs/tasks/phase24_vue3_candidate_audit_workbench_v2.md` | CEK-TA-101 |
| CEK-TA-104 | P0 | done | 生成 Phase 23 candidate 前端数据 fixture | `codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py`、`ui/src/data/phase23Candidates.ts` | CEK-TA-103 |
| CEK-TA-105 | P0 | done | 重构候选知识审计台 | `ui/src/views/IngestionReview.vue`、必要的局部组件 | CEK-TA-104 |
| CEK-TA-106 | P1 | done | 增加来源、冲突、治理、转换预览面板 | `ui/src/components/`、`ui/src/views/IngestionReview.vue` | CEK-TA-105 |
| CEK-TA-107 | P1 | done | 增强知识树覆盖联动 | `ui/src/views/KnowledgeTreeView.vue`、`ui/src/stores/auditStore.ts` | CEK-TA-104 |
| CEK-TA-108 | P1 | done | 增加审计决策导出与 CEK-TA-102 交接契约 | `ui/src/data/`、`docs/reports/phase24_candidate_audit_handoff.md` | CEK-TA-106 |
| CEK-TA-109 | P1 | done | 执行 Vue3 构建、布局和审计链路验收 | `docs/reports/phase24_vue3_candidate_audit_report.md` | CEK-TA-105、CEK-TA-106、CEK-TA-107、CEK-TA-108 |

## Phase 25: Vue3 审计界面实机验收

目标：用 Playwright 对候选审计页、知识树页和 SearchLab 页执行桌面/移动端实机验收，生成截图并检查无空白、无横向溢出、过滤跳转可用。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-110 | P0 | done | 创建 Phase 25 任务卡并登记任务索引 | `docs/tasks/phase25_vue3_playwright_visual_acceptance.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-109 |
| CEK-TA-111 | P0 | done | 增加 Playwright 实机验收配置与测试 | `ui/playwright.config.ts`、`ui/tests/e2e/audit-workbench.spec.ts` | CEK-TA-110 |
| CEK-TA-112 | P0 | done | 执行桌面/移动端截图和交互验证 | `ui/test-results/`、`ui/playwright-report/` | CEK-TA-111 |
| CEK-TA-113 | P1 | done | 生成 Phase 25 实机验收报告 | `docs/reports/phase25_vue3_playwright_visual_acceptance_report.md` | CEK-TA-112 |

## Phase 26: 知识树 3 级目录 UI

目标：把现有知识树平铺表格升级为固定 3 级目录浏览模式，用户可以按“主枝 -> 分区 -> 专题”查看同一板块下的知识，并在专题详情里审计正式知识、draft、候选、来源、冲突和缺口。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-114 | P0 | done | 对齐知识树 3 级 UI 上下游、契约和任务卡 | `docs/tasks/phase26_knowledge_tree_hierarchical_ui.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-109、CEK-TA-113 |
| CEK-TA-115 | P0 | done | 建立知识树 3 级 view model | `ui/src/stores/auditStore.ts`、`ui/src/types.ts` | CEK-TA-114 |
| CEK-TA-116 | P0 | done | 重构 KnowledgeTreeView 为 3 级目录浏览界面 | `ui/src/views/KnowledgeTreeView.vue`、必要组件 | CEK-TA-115 |
| CEK-TA-117 | P1 | done | 增加 Level 3 专题详情、知识条目、候选和缺口联动 | `ui/src/views/KnowledgeTreeView.vue`、`ui/src/components/` | CEK-TA-116 |
| CEK-TA-118 | P1 | done | 增加 Playwright 3 级浏览实机验收 | `ui/tests/e2e/audit-workbench.spec.ts`、`docs/reports/phase26_knowledge_tree_hierarchical_ui_report.md` | CEK-TA-117 |

## Phase 27: 知识树阅读体验优化

目标：只针对知识树页面优化人类阅读体验，先产出独立 HTML 原型，再迁移到 Vue3。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-119 | P0 | done | 创建知识树阅读型 HTML 原型 | `docs/prototypes/knowledge_tree_reading_ui_prototype.html` | CEK-TA-118 |
| CEK-TA-120 | P0 | done | 对齐 HTML 原型到 Vue3 组件契约 | `ui/src/views/KnowledgeTreeView.vue`、`ui/src/types.ts`、`ui/src/stores/auditStore.ts` | CEK-TA-119 |
| CEK-TA-121 | P0 | done | 实现左侧可折叠知识树导航 | `ui/src/views/KnowledgeTreeView.vue`、必要组件 | CEK-TA-120 |
| CEK-TA-122 | P1 | done | 实现节点阅读区和右侧审计栏 | `ui/src/views/KnowledgeTreeView.vue`、必要组件 | CEK-TA-121 |
| CEK-TA-123 | P1 | done | 实现树内搜索、状态过滤和移动端 Tabs | `ui/src/views/KnowledgeTreeView.vue`、`ui/src/styles.css` | CEK-TA-122 |
| CEK-TA-124 | P1 | done | 增加 Playwright 阅读体验验收 | `ui/tests/e2e/audit-workbench.spec.ts`、`docs/reports/phase27_knowledge_tree_reading_ui_report.md` | CEK-TA-123 |

## Phase 28: 知识树阅读 UI Vue3 与 FastAPI 落地

目标：把 Phase 27 已对齐的 HTML 原型、用户截图目标和任务文档，落成真实可运行的 Vue3 知识树阅读页面，并补齐 FastAPI 只读数据服务契约。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-125 | P0 | done | 创建 Phase 28 任务卡并对齐 HTML、截图、文档、Vue3、FastAPI 落地范围 | `docs/tasks/phase28_knowledge_tree_vue_fastapi_delivery.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-119 |
| CEK-TA-126 | P0 | done | 定义 KnowledgeTree FastAPI 只读接口契约 | `docs/contracts/knowledge_tree_reading_api_contract.md` | CEK-TA-125 |
| CEK-TA-127 | P0 | done | 明确 FastAPI 服务位置、依赖和 resolver 路径策略 | `docs/contracts/knowledge_tree_fastapi_runtime_plan.md`、`codex-expert-kit/api/`、`codex-expert-kit/core/path_resolver.py` | CEK-TA-126 |
| CEK-TA-128 | P0 | done | 将 HTML 原型迁移到 Vue3 `KnowledgeTreeView` 信息架构 | `ui/src/views/KnowledgeTreeView.vue`、`ui/src/styles.css`、`ui/tests/e2e/audit-workbench.spec.ts` | CEK-TA-126 |
| CEK-TA-129 | P1 | done | 为 Vue3 增加 KnowledgeTree 数据 adapter，支持 FastAPI 与 fixture fallback | `ui/src/services/knowledgeTreeApi.ts`、`ui/src/stores/auditStore.ts`、`ui/src/views/KnowledgeTreeView.vue` | CEK-TA-127 |
| CEK-TA-130 | P1 | done | 增加上千知识点场景的搜索、分页、排序、页大小和虚拟列表预留 | `ui/src/views/KnowledgeTreeView.vue`、`ui/src/styles.css`、`ui/tests/e2e/audit-workbench.spec.ts` | CEK-TA-128 |
| CEK-TA-131 | P1 | done | 实现右侧审计摘要、候选跳转、SearchLab 跳转、复制 canonical_node_id | `ui/src/views/KnowledgeTreeView.vue`、`ui/tests/e2e/audit-workbench.spec.ts` | CEK-TA-129 |
| CEK-TA-132 | P1 | done | 增加 FastAPI 契约测试、Vue3 build 和 Playwright 实机验收 | `codex-expert-kit/api/tests/`、`ui/tests/e2e/audit-workbench.spec.ts` | CEK-TA-130、CEK-TA-131 |
| CEK-TA-133 | P1 | done | 生成 Phase 28 验收报告 | `docs/reports/phase28_knowledge_tree_vue_fastapi_delivery_report.md` | CEK-TA-132 |

## Phase 29: 候选知识人工审核阅读体验优化

目标：把 Phase 24 的候选知识审计页继续升级为更适合人工阅读、风险判断、来源核查、冲突核查、审核 checklist 和 CEK-TA-102 交接的工作台。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-134 | P0 | done | 创建 Phase 29 任务卡并登记任务索引 | `docs/tasks/phase29_candidate_audit_readability_workbench.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-109、CEK-TA-133 |
| CEK-TA-135 | P0 | done | 对齐候选审核页上下游、状态流和人工审核契约 | `docs/contracts/candidate_audit_readability_contract.md` | CEK-TA-134 |
| CEK-TA-136 | P0 | done | 重构候选页为“队列、正文、证据、审计动作”阅读布局 | `ui/src/views/IngestionReview.vue`、`ui/src/styles.css`、必要组件 | CEK-TA-135 |
| CEK-TA-137 | P0 | done | 增加候选审核 DoD 检查清单和阻断原因可视化 | `ui/src/components/`、`ui/src/views/IngestionReview.vue` | CEK-TA-136 |
| CEK-TA-138 | P1 | done | 增强候选筛选、批量阅读、分页和上千候选预留 | `ui/src/views/IngestionReview.vue`、`ui/src/stores/auditStore.ts` | CEK-TA-136 |
| CEK-TA-139 | P1 | done | 对齐 FastAPI/fixture 候选读取入口和只读错误契约 | `codex-expert-kit/api/`、`ui/src/services/`、`docs/contracts/candidate_audit_readability_contract.md` | CEK-TA-135 |
| CEK-TA-140 | P1 | done | 增加 Vue3 build、Playwright 桌面/移动端和审核链路验收 | `ui/tests/e2e/audit-workbench.spec.ts`、`docs/reports/phase29_candidate_audit_readability_report.md` | CEK-TA-137、CEK-TA-138、CEK-TA-139 |

## Phase 30: 候选知识 AI 审计包导出

目标：在候选页一键导出适合外部 AI 审计的 JSON 包，包内必须说明审计目标、审计规则、禁止事项、候选数据和要求返回的结果 schema。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-141 | P0 | done | 创建 Phase 30 任务卡并登记任务索引 | `docs/tasks/phase30_candidate_ai_audit_package_export.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-140 |
| CEK-TA-142 | P0 | done | 定义 AI 审计包 JSON 契约 | `docs/contracts/candidate_ai_audit_package_contract.md` | CEK-TA-141 |
| CEK-TA-143 | P0 | done | 实现候选页一键导出 AI 审计包 JSON | `ui/src/data/candidateAuditPackage.ts`、`ui/src/views/IngestionReview.vue` | CEK-TA-142 |
| CEK-TA-144 | P1 | done | 增加构建和 Playwright 导出按钮验收 | `ui/tests/e2e/audit-workbench.spec.ts` | CEK-TA-143 |

## Phase 31: 候选知识 AI 审计结果回写

目标：把外部 AI 对 Phase 30 审计包返回的审计结果，回写到 Phase 23 候选和正式 draft 知识中；补齐审计指出的来源版本、适用边界、只读权限、RAG 治理边界等修正点，并将候选设为 accepted、正式知识设为 reviewed。Phase 31 不产生 approved。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-145 | P0 | done | 创建 Phase 31 任务卡并登记任务索引 | `docs/tasks/phase31_candidate_ai_audit_result_backwrite.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-144 |
| CEK-TA-146 | P0 | done | 定义 AI 审计结果回写契约 | `docs/contracts/candidate_ai_audit_result_backwrite_contract.md` | CEK-TA-145 |
| CEK-TA-147 | P0 | done | 落地外部 AI 审计结果 JSON | `docs/audit/phase31_candidate_ai_audit_result_20260609.json` | CEK-TA-146 |
| CEK-TA-148 | P0 | done | 实现审计结果回写脚本 | `codex-expert-kit/rag/scripts/apply_candidate_ai_audit_result.py` | CEK-TA-147 |
| CEK-TA-149 | P0 | done | 修正 7 条知识并标记审计通过 | `codex-expert-kit/rag/candidates/**/*.json`、`codex-expert-kit/rag/knowledge/**/*.json` | CEK-TA-148 |
| CEK-TA-150 | P1 | done | 重建索引、fixture 并跑验证 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/phase23Candidates.ts`、`docs/reports/phase31_candidate_ai_audit_result_backwrite_report.md` | CEK-TA-149 |

## Phase 32: 候选到 reviewed 知识的批量审计工作流

目标：建立可重复、可批量、可审计的候选知识沉淀工作流，让 AI 审计通过的候选从默认待审计队列移入“AI 已通过 / 已沉淀知识”分组，并与正式 reviewed 知识、知识树、SearchLab、MCP 保持稳定回链。Phase 32 不自动产生 approved。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-151 | P0 | done | 定义候选审计流水线状态机 | `docs/contracts/candidate_to_reviewed_workflow_contract.md`、`codex-expert-kit/rag/ingestion_candidate_schema.md` | CEK-TA-150 |
| CEK-TA-152 | P0 | done | 扩展 candidate workflow 字段和 formal knowledge 回链字段 | `codex-expert-kit/rag/candidates/**/*.json`、`codex-expert-kit/rag/knowledge/**/*.json`、`ui/src/types.ts` | CEK-TA-151 |
| CEK-TA-153 | P0 | done | 优化候选页分组和默认队列 | `ui/src/views/IngestionReview.vue`、`ui/src/stores/auditStore.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-152 |
| CEK-TA-154 | P0 | done | 标准化批量 AI 审计结果导入与回写报告 | `codex-expert-kit/rag/scripts/apply_candidate_ai_audit_result.py`、`docs/audit/`、`docs/reports/` | CEK-TA-152 |
| CEK-TA-155 | P1 | done | 增加批量质量门禁 | `codex-expert-kit/rag/scripts/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`docs/reports/` | CEK-TA-154 |
| CEK-TA-156 | P1 | done | 增加知识树、SearchLab、MCP 联动验证 | `ui/tests/e2e/audit-workbench.spec.ts`、`codex-expert-kit/api/tests/`、`codex-expert-kit/mcp/tests/` | CEK-TA-155 |
| CEK-TA-157 | P1 | done | 生成 Phase 32 验收报告 | `docs/reports/phase32_candidate_to_reviewed_workflow_report.md` | CEK-TA-156 |
| CEK-TA-494 | P1 | done | 将已重建且已有 formal reviewed 替代知识的 rejected 候选拆分为“已重建归档” | `codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py`、`ui/src/views/IngestionReview.vue`、`ui/src/types.ts`、`ui/src/data/phase23Candidates.ts`、`docs/reports/phase32_rebuilt_archived_candidate_ui_report.json` | CEK-TA-157 |

## Phase 33: 知识库污染清理与门禁

目标：清理正式知识库中由 mock、demo、test、fixture、internal-only 占位资料造成的污染，并增加门禁，确保 MCP/SearchLab/Vue3 默认读取的都是正式、可追踪、可审计的专业知识。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-158 | P0 | done | 定义知识污染判定契约 | `docs/contracts/knowledge_pollution_cleanup_contract.md` | CEK-TA-157 |
| CEK-TA-159 | P0 | done | 扫描正式知识库污染候选并生成报告 | `docs/reports/phase33_knowledge_pollution_scan_report.json` | CEK-TA-158 |
| CEK-TA-160 | P0 | done | 从正式知识库移除 mock/test/internal-only 污染知识点 | `codex-expert-kit/rag/knowledge/` | CEK-TA-159 |
| CEK-TA-161 | P0 | done | 增加知识污染质量门禁 | `codex-expert-kit/rag/scripts/validate_knowledge_pollution.py` | CEK-TA-160 |
| CEK-TA-162 | P1 | done | 重建索引、Vue3 fixture 并验证知识树/MCP/SearchLab | `knowledge_items.json`、`formalKnowledgeItems.ts`、测试报告 | CEK-TA-161 |
| CEK-TA-163 | P1 | done | 生成 Phase 33 验收报告并更新索引 | `docs/reports/phase33_knowledge_pollution_cleanup_report.md` | CEK-TA-162 |

## Phase 34: 知识卡片 Schema v1.1 与默认指导门禁升级

目标：把正式知识卡片升级为可审计、可检索、可治理、可被 MCP/RAG 安全调用的专业知识项；补齐 `claim_type`、`classification_notes`、`llm_usage_policy`、`machine_gate` 和 `recommended_extra_sources`，并对齐 MCP、SearchLab、FastAPI 和 Vue3 展示契约。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-164 | P0 | done | 定义 KnowledgeItem Schema v1.1 补强契约 | `codex-expert-kit/rag/knowledge_item_schema.md`、`docs/contracts/knowledge_item_schema_v1_1_contract.md` | CEK-TA-163 |
| CEK-TA-165 | P0 | done | 增加 claim_type、classification_notes、llm_usage_policy、machine_gate 字段规范 | `codex-expert-kit/rag/knowledge_item_schema.md`、`codex-expert-kit/rag/metadata_schema.md` | CEK-TA-164 |
| CEK-TA-166 | P0 | done | 批量升级正式知识卡片并保持向后兼容 | `codex-expert-kit/rag/knowledge/**/*.json` | CEK-TA-165 |
| CEK-TA-167 | P0 | done | 增加 machine_gate 生成与验证脚本 | `codex-expert-kit/rag/scripts/build_machine_gate.py`、`codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py` | CEK-TA-166 |
| CEK-TA-168 | P0 | done | 更新 MCP/SearchLab 默认指导门禁 | `codex-expert-kit/mcp/`、`codex-expert-kit/rag/searchlab/`、相关测试 | CEK-TA-167 |
| CEK-TA-169 | P1 | done | 更新 FastAPI 知识读取接口契约和返回字段 | `codex-expert-kit/api/`、`docs/contracts/knowledge_tree_reading_api_contract.md` | CEK-TA-167 |
| CEK-TA-170 | P1 | done | 更新 Vue3 知识详情和知识树审计栏展示 | `ui/src/types.ts`、`ui/src/views/KnowledgeTreeView.vue`、`ui/src/views/KnowledgeDetail.vue` | CEK-TA-169 |
| CEK-TA-171 | P1 | done | 建立 recommended_extra_sources 来源增强队列 | `docs/research/`、正式知识 JSON、来源增强任务模板 | CEK-TA-165 |
| CEK-TA-172 | P1 | done | 重建索引、fixture，并跑 API/MCP/Vue3 验收 | `knowledge_items.json`、`formalKnowledgeItems.ts`、测试报告、Phase 34 验收报告 | CEK-TA-168、CEK-TA-170 |

## Phase 35: 外部项目 AI 主动检索协议

目标：让外部项目 AI 在涉及交易、回测、模拟盘、实盘、RAG、MCP、LLM 训练和知识治理任务时，主动调用 CEK-TA MCP，而不是依赖模型记忆；明确“什么时候必须搜、怎么搜、怎么引用、没搜到怎么办”。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-173 | P0 | done | 定义外部项目 AI 主动检索协议 | `docs/contracts/external_ai_active_retrieval_protocol.md` | CEK-TA-172 |
| CEK-TA-174 | P0 | done | 创建外部项目 AGENTS 主动检索模板 | `codex-expert-kit/templates/external_project_active_retrieval_AGENTS.md` | CEK-TA-173 |
| CEK-TA-175 | P0 | done | 更新外部项目 AGENTS 模板引用主动检索协议 | `codex-expert-kit/templates/external_project_AGENTS.md` | CEK-TA-174 |
| CEK-TA-176 | P1 | done | 创建主动检索测试计划 | `codex-expert-kit/templates/external_project_active_retrieval_test_plan.md` | CEK-TA-174 |
| CEK-TA-177 | P1 | done | 增加主动检索协议 pytest 验证 | `codex-expert-kit/mcp/tests/test_external_ai_active_retrieval_protocol.py` | CEK-TA-176 |
| CEK-TA-178 | P1 | done | 更新任务索引并完成验收 | `docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-177 |
| CEK-TA-262 | P1 | done | 调整 MCP 默认检索信用语义：正式入库 reviewed 知识默认作为 accepted_reference 返回，approved/allow 仍作为高置信默认指导 | `codex-expert-kit/mcp/common.py`、`docs/contracts/external_ai_active_retrieval_protocol.md`、`codex-expert-kit/templates/external_project_active_retrieval_AGENTS.md`、`codex-expert-kit/mcp/tests/` | CEK-TA-178 |

## Phase 36: AI Engineering 交易 LLM Gating/Scoring 知识扩展

目标：为第一个外接项目“训练 LLM 进行交易 gating/scoring，提高交易质量（R/R、胜率、PnL、风险过滤质量等）”扩展 AI Engineering 专业知识树、采集队列、上下游契约和 MCP/SearchLab/KnowledgeTree 运行时验证。

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

## Phase 37: Trading Engineering 专业知识库扩展

目标：承接 Phase 36 划出的交易专业规则本体边界，把 K 线、策略、市场数据、回测、回放、模拟盘、实盘执行、风控和交易复盘等知识点归入 Trading Engineering 对应分支，防止后续都塞进 AI Engineering。

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

## Phase 45: Trading Engineering P1 专业知识补全

目标：基于 Phase 37 完成后缺口审计，补齐机构级交易系统需要的 TCA、审计追踪、分层风控、系统韧性、压力测试、订单语义、数据授权和 crypto perpetual 特有风险知识。Phase 45 不推翻 Phase 37 P0，只做 P1/P2 扩展；新增知识不得直接进入 approved、default guidance 或 hard gate。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-452 | P0 | done | 定义 Phase 45 Trading Engineering P1/P2 知识范围、分区、canonical node 和边界 | `docs/research/phase45_trading_engineering_p1_knowledge_scope.md`、`codex-expert-kit/rag/knowledge_tree.md` | CEK-TA-451 |
| CEK-TA-453 | P0 | done | 定义 Execution TCA、Audit Trail、Layered Risk、Resilience、Stress、Order Semantics 的跨分支契约 | `docs/contracts/phase45_trading_engineering_p1_runtime_contract.md` | CEK-TA-452 |
| CEK-TA-454 | P0 | done | 创建 Phase 45 ResearchIngestionTask 队列和来源种子库 | `docs/research/phase45_trading_engineering_p1_research_task_queue.md`、`docs/research/phase45_trading_engineering_p1_source_seed.md` | CEK-TA-453 |
| CEK-TA-455 | P0 | done | 生成 Phase 45 知识范围审计 JSON，供外部 AI/人工先审分支、边界、知识点数量和优先级 | `docs/audit/phase45_trading_engineering_p1_knowledge_scope_for_audit.json` | CEK-TA-454 |
| CEK-TA-456 | P1 | done | 采集 Execution TCA 6 条 P1 候选知识 | `codex-expert-kit/rag/candidates/KB_06_LIVE_EXECUTION/`、`codex-expert-kit/rag/candidates/KB_07_TRADE_ANALYSIS/`、`docs/research/phase45_execution_tca_candidate_research.md` | CEK-TA-455 |
| CEK-TA-457 | P1 | done | 导出 Execution TCA 候选审计包并运行质量门禁 | `docs/audit/phase45_execution_tca_candidate_audit_package_20260612.json`、`docs/reports/phase45_execution_tca_candidate_audit_package_quality_gate.json` | CEK-TA-456 |
| CEK-TA-458 | P1 | done | 按审计结果处理 Execution TCA 候选，补证并沉淀 formal reviewed/caveat_only | `codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/`、`codex-expert-kit/rag/knowledge/KB_07_TRADE_ANALYSIS/`、`docs/reports/phase45_execution_tca_import_report.json` | CEK-TA-457 |
| CEK-TA-459 | P1 | done | 采集 Audit Trail / Clock Sync 6 条 P1 候选知识 | `codex-expert-kit/rag/candidates/KB_02_DATA_ENGINEERING/`、`codex-expert-kit/rag/candidates/KB_06_LIVE_EXECUTION/`、`codex-expert-kit/rag/candidates/KB_AI_26_DATABASE_STORAGE/`、`docs/research/phase45_trade_audit_candidate_research.md` | CEK-TA-455 |
| CEK-TA-460 | P1 | done | 导出 Audit Trail / Clock Sync 审计包、处理审计结果并沉淀 formal reviewed/caveat_only | `docs/audit/phase45_trade_audit_candidate_audit_package_20260612.json`、`codex-expert-kit/rag/knowledge/`、`docs/reports/phase45_trade_audit_formal_import_report.json` | CEK-TA-459 |
| CEK-TA-461 | P1 | done | 采集 Layered Risk Controls / Credit / Margin 6 条 P1 候选知识 | `codex-expert-kit/rag/candidates/KB_07_RISK_MANAGEMENT/`、`docs/research/phase45_layered_risk_candidate_research.md` | CEK-TA-455 |
| CEK-TA-462 | P1 | done | 导出 Layered Risk 审计包、处理审计结果并沉淀 formal reviewed/caveat_only | `docs/audit/phase45_layered_risk_candidate_audit_package_20260612.json`、`docs/audit/audit_phase45_layered_risk_p45_c_20260612_external_strict_v1.json`、`docs/audit/phase45_layered_risk_supplemental_reaudit_package_20260612.json`、`docs/audit/audit_phase45_layered_risk_supplemental_reaudit_20260612_v1.json`、`docs/audit/phase45_layered_risk_reviewed_preparation_audit_package_20260612.json`、`docs/audit/audit_phase45_layered_risk_reviewed_caveat_only_preparation_20260612_v1.json`、`docs/reports/phase45_layered_risk_formal_import_report.json`、`docs/contracts/phase45_layered_risk_controls_contract.md` | CEK-TA-461 |
| CEK-TA-463 | P1 | done | 采集 Resilience / Incident / Log Management 6 条 P1 候选知识 | `codex-expert-kit/rag/candidates/KB_06_LIVE_EXECUTION/`、`codex-expert-kit/rag/candidates/KB_AI_26_DATABASE_STORAGE/`、`docs/research/phase45_resilience_incident_log_candidate_research.md`、`docs/reports/phase45_resilience_incident_log_candidate_generation_report.json` | CEK-TA-455 |
| CEK-TA-464 | P1 | done | 导出 Resilience / Incident / Log 审计包、处理审计结果并沉淀 formal reviewed/caveat_only | `docs/audit/phase45_resilience_incident_log_candidate_audit_package_20260612.json`、`docs/audit/audit_phase45_resilience_incident_log_20260612_external_strict_v1.json`、`docs/contracts/phase45_resilience_incident_log_runtime_contract.md`、`docs/audit/phase45_resilience_incident_log_supplemental_reaudit_package_20260612.json`、`docs/audit/audit_phase45_resilience_incident_log_supplemental_reaudit_20260612_v1.json`、`docs/reports/phase45_resilience_incident_log_audit_import_report.json`、`docs/reports/phase45_resilience_incident_log_supplemental_reaudit_import_report.json`、`docs/audit/phase45_resilience_incident_log_reviewed_preparation_audit_package_20260612.json`、`docs/audit/audit_phase45_resilience_incident_log_reviewed_preparation_20260612.json`、`docs/reports/phase45_resilience_incident_log_reviewed_preparation_gap_report.json`、`docs/reports/phase45_resilience_incident_log_formal_import_report.json`、`docs/audit/phase45_resilience_incident_log_reviewed_blocked_supplemental_reaudit_package_20260612.json`、`docs/audit/audit_phase45_resilience_incident_log_reviewed_blocked_supplemental_reaudit_20260612.json`、`docs/reports/phase45_resilience_incident_log_reviewed_blocked_supplemental_reaudit_gate.json`、`docs/reports/phase45_resilience_incident_log_blocked_supplemental_reaudit_import_report.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/`、`codex-expert-kit/rag/knowledge/KB_AI_26_DATABASE_STORAGE/` | CEK-TA-463 |
| CEK-TA-465 | P1 | done | 采集 Stress Testing / Scenario Risk 6 条 P1 候选知识 | `codex-expert-kit/rag/scripts/generate_phase45_stress_scenario_candidates.py`、`codex-expert-kit/rag/candidates/KB_07_RISK_MANAGEMENT/`、`docs/research/phase45_stress_scenario_candidate_research.md`、`docs/reports/phase45_stress_scenario_candidate_generation_report.json`、`docs/reports/phase45_stress_scenario_candidate_quality_gate.json` | CEK-TA-455 |
| CEK-TA-466 | P1 | done | 导出 Stress Testing / Scenario Risk 审计包、处理审计结果并沉淀 formal reviewed/caveat_only | `codex-expert-kit/rag/scripts/export_phase45_stress_scenario_candidate_audit_package.py`、`codex-expert-kit/rag/scripts/apply_phase45_stress_scenario_candidate_audit_result.py`、`codex-expert-kit/rag/scripts/apply_phase45_stress_scenario_supplemental_reaudit_result.py`、`codex-expert-kit/rag/scripts/apply_phase45_stress_scenario_stress04_margin_funding_reaudit_result.py`、`codex-expert-kit/rag/scripts/apply_phase45_stress_scenario_reviewed_preparation_result.py`、`codex-expert-kit/rag/scripts/apply_phase45_stress02_market_liquidity_reaudit_result.py`、`codex-expert-kit/rag/scripts/validate_phase45_runtime_linkage.py`、`docs/contracts/phase45_stress_scenario_risk_contract.md`、`docs/audit/phase45_stress_scenario_candidate_audit_package_20260612.json`、`docs/audit/audit_phase45_stress_scenario_candidate_20260612_external_strict.json`、`docs/audit/audit_phase45_stress_scenario_supplemental_reaudit_20260612.json`、`docs/audit/audit_phase45_stress04_margin_funding_reaudit_20260612.json`、`docs/audit/audit_phase45_stress_scenario_reviewed_preparation_20260612.json`、`docs/audit/phase45_stress_scenario_reviewed_preparation_audit_package_20260612.json`、`docs/audit/phase45_stress_scenario_stress02_market_liquidity_reaudit_package_20260612.json`、`docs/audit/audit_phase45_stress02_market_liquidity_reaudit_20260612.json`、`docs/reports/phase45_stress_scenario_candidate_audit_package_quality_gate.json`、`docs/reports/phase45_stress_scenario_candidate_audit_import_report.json`、`docs/reports/phase45_stress_scenario_supplemental_reaudit_import_report.json`、`docs/reports/phase45_stress_scenario_stress04_margin_funding_reaudit_import_report.json`、`docs/reports/phase45_stress_scenario_reviewed_preparation_gap_report.json`、`docs/reports/phase45_stress_scenario_reviewed_preparation_import_report.json`、`docs/reports/phase45_stress_scenario_stress02_market_liquidity_reaudit_gate.json`、`docs/reports/phase45_stress02_market_liquidity_reaudit_import_report.json`、`docs/reports/phase45_runtime_linkage_report.json`、`docs/research/phase45_stress_scenario_supplemental_research.md`、`docs/research/phase45_stress_scenario_stress04_margin_funding_research.md`、`docs/research/phase45_stress_scenario_stress02_market_liquidity_research.md`、`codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/` | CEK-TA-465 |
| CEK-TA-467 | P1 | done | 采集 Order Type / TIF / Venue Semantics 6 条 P1 候选知识 | `codex-expert-kit/rag/scripts/generate_phase45_order_semantics_candidates.py`、`codex-expert-kit/rag/candidates/KB_06_LIVE_EXECUTION/`、`docs/research/phase45_order_semantics_candidate_research.md`、`docs/reports/phase45_order_semantics_candidate_generation_report.json`、`docs/reports/phase45_order_semantics_candidate_quality_gate.json` | CEK-TA-455 |
| CEK-TA-468 | P1 | done | 导出 Order Semantics 审计包、处理审计结果并沉淀 formal reviewed/caveat_only | `codex-expert-kit/rag/scripts/export_phase45_order_semantics_candidate_audit_package.py`、`codex-expert-kit/rag/scripts/apply_phase45_order_semantics_candidate_audit_result.py`、`codex-expert-kit/rag/scripts/apply_phase45_order_semantics_reviewed_preparation_result.py`、`codex-expert-kit/rag/scripts/apply_phase45_order_semantics_ord05_supplemental_reaudit_result.py`、`docs/contracts/phase45_order_semantics_runtime_contract.md`、`docs/audit/phase45_order_semantics_candidate_audit_package_20260612.json`、`docs/audit/audit_phase45_order_semantics_candidate_20260612_external_strict.json`、`docs/audit/phase45_order_semantics_reviewed_preparation_audit_package_20260612.json`、`docs/audit/audit_phase45_order_semantics_reviewed_preparation_20260612.json`、`docs/audit/phase45_order_semantics_ord05_supplemental_reaudit_package_20260612.json`、`docs/audit/audit_phase45_order_semantics_ord05_supplemental_reaudit_20260612.json`、`docs/research/phase45_order_semantics_ord05_supplemental_research.md`、`docs/reports/phase45_order_semantics_candidate_audit_package_quality_gate.json`、`docs/reports/phase45_order_semantics_candidate_audit_import_report.json`、`docs/reports/phase45_order_semantics_reviewed_preparation_gap_report.json`、`docs/reports/phase45_order_semantics_ord05_supplemental_reaudit_gate.json`、`docs/reports/phase45_order_semantics_import_report.json`、`docs/reports/phase45_order_semantics_ord05_formal_import_report.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_phase45_order_semantics.order_type_semantics_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_phase45_order_semantics.time_in_force_semantics_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_phase45_order_semantics.post_only_reduce_only_boundary.v1.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_phase45_order_semantics.self_trade_prevention_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_phase45_order_semantics.exchange_specific_order_type_caveat.v1.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_phase45_order_semantics.maker_taker_fee_order_type_boundary.v1.json` | CEK-TA-467 |
| CEK-TA-469 | P2 | done | 采集 Market Data Entitlement / Reference Data 6 条 P2 候选知识 | `codex-expert-kit/rag/scripts/generate_phase45_reference_data_entitlement_candidates.py`、`codex-expert-kit/rag/candidates/KB_02_DATA_ENGINEERING/`、`docs/research/phase45_reference_data_entitlement_candidate_research.md`、`docs/reports/phase45_reference_data_entitlement_candidate_generation_report.json`、`docs/reports/phase45_reference_data_entitlement_candidate_quality_gate.json` | CEK-TA-468 |
| CEK-TA-470 | P2 | done | 采集 Crypto Perpetual 特有风险 5 条 P2 候选知识 | `codex-expert-kit/rag/scripts/generate_phase45_crypto_perp_candidates.py`、`codex-expert-kit/rag/candidates/KB_03_MARKET_MICROSTRUCTURE/`、`codex-expert-kit/rag/candidates/KB_07_RISK_MANAGEMENT/`、`docs/research/phase45_crypto_perp_candidate_research.md`、`docs/reports/phase45_crypto_perp_candidate_generation_report.json`、`docs/reports/phase45_crypto_perp_candidate_quality_gate.json` | CEK-TA-469 |
| CEK-TA-471 | P2 | done | 导出 P2 候选审计包、处理审计结果并沉淀 11 条 formal reviewed/caveat_only | `codex-expert-kit/rag/scripts/export_phase45_p2_candidate_audit_package.py`、`codex-expert-kit/rag/scripts/apply_phase45_p2_candidate_audit_result.py`、`codex-expert-kit/rag/scripts/apply_phase45_p2_supplemental_reaudit_result.py`、`codex-expert-kit/rag/scripts/apply_phase45_p2_reviewed_preparation_result.py`、`codex-expert-kit/rag/scripts/apply_phase45_p2_blocked_supplemental_reaudit_result.py`、`docs/audit/phase45_p2_candidate_audit_package_20260612.json`、`docs/audit/audit_phase45_p2_reviewed_blocked_supplemental_reaudit_20260612.json`、`docs/reports/phase45_p2_reviewed_blocked_supplemental_import_report.json`、`codex-expert-kit/rag/knowledge/KB_02_DATA_ENGINEERING/kb_phase45_p2.dataset_coverage_universe_declaration_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/kb_phase45_p2.maintenance_margin_liquidation_boundary.v1.json`、`codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/kb_phase45_p2.exchange_outage_and_clawback_risk.v1.json`；P2-G/P2-H 共 11 条已全部沉淀 formal reviewed/caveat_only，未创建 approved/default guidance/hard gate | CEK-TA-470 |
| CEK-TA-472 | P1 | done | 重建 knowledge_items、Vue3 fixture、知识树，并验证 MCP/SearchLab/KnowledgeTree 能命中、引用和阻断 Phase 45 知识 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts`、`ui/src/data/knowledgeTreeNodes.ts`、`codex-expert-kit/rag/scripts/validate_phase45_runtime_linkage.py`、`docs/reports/phase45_runtime_linkage_report.json`；Phase 45 47 条均为 reviewed/caveat_only，default guidance/approved/hard gate 均未开启 | CEK-TA-471 |
| CEK-TA-473 | P1 | done | 生成 Phase 45 验收报告并更新索引 | `docs/reports/phase45_trading_engineering_p1_completion_report.md`；Phase 45 状态已更新为 done | CEK-TA-472 |

## Phase 46: Trading Engineering 知识回归评测

目标：将 Phase 37/45 Trading Engineering 正式知识转成可持续回归评测集，验证 MCP/SearchLab/KnowledgeTree 能稳定命中、返回来源、保持边界并阻断默认指导误用。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-474 | P0 | done | 创建 Phase 46 任务卡、索引入口和评测契约 | `docs/tasks/phase46_trading_engineering_regression_eval.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-473 |
| CEK-TA-475 | P0 | done | 建立 Trading Engineering 回归评测集和验证脚本 | `codex-expert-kit/rag/scripts/validate_trading_engineering_regression.py`、`docs/reports/phase46_trading_engineering_regression_report.json` | CEK-TA-474 |
| CEK-TA-476 | P1 | done | 扩展 SearchLab/MCP 检索案例，覆盖 13 个 Trading 分区和 Phase 45 扩展节点 | `docs/reports/phase46_searchlab_case_matrix.json` | CEK-TA-475 |
| CEK-TA-477 | P1 | done | 增加 Vue3 知识树与候选队列一致性验收 | `docs/reports/phase46_vue_tree_candidate_consistency_report.json` | CEK-TA-475 |
| CEK-TA-478 | P1 | done | 生成 Phase 46 验收报告并更新状态 | `docs/reports/phase46_trading_engineering_regression_eval_report.md` | CEK-TA-476、CEK-TA-477 |

## Phase 47: AI/Trading Engineering 双主线归类与运行时一致性审计

目标：审计 AI Engineering 与 Trading Engineering 两条主线的 L1/L2/L3 知识树、正式知识归类、候选回链、Vue3 展示和 MCP Server 调用是否一致，避免知识点误挂、前端统计错位或 MCP 检索边界失效。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-479 | P0 | done | 创建 Phase 47 任务卡、索引入口和审计契约 | `docs/tasks/phase47_ai_trade_engineering_alignment_audit.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-478 |
| CEK-TA-480 | P0 | done | 建立 AI/Trading 双主线知识树归类审计脚本 | `codex-expert-kit/rag/scripts/audit_ai_trade_engineering_tree_alignment.py`、`docs/reports/phase47_tree_alignment_audit_report.json` | CEK-TA-479 |
| CEK-TA-481 | P0 | done | 审计正式知识条目的分类、状态、来源、冲突和机器门控 | `docs/reports/phase47_formal_knowledge_classification_audit.json` | CEK-TA-480 |
| CEK-TA-482 | P1 | done | 审计候选知识和正式知识的队列关系、回链和重复挂载 | `docs/reports/phase47_candidate_formal_linkage_audit.json` | CEK-TA-480 |
| CEK-TA-483 | P1 | done | 审计 Vue3 前端知识树、候选页、SearchLab 页显示是否对齐 | `docs/reports/phase47_vue3_display_alignment_report.json` | CEK-TA-480 |
| CEK-TA-484 | P1 | done | 审计 MCP Server 对 AI/Trading 两条主线的检索、引用和阻断是否正常 | `docs/reports/phase47_mcp_runtime_alignment_report.json` | CEK-TA-480 |
| CEK-TA-485 | P1 | done | 整理发现的问题、修复建议和后续任务拆分 | `docs/reports/phase47_alignment_findings_and_fix_plan.md` | CEK-TA-481、CEK-TA-482、CEK-TA-483、CEK-TA-484 |
| CEK-TA-486 | P1 | done | 生成 Phase 47 验收报告并更新状态 | `docs/reports/phase47_ai_trade_engineering_alignment_audit_report.md` | CEK-TA-485 |

## Phase 48: 知识树 canonical alias 与 reviewed schema backfill 修复

目标：承接 Phase 47 的审计发现，先修复 AI/Trading 知识树 canonical node / alias，再对历史 reviewed/caveat_only 正式知识补齐显式权限字段，确保 Vue3、MCP/SearchLab 和可迁移 RAG 平台都能按同一治理口径消费知识。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-487 | P0 | done | 创建 Phase 48 任务卡、索引入口和修复契约 | `docs/tasks/phase48_tree_alias_schema_backfill.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-486 |
| CEK-TA-488 | P0 | done | 建立 canonical node / alias 修复计划 | `docs/reports/phase48_tree_alias_repair_plan.json` | CEK-TA-487 |
| CEK-TA-489 | P0 | done | 实现知识树 canonical/alias 修复脚本并重建 Vue3 知识树 fixture | `codex-expert-kit/rag/scripts/repair_phase48_tree_aliases.py`、`ui/src/data/knowledgeTreeNodes.ts`、`docs/reports/phase48_tree_alias_repair_report.json` | CEK-TA-488 |
| CEK-TA-490 | P0 | done | 运行知识树、Vue3、MCP/SearchLab 联动回归验证 | `docs/reports/phase48_tree_alias_validation_report.json` | CEK-TA-489 |
| CEK-TA-491 | P0 | done | 实现历史 reviewed schema 权限字段 backfill | `codex-expert-kit/rag/scripts/backfill_phase48_reviewed_permissions.py`、`docs/reports/phase48_reviewed_schema_backfill_report.json` | CEK-TA-490 |
| CEK-TA-492 | P0 | done | 重建正式知识索引和前端 fixture，验证无权限升级 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`docs/reports/phase48_runtime_permission_validation_report.json` | CEK-TA-491 |
| CEK-TA-493 | P1 | done | 生成 Phase 48 验收报告并更新状态 | `docs/reports/phase48_tree_alias_schema_backfill_report.md` | CEK-TA-492 |

## Phase 49: Vue3 前端白屏与 Dev Server 稳定性修复

目标：定位并修复 Vue3 审计工作台刷新后白屏的问题，避免大体量 fixture 重写时被 Vite dev server 缓存为空模块或半写模块。

任务卡：[tasks/phase49_vue3_dev_server_stability.md](./tasks/phase49_vue3_dev_server_stability.md)

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-495 | P0 | done | 复现 Vue3 刷新白屏并记录根因 | `docs/reports/phase49_vue3_white_screen_root_cause_report.json` | CEK-TA-494 |
| CEK-TA-496 | P0 | done | 将 Vue3 大 fixture 生成改为原子写入 | `codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py`、`codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py`、`codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py` | CEK-TA-495 |
| CEK-TA-497 | P0 | done | 调整 Vite watcher 等待写入稳定，降低半写模块被缓存风险 | `ui/vite.config.ts` | CEK-TA-496 |
| CEK-TA-498 | P1 | done | 运行 build、fixture 生成、浏览器刷新验证 | `docs/reports/phase49_vue3_dev_server_stability_report.json` | CEK-TA-497 |

## Phase 50: Vue3 大 Fixture 拆包与懒加载

目标：承接 Phase 49 的白屏根因修复，把候选、正式知识和知识树大 fixture 从 Vue3 首包拆出，形成可分页、可缓存、可按需加载的数据访问层，降低刷新白屏、首包过大和 dev server 压力。

任务卡：[tasks/phase50_vue3_fixture_lazy_loading.md](./tasks/phase50_vue3_fixture_lazy_loading.md)

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-499 | P0 | done | 定义 Vue3 fixture 拆包与懒加载数据契约 | `docs/contracts/phase50_vue3_data_loading_contract.md` | CEK-TA-498 |
| CEK-TA-500 | P0 | done | 拆分候选、正式知识、知识树静态数据输出格式 | `ui/public/data/*.json` 或等价数据目录、生成脚本改造方案 | CEK-TA-499 |
| CEK-TA-501 | P0 | done | 实现 Vue3 数据访问 adapter，替代页面直接 import 大 fixture | `ui/src/services/knowledgeDataClient.ts`、相关 composables | CEK-TA-500 |
| CEK-TA-502 | P1 | done | 优化候选页、知识树页、SearchLab 页 loading/empty/error 与分页状态 | `ui/src/views/*`、相关组件 | CEK-TA-501 |
| CEK-TA-503 | P1 | done | 增加大数据量刷新、分页、过滤和离线 fallback 的 Playwright 验收 | `ui/tests/e2e/fixture-lazy-loading.spec.ts` | CEK-TA-502 |
| CEK-TA-504 | P1 | done | 增加首包体积、白屏、模块导出和中文文案回归门禁 | `docs/reports/phase50_vue3_lazy_loading_validation_report.json` | CEK-TA-503 |
| CEK-TA-505 | P1 | done | 生成 Phase 50 验收报告并更新任务索引 | `docs/reports/phase50_vue3_fixture_lazy_loading_report.md` | CEK-TA-504 |

## Phase 51: Vue3 KnowledgeTree 大分支性能优化

目标：承接 Phase 50 的拆包与懒加载，把知识树大分支页面从“前端一次性生成全量卡片”升级为“预计算范围索引 + 分页摘要 + 详情按需加载 + 虚拟滚动 + 搜索 debounce”，确保知识点数量继续增长后仍能稳定阅读和审计。

任务卡：[tasks/phase51_knowledge_tree_large_scope_performance.md](./tasks/phase51_knowledge_tree_large_scope_performance.md)

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-506 | P0 | done | 定义知识树大分支性能预算与当前基线 | `docs/reports/phase51_knowledge_tree_performance_baseline.json` | CEK-TA-505 |
| CEK-TA-507 | P0 | done | 给知识树数据增加 `node_id -> knowledge_ids/candidate_ids` 预计算索引 | `ui/public/data/knowledgeTreeScopeIndex.json`、相关生成脚本 | CEK-TA-506 |
| CEK-TA-508 | P0 | done | 定义知识树范围分页、摘要卡和详情懒加载契约 | `docs/contracts/phase51_knowledge_tree_scope_paging_contract.md` | CEK-TA-507 |
| CEK-TA-509 | P0 | done | 将知识树页面列表改成范围分页读取，不一次生成全量卡片 | `ui/src/views/KnowledgeTreeView.vue`、`ui/src/services/knowledgeDataClient.ts` | CEK-TA-508 |
| CEK-TA-510 | P1 | done | 将知识点卡片改成摘要卡，点击后再加载详情 | `ui/src/components/`、知识详情加载逻辑 | CEK-TA-509 |
| CEK-TA-511 | P1 | done | 大列表接入虚拟滚动，搜索输入增加 debounce 和最小搜索长度 | `ui/src/components/`、`ui/src/composables/` | CEK-TA-510 |
| CEK-TA-512 | P1 | done | 增加 Playwright 大分支性能验收 | `ui/tests/e2e/knowledge-tree-performance.spec.ts`、`docs/reports/phase51_knowledge_tree_large_scope_performance_report.json` | CEK-TA-511 |
| CEK-TA-513 | P1 | done | 生成 Phase 51 验收报告并更新任务索引 | `docs/reports/phase51_knowledge_tree_large_scope_performance_report.md` | CEK-TA-512 |

## Phase 52: AI/Trading Engineering 权威资料缺口复审

目标：对照全网权威资料、标准、官方文档和典型案例，复审当前 AI Engineering 与 Trading Engineering 两条主线的知识覆盖、分类边界和后续补充优先级。

任务卡：[tasks/phase52_ai_trade_authoritative_gap_audit.md](./tasks/phase52_ai_trade_authoritative_gap_audit.md)

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-514 | P0 | done | 创建 Phase 52 任务卡和任务索引 | `docs/tasks/phase52_ai_trade_authoritative_gap_audit.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-513 |
| CEK-TA-515 | P0 | done | 扫描本地 AI/Trading 知识覆盖和关键词缺口 | `docs/reports/phase52_ai_trade_authoritative_gap_audit_report.md` | CEK-TA-514 |
| CEK-TA-516 | P0 | done | 联网检索权威资料、标准和案例并建立对照判断 | `docs/reports/phase52_ai_trade_authoritative_gap_audit_report.md` | CEK-TA-515 |
| CEK-TA-517 | P1 | done | 输出补充知识点建议、优先级和后续 Phase 建议 | `docs/reports/phase52_ai_trade_authoritative_gap_audit_report.md` | CEK-TA-516 |

## Phase 53: AI/Trading 安全、市场行为与运行治理知识扩展

目标：承接 Phase 52 的缺口审计结论，补齐 AI Agent 安全、AI SBOM、市场行为监控、Market Access / DEA / Reg NMS 边界，以及交易审计时间同步知识。

任务卡：[tasks/phase53_ai_trade_security_market_conduct_extension.md](./tasks/phase53_ai_trade_security_market_conduct_extension.md)

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-518 | P0 | done | 定义 Phase 53 知识范围、L2/L3 节点和跨分支边界 | `docs/research/phase53_ai_trade_security_market_conduct_scope.md` | CEK-TA-517 |
| CEK-TA-519 | P0 | done | 创建 Phase 53 来源种子库和 ResearchIngestionTask 队列 | `docs/research/phase53_source_seed.md`、`docs/research/phase53_research_task_queue.md` | CEK-TA-518 |
| CEK-TA-520 | P0 | done | 生成 Phase 53 知识范围审计 JSON | `docs/audit/phase53_knowledge_scope_for_audit.json` | CEK-TA-519 |
| CEK-TA-521 | P1 | done | 联网采集 5 条 P0 候选知识并运行来源/冲突/乱码门禁 | `codex-expert-kit/rag/candidates/`、`docs/reports/phase53_candidate_generation_report.md` | CEK-TA-520 |
| CEK-TA-522 | P1 | done | 导出 Phase 53 候选 AI 审计包 | `docs/audit/phase53_candidate_audit_package_20260613.json`、`docs/reports/phase53_candidate_quality_gate.json` | CEK-TA-521 |
| CEK-TA-523 | P1 | done | 导入审计结果，按 patch notes 补证、重建或阻断候选 | `docs/reports/phase53_audit_import_report.json`、`ui/public/data/` | CEK-TA-522 |
| CEK-TA-524 | P1 | done | 将通过 reviewed-preparation 的候选沉淀为 formal reviewed/caveat_only 并重建索引；对剩余 AI Security/SBOM 候选导出补证二审包 | `codex-expert-kit/rag/knowledge/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`docs/audit/phase53_ai_security_sbom_supplemental_reaudit_package_20260613.json`、`docs/reports/phase53_ai_security_sbom_supplemental_reaudit_import_report.json` | CEK-TA-523 |
| CEK-TA-525 | P1 | done | 验证 MCP/SearchLab/KnowledgeTree/Vue3 能命中、引用、阻断和正确展示 Phase 53 知识 | `docs/reports/phase53_runtime_linkage_validation_report.json` | CEK-TA-524 |
| CEK-TA-526 | P1 | done | 生成 Phase 53 验收报告并更新任务索引 | `docs/reports/phase53_ai_trade_security_market_conduct_extension_report.md` | CEK-TA-525 |

## Phase 54: 历史 reviewed schema 与候选回链全量回填

目标：补齐历史 formal reviewed/caveat_only 知识卡的 schema v1.1 治理字段，并修复候选到正式知识的 workflow 回链门禁。

任务卡：[tasks/phase54_historical_reviewed_schema_workflow_backfill.md](./tasks/phase54_historical_reviewed_schema_workflow_backfill.md)

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-527 | P0 | done | 创建 Phase 54 任务卡、索引入口和回填契约 | `docs/tasks/phase54_historical_reviewed_schema_workflow_backfill.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-526 |
| CEK-TA-528 | P0 | done | 统计历史 schema v1.1 与 candidate workflow 失败项 | `docs/reports/phase54_backfill_precheck_report.json` | CEK-TA-527 |
| CEK-TA-529 | P0 | done | 实现历史 formal reviewed schema v1.1 字段回填脚本 | `codex-expert-kit/rag/scripts/backfill_phase54_reviewed_schema_v1_1.py`、`docs/reports/phase54_reviewed_schema_backfill_report.json` | CEK-TA-528 |
| CEK-TA-530 | P0 | done | 实现历史 candidate workflow 与 formal knowledge 回链回填脚本 | `codex-expert-kit/rag/scripts/backfill_phase54_candidate_workflow_links.py`、`docs/reports/phase54_candidate_workflow_backfill_report.json` | CEK-TA-529 |
| CEK-TA-531 | P0 | done | 重建正式知识索引、候选 fixture、正式知识 fixture 和知识树范围索引 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/public/data/`、`ui/src/data/` | CEK-TA-530 |
| CEK-TA-532 | P0 | done | 运行 schema/workflow/乱码/知识树/前端构建门禁 | `docs/reports/phase54_validation_report.json` | CEK-TA-531 |
| CEK-TA-533 | P1 | done | 生成 Phase 54 验收报告并更新任务状态 | `docs/reports/phase54_historical_reviewed_schema_workflow_backfill_report.md` | CEK-TA-532 |

## Phase 55: MCP/SearchLab/Vue3 全链路运行时验收与知识库基线

目标：在 Phase 54 清理历史 schema 与候选回链后，固化当前知识库基线，并验证 MCP/SearchLab/Vue3 对正式知识、候选分组、权限阻断和治理语义的读取一致性。

任务卡：[tasks/phase55_runtime_acceptance_baseline.md](./tasks/phase55_runtime_acceptance_baseline.md)

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-534 | P0 | done | 创建 Phase 55 任务卡、索引入口和运行时验收契约 | `docs/tasks/phase55_runtime_acceptance_baseline.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-533 |
| CEK-TA-535 | P0 | done | 生成正式知识库基线统计报告 | `docs/reports/phase55_knowledge_base_baseline_report.json` | CEK-TA-534 |
| CEK-TA-536 | P0 | done | 验证 MCP 只读查询、来源返回和权限阻断 | `docs/reports/phase55_runtime_acceptance_report.json` | CEK-TA-535 |
| CEK-TA-537 | P0 | done | 验证 SearchLab 等价检索命中 AI/Trading 关键知识 | `docs/reports/phase55_runtime_acceptance_report.json` | CEK-TA-536 |
| CEK-TA-538 | P0 | done | 验证 Vue3 KnowledgeTree、候选页和 fixture 数据一致性 | `docs/reports/phase55_runtime_acceptance_report.json` | CEK-TA-537 |
| CEK-TA-539 | P0 | done | 验证 reviewed/approved/default guidance/hard gate 语义一致性 | `docs/reports/phase55_runtime_acceptance_report.json` | CEK-TA-538 |
| CEK-TA-540 | P1 | done | 生成 Phase 55 验收报告并更新任务状态 | `docs/reports/phase55_runtime_acceptance_baseline_report.md` | CEK-TA-539 |

## Phase 56: 外部调用 README 与 MCP 接入文档清晰化

目标：把外部项目调用 CEK-TA 知识库的入口文档补清楚，让使用者能从 README、快速接入手册、MCP spec 和配置模板中完成路径配置、健康检查、只读查询和治理边界理解。

任务卡：[tasks/phase56_external_call_readme_mcp_docs.md](./tasks/phase56_external_call_readme_mcp_docs.md)

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-541 | P0 | done | 创建 Phase 56 任务卡、索引入口和文档契约 | `docs/tasks/phase56_external_call_readme_mcp_docs.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-540 |
| CEK-TA-542 | P0 | done | 重写根 README 快速接入区 | `README.md` | CEK-TA-541 |
| CEK-TA-543 | P0 | done | 新增外部项目 MCP 快速接入手册 | `docs/external_mcp_quickstart.md` | CEK-TA-542 |
| CEK-TA-544 | P0 | done | 更新其他项目接入指南中的 MCP 调用入口和启用时机 | `docs/其他项目接入指南.md` | CEK-TA-543 |
| CEK-TA-545 | P0 | done | 对齐 MCP server spec 到当前运行时能力 | `codex-expert-kit/mcp/mcp_server_spec.md` | CEK-TA-544 |
| CEK-TA-546 | P1 | done | 更新 MCP 配置模板和正式索引 README 的调用说明 | `codex-expert-kit/templates/codex_config_mcp.toml`、`codex-expert-kit/rag/indexes/README.md` | CEK-TA-545 |
| CEK-TA-547 | P1 | done | 运行文档链接、UTF-8、MCP CLI smoke 和 Phase 56 验收报告 | `docs/reports/phase56_external_call_docs_acceptance_report.md` | CEK-TA-546 |

## Phase 57: DogSignal Gate 开源品牌 UI 方案与 HTML 原型

目标：明确 DogSignal Gate 是整体开源项目品牌，MCP/RAG/知识树/候选审计/外部接入只是平台能力模块，并产出适合后续 Vue3 落地的 UI 优化方案和 HTML 原型。

任务卡：[tasks/phase57_dogsignal_gate_open_source_ui_concept.md](./tasks/phase57_dogsignal_gate_open_source_ui_concept.md)

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-548 | P0 | done | 创建 Phase 57 任务卡、索引入口和 UI 原型契约 | `docs/tasks/phase57_dogsignal_gate_open_source_ui_concept.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-547 |
| CEK-TA-549 | P0 | done | 梳理 DogSignal Gate 开源品牌 UI 优化方案 | `docs/ui/dogsignal_gate_ui_optimization_plan.md` | CEK-TA-548 |
| CEK-TA-550 | P0 | done | 产出 DogSignal Gate 审计工作台 HTML 原型 | `docs/prototypes/dogsignal_gate_open_source_ui_concept.html` | CEK-TA-549 |
| CEK-TA-551 | P1 | done | 对齐当前 Vue3 导航、模块命名和后续落地拆分 | `docs/ui/dogsignal_gate_ui_optimization_plan.md` | CEK-TA-550 |
| CEK-TA-552 | P1 | done | 运行 HTML/UTF-8/文案边界验收 | `docs/reports/phase57_dogsignal_gate_ui_concept_report.md` | CEK-TA-551 |

## Phase 58: 回测 / 回放 / 模拟盘 / 实盘等效链条知识补充

目标：补齐 Trading Engineering 中“同一系统内回测、回放、模拟盘和实盘之间的关系与等效条件”知识，明确必须走策略真实链条或字段级等效链条，并通过差异报告证明可比较。

任务卡：[tasks/phase58_backtest_sim_live_equivalence_chain.md](./tasks/phase58_backtest_sim_live_equivalence_chain.md)

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

## Phase 59: Microstructure Feature Store 与 Hybrid Snapshot Contract

目标：补齐 Trading AI 数据架构中“低频 K 线 snapshot、高频 microstructure 原始/聚合数据、训练 dataset snapshot manifest、中央 canonical registry / audit ledger”之间的边界，明确按数据粒度、写入频率、查询模式和审计需求物理分层，再通过 point-in-time manifest 逻辑组合。

任务卡：[tasks/phase59_microstructure_feature_store_hybrid_snapshot.md](./tasks/phase59_microstructure_feature_store_hybrid_snapshot.md)

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-563 | P0 | done | 创建 Phase 59 任务卡与索引入口 | `docs/tasks/phase59_microstructure_feature_store_hybrid_snapshot.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-562 |
| CEK-TA-564 | P0 | done | 搜索专业资料并梳理 feature store、partition evolution、高写入时序存储、kdb+ tick 架构案例 | `docs/research/phase59_microstructure_feature_store_hybrid_snapshot_research.md` | CEK-TA-563 |
| CEK-TA-565 | P0 | done | 定义 Microstructure Feature Store & Hybrid Snapshot Contract | `docs/contracts/phase59_microstructure_feature_store_hybrid_snapshot_contract.md` | CEK-TA-564 |
| CEK-TA-566 | P0 | done | 创建 3 条候选知识卡：物理分层、hybrid dataset manifest、canonical registry 不按 Trader 分库 | `codex-expert-kit/rag/candidates/KB_03_MARKET_MICROSTRUCTURE/cand_20260617_phase59_kline_microstructure_store_separation_001.json`、`codex-expert-kit/rag/candidates/KB_AI_26_DATABASE_STORAGE/cand_20260617_phase59_hybrid_training_dataset_snapshot_manifest_001.json`、`codex-expert-kit/rag/candidates/KB_AI_26_DATABASE_STORAGE/cand_20260617_phase59_canonical_registry_not_per_trader_db_001.json` | CEK-TA-565 |
| CEK-TA-567 | P0 | done | 导出 Phase 59 候选 AI 审计包并运行 JSON/UTF-8/边界质量门禁 | `docs/audit/phase59_microstructure_feature_store_candidate_audit_package_20260617.json`、`docs/reports/phase59_microstructure_feature_store_candidate_quality_gate.json` | CEK-TA-566 |
| CEK-TA-568 | P0 | done | 导入 Phase 59 严格审计结果，三条候选升级为 accepted_for_draft 并按补丁收窄边界 | `docs/audit/audit_result_phase59_microstructure_feature_store_candidate_20260617_strict_v1.json`、`docs/reports/phase59_candidate_audit_import_report.json`、3 条 Phase 59 candidate JSON | CEK-TA-567 |
| CEK-TA-569 | P0 | done | 导出 Phase 59 reviewed/caveat_only 准备审计包，阻止 accepted_for_draft 直接入 formal reviewed | `docs/audit/phase59_reviewed_preparation_audit_package_20260617.json`、`docs/reports/phase59_reviewed_preparation_gap_report.json` | CEK-TA-568 |
| CEK-TA-570 | P0 | done | 导入 Phase 59 reviewed/caveat_only 审计结果，三条候选沉淀为 formal reviewed/caveat_only 并重建索引 | `docs/audit/audit_result_phase59_reviewed_preparation_20260617_strict_v1.json`、`docs/reports/phase59_reviewed_preparation_import_report.json`、`codex-expert-kit/rag/knowledge/KB_03_MARKET_MICROSTRUCTURE/kb_phase59_market_microstructure.kline_microstructure_store_separation_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_AI_26_DATABASE_STORAGE/kb_phase59_database_storage.hybrid_training_dataset_snapshot_manifest_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_AI_26_DATABASE_STORAGE/kb_phase59_database_storage.canonical_registry_not_per_trader_db_required.v1.json`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts` | CEK-TA-569 |

## Phase 60: Sandbox / Replay / Paper Trading 环境治理知识扩展

目标：补齐沙盒、测试网、历史回放、实时模拟执行、模拟盘 / paper trading 和 live canary 的环境边界、证据契约、晋级决策和 gap report，让测试/回放/模拟盘环节能证明系统链条、订单生命周期、风控 rehearsal 和审计追踪，而不是误证明策略收益或实盘许可。

任务卡：[tasks/phase60_sandbox_replay_paper_environment_governance.md](./tasks/phase60_sandbox_replay_paper_environment_governance.md)

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
| CEK-TA-586 | P1 | done | 导入 P1 reviewed/caveat_only 审计结果；3 条已沉淀 formal reviewed/caveat_only，3 条保持 needs_more_evidence，不创建 approved/default guidance/hard gate | `docs/audit/audit_result_phase60_p1_reviewed_preparation_20260618_strict_v1.json`、`codex-expert-kit/rag/scripts/apply_phase60_p1_reviewed_preparation_result.py`、`docs/reports/phase60_p1_reviewed_preparation_import_report.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_phase60_live_execution.adapter_certification.fix_broker_certification_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_phase60_live_execution.paper_account_state.reset_trace_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_phase60_live_execution.environment_health.monitor_required.v1.json`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/public/data/formalKnowledgeItems.json`、`ui/src/data/phase23Candidates.ts`、`ui/public/data/phase23Candidates.json` | CEK-TA-585 |
| CEK-TA-587 | P1 | done | 为 P60-P1-02 / P60-P1-05 / P60-P1-06 补充来源证据并导出 reviewed/caveat_only 补证复审包 | `codex-expert-kit/rag/scripts/prepare_phase60_p1_supplemental_reaudit.py`、`docs/audit/phase60_p1_needs_evidence_supplemental_reaudit_package_20260618.json`、`docs/reports/phase60_p1_needs_evidence_supplemental_reaudit_report.json`、`docs/research/phase60_p1_needs_evidence_supplemental_research.md`、`ui/src/data/phase23Candidates.ts`、`ui/public/data/phase23Candidates.json` | CEK-TA-586 |
| CEK-TA-588 | P1 | done | 导入 P1 needs_more_evidence 补证复审结果，3 条剩余候选均沉淀为 formal reviewed/caveat_only，不创建 approved/default guidance/hard gate | `docs/audit/audit_result_phase60_p1_needs_evidence_supplemental_reaudit_20260618_strict_v1.json`、`codex-expert-kit/rag/scripts/apply_phase60_p1_supplemental_reaudit_result.py`、`docs/reports/phase60_p1_supplemental_reaudit_import_report.json`、`codex-expert-kit/rag/knowledge/KB_05_REPLAY_SIMULATION/kb_phase60_replay_simulation.scenario_library.versioned_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/kb_phase60_risk_management.live_canary.rollback_owner_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_05_REPLAY_SIMULATION/kb_phase60_replay_simulation.environment_drift.monitor_required.v1.json` | CEK-TA-587 |
| CEK-TA-589 | P1 | done | 验证 MCP/SearchLab/KnowledgeTree/Vue3 能检索 Phase 60 P1 全量知识并更新 Phase 60 最终报告 | `codex-expert-kit/rag/scripts/validate_phase60_runtime_linkage.py`、`docs/reports/phase60_runtime_linkage_validation_report.json`、`docs/reports/phase60_sandbox_replay_paper_environment_report.md`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/public/data/formalKnowledgeItems.json`、`ui/src/data/phase23Candidates.ts`、`ui/public/data/phase23Candidates.json`、`ui/public/data/knowledgeTreeScopeIndex.json` | CEK-TA-588 |

## Phase 38: AI 模型平台与交易 Gating/Scoring POC 知识扩展

目标：承接 Phase 36 的模型与训练平台选型方案，把外接交易 LLM gating/scoring 项目继续拆成可采集、可审计、可检索、可被 AI IDE 复用的专业知识子板块。Phase 38 不训练真实模型，先补齐数值 scorer、LLM 审计助手、确定性 final gate、校准阈值、shadow/paper/OPE 和发布治理的知识库与契约。

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-266 | P0 | done | 定义 Phase 38 AI 模型平台与 POC 知识子板块、canonical node 和跨分支路由 | `codex-expert-kit/rag/knowledge_tree.md`、`docs/research/phase38_ai_model_platform_knowledge_scope.md` | CEK-TA-265 |
| CEK-TA-267 | P0 | done | 定义 Numeric Scorer、LLM Audit Assistant、Deterministic Final Gate 的职责与 API 契约 | `docs/contracts/phase38_ai_scoring_gate_runtime_contract.md` | CEK-TA-266 |
| CEK-TA-268 | P0 | done | 定义训练数据、决策时特征、标签、校准集和评估集的数据契约 | `docs/contracts/phase38_training_data_and_eval_contract.md` | CEK-TA-267 |
| CEK-TA-269 | P0 | done | 创建 60-66 条 Phase 38 知识点采集矩阵和 ResearchIngestionTask 队列 | `docs/research/phase38_ai_model_platform_collection_matrix.md`、`docs/research/phase38_ai_model_platform_research_task_queue.md` | CEK-TA-268 |
| CEK-TA-270 | P0 | done | 生成 Phase 38 知识范围审计 JSON，供外部 AI/人工先审计分支、边界和知识点数量 | `docs/audit/phase38_ai_model_platform_knowledge_scope_for_audit.json` | CEK-TA-269 |
| CEK-TA-271 | P1 | done | 联网采集 P0-Core 知识来源，生成候选知识包 | `codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/`、`docs/reports/phase38_p0_core_candidate_generation_report.md` | CEK-TA-270 |
| CEK-TA-272 | P1 | done | 导出 Phase 38 候选 AI 审计包并等待统一审计；needs_more_evidence 补证在审计结果返回后处理 | `docs/audit/phase38_p0_core_candidate_audit_package_20260610.json`、`docs/reports/phase38_p0_core_candidate_quality_gate.json` | CEK-TA-271 |
| CEK-TA-273 | P1 | done | 将通过审计的 Phase 38 候选沉淀为 formal reviewed 知识并重建索引 | `codex-expert-kit/rag/knowledge/KB_AI_20_NUMERIC_SCORING/`、`codex-expert-kit/rag/knowledge/KB_AI_21_CALIBRATION_THRESHOLD/`、`codex-expert-kit/rag/knowledge/KB_AI_22_DECISION_TIME_FEATURES/`、`codex-expert-kit/rag/knowledge/KB_AI_23_LLM_AUDIT_ASSISTANT/`、`codex-expert-kit/rag/knowledge/KB_AI_24_SHADOW_PAPER_OPE/`、`codex-expert-kit/rag/knowledge/KB_AI_25_MODEL_RELEASE_GOVERNANCE/`、`codex-expert-kit/rag/knowledge/KB_10_RAG_ENGINEERING/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts` | CEK-TA-272 |
| CEK-TA-274 | P1 | done | 验证 MCP/SearchLab/KnowledgeTree 能按 Phase 38 子板块检索、引用、阻断和降级 | `codex-expert-kit/rag/scripts/validate_phase38_runtime_linkage.py`、`docs/reports/phase38_runtime_linkage_validation_report.json`、`codex-expert-kit/mcp/tests/`、`codex-expert-kit/api/tests/`、`ui/tests/e2e/` | CEK-TA-273 |
| CEK-TA-275 | P1 | done | 生成 Phase 38 验收报告并更新任务索引 | `docs/reports/phase38_ai_model_platform_poc_knowledge_report.md` | CEK-TA-274 |
| CEK-TA-276 | P1 | done | 导入 Phase 38 P0-Core 严格审计结果，分流 draft、补证和拒绝重建候选 | `docs/audit/audit_result_phase38_p0_core_20260610_strict_v1.json`、`docs/reports/phase38_p0_core_audit_import_report.json` | CEK-TA-272 |
| CEK-TA-277 | P1 | done | 为 Phase 38 P0-Core 7 条 needs_more_evidence 候选补 claim-specific 来源和 CEK-TA 内部契约 | `docs/contracts/phase38_rag_citation_and_reason_taxonomy_contract.md`、`docs/research/phase38_p0_core_supplemental_research.md` | CEK-TA-276 |
| CEK-TA-278 | P1 | done | 导出 Phase 38 P0-Core 补证后二审包，供外部 AI/人工复审 | `docs/audit/phase38_p0_core_supplemental_audit_package_20260610.json` | CEK-TA-277 |
| CEK-TA-279 | P1 | done | 导入 Phase 38 P0-Core 补证二审结果，7 条进入 formal draft 队列，G04-R1 保留补证并修正默认指导元数据 | `docs/audit/audit_result_phase38_p0_core_supplemental_reaudit_20260610_strict_v2.json`、`docs/reports/phase38_p0_core_supplemental_reaudit_import_report.json` | CEK-TA-278 |
| CEK-TA-280 | P1 | done | 为 G04-R1 补充上下文预算、字段白名单、top-k 和显式展开策略证据，并导出三审包 | `docs/research/phase38_g04_context_budget_supplemental_research.md`、`docs/audit/phase38_g04_context_budget_third_audit_package_20260610.json` | CEK-TA-279 |
| CEK-TA-281 | P1 | done | 同步 Phase 38 AI Engineering 子板块到 FastAPI/Vue3 知识树节点，校验候选归类和 UI 可见性 | `codex-expert-kit/api/codex_expert_kit_api/services.py`、`codex-expert-kit/api/tests/`、`docs/reports/phase38_knowledge_tree_ui_node_sync_report.json` | CEK-TA-266 |
| CEK-TA-282 | P1 | done | 导入 G04-R1 三审结果，将其升级为 accepted_for_draft 但继续阻断 reviewed/approved/default guidance/hard gate | `docs/audit/audit_result_phase38_g04_context_budget_third_reaudit_20260610_strict_v3.json`、`docs/reports/phase38_g04_context_budget_third_reaudit_import_report.json`、`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase38_p38_g04_context_budget_field_trimming_001.json` | CEK-TA-280 |
| CEK-TA-283 | P1 | done | 对齐 Phase 38 P0-Extended/P1 剩余采集范围，修正矩阵与队列优先级口径并确认 66 条总量 | `docs/research/phase38_ai_model_platform_collection_matrix.md`、`docs/research/phase38_ai_model_platform_research_task_queue.md`、`docs/reports/phase38_extended_p1_scope_alignment_report.json` | CEK-TA-275 |
| CEK-TA-284 | P1 | done | 联网采集 Phase 38 P0-Extended/P1 来源并生成剩余候选知识包 | `codex-expert-kit/rag/scripts/generate_phase38_extended_p1_candidates.py`、`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/`、`docs/reports/phase38_extended_p1_candidate_generation_report.md` | CEK-TA-283 |
| CEK-TA-285 | P1 | done | 导出 Phase 38 P0-Extended/P1 候选 AI 审计包并运行质量门禁 | `codex-expert-kit/rag/scripts/export_phase38_extended_p1_audit_package.py`、`docs/audit/phase38_extended_p1_candidate_audit_package_20260610.json`、`docs/reports/phase38_extended_p1_candidate_quality_gate.json` | CEK-TA-284 |
| CEK-TA-286 | P1 | done | 导入 Phase 38 P0-Extended/P1 审计结果并按 Phase 32 工作流分流补证、拒绝和 reviewed 沉淀 | `docs/audit/audit_result_phase38_extended_p1_20260610_strict_v1.json`、`docs/reports/phase38_extended_p1_audit_import_report.json`、`codex-expert-kit/rag/scripts/apply_phase38_extended_p1_audit_result.py`、`ui/src/data/phase23Candidates.ts` | CEK-TA-285 |
| CEK-TA-287 | P1 | done | 为 Phase 38 P0-Extended/P1 13 条 needs_more_evidence 和 C10-R1 补充 claim-specific 来源并导出二审包 | `codex-expert-kit/rag/scripts/apply_phase38_extended_p1_supplemental_evidence.py`、`docs/research/phase38_extended_p1_supplemental_research.md`、`docs/audit/phase38_extended_p1_supplemental_audit_package_20260610.json`、`docs/reports/phase38_extended_p1_supplemental_evidence_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-286 |
| CEK-TA-288 | P1 | done | 导入 Phase 38 P0-Extended/P1 补证二审结果，13 条进入 formal draft 队列，B10 保留补证 | `codex-expert-kit/rag/scripts/apply_phase38_extended_p1_supplemental_reaudit_result.py`、`docs/audit/audit_result_phase38_extended_p1_supplemental_reaudit_20260610_strict_v2.json`、`docs/reports/phase38_extended_p1_supplemental_reaudit_import_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-287 |
| CEK-TA-289 | P1 | done | 为 B10 单独补 Bayesian calibration / Bayesian uncertainty calibration 直接来源并导出三审包 | `codex-expert-kit/rag/scripts/apply_phase38_b10_bayesian_calibration_supplement.py`、`docs/research/phase38_b10_bayesian_calibration_supplemental_research.md`、`docs/audit/phase38_b10_bayesian_calibration_third_audit_package_20260610.json`、`docs/reports/phase38_b10_bayesian_calibration_supplement_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-288 |
| CEK-TA-290 | P1 | done | 导入 B10 三审结果，将其升级为 accepted_for_draft，并保留校准层边界、来源去重和治理来源降级说明 | `codex-expert-kit/rag/scripts/apply_phase38_b10_third_reaudit_result.py`、`docs/audit/audit_result_phase38_b10_bayesian_calibration_third_reaudit_20260610_strict_v3.json`、`docs/reports/phase38_b10_bayesian_calibration_third_reaudit_import_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-289 |
| CEK-TA-341 | P1 | done | 将 Phase 38 残留 23 条 ai_passed 候选沉淀为 formal reviewed/caveat_only 知识并重建索引 | `codex-expert-kit/rag/scripts/promote_phase38_ai_passed_candidates_to_reviewed.py`、`docs/reports/phase38_ai_passed_to_reviewed_promotion_report.json`、`codex-expert-kit/rag/knowledge/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-290 |

## Phase 39: 知识树单一数据源与统计对齐

目标：统一 MCP、FastAPI、Vue3 和正式知识索引的知识树节点来源，让 `codex-expert-kit/rag/knowledge_tree.md` 成为唯一结构源，并修复 L1/L2/L3 节点、正式知识数、候选知识数、来源数、缺口数和冲突数的统计口径。

任务卡：[tasks/phase39_knowledge_tree_single_source_stats_alignment.md](./tasks/phase39_knowledge_tree_single_source_stats_alignment.md)

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-291 | P0 | done | 创建 Phase 39 任务卡并登记索引 | `docs/tasks/phase39_knowledge_tree_single_source_stats_alignment.md`、`docs/index_tasks.md`、`docs/tasks/README.md` |
| CEK-TA-292 | P0 | done | 将 FastAPI 知识树节点源切换为 `knowledge_tree.md` 解析结果 | `codex-expert-kit/api/codex_expert_kit_api/services.py`、`codex-expert-kit/api/tests/` |
| CEK-TA-293 | P0 | done | 统一知识节点归类匹配和 legacy alias 兼容 | `codex-expert-kit/api/codex_expert_kit_api/services.py`、`ui/src/stores/auditStore.ts` |
| CEK-TA-294 | P0 | done | 生成 Vue3 知识树 fixture，替代手写静态节点 | `codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py`、`ui/src/data/knowledgeTreeNodes.ts` |
| CEK-TA-295 | P0 | done | 修复 Vue3 知识树统计口径和目录数字显示 | `ui/src/stores/auditStore.ts`、`ui/src/views/KnowledgeTreeView.vue` |
| CEK-TA-296 | P0 | done | 增加知识树覆盖与统计一致性验证脚本 | `codex-expert-kit/rag/scripts/validate_knowledge_tree_alignment.py`、`docs/reports/phase39_knowledge_tree_alignment_report.json` |
| CEK-TA-297 | P1 | done | 运行 FastAPI、Vue3 build 和知识树对齐验收 | `codex-expert-kit/api/tests/`、`ui` build、验收报告 |
| CEK-TA-401 | P0 | done | 修复 Trading Engineering 下 Data Engineering L2 节点缺失和错误 alias，确保 Data Engineering 知识显示在 Trading Engineering 子页面 | `codex-expert-kit/rag/knowledge_tree.md`、`codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py`、`codex-expert-kit/api/codex_expert_kit_api/services.py`、`ui/src/stores/auditStore.ts`、`ui/src/data/knowledgeTreeNodes.ts` |

## Phase 40: AI Continuous Learning 与再训练闭环

目标：补齐 AI Engineering 持续反馈、标签刷新、漂移监控、周期再训练、再校准、champion/challenger、shadow/paper/canary、发布回滚和 LLM prompt/RAG/SFT 闭环知识。

任务卡：[tasks/phase40_ai_continuous_learning_retraining_loop.md](./tasks/phase40_ai_continuous_learning_retraining_loop.md)

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-298 | P0 | done | 创建 Phase 40 任务卡并登记任务索引 | `docs/tasks/phase40_ai_continuous_learning_retraining_loop.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | Phase 39 |
| CEK-TA-299 | P0 | done | 定义 Continuous Learning 知识范围和 L3 专题结构 | `docs/research/phase40_ai_continuous_learning_scope.md`、`codex-expert-kit/rag/knowledge_tree.md` | CEK-TA-298 |
| CEK-TA-300 | P0 | done | 定义反馈日志、标签更新、数据集版本和审计追踪数据契约 | `docs/contracts/phase40_feedback_dataset_contract.md` | CEK-TA-299 |
| CEK-TA-301 | P0 | done | 定义漂移检测、再训练触发、再校准和阈值稳定性契约 | `docs/contracts/phase40_drift_retraining_recalibration_contract.md` | CEK-TA-300 |
| CEK-TA-302 | P0 | done | 定义 champion/challenger、shadow/paper/canary 和 release/rollback 契约 | `docs/contracts/phase40_champion_challenger_release_contract.md` | CEK-TA-301 |
| CEK-TA-303 | P0 | done | 创建 36 条持续学习知识点采集矩阵和 ResearchIngestionTask 队列 | `docs/research/phase40_continuous_learning_collection_matrix.md`、`docs/research/phase40_research_task_queue.md` | CEK-TA-302 |
| CEK-TA-304 | P0 | done | 导出 Phase 40 知识范围审计 JSON，先审计边界、专题和知识点数量 | `docs/audit/phase40_continuous_learning_scope_for_audit.json` | CEK-TA-303 |
| CEK-TA-305 | P1 | done | 联网采集 P0-Core 持续学习知识来源，生成候选知识包 | `codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/`、`docs/research/phase40_*`、`docs/reports/phase40_candidate_generation_report.md` | CEK-TA-304 |
| CEK-TA-306 | P1 | done | 导出候选 AI 审计包并运行来源、冲突、乱码和污染门禁 | `docs/audit/phase40_candidate_audit_package_*.json`、`docs/reports/phase40_candidate_quality_gate.json` | CEK-TA-305 |
| CEK-TA-307 | P1 | done | 按审计结果补证、回写、沉淀 formal reviewed，并重建索引和 Vue3 fixture | `codex-expert-kit/rag/knowledge/KB_AI_18_FEEDBACK_GOVERNANCE/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-306 |
| CEK-TA-308 | P1 | done | 验证 MCP/SearchLab/KnowledgeTree 能按持续学习子板块检索、引用、阻断和降级 | `codex-expert-kit/rag/scripts/validate_phase40_runtime_linkage.py`、`docs/reports/phase40_runtime_linkage_validation_report.json`、`codex-expert-kit/mcp/tests/`、`codex-expert-kit/api/tests/` | CEK-TA-307 |
| CEK-TA-310 | P1 | done | 继续采集 Phase 40 Batch D/E 剩余 18 条持续学习知识点，生成候选知识包 | `codex-expert-kit/rag/scripts/generate_phase40_extended_p1_candidates.py`、`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/`、`docs/research/phase40_batch_d_e_research.md`、`docs/reports/phase40_extended_p1_candidate_generation_report.md` | CEK-TA-308 |
| CEK-TA-311 | P1 | done | 导出 Phase 40 Batch D/E 候选 AI 审计包并运行质量门禁 | `codex-expert-kit/rag/scripts/export_phase40_extended_p1_audit_package.py`、`docs/audit/phase40_extended_p1_candidate_audit_package_20260610.json`、`docs/reports/phase40_extended_p1_candidate_quality_gate.json` | CEK-TA-310 |
| CEK-TA-312 | P1 | done | 导入 Phase 40 Batch D/E 严格审计结果，回写 13 条 accepted_for_draft 与 5 条 needs_more_evidence 候选状态 | `codex-expert-kit/rag/scripts/apply_phase40_extended_p1_audit_result.py`、`docs/audit/audit_result_phase40_extended_p1_batch_de_20260610_strict_v1.json`、`docs/reports/phase40_extended_p1_audit_import_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-311 |
| CEK-TA-313 | P1 | done | 为 Phase 40 Batch D/E 的 5 条 needs_more_evidence 候选补充证据并导出二审 JSON | `codex-expert-kit/rag/scripts/supplement_phase40_extended_p1_needs_evidence.py`、`docs/contracts/phase40_decision_cost_dashboard_metric_contract.md`、`docs/contracts/phase40_composite_release_artifact_contract.md`、`docs/audit/phase40_extended_p1_supplemental_reaudit_package_20260610.json`、`docs/reports/phase40_extended_p1_supplemental_evidence_report.json` | CEK-TA-312 |
| CEK-TA-314 | P1 | done | 导入 Phase 40 Batch D/E 补证二审结果，沉淀 5 条 formal reviewed 知识并重建索引 | `codex-expert-kit/rag/scripts/apply_phase40_extended_p1_supplemental_reaudit_result.py`、`docs/audit/audit_result_phase40_extended_p1_supplemental_reaudit_20260610_strict_v2.json`、`docs/reports/phase40_extended_p1_supplemental_reaudit_to_reviewed_report.json`、`codex-expert-kit/rag/knowledge/KB_AI_18_FEEDBACK_GOVERNANCE/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-313 |
| CEK-TA-309 | P1 | done | 生成 Phase 40 验收报告并更新任务状态 | `docs/reports/phase40_ai_continuous_learning_retraining_loop_report.md` | CEK-TA-314 |
| CEK-TA-315 | P1 | done | 导出 Phase 40 23 条 ai_passed 候选的 reviewed preparation 二审包，解决 formal_knowledge_id 存在但未入正式索引的准入缺口 | `codex-expert-kit/rag/scripts/export_phase40_ai_passed_reviewed_preparation_package.py`、`docs/audit/phase40_ai_passed_reviewed_preparation_audit_package_20260610.json`、`docs/reports/phase40_ai_passed_reviewed_preparation_gap_report.json` | CEK-TA-309 |
| CEK-TA-316 | P1 | done | 导入 Phase 40 reviewed preparation 二审结果，将 reviewed_allowed=true 的候选沉淀为 formal reviewed 并验证 MCP/SearchLab/知识树联动 | `codex-expert-kit/rag/scripts/apply_phase40_ai_passed_reviewed_preparation_result.py`、`docs/audit/audit_result_phase40_ai_passed_reviewed_preparation_20260610_strict_v1.json`、`docs/reports/phase40_ai_passed_reviewed_preparation_import_report.json`、`codex-expert-kit/rag/knowledge/KB_AI_18_FEEDBACK_GOVERNANCE/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-315 |
| CEK-TA-317 | P1 | done | 为 Phase 40 reviewed preparation 二审后仍需补证的 5 条候选补充来源和契约，再导出三审 JSON | `codex-expert-kit/rag/scripts/supplement_phase40_reviewed_preparation_needs_evidence.py`、`docs/contracts/phase40_review_budget_threshold_policy_contract.md`、`docs/contracts/phase40_release_manifest_kill_switch_contract.md`、`docs/research/phase40_reviewed_preparation_supplemental_research.md`、`docs/audit/phase40_reviewed_preparation_supplemental_reaudit_package_20260610.json`、`docs/reports/phase40_reviewed_preparation_supplemental_evidence_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-316 |
| CEK-TA-328 | P1 | done | 导入 Phase 40 reviewed preparation 补证三审结果，沉淀 5 条 formal reviewed 知识并重建索引 | `codex-expert-kit/rag/scripts/apply_phase40_reviewed_preparation_supplemental_reaudit_result.py`、`docs/audit/audit_result_phase40_reviewed_preparation_supplemental_reaudit_20260610_strict_v1.json`、`docs/reports/phase40_reviewed_preparation_supplemental_reaudit_import_report.json`、`codex-expert-kit/rag/knowledge/KB_AI_18_FEEDBACK_GOVERNANCE/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-317 |

## Phase 41: Hybrid Scoring 与 Qwen3 审计助手知识扩展

目标：沿着“表格/统计模型负责数值 scoring，Qwen3/LLM 负责审计解释和 RAG 引用，deterministic final gate 负责最终交易权限”的主线，补齐模型组合、训练数据、校准阈值、Qwen3 审计助手和发布治理知识。

任务卡：[tasks/phase41_hybrid_scoring_qwen3_audit_stack.md](./tasks/phase41_hybrid_scoring_qwen3_audit_stack.md)

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-318 | P0 | done | 创建 Phase 41 任务卡并登记任务索引 | `docs/tasks/phase41_hybrid_scoring_qwen3_audit_stack.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-317 |
| CEK-TA-319 | P0 | done | 定义 Hybrid Scoring Stack 知识范围、L3 专题和跨分支边界 | `docs/research/phase41_hybrid_scoring_qwen3_scope.md`、`codex-expert-kit/rag/knowledge_tree.md` | CEK-TA-318 |
| CEK-TA-320 | P0 | done | 定义表格模型、Qwen3 审计助手、final gate 的组合运行时契约 | `docs/contracts/phase41_hybrid_scoring_runtime_contract.md` | CEK-TA-319 |
| CEK-TA-321 | P0 | done | 定义训练数据、point-in-time feature、标签、校准、阈值和模型 registry 契约 | `docs/contracts/phase41_tabular_llm_training_data_contract.md` | CEK-TA-320 |
| CEK-TA-322 | P0 | done | 创建并按范围审计补丁修正 41 条 Phase 41 知识点采集矩阵和 ResearchIngestionTask 队列 | `docs/research/phase41_hybrid_scoring_collection_matrix.md`、`docs/research/phase41_research_task_queue.md` | CEK-TA-321 |
| CEK-TA-323 | P0 | done | 导出 Phase 41 知识范围审计 JSON，导入范围审计结果并回写补丁 | `docs/audit/phase41_hybrid_scoring_qwen3_scope_for_audit.json`、`docs/audit/audit_result_phase41_hybrid_scoring_qwen3_scope_20260610_strict_v1.json`、`docs/reports/phase41_scope_audit_patch_import_report.json` | CEK-TA-322 |
| CEK-TA-324 | P1 | done | 联网采集 P0-Core 来源，生成候选知识包 | `codex-expert-kit/rag/scripts/generate_phase41_p0_core_candidates.py`、`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase41_*.json`、`docs/research/phase41_p0_core_candidate_research.md`、`docs/reports/phase41_candidate_generation_report.md`、`docs/reports/phase41_candidate_quality_gate.json` | CEK-TA-323 |
| CEK-TA-325 | P1 | done | 导出 Phase 41 候选 AI 审计包并运行来源、冲突、乱码和污染门禁 | `codex-expert-kit/rag/scripts/export_phase41_candidate_audit_package.py`、`docs/audit/phase41_candidate_audit_package_20260610.json`、`docs/reports/phase41_candidate_quality_gate.json` | CEK-TA-324 |
| CEK-TA-326 | P1 | done | 按审计结果补证、回写、沉淀 formal reviewed，并重建索引和 Vue3 fixture；Phase 41 P0-Core 22 条已全部转 formal reviewed/caveat_only，P41-B05 与 P41-D03 二审通过并已入库；approved/default guidance/hard gate 均为 0 | `codex-expert-kit/rag/scripts/apply_phase41_candidate_audit_result.py`、`codex-expert-kit/rag/scripts/apply_phase41_candidate_supplemental_reaudit_result.py`、`codex-expert-kit/rag/scripts/prepare_phase41_a05_r1_third_audit_package.py`、`codex-expert-kit/rag/scripts/apply_phase41_a05_r1_third_audit_result.py`、`codex-expert-kit/rag/scripts/export_phase41_ai_passed_reviewed_preparation_package.py`、`codex-expert-kit/rag/scripts/apply_phase41_reviewed_preparation_result.py`、`codex-expert-kit/rag/scripts/supplement_phase41_reviewed_preparation_needs_evidence.py`、`codex-expert-kit/rag/scripts/apply_phase41_reviewed_preparation_supplemental_reaudit_result.py`、`docs/contracts/phase41_tabular_llm_training_data_contract.md`、`docs/audit/audit_result_phase41_candidate_audit_package_20260610_strict_v1.json`、`docs/audit/audit_result_phase41_candidate_supplemental_reaudit_20260610_strict_v2.json`、`docs/audit/phase41_a05_r1_third_audit_package_20260610.json`、`docs/audit/audit_result_phase41_a05_r1_third_audit_20260610_strict_v3.json`、`docs/audit/phase41_ai_passed_reviewed_preparation_audit_package_20260610.json`、`docs/audit/audit_result_phase41_ai_passed_reviewed_preparation_20260610_strict_v1.json`、`docs/audit/phase41_reviewed_preparation_supplemental_reaudit_package_20260610.json`、`docs/audit/audit_result_phase41_reviewed_preparation_supplemental_reaudit_20260610_strict_v1.json`、`docs/reports/phase41_candidate_audit_import_report.json`、`docs/reports/phase41_candidate_supplemental_reaudit_import_report.json`、`docs/reports/phase41_candidate_remaining_evidence_followups.json`、`docs/reports/phase41_a05_r1_third_audit_preparation_report.md`、`docs/reports/phase41_a05_r1_third_audit_import_report.json`、`docs/reports/phase41_ai_passed_reviewed_preparation_gap_report.json`、`docs/reports/phase41_reviewed_preparation_import_report.json`、`docs/reports/phase41_reviewed_preparation_supplemental_evidence_report.json`、`docs/reports/phase41_reviewed_preparation_supplemental_evidence_report.md`、`docs/reports/phase41_reviewed_preparation_supplemental_reaudit_import_report.json`、`docs/reports/phase41_reviewed_preparation_remaining_followups.json`、`codex-expert-kit/rag/knowledge/KB_AI_20_NUMERIC_SCORING/`、`codex-expert-kit/rag/knowledge/KB_AI_21_CALIBRATION_THRESHOLD/`、`codex-expert-kit/rag/knowledge/KB_AI_22_DECISION_TIME_FEATURES/`、`codex-expert-kit/rag/knowledge/KB_AI_23_LLM_AUDIT_ASSISTANT/`、`codex-expert-kit/rag/knowledge/KB_AI_25_MODEL_RELEASE_GOVERNANCE/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/phase23Candidates.ts`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/knowledgeTreeNodes.ts`、`ui/src/types.ts` | CEK-TA-325 |
| CEK-TA-327 | P1 | done | 验证 MCP/SearchLab/KnowledgeTree 能按 Phase 41 子板块检索、引用、阻断和降级；确认 22 条 Phase 41 formal reviewed 知识可检索、可引用，默认指导检索被 caveat_only 阻断，MCP 写权限被拒绝 | `codex-expert-kit/rag/scripts/validate_phase41_runtime_linkage.py`、`docs/reports/phase41_runtime_linkage_validation_report.json` | CEK-TA-326 |
| CEK-TA-329 | P1 | done | 重新核对 Phase 41 优先级覆盖，确认 P0-Core 22 条已完成，P0-Extended 12 条和 P1 7 条尚未采集，并修正 Phase 41 状态为 doing | `docs/reports/phase41_remaining_scope_alignment_report.json`、`docs/index_tasks.md`、`docs/tasks/README.md`、`docs/tasks/phase41_hybrid_scoring_qwen3_audit_stack.md` | CEK-TA-327 |
| CEK-TA-330 | P1 | done | 联网采集 Phase 41 P0-Extended/P1 剩余 19 条来源并生成候选知识包；本批 P0-Extended 12 条和 P1 7 条统一采集 | `codex-expert-kit/rag/scripts/generate_phase41_extended_p1_candidates.py`、`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/`、`docs/research/phase41_extended_p1_candidate_research.md`、`docs/reports/phase41_extended_p1_candidate_generation_report.md` | CEK-TA-329 |
| CEK-TA-331 | P1 | done | 导出 Phase 41 P0-Extended/P1 候选 AI 审计包并运行来源、冲突、乱码和污染门禁；联合审计包包含 19 条候选，质量门禁 pass | `codex-expert-kit/rag/scripts/export_phase41_extended_p1_audit_package.py`、`docs/audit/phase41_extended_p1_candidate_audit_package_20260610.json`、`docs/reports/phase41_extended_p1_candidate_quality_gate.json` | CEK-TA-330 |
| CEK-TA-332 | P1 | done | 导入 Phase 41 P0-Extended/P1 审计结果，按 Phase 32 工作流分流 accepted、needs_more_evidence、rejected 并完成 6 条补证与二审包导出；本轮不创建 reviewed/approved/default/hard gate | `codex-expert-kit/rag/scripts/apply_phase41_extended_p1_audit_result.py`、`codex-expert-kit/rag/scripts/supplement_phase41_extended_p1_needs_evidence.py`、`docs/audit/audit_result_phase41_extended_p1_candidate_audit_package_20260610_strict_v1.json`、`docs/reports/phase41_extended_p1_audit_import_report.json`、`docs/research/phase41_extended_p1_supplemental_research.md`、`docs/reports/phase41_extended_p1_supplemental_evidence_report.json`、`docs/audit/phase41_extended_p1_supplemental_reaudit_package_20260610.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-331 |
| CEK-TA-333 | P1 | done | 将二审允许的 6 条 Phase 41 P0-Extended/P1 候选沉淀为 formal reviewed/caveat_only，并重建索引、Vue3 fixture 和运行时联动验证；approved/default/hard gate 均保持 0 | `codex-expert-kit/rag/scripts/apply_phase41_extended_p1_supplemental_reaudit_result.py`、`docs/audit/audit_result_phase41_extended_p1_supplemental_reaudit_20260610_strict_v2.json`、`docs/reports/phase41_extended_p1_supplemental_reaudit_import_report.json`、`codex-expert-kit/rag/knowledge/KB_AI_20_NUMERIC_SCORING/`、`codex-expert-kit/rag/knowledge/KB_AI_23_LLM_AUDIT_ASSISTANT/`、`codex-expert-kit/rag/knowledge/KB_AI_25_MODEL_RELEASE_GOVERNANCE/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/`、`docs/reports/phase41_runtime_linkage_validation_report.json` | CEK-TA-332 |
| CEK-TA-335 | P1 | done | 导出 Phase 41 P0-Extended/P1 剩余 13 条 ai_passed 候选 reviewed-preparation 再审计包；本轮只请求 reviewed 许可，不创建 formal reviewed/approved/default/hard gate | `codex-expert-kit/rag/scripts/export_phase41_extended_p1_remaining_reviewed_preparation_package.py`、`docs/audit/phase41_extended_p1_remaining_reviewed_preparation_audit_package_20260610.json`、`docs/reports/phase41_extended_p1_remaining_reviewed_preparation_gap_report.json` | CEK-TA-333 |
| CEK-TA-336 | P1 | done | 导入 Phase 41 剩余 13 条 reviewed-preparation 再审计结果；12 条沉淀为 formal reviewed/caveat_only，P41-A06 修正 slug/formal_knowledge_id 后继续 needs_more_evidence；approved/default/hard gate 均保持 0 | `codex-expert-kit/rag/scripts/apply_phase41_extended_p1_remaining_reviewed_preparation_result.py`、`docs/audit/audit_result_phase41_extended_p1_remaining_reviewed_preparation_20260610_strict_v1.json`、`docs/reports/phase41_extended_p1_remaining_reviewed_preparation_import_report.json`、`docs/reports/phase41_a06_metadata_slug_followup_report.json`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-335 |
| CEK-TA-337 | P1 | done | 为 P41-A06 补充 single-model baseline comparison report 和 auditability impact report，并导出单条三审 JSON；本轮不创建 formal reviewed/approved/default/hard gate | `codex-expert-kit/rag/scripts/prepare_phase41_a06_single_model_baseline_third_audit_package.py`、`docs/research/phase41_a06_ensemble_baseline_auditability_supplemental_research.md`、`docs/audit/phase41_a06_single_model_baseline_third_audit_package_20260611.json`、`docs/reports/phase41_a06_single_model_baseline_third_audit_package_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-336 |
| CEK-TA-338 | P1 | done | 导入 P41-A06 三审结果，只升级候选为 accepted_for_draft，并保持 reviewed/approved/default/hard gate 全部关闭 | `codex-expert-kit/rag/scripts/apply_phase41_a06_third_audit_result.py`、`docs/audit/audit_result_phase41_a06_single_model_baseline_third_audit_20260611_strict_v3.json`、`docs/reports/phase41_a06_third_audit_import_report.json`、`ui/src/data/phase23Candidates.ts` | CEK-TA-337 |
| CEK-TA-339 | P1 | done | 为 P41-A06 生成 reviewed/caveat_only 准备审计包，只请求 formal reviewed 许可；不创建 formal knowledge/approved/default/hard gate | `codex-expert-kit/rag/scripts/export_phase41_a06_reviewed_preparation_package.py`、`docs/audit/phase41_a06_reviewed_preparation_audit_package_20260611.json`、`docs/reports/phase41_a06_reviewed_preparation_gap_report.json` | CEK-TA-338 |
| CEK-TA-340 | P1 | done | 导入 P41-A06 reviewed-preparation 审计结果，创建 formal reviewed/caveat_only 知识并重建索引和 Vue3 fixture；保持 approved/default/hard gate 全部关闭 | `codex-expert-kit/rag/scripts/apply_phase41_a06_reviewed_preparation_result.py`、`docs/audit/audit_result_phase41_a06_reviewed_preparation_20260611_strict_v1.json`、`docs/reports/phase41_a06_reviewed_preparation_import_report.json`、`codex-expert-kit/rag/knowledge/KB_AI_20_NUMERIC_SCORING/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/` | CEK-TA-339 |
| CEK-TA-334 | P1 | done | 验证 Phase 41 全量 41 条目标的 MCP/SearchLab/KnowledgeTree 联动，生成最终验收报告并更新 Phase 状态 | `codex-expert-kit/rag/scripts/validate_phase41_runtime_linkage.py`、`docs/reports/phase41_final_acceptance_report.md` | CEK-TA-340 |

## Phase 42: Database / Data Contract / Storage Engineering for Trading AI

目标：补齐外接交易 AI 项目的数据库、数据契约、存储、审计日志、向量库、迁移、备份恢复和数据生命周期治理知识。

任务卡：[tasks/phase42_database_data_contract_storage_engineering.md](./tasks/phase42_database_data_contract_storage_engineering.md)

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-342 | P0 | done | 创建 Phase 42 任务卡并登记任务索引 | `docs/tasks/phase42_database_data_contract_storage_engineering.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-340 |
| CEK-TA-343 | P0 | done | 定义 Database / Data Contract / Storage Engineering 知识范围、L3 专题和跨分支边界 | `docs/research/phase42_database_storage_scope.md`、`codex-expert-kit/rag/knowledge_tree.md` | CEK-TA-342 |
| CEK-TA-344 | P0 | done | 定义交易 AI 数据库核心表、主键、索引、时间字段、版本字段、审计字段和 append-only 边界契约 | `docs/contracts/phase42_database_storage_contract.md` | CEK-TA-343 |
| CEK-TA-345 | P0 | done | 定义 RAG 文档、chunk、embedding、vector index、citation 和 source provenance 存储契约 | `docs/contracts/phase42_rag_vector_storage_contract.md` | CEK-TA-344 |
| CEK-TA-346 | P0 | done | 创建 34 条 Phase 42 知识点采集矩阵和 ResearchIngestionTask 队列 | `docs/research/phase42_database_storage_collection_matrix.md`、`docs/research/phase42_research_task_queue.md` | CEK-TA-345 |
| CEK-TA-347 | P0 | done | 导出 Phase 42 知识范围审计 JSON，先审计边界、专题、表结构和知识点数量 | `docs/audit/phase42_database_storage_scope_for_audit.json` | CEK-TA-346 |
| CEK-TA-348 | P1 | done | 联网采集 P0 来源，生成候选知识包并运行来源、冲突、乱码和污染门禁 | `codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/`、`docs/research/phase42_p0_candidate_research.md`、`docs/reports/phase42_candidate_generation_report.md`、`docs/reports/phase42_candidate_quality_gate.json` | CEK-TA-347 |
| CEK-TA-349 | P1 | done | 导出 Phase 42 候选 AI 审计包，等待按 Phase 32 工作流处理 accepted、needs_more_evidence、rejected | `docs/audit/phase42_candidate_audit_package_20260611.json`、`docs/reports/phase42_candidate_audit_package_quality_gate.json` | CEK-TA-348 |
| CEK-TA-350 | P1 | done | 按审计结果补证、回写、沉淀 formal reviewed/caveat_only 知识并重建索引和 Vue3 fixture | `docs/audit/audit_result_phase42_candidate_audit_package_20260611_strict_v1.json`、`docs/reports/phase42_candidate_audit_import_report.json`、`docs/audit/phase42_needs_evidence_supplemental_reaudit_package_20260611.json`、`docs/research/phase42_needs_evidence_supplemental_research.md`、`docs/audit/audit_result_phase42_needs_evidence_supplemental_reaudit_20260611_strict_v2.json`、`docs/reports/phase42_supplemental_reaudit_import_report.json`、`docs/reports/phase42_candidates_to_reviewed_promotion_report.json`、`codex-expert-kit/rag/scripts/apply_phase42_supplemental_reaudit_result.py`、`codex-expert-kit/rag/scripts/promote_phase42_accepted_candidates_to_reviewed.py`、`codex-expert-kit/rag/knowledge/KB_AI_26_DATABASE_STORAGE/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-349 |
| CEK-TA-351 | P1 | done | 验证 MCP/SearchLab/KnowledgeTree 能按数据库存储子板块检索、引用、阻断和降级 | `codex-expert-kit/rag/scripts/validate_phase42_runtime_linkage.py`、`docs/reports/phase42_runtime_linkage_validation_report.json` | CEK-TA-350 |
| CEK-TA-352 | P1 | done | 生成 Phase 42 P0 验收报告，明确 P1 6 条仍需继续采集 | `docs/reports/phase42_database_storage_engineering_report.md` | CEK-TA-351 |
| CEK-TA-353 | P1 | done | 联网采集 Phase 42 P1 6 条来源，生成候选知识包并运行来源、冲突、乱码和污染门禁 | `codex-expert-kit/rag/scripts/generate_phase42_p1_candidates.py`、`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/`、`docs/research/phase42_p1_candidate_research.md`、`docs/reports/phase42_p1_candidate_generation_report.md`、`docs/reports/phase42_p1_candidate_quality_gate.json` | CEK-TA-352 |
| CEK-TA-354 | P1 | done | 导出 Phase 42 P1 6 条候选 AI 审计包，等待外部 AI/人工严格审计 | `codex-expert-kit/rag/scripts/export_phase42_p1_candidate_audit_package.py`、`docs/audit/phase42_p1_candidate_audit_package_20260611.json`、`docs/reports/phase42_p1_candidate_audit_package_quality_gate.json` | CEK-TA-353 |
| CEK-TA-355 | P1 | done | 按 Phase 32 工作流处理 P1 审计结果、补证、回写并沉淀 6 条 formal reviewed/caveat_only 知识；不创建 approved、default guidance 或 hard gate | `codex-expert-kit/rag/scripts/apply_phase42_p1_candidate_audit_result.py`、`codex-expert-kit/rag/scripts/apply_phase42_p1_p003_supplemental_reaudit_result.py`、`codex-expert-kit/rag/scripts/apply_phase42_p1_reviewed_preparation_result.py`、`docs/audit/audit_result_phase42_p1_candidate_audit_package_20260611_strict_v1.json`、`docs/reports/phase42_p1_audit_import_report.json`、`docs/research/phase42_p1_p003_supplemental_research.md`、`docs/audit/audit_result_phase42_p1_p003_supplemental_reaudit_20260611_strict_v2.json`、`docs/reports/phase42_p1_p003_supplemental_reaudit_import_report.json`、`docs/audit/phase42_p1_reviewed_preparation_audit_package_20260611.json`、`docs/audit/audit_result_phase42_p1_reviewed_preparation_20260611_strict_v1.json`、`docs/reports/phase42_p1_reviewed_preparation_import_report.json`、`codex-expert-kit/rag/knowledge/KB_AI_26_DATABASE_STORAGE/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts`、`ui/src/data/knowledgeTreeNodes.ts` | CEK-TA-354 |
| CEK-TA-356 | P1 | done | 验证 MCP/SearchLab/KnowledgeTree 能按 Phase 42 P1 子板块检索、引用、阻断和降级 | `codex-expert-kit/rag/scripts/validate_phase42_runtime_linkage.py`、`docs/reports/phase42_runtime_linkage_validation_report.json` | CEK-TA-355 |
| CEK-TA-357 | P1 | done | 生成 Phase 42 全量验收报告并更新 Phase 状态为 done | `docs/reports/phase42_database_storage_engineering_report.md` | CEK-TA-356 |

## Phase 43: External Project AI Memory Layer

目标：为使用 CEK-TA 的外接 AI 项目定义项目记忆层、Memory Contract、Project Memory MCP/API 契约、写入门禁、检索预算、安全治理和 adapter 选型知识。

任务卡：[tasks/phase43_external_project_ai_memory_layer.md](./tasks/phase43_external_project_ai_memory_layer.md)

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-358 | P0 | done | 创建 Phase 43 任务卡并登记任务索引 | `docs/tasks/phase43_external_project_ai_memory_layer.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-357 |
| CEK-TA-359 | P0 | done | 定义 External Project AI Memory 范围、知识树节点和 RAG/Memory 边界 | `docs/research/phase43_external_project_ai_memory_scope.md`、`codex-expert-kit/rag/knowledge_tree.md` | CEK-TA-358 |
| CEK-TA-360 | P0 | done | 定义 MemoryItem schema、memory_event_log、memory_links 和 lifecycle contract | `docs/contracts/phase43_project_memory_contract.md` | CEK-TA-359 |
| CEK-TA-361 | P0 | done | 定义 Project Memory MCP/API 只读与受控写入契约 | `docs/contracts/phase43_project_memory_mcp_api_contract.md` | CEK-TA-360 |
| CEK-TA-362 | P0 | done | 定义 memory write gate、retrieval policy、visibility、supersede 和 context budget 规则 | `docs/contracts/phase43_memory_write_retrieval_policy.md` | CEK-TA-361 |
| CEK-TA-363 | P0 | done | 定义 memory poisoning、prompt injection、secret scan、rollback 和 integrity check 安全规则 | `docs/contracts/phase43_memory_security_governance_contract.md` | CEK-TA-362 |
| CEK-TA-364 | P0 | done | 创建 29 条 AI Memory 知识点采集矩阵和 ResearchIngestionTask 队列 | `docs/research/phase43_memory_collection_matrix.md`、`docs/research/phase43_research_task_queue.md` | CEK-TA-363 |
| CEK-TA-365 | P1 | done | 导出 Phase 43 知识范围审计 JSON，先审计边界、schema、任务数量和 adapter 选型口径 | `docs/audit/phase43_external_project_ai_memory_scope_for_audit.json` | CEK-TA-364 |
| CEK-TA-366 | P1 | done | 联网采集 29 条记忆层知识来源，生成候选知识包并运行来源、冲突、乱码和污染门禁 | `codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/`、`docs/research/phase43_candidate_research.md`、`docs/reports/phase43_candidate_generation_report.md` | CEK-TA-365 |
| CEK-TA-367 | P1 | done | 导出 Phase 43 候选 AI 审计包并按 Phase 32 工作流等待审计结果 | `docs/audit/phase43_candidate_audit_package_20260611.json`、`docs/reports/phase43_candidate_audit_package_quality_gate.json` | CEK-TA-366 |
| CEK-TA-368 | P1 | done | 按审计结果补证、回写、沉淀 formal reviewed/caveat_only 知识并重建索引和 Vue3 fixture | `docs/reports/phase43_candidate_audit_import_report.json`、`docs/audit/phase43_supplemental_reaudit_package_20260611.json`、`docs/reports/phase43_formal_draft_reviewed_import_report.json`、`ui/src/data/` | CEK-TA-367 |
| CEK-TA-369 | P1 | done | 验证 MCP/SearchLab/KnowledgeTree 能按 AI Memory 子板块检索、引用、阻断和降级 | `codex-expert-kit/rag/scripts/validate_phase43_runtime_linkage.py`、`docs/reports/phase43_runtime_linkage_validation_report.json` | CEK-TA-368 |
| CEK-TA-370 | P1 | done | 生成 Phase 43 验收报告并更新 Phase 状态 | `docs/reports/phase43_external_project_ai_memory_layer_report.md` | CEK-TA-369 |

## Phase 44: AI Trader Project Gap Audit

目标：使用当前正式知识库推演一个 AI 交易者项目理论方案，检查数据收集、数据治理、交易分析、AI 训练、持续学习、模拟盘、实盘风控和项目记忆链路中的知识断层。

任务卡：[tasks/phase44_ai_trader_project_gap_audit.md](./tasks/phase44_ai_trader_project_gap_audit.md)

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-371 | P0 | done | 创建 Phase 44 任务卡并登记任务索引 | `docs/tasks/phase44_ai_trader_project_gap_audit.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-370 |
| CEK-TA-372 | P0 | done | 生成 AI 交易者项目方案断层审计任务 JSON，供 AI/人工复核 | `docs/audit/phase44_ai_trader_project_gap_audit_task.json` | CEK-TA-371 |
| CEK-TA-373 | P0 | done | 使用当前正式知识库推演 AI 交易者项目理论方案，并输出知识断层报告 | `docs/reports/phase44_ai_trader_project_gap_audit_report.md` | CEK-TA-372 |
| CEK-TA-374 | P0 | done | 聚焦 AI 层技术底座重新推演业务流拓扑，排除 Trading Engineering 本体断点 | `docs/reports/phase44_ai_layer_business_flow_topology.md` | CEK-TA-373 |

## 首轮执行顺序

第一轮只推进 P0，建议顺序如下：

```text
CEK-TA-000
CEK-TA-001
CEK-TA-002
CEK-TA-003
CEK-TA-006
CEK-TA-007
CEK-TA-022
CEK-TA-023
CEK-TA-024
CEK-TA-010
CEK-TA-013
CEK-TA-014
CEK-TA-016
CEK-TA-027
CEK-TA-033
CEK-TA-037
```

## 第二轮执行顺序

第二轮目标是把框架升级为可复用、可检索、可运营的专业 RAG 知识库。建议顺序如下：

```text
CEK-TA-044
CEK-TA-045
CEK-TA-047
CEK-TA-048
CEK-TA-053
CEK-TA-054
CEK-TA-056
CEK-TA-057
CEK-TA-059
CEK-TA-050
CEK-TA-051
CEK-TA-062
CEK-TA-065
CEK-TA-066
```

## 每个任务的完成标准

```text
1. 交付物文件或目录真实存在。
2. 内容能回链到需求框架中的目标。
3. 如果是知识相关任务，必须包含来源、适用范围、冲突处理规则。
4. 如果是接口相关任务，必须包含输入、输出、错误处理、验证方式。
5. 如果是 Skill 相关任务，必须包含 Use When、Workflow、Output。
6. 如果是 Vue3 相关任务，必须能在界面中审计知识来源和冲突状态。
7. 完成后必须更新本文件中对应任务状态。
```

## 文档入口

| 文档 | 用途 |
| --- | --- |
| `需求框架.md` | 总体愿景、架构、领域设计 |
| `任务需求清单.md` | 需求拆解、任务定义、P0/P1/P2 |
| `知识库采集与审计规范.md` | 联网采集、来源评估、冲突审计 |
| `Vue3知识审计界面需求.md` | 审计工作台产品需求 |
| `其他项目接入指南.md` | 其他项目调用 CEK-TA 的接入规范 |
| `知识倒灌与反哺规范.md` | 其他项目向 CEK-TA 贡献知识的规范 |
| `knowledge_research_backlog.md` | Phase 12 首批专业知识采集主题 backlog |
| `../codex-expert-kit/rag/quality_metrics.md` | Phase 16 知识质量指标体系 |
| `../codex-expert-kit/rag/eval_sets/` | Phase 16 检索、问答、知识树路由评测集 |
| `../codex-expert-kit/templates/knowledge_quality_report.md` | Phase 16 知识质量报告模板 |
| `seed_knowledge_assets_plan.md` | Phase 17 首批真实知识资产范围、来源策略和验收门槛 |
| `reports/seed_knowledge_quality_report.md` | Phase 17 首批真实知识资产质量评测报告 |
| `knowledge_tree_v2_integration_plan.md` | Phase 18 知识树 v2 与 RAG/MCP/Vue3 的兼容改造计划 |
| `tasks/phase19_seed_runtime_validation.md` | Phase 19 Seed 知识 MCP/SearchLab 运行时验证任务卡 |
| `tasks/phase20_searchlab_mcp_runtime_quality.md` | Phase 20 SearchLab MCP 真实运行时与检索质量闭环任务卡 |
| `searchlab_mcp_runtime_contract.md` | Phase 20 SearchLab 调用 MCP runtime 的本地契约 |
| `../codex-expert-kit/rag/eval_sets/runtime_ranking_eval_cases.json` | Phase 20 运行时检索排序质量评测集 |
| `reports/runtime_ranking_quality_report.md` | Phase 20 运行时检索排序质量报告 |
| `reports/searchlab_mcp_runtime_quality_report.md` | Phase 20 SearchLab MCP 运行时质量验收报告 |
| `reports/phase24_candidate_audit_handoff.md` | Phase 24 候选知识审计到 CEK-TA-102 的交接报告 |
| `reports/phase24_vue3_candidate_audit_report.md` | Phase 24 Vue3 候选知识审计工作台验收报告 |
| `reports/phase23_candidate_to_draft_report.md` | Phase 23 CEK-TA-102 候选转正式知识 draft 验收报告 |
| `../codex-expert-kit/rag/scripts/convert_candidates_to_knowledge_drafts.py` | CEK-TA-102 候选知识转正式知识 draft 转换脚本 |
| `tasks/phase25_vue3_playwright_visual_acceptance.md` | Phase 25 Vue3 审计界面 Playwright 实机验收任务卡 |
| `reports/phase25_vue3_playwright_visual_acceptance_report.md` | Phase 25 Vue3 审计界面 Playwright 实机验收报告 |
| `../ui/playwright.config.ts` | Vue3 审计界面 Playwright 实机验收配置 |
| `../ui/tests/e2e/audit-workbench.spec.ts` | Vue3 候选审计、知识树、SearchLab 桌面/移动端验收测试 |
| `tasks/phase26_knowledge_tree_hierarchical_ui.md` | Phase 26 知识树 3 级目录 UI 任务卡 |
| `reports/phase26_knowledge_tree_hierarchical_ui_report.md` | Phase 26 知识树 3 级目录 UI 验收报告 |
| `tasks/phase27_knowledge_tree_reading_ui.md` | Phase 27 知识树阅读体验优化任务卡 |
| `prototypes/knowledge_tree_reading_ui_prototype.html` | Phase 27 知识树阅读型 HTML 原型 |
| `reports/phase27_knowledge_tree_reading_ui_report.md` | Phase 27 知识树阅读体验 Vue3 与 Playwright 验收报告 |
| `tasks/phase28_knowledge_tree_vue_fastapi_delivery.md` | Phase 28 知识树阅读 UI Vue3 与 FastAPI 落地任务卡 |
| `contracts/knowledge_tree_reading_api_contract.md` | Phase 28 KnowledgeTree FastAPI 只读接口契约 |
| `contracts/knowledge_tree_fastapi_runtime_plan.md` | Phase 28 KnowledgeTree FastAPI 服务位置、依赖和 resolver 运行时方案 |
| `reports/phase28_knowledge_tree_vue_fastapi_delivery_report.md` | Phase 28 知识树阅读 UI Vue3 与 FastAPI 落地验收报告 |
| `tasks/phase29_candidate_audit_readability_workbench.md` | Phase 29 候选知识人工审核阅读体验优化任务卡 |
| `contracts/candidate_audit_readability_contract.md` | Phase 29 候选审核页阅读体验、审核 checklist、handoff 和只读错误契约 |
| `reports/phase29_candidate_audit_readability_report.md` | Phase 29 候选知识人工审核阅读体验优化验收报告 |
| `tasks/phase30_candidate_ai_audit_package_export.md` | Phase 30 候选知识 AI 审计包导出任务卡 |
| `contracts/candidate_ai_audit_package_contract.md` | Phase 30 AI 审计包 JSON 契约 |
| `tasks/phase31_candidate_ai_audit_result_backwrite.md` | Phase 31 候选知识 AI 审计结果回写任务卡 |
| `contracts/candidate_ai_audit_result_backwrite_contract.md` | Phase 31 AI 审计结果回写契约 |
| `audit/phase31_candidate_ai_audit_result_20260609.json` | Phase 31 外部 AI 审计结果结构化记录 |
| `reports/phase31_candidate_ai_audit_result_backwrite_report.md` | Phase 31 候选知识 AI 审计结果回写验收报告 |
| `tasks/phase32_candidate_to_reviewed_workflow.md` | Phase 32 候选到 reviewed 知识的批量审计工作流任务卡 |
| `tasks/phase34_knowledge_item_schema_v1_1.md` | Phase 34 知识卡片 Schema v1.1 与默认指导门禁升级任务卡 |
| `contracts/knowledge_item_schema_v1_1_contract.md` | Phase 34 KnowledgeItem Schema v1.1、LLM 使用策略和 machine_gate 契约 |
| `research/phase34_recommended_extra_sources_queue.md` | Phase 34 推荐补充来源待核验队列 |
| `reports/phase34_knowledge_item_schema_v1_1_report.md` | Phase 34 知识卡片 Schema v1.1 验收报告 |
| `tasks/phase35_external_ai_active_retrieval_protocol.md` | Phase 35 外部项目 AI 主动检索协议任务卡 |
| `contracts/external_ai_active_retrieval_protocol.md` | Phase 35 外部项目 AI 主动检索协议 |
| `../codex-expert-kit/templates/external_project_active_retrieval_AGENTS.md` | Phase 35 外部项目 AGENTS 主动检索模板 |
| `../codex-expert-kit/templates/external_project_active_retrieval_test_plan.md` | Phase 35 主动检索测试计划 |
| `../codex-expert-kit/mcp/tests/test_external_ai_active_retrieval_protocol.py` | Phase 35 主动检索协议 pytest |
| `tasks/phase36_ai_engineering_gating_scoring_knowledge.md` | Phase 36 AI Engineering 交易 LLM Gating/Scoring 知识扩展任务卡 |
| `research/phase36_ai_engineering_knowledge_framework.md` | Phase 36 AI Engineering 知识树扩展框架 |
| `contracts/ai_engineering_gating_scoring_contract.md` | Phase 36 外接 LLM gating/scoring 业务流和边界契约 |
| `contracts/ai_engineering_knowledge_item_policy.md` | Phase 36 AI Engineering 知识卡 claim_type、llm_usage_policy 和 machine_gate 策略 |
| `research/phase36_ai_engineering_p0_collection_matrix.md` | Phase 36 AI Engineering 分层知识点采集矩阵 |
| `research/phase36_ai_engineering_research_task_queue.md` | Phase 36 AI Engineering ResearchIngestionTask 队列 |
| `reports/phase36_ai_engineering_collection_report.md` | Phase 36 首批 AI Engineering P0-Core 候选采集报告 |
| `reports/phase36_ai_engineering_full_candidate_generation_report.md` | Phase 36 AI Engineering 113 条候选知识补齐报告 |
| `reports/phase36_ai_engineering_candidate_quality_gate.json` | Phase 36 首批候选质量门禁报告 |
| `audit/phase36_ai_engineering_candidate_audit_package_20260609.json` | Phase 36 首批 AI Engineering 候选 AI/人工审计包 |
| `audit/phase36_ai_engineering_batches/` | Phase 36 AI Engineering 113 条候选知识的 10 份分批审计包 |
| `audit/audit_result_phase36_ai_engineering_batch_01_of_10_20260609_gpt55_pro.json` | Phase 36 AI Engineering 第一批候选外部审计结果 |
| `reports/phase36_batch_01_audit_import_report.json` | Phase 36 AI Engineering 第一批审计结果导入与 reviewed 沉淀报告 |
| `research/phase36_capability_boundary_supplemental_research.md` | Phase 36 第一批 needs_more_evidence 能力边界候选补证采集记录 |
| `audit/phase36_capability_boundary_supplemental_audit_package_20260609.json` | Phase 36 两条能力边界候选补证后二次审计包 |
| `audit/audit_result_phase36_capability_boundary_supplemental_reaudit_20260609_gpt55_pro.json` | Phase 36 第一批能力边界补证二次审计结果 |
| `reports/audit_result_phase36_capability_boundary_supplemental_reaudit_20260609_gpt55_pro_import_report.json` | Phase 36 第一批能力边界补证二审导入与 reviewed 沉淀报告 |
| `audit/audit_result_phase36_ai_engineering_batch_02_of_10_20260609_gpt55_pro_strict_sources.json` | Phase 36 AI Engineering 第二批候选外部审计结果 |
| `reports/phase36_batch_02_audit_import_report.json` | Phase 36 AI Engineering 第二批审计结果导入与 reviewed 沉淀报告 |
| `research/phase36_batch02_supplemental_research.md` | Phase 36 第二批 needs_more_evidence 候选补证采集记录 |
| `audit/phase36_batch02_supplemental_audit_package_20260609.json` | Phase 36 第二批 2 条 needs_more_evidence 候选补证后二次审计包 |
| `audit/audit_result_phase36_batch02_supplemental_reaudit_20260609_gpt55_pro_strict_sources.json` | Phase 36 第二批补证二次审计结果 |
| `reports/audit_result_phase36_batch02_supplemental_reaudit_20260609_gpt55_pro_strict_sources_import_report.json` | Phase 36 第二批补证二审导入与 reviewed 沉淀报告 |
| `audit/audit_result_phase36_ai_engineering_batch_03_of_10_20260609_gpt55_pro_strict_sources.json` | Phase 36 AI Engineering 第三批候选外部审计结果 |
| `reports/phase36_batch_03_audit_import_report.json` | Phase 36 AI Engineering 第三批审计结果导入与 reviewed 沉淀报告 |
| `research/phase36_batch03_supplemental_research.md` | Phase 36 第三批 needs_more_evidence 候选补证采集记录 |
| `audit/phase36_batch03_supplemental_audit_package_20260609.json` | Phase 36 第三批 5 条 needs_more_evidence 候选补证后二次审计包 |
| `audit/audit_result_phase36_batch03_supplemental_reaudit_20260609_gpt55_pro_strict_sources.json` | Phase 36 第三批补证二次审计结果 |
| `reports/audit_result_phase36_batch03_supplemental_reaudit_20260609_gpt55_pro_strict_sources_import_report.json` | Phase 36 第三批补证二审导入与 reviewed 沉淀报告 |
| `audit/audit_result_phase36_ai_engineering_batch_04_of_10_20260609_gpt55_pro_strict_sources.json` | Phase 36 AI Engineering 第四批候选外部审计结果 |
| `reports/phase36_batch_04_audit_import_report.json` | Phase 36 AI Engineering 第四批审计结果导入与 reviewed 沉淀报告 |
| `research/phase36_batch04_false_allow_supplemental_research.md` | Phase 36 第四批 false allow needs_more_evidence 候选补证采集记录 |
| `audit/phase36_batch04_false_allow_supplemental_audit_package_20260609.json` | Phase 36 第四批 false allow 候选补证后二次审计包 |
| `audit/audit_result_phase36_batch04_false_allow_supplemental_reaudit_20260609_gpt55_pro_strict_sources.json` | Phase 36 第四批 false allow 补证二次审计结果 |
| `reports/audit_result_phase36_batch04_false_allow_supplemental_reaudit_20260609_gpt55_pro_strict_sources_import_report.json` | Phase 36 第四批 false allow 补证二审导入与 reviewed 沉淀报告 |
| `audit/audit_result_phase36_ai_engineering_batch_05_of_10_20260609_gpt55_pro_strict_sources.json` | Phase 36 AI Engineering 第五批候选外部审计结果 |
| `reports/phase36_batch_05_audit_import_report.json` | Phase 36 AI Engineering 第五批审计结果导入与 reviewed 沉淀报告 |
| `research/phase36_batch05_good_loss_bad_win_supplemental_research.md` | Phase 36 第五批 good_loss/bad_win needs_more_evidence 候选补证采集记录 |
| `audit/phase36_batch05_good_loss_bad_win_supplemental_audit_package_20260609.json` | Phase 36 第五批 good_loss/bad_win 候选补证后二次审计包 |
| `audit/audit_result_phase36_batch05_good_loss_bad_win_supplemental_reaudit_20260609_gpt55_pro_strict_sources.json` | Phase 36 第五批 good_loss/bad_win 补证二次审计结果 |
| `reports/audit_result_phase36_batch05_good_loss_bad_win_supplemental_reaudit_20260609_gpt55_pro_strict_sources_import_report.json` | Phase 36 第五批 good_loss/bad_win 补证二审导入与 reviewed 沉淀报告 |
| `audit/audit_result_phase36_ai_engineering_batch_06_of_10_20260609_gpt55_pro_strict_sources.json` | Phase 36 AI Engineering 第六批候选外部审计结果 |
| `reports/phase36_batch_06_audit_import_report.json` | Phase 36 AI Engineering 第六批审计结果导入与 reviewed 沉淀报告 |
| `research/phase36_batch06_llm_judge_preference_pair_supplemental_research.md` | Phase 36 第六批 llm_judge/preference_pair needs_more_evidence 候选补证采集记录 |
| `audit/phase36_batch06_llm_judge_preference_pair_supplemental_audit_package_20260609.json` | Phase 36 第六批 llm_judge/preference_pair 候选补证后二次审计包 |
| `audit/audit_result_phase36_batch06_llm_judge_preference_pair_supplemental_reaudit_20260609_gpt55_pro_strict_sources.json` | Phase 36 第六批 llm_judge/preference_pair 补证二次审计结果 |
| `reports/audit_result_phase36_batch06_llm_judge_preference_pair_supplemental_reaudit_20260609_gpt55_pro_strict_sources_import_report.json` | Phase 36 第六批 llm_judge/preference_pair 补证二审导入与 reviewed 沉淀报告 |
| `audit/audit_result_phase36_ai_engineering_batch_07_of_10_20260609_gpt55_pro_strict_sources.json` | Phase 36 AI Engineering 第七批候选外部审计结果 |
| `reports/phase36_batch_07_audit_import_report.json` | Phase 36 AI Engineering 第七批审计结果导入与 reviewed 沉淀报告 |
| `research/phase36_batch07_rag_parameter_risk_ledger_supplemental_research.md` | Phase 36 第七批 rag_no_hit/research_feedback/risk_ledger needs_more_evidence 候选补证采集记录 |
| `audit/phase36_batch07_rag_parameter_risk_ledger_supplemental_audit_package_20260609.json` | Phase 36 第七批 rag_no_hit/research_feedback/risk_ledger 候选补证后二次审计包 |
| `audit/audit_result_phase36_batch07_rag_parameter_risk_ledger_supplemental_reaudit_20260609_gpt55_pro_strict_sources.json` | Phase 36 第七批 rag_no_hit/research_feedback/risk_ledger 补证二次审计结果 |
| `reports/audit_result_phase36_batch07_rag_parameter_risk_ledger_supplemental_reaudit_20260609_gpt55_pro_strict_sources_import_report.json` | Phase 36 第七批 rag_no_hit/research_feedback/risk_ledger 补证二审导入与 reviewed 沉淀报告 |
| `audit/audit_result_phase36_ai_engineering_batch_08_of_10_20260609_gpt55_pro_strict_sources.json` | Phase 36 AI Engineering 第八批候选外部审计结果 |
| `reports/phase36_batch_08_audit_import_report.json` | Phase 36 AI Engineering 第八批审计结果导入与 reviewed 沉淀报告 |
| `contracts/ai_engineering_scoring_rubric_dimension_contract.md` | Phase 36 AI Engineering scoring rubric 细分维度边界契约 |
| `research/phase36_batch08_scoring_rubric_supplemental_research.md` | Phase 36 第八批 5 条 scoring_rubric needs_more_evidence 候选补证采集记录 |
| `audit/phase36_batch08_scoring_rubric_supplemental_audit_package_20260609.json` | Phase 36 第八批 5 条 scoring_rubric 候选补证后二次审计包 |
| `audit/audit_result_phase36_batch08_scoring_rubric_supplemental_reaudit_20260609_gpt55_pro_strict_sources.json` | Phase 36 第八批 5 条 scoring_rubric 补证二次审计结果 |
| `reports/audit_result_phase36_batch08_scoring_rubric_supplemental_reaudit_20260609_gpt55_pro_strict_sources_import_report.json` | Phase 36 第八批 5 条 scoring_rubric 补证二审导入与 reviewed 沉淀报告 |
| `audit/audit_result_phase36_ai_engineering_batch_09_of_10_20260609_gpt55_pro_strict_sources.json` | Phase 36 AI Engineering 第九批候选外部审计结果 |
| `reports/phase36_batch_09_audit_import_report.json` | Phase 36 AI Engineering 第九批审计结果导入与 reviewed 沉淀报告 |
| `research/phase36_batch09_sft_trade_data_supplemental_research.md` | Phase 36 第九批 5 条 SFT/trade_candidate/trade_data needs_more_evidence 候选补证采集记录 |
| `audit/phase36_batch09_sft_trade_data_supplemental_audit_package_20260609.json` | Phase 36 第九批 5 条 SFT/trade_candidate/trade_data 候选补证后二次审计包 |
| `audit/audit_result_phase36_batch09_sft_trade_data_supplemental_reaudit_20260609_gpt55_pro_strict_sources.json` | Phase 36 第九批 SFT/trade_candidate/trade_data 补证二次审计结果 |
| `reports/audit_result_phase36_batch09_sft_trade_data_supplemental_reaudit_20260609_gpt55_pro_strict_sources_import_report.json` | Phase 36 第九批 SFT/trade_candidate/trade_data 二审导入与 reviewed 沉淀报告 |
| `audit/audit_result_phase36_ai_engineering_batch_10_of_10_20260609_gpt55_pro_strict_sources.json` | Phase 36 AI Engineering 第十批候选外部审计结果 |
| `reports/phase36_batch_10_audit_import_report.json` | Phase 36 AI Engineering 第十批审计结果导入与 reviewed 沉淀报告 |
| `research/phase36_batch10_strategy_training_example_supplemental_research.md` | Phase 36 第十批 4 条 strategy_version/training_example needs_more_evidence 候选补证采集记录 |
| `audit/phase36_batch10_strategy_training_example_supplemental_audit_package_20260609.json` | Phase 36 第十批 4 条 strategy_version/training_example 候选补证后二次审计包 |
| `audit/audit_result_phase36_batch10_strategy_training_example_supplemental_reaudit_20260609_gpt55_pro_strict_sources.json` | Phase 36 第十批 strategy_version/training_example 补证二次审计结果 |
| `reports/audit_result_phase36_batch10_strategy_training_example_supplemental_reaudit_20260609_gpt55_pro_strict_sources_import_report.json` | Phase 36 第十批 strategy_version/training_example 二审导入与 reviewed 沉淀报告 |
| `reports/phase36_ai_engineering_completion_audit_report.md` | Phase 36 AI Engineering 113 条知识点完整性复审报告 |
| `research/phase36_ai_engineering_model_platform_selection_proposal.md` | Phase 36 AI Engineering 模型与训练平台选型审计融合方案 |
| `reports/phase36_ai_engineering_review_handoff_report.md` | Phase 36 候选转 reviewed 前的审计结果交接与阻断说明 |
| `../codex-expert-kit/rag/scripts/generate_phase36_ai_engineering_candidates.py` | Phase 36 AI Engineering 候选知识批量生成脚本 |
| `../codex-expert-kit/rag/scripts/split_phase36_ai_audit_package.py` | Phase 36 AI Engineering 候选审计包拆分脚本 |
| `../codex-expert-kit/rag/scripts/import_phase36_batch_audit_result.py` | Phase 36 AI Engineering 分批审计结果导入与 reviewed 知识生成脚本 |
| `../codex-expert-kit/rag/scripts/validate_no_mojibake.py` | UTF-8 中文内容和前端 fixture 乱码门禁脚本 |
| `tasks/phase37_trading_engineering_knowledge_expansion.md` | Phase 37 Trading Engineering 专业知识库扩展任务卡 |
| `research/phase37_trading_engineering_knowledge_scope.md` | Phase 37 Trading Engineering 96 条 P0 知识点范围 |
| `audit/phase37_trading_engineering_knowledge_scope_for_audit.json` | Phase 37 Trading Engineering 知识范围审计 JSON |
| `contracts/trading_ai_cross_branch_knowledge_contract.md` | Phase 37 Trading 与 AI 跨分支引用契约 |
| `research/phase37_trading_engineering_research_task_queue.md` | Phase 37 Trading Engineering ResearchIngestionTask 队列 |
| `reports/phase37_trading_engineering_knowledge_expansion_report.md` | Phase 37 Trading Engineering 96 条 P0 知识全量验收报告 |
| `reports/phase37_full_runtime_linkage_report.json` | Phase 37 全量 MCP/SearchLab/KnowledgeTree/Vue3 联动验证报告 |
| `../codex-expert-kit/rag/scripts/validate_phase37_full_runtime_linkage.py` | Phase 37 全量 96 条 formal reviewed/caveat_only 运行时验证脚本 |
| `reports/phase37_trading_engineering_post_completion_gap_audit_report.md` | Phase 37 Trading Engineering P0 完成后的外部专业资料对照缺口审计报告 |
| `tasks/phase45_trading_engineering_p1_completion.md` | Phase 45 Trading Engineering P1/P2 专业知识补全任务卡 |
| `research/phase45_trading_engineering_p1_knowledge_scope.md` | Phase 45 Trading Engineering P1/P2 知识范围 |
| `research/phase45_trading_engineering_p1_research_task_queue.md` | Phase 45 Trading Engineering P1/P2 ResearchIngestionTask 队列 |
| `research/phase45_trading_engineering_p1_source_seed.md` | Phase 45 Trading Engineering P1/P2 来源种子库 |
| `contracts/phase45_trading_engineering_p1_runtime_contract.md` | Phase 45 Trading Engineering P1/P2 运行时与跨分支契约 |
| `audit/phase45_trading_engineering_p1_knowledge_scope_for_audit.json` | Phase 45 Trading Engineering P1/P2 知识范围审计 JSON |
| `../codex-expert-kit/rag/scripts/generate_phase45_execution_tca_candidates.py` | Phase 45 Execution TCA 6 条候选知识生成脚本 |
| `../codex-expert-kit/rag/scripts/export_phase45_execution_tca_candidate_audit_package.py` | Phase 45 Execution TCA 候选审计包导出脚本 |
| `research/phase45_execution_tca_candidate_research.md` | Phase 45 Execution TCA 候选知识采集来源记录 |
| `reports/phase45_execution_tca_candidate_generation_report.md` | Phase 45 Execution TCA 候选知识生成报告 |
| `reports/phase45_execution_tca_candidate_quality_gate.json` | Phase 45 Execution TCA 候选质量门禁 |
| `audit/phase45_execution_tca_candidate_audit_package_20260612.json` | Phase 45 Execution TCA 6 条候选外部严格审计包 |
| `reports/phase45_execution_tca_candidate_audit_package_quality_gate.json` | Phase 45 Execution TCA 审计包质量门禁 |
| `../codex-expert-kit/rag/scripts/apply_phase45_execution_tca_candidate_audit_result.py` | Phase 45 Execution TCA 首轮审计结果导入、2 条补证和二审包导出脚本 |
| `audit/audit_phase45_execution_tca_p45_a_20260612_external_strict_v1.json` | Phase 45 Execution TCA 首轮严格审计结果归档，4 条 accepted_for_draft、2 条 needs_more_evidence |
| `reports/phase45_execution_tca_audit_import_report.json` | Phase 45 Execution TCA 首轮审计导入和补证处理报告 |
| `research/phase45_execution_tca_supplemental_research.md` | Phase 45 Execution TCA TCA03/TCA06 补证来源记录 |
| `audit/phase45_execution_tca_supplemental_reaudit_package_20260612.json` | Phase 45 Execution TCA 2 条补证候选二审包 |
| `reports/phase45_execution_tca_supplemental_reaudit_package_quality_gate.json` | Phase 45 Execution TCA 补证二审包质量门禁 |
| `../codex-expert-kit/rag/scripts/apply_phase45_execution_tca_supplemental_reaudit_result.py` | Phase 45 Execution TCA 二审结果导入与 6 条 reviewed/caveat_only 准备审计包导出脚本 |
| `audit/audit_phase45_execution_tca_supplemental_reaudit_20260612_v1.json` | Phase 45 Execution TCA TCA03/TCA06 二审结果归档，2 条 accepted_for_draft |
| `reports/phase45_execution_tca_supplemental_reaudit_import_report.json` | Phase 45 Execution TCA 二审结果导入报告 |
| `audit/phase45_execution_tca_reviewed_preparation_audit_package_20260612.json` | Phase 45 Execution TCA 6 条 accepted_for_draft 候选 reviewed/caveat_only 准备审计包 |
| `reports/phase45_execution_tca_reviewed_preparation_gap_report.json` | Phase 45 Execution TCA reviewed/caveat_only 准备包缺口与质量门禁 |
| `../codex-expert-kit/rag/scripts/apply_phase45_execution_tca_reviewed_preparation_result.py` | Phase 45 Execution TCA reviewed/caveat_only 准备审计结果导入和 formal knowledge 沉淀脚本 |
| `audit/audit_phase45_execution_tca_reviewed_caveat_only_preparation_20260612_v1.json` | Phase 45 Execution TCA 6 条候选 reviewed/caveat_only 准备审计结果归档 |
| `reports/phase45_execution_tca_import_report.json` | Phase 45 Execution TCA 6 条候选沉淀为 formal reviewed/caveat_only 的导入报告 |
| `../codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/` | Phase 45 Execution TCA Live Execution formal reviewed/caveat_only 知识 |
| `../codex-expert-kit/rag/knowledge/KB_07_TRADE_ANALYSIS/` | Phase 45 Execution TCA Trade Analysis formal reviewed/caveat_only 知识 |
| `../codex-expert-kit/rag/scripts/generate_phase45_trade_audit_candidates.py` | Phase 45 Audit Trail / Clock Sync 6 条候选知识生成脚本 |
| `../codex-expert-kit/rag/scripts/export_phase45_trade_audit_candidate_audit_package.py` | Phase 45 Audit Trail / Clock Sync 候选审计包导出脚本 |
| `research/phase45_trade_audit_candidate_research.md` | Phase 45 Audit Trail / Clock Sync 候选知识采集来源记录 |
| `reports/phase45_trade_audit_candidate_generation_report.md` | Phase 45 Audit Trail / Clock Sync 候选知识生成报告 |
| `reports/phase45_trade_audit_candidate_quality_gate.json` | Phase 45 Audit Trail / Clock Sync 候选质量门禁 |
| `audit/phase45_trade_audit_candidate_audit_package_20260612.json` | Phase 45 Audit Trail / Clock Sync 6 条候选外部严格审计包 |
| `reports/phase45_trade_audit_candidate_audit_package_quality_gate.json` | Phase 45 Audit Trail / Clock Sync 审计包质量门禁 |
| `../codex-expert-kit/rag/scripts/apply_phase45_trade_audit_candidate_audit_result.py` | Phase 45 Audit Trail / Clock Sync 首轮审计结果导入、2 条补证和二审包导出脚本 |
| `audit/audit_phase45_trade_audit_p45_b_20260612_external_strict_v1.json` | Phase 45 Audit Trail / Clock Sync 首轮严格审计结果归档，4 条 accepted_for_draft、2 条 needs_more_evidence |
| `reports/phase45_trade_audit_import_report.json` | Phase 45 Audit Trail / Clock Sync 首轮审计导入和补证处理报告 |
| `research/phase45_trade_audit_supplemental_research.md` | Phase 45 Audit Trail / Clock Sync AUD04/AUD05 补证来源记录 |
| `audit/phase45_trade_audit_supplemental_reaudit_package_20260612.json` | Phase 45 Audit Trail / Clock Sync 2 条补证候选二审包 |
| `reports/phase45_trade_audit_supplemental_reaudit_package_quality_gate.json` | Phase 45 Audit Trail / Clock Sync 补证二审包质量门禁 |
| `contracts/phase45_trade_audit_clock_sync_contract.md` | Phase 45 Audit Trail / Clock Sync 内部字段契约、schema extract 和 owner 边界 |
| `../codex-expert-kit/rag/scripts/apply_phase45_trade_audit_supplemental_reaudit_result.py` | Phase 45 Audit Trail / Clock Sync 二审结果导入与 reviewed/caveat_only 准备包导出脚本 |
| `audit/audit_phase45_trade_audit_supplemental_reaudit_20260612_v1.json` | Phase 45 Audit Trail / Clock Sync AUD04/AUD05 二审结果归档，2 条 accepted_for_draft |
| `reports/phase45_trade_audit_supplemental_reaudit_import_report.json` | Phase 45 Audit Trail / Clock Sync 二审结果导入报告 |
| `audit/phase45_trade_audit_reviewed_preparation_audit_package_20260612.json` | Phase 45 Audit Trail / Clock Sync 6 条 accepted_for_draft 候选 reviewed/caveat_only 准备审计包 |
| `reports/phase45_trade_audit_reviewed_preparation_gap_report.json` | Phase 45 Audit Trail / Clock Sync reviewed/caveat_only 准备包缺口与质量门禁 |
| `../codex-expert-kit/rag/scripts/apply_phase45_trade_audit_reviewed_preparation_result.py` | Phase 45 Audit Trail / Clock Sync reviewed/caveat_only 准备审计结果导入和 formal knowledge 沉淀脚本 |
| `audit/audit_phase45_trade_audit_reviewed_caveat_only_preparation_20260612_v1.json` | Phase 45 Audit Trail / Clock Sync 6 条候选 reviewed/caveat_only 准备审计结果归档 |
| `reports/phase45_trade_audit_formal_import_report.json` | Phase 45 Audit Trail / Clock Sync 6 条候选沉淀为 formal reviewed/caveat_only 的导入报告 |
| `../codex-expert-kit/rag/knowledge/KB_02_DATA_ENGINEERING/` | Phase 45 Audit Trail / Clock Sync Data Engineering formal reviewed/caveat_only 知识 |
| `../codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/` | Phase 45 Audit Trail / Clock Sync Live Execution formal reviewed/caveat_only 知识 |
| `../codex-expert-kit/rag/knowledge/KB_AI_26_DATABASE_STORAGE/` | Phase 45 Audit Trail / Clock Sync Database/Storage formal reviewed/caveat_only 知识 |
| `../codex-expert-kit/rag/scripts/generate_phase45_layered_risk_candidates.py` | Phase 45 Layered Risk / Credit / Margin 6 条候选知识生成脚本 |
| `../codex-expert-kit/rag/scripts/export_phase45_layered_risk_candidate_audit_package.py` | Phase 45 Layered Risk / Credit / Margin 候选审计包导出脚本 |
| `research/phase45_layered_risk_candidate_research.md` | Phase 45 Layered Risk / Credit / Margin 候选知识采集来源记录 |
| `reports/phase45_layered_risk_candidate_generation_report.json` | Phase 45 Layered Risk / Credit / Margin 候选知识生成报告 |
| `reports/phase45_layered_risk_candidate_quality_gate.json` | Phase 45 Layered Risk / Credit / Margin 候选质量门禁 |
| `audit/phase45_layered_risk_candidate_audit_package_20260612.json` | Phase 45 Layered Risk / Credit / Margin 6 条候选外部严格审计包 |
| `reports/phase45_layered_risk_candidate_audit_package_quality_gate.json` | Phase 45 Layered Risk / Credit / Margin 审计包质量门禁 |
| `../codex-expert-kit/rag/scripts/apply_phase45_layered_risk_candidate_audit_result.py` | Phase 45 Layered Risk / Credit / Margin 首轮审计结果回写与 RISK05 补证脚本 |
| `audit/audit_phase45_layered_risk_p45_c_20260612_external_strict_v1.json` | Phase 45 Layered Risk / Credit / Margin 首轮外部严格审计结果归档 |
| `reports/phase45_layered_risk_audit_import_report.json` | Phase 45 Layered Risk / Credit / Margin 首轮审计回写报告 |
| `research/phase45_layered_risk_supplemental_research.md` | Phase 45 Layered Risk / Credit / Margin RISK05 补证来源记录 |
| `audit/phase45_layered_risk_supplemental_reaudit_package_20260612.json` | Phase 45 Layered Risk / Credit / Margin RISK05 二审补证包 |
| `reports/phase45_layered_risk_supplemental_reaudit_package_quality_gate.json` | Phase 45 Layered Risk / Credit / Margin RISK05 二审补证包质量门禁 |
| `../codex-expert-kit/rag/scripts/apply_phase45_layered_risk_supplemental_reaudit_result.py` | Phase 45 Layered Risk / Credit / Margin RISK05 二审结果回写与 reviewed preparation 包导出脚本 |
| `audit/audit_phase45_layered_risk_supplemental_reaudit_20260612_v1.json` | Phase 45 Layered Risk / Credit / Margin RISK05 二审结果归档 |
| `contracts/phase45_layered_risk_controls_contract.md` | Phase 45 Layered Risk / Credit / Margin reviewed 前内部字段契约 |
| `audit/phase45_layered_risk_reviewed_preparation_audit_package_20260612.json` | Phase 45 Layered Risk / Credit / Margin 6 条候选 reviewed/caveat_only 准备审计包 |
| `reports/phase45_layered_risk_supplemental_reaudit_import_report.json` | Phase 45 Layered Risk / Credit / Margin 二审回写报告 |
| `reports/phase45_layered_risk_reviewed_preparation_gap_report.json` | Phase 45 Layered Risk / Credit / Margin reviewed preparation 包门禁报告 |
| `../codex-expert-kit/rag/scripts/apply_phase45_layered_risk_reviewed_preparation_result.py` | Phase 45 Layered Risk / Credit / Margin reviewed/caveat_only 准备审计结果落库脚本 |
| `audit/audit_phase45_layered_risk_reviewed_caveat_only_preparation_20260612_v1.json` | Phase 45 Layered Risk / Credit / Margin reviewed/caveat_only 准备审计结果归档 |
| `reports/phase45_layered_risk_formal_import_report.json` | Phase 45 Layered Risk / Credit / Margin formal reviewed/caveat_only 落库报告 |
| `../codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/kb_phase45_layered_risk.layered_pre_trade_controls_required.v1.json` | Phase 45 Layered Risk formal reviewed 知识：分层 pre-trade controls |
| `../codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/kb_phase45_layered_risk.credit_limit_not_strategy_risk_limit.v1.json` | Phase 45 Layered Risk formal reviewed 知识：credit limit 与策略风险边界 |
| `../codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/kb_phase45_layered_risk.max_order_size_and_price_collar_required.v1.json` | Phase 45 Layered Risk formal reviewed 知识：最大订单量与价格 collar |
| `../codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/kb_phase45_layered_risk.message_throttle_and_cancel_rate_controls.v1.json` | Phase 45 Layered Risk formal reviewed 知识：消息节流与撤单率控制 |
| `../codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/kb_phase45_layered_risk.margin_collateral_available_funds_boundary.v1.json` | Phase 45 Layered Risk formal reviewed 知识：margin/collateral/available funds 边界 |
| `../codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/kb_phase45_layered_risk.post_trade_surveillance_not_pre_trade_gate.v1.json` | Phase 45 Layered Risk formal reviewed 知识：post-trade surveillance 与 pre-trade gate 边界 |
| `research/phase37_quant_foundation_candidate_research.md` | Phase 37 Quant Foundation 首批 12 条候选研究记录 |
| `reports/phase37_trading_tree_mapping_report.md` | Phase 37 Trading 分支知识树映射检查报告 |
| `reports/phase37_trading_collection_report.md` | Phase 37 首批 Trading Engineering P0 候选采集报告 |
| `reports/phase37_quant_foundation_candidate_quality_gate.json` | Phase 37 Quant Foundation 候选质量门禁 |
| `audit/phase37_quant_foundation_candidate_audit_package_20260611.json` | Phase 37 Quant Foundation 首批候选审计包 |
| `../codex-expert-kit/rag/scripts/generate_phase37_quant_foundation_candidates.py` | Phase 37 Quant Foundation 候选、审计包和质量门禁生成脚本 |
| `audit/audit_result_phase37_quant_foundation_candidate_audit_20260611_strict_v1.json` | Phase 37 Quant Foundation 首轮严格审计结果归档 |
| `reports/phase37_quant_foundation_audit_import_report.json` | Phase 37 Quant Foundation 首轮审计结果导入报告 |
| `research/phase37_quant_foundation_supplemental_research.md` | Phase 37 Quant Foundation 3 条 needs_more_evidence 补证研究记录 |
| `reports/phase37_quant_foundation_supplemental_evidence_report.json` | Phase 37 Quant Foundation 补证执行报告 |
| `audit/phase37_quant_foundation_supplemental_reaudit_package_20260611.json` | Phase 37 Quant Foundation 3 条补证候选二审包 |
| `reports/phase37_quant_foundation_supplemental_reaudit_quality_gate.json` | Phase 37 Quant Foundation 补证二审包质量门禁 |
| `../codex-expert-kit/rag/scripts/apply_phase37_quant_foundation_audit_result.py` | Phase 37 Quant Foundation 首轮审计结果导入脚本 |
| `../codex-expert-kit/rag/scripts/supplement_phase37_quant_foundation_needs_evidence.py` | Phase 37 Quant Foundation needs_more_evidence 补证与二审包导出脚本 |
| `audit/audit_result_phase37_quant_foundation_supplemental_reaudit_20260611_strict_v1.json` | Phase 37 Quant Foundation 3 条补证候选二审结果归档，2 条 accepted_for_draft、1 条继续 needs_more_evidence |
| `reports/phase37_quant_foundation_supplemental_reaudit_import_report.json` | Phase 37 Quant Foundation 二审结果导入报告 |
| `../codex-expert-kit/rag/scripts/apply_phase37_quant_foundation_supplemental_reaudit_result.py` | Phase 37 Quant Foundation 二审结果导入脚本 |
| `../codex-expert-kit/rag/scripts/export_phase37_quant_foundation_reviewed_preparation_package.py` | Phase 37 Quant Foundation reviewed/caveat_only 准备审计包导出脚本 |
| `audit/phase37_quant_foundation_reviewed_preparation_audit_package_20260611.json` | Phase 37 Quant Foundation 12 条 accepted_for_draft 候选 reviewed/caveat_only 准备审计包 |
| `reports/phase37_quant_foundation_reviewed_preparation_gap_report.json` | Phase 37 Quant Foundation reviewed/caveat_only 准备审计质量门禁报告 |
| `audit/phase37_quant_foundation_reviewed_preparation_audit_result_20260611_strict_v2.json` | Phase 37 Quant Foundation reviewed-preparation 严格审计结果，9 条 accepted_for_reviewed_caveat_only、3 条 needs_more_evidence |
| `../codex-expert-kit/rag/scripts/apply_phase37_quant_foundation_reviewed_preparation_result.py` | Phase 37 Quant Foundation reviewed-preparation 审计结果导入、formal reviewed 沉淀和补证分流脚本 |
| `reports/phase37_quant_foundation_reviewed_preparation_import_report.json` | Phase 37 Quant Foundation 9 条 formal reviewed/caveat_only 沉淀和 3 条补证分流报告 |
| `../codex-expert-kit/rag/knowledge/KB_01_QUANT_FOUNDATION/` | Phase 37 Quant Foundation formal reviewed/caveat_only 知识目录 |
| `../codex-expert-kit/rag/scripts/generate_phase37_data_engineering_candidates.py` | Phase 37 Data Engineering 12 条候选知识、研究记录和质量门禁生成脚本 |
| `../codex-expert-kit/rag/scripts/export_phase37_data_engineering_candidate_audit_package.py` | Phase 37 Data Engineering 候选严格审计包导出脚本 |
| `../codex-expert-kit/rag/candidates/KB_02_DATA_ENGINEERING/` | Phase 37 Data Engineering 12 条 candidate_ready 候选知识目录 |
| `research/phase37_data_engineering_candidate_research.md` | Phase 37 Data Engineering 候选来源、分类和边界研究记录 |
| `reports/phase37_data_engineering_candidate_generation_report.md` | Phase 37 Data Engineering 候选生成报告 |
| `reports/phase37_data_engineering_candidate_quality_gate.json` | Phase 37 Data Engineering 候选来源、分类、冲突、边界和 UTF-8 质量门禁 |
| `audit/phase37_data_engineering_candidate_audit_package_20260611.json` | Phase 37 Data Engineering 12 条候选外部 AI/人工严格审计包 |
| `reports/phase37_data_engineering_candidate_audit_package_quality_gate.json` | Phase 37 Data Engineering 候选审计包质量门禁 |
| `../codex-expert-kit/rag/scripts/apply_phase37_data_engineering_audit_result.py` | Phase 37 Data Engineering 首轮严格审计结果导入脚本 |
| `audit/audit_result_phase37_data_engineering_candidate_audit_20260611_strict_v1.json` | Phase 37 Data Engineering 首轮严格审计结果归档，12 条 accepted_for_draft |
| `audit/audit_result_phase37_data_engineering_candidate_audit_20260611_strict_v1_schema_patched.json` | Phase 37 Data Engineering 首轮严格审计结果 schema patched 归档，修正 confidence 枚举 |
| `audit/meta_audit_result_phase37_data_engineering_candidate_audit_20260611_strict_v1.json` | Phase 37 Data Engineering 首轮审计结果 meta-audit，确认 12 条决策维持并要求 schema patch |
| `reports/phase37_data_engineering_audit_import_report.json` | Phase 37 Data Engineering 首轮审计结果导入与候选分流报告 |
| `../codex-expert-kit/rag/scripts/export_phase37_data_engineering_reviewed_preparation_package.py` | Phase 37 Data Engineering reviewed/caveat_only 准备审计包导出脚本 |
| `audit/phase37_data_engineering_reviewed_preparation_audit_package_20260611.json` | Phase 37 Data Engineering 12 条 accepted_for_draft 候选 reviewed/caveat_only 准备审计包 |
| `reports/phase37_data_engineering_reviewed_preparation_gap_report.json` | Phase 37 Data Engineering reviewed-preparation 缺口与质量门禁报告 |
| `audit/audit_result_phase37_data_engineering_reviewed_preparation_20260611_strict_v1.json` | Phase 37 Data Engineering reviewed-preparation 严格审计结果，10 条允许 formal reviewed/caveat_only，2 条 needs_more_evidence |
| `../codex-expert-kit/rag/scripts/apply_phase37_data_engineering_reviewed_preparation_result.py` | Phase 37 Data Engineering reviewed-preparation 审计结果导入、formal reviewed 沉淀和补证分流脚本 |
| `reports/phase37_data_engineering_reviewed_preparation_import_report.json` | Phase 37 Data Engineering 10 条 formal reviewed/caveat_only 沉淀和 2 条补证分流报告 |
| `../codex-expert-kit/rag/knowledge/KB_02_DATA_ENGINEERING/` | Phase 37 Data Engineering formal reviewed/caveat_only 知识目录，当前 10 条 |
| `../codex-expert-kit/rag/scripts/supplement_phase37_data_engineering_blocked_candidates.py` | Phase 37 Data Engineering D10/D11 reviewed 阻断项补证与再审包导出脚本 |
| `contracts/phase37_data_engineering_dataset_layers_contract.md` | Phase 37 Data Engineering raw/cleaned/adjusted/feature-ready/label-ready 数据层契约 |
| `research/phase37_data_engineering_blocked_supplemental_research.md` | Phase 37 Data Engineering D10/D11 补证研究记录 |
| `audit/phase37_data_engineering_blocked_supplemental_reaudit_package_20260611.json` | Phase 37 Data Engineering D10/D11 reviewed 阻断项补证二审包 |
| `reports/phase37_data_engineering_blocked_supplemental_reaudit_report.json` | Phase 37 Data Engineering D10/D11 补证质量门禁与导出报告 |
| `../codex-expert-kit/rag/scripts/apply_phase37_data_engineering_blocked_supplemental_reaudit_result.py` | Phase 37 Data Engineering D10/D11 补证二审结果导入脚本 |
| `audit/audit_result_phase37_data_engineering_blocked_supplemental_reaudit_20260611_strict_v1.json` | Phase 37 Data Engineering D10/D11 补证二审结果归档，D10 reviewed/caveat_only，D11 needs_more_evidence |
| `reports/phase37_data_engineering_blocked_supplemental_reaudit_import_report.json` | Phase 37 Data Engineering D10 formal reviewed 沉淀与 D11 继续补证分流报告 |
| `../codex-expert-kit/rag/knowledge/KB_02_DATA_ENGINEERING/kb_02_data_engineering.outlier_detection_required.v1.json` | Phase 37 Data Engineering D10 formal reviewed/caveat_only 知识 |
| `../codex-expert-kit/rag/scripts/supplement_phase37_data_engineering_d11_contract_inline_third_audit.py` | Phase 37 Data Engineering D11 契约内联三审补证脚本 |
| `research/phase37_data_engineering_d11_contract_inline_third_audit_research.md` | Phase 37 Data Engineering D11 契约内联三审补证研究记录 |
| `audit/phase37_data_engineering_d11_contract_inline_third_audit_package_20260611.json` | Phase 37 Data Engineering D11 契约正文与 lineage 来源内联三审包 |
| `reports/phase37_data_engineering_d11_contract_inline_third_audit_report.json` | Phase 37 Data Engineering D11 契约内联三审包质量门禁报告 |
| `../codex-expert-kit/rag/scripts/apply_phase37_data_engineering_d11_contract_inline_third_audit_result.py` | Phase 37 Data Engineering D11 契约内联三审结果导入与 formal reviewed/caveat_only 沉淀脚本 |
| `audit/audit_result_phase37_data_engineering_d11_contract_inline_third_audit_20260611_strict_v1.json` | Phase 37 Data Engineering D11 契约内联三审结果归档，允许 formal reviewed/caveat_only |
| `reports/phase37_data_engineering_d11_contract_inline_third_audit_import_report.json` | Phase 37 Data Engineering D11 formal reviewed/caveat_only 沉淀报告 |
| `../codex-expert-kit/rag/knowledge/KB_02_DATA_ENGINEERING/kb_02_data_engineering.raw_vs_adjusted_data_boundary.v1.json` | Phase 37 Data Engineering D11 formal reviewed/caveat_only 知识 |
| `../codex-expert-kit/rag/scripts/generate_phase37_kline_strategy_candidates.py` | Phase 37 Kline / Strategy Engineering 12 条候选知识生成脚本 |
| `../codex-expert-kit/rag/scripts/export_phase37_kline_strategy_candidate_audit_package.py` | Phase 37 Kline / Strategy Engineering 候选严格审计包导出脚本 |
| `../codex-expert-kit/rag/candidates/KB_02_KLINE_STRATEGY/` | Phase 37 Kline / Strategy Engineering candidate_ready 候选知识目录 |
| `research/phase37_kline_strategy_candidate_research.md` | Phase 37 Kline / Strategy Engineering 候选来源、分类和边界研究记录 |
| `reports/phase37_kline_strategy_candidate_generation_report.md` | Phase 37 Kline / Strategy Engineering 候选生成报告 |
| `reports/phase37_kline_strategy_candidate_quality_gate.json` | Phase 37 Kline / Strategy Engineering 候选来源、分类、冲突、边界和 UTF-8 质量门禁 |
| `audit/phase37_kline_strategy_candidate_audit_package_20260611.json` | Phase 37 Kline / Strategy Engineering 12 条候选外部 AI/人工严格审计包 |
| `reports/phase37_kline_strategy_candidate_audit_package_quality_gate.json` | Phase 37 Kline / Strategy Engineering 候选审计包质量门禁 |
| `../codex-expert-kit/rag/scripts/apply_phase37_kline_strategy_audit_result.py` | Phase 37 Kline / Strategy Engineering 首轮严格审计结果导入脚本 |
| `audit/audit_result_phase37_kline_strategy_candidate_audit_20260611_strict_v1.json` | Phase 37 Kline / Strategy Engineering 首轮严格审计结果归档，8 条 accepted_for_draft、4 条 needs_more_evidence |
| `reports/phase37_kline_strategy_audit_import_report.json` | Phase 37 Kline / Strategy Engineering 首轮审计导入与候选分流报告 |
| `../codex-expert-kit/rag/scripts/supplement_phase37_kline_strategy_needs_evidence.py` | Phase 37 Kline / Strategy Engineering 4 条 needs_more_evidence 候选补证与二审包导出脚本 |
| `research/phase37_kline_strategy_supplemental_research.md` | Phase 37 Kline / Strategy Engineering K04/K05/K10/K12 补证来源、边界和质量门禁记录 |
| `audit/phase37_kline_strategy_supplemental_reaudit_package_20260611.json` | Phase 37 Kline / Strategy Engineering 4 条补证候选二审包 |
| `reports/phase37_kline_strategy_supplemental_reaudit_report.json` | Phase 37 Kline / Strategy Engineering 补证二审包导出报告 |
| `../codex-expert-kit/rag/scripts/apply_phase37_kline_strategy_supplemental_reaudit_result.py` | Phase 37 Kline / Strategy Engineering 补证二审结果导入脚本 |
| `audit/audit_result_phase37_kline_strategy_supplemental_reaudit_20260611_strict_v1.json` | Phase 37 Kline / Strategy Engineering 补证二审结果归档，4 条 accepted_for_draft |
| `reports/phase37_kline_strategy_supplemental_reaudit_import_report.json` | Phase 37 Kline / Strategy Engineering 补证二审结果导入报告 |
| `../codex-expert-kit/rag/scripts/export_phase37_kline_strategy_reviewed_preparation_package.py` | Phase 37 Kline / Strategy Engineering 12 条 ai_passed 候选 reviewed/caveat_only 准备审计包导出脚本 |
| `audit/phase37_kline_strategy_reviewed_preparation_audit_package_20260611.json` | Phase 37 Kline / Strategy Engineering 12 条候选 reviewed/caveat_only 准备审计包 |
| `reports/phase37_kline_strategy_reviewed_preparation_gap_report.json` | Phase 37 Kline / Strategy Engineering reviewed-preparation 缺口与质量门禁报告 |
| `../codex-expert-kit/rag/scripts/apply_phase37_kline_strategy_reviewed_preparation_result.py` | Phase 37 Kline / Strategy Engineering reviewed-preparation 审计结果导入与 12 条 formal reviewed/caveat_only 沉淀脚本 |
| `audit/audit_result_phase37_kline_strategy_reviewed_preparation_20260611_strict_v1.json` | Phase 37 Kline / Strategy Engineering 12 条候选 reviewed-preparation 严格复审计结果，全部允许 formal reviewed/caveat_only |
| `reports/phase37_kline_strategy_reviewed_preparation_import_report.json` | Phase 37 Kline / Strategy Engineering 12 条候选沉淀为 formal reviewed/caveat_only 的导入报告 |
| `../codex-expert-kit/rag/knowledge/KB_02_KLINE_STRATEGY/` | Phase 37 Kline / Strategy Engineering 正式 reviewed/caveat_only 知识目录，含本轮新增 12 条 |
| `../codex-expert-kit/rag/scripts/generate_phase37_backtest_candidates.py` | Phase 37 Backtest / 回测可信度 12 条 candidate_ready 候选生成脚本 |
| `../codex-expert-kit/rag/scripts/export_phase37_backtest_candidate_audit_package.py` | Phase 37 Backtest / 回测可信度候选严格审计包导出脚本 |
| `../codex-expert-kit/rag/candidates/KB_04_BACKTEST/` | Phase 37 Backtest / 回测可信度候选知识目录，本轮新增 12 条 |
| `research/phase37_backtest_candidate_research.md` | Phase 37 Backtest / 回测可信度候选来源、分类和边界研究记录 |
| `reports/phase37_backtest_candidate_generation_report.md` | Phase 37 Backtest / 回测可信度候选生成报告 |
| `reports/phase37_backtest_candidate_quality_gate.json` | Phase 37 Backtest / 回测可信度候选来源、分类、冲突、边界和 UTF-8 质量门禁 |
| `audit/phase37_backtest_candidate_audit_package_20260611.json` | Phase 37 Backtest / 回测可信度 12 条候选外部 AI/人工严格审计包 |
| `reports/phase37_backtest_candidate_audit_package_quality_gate.json` | Phase 37 Backtest / 回测可信度候选审计包质量门禁 |
| `../codex-expert-kit/rag/scripts/create_phase37_backtest_audit_result_from_report.py` | Phase 37 Backtest 首轮 Markdown 审计报告转 UTF-8 JSON 审计结果脚本 |
| `../codex-expert-kit/rag/scripts/apply_phase37_backtest_audit_result.py` | Phase 37 Backtest 首轮严格审计结果导入脚本 |
| `../codex-expert-kit/rag/scripts/export_phase37_backtest_reviewed_preparation_package.py` | Phase 37 Backtest reviewed/caveat_only 准备审计包导出脚本 |
| `audit/audit_result_phase37_backtest_candidate_audit_20260611_strict_v1.json` | Phase 37 Backtest 首轮严格审计结果归档，12 条 accepted_for_draft |
| `reports/phase37_backtest_audit_import_report.json` | Phase 37 Backtest 首轮审计结果导入与候选分流报告 |
| `reports/phase37_backtest_no_supplement_needed_report.json` | Phase 37 Backtest 无 needs_more_evidence 候选，补证链路 no-op 报告 |
| `audit/phase37_backtest_reviewed_preparation_audit_package_20260611.json` | Phase 37 Backtest 12 条 accepted_for_draft 候选 reviewed/caveat_only 准备审计包 |
| `reports/phase37_backtest_reviewed_preparation_gap_report.json` | Phase 37 Backtest reviewed-preparation 缺口与质量门禁报告 |
| `../codex-expert-kit/rag/scripts/apply_phase37_backtest_reviewed_preparation_result.py` | Phase 37 Backtest reviewed-preparation 审计结果导入、formal reviewed 沉淀和补证分流脚本 |
| `audit/audit_result_phase37_backtest_reviewed_preparation_20260611_strict_v1.json` | Phase 37 Backtest reviewed-preparation 严格审计结果，9 条允许 formal reviewed/caveat_only，3 条 needs_more_evidence |
| `reports/phase37_backtest_reviewed_preparation_import_report.json` | Phase 37 Backtest 9 条 formal reviewed/caveat_only 沉淀和 3 条补证分流报告 |
| `../codex-expert-kit/rag/knowledge/KB_04_BACKTEST/` | Phase 37 Backtest formal reviewed/caveat_only 知识目录，当前本轮新增 9 条，B10/B11/B12 待补证 |
| `../codex-expert-kit/rag/scripts/supplement_phase37_backtest_reviewed_blocked_candidates.py` | Phase 37 Backtest B10/B11/B12 reviewed 阻断项补证与再审包导出脚本 |
| `contracts/phase37_backtest_run_manifest_contract.md` | Phase 37 Backtest run manifest、metric_report、reproducibility_package 和 versioning 字段契约 |
| `research/phase37_backtest_reviewed_blocked_supplemental_research.md` | Phase 37 Backtest B10/B11/B12 补证研究记录 |
| `audit/phase37_backtest_reviewed_blocked_supplemental_reaudit_package_20260611.json` | Phase 37 Backtest B10/B11/B12 补证再审包 |
| `reports/phase37_backtest_reviewed_blocked_supplemental_report.json` | Phase 37 Backtest B10/B11/B12 补证质量门禁与导出报告 |
| `../codex-expert-kit/rag/scripts/create_phase37_backtest_blocked_supplemental_reaudit_result_from_report.py` | Phase 37 Backtest B10/B11/B12 补证再审 Markdown 结论转 UTF-8 JSON 审计结果脚本 |
| `../codex-expert-kit/rag/scripts/apply_phase37_backtest_reviewed_blocked_supplemental_result.py` | Phase 37 Backtest B10 formal reviewed/caveat_only 沉淀与 B11/B12 继续补证分流脚本 |
| `audit/audit_result_phase37_backtest_reviewed_blocked_supplemental_reaudit_20260611_strict_v1.json` | Phase 37 Backtest B10/B11/B12 补证再审结果归档，B10 允许 formal reviewed/caveat_only，B11/B12 仍需内联契约补证 |
| `reports/phase37_backtest_reviewed_blocked_supplemental_import_report.json` | Phase 37 Backtest B10 formal reviewed/caveat_only 沉淀与 B11/B12 继续补证导入报告 |
| `../codex-expert-kit/rag/knowledge/KB_04_BACKTEST/kb_04_backtest.profit_factor_drawdown_context_required.v1.json` | Phase 37 Backtest B10 formal reviewed/caveat_only 知识 |
| `../codex-expert-kit/rag/scripts/supplement_phase37_backtest_b11_b12_inline_contract.py` | Phase 37 Backtest B11/B12 内联 backtest_run_manifest contract/schema extract 并导出下一轮再审包脚本 |
| `contracts/phase37_backtest_run_manifest_schema_extract.json` | Phase 37 Backtest run manifest 结构化字段表、required/optional 标记、owner 映射和 contract sha256 |
| `research/phase37_backtest_b11_b12_inline_contract_research.md` | Phase 37 Backtest B11/B12 内联契约补证研究记录 |
| `audit/phase37_backtest_b11_b12_inline_contract_reaudit_package_20260611.json` | Phase 37 Backtest B11/B12 内联契约再审包 |
| `reports/phase37_backtest_b11_b12_inline_contract_report.json` | Phase 37 Backtest B11/B12 内联契约补证质量门禁和导出报告 |
| `../codex-expert-kit/rag/scripts/create_phase37_backtest_b11_b12_inline_contract_reaudit_result_from_report.py` | Phase 37 Backtest B11/B12 内联契约再审 Markdown 结论转 UTF-8 JSON 审计结果脚本 |
| `../codex-expert-kit/rag/scripts/apply_phase37_backtest_b11_b12_inline_contract_result.py` | Phase 37 Backtest B11/B12 内联契约再审结果导入和 formal reviewed/caveat_only 沉淀脚本 |
| `audit/audit_result_phase37_backtest_b11_b12_inline_contract_reaudit_20260611_strict_v1.json` | Phase 37 Backtest B11/B12 内联契约再审结果归档，2 条均允许 formal reviewed/caveat_only |
| `reports/phase37_backtest_b11_b12_inline_contract_import_report.json` | Phase 37 Backtest B11/B12 formal reviewed/caveat_only 沉淀导入报告 |
| `../codex-expert-kit/rag/knowledge/KB_04_BACKTEST/kb_04_backtest.reproducibility_package_required.v1.json` | Phase 37 Backtest B11 formal reviewed/caveat_only 知识 |
| `../codex-expert-kit/rag/knowledge/KB_04_BACKTEST/kb_04_backtest.strategy_version_and_data_version_required.v1.json` | Phase 37 Backtest B12 formal reviewed/caveat_only 知识 |
  | `tasks/phase38_ai_model_platform_poc_knowledge.md` | Phase 38 AI 模型平台与交易 Gating/Scoring POC 知识扩展任务卡 |
| `research/phase38_ai_model_platform_knowledge_scope.md` | Phase 38 AI 模型平台与 POC 知识子板块、canonical node 和范围文档 |
| `contracts/phase38_ai_scoring_gate_runtime_contract.md` | Phase 38 Numeric Scorer、LLM Audit Assistant 和 Deterministic Final Gate 运行时契约 |
| `contracts/phase38_training_data_and_eval_contract.md` | Phase 38 训练数据、决策时特征、标签、校准集和评估集契约 |
| `research/phase38_ai_model_platform_collection_matrix.md` | Phase 38 66 条 AI 模型平台知识点采集矩阵 |
| `research/phase38_ai_model_platform_research_task_queue.md` | Phase 38 ResearchIngestionTask 队列 |
| `audit/phase38_ai_model_platform_knowledge_scope_for_audit.json` | Phase 38 知识范围审计 JSON |
| `audit/phase38_p0_core_candidate_audit_package_20260610.json` | Phase 38 P0-Core 候选知识统一审计包 |
| `reports/phase38_p0_core_candidate_generation_report.md` | Phase 38 P0-Core 候选知识生成报告 |
| `reports/phase38_p0_core_candidate_quality_gate.json` | Phase 38 P0-Core 候选知识质量门禁报告 |
| `../codex-expert-kit/rag/scripts/generate_phase38_ai_model_platform_candidates.py` | Phase 38 P0-Core 候选知识生成脚本 |
| `../codex-expert-kit/rag/scripts/export_phase38_p0_core_audit_package.py` | Phase 38 P0-Core 候选知识审计包导出脚本 |
| `audit/audit_result_phase38_p0_core_20260610_strict_v1.json` | Phase 38 P0-Core 严格审计结构化结果 |
| `reports/phase38_p0_core_audit_import_report.json` | Phase 38 P0-Core 审计结果导入与候选分流报告 |
| `../codex-expert-kit/rag/scripts/apply_phase38_p0_core_audit_result.py` | Phase 38 P0-Core 审计结果导入脚本 |
| `contracts/phase38_rag_citation_and_reason_taxonomy_contract.md` | Phase 38 RAG 引用、Reason Taxonomy 与默认指导门禁契约 |
| `research/phase38_p0_core_supplemental_research.md` | Phase 38 P0-Core needs_more_evidence 补证采集记录 |
| `audit/phase38_p0_core_supplemental_audit_package_20260610.json` | Phase 38 P0-Core 补证后二审包 |
| `../codex-expert-kit/rag/scripts/apply_phase38_p0_core_supplemental_evidence.py` | Phase 38 P0-Core 补证回写与二审包导出脚本 |
| `audit/audit_result_phase38_p0_core_supplemental_reaudit_20260610_strict_v2.json` | Phase 38 P0-Core 补证二审结构化结果 |
| `reports/phase38_p0_core_supplemental_reaudit_import_report.json` | Phase 38 P0-Core 补证二审导入报告 |
| `../codex-expert-kit/rag/scripts/apply_phase38_p0_core_supplemental_reaudit_result.py` | Phase 38 P0-Core 补证二审导入脚本 |
| `research/phase38_g04_context_budget_supplemental_research.md` | Phase 38 G04-R1 上下文预算三审补证记录 |
| `audit/phase38_g04_context_budget_third_audit_package_20260610.json` | Phase 38 G04-R1 三审包 |
| `reports/phase38_g04_context_budget_third_audit_package_report.json` | Phase 38 G04-R1 三审包导出报告 |
| `../codex-expert-kit/rag/scripts/apply_phase38_g04_context_budget_third_audit_package.py` | Phase 38 G04-R1 三审补证与审计包导出脚本 |
| `../codex-expert-kit/rag/scripts/promote_phase38_accepted_candidates_to_reviewed.py` | Phase 38 accepted_for_draft 候选沉淀为 formal reviewed 知识脚本 |
| `reports/phase38_candidates_to_reviewed_promotion_report.json` | Phase 38 候选沉淀为 formal reviewed 知识报告 |
| `../codex-expert-kit/rag/scripts/validate_phase38_runtime_linkage.py` | Phase 38 MCP/SearchLab/KnowledgeTree 运行时联动验证脚本 |
| `reports/phase38_runtime_linkage_validation_report.json` | Phase 38 MCP/SearchLab/KnowledgeTree 运行时联动验证报告 |
| `reports/phase38_ai_model_platform_poc_knowledge_report.md` | Phase 38 AI 模型平台与交易 Gating/Scoring POC 知识扩展验收报告 |
| `reports/phase38_ai_model_platform_poc_final_closure_report.md` | Phase 38 AI 模型平台与交易 Gating/Scoring POC 最终收口报告 |
| `reports/phase38_extended_p1_scope_alignment_report.json` | Phase 38 P0-Extended / P1 剩余范围对齐报告 |
| `../codex-expert-kit/rag/scripts/generate_phase38_extended_p1_candidates.py` | Phase 38 P0-Extended / P1 候选知识生成脚本 |
| `reports/phase38_extended_p1_candidate_generation_report.md` | Phase 38 P0-Extended / P1 候选知识生成报告 |
| `reports/phase38_extended_p1_candidate_quality_gate.json` | Phase 38 P0-Extended / P1 候选知识质量门禁 |
| `../codex-expert-kit/rag/scripts/export_phase38_extended_p1_audit_package.py` | Phase 38 P0-Extended / P1 候选审计包导出脚本 |
| `audit/phase38_extended_p1_candidate_audit_package_20260610.json` | Phase 38 P0-Extended / P1 候选知识 AI 审计包 |
| `audit/audit_result_phase38_extended_p1_20260610_strict_v1.json` | Phase 38 P0-Extended / P1 严格审计结构化结果 |
| `reports/phase38_extended_p1_audit_import_report.json` | Phase 38 P0-Extended / P1 审计结果导入与候选分流报告 |
| `../codex-expert-kit/rag/scripts/apply_phase38_extended_p1_audit_result.py` | Phase 38 P0-Extended / P1 审计结果导入脚本 |
| `../codex-expert-kit/rag/scripts/apply_phase38_extended_p1_supplemental_evidence.py` | Phase 38 P0-Extended / P1 补证与二审包导出脚本 |
| `research/phase38_extended_p1_supplemental_research.md` | Phase 38 P0-Extended / P1 14 条候选补证采集记录 |
| `audit/phase38_extended_p1_supplemental_audit_package_20260610.json` | Phase 38 P0-Extended / P1 补证后二审包 |
| `reports/phase38_extended_p1_supplemental_evidence_report.json` | Phase 38 P0-Extended / P1 补证执行报告 |
| `../codex-expert-kit/rag/scripts/apply_phase38_extended_p1_supplemental_reaudit_result.py` | Phase 38 P0-Extended / P1 补证二审导入脚本 |
| `audit/audit_result_phase38_extended_p1_supplemental_reaudit_20260610_strict_v2.json` | Phase 38 P0-Extended / P1 补证二审结构化结果 |
| `reports/phase38_extended_p1_supplemental_reaudit_import_report.json` | Phase 38 P0-Extended / P1 补证二审导入报告 |
| `../codex-expert-kit/rag/scripts/apply_phase38_b10_bayesian_calibration_supplement.py` | Phase 38 B10 Bayesian calibration 补证与三审包导出脚本 |
| `research/phase38_b10_bayesian_calibration_supplemental_research.md` | Phase 38 B10 Bayesian calibration 单条补证记录 |
| `audit/phase38_b10_bayesian_calibration_third_audit_package_20260610.json` | Phase 38 B10 Bayesian calibration 三审包 |
| `reports/phase38_b10_bayesian_calibration_supplement_report.json` | Phase 38 B10 Bayesian calibration 补证执行报告 |
| `../codex-expert-kit/rag/scripts/apply_phase38_b10_third_reaudit_result.py` | Phase 38 B10 Bayesian calibration 三审结果导入脚本 |
| `audit/audit_result_phase38_b10_bayesian_calibration_third_reaudit_20260610_strict_v3.json` | Phase 38 B10 Bayesian calibration 三审结构化结果 |
| `reports/phase38_b10_bayesian_calibration_third_reaudit_import_report.json` | Phase 38 B10 Bayesian calibration 三审导入报告 |
| `../codex-expert-kit/rag/scripts/promote_phase38_ai_passed_candidates_to_reviewed.py` | Phase 38 残留 23 条 ai_passed 候选沉淀为 formal reviewed/caveat_only 知识脚本 |
| `reports/phase38_ai_passed_to_reviewed_promotion_report.json` | Phase 38 残留 23 条 ai_passed 候选沉淀报告 |
| `tasks/phase41_hybrid_scoring_qwen3_audit_stack.md` | Phase 41 Hybrid Scoring 与 Qwen3 审计助手知识扩展任务卡 |
| `research/phase41_hybrid_scoring_qwen3_scope.md` | Phase 41 Hybrid Scoring Stack 知识范围、L3 专题和跨分支边界 |
| `contracts/phase41_hybrid_scoring_runtime_contract.md` | Phase 41 表格 scorer、校准器、Qwen3 审计助手、RAG 和 deterministic final gate 组合运行时契约 |
| `contracts/phase41_tabular_llm_training_data_contract.md` | Phase 41 表格模型、Qwen3 审计助手、point-in-time feature、标签、校准、阈值和模型 registry 数据契约 |
| `research/phase41_hybrid_scoring_collection_matrix.md` | Phase 41 41 条 Hybrid Scoring 与 Qwen3 审计助手知识点采集矩阵 |
| `research/phase41_research_task_queue.md` | Phase 41 ResearchIngestionTask 队列 |
| `audit/phase41_hybrid_scoring_qwen3_scope_for_audit.json` | Phase 41 Hybrid Scoring 与 Qwen3 审计助手知识范围审计 JSON |
| `audit/audit_result_phase41_hybrid_scoring_qwen3_scope_20260610_strict_v1.json` | Phase 41 知识范围严格审计结构化结果 |
| `reports/phase41_scope_audit_patch_import_report.json` | Phase 41 知识范围审计补丁导入报告 |
| `../codex-expert-kit/rag/scripts/generate_phase41_p0_core_candidates.py` | Phase 41 P0-Core 候选知识生成脚本 |
| `research/phase41_p0_core_candidate_research.md` | Phase 41 P0-Core 候选知识来源采集记录 |
| `reports/phase41_candidate_generation_report.md` | Phase 41 P0-Core 候选知识生成报告 |
| `reports/phase41_candidate_quality_gate.json` | Phase 41 P0-Core 候选知识质量门禁 |
| `../codex-expert-kit/rag/scripts/export_phase41_candidate_audit_package.py` | Phase 41 P0-Core 候选知识 AI 审计包导出脚本 |
| `audit/phase41_candidate_audit_package_20260610.json` | Phase 41 P0-Core 候选知识 AI 审计包 |
| `../codex-expert-kit/rag/scripts/apply_phase41_candidate_audit_result.py` | Phase 41 候选严格审计结果导入、补证和重建脚本 |
| `audit/audit_result_phase41_candidate_audit_package_20260610_strict_v1.json` | Phase 41 P0-Core 候选严格审计结构化结果 |
| `reports/phase41_candidate_audit_import_report.json` | Phase 41 候选严格审计导入报告 |
| `research/phase41_candidate_supplemental_research.md` | Phase 41 needs_more_evidence 与重建候选补证记录 |
| `audit/phase41_candidate_supplemental_reaudit_package_20260610.json` | Phase 41 needs_more_evidence 与重建候选二审包 |
| `../codex-expert-kit/rag/scripts/apply_phase41_candidate_supplemental_reaudit_result.py` | Phase 41 二审结果导入与候选状态回写脚本 |
| `audit/audit_result_phase41_candidate_supplemental_reaudit_20260610_strict_v2.json` | Phase 41 二审严格审计结构化结果 |
| `reports/phase41_candidate_supplemental_reaudit_import_report.json` | Phase 41 二审导入报告 |
| `reports/phase41_candidate_remaining_evidence_followups.json` | Phase 41 二审后剩余待补证清单 |
| `../codex-expert-kit/rag/scripts/prepare_phase41_a05_r1_third_audit_package.py` | Phase 41 P41-A05-R1 三审补证与三审包导出脚本 |
| `audit/phase41_a05_r1_third_audit_package_20260610.json` | Phase 41 P41-A05-R1 三审补证包 |
| `reports/phase41_a05_r1_third_audit_preparation_report.md` | Phase 41 P41-A05-R1 三审补证报告 |
| `../codex-expert-kit/rag/scripts/apply_phase41_a05_r1_third_audit_result.py` | Phase 41 P41-A05-R1 三审结果导入脚本 |
| `audit/audit_result_phase41_a05_r1_third_audit_20260610_strict_v3.json` | Phase 41 P41-A05-R1 三审严格审计结构化结果 |
| `reports/phase41_a05_r1_third_audit_import_report.json` | Phase 41 P41-A05-R1 三审导入报告 |
| `../codex-expert-kit/rag/scripts/export_phase41_ai_passed_reviewed_preparation_package.py` | Phase 41 22 条 ai_passed 候选 reviewed-preparation 审计包导出脚本 |
| `audit/phase41_ai_passed_reviewed_preparation_audit_package_20260610.json` | Phase 41 22 条 ai_passed 候选 reviewed-preparation 审计包 |
| `reports/phase41_ai_passed_reviewed_preparation_gap_report.json` | Phase 41 reviewed-preparation 缺口与门禁报告 |
| `../codex-expert-kit/rag/scripts/apply_phase41_reviewed_preparation_result.py` | Phase 41 reviewed-preparation 审计结果导入和 formal reviewed 知识沉淀脚本 |
| `audit/audit_result_phase41_ai_passed_reviewed_preparation_20260610_strict_v1.json` | Phase 41 reviewed-preparation 严格审计结果 |
| `reports/phase41_reviewed_preparation_import_report.json` | Phase 41 reviewed-preparation 导入与 formal reviewed 沉淀报告 |
| `reports/phase41_reviewed_preparation_remaining_followups.json` | Phase 41 reviewed-preparation 后续补证清单 |
| `../ui/src/types.ts` | Vue3 候选来源类型契约，已补齐 Phase 41 新增 source_type |
| `../codex-expert-kit/rag/scripts/validate_phase41_runtime_linkage.py` | Phase 41 MCP/SearchLab/KnowledgeTree/Vue3 运行时联动验证脚本 |
| `reports/phase41_runtime_linkage_validation_report.json` | Phase 41 运行时联动验证报告 |
| `reports/phase41_remaining_scope_alignment_report.json` | Phase 41 剩余 P0-Extended/P1 范围核对报告 |
| `../codex-expert-kit/rag/scripts/generate_phase41_extended_p1_candidates.py` | Phase 41 P0-Extended/P1 联合候选知识生成脚本 |
| `research/phase41_extended_p1_candidate_research.md` | Phase 41 P0-Extended/P1 联合候选来源采集记录 |
| `reports/phase41_extended_p1_candidate_generation_report.md` | Phase 41 P0-Extended/P1 联合候选生成报告 |
| `../codex-expert-kit/rag/scripts/export_phase41_extended_p1_audit_package.py` | Phase 41 P0-Extended/P1 联合候选审计包导出脚本 |
| `audit/phase41_extended_p1_candidate_audit_package_20260610.json` | Phase 41 P0-Extended/P1 19 条候选联合 AI 审计包 |
| `reports/phase41_extended_p1_candidate_quality_gate.json` | Phase 41 P0-Extended/P1 联合候选质量门禁报告 |
| `../codex-expert-kit/rag/scripts/apply_phase41_extended_p1_audit_result.py` | Phase 41 P0-Extended/P1 严格审计结果导入与候选分流脚本 |
| `audit/audit_result_phase41_extended_p1_candidate_audit_package_20260610_strict_v1.json` | Phase 41 P0-Extended/P1 严格审计结构化结果归档 |
| `reports/phase41_extended_p1_audit_import_report.json` | Phase 41 P0-Extended/P1 审计结果导入与候选分流报告 |
| `../codex-expert-kit/rag/scripts/supplement_phase41_extended_p1_needs_evidence.py` | Phase 41 P0-Extended/P1 needs_more_evidence 补证与二审包导出脚本 |
| `research/phase41_extended_p1_supplemental_research.md` | Phase 41 P0-Extended/P1 6 条候选补证采集记录 |
| `reports/phase41_extended_p1_supplemental_evidence_report.json` | Phase 41 P0-Extended/P1 6 条候选补证执行报告 |
| `audit/phase41_extended_p1_supplemental_reaudit_package_20260610.json` | Phase 41 P0-Extended/P1 6 条候选补证后二审包 |
| `audit/audit_result_phase41_extended_p1_supplemental_reaudit_20260610_strict_v2.json` | Phase 41 P0-Extended/P1 6 条补证候选二审结构化结果 |
| `../codex-expert-kit/rag/scripts/apply_phase41_extended_p1_supplemental_reaudit_result.py` | Phase 41 P0-Extended/P1 二审结果导入和 formal reviewed 沉淀脚本 |
| `reports/phase41_extended_p1_supplemental_reaudit_import_report.json` | Phase 41 P0-Extended/P1 6 条候选沉淀为 formal reviewed 报告 |
| `../codex-expert-kit/rag/scripts/export_phase41_extended_p1_remaining_reviewed_preparation_package.py` | Phase 41 P0-Extended/P1 剩余 13 条 ai_passed 候选 reviewed-preparation 再审计包导出脚本 |
| `audit/phase41_extended_p1_remaining_reviewed_preparation_audit_package_20260610.json` | Phase 41 P0-Extended/P1 剩余 13 条候选 reviewed-preparation 再审计包 |
| `reports/phase41_extended_p1_remaining_reviewed_preparation_gap_report.json` | Phase 41 P0-Extended/P1 剩余 13 条候选 reviewed-preparation 缺口与门禁报告 |
| `audit/audit_result_phase41_extended_p1_remaining_reviewed_preparation_20260610_strict_v1.json` | Phase 41 P0-Extended/P1 剩余 13 条候选 reviewed-preparation 严格再审计结果 |
| `../codex-expert-kit/rag/scripts/apply_phase41_extended_p1_remaining_reviewed_preparation_result.py` | Phase 41 剩余 13 条再审计结果导入、12 条 formal reviewed 沉淀和 P41-A06 metadata/slug 修复脚本 |
| `reports/phase41_extended_p1_remaining_reviewed_preparation_import_report.json` | Phase 41 剩余 13 条再审计结果导入报告；12 条入 formal reviewed，1 条继续 needs_more_evidence |
| `reports/phase41_a06_metadata_slug_followup_report.json` | Phase 41 P41-A06 metadata/slug 修复与后续补证报告 |
| `../codex-expert-kit/rag/scripts/prepare_phase41_a06_single_model_baseline_third_audit_package.py` | Phase 41 P41-A06 single-model baseline comparison 与 auditability impact 补证及三审包导出脚本 |
| `research/phase41_a06_ensemble_baseline_auditability_supplemental_research.md` | Phase 41 P41-A06 单模型 baseline 与 ensemble 可审计性补证记录 |
| `audit/phase41_a06_single_model_baseline_third_audit_package_20260611.json` | Phase 41 P41-A06 单条三审 JSON 包 |
| `reports/phase41_a06_single_model_baseline_third_audit_package_report.json` | Phase 41 P41-A06 补证执行与三审包导出报告 |
| `../codex-expert-kit/rag/scripts/apply_phase41_a06_third_audit_result.py` | Phase 41 P41-A06 三审结果导入脚本，只升级候选为 accepted_for_draft |
| `audit/audit_result_phase41_a06_single_model_baseline_third_audit_20260611_strict_v3.json` | Phase 41 P41-A06 三审结构化结果归档 |
| `reports/phase41_a06_third_audit_import_report.json` | Phase 41 P41-A06 三审结果导入报告 |
| `../codex-expert-kit/rag/scripts/export_phase41_a06_reviewed_preparation_package.py` | Phase 41 P41-A06 reviewed/caveat_only 准备审计包导出脚本 |
| `audit/phase41_a06_reviewed_preparation_audit_package_20260611.json` | Phase 41 P41-A06 reviewed/caveat_only 准备审计包 |
| `reports/phase41_a06_reviewed_preparation_gap_report.json` | Phase 41 P41-A06 reviewed/caveat_only 准备缺口报告 |
| `audit/audit_result_phase41_a06_reviewed_preparation_20260611_strict_v1.json` | Phase 41 P41-A06 reviewed/caveat_only 准备审计结构化结果 |
| `../codex-expert-kit/rag/scripts/apply_phase41_a06_reviewed_preparation_result.py` | Phase 41 P41-A06 reviewed/caveat_only 审计结果导入与 formal reviewed 沉淀脚本 |
| `reports/phase41_a06_reviewed_preparation_import_report.json` | Phase 41 P41-A06 formal reviewed/caveat_only 沉淀报告 |
| `reports/phase41_final_acceptance_report.md` | Phase 41 全量 41 条 MCP/SearchLab/KnowledgeTree/Vue3 最终验收报告 |
| `tasks/phase42_database_data_contract_storage_engineering.md` | Phase 42 Database / Data Contract / Storage Engineering for Trading AI 任务卡 |
| `tasks/phase43_external_project_ai_memory_layer.md` | Phase 43 External Project AI Memory Layer 任务卡 |
| `research/phase43_external_project_ai_memory_scope.md` | Phase 43 外接项目 AI 记忆层范围、知识树节点和 RAG/Memory 边界 |
| `contracts/phase43_project_memory_contract.md` | Phase 43 MemoryItem、memory_event_log、memory_links 和生命周期契约 |
| `contracts/phase43_project_memory_mcp_api_contract.md` | Phase 43 Project Memory MCP/API 只读与受控写入契约 |
| `contracts/phase43_memory_write_retrieval_policy.md` | Phase 43 记忆写入门禁、检索预算、visibility、supersede 和上下文注入策略 |
| `contracts/phase43_memory_security_governance_contract.md` | Phase 43 memory poisoning、prompt injection、secret scan、rollback 和完整性安全治理契约 |
| `contracts/phase43_memory_retention_privacy_contract.md` | Phase 43 retention、deletion、export、privacy minimization、tombstone 和生命周期证据契约 |
| `research/phase43_memory_collection_matrix.md` | Phase 43 29 条 AI Memory 知识点采集矩阵 |
| `research/phase43_research_task_queue.md` | Phase 43 ResearchIngestionTask 队列 |
| `audit/audit_result_phase43_external_project_ai_memory_scope_20260611_strict_v1.md` | Phase 43 范围严格审计结果归档，结论为 accept_with_patch |
| `audit/phase43_external_project_ai_memory_scope_for_audit.json` | Phase 43 知识范围、L3 专题、Memory Contract、adapter 选型和 29 条知识点审计 JSON |
| `../codex-expert-kit/rag/scripts/generate_phase43_candidates.py` | Phase 43 29 条 External Project AI Memory Layer 候选知识生成脚本 |
| `../codex-expert-kit/rag/scripts/export_phase43_candidate_audit_package.py` | Phase 43 候选知识 AI 审计包导出脚本 |
| `research/phase43_candidate_research.md` | Phase 43 29 条候选知识联网采集来源记录 |
| `reports/phase43_candidate_generation_report.md` | Phase 43 29 条候选知识生成报告 |
| `reports/phase43_candidate_quality_gate.json` | Phase 43 候选来源、冲突、边界和默认指导质量门禁 |
| `audit/phase43_candidate_audit_package_20260611.json` | Phase 43 29 条候选 AI 审计包 |
| `reports/phase43_candidate_audit_package_quality_gate.json` | Phase 43 候选审计包质量门禁 |
| `audit/audit_result_phase43_candidate_audit_package_20260611_strict_v1.json` | Phase 43 29 条候选严格审计结果归档，12 条 accepted_for_draft、11 条 needs_more_evidence、6 条 rejected |
| `../codex-expert-kit/rag/scripts/apply_phase43_candidate_audit_result.py` | Phase 43 候选严格审计结果导入、补证、重建和二审包导出脚本 |
| `reports/phase43_candidate_audit_import_report.json` | Phase 43 首轮候选审计导入报告 |
| `research/phase43_supplemental_research.md` | Phase 43 11 条补证和 6 条重建候选二审来源记录 |
| `audit/phase43_supplemental_reaudit_package_20260611.json` | Phase 43 17 条补证/重建候选二审包 |
| `reports/phase43_supplemental_reaudit_quality_gate.json` | Phase 43 17 条二审包质量门禁 |
| `audit/audit_result_phase43_supplemental_reaudit_20260611_strict_v2.json` | Phase 43 17 条补证/重建候选二审结果归档，全部 accepted_for_draft |
| `../codex-expert-kit/rag/scripts/apply_phase43_supplemental_reaudit_result.py` | Phase 43 补证/重建候选二审结果导入脚本，仅推进 formal draft queue |
| `reports/phase43_supplemental_reaudit_import_report.json` | Phase 43 二审结果导入报告，29 条有效候选均进入 accepted_for_draft |
| `../codex-expert-kit/rag/scripts/promote_phase43_accepted_candidates_to_formal_draft.py` | Phase 43 accepted_for_draft 候选转 formal draft 脚本，仅生成 draft，不创建 reviewed/approved/default guidance/hard gate |
| `../codex-expert-kit/rag/knowledge/KB_AI_27_PROJECT_MEMORY/` | Phase 43 External Project AI Memory Layer 的 29 条 formal draft 知识目录 |
| `reports/phase43_formal_draft_generation_report.json` | Phase 43 formal draft 生成报告，29 条 draft、6 条 rejected 原始候选跳过 |
| `../codex-expert-kit/rag/scripts/export_phase43_formal_draft_reviewed_audit_package.py` | Phase 43 formal draft reviewed/caveat_only 准备审计包导出脚本，不创建 reviewed/approved/default guidance/hard gate |
| `audit/phase43_formal_draft_reviewed_audit_package_20260611.json` | Phase 43 29 条 formal draft reviewed/caveat_only 准备审计包 |
| `reports/phase43_formal_draft_reviewed_audit_package_quality_gate.json` | Phase 43 formal draft reviewed/caveat_only 审计包质量门禁，29 条通过 |
| `reports/phase43_formal_draft_reviewed_preparation_gap_report.json` | Phase 43 formal draft reviewed/caveat_only 准备缺口报告 |
| `audit/audit_result_phase43_formal_draft_reviewed_preparation_20260611_strict_v1.json` | Phase 43 formal draft reviewed/caveat_only 准备审计结果归档，29 条全部允许进入 reviewed/caveat_only |
| `../codex-expert-kit/rag/scripts/apply_phase43_formal_draft_reviewed_result.py` | Phase 43 formal draft reviewed/caveat_only 审计结果导入与正式 reviewed 知识沉淀脚本 |
| `reports/phase43_formal_draft_reviewed_import_report.json` | Phase 43 29 条 formal draft 沉淀为 formal reviewed/caveat_only 的导入报告 |
| `../codex-expert-kit/rag/scripts/validate_phase43_runtime_linkage.py` | Phase 43 MCP/SearchLab/KnowledgeTree/Vue3 运行时联动验证脚本 |
| `reports/phase43_runtime_linkage_validation_report.json` | Phase 43 29 条 External Project AI Memory Layer 知识运行时联动验证报告 |
| `reports/phase43_external_project_ai_memory_layer_report.md` | Phase 43 External Project AI Memory Layer 全量验收报告，29 条知识均为 reviewed/caveat_only |
| `tasks/phase44_ai_trader_project_gap_audit.md` | Phase 44 AI 交易者项目方案知识断层审计任务卡 |
| `audit/phase44_ai_trader_project_gap_audit_task.json` | Phase 44 AI 交易者项目方案知识断层审计任务 JSON |
| `reports/phase44_ai_trader_project_gap_audit_report.md` | Phase 44 使用当前正式知识库推演 AI 交易者项目理论方案后的知识断层审计报告 |
| `reports/phase44_ai_layer_business_flow_topology.md` | Phase 44 聚焦 AI 层技术底座的业务流拓扑、技术栈和断点审计报告 |
| `research/phase42_database_storage_scope.md` | Phase 42 数据库、数据契约、存储工程知识范围、L3 专题和跨分支边界 |
| `contracts/phase42_database_storage_contract.md` | Phase 42 交易 AI 数据库核心表、主键、索引、时间字段、版本字段和审计字段契约 |
| `contracts/phase42_rag_vector_storage_contract.md` | Phase 42 RAG 文档、chunk、embedding、vector index、citation 和 source provenance 存储契约 |
| `research/phase42_database_storage_collection_matrix.md` | Phase 42 34 条数据库/存储工程知识点采集矩阵 |
| `research/phase42_research_task_queue.md` | Phase 42 ResearchIngestionTask 队列 |
| `audit/phase42_database_storage_scope_for_audit.json` | Phase 42 知识范围、L3 专题、表结构和知识点数量审计 JSON |
| `research/phase42_p0_candidate_research.md` | Phase 42 P0 候选知识联网采集来源记录 |
| `reports/phase42_candidate_generation_report.md` | Phase 42 P0 候选知识生成报告 |
| `reports/phase42_candidate_quality_gate.json` | Phase 42 P0 候选来源、冲突、边界和默认指导质量门禁 |
| `audit/phase42_candidate_audit_package_20260611.json` | Phase 42 P0 28 条候选 AI 审计包 |
| `audit/audit_result_phase42_candidate_audit_package_20260611_strict_v1.json` | Phase 42 P0 28 条候选第一轮严格审计结果 |
| `reports/phase42_candidate_audit_package_quality_gate.json` | Phase 42 候选审计包质量门禁 |
| `reports/phase42_candidate_audit_import_report.json` | Phase 42 第一轮审计结果导入和候选队列回写报告 |
| `audit/phase42_needs_evidence_supplemental_reaudit_package_20260611.json` | Phase 42 第一轮 14 条 needs_more_evidence 候选补证后二审包 |
| `research/phase42_needs_evidence_supplemental_research.md` | Phase 42 14 条 needs_more_evidence 候选补证来源记录 |
| `reports/phase42_needs_evidence_supplemental_report.json` | Phase 42 14 条 needs_more_evidence 候选补证质量门禁报告 |
| `audit/audit_result_phase42_needs_evidence_supplemental_reaudit_20260611_strict_v2.json` | Phase 42 14 条补证候选二审结果，全部 accepted_for_draft，不允许直接 reviewed/approved/default/hard gate |
| `reports/phase42_supplemental_reaudit_import_report.json` | Phase 42 补证二审结果导入报告，28 条 P0 候选全部进入 ai_passed |
| `reports/phase42_candidates_to_reviewed_promotion_report.json` | Phase 42 28 条 P0 候选沉淀为 formal reviewed/caveat_only 的转换报告 |
| `reports/phase42_runtime_linkage_validation_report.json` | Phase 42 MCP/SearchLab/KnowledgeTree/Vue3 联动验证报告 |
| `reports/phase42_database_storage_engineering_report.md` | Phase 42 全量 34 条数据库/数据契约/存储工程知识验收报告 |
| `../codex-expert-kit/rag/scripts/generate_phase42_p0_candidates.py` | Phase 42 P0 候选知识生成脚本 |
| `../codex-expert-kit/rag/scripts/export_phase42_candidate_audit_package.py` | Phase 42 P0 候选 AI 审计包导出脚本 |
| `../codex-expert-kit/rag/scripts/apply_phase42_candidate_audit_result.py` | Phase 42 第一轮候选审计结果导入脚本 |
| `../codex-expert-kit/rag/scripts/supplement_phase42_needs_evidence.py` | Phase 42 14 条 needs_more_evidence 候选补证和二审包导出脚本 |
| `../codex-expert-kit/rag/scripts/apply_phase42_supplemental_reaudit_result.py` | Phase 42 补证二审结果导入脚本，只推进候选到 accepted_for_draft，不创建正式知识 |
| `../codex-expert-kit/rag/scripts/promote_phase42_accepted_candidates_to_reviewed.py` | Phase 42 accepted_for_draft 候选沉淀为 formal reviewed/caveat_only 的转换脚本 |
| `../codex-expert-kit/rag/scripts/validate_phase42_runtime_linkage.py` | Phase 42 MCP/SearchLab/KnowledgeTree/Vue3 联动验证脚本 |
| `../codex-expert-kit/rag/scripts/generate_phase42_p1_candidates.py` | Phase 42 P1 6 条候选知识生成脚本 |
| `research/phase42_p1_candidate_research.md` | Phase 42 P1 6 条候选知识联网采集来源记录 |
| `reports/phase42_p1_candidate_generation_report.md` | Phase 42 P1 6 条候选知识生成报告 |
| `reports/phase42_p1_candidate_quality_gate.json` | Phase 42 P1 候选来源、冲突、边界和默认指导质量门禁 |
| `../codex-expert-kit/rag/scripts/export_phase42_p1_candidate_audit_package.py` | Phase 42 P1 6 条候选 AI 审计包导出脚本 |
| `audit/phase42_p1_candidate_audit_package_20260611.json` | Phase 42 P1 6 条候选 AI 审计包 |
| `reports/phase42_p1_candidate_audit_package_quality_gate.json` | Phase 42 P1 候选审计包质量门禁 |
| `../codex-expert-kit/rag/scripts/apply_phase42_p1_candidate_audit_result.py` | Phase 42 P1 首轮审计结果导入与 P42-P1-003 补证二审包导出脚本 |
| `audit/audit_result_phase42_p1_candidate_audit_package_20260611_strict_v1.json` | Phase 42 P1 6 条候选首轮严格审计结构化结果归档 |
| `reports/phase42_p1_audit_import_report.json` | Phase 42 P1 首轮审计导入报告，5 条 accepted_for_draft，1 条 needs_more_evidence |
| `research/phase42_p1_p003_supplemental_research.md` | Phase 42 P1 P42-P1-003 CEK-TA formal index/citation/RAG vector storage 契约补证记录 |
| `audit/phase42_p1_p003_supplemental_reaudit_package_20260611.json` | Phase 42 P1 P42-P1-003 补证后二审包 |
| `reports/phase42_p1_p003_supplemental_reaudit_package_report.json` | Phase 42 P1 P42-P1-003 补证二审包导出报告 |
| `../codex-expert-kit/rag/scripts/apply_phase42_p1_p003_supplemental_reaudit_result.py` | Phase 42 P1 P42-P1-003 二审结果导入与 6 条 P1 reviewed-preparation 审计包导出脚本 |
| `audit/audit_result_phase42_p1_p003_supplemental_reaudit_20260611_strict_v2.json` | Phase 42 P1 P42-P1-003 补证二审结构化结果归档 |
| `reports/phase42_p1_p003_supplemental_reaudit_import_report.json` | Phase 42 P1 P42-P1-003 二审导入报告，P003 升级为 accepted_for_draft |
| `audit/phase42_p1_reviewed_preparation_audit_package_20260611.json` | Phase 42 P1 6 条 accepted_for_draft 候选 reviewed/caveat_only 准备审计包 |
| `reports/phase42_p1_reviewed_preparation_gap_report.json` | Phase 42 P1 6 条候选 reviewed-preparation 缺口与质量门禁报告 |
| `audit/audit_result_phase42_p1_reviewed_preparation_20260611_strict_v1.json` | Phase 42 P1 6 条候选 reviewed-preparation 严格审计结果，全部允许 formal reviewed/caveat_only |
| `reports/phase42_p1_reviewed_preparation_import_report.json` | Phase 42 P1 6 条候选沉淀为 formal reviewed/caveat_only 的导入报告 |
| `../codex-expert-kit/rag/scripts/apply_phase42_p1_reviewed_preparation_result.py` | Phase 42 P1 reviewed-preparation 审计结果导入与正式 reviewed/caveat_only 沉淀脚本 |
| `tasks/phase21_formal_mcp_knowledge_index.md` | Phase 21 MCP 正式知识聚合索引任务卡 |
| `../codex-expert-kit/rag/scripts/build_knowledge_items_index.py` | Phase 21 正式知识聚合索引生成脚本 |
| `../codex-expert-kit/rag/indexes/knowledge_items.json` | Phase 21 MCP 默认正式知识聚合索引 |
| `reports/formal_mcp_knowledge_index_report.md` | Phase 21 MCP 正式知识聚合索引验收报告 |
| `tasks/phase22_path_resolver_foundation.md` | Phase 22 Path Resolver 移植复用地基任务卡 |
| `../codex-expert-kit/core/path_resolver.py` | Phase 22 CEK-TA 统一路径 resolver |
| `reports/path_resolver_foundation_report.md` | Phase 22 Path Resolver 验收报告 |
| `tasks/phase23_partition_wide_research_ingestion.md` | Phase 23 13 分区全网专业知识采集任务卡 |
| `tasks/phase24_vue3_candidate_audit_workbench_v2.md` | Phase 24 Vue3 候选知识审计工作台 v2 任务卡 |
| `research/phase23_partition_collection_plan.md` | Phase 23 13 分区采集矩阵 |
| `research/phase23_source_seed_catalog.md` | Phase 23 可信来源种子库 |
| `research/phase23_research_task_queue.md` | Phase 23 ResearchIngestionTask 队列 |
| `seed_runtime_validation_plan.md` | Phase 19 Seed 知识运行时验证计划 |
| `reports/seed_runtime_validation_report.md` | Phase 19 Seed 知识 MCP/SearchLab 运行时验证报告 |
| `index_tasks.md` | 项目管理总入口和任务状态索引 |
| `tasks/README.md` | Phase 任务卡目录 |
| `../AGENTS.md` | 项目级开发规范和 Codex 持久规则 |
| `../.agents/skills/cek-ta-development-workflow/SKILL.md` | CEK-TA 开发流程 Skill |


