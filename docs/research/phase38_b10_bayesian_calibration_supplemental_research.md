# Phase 38 B10 Bayesian Calibration 补证记录

## 目标

为二审保留的 B10 单独补充 Bayesian calibration / Bayesian uncertainty calibration 直接来源。本记录只用于三审准备，不代表 reviewed、approved、default guidance 或 hard gate。

## 候选

- candidate_id: `cand_20260610_phase38_p38_b10_conformal_bayesian_calibration_001`
- research_task_id: `P38-B10`
- normalized_claim: `phase38.conformal_bayesian_calibration.v1`
- statement: conformal / Bayesian calibration 只能作为增强层

## 新增来源

### src_pmlr_kuleshov_calibrated_regression_bayesian_uncertainty

- 标题：Accurate Uncertainties for Deep Learning Using Calibrated Regression
- 链接：https://proceedings.mlr.press/v80/kuleshov18a.html
- 类型：paper
- 证据摘要：Kuleshov et al. state that Bayesian methods provide an uncertainty framework, but approximate inference and model misspecification can make Bayesian uncertainty estimates inaccurate; they propose calibrated regression that can calibrate Bayesian/probabilistic uncertainty estimates given enough data.

### src_aaai_bayesian_binning_into_quantiles

- 标题：Obtaining Well Calibrated Probabilities Using Bayesian Binning
- 链接：https://ojs.aaai.org/index.php/AAAI/article/view/9602
- 类型：paper
- 证据摘要：The AAAI paper presents Bayesian Binning into Quantiles as a non-parametric Bayesian calibration method for classifier probability estimates and compares calibration performance against common post-processing methods.

## 补丁摘要

B10 已补 Bayesian calibration / Bayesian uncertainty calibration 直接来源：PMLR calibrated regression 支撑 Bayesian/probabilistic uncertainty estimates 需要校准；AAAI Bayesian Binning into Quantiles 支撑 Bayesian classifier probability calibration。本条仍只能作为 calibration/uncertainty 增强层，不能替代 deterministic final gate。

## 边界

```text
1. B10 仍是 candidate，等待三审。
2. 不直接 reviewed，不 approved，不进入 default guidance，不允许 hard gate。
3. calibration / uncertainty layer 只作为模型风险和人工复核辅助，不能替代确定性风控。
```
