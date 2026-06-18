# Phase 44 AI 交易者项目方案知识断层审计报告

生成日期：2026-06-11

## 结论

当前 CEK-TA 知识库已经可以支撑“AI 交易者项目”的 AI Engineering 主干方案审计，尤其是：

```text
1. 数据契约、特征时间、dataset snapshot、lineage 和审计日志。
2. 表格模型 scorer 与 Qwen3 审计助手的职责分离。
3. calibration、threshold、abstain band 和 deterministic final gate。
4. shadow / paper / OPE / ablation / 持续学习闭环。
5. Project Memory 与 RAG Knowledge 的边界。
6. MCP/SearchLab/KnowledgeTree 运行时检索与阻断。
```

但如果目标是让外接项目的开发 AI 真正设计一个“交易质量提升型 AI 交易者系统”，知识库还有明显断层：

```text
1. Trading Engineering 本体偏薄，AI Engineering 很强，但交易本体规则不够丰富。
2. 行情/成交/订单/账户等真实数据采集知识不足。
3. 交易质量标签体系还缺 MAE/MFE、机会成本、持仓路径、出场质量和滑点调整等细粒度知识。
4. 从回测到 paper/live 的桥接验收规则还不够系统。
5. 实盘执行、组合风险、交易所异常、账户同步和权限恢复知识仍偏少。
```

因此，目前知识库适合指导“AI trading quality gating/scoring 项目”的工程架构和治理，不适合独立指导一个完整的自动交易系统。

## 当前知识库总体状态

正式知识总数：

```text
336 条
```

治理状态：

```text
approved / allow：10 条
reviewed / caveat_only：326 条
```

主要覆盖：

```text
AI Engineering、LLM Training、Hybrid Scoring、Continuous Learning、Database/Storage、Project Memory 覆盖较强。
Trading Engineering seed 知识存在，但数量明显少于 AI Engineering。
```

## AI 交易者项目理论方案

### 1. 项目目标与边界

理论方案：

```text
构建一个交易质量提升系统，而不是自动策略生成系统。
系统由表格 scorer 评估交易候选质量，由 Qwen3 类 LLM 审计解释、缺字段、RAG 引用和 reason code，由 deterministic final gate 统一放行、阻断或降级。
```

可用知识：

```text
kb_08_llm_training.eval_and_risk.source_boundary_human_escalation.v1
kb_ai_project_memory.phase43.rag_knowledge_project_memory.v1
kb_ai_project_memory.phase43.project_memory_cek_ta.v1
kb_ai_project_memory.phase43.ai_ide_cek_ta_mcp_project_memory_mcp.v1
```

判断：

```text
项目边界清楚：AI 不直接下单、不直接给买卖点、不替代 final gate。
```

### 2. 数据收集与数据契约

理论方案：

```text
数据进入系统前必须拆成 market_event、order_event、position_snapshot、trade_log、feature_snapshot、label_snapshot、audit_event。
每条数据必须带 event_time、decision_time、ingestion_time、label_time、source_hash、schema_version 和 lineage_ref。
```

可用知识：

```text
kb_ai_database_storage.phase42.event_decision_ingestion_label_time_separated.v1
kb_ai_database_storage.phase42.dataset_snapshot_manifest_dataset_hash.v1
kb_ai_database_storage.phase42.feature_snapshot_manifest_schema_hash.v1
kb_ai_database_storage.phase42.feature_lineage_record_source_object_ref.v1
kb_ai_database_storage.phase42.canonical_records_postgresql_not_vector_db.v1
```

断层：

```text
P0 thin：缺“真实行情源采集”知识，例如交易所 REST/WebSocket、K线重采样、盘口快照、成交流、缺失补齐、重复去重、交易日历、时区和 corporate action。
P0 thin：缺“订单/账户/持仓数据采集契约”，尤其是账户快照、资金费率、保证金、部分成交、撤单回报和交易所状态同步。
```

### 3. 交易知识归类与信号边界

理论方案：

```text
交易信号、K 线结构、市场微观结构、fill model、风控本体归 Trading Engineering。
AI Engineering 只记录 scoring/gating、训练、评估、RAG、LLM 审计和治理规则。
```

可用知识：

