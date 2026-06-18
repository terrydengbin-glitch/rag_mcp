# Phase 37 Trading Engineering 专业知识库扩展验收报告

生成日期：2026-06-12  
任务范围：CEK-TA-189 至 CEK-TA-450，验收 Trading Engineering 96 条 P0 专业知识从范围定义、联网采集、候选审计、补证再审、formal reviewed/caveat_only 沉淀，到 MCP/SearchLab/KnowledgeTree/Vue3 联动验证的完整闭环。

## 验收结论

Phase 37 全量验收通过。

本轮已完成 Trading Engineering 8 组 P0 知识点，共 96 条 formal reviewed/caveat_only 知识。所有知识均保持来源、适用边界、非适用场景、冲突审计、审计追踪、候选回链和机器门禁。

本轮没有创建 approved 知识，没有启用 default guidance，没有启用 hard gate，也没有允许 risk threshold advice。

## 分组统计

| 分组 | 分区 | 正式知识数 | 状态 |
| --- | --- | ---: | --- |
| Quant Foundation / 量化基础 | `KB_01_QUANT_FOUNDATION` | 12 | reviewed/caveat_only |
| Data Engineering / 市场数据工程 | `KB_02_DATA_ENGINEERING` | 12 | reviewed/caveat_only |
| Kline / Strategy Engineering / K 线与策略工程 | `KB_02_KLINE_STRATEGY` | 12 | reviewed/caveat_only |
| Market Microstructure / 市场微观结构 | `KB_03_MARKET_MICROSTRUCTURE` | 12 | reviewed/caveat_only |
| Backtest / 回测可信度 | `KB_04_BACKTEST` | 12 | reviewed/caveat_only |
| Replay / Simulation / 回放与模拟 | `KB_05_REPLAY_SIMULATION` | 12 | reviewed/caveat_only |
| Live Execution / 实盘执行 | `KB_06_LIVE_EXECUTION` | 6 | reviewed/caveat_only |
| Risk Management / 风险管理 | `KB_07_RISK_MANAGEMENT` | 6 | reviewed/caveat_only |
| Trade Analysis / 交易复盘 | `KB_07_TRADE_ANALYSIS` | 12 | reviewed/caveat_only |

合计：96 条。

## 关键交付物

| 类别 | 交付物 |
| --- | --- |
| 范围文档 | `docs/research/phase37_trading_engineering_knowledge_scope.md` |
| 审计范围 JSON | `docs/audit/phase37_trading_engineering_knowledge_scope_for_audit.json` |
| 跨分支契约 | `docs/contracts/trading_ai_cross_branch_knowledge_contract.md` |
| 采集队列 | `docs/research/phase37_trading_engineering_research_task_queue.md` |
| 正式知识目录 | `codex-expert-kit/rag/knowledge/KB_01_QUANT_FOUNDATION/` 等 Phase 37 分区目录 |
| 正式聚合索引 | `codex-expert-kit/rag/indexes/knowledge_items.json` |
| Vue3 正式知识 fixture | `ui/src/data/formalKnowledgeItems.ts` |
| Vue3 候选 fixture | `ui/src/data/phase23Candidates.ts` |
| Vue3 知识树 fixture | `ui/src/data/knowledgeTreeNodes.ts` |
| 全量验证脚本 | `codex-expert-kit/rag/scripts/validate_phase37_full_runtime_linkage.py` |
| 全量验证报告 | `docs/reports/phase37_full_runtime_linkage_report.json` |

## 运行时验证

CEK-TA-450 已通过 `validate_phase37_full_runtime_linkage.py` 验证。

验证结果：

```text
gate_status: pass
expected_total: 96
actual_total: 96
review_status: reviewed = 96
machine_gate.default_guidance: caveat_only = 96
missing_sources_count: 0
local_path_leak_count: 0
forbidden_flag_hits: {}
```

验证覆盖：

```text
1. knowledge_items.json 能加载 Phase 37 全量 96 条 formal knowledge。
2. 每个分区数量与规划一致。
3. 所有条目均为 reviewed/caveat_only。
4. 所有条目均未开启 approved/default guidance/hard gate/risk threshold advice。
5. 所有条目均有 source_evidence。
6. formal knowledge 中无本机绝对路径泄漏。
7. Vue3 formal fixture 包含全量 96 条。
8. Trade Analysis 候选 fixture 保留 formal 回链。
9. KnowledgeTree fixture 包含 Phase 37 关键分支节点。
10. SearchLab/MCP 风格查询在每个分区均能命中。
```

## 边界与治理

Phase 37 知识只沉淀交易工程方法、证据边界、审计结构和跨分支 owner 约束，不输出：

```text
买卖点
仓位建议
杠杆建议
止损止盈价格
风险阈值数值
实盘执行许可
hard gate 交易放行
默认指导规则
```

Trading Engineering 负责交易规则本体；AI Engineering 只能通过 `knowledge_refs`、`reason_code_id`、`review_id`、`taxonomy_version` 等字段引用这些知识，不能复制改写成模型训练本体或交易执行规则。

## 测试与验收

已执行：

```text
python -m py_compile codex-expert-kit/rag/scripts/validate_phase37_full_runtime_linkage.py
python codex-expert-kit/rag/scripts/validate_phase37_full_runtime_linkage.py
python codex-expert-kit/rag/scripts/validate_phase37_trade_analysis_runtime_linkage.py
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
npm --prefix ui run build
```

结果：

```text
Phase 37 full runtime linkage: pass
Trade Analysis runtime linkage: pass
Knowledge pollution gate: pass
UTF-8 / mojibake gate: pass
Vue3 production build: pass
```

前端构建存在 Vite chunk 体积警告，但不影响本次知识索引、fixture 或运行时验证。

## 回滚方式

如发现某条 Phase 37 reviewed/caveat_only 知识存在来源、分类或冲突问题：

```text
1. 不删除候选源文件。
2. 将 formal knowledge 的 review_status 降回 draft 或 deprecated。
3. 将 machine_gate.default_guidance 设为 deny。
4. 将 candidate workflow 回到 needs_more_evidence。
5. 重建 knowledge_items.json 和 Vue3 fixture。
6. 重新执行 validate_phase37_full_runtime_linkage.py。
```

## 下一步

Phase 37 已完成 Trading Engineering 96 条 P0 知识闭环。后续建议：

```text
1. 继续 Phase 44 的 AI 交易者项目断点审计，把实际方案中的缺口反向映射到 Trading / AI / Database / Memory 分支。
2. 对 Phase 37 知识做定期复审，尤其是交易所规则、数据源 schema、broker API、市场制度和监管文件。
3. 根据外接项目真实使用反馈，再进入 Phase 37 P1 扩展，而不是把 reviewed/caveat_only 直接升级为 approved。
```
