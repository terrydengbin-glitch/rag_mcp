# AI Engineering Scoring Rubric 维度边界契约

## 目标

本契约定义 AI Engineering 中交易 LLM gating/scoring rubric 的细分维度边界，避免把市场状态、setup、风险收益、交易规则和阈值本体错误沉淀到 AI Engineering。

AI Engineering 可以沉淀 rubric 字段、引用关系、缺失状态、reason codes、证据要求、审计状态和 UI 展示字段；Trading Engineering 或外部项目 owner 负责定义交易语义本体。

## 总边界

```text
AI Engineering 负责：
- scoring_rubric 输出 schema
- reason_code 受控枚举
- evidence_refs / source_refs
- *_ref 引用字段
- unknown / missing / conflict 状态
- review_owner / owner_review_status
- fallback_action
- audit_event_id

Trading Engineering 负责：
- 市场 regime taxonomy
- setup 定义和策略版本解释
- risk/reward 语义、成本函数、风险预算和机会成本
- rule registry、policy registry 和交易规则解释
- 具体阈值、仓位、止损止盈、订单执行和实盘权限
```

## 五个受控维度

| 维度 | AI Engineering 允许保存 | 必须外部引用 | 缺失时动作 |
| --- | --- | --- | --- |
| `market_regime_fit` | `market_regime_ref`、`regime_fit_status`、`reason_codes`、`evidence_refs` | `regime_label_policy` 或 `market_regime_taxonomy` | `needs_review` |
| `risk_reward_quality` | `risk_context_ref`、`reward_context_ref`、`cost_matrix_ref`、`reason_codes` | Trading Engineering 的 risk/reward contract | `needs_more_evidence` |
| `rule_compliance` | `rule_refs`、`policy_refs`、`rule_compliance_status`、`reason_codes` | rule registry 或 policy registry | `needs_review` 或 `block_default_guidance` |
| `setup_quality` | `setup_quality_ref`、`strategy_version_ref`、`setup_quality_status`、`reason_codes` | setup taxonomy 或 strategy version contract | `needs_more_evidence` |
| `uncertainty_penalty` | `confidence_status`、`calibration_report_id`、`uncertainty_reason_code`、`fallback_action` | calibration report 或 uncertainty policy | `neutral`、`needs_review` 或 `block_default_guidance` |

## 禁止事项

```text
1. 不得让 LLM 自行发明 market regime、setup、交易规则、风险预算或阈值。
2. 不得把 rubric 分数直接当成最终 allow/block。
3. 不得把具体 K 线形态、买卖点、仓位、止损止盈、订单动作写入 AI Engineering rubric 知识。
4. 不得把项目私有策略参数、账户字段、订单样本或未脱敏交易记录写入通用知识库。
5. 不得用无来源的自然语言解释替代 rule_ref、setup_ref、risk_context_ref 或 calibration_report_id。
```

## 二审导出要求

补证后的候选二审包必须要求审计者确认：

```text
1. statement 是否已经对齐具体 rubric 维度。
2. source_refs 是否足够支撑该维度的工程边界。
3. 具体交易语义是否仍由 Trading Engineering / project owner 提供。
4. 缺失外部引用时是否会降级到 needs_review、neutral 或 block_default_guidance。
5. accepted_for_draft 是否仍只允许转 formal reviewed，不得进入 approved。
```