```text
kb_02_kline_strategy.signal_boundary.timeframe_market_scope.v1
kb_ai_engineering.scoring_rubric.market_regime_fit.v1
kb_ai_engineering.scoring_rubric.rule_compliance.v1
kb_ai_engineering.scoring_rubric.setup_quality.v1
```

断层：

```text
P0 missing：Trading Engineering 下缺系统化的 K 线结构、趋势/震荡/波动 regime、支撑阻力、盘口微观结构、成交量结构、订单流、资金费率和跨周期一致性知识。
P1 contract_gap：scoring rubric 能描述交易质量维度，但这些维度和 Trading Engineering 真实信号 taxonomy 之间缺正式映射。
```

### 4. 回测、回放和模拟盘

理论方案：

```text
任何策略或 scorer 标签来自回测时，必须先审计数据泄漏、lookahead、参数搜索、多重测试、fill model、slippage、fee model 和 OHLC 同 bar TP/SL 模糊。
回测通过后必须进入回放或模拟盘，不能把回测成交语义直接当实盘语义。
```

可用知识：

```text
kb_04_backtest.bias.multiple_testing_overfit.v1
kb_04_backtest.bias.leakage_overfit_audit_gates.v1
kb_04_backtest.fill_model.explicit_slippage_fee_assumptions.v1
kb_04_backtest.fill_model.ohlc_same_bar_path_ambiguity.v1
kb_05_replay_simulation.execution_semantics.backtest_not_live_truth.v1
kb_05_replay_simulation.fill_model.ohlc_same_bar_tp_sl_ambiguity.v1
```

断层：

```text
P0 thin：缺 walk-forward、purged CV、embargo、deflated Sharpe、白噪声检验、参数稳定性和样本外退化阈值的完整知识。
P1 thin：缺主流回测框架差异表，例如 Backtrader、Zipline、Lean、VectorBT 在订单语义、撮合、滑点、费用和时区处理上的差异。
```

### 5. 交易质量标签与训练数据

理论方案：

```text
AI 交易者训练数据不应只用 PnL。标签应至少包括风险调整收益、R/R、最大不利波动、最大有利波动、持仓时间、出场质量、执行成本、规则合规、解释质量和审计成本。
```

可用知识：

```text
kb_ai_engineering.trade_quality.success_metric_not_pnl_only.v1
kb_ai_engineering.data_quality.execution_cost_required.v1
kb_ai_hybrid_scoring.phase41.dataset_hash_split_manifest_hash_feature_schema_version_label_policy_version.v1
kb_ai_hybrid_scoring.phase41.training_data_strategy_version_required.v1
```

断层：

```text
P0 missing：缺正式“交易质量标签 taxonomy”，特别是 MAE/MFE、time-in-trade、entry quality、exit quality、missed opportunity、slippage-adjusted outcome、risk-normalized outcome。
P0 contract_gap：缺 TradeQualityLabel schema，与 feature_snapshot、order_event、position_snapshot、final_gate_decision 的字段级连接还不完整。
```

### 6. AI 评分模型与 LLM 审计助手

理论方案：

```text
LightGBM / XGBoost / Logistic Regression 负责数值 scoring。
Qwen3 类 LLM 负责审计解释、reason code、RAG 引用、缺字段检查和报告，不负责数值评分，也不负责 final gate。
最终交易放行由 deterministic final gate 决定。
```

可用知识：

```text
kb_ai_hybrid_scoring.phase41.logistic_regression_baseline_before_complex_model.v1
kb_ai_hybrid_scoring.phase41.lightgbm_xgboost_for_tabular_scoring.v1
kb_ai_hybrid_scoring.phase41.qwen3_numeric_scorer_final_gate.v1
kb_ai_hybrid_scoring.phase41.final_gate_scorer_risk_bucket_threshold_policy_allow_block_reduce_size_deterministic_final_gate_qwen3_recommendation_raw_model_score.v1
kb_ai_hybrid_scoring.phase41.conformal_abstain_band_deterministic_final_gate.v1
```

判断：

```text
这一段知识链条较强，足以指导外接项目 AI 架构边界。
```

断层：

```text
P1 thin：缺“交易场景特征工程模板”，例如 volatility、liquidity、spread、order imbalance、regime、holding context 与风险暴露的标准特征族。
P1 thin：缺模型输入漂移与市场 regime 漂移的联合诊断案例。
```

