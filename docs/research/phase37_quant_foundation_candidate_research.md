# Phase 37 Quant Foundation 候选研究记录

生成日期：2026-06-11

## 范围

本文件记录 Phase 37 首批 `P37-A` Quant Foundation 12 条候选知识的来源选择、分类和边界。所有条目仍是 candidate，不是 formal reviewed，不是 approved，不进入默认指导。

## 来源原则

```text
1. 优先使用专业机构、监管机构、论文、教材或官方资料。
2. 教育类和供应商资料只能作为 supporting source。
3. R/R、胜率、R multiple、仓位、成本、杠杆等规则必须写明适用边界和不适用场景。
4. 不输出买卖点、仓位、杠杆、止损止盈或实盘执行建议。
```

## 候选清单

| 任务 | 候选 | 节点 | 来源数 | 主来源数 | 状态 |
| --- | --- | --- | --- | --- | --- |
| P37-A-Q01 | `kb_01_quant_foundation.expected_value_definition.v1` | `kt.quant_foundation` | 3 | 1 | candidate_ready |
| P37-A-Q02 | `kb_01_quant_foundation.r_multiple_definition.v1` | `kt.quant_foundation.position_sizing` | 4 | 2 | candidate_ready |
| P37-A-Q03 | `kb_01_quant_foundation.risk_reward_boundary.v1` | `kt.quant_foundation` | 4 | 1 | candidate_ready |
| P37-A-Q04 | `kb_01_quant_foundation.cost_adjusted_expectancy_required.v1` | `kt.quant_foundation` | 3 | 2 | candidate_ready |
| P37-A-Q05 | `kb_01_quant_foundation.win_rate_not_enough.v1` | `kt.quant_foundation` | 4 | 2 | candidate_ready |
| P37-A-Q06 | `kb_01_quant_foundation.position_sizing_requires_risk_unit.v1` | `kt.quant_foundation.position_sizing` | 4 | 2 | candidate_ready |
| P37-A-Q07 | `kb_01_quant_foundation.leverage_amplifies_drawdown.v1` | `kt.quant_foundation.position_sizing` | 4 | 4 | candidate_ready |
| P37-A-Q08 | `kb_01_quant_foundation.signal_decision_execution_separation.v1` | `kt.quant_foundation.signal_flow` | 3 | 3 | candidate_ready |
| P37-A-Q09 | `kb_01_quant_foundation.trade_frequency_vs_quality_boundary.v1` | `kt.quant_foundation` | 4 | 4 | candidate_ready |
| P37-A-Q10 | `kb_01_quant_foundation.edge_requires_out_of_sample_evidence.v1` | `kt.quant_foundation` | 4 | 4 | candidate_ready |
| P37-A-Q11 | `kb_01_quant_foundation.sample_size_and_regime_caveat.v1` | `kt.quant_foundation` | 3 | 3 | candidate_ready |
| P37-A-Q12 | `kb_01_quant_foundation.no_profit_claim_without_costs.v1` | `kt.quant_foundation` | 4 | 3 | candidate_ready |

## 下游

```text
docs/audit/phase37_quant_foundation_candidate_audit_package_20260611.json
```
