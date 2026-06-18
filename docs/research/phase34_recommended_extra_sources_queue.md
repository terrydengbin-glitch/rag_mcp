# Phase 34 Recommended Extra Sources Queue

## 目标

本队列承接 `recommended_extra_sources` 字段中的待核验来源建议。它们用于后续联网核验和来源增强，不是正式 `source_evidence`。

## 使用规则

```text
1. status=proposed 的来源不得作为正式证据。
2. 只有经过联网核验、来源摘要、适用边界和版权检查后，才能移动到 source_evidence。
3. 移动到 source_evidence 后必须从 recommended_extra_sources 移除或标记 rejected，并写入 decision_log。
4. 不得用 recommended_extra_sources 提升 review_status 或 machine_gate。
```

## 当前队列

| 主题 | 推荐来源 | 目的 | 状态 |
| --- | --- | --- | --- |
| Backtest / data snooping | White, 2000, A Reality Check for Data Snooping | 补强 data snooping、多重测试和样本外检验边界 | proposed |
| Backtest / overfitting | Bailey et al., The Probability of Backtest Overfitting | 补强回测过拟合概率、参数搜索和模型选择风险 | proposed |
| K-line / technical rule boundary | Sullivan, Timmermann, White, 1999, Data-Snooping, Technical Trading Rule Performance, and the Bootstrap | 补强技术交易规则的数据窥探和 bootstrap 检验边界 | proposed |
| RAG governance | NIST AI Risk Management Framework | 补强 AI 系统风险治理、可追踪性和文档化边界 | proposed |

## 下游任务

后续应通过专业知识采集流水线创建研究任务：

```text
1. 查询来源原文或官方入口。
2. 记录 source_url、publisher、published_at、accessed_at、version。
3. 写 evidence_summary。
4. 检查与现有知识是否重复或冲突。
5. 通过后再写入对应 knowledge item 的 source_evidence。
```
