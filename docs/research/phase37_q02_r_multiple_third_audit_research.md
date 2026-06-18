# Phase 37 P37-A-Q02 R-multiple 三审补证记录

生成日期：2026-06-11

## 目标

补齐 `P37-A-Q02 / quant_foundation.r_multiple_definition.v1` 的两个二审阻断点：

```text
1. R-multiple 本体来源不足，不能只依赖 vendor/教育页面。
2. 主分类不应继续放在 position_sizing，应调整为 risk_normalized_metrics，position_sizing 只作为初始风险单位依赖。
```

## 本轮处理

```text
1. 新增 `kt.quant_foundation.risk_normalized_metrics` 知识树三级节点。
2. 将候选 canonical_node_id 改为 `kt.quant_foundation.risk_normalized_metrics`。
3. 补充 Van Tharp 书籍元数据、Position Sizing 书籍元数据、SQN/R-multiple distribution 资料、系统交易者 R-multiple/expectancy 资料和 Van Tharp Institute 训练线索。
4. 保留 candidate-only 边界，不创建 reviewed、approved、default guidance 或 hard gate。
```

## 三审入口

```text
docs/audit/phase37_q02_r_multiple_third_audit_package_20260611.json
```
