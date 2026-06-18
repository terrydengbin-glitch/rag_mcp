# Phase 37 Quant Foundation 补证研究记录

生成日期：2026-06-11

## 范围

本文件只记录首轮审计中 3 条 `needs_more_evidence` 候选的补证，不创建正式知识、不创建 reviewed、不创建 approved、不进入默认指导。

## 补证清单

| 任务 | 候选 | 补证重点 | 来源数 |
| --- | --- | --- | ---: |
| P37-A-Q02 | `cand_20260611_phase37_r_multiple_definition_001` | 保留主归属 kt.quant_foundation.position_sizing，因为 R multiple 依赖初始风险单位；增加 kt.trade_analysis 与 kt.backtest.metrics 作为 related_nodes。；把 R multiple 定位为 risk-normalized performance metric，不再暗示其可替代成本、滑点、样本外或风控审计。；补充 Van Tharp 来源线索和多家交易绩效教育来源；仍要求二审确认是否足以进入 accepted_for_draft。 | 5 |
| P37-A-Q08 | `cand_20260611_phase37_signal_decision_execution_separation_001` | 补充 FIX/FIXimate/OnixS Execution Report 来源，直接支撑订单状态、成交、拒单、费用和执行回报与信号/决策分层记录的必要性。；将 claim 强化为事件链审计规则：signal、decision、order intent、execution report、fill report、trade result 必须可追踪分层。；保留不输出下单许可或执行建议的边界。 | 6 |
| P37-A-Q09 | `cand_20260611_phase37_trade_frequency_vs_quality_boundary_001` | 按审计意见缩窄 general claim，不再泛化为所有市场频率上升必然放大风险。；补 TCA、market impact、factor strategy turnover cost 和 execution cost 来源。；将频率质量边界与 cost/TCA 关联，避免把交易次数当作交易质量指标。 | 7 |

## 二审入口

```text
docs/audit/phase37_quant_foundation_supplemental_reaudit_package_20260611.json
```
