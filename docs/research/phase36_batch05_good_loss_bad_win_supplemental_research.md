# Phase 36 第五批 good_loss / bad_win 补证采集记录

## 目标

为第五批审计中 2 条 needs_more_evidence 候选补充证据，并把 good_loss / bad_win 从交易判断事实改写为 CEK-TA 内部标签 reason-code / review_category 规则。

## 补证结论

1. `good_loss / bad_win` 不应写成跨策略通用交易事实，也不能由 PnL 自动推出。
2. 可以作为 CEK-TA 内部标签分类：用于分离 PnL outcome、过程质量、风险合规、规则合规、证据质量和 owner review。
3. 正式入库前必须保留 Trading Engineering/domain owner guideline、匿名案例、reason-code taxonomy 和 adjudication 字段。

## 补充来源

- Baron & Hershey, Outcome Bias in Decision Evaluation：支撑结果不能替代决策质量评估。
- FINRA Regulatory Notice 15-09：支撑算法交易监督、测试、风险控制和合规维度。
- Label Studio human consensus / inter-annotator agreement：支撑含糊标签需要共识和审定。
- TensorFlow Data Validation：支撑标签字段 schema、skew/drift 和泄漏检查。
- CMC Markets trading journal：作为交易日志实践参考，支撑过程/结果分离记录。

## 边界

AI Engineering 只定义标签字段、reason-code、review 状态、审计链和回灌边界；具体交易语义、策略执行、风控阈值和订单逻辑必须路由到 Trading Engineering。
