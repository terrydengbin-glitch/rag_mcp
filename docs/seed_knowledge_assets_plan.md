# CEK-TA 首批真实知识资产计划

本文定义 Phase 17 首批真实知识资产的范围、来源策略、审计流程、验收门槛和质量报告要求。目标是先沉淀一批少量但高质量、可复用、可审计、可检索的专业知识样板，而不是一次性填满全部知识树。

## 计划身份

```yaml
plan_id: cek_ta_seed_knowledge_assets_20260608
phase: Phase 17
owner: codex
status: approved_for_seed_execution
created_at: 2026-06-08
updated_at: 2026-06-08
encoding: UTF-8
```

## 目标

```text
1. 跑通真实专业知识从选题、采集、来源审计、冲突审计、知识树归类、正式入库到质量评测的闭环。
2. 为其他交易项目提供第一批可复用的回测、K线边界、风控、执行、复盘、LLM/RAG 专业知识。
3. 为后续批量采集建立 accepted 知识样板。
4. 用 Phase 16 指标和评测集验收首批知识，不靠主观判断。
```

## 执行策略

第一轮不按任务卡中的 100 条目标直接铺开。第一轮先做 `10` 条高质量 seed 知识资产，形成可复制流程。

```yaml
target_count_first_seed: 10
target_count_later_expansion: 100
first_seed_policy: quality_before_quantity
review_mode: codex_reviewed_with_source_trace
storage_mode: file_based_mvp
default_review_status_target: approved
quality_report_path: docs/reports/seed_knowledge_quality_report.md
knowledge_storage_root: codex-expert-kit/rag/knowledge/
index_storage_root: codex-expert-kit/rag/indexes/
```

## 上游输入

```text
codex-expert-kit/rag/knowledge_tree.md
codex-expert-kit/rag/knowledge_tree_v2.md
codex-expert-kit/rag/knowledge_tree_aliases.md
codex-expert-kit/rag/tree_routing_policy.md
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/source_quality_rules.md
codex-expert-kit/rag/conflict_detection_rules.md
codex-expert-kit/rag/quality_metrics.md
codex-expert-kit/rag/eval_sets/
codex-expert-kit/templates/knowledge_quality_report.md
codex-expert-kit/templates/knowledge_leaf_package_template.md
codex-expert-kit/templates/research_ingestion_runbook.md
```

## 下游输出

```text
codex-expert-kit/rag/knowledge/**/*.json
codex-expert-kit/rag/indexes/knowledge_index.json
codex-expert-kit/rag/indexes/source_index.json
codex-expert-kit/rag/indexes/conflict_index.json
docs/reports/seed_knowledge_quality_report.md
Vue3 知识审计工作台可展示的知识条目
MCP/RAG 可检索的 approved 知识样例
后续批量知识采集的模板样板
```

## Topic Distribution

第一轮 seed 分布：

| Area | Count | 目标 | 主要消费者 |
| --- | ---: | --- | --- |
| 回测偏差与数据质量 | 2 | 防止未来函数、过拟合、多重测试、数据粒度误用 | 回测项目、策略审计、Codex code review |
| K线/指标使用边界 | 1 | 防止把 K线形态或指标信号当成跨市场通用真理 | 策略设计、策略审计 |
| 风控与仓位管理 | 2 | 明确 kill switch、最大亏损、风险预算的保守默认 | 模拟盘、实盘、风控审计 |
| 执行、滑点与成交模型 | 2 | 明确 fill model、slippage、同 bar 路径不确定性 | 回测、回放、模拟盘、实盘适配器 |
| 交易复盘与坏交易分类 | 1 | 把交易结果转为可诊断的改进样本 | trade_analysis、LLM 训练 |
| LLM/RAG 交易项目边界 | 2 | 防止无来源知识、项目私有事实、过期模型/API 行为进入默认指导 | RAG、MCP、其他项目接入 |

## 第一轮 Seed 候选清单