### 7. RAG/MCP 检索与来源引用

理论方案：

```text
AI IDE 在高风险交易、回测、模型训练、数据库、实盘风控、知识入库和外部项目接入任务中必须主动检索 CEK-TA。
所有输出必须带 source、citation、confidence、适用边界和不适用边界。
```

可用知识：

```text
kb_09_rag_engineering.source_quality.unsourced_default_block.v1
kb_08_llm_training.eval_and_risk.source_boundary_human_escalation.v1
kb_ai_engineering.security.rag_context_is_untrusted_input.v1
kb_ai_project_memory.phase43.ai_ide_cek_ta_mcp_project_memory_mcp.v1
```

判断：

```text
RAG/MCP 治理足够支撑 AI IDE 使用知识库。
```

断层：

```text
P2 runtime_gap：缺“AI 交易者方案审计”专用 MCP query template 和自动断层扫描脚本。
```

### 8. Shadow / Paper / OPE 验证

理论方案：

```text
模型不得直接上线。先做 shadow mode，记录 scorer、calibrator、RAG、LLM 审计、final gate 的完整 trace；再进入 paper trading，对比模拟订单和理论放行结果；最后用 OPE、ablation 和回归集评估改动影响。
```

可用知识：

```text
kb_ai_engineering.phase38.hard_gate_shadow_mode.v1
kb_ai_engineering.phase38.shadow_paper_ope_before_release.v1
kb_ai_engineering.phase38.rag_prompt_model_threshold_ablation.v1
kb_ai_engineering.phase38.shadow_no_hit_conflict_citation_completeness.v1
```

断层：

```text
P0 contract_gap：缺 PaperTradingEvaluation schema，无法清楚表达 paper order、simulated fill、actual fill、missed trade、blocked trade、override decision 的统一评估口径。
P1 thin：缺从 shadow 到 paper 到 limited-live 的阶段门槛表。
```

### 9. 实盘前 final gate 与风控执行

理论方案：

```text
final gate 汇总 scorer、calibrator、RAG、LLM 审计、风险限额、账户状态和交易规则，只输出 allow / block / reduce_size / review。
实盘执行仍由 Trading Engineering 的订单状态机、pre-trade risk gate、kill switch 和人工权限控制。
```

可用知识：

```text
kb_07_risk_management.risk_gate.pre_trade_order_risk_controls.v1
kb_06_live_execution.risk_control.kill_switch_no_new_orders.v1
kb_06_live_execution.order_state_machine.event_rest_position_reconciliation.v1
kb_ai_database_storage.phase42.every_decision_requires_audit_trace_id.v1
```

断层：

```text
P0 missing：组合级风险知识不足，例如相关性、行业/币种集中度、杠杆、保证金、流动性、最大日亏损、连续亏损、账户级暴露。
P0 missing：实盘 execution adapter 知识不足，例如交易所断连、订单幂等、重复下单防护、撤单失败、部分成交恢复、仓位重建。
P1 contract_gap：final gate 输出与真实 order router / risk engine 的接口契约还不完整。
```

### 10. 持续学习与模型发布治理

理论方案：

```text
每次交易候选、放行、阻断、人工覆盖、实际结果和复盘都进入 feedback log。
当 drift、label refresh、hard examples、误杀/漏放和市场 regime 变化达到阈值时触发再训练候选。
模型进入 registry，经 shadow/paper/OPE 通过后才能发布。
```

可用知识：

```text
kb_ai_feedback_governance.phase40.feedback_event_log_required.v1
kb_ai_feedback_governance.phase40.label_refresh_policy_required.v1
kb_ai_feedback_governance.phase40.drift_monitoring_required.v1
kb_ai_feedback_governance.phase40.retraining_trigger_requires_evidence.v1
kb_ai_hybrid_scoring.phase41.mlflow_registry_release_manifest_poc_registry.v1
```

判断：

```text
持续学习闭环较强，能支撑外接项目做模型治理。
```

断层：

```text
P1 thin：缺交易领域专用 drift taxonomy，例如 volatility regime drift、liquidity drift、execution cost drift、strategy behavior drift。
P1 runtime_gap：缺自动从 feedback log 生成 retraining candidate 的示例流程。
```

