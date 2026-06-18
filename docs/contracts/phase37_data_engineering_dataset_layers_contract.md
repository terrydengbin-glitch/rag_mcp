# Phase 37 Data Engineering Dataset Layers Contract

生成日期：2026-06-11

## 目标

本契约为 CEK-TA Trading Engineering / Data Engineering 的数据层命名、写入边界、血缘字段和审计字段提供内部规范。它用于补强 `P37-B-D11 raw_vs_adjusted_data_boundary`，但不创建正式知识、不创建 approved，也不改变外部项目自己的数据库实现。

## 上游

```text
交易所或数据供应商原始行情
成交、盘口、bar、reference data、corporate action、contract rollover 和 vendor correction
外接项目的数据接入器、数据质量报告、特征生成器和标签生成器
```

## 下游

```text
回测数据集
训练数据集
特征表
标签表
质量审计报告
RAG 知识审计与 AI IDE 方案审计
```

## CEK-TA 数据层

| 层级 | 语义 | 写入边界 | 典型字段 |
| --- | --- | --- | --- |
| raw | 原始供应商/交易所事实记录，保留 source provenance 和接收时间 | append-only；不得被清洗、复权、特征或标签回写覆盖 | source_id, instrument_id, event_time, receive_time, raw_payload_hash, vendor_sequence |
| cleaned | 对 raw 做校验、去重、隔离、修复候选和质量标记后的可计算层 | 只能从 raw 派生；必须记录质量规则、隔离记录和修复记录 | quality_flags, quarantine_reason, repair_policy_id, quality_report_id |
| adjusted | 复权、合约换月、连续合约映射或 back-adjusted 数据层 | 只能从 raw/cleaned 派生；必须记录 adjustment_policy_id 和版本 | adjustment_policy_id, adjustment_factor, roll_rule_id, adjusted_price |
| feature_ready | 点时正确的特征层，不包含未来标签 | 必须记录 feature_version、available_time 和输入数据版本 | feature_name, feature_value, feature_version, available_time, source_dataset_version |
| label_ready | 训练/评估标签层，记录 horizon、label policy 和泄漏边界 | 不得回写 raw/cleaned/adjusted；只能作为训练或评估下游输入 | label_name, label_value, horizon, label_policy_id, label_generated_at |

## 转换清单

每次跨层转换必须生成 transformation manifest：

```text
input_layer
output_layer
source_dataset_version
source_table_snapshot
code_version
parameter_hash
produced_at
actor
quality_report_id
lineage_id
rollback_pointer
```

## 强制边界

```text
1. downstream layer 不得回写污染 raw layer。
2. raw 修正必须以 correction record 或新 dataset version 体现，不得静默覆盖。
3. adjusted 数据不能替代 raw 数据；回测/训练必须声明使用 raw、cleaned、adjusted、feature_ready 还是 label_ready。
4. feature_ready 必须有 available_time，不能含未来标签。
5. label_ready 必须声明 horizon 和 label policy，不能作为特征源回写。
6. AI Engineering 只能通过 knowledge_refs 引用本契约，不得把本契约改写为模型训练或交易执行规则本体。
```

## 不做什么

```text
不指定具体数据库产品。
不要求所有外接项目必须使用同一物理表名。
不提供买卖点、仓位、杠杆、止损止盈或实盘执行建议。
不把 candidate 直接升级为 reviewed/approved/default guidance。
```
