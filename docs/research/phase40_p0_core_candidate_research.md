# Phase 40 P0-Core 候选知识来源采集记录

生成日期：2026-06-10

## 结论

本轮按 Phase 40 P0-Core 矩阵生成候选知识 18 条，跳过已存在候选 0 条。

本轮只生成 candidate，不进入 formal reviewed，不进入 approved，也不会作为默认指导。

## 主要来源族

| 来源族 | 用途 |
| --- | --- |
| Evidently / TFDV / whylogs | 数据漂移、预测漂移、数据质量、日志和监控 |
| scikit-learn calibration / Brier / cost-sensitive threshold | 概率校准、Brier/ECE、成本阈值 |
| MLflow Model Registry | candidate/champion 版本、别名、生命周期和发布证据 |
| Argo Rollouts | canary、progressive delivery、停止条件和灰度发布语义 |
| OpenAI / Hugging Face TRL | prompt、RAG、SFT/LoRA、LLM 训练和评估触发边界 |
| NIST AI RMF | AI 风险治理、度量、管理和人类审批边界 |
| Logged bandit / OPE 论文 | 被阻断/未执行候选的反事实和日志反馈边界 |

## 边界

本轮没有采集 K 线、fill model、订单状态机、实盘风控阈值或交易所执行适配器本体知识。这些内容仍归 Trading Engineering。