### 11. 数据库、审计日志和项目记忆

理论方案：

```text
PostgreSQL 作为 canonical store，向量库只做检索索引。
所有 gating/scoring 决策带 audit_trace_id。
Project Memory 保存外接项目目标、任务、决策、产物、边界和错误复盘，但不能污染 CEK-TA 通用知识库。
```

可用知识：

```text
kb_ai_database_storage.phase42.canonical_records_postgresql_not_vector_db.v1
kb_ai_database_storage.phase42.audit_ledger_tamper_evidence.v1
kb_ai_database_storage.phase42.every_decision_requires_audit_trace_id.v1
kb_ai_project_memory.phase43.memoryitem_hash_trust_write_origin.v1
kb_ai_project_memory.phase43.project_memory_mcp_api.v1
```

判断：

```text
数据库和项目记忆的治理基础充足。
```

断层：

```text
P1 contract_gap：缺 AI 交易者项目的最小数据库 ERD 样板，只能从 Phase 42 通用规则推导。
P1 runtime_gap：缺 Project Memory MCP 真实实现验收用例。
```

## 知识断层清单

| 优先级 | 类型 | 断层 | 影响 |
| --- | --- | --- | --- |
| P0 | missing | Trading Engineering 本体知识不足 | AI 项目能做 scoring 架构，但难以正确理解交易信号、市场结构和风控本体 |
| P0 | thin | 行情、成交、订单、账户数据采集知识不足 | 数据入口容易不可复现、不可审计，训练数据来源边界不清 |
| P0 | missing | 交易质量标签 taxonomy 不完整 | 训练目标可能退化成 PnL-only，无法真正提升交易质量 |
| P0 | contract_gap | PaperTradingEvaluation schema 缺失 | shadow/paper 结果难以比较，不能证明模型改善真实交易质量 |
| P0 | missing | 组合级风险和实盘 execution adapter 知识不足 | final gate 到实盘执行之间存在安全断层 |
| P1 | thin | walk-forward、purged CV、embargo、deflated Sharpe 等回测稳健性知识不足 | 回测标签和模型评估可能高估 |
| P1 | thin | 交易场景特征工程模板不足 | scorer 训练需要外接项目自行摸索特征族 |
| P1 | contract_gap | final gate 到 order router / risk engine 接口契约不足 | 理论 gate 与真实执行层对接不清 |
| P1 | thin | 交易领域 drift taxonomy 不足 | 持续学习能做，但难以解释是市场、执行还是策略行为漂移 |
| P2 | runtime_gap | 缺 AI 交易者方案专用断层扫描脚本 | 目前审计依靠人工阅读和通用检索 |

## 建议后续补强方向

### 建议 1：Trading Engineering 核心交易本体补强

优先补：

```text
1. 市场数据与交易日历。
2. K 线结构、趋势/震荡/波动 regime。
3. 市场微观结构、盘口、成交量、流动性。
4. 策略信号 taxonomy 与不适用边界。
5. 组合风险、保证金、杠杆、集中度和日亏损。
6. 实盘 order router、position reconciliation、异常恢复。
```

### 建议 2：Phase 46 Trade Quality Label 与 Paper Evaluation 契约

优先补：

```text
1. TradeQualityLabel schema。
2. MAE/MFE、R/R、holding time、entry/exit quality、slippage-adjusted outcome。
3. PaperTradingEvaluation schema。
4. blocked trade / allowed trade / missed trade / overridden trade 评估口径。
5. shadow -> paper -> limited-live 阶段门槛表。
```

### 建议 3：Phase 47 AI Trader Project Blueprint Audit Tooling

优先补：

```text
1. 自动读取 knowledge_items.json。
2. 按 AI 交易者 11 阶段生成覆盖矩阵。
3. 自动输出 missing/thin/contract_gap/runtime_gap/governance_gap。
4. 自动生成待补知识点候选清单。
```

## 最终判断

当前知识库已经适合支撑外接 AI 项目做：

```text
AI trading quality scoring/gating
RAG + Qwen3 audit assistant
数据契约与模型治理
shadow/paper/OPE
持续学习与项目记忆
```

但还不适合单独支撑完整 AI 交易者系统，关键原因不是 AI Engineering 不够，而是 Trading Engineering 本体和交易质量标签层还需要补强。
