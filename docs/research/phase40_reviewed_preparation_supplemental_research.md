# Phase 40 Reviewed Preparation 补证研究记录

生成日期：2026-06-10
对应任务：CEK-TA-317

## 范围

本记录只服务于 Phase 40 reviewed preparation 二审后仍需补证的 5 条候选：

```text
P40-C01 allow/block/skip/human_review 全候选记录
P40-C02 FeedbackRecord 可回放字段
P40-C07 drift 类型与 calibration drift
P40-C12 threshold policy 与人审预算
P40-C15 release manifest、rollback target、kill switch
```

边界：

```text
本次只补来源、契约和三审包。
不生成 formal reviewed。
不设置 approved。
不允许 default guidance。
不允许 hard gate。
不把 K 线、fill model、订单状态机、实盘风控本体混入 AI Engineering。
```

## 来源研究结论

### P40-C01

补证方向：

```text
logged bandit / OPE 要求记录历史策略下的 context、action、probability/cost/reward 或 logged feedback。
CEK-TA Feedback Dataset Contract 要求 allow、block、skip、human_review、error 全候选记录。
blocked/skipped 的 outcome 是反事实或未执行状态，不等于扩大实盘执行。
```

新增来源：

| source_id | 来源 | 用途 |
| --- | --- | --- |
| `src_vowpal_wabbit_contextual_bandit` | Vowpal Wabbit contextual bandit official docs | 支撑 action、cost、probability 的 logged bandit 数据结构 |
| `src_open_bandit_pipeline_docs` | Open Bandit Pipeline docs | 支撑 logged bandit feedback 和 OPE |
| `src_doubly_robust_policy_evaluation` | Dudík, Langford, Li, Doubly Robust Policy Evaluation and Learning | 支撑 contextual bandit 历史数据中 context、action、reward 和 past policy |
| `src_cek_ta_phase40_feedback_dataset_contract` | CEK-TA Feedback Dataset Contract | 支撑 CEK-TA 全候选记录字段 |

### P40-C02

补证方向：

```text
训练和推理必须使用 point-in-time correct / decision-time available features。
post-trade outcome 只能作为 outcome_ref 和 observation window，不能进入 scorer 输入。
FeedbackRecord 必须回链 scorer、LLM audit、final gate、后验 outcome 和版本号。
```

新增来源：

| source_id | 来源 | 用途 |
| --- | --- | --- |
| `src_feast_point_in_time_joins` | Feast point-in-time joins | 支撑按历史时间点复现 feature state，避免未来信息泄漏 |
| `src_tecton_training_data` | Tecton constructing training data | 支撑 training events/key/timestamp 构造训练数据 |
| `src_databricks_point_in_time` | Databricks point-in-time feature joins | 支撑用标签时间可见的 feature values 防止 leakage |
| `src_cek_ta_phase40_feedback_dataset_contract` | CEK-TA Feedback Dataset Contract | 支撑 FeedbackRecord 字段契约 |

### P40-C07

补证方向：

```text
feature drift、label/target drift、score distribution drift 和 calibration drift 必须分开记录。
calibration drift 需要通过 calibration curve、reliability diagram、Brier/ECE 等概率校准证据判断。
drift alert 只能触发 investigation/review/retraining_review，不能自动 hard gate。
```

新增来源：

| source_id | 来源 | 用途 |
| --- | --- | --- |
| `src_sklearn_calibration` | scikit-learn Probability calibration | 支撑概率校准 |
| `src_sklearn_calibration_curve_example` | scikit-learn calibration curves / reliability diagrams | 支撑 reliability diagram |
| `src_sklearn_calibration_display` | scikit-learn CalibrationDisplay | 支撑 predicted probability bin 与 positive fraction |
| `src_cek_ta_phase40_drift_retraining_contract` | CEK-TA Drift Retraining Recalibration Contract | 支撑 calibration_drift_metric 和 drift action 边界 |

### P40-C12

补证方向：

```text
threshold policy 必须绑定 cost_matrix、calibrator、review_budget、queue capacity 和 owner approval。
人审预算不足不能自动 allow/block。
超预算应触发 freeze_threshold_change、safe_mode、owner_review 或 collect_more_evidence。
```

新增来源：

| source_id | 来源 | 用途 |
| --- | --- | --- |
| `src_aws_augmented_ai_human_review` | Amazon A2I human review workflows | 支撑 ML 应用中的 human review loop |
| `src_aws_augmented_ai_create_workflow` | Amazon A2I create human review workflow | 支撑人审 workflow 和 workforce 配置 |
| `src_cek_ta_phase40_review_budget_threshold_policy_contract` | CEK-TA Review Budget Threshold Policy Contract | 支撑预算、队列和溢出契约 |
| `src_cek_ta_phase40_drift_retraining_contract` | CEK-TA Drift Retraining Recalibration Contract | 支撑 ThresholdStabilityReport |

### P40-C15

补证方向：

```text
release manifest 必须覆盖 rollback target、kill switch、secret scan、rollback drill 和人工审批。
secret scan 只能记录扫描状态和告警引用，不保存密钥正文。
kill switch 只作为发布控制，不执行交易策略逻辑。
```

新增来源：

| source_id | 来源 | 用途 |
| --- | --- | --- |
| `src_google_sre_canarying` | Google SRE canarying releases | 支撑小流量发布和发布风险控制 |
| `src_github_secret_scanning` | GitHub secret scanning docs | 支撑发布前密钥扫描 |
| `src_nist_ai_rmf_manage` | NIST AI RMF Manage Playbook | 支撑部署后监控、响应、恢复和变更管理 |
| `src_fca_algo_trading_controls` | FCA Algorithmic Trading Compliance in Wholesale Markets | 支撑算法交易控制、kill functionality 和风险控制清单 |
| `src_cek_ta_phase40_release_manifest_kill_switch_contract` | CEK-TA Release Manifest Kill Switch Contract | 支撑 release safety checklist 字段 |

## 三审请求

请外部审计对 5 条候选逐条判断：

```text
accepted_for_draft
needs_more_evidence
rejected
```

即使三审给出 `accepted_for_draft`，也只允许后续 Codex 生成 `formal reviewed + caveat_only`，不得直接 `approved`、`default_guidance_allowed` 或 `hard_gate_allowed`。
