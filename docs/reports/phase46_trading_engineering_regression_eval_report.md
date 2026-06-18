# Phase 46 Trading Engineering 知识回归评测验收报告

## 结论

Phase 46 已完成。当前 Trading Engineering 正式知识已形成可重复运行的 MCP/SearchLab/KnowledgeTree/Vue3 回归评测。

本轮不新增专业知识，不升级 `approved`，不启用 `default guidance`，不启用 `hard gate`。所有被测知识仍保持 `reviewed / caveat_only` 边界。

## 交付物

```text
codex-expert-kit/rag/scripts/validate_trading_engineering_regression.py
docs/reports/phase46_trading_engineering_regression_report.json
docs/reports/phase46_searchlab_case_matrix.json
docs/reports/phase46_vue_tree_candidate_consistency_report.json
docs/reports/phase46_trading_engineering_regression_eval_report.md
```

## 覆盖范围

本轮回归覆盖 14 个代表性 case，覆盖 Phase 37 Trading Engineering 核心分支和 Phase 45 扩展节点：

```text
Quant Foundation / R-multiple
Data Engineering / point-in-time reference data
Backtest / overfitting and parameter search
Replay Simulation / OHLC same-bar ordering
Execution TCA / implementation shortfall
Order Semantics / venue-specific order behavior
Risk Management / layered pre-trade controls
Stress Scenario / stress test is not permission
Trade Analysis / reason code taxonomy
Crypto Perpetual / mark-index-last boundary
Crypto Perpetual / exchange outage and clawback
Live Trade Audit / order event causality
Resilience / degraded and read-only mode
Market Data Entitlement / data license boundary
```

## 验收结果

```text
正式知识索引总量：479
Trading Engineering scoped inventory：153
回归 case 数：14
SearchLab/MCP 命中：14 / 14
默认指导阻断：14 / 14
Vue formal fixture 缺失：0
Vue knowledge tree node 缺失：0
状态：pass
```

## 治理边界

```text
reviewed/caveat_only 不等于 approved。
reviewed/caveat_only 不进入 default guidance。
reviewed/caveat_only 不启用 hard gate。
本回归只验证检索、引用、归类、阻断和前端 fixture 一致性。
不得用本评测输出买卖点、仓位、杠杆、止损止盈、风险阈值或实盘执行建议。
```

## 测试

已执行：

```text
python codex-expert-kit/rag/scripts/validate_trading_engineering_regression.py
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
npm --prefix ui run build
```

## 风险与回滚

本 Phase 只新增评测脚本和报告，不修改正式知识内容。若后续发现某个 case 关键词过窄，可以只回滚或调整 `validate_trading_engineering_regression.py` 中的 case 配置，不影响知识库本体。

## 后续建议

```text
1. 将 Phase 46 回归脚本接入后续知识上架流程，作为 Phase 37/45 Trading Engineering 的固定验收门禁。
2. 后续新增 Trading Engineering 知识时，同步追加至少 1 个代表性检索 case。
3. 后续如果开放 CI，再把本脚本加入 CI 的非联网本地验证阶段。
```