| Seed ID | 知识主题 | partition_id | v1 tree_node_id | canonical_node_id | risk_level | 目标状态 |
| --- | --- | --- | --- | --- | --- | --- |
| SEED-001 | 回测多重测试与过拟合偏差 | KB_04_BACKTEST | kt.backtest.bias | kt.trading_engineering.backtest.bias | high | approved |
| SEED-002 | OHLC K线无法确定同 bar 止盈止损先后顺序 | KB_04_BACKTEST | kt.backtest.bias | kt.trading_engineering.backtest.fill_assumption | high | approved |
| SEED-003 | K线/指标信号必须绑定周期、市场和样本边界 | KB_02_KLINE_STRATEGY | kt.kline_strategy | kt.trading_engineering.strategy_engineering.signal_boundary | medium | approved |
| SEED-004 | 实盘 kill switch 触发后默认禁止新开仓 | KB_06_LIVE_EXECUTION | kt.live_execution.risk_control | kt.trading_engineering.risk_management.kill_switch | critical | approved |
| SEED-005 | 最大亏损与仓位风险预算必须先于策略信号定义 | KB_01_QUANT_FOUNDATION | kt.quant_foundation.risk_return | kt.trading_engineering.risk_management.position_sizing | high | approved |
| SEED-006 | 回测 fill model 必须显式声明成交、滑点、费用假设 | KB_04_BACKTEST | kt.backtest.fill_model | kt.trading_engineering.backtest.fill_assumption | high | approved |
| SEED-007 | 模拟盘和实盘执行语义不能用回测成交结果直接替代 | KB_05_REPLAY_SIMULATION | kt.replay_simulation.fill_model | kt.trading_engineering.replay_simulation.execution_semantics | high | approved |
| SEED-008 | 坏交易分类必须区分信号错误、执行错误、风控错误和数据错误 | KB_07_TRADE_ANALYSIS | kt.trade_analysis.bad_trade | kt.trading_engineering.trade_analysis.bad_case_taxonomy | medium | approved |
| SEED-009 | 无来源 RAG 知识不能作为 Codex 默认专业指导 | KB_09_RAG_ENGINEERING | kt.rag_engineering.source_quality | kt.ai_engineering.rag_engineering.source_quality | high | approved |
| SEED-010 | 交易项目中的 LLM/RAG 输出必须保留来源、边界和人工升级动作 | KB_08_LLM_TRAINING | kt.llm_training.eval | kt.ai_engineering.llm_training.eval_and_risk | high | approved |

## Source Policy

允许来源：

```text
official_doc
exchange_rule
paper
framework_doc
book
research_report
engineering_article
internal_report after sanitization
task_card with external source support
code_doc for implementation-specific behavior
runbook after sanitization
```

首批 accepted 知识最低要求：

```text
1. 每条知识至少 1 个 medium/high 来源。
2. 高风险或 critical 知识优先使用 official_doc、exchange_rule、paper、framework_doc。
3. low 来源只能作为辅助，不得单独支撑 approved。
4. 性能、回测、风险控制类结论必须写明样本、假设或不可泛化边界。
5. 交易所、API、模型行为、实盘执行类知识必须带 accessed_at 和 freshness。
6. 不保存长篇版权内容，只保存摘要、证据说明和来源链接。
```

## Initial Source Backlog

| Source ID | Title | URL | source_type | Reliability | 用途 |
| --- | --- | --- | --- | --- | --- |
| SRC-SEED-001 | Backtesting Strategies Based on Multiple Signals | https://www.nber.org/papers/w21329 | paper | high | SEED-001 多重测试、过拟合偏差 |
| SRC-SEED-002 | Backtrader Orders - Creation/Execution | https://www.backtrader.com/docu/order-creation-execution/order-creation-execution/ | framework_doc | high | SEED-002/006 OHLC、limit、stop、stop-limit 成交假设 |
| SRC-SEED-003 | QuantConnect Trade Fills - Key Concepts | https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts | framework_doc | high | SEED-006/007 fill model、slippage model |
| SRC-SEED-004 | QuantConnect Trading and Orders | https://www.quantconnect.com/docs/v1/algorithm-reference/trading-and-orders | framework_doc | high | SEED-006 滑点、费用、brokerage model |
| SRC-SEED-005 | NIST AI Risk Management Framework | https://www.nist.gov/itl/ai-risk-management-framework | official_doc | high | SEED-010 AI 风险管理、生命周期治理 |
| SRC-SEED-006 | NIST AI RMF Core | https://airc.nist.gov/airmf-resources/airmf/5-sec-core/ | official_doc | high | SEED-010 govern/map/measure/manage、持续评估 |
| SRC-SEED-007 | CEK-TA Source Quality Rules | codex-expert-kit/rag/source_quality_rules.md | internal_report | medium | SEED-009 CEK-TA 来源质量规则 |
| SRC-SEED-008 | CEK-TA Search Result Contract | codex-expert-kit/rag/search_result_contract.md | internal_report | medium | SEED-009 RAG 默认指导阻断规则 |
| SRC-SEED-009 | CEK-TA Trade Bad Case Taxonomy | codex-expert-kit/domains/trade_analysis/knowledge/bad_trade_taxonomy.md | internal_report | medium | SEED-008 坏交易分类基础 |

## Review Policy

每条知识从候选到 approved 必须经过：

```text
candidate
  -> sourced
  -> classified
  -> conflict_checked
  -> reviewed
  -> approved
```

