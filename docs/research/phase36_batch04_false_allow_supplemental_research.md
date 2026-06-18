# Phase 36 第四批 false_allow needs_more_evidence 补证采集记录

## 任务信息

```text
Phase: Phase 36 AI Engineering gating/scoring 知识扩充
任务 ID: CEK-TA-217
下游任务: CEK-TA-218
创建日期: 2026-06-09
状态: done
```

## 目标

为第四批审计中唯一 `needs_more_evidence` 的 `gating.false_allow_more_dangerous_than_false_block.v1` 补充直接来源、重写 statement，并导出二次审计包。

本任务只处理候选补证，不把候选转成正式知识，不设置 `reviewed`，不设置 `approved`，也不允许进入默认指导。

## 重写后的边界

```text
在 CEK-TA hard-gate 交易 LLM 工作流中，false allow 默认按更高严重度处理；但这不是跨所有交易场景的普适事实，只有在 approved risk ledger、cost matrix 和 Trading Engineering owner 未定义覆盖模型时才作为默认风险偏好。
```

## 联网来源

| source_id | 来源 | 用途 |
| --- | --- | --- |
| `src_elkan_cost_sensitive_learning` | [The Foundations of Cost-Sensitive Learning](https://cseweb.ucsd.edu/~elkan/rescale.pdf) | 该论文讨论不同误分类错误有不同惩罚，并强调 cost matrix 需要经济一致性；可支撑 false allow/false block 不能靠通用准确率判断，而要由成本矩阵定义。 |
| `src_sklearn_cost_sensitive_threshold` | [Post-tuning the decision threshold for cost-sensitive learning](https://scikit-learn.org/stable/auto_examples/model_selection/plot_cost_sensitive_learning.html) | scikit-learn 官方示例说明可用 misclassification cost matrix 调整决策阈值，支持阈值应由错误成本而不是单一 accuracy 决定。 |
| `src_nist_ai_rmf_core_manage_impact_likelihood` | [AI RMF Core - Manage risks based on impact, likelihood, and resources](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) | NIST AI RMF Core 支持按影响、可能性和资源优先处理已记录 AI 风险，可支撑 risk ledger 需要记录 severity、likelihood 和 owner。 |
| `src_openai_usage_policies_high_impact_human_review` | [Usage policies | OpenAI](https://openai.com/policies/usage-policies/) | OpenAI usage policies 对金融等高影响自动化决策强调安全边界和 human review，可作为 LLM hard-gate 场景不能无审计默认放行的 supporting source。 |
| `src_finra_regulatory_notice_15_09` | [Regulatory Notice 15-09: Guidance on Effective Supervision and Control Practices for Firms Engaging in Algorithmic Trading Strategies](https://www.finra.org/rules-guidance/notices/15-09) | FINRA 15-09 支持算法交易需要监督、测试、控制、风险管理和治理；可作为交易自动化 hard-gate 风险边界的行业治理来源。 |

## 建议字段

```text
risk_ledger_id
risk_event_id
gate_context
false_allow_severity
false_block_severity
cost_matrix_ref
cost_model_ref
risk_owner
trading_engineering_owner
override_reason
fallback_action
review_queue_id
reviewed_at
```

## 审计重点

```text
1. 是否已经从绝对断言改成 CEK-TA hard-gate 默认风险偏好。
2. 是否有 cost-sensitive learning / cost matrix 直接来源支撑。
3. 是否明确 risk ledger 和 Trading Engineering owner 可覆盖默认 severity。
4. 是否没有把具体交易阈值、仓位、止损止盈或订单执行逻辑写入 AI Engineering。
```
