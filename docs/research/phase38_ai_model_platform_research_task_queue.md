# Phase 38 ResearchIngestionTask 队列

生成日期：2026-06-10
状态：queue draft
对应任务：CEK-TA-269

## 队列契约

每个任务必须按以下结构执行：

```text
task_id
knowledge_topic_id
target_canonical_node_id
priority
claim_type
query_plan
required_source_types
minimum_source_count
acceptance_gate
boundary_check
downstream
```

默认门槛：

```text
P0-Core: 至少 3 个来源，其中至少 1 个 official_doc 或 research_paper。
P0-Extended: 至少 2 个来源，其中至少 1 个 official_doc、framework_doc 或 research_paper。
P1: 至少 2 个来源，可以包含 engineering_article，但不能只有博客。
```

## P0-Core 队列

```text
P38-RT-001 -> P38-A01 scorer / soft gate / final gate 必须分权
P38-RT-002 -> P38-A02 deterministic rule baseline 必须先建立
P38-RT-003 -> P38-A03 Logistic Regression 作为透明 baseline
P38-RT-004 -> P38-A04 LightGBM 只能作为候选 scorer
P38-RT-005 -> P38-A05 XGBoost 应作为 strong baseline
P38-RT-006 -> P38-A06 meta-labeling 只能过滤候选
P38-RT-007 -> P38-A07 numeric scorer 输出不是最终交易动作
P38-RT-008 -> P38-B01 scorer 概率必须校准
P38-RT-009 -> P38-B02 calibrator 不得使用 scorer 训练集
P38-RT-010 -> P38-B03 Brier score 必须作为概率质量指标
P38-RT-011 -> P38-B04 reliability diagram 必须输出
P38-RT-012 -> P38-B05 threshold 不得固定 0.5
P38-RT-013 -> P38-B06 false allow / false block 必须进入 cost matrix
P38-RT-014 -> P38-B07 threshold_policy_version 必须进入 trace
P38-RT-015 -> P38-C01 每个样本必须有 decision_time
P38-RT-016 -> P38-C02 每个特征必须有 feature_available_time
P38-RT-017 -> P38-C03 feature_available_time 晚于 decision_time 必须阻断
P38-RT-018 -> P38-C04 post-trade outcome 不得进入 scorer 输入
P38-RT-019 -> P38-C05 label_observation_end_time 必须声明
P38-RT-020 -> P38-C06 feature lineage 必须记录 source_object
P38-RT-021 -> P38-C07 training-serving parity test 必须存在
P38-RT-022 -> P38-D01 LLM audit assistant 必须输出 strict JSON schema
P38-RT-023 -> P38-D02 LLM recommendation 不能等于 final gate decision
P38-RT-024 -> P38-D03 knowledge_refs 必须解析到 formal index
P38-RT-025 -> P38-D04 无来源或 no-hit 必须 abstain / neutral
P38-RT-026 -> P38-D05 unsupported_claims 不为空时不得默认放行
P38-RT-027 -> P38-D06 reason_codes 必须来自受控 taxonomy
P38-RT-028 -> P38-E01 offline eval 只能评估已执行交易样本
P38-RT-029 -> P38-E02 blocked trade 不能直接标注为亏损
P38-RT-030 -> P38-E03 hard gate 前必须 shadow mode
P38-RT-031 -> P38-E04 paper/replay 必须声明 fill/cost 假设来自 Trading
P38-RT-032 -> P38-E05 OPE 必须声明 behavior policy 和目标策略假设
P38-RT-033 -> P38-E06 human_review_precision 必须作为 POC 指标
P38-RT-034 -> P38-F01 release_manifest 必须绑定版本
P38-RT-035 -> P38-F02 model registry 必须记录 model_version
P38-RT-036 -> P38-F03 dataset_hash 和 split_manifest_hash 必须进入发布记录
P38-RT-037 -> P38-F04 rollback_target 必须在上线前定义
P38-RT-038 -> P38-F05 hard gate 开启必须有 owner approval
P38-RT-039 -> P38-F06 kill switch policy 必须纳入 release_manifest
P38-RT-040 -> P38-G01 scoring/gating 任务必须主动检索 CEK-TA
P38-RT-041 -> P38-G02 RAG context 默认是不可信输入
P38-RT-042 -> P38-G03 machine_gate 和 review_status 必须过滤默认指导
```

## P0-Extended 队列

```text
P38-RT-043 -> P38-A08 CatBoost 仅在类别特征占比高时条件引入
P38-RT-044 -> P38-A09 feature attribution 只能辅助调试
P38-RT-045 -> P38-B08 校准必须按 strategy/regime/horizon 切片检查
P38-RT-046 -> P38-B09 calibration drift 必须进入 shadow 监控
P38-RT-047 -> P38-C08 feature schema registry 必须版本化
P38-RT-048 -> P38-C09 data quality expectation suite 应覆盖核心字段
P38-RT-049 -> P38-D07 RAG + prompt baseline 必须先于 SFT
P38-RT-050 -> P38-D08 SFT LoRA 仅用于稳定输出 schema 和 reason code
P38-RT-051 -> P38-D09 DPO 只优化审计偏好
P38-RT-052 -> P38-E07 RAG/prompt/model/threshold 必须可 ablation
P38-RT-053 -> P38-E08 shadow 日志必须记录 no-hit/conflict/citation completeness
P38-RT-054 -> P38-E09 false block opportunity 必须用 paper/replay 或人工复核估计
P38-RT-055 -> P38-F07 incident freeze 必须冻结模型、prompt、RAG index 和 threshold
P38-RT-056 -> P38-F08 model card / dataset card 必须描述 intended use 和 out-of-scope use
P38-RT-057 -> P38-F09 latency budget 和 fallback 必须纳入发布验收
P38-RT-058 -> P38-G04 知识包必须裁剪字段，控制上下文预算
P38-RT-059 -> P38-G05 citation completeness 必须进入 shadow 指标
```

## P1 队列

```text
P38-RT-061 -> P38-A10 ranking model 可作为 review_priority 增强项
P38-RT-060 -> P38-B10 conformal / Bayesian calibration 只能作为增强层
P38-RT-062 -> P38-C10 多市场迁移时必须重新检查特征可用性
P38-RT-063 -> P38-D10 teacher model 只能作为审计 baseline
P38-RT-064 -> P38-E10 active learning review sampling 只能作为增强
P38-RT-065 -> P38-F10 model compression 只能在不破坏审计和校准后考虑
P38-RT-066 -> P38-G06 no-hit query 应进入知识缺口队列
```

## 批次建议

```text
Batch 01: P38-RT-001 至 P38-RT-012，scorer 与校准基础。
Batch 02: P38-RT-013 至 P38-RT-024，阈值、特征、LLM strict schema。
Batch 03: P38-RT-025 至 P38-RT-036，LLM 安全、eval、release manifest。
Batch 04: P38-RT-037 至 P38-RT-048，rollback、RAG、CatBoost、schema registry。
Batch 05: P38-RT-049 至 P38-RT-059，SFT/DPO、ablation、shadow、dataset/model card。
Batch 06: P38-RT-060 至 P38-RT-066，P1 增强项。
```

## 下游处理

```text
1. 每个 ResearchIngestionTask 生成 candidate knowledge。
2. candidate 统一进入 Phase 32 审计工作流。
3. 通过审计后进入 formal reviewed。
4. 人工另行决定 approved，不在本队列自动升级。
```