审计项：

```text
1. 来源是否支撑具体 statement。
2. source_type、publisher、accessed_at、reliability 是否完整。
3. domain/subdomain、partition_id、tree_node_id、canonical_node_id 是否一致。
4. applies_when 与 not_applicable_when 是否明确。
5. market、timeframe、data_granularity、project_type 是否没有被偷换。
6. conflict_status 是否为 none 或 resolved。
7. 是否包含投资建议、交易信号、项目私有字段或实时行情数据。
8. 是否能被 Phase 16 评测集检索或问答用例覆盖。
```

## Acceptance Threshold

首批 seed accepted 必须满足：

```yaml
source_presence_rate: 1.0
medium_high_source_rate: ">= 0.95"
low_only_approved_count: 0
unresolved_confirmed_conflict_count: 0
approved_unchecked_conflict_count: 0
applicability_boundary_rate: ">= 0.95"
citation_completeness: ">= 0.95"
unsafe_default_guidance_rate: 0
alias_mismatch_block_rate: 1.0
high_impact_stale_count: 0
```

首批 seed 可接受的限制：

```text
1. leaf_coverage_rate 不要求覆盖全树，只统计本计划目标节点。
2. reuse_count 初期可为 0，因为外部项目真实复用还未发生。
3. v1/v2 route consistency 如缺少正式 alias，可在报告中标注 needs_review，但不能影响安全阻断。
```

## Excluded Topics

```text
1. 实时行情、实时 K线、订单流原始数据。
2. 具体买卖点、交易信号、收益承诺、投资建议。
3. 无来源观点、论坛单帖、未经验证的社交媒体结论。
4. 其他项目的私有字段、账号信息、订单记录、未脱敏事故细节。
5. 与现有 accepted 规则冲突但未消解的理论。
6. 仅适用于单一项目但被伪装为通用知识的经验。
```

## Knowledge Item Output Contract

正式 JSON 知识条目写入：

```text
codex-expert-kit/rag/knowledge/<partition_id>/<knowledge_id>.json
```

每条必须包含：

```text
schema_version
knowledge_id
title
metadata.partition_id
metadata.domain
metadata.subdomain
metadata.rule_type
metadata.project_binding
metadata.used_for
metadata.tree_node_id
metadata.tree_path
metadata.canonical_node_id
metadata.canonical_tree_path
applicability
content.statement
content.rationale
content.procedure
content.anti_patterns
content.validation
content.risk_notes
source_evidence
source_quality
conflict_audit
review
contribution
```

## Index Output Contract

首批 seed 完成后同步维护：

```text
codex-expert-kit/rag/indexes/knowledge_index.json
codex-expert-kit/rag/indexes/source_index.json
codex-expert-kit/rag/indexes/conflict_index.json
```

索引只保存检索和审计摘要，不保存长正文。

## Quality Report Contract

质量报告写入：

```text
docs/reports/seed_knowledge_quality_report.md
```

报告必须包含：

```text
report_id
period
scope
input_inventory
score_summary
core_rates
regression_result
hard_gates
top_gaps
blocking_issues
recommended_actions
human_review_notes
boundaries
DoD checklist
```

## RAG/MCP Expected Behavior

默认指导模式只返回：

```text
review_status = approved
conflict_status = none or resolved
source_evidence present
project_binding = none or sanitized_project_case
freshness != deprecated
```

必须阻断：

```text
draft
rejected
deprecated
unsourced
confirmed unresolved conflict
project-private mismatch
high-impact stale without warning
alias mismatch
```

## Vue3 Audit Expected Behavior

Vue3 需要能展示：

```text
knowledge_id
title
partition_id
domain/subdomain
tree_node_id
canonical_node_id
source_count
source_reliability
review_status
conflict_status
confidence
freshness
risk_level
applicability boundary
not-applicable boundary
quality gate status
```

## Rollback

```text
1. 未达标知识保持 reviewed 或 draft，不进入 approved。
2. 已写入的 approved 知识如发现来源或冲突问题，降级为 reviewed 或 deprecated。
3. indexes 可由 knowledge/**/*.json 重建。
4. 质量报告记录降级原因和后续修复动作。
5. 不删除已审计历史，除非包含隐私、密钥或项目私有敏感信息。
```

## DoD

```text
1. 首批 seed 范围、数量、主题分布明确。
2. source_policy、review_policy、acceptance_threshold 明确。
3. excluded_topics 明确。
4. knowledge item、index、quality report 输出契约明确。
5. Phase 16 hard gates 被纳入验收。
6. v1/v2 tree routing 被纳入验收。
7. 不采集实时行情或原始 K线数据。
8. UTF-8 中文可读，无乱码。
```
