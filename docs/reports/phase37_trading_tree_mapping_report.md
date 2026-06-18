# Phase 37 Trading 分支知识树映射检查报告

生成日期：2026-06-11

## 结论

首批 P37-A Quant Foundation 候选均归属 `KB_01_QUANT_FOUNDATION`，主节点挂载在 `kt.quant_foundation` 或其现有 Level 3 子节点。当前不修改 `knowledge_tree.md`，原因是现有树已包含 Quant Foundation、Signal Flow、Position Sizing，并且 `kt.quant_foundation.item_mapping.allowed_subdomains` 已覆盖 foundation、signal_flow、sizing、risk_reward、cost。

## 映射统计

| 节点 | 候选数 | 说明 |
| --- | ---: | --- |
| `kt.quant_foundation` | 8 | Phase 37 首批 Quant Foundation 候选挂载节点 |
| `kt.quant_foundation.position_sizing` | 3 | Phase 37 首批 Quant Foundation 候选挂载节点 |
| `kt.quant_foundation.signal_flow` | 1 | Phase 37 首批 Quant Foundation 候选挂载节点 |

## 边界

```text
1. K 线、fill model、订单状态机、实盘风控本体不放入 Quant Foundation。
2. AI Engineering 只能引用这些 Trading Engineering 规则。
3. 后续如 UI 需要更细的 L3 导航，可单独新增 EV / Risk Reward / Cost 子节点任务。
```
