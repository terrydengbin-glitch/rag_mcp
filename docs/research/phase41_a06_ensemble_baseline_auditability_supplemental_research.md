# Phase 41 P41-A06 baseline 与可审计性补证记录

生成日期：2026-06-11

## 任务目标

为 `P41-A06` 补齐三审前必须具备的两类证据：

1. `single-model baseline comparison report`：证明 ensemble 不是默认选项，而是在单模型 baseline 不足时才作为增强候选。
2. `auditability impact report`：证明 ensemble 引入后不会破坏解释、trace、校准、阈值、回滚和 final gate 分责。

## 上下游

- 上游：`CEK-TA-336` 的 reviewed-preparation 再审结果，P41-A06 因需补充 baseline/auditability 证据继续 `needs_more_evidence`。
- 下游：外部三审 JSON；如果三审通过，只能进入 `accepted_for_draft`，再由后续任务决定是否沉淀 formal reviewed/caveat_only。

## 来源与证据维度

| 来源 | 类型 | 维度 | 用法 | 边界 |
| --- | --- | --- | --- | --- |
| Rules of Machine Learning - Google for Developers | official_doc | single_model_baseline_comparison | Google ML engineering guidance emphasizes robust infrastructure, simple first models, baseline metrics, and delaying added complexity until simpler approaches are exhausted. | This supports the engineering baseline requirement; it does not prove any trading performance edge. |
| Ensemble methods - scikit-learn documentation | official_doc | ensemble_as_enhancement | scikit-learn frames ensemble methods as combining base estimators to improve generalizability or robustness over a single estimator. | The source supports ensemble motivation, not automatic adoption or final gate authority. |
| Stacked generalization - scikit-learn documentation | official_doc | ensemble_validation_complexity | scikit-learn describes stacking as using base-estimator predictions as inputs to a final estimator trained through cross-validation, which adds validation and trace complexity. | This supports added audit complexity; it does not prescribe a CEK-TA production architecture. |
| AI Risks and Trustworthiness - NIST AI Resource Center | governance_framework | auditability_impact_report | NIST distinguishes transparency, explainability, and interpretability and links explainable systems to easier debugging, monitoring, documentation, audit, and governance. | This supports auditability criteria; CEK-TA still needs project-specific audit reports before adoption. |
| Phase 41 hybrid scoring runtime contract | internal_contract | final_gate_boundary | CEK-TA Phase 41 runtime contract separates scorer, calibrator, Qwen3 audit assistant, RAG, and deterministic final gate responsibilities. | Internal contract evidence must be paired with external sources for professional knowledge claims. |
| Phase 41 tabular and LLM training data contract | internal_contract | single_model_baseline_comparison | CEK-TA Phase 41 data contract defines split manifests, feature schema, label policy, calibration, threshold, and model registry evidence required for scorer comparison. | Internal contract evidence is a CEK-TA acceptance boundary, not an external proof of model performance. |

## 补证后的最低审计要求

### single-model baseline comparison report

必须至少说明：

- 单模型候选：rule baseline、Logistic Regression、LightGBM/XGBoost 等。
- 同一时间切分、同一 feature schema、同一 label policy、同一 calibration/threshold policy。
- 主指标、业务成本维度、误放行/误阻断、校准质量、延迟、模型复杂度和回滚复杂度。
- 为什么单模型 baseline 不足，以及 ensemble 解决的是哪类不足。

### auditability impact report

必须至少说明：

- ensemble 后 top_features / attribution / reason code 是否仍可解释和复核。
- base estimator、final estimator、calibrator、threshold policy、Qwen3 prompt、RAG index、release manifest 是否可追踪。
- 失败时是否能回退到单模型 baseline 或 deterministic final gate 的人工复核路径。
- 是否新增无法接受的延迟、监控、文档、审计或治理复杂度。

## 边界

- 本条仍是候选知识，三审通过也只能进入 `accepted_for_draft`。
- 不允许创建 `formal reviewed`、`approved`、`default guidance` 或 `hard gate`。
- ensemble 只做 scorer/review-priority 增强，不得绕过 calibrator、threshold policy 或 deterministic final gate。
- Trading PnL、K 线、fill model、slippage、仓位、止损止盈和实盘执行继续路由到 Trading Engineering。

## 产物

- 候选：`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/cand_20260610_phase41_p41_a06_baseline_001.json`
- 三审包：`docs/audit/phase41_a06_single_model_baseline_third_audit_package_20260611.json`
- 执行报告：`docs/reports/phase41_a06_single_model_baseline_third_audit_package_report.json`
