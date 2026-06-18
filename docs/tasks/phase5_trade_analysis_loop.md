# Phase 5 交易分析闭环任务卡

## Phase 目标

建立 CEK-TA 的交易分析闭环，让每一笔交易都能从执行结果变成可复盘、可归因、可统计、可回放、可倒灌、可用于 LLM 训练的结构化样本。

核心目标：

```text
Every trade becomes a learning sample.
Trade result must connect decision, order intent, fills, risk, outcome, labels, and next action.
Bad trade taxonomy must distinguish signal, entry, risk, execution, data, and review failures.
```

## 任务列表

| ID | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- |
| CEK-TA-016 | done | 定义 trade result schema | `codex-expert-kit/templates/trade_result_schema.md` |
| CEK-TA-017 | done | 定义 bad case taxonomy | `codex-expert-kit/domains/trade_analysis/knowledge/bad_trade_taxonomy.md` |
| CEK-TA-018 | done | 创建 trade-quality-analyst Skill | `codex-expert-kit/skills/trade-quality-analyst/SKILL.md` |

## 上游输入

```text
codex-expert-kit/templates/interface_contract.md
codex-expert-kit/templates/execution_adapter_spec.md
codex-expert-kit/templates/fill_model_spec.md
codex-expert-kit/core/AGENTS.md
codex-expert-kit/skills/backtest-reviewer/SKILL.md
codex-expert-kit/skills/strategy-auditor/SKILL.md
```

## 下游输出

```text
Phase 6 LLM 训练闭环:
  使用 trade_result_schema 和 bad_trade_taxonomy 生成训练、评测、偏好样本。

Phase 7 Vue3 知识审计界面:
  可展示交易质量标签、bad case、原因链、修复建议和人工审核状态。

Phase 9 知识倒灌与反哺:
  经过脱敏后的 trade case 可作为 sanitized_project_case 贡献给 CEK-TA。

业务项目:
  每笔交易可以按统一 schema 输出，并使用 trade-quality-analyst 复盘。
```

## 输入契约

交易分析输入至少来自：

```text
Decision
OrderIntent
ExecutionReport
FillEvent
PositionSnapshot
FillAssumption
RiskState
AuditTrace
MarketContext
PostTradeOutcome
```

如果业务项目无法提供完整输入，必须显式标记缺失字段和可信度，不允许把缺失数据当成正常样本。

## 输出契约

交易分析输出必须包含：

```text
TradeResult
OutcomeMetrics
QualityLabels
BadCaseLabels
RootCauseChain
RepairAction
ReviewStatus
TrainingUse
```

每个 bad case 必须可回链到：

```text
trade_result_id
decision_id
intent_id
execution_report_id
source_event_ids
assumption_id
```

## 边界范围

本 Phase 做：

```text
1. 定义 TradeResult 结构化 schema。
2. 定义坏交易分类和原因链。
3. 创建 trade-quality-analyst Skill。
4. 建立 trade result 到 LLM/RAG/倒灌的边界。
5. 更新索引和 README。
```

本 Phase 不做：

```text
1. 不实现交易分析数据库。
2. 不连接真实账户或交易所。
3. 不读取原始私密订单。
4. 不把项目私有交易记录直接写入 CEK-TA。
5. 不做 LLM 训练实现。
6. 不把单笔交易结论当成通用策略规则。
```

## 涉及组件

```text
docs/tasks/phase5_trade_analysis_loop.md
codex-expert-kit/templates/trade_result_schema.md
codex-expert-kit/domains/trade_analysis/README.md
codex-expert-kit/domains/trade_analysis/AGENTS.domain.md
codex-expert-kit/domains/trade_analysis/knowledge/bad_trade_taxonomy.md
codex-expert-kit/skills/trade-quality-analyst/SKILL.md
docs/index_tasks.md
docs/tasks/README.md
codex-expert-kit/README.md
```

## 涉及数据结构

```text
TradeResult
OutcomeMetrics
PlannedTrade
ExecutedTrade
TradeContext
QualityLabel
BadCaseLabel
RootCauseChain
RepairAction
TrainingUse
ReviewStatus
```

## 涉及数据库/存储

当前 Phase 不引入数据库。所有结构先作为 Markdown 契约。业务项目若要存储 TradeResult，必须在业务项目中定义主键、索引、状态字段、时间字段、审计字段、版本字段、迁移和回滚。

## 实施步骤

```text
1. 创建 Phase 5 任务卡。
2. 创建 trade_analysis 领域目录。
3. 创建 trade_result_schema.md。
4. 创建 bad_trade_taxonomy.md。
5. 创建 trade-quality-analyst Skill。
6. 更新 docs/index_tasks.md。
7. 更新 docs/tasks/README.md。
8. 更新 codex-expert-kit/README.md。
9. 执行文件存在性、关键章节、状态一致性和 UTF-8 检查。
```

## Definition of Done

```text
1. Phase 5 任务卡存在，并包含上下游、契约、边界、DoD 和测试。
2. trade_result_schema.md 定义完整 TradeResult、指标、标签、原因链和训练用途。
3. bad_trade_taxonomy.md 定义坏交易分类、严重度、原因链、修复动作和禁止误判。
4. trade-quality-analyst Skill 包含 Use When、Workflow、Inputs、Output、Hard Rules。
5. docs/index_tasks.md、docs/tasks/README.md、Phase 任务卡状态一致。
6. codex-expert-kit/README.md 有 Phase 5 入口。
7. 中文文档 UTF-8 读取无乱码。
```

## 测试与验收

```text
1. Test-Path 检查全部交付物存在。
2. Select-String 检查关键章节存在。
3. 检查 Phase 5、CEK-TA-016、CEK-TA-017、CEK-TA-018 均为 done。
4. 检查 Skill frontmatter 包含 name 和 description。
5. Get-Content -Encoding UTF8 检查中文文档无乱码。
6. 检查文档不包含真实账户、密钥、原始私密订单或实盘操作。
```

## 风险与回滚

风险：

```text
1. 标签过粗会导致交易复盘无法指导策略修复。
2. 标签过细会导致人工标注成本过高。
3. 单笔交易容易被误读为通用规律。
4. 如果不记录缺失字段，LLM 训练会学习错误归因。
```

回滚：

```text
1. 文档变更可通过版本控制回退。
2. taxonomy 后续扩展时优先新增 label，不直接删除旧 label。
3. 已用于训练的数据集必须记录 taxonomy_version，避免版本混淆。
```

## 需要开发者确认的问题

当前 Phase 只定义文档契约、领域知识和 Skill，不引入数据库、后端框架、外部服务、实盘权限或不可逆迁移，因此无需确认。

后续如果要把 TradeResult 落数据库、接真实交易日志、自动提交知识倒灌或生成训练集，需要单独确认。

## 状态更新要求

完成后必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase5_trade_analysis_loop.md
codex-expert-kit/README.md
```
