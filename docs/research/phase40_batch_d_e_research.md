# Phase 40 Batch D/E 候选知识来源采集记录

生成日期：2026-06-10

## 结论

本轮按 Phase 40 Batch D/E 矩阵生成候选知识 18 条，跳过已存在候选 0 条。

本轮只生成 candidate，不进入 formal reviewed，不进入 approved，也不会作为默认指导。

## 覆盖范围

| 批次 | 数量 | 说明 |
| --- | ---: | --- |
| Batch D / P0-Extended | 12 | replayable audit trail、标签版本、drift root cause、事故触发、校准分桶、风险指标、shadow/paper 差异、rollback freeze、RAG 回归、人审审计、confidence 边界、监控看板 |
| Batch E / P1 | 6 | 长尾采样、标签仲裁、混合再训练、拒绝实验追踪、组合回滚、prompt/RAG/model eval 分离 |

## 主要来源族

| 来源族 | 用途 |
| --- | --- |
| Snowflake / MLflow / Google Data Cards | 预测日志、模型 lineage、数据集/标签版本和发布元数据 |
| Fiddler / DataRobot / Arize | drift root cause、监控指标、dashboard 和模型可观测性 |
| scikit-learn | 校准曲线、reliability diagram、分桶可靠性 |
| AWS SageMaker / Microsoft Shadow Testing | shadow/paper 验证和非生产等价边界 |
| Coalition for Secure AI / NIST AI RMF | AI incident response、rollback、治理和风险边界 |
| Evidently / Google Cloud / Promptfoo / Arize | RAG 检索评测、测试集、回归和检索/生成分离 |
| Label Studio / IBM Watson Knowledge Studio | 人工标注复核、冲突处理、adjudication 和 gold set |
| Long-tailed learning survey / tail sampling docs | 长尾覆盖和选择性采样边界 |

## 边界

本轮没有采集 K 线、fill model、订单状态机、实盘风控阈值或交易所执行适配器本体知识。这些内容仍归 Trading Engineering。

