# Phase 9 知识倒灌与反哺任务卡

## Phase 目标

允许其他项目把专业经验、安全脱敏后的案例、审计结论、bad case、规则更新和 LLM/RAG 工程经验反哺到 CEK-TA，同时避免项目私有事实、密钥、账户、原始订单和未审计冲突污染通用知识库。

倒灌不是直接入库，而是一条审计队列：

```text
proposed -> sanitized -> sourced -> classified -> conflict_checked -> reviewed -> accepted
```

## 任务列表

| ID | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- |
| CEK-TA-037 | done | 编写知识倒灌与反哺规范 | `docs/知识倒灌与反哺规范.md` |
| CEK-TA-038 | done | 创建倒灌任务卡模板 | `codex-expert-kit/templates/knowledge_contribution_task.md` |
| CEK-TA-039 | done | 定义倒灌知识 schema | `codex-expert-kit/rag/contribution_schema.md` |
| CEK-TA-040 | done | 定义脱敏与去项目私有化规则 | `codex-expert-kit/rag/sanitization_rules.md` |
| CEK-TA-041 | done | 实现倒灌队列目录 | `contributions/` |
| CEK-TA-042 | done | Vue3 增加倒灌队列视图 | `ui/src/views/ContributionQueue.vue` |

## 上游输入

```text
docs/知识倒灌与反哺规范.md
docs/其他项目接入指南.md
codex-expert-kit/templates/external_project_AGENTS.md
codex-expert-kit/templates/project_adapter.md
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/conflict_detection_rules.md
codex-expert-kit/rag/source_quality_rules.md
codex-expert-kit/templates/trade_result_schema.md
ui/src/views/TaskLog.vue
```

## 下游输出

```text
业务项目:
  使用 knowledge_contribution_task.md 提交 proposed 倒灌任务。

CEK-TA 审计:
  使用 contribution_schema.md、sanitization_rules.md 和 Vue3 ContributionQueue 审核倒灌队列。

RAG/知识库:
  accepted 后才允许生成 knowledge_item 或 Skill 修改建议。

LLM 训练:
  仅 sanitized + reviewed/accepted 的样本可进入 dataset_card。
```

## 输入契约

倒灌任务必须提供：

```text
contribution_id
source_project
contribution_type
raw_finding_summary
private_data_risk
sanitization_report
generalized_rule
applicability
sources
conflict_check
target_location
review_decision
```

## 输出契约

倒灌审计输出必须包含：

```text
ContributionRecord
sanitization_status
source_status
classification_status
conflict_status
review_status
accepted_outputs
rejection_reason
audit_log
```

## 边界范围

本 Phase 做：

```text
1. 定义倒灌任务卡模板。
2. 定义 contribution_schema。
3. 定义 sanitization_rules。
4. 创建 contributions 队列目录和 README。
5. Vue3 增加 ContributionQueue 只读视图。
6. 更新索引和 README。
```

本 Phase 不做：

```text
1. 不接受真实业务项目倒灌内容。
2. 不把 proposed 内容直接写入 approved 知识。
3. 不保存密钥、账户、原始订单、未脱敏日志。
4. 不实现后端写接口或数据库。
5. 不改变 MCP 权限。
```

## 涉及组件

```text
docs/tasks/phase9_knowledge_contribution.md
codex-expert-kit/templates/knowledge_contribution_task.md
codex-expert-kit/rag/contribution_schema.md
codex-expert-kit/rag/sanitization_rules.md
contributions/README.md
ui/src/views/ContributionQueue.vue
ui/src/router.ts
ui/src/App.vue
ui/src/types.ts
ui/src/data/mockData.ts
ui/src/stores/auditStore.ts
```

## 涉及数据结构

```text
ContributionRecord
ContributionSourceProject
SanitizationReport
PrivateDataRisk
GeneralizedRule
ContributionConflictCheck
AcceptedOutput
AuditLogEntry
```

## 涉及数据库/存储

当前 Phase 不引入数据库。`contributions/` 是文件队列目录，用于保存 proposed/reviewed/accepted/rejected 的任务卡或 JSON 记录。后续若要数据库化，必须另开任务卡定义主键、索引、状态流、迁移和回滚。

## 实施步骤

```text
1. 创建 Phase 9 任务卡。
2. 创建 knowledge_contribution_task.md。
3. 创建 contribution_schema.md。
4. 创建 sanitization_rules.md。
5. 创建 contributions/README.md。
6. Vue3 增加 ContributionQueue 视图、路由、导航和 mock 数据。
7. 更新 docs/index_tasks.md。
8. 更新 docs/tasks/README.md。
9. 更新 README 入口。
10. 执行文档检查、UTF-8 检查、Vue build。
```

## Definition of Done

```text
1. Phase 9 任务卡存在。
2. 倒灌任务卡模板包含来源项目、脱敏、泛化规则、适用范围、来源证据、冲突检查和审计结论。
3. contribution_schema.md 定义状态流、必填字段、入库门槛和 accepted 输出。
4. sanitization_rules.md 定义敏感信息、字段映射、禁止项和验收清单。
5. contributions/ 目录存在并有 README。
6. Vue3 ContributionQueue 能展示 proposed/sanitized/sourced/conflict_checked/reviewed/accepted 等状态。
7. 索引状态一致。
8. UTF-8 无乱码。
9. Vue build 通过。
```

## 测试与验收

```text
1. Test-Path 检查全部交付物存在。
2. Select-String 检查关键章节存在。
3. 检查 Phase 9、CEK-TA-038 到 CEK-TA-042 均为 done。
4. npm run build 验证 Vue3。
5. Get-Content -Encoding UTF8 检查中文文档无乱码。
6. 检查模板不包含真实密钥、账户、原始订单或未脱敏样例。
```

## 风险与回滚

风险：

```text
1. 未脱敏样本进入 CEK-TA 会泄漏项目事实。
2. 未补来源的经验会污染专业知识库。
3. 未消解冲突的规则进入 approved 会导致 Codex 输出矛盾建议。
4. Vue3 当前是 mock 数据，不代表真实队列。
```

回滚：

```text
1. 文档和 UI 变更可通过版本控制回退。
2. contributions 队列记录不得物理删除已审计条目，优先 rejected 或 deprecated。
3. 如果发现泄漏风险，贡献记录必须标记 rejected 并移出可训练/可入库流程。
```

## 需要开发者确认的问题

当前 Phase 只定义模板、schema、规则、目录和只读 UI mock，不引入数据库、后端写接口、真实项目数据或 MCP 权限变更，因此无需确认。

后续如要接真实业务项目倒灌、启用写接口、接数据库或改变 MCP 权限，必须单独向开发者确认。

## 状态更新要求

完成后必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase9_knowledge_contribution.md
README.md
codex-expert-kit/README.md
```
