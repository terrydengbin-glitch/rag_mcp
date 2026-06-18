# Phase 6 LLM 训练闭环任务卡

## Phase 目标

把 CEK-TA 的策略审计、交易分析、任务卡写法、知识检索和错误归因能力，整理成可训练、可评测、可回归的 LLM 数据闭环。

本 Phase 只定义训练闭环的领域、数据集卡、评测报告和 Skill 工作流，不执行真实模型训练，不选择具体模型供应商，不引入外部训练服务。

## 任务列表

| ID | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- |
| CEK-TA-019 | done | 创建 LLM training domain | `codex-expert-kit/domains/llm_training/` |
| CEK-TA-020 | done | 创建数据集与评测模板 | `codex-expert-kit/templates/dataset_card.md`、`codex-expert-kit/templates/eval_report.md` |
| CEK-TA-021 | done | 创建训练相关 Skills | `llm-data-curator`、`sft-engineer`、`eval-engineer` |

## 上游输入

```text
codex-expert-kit/core/AGENTS.md
codex-expert-kit/rag/retrieval_policy.md
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/templates/trade_result_schema.md
codex-expert-kit/domains/trade_analysis/knowledge/bad_trade_taxonomy.md
codex-expert-kit/skills/trade-quality-analyst/SKILL.md
docs/知识库采集与审计规范.md
docs/知识倒灌与反哺规范.md
```

## 下游输出

```text
Phase 7 Vue3 知识审计界面:
  展示 dataset card、eval report、样本来源、标签质量、训练适用性和评测回归状态。

Phase 8 其他项目接入:
  业务项目可按 dataset_card 模板提交脱敏训练样本。

Phase 9 知识倒灌与反哺:
  训练样本如果来自项目经验，必须先走 sanitization 和 contribution 流程。

Codex Skills:
  llm-data-curator、sft-engineer、eval-engineer 用于稳定执行数据整理、训练计划和评测工作流。
```

## 输入契约

LLM 训练闭环输入必须来自：

```text
source-backed knowledge item
reviewed task card
sanitized trade result
approved bad-case label
reviewed audit report
explicit human preference
```

每条样本必须声明：

```text
sample_id
source_type
source_ref
task_type
target_capability
label_quality
split
license_or_reuse_status
sanitization_status
review_status
```

## 输出契约

Phase 6 输出必须包含：

```text
DatasetCard
EvalReport
DataCuration workflow
SFT planning workflow
Eval workflow
train/eval/holdout split rules
leakage controls
regression gates
```

## 边界范围

本 Phase 做：

```text
1. 定义 LLM training domain。
2. 定义数据集卡模板。
3. 定义评测报告模板。
4. 创建 llm-data-curator Skill。
5. 创建 sft-engineer Skill。
6. 创建 eval-engineer Skill。
7. 更新索引和 README。
```

本 Phase 不做：

```text
1. 不执行真实训练。
2. 不选择具体模型或供应商。
3. 不调用外部训练 API。
4. 不收集 raw private trades。
5. 不把最新市场事实、交易所规则或项目配置写进模型权重。
6. 不把未审计样本加入训练集。
```

## 涉及组件

```text
docs/tasks/phase6_llm_training_loop.md
codex-expert-kit/domains/llm_training/README.md
codex-expert-kit/domains/llm_training/AGENTS.domain.md
codex-expert-kit/templates/dataset_card.md
codex-expert-kit/templates/eval_report.md
codex-expert-kit/skills/llm-data-curator/SKILL.md
codex-expert-kit/skills/sft-engineer/SKILL.md
codex-expert-kit/skills/eval-engineer/SKILL.md
docs/index_tasks.md
docs/tasks/README.md
codex-expert-kit/README.md
```

## 涉及数据结构

```text
DatasetCard
TrainingSample
PreferencePair
EvalCase
EvalReport
RegressionGate
CapabilityMap
LeakageCheck
DataProvenance
```

## 涉及数据库/存储

当前 Phase 不引入数据库。数据集、评测和训练记录先以模板契约形式定义。后续如果落地样本仓库、训练记录库、评测服务或外部训练平台，必须单独开任务卡并向开发者确认。

## 实施步骤

```text
1. 创建 Phase 6 任务卡。
2. 创建 llm_training domain 目录与 AGENTS.domain.md。
3. 创建 dataset_card.md。
4. 创建 eval_report.md。
5. 创建 llm-data-curator Skill。
6. 创建 sft-engineer Skill。
7. 创建 eval-engineer Skill。
8. 更新 docs/index_tasks.md。
9. 更新 docs/tasks/README.md。
10. 更新 codex-expert-kit/README.md。
11. 执行文件存在性、关键章节、Skill frontmatter、状态一致性和 UTF-8 检查。
```

## Definition of Done

```text
1. Phase 6 任务卡存在，并包含上下游、契约、边界、DoD 和测试。
2. llm_training domain 存在，并定义 RAG/SFT/DPO/Eval 决策边界。
3. dataset_card.md 定义样本来源、脱敏、标签质量、split、泄漏检查和训练用途。
4. eval_report.md 定义评测用例、指标、回归门槛、失败样本和发布决策。
5. 三个 Skill 均包含 name、description、Use When、Workflow、Output。
6. docs/index_tasks.md、docs/tasks/README.md、Phase 任务卡状态一致。
7. codex-expert-kit/README.md 有 Phase 6 入口。
8. 中文文档 UTF-8 读取无乱码。
```

## 测试与验收

```text
1. Test-Path 检查全部交付物存在。
2. Select-String 检查关键章节存在。
3. 检查 Skill frontmatter 包含 name 和 description。
4. 检查 Phase 6、CEK-TA-019、CEK-TA-020、CEK-TA-021 均为 done。
5. Get-Content -Encoding UTF8 检查中文文档无乱码。
6. 检查文档没有引入具体外部训练服务、真实密钥、raw private trades 或未审计训练许可。
```

## 风险与回滚

风险：

```text
1. 未脱敏样本进入训练集会泄漏项目事实。
2. train/eval 泄漏会导致能力虚高。
3. 把最新市场事实或交易所规则写进权重会快速过期。
4. 只做 SFT 不做 eval 会让能力退化不可见。
```

回滚：

```text
1. 文档变更可通过版本控制回退。
2. 数据集版本必须保留 dataset_version，不直接覆盖旧版本。
3. 评测失败时不得发布新训练产物。
4. 出现泄漏风险时，先撤回样本并标记 rejected。
```

## 需要开发者确认的问题

当前 Phase 不执行真实训练、不选模型、不接外部服务，因此无需确认。

后续如果要选择模型、连接训练平台、上传数据集、引入评测服务或改变训练数据许可策略，必须单独向开发者确认。

## 状态更新要求

完成后必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase6_llm_training_loop.md
codex-expert-kit/README.md
```
