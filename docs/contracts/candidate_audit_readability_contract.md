# Candidate Audit Readability Contract

本文定义 Phase 29 候选知识人工审核页的上下游、阅读型 view model、审核 checklist、handoff 输出、Vue3 页面契约、FastAPI/fixture 只读读取契约和安全边界。

## 目标

候选页是人工审核入口，不是正式知识入库页面。它负责把联网采集、项目回灌或人工补充产生的候选知识，以便于阅读和判断的方式展示给审计员，并把审核结果交接给 `CEK-TA-102` 的候选转正式知识 draft 流程。

本契约要求候选页帮助审计员稳定判断：

```text
1. 候选知识是否有来源。
2. 来源质量是否足以支撑结论。
3. 是否存在冲突、过期、无来源或边界缺失。
4. 适用范围、不适用范围、假设和限制是否清楚。
5. 是否已归类到正确知识树节点。
6. 是否可以进入 accepted_for_draft。
```

## 上游

| 上游 | 产物 | 消费方式 |
| --- | --- | --- |
| Phase 23 | `codex-expert-kit/rag/candidates/**/*.json` | 候选知识源文件 |
| Phase 24 | `ui/src/data/phase23Candidates.ts`、`candidateHandoff.ts` | 当前候选 fixture 和 handoff 逻辑 |
| Phase 28 | `codex-expert-kit/api/`、`knowledgeTreeApi.ts` | 只读 API/fallback 模式参考 |
| 知识树 | `knowledge_tree_v2.md`、`knowledge_items.json` | `tree_node_id`、`canonical_node_id`、覆盖统计 |
| 治理规则 | `source_quality_rules.md`、`conflict_detection_rules.md` | 来源质量和冲突阻断规则 |

## 下游

| 下游 | 需要的输出 | 约束 |
| --- | --- | --- |
| CEK-TA-102 | accepted_for_draft handoff | 只能转 draft，不能直接 approved |
| KnowledgeTreeView | `/ingestion?tree_node_id=...` 跳转 | 候选页必须支持 tree filter |
| SearchLab/MCP | 后续验证正式知识 | candidate 不作为默认指导 |
| Playwright | 页面和交互验收 | 桌面/移动端无重叠、无横向溢出 |
| 人工审计 | 可读候选正文、来源、冲突、边界、下一步动作 | 高风险项必须显式提示 |

## 状态流

### 候选生命周期

```text
proposed
-> sanitized
-> sourced
-> classified
-> conflict_checked
-> reviewed
-> accepted | rejected
```

### 页面审核决策

```text
candidate_ready
-> accepted_for_draft
-> CEK-TA-102 转 KnowledgeItem draft
-> MCP/SearchLab runtime validation
-> reviewed/approved
```

```text
needs_more_evidence
-> 补来源、补边界、补冲突审计
-> 回到 candidate_ready 或 rejected
```

```text
blocked
-> 冲突、无来源、过期、分类错误或边界不清
-> 不允许进入 accepted_for_draft
```

```text
rejected
-> 不进入正式知识库
-> 不参与 MCP 默认检索
```

## 安全边界

硬规则：

```text
1. candidate、proposed、draft 不能显示为 approved。
2. 候选页不能直接写入 codex-expert-kit/rag/knowledge/。
3. 候选页不能绕过 CEK-TA-102。
4. 候选页不能开放 MCP 写权限。
5. 无 source_refs 的候选不能进入 accepted_for_draft。
6. conflict_status 为 confirmed 或 unchecked 的候选不能进入 accepted_for_draft。
7. 缺少 applies_when、not_applicable_when 或 assumptions 时必须显示缺口。
8. time_sensitive 候选必须显示 freshness 风险。
9. 回灌知识必须保持 proposed/sanitized/reviewed/accepted 状态链，不能直接 accepted。
```

## 页面信息架构

候选页采用“三栏审核工作台”：

```text
左侧：候选队列
中间：候选正文、证据、冲突、边界、转换预览
右侧：审核摘要、checklist、阻断原因、下一步动作、handoff 导出
```

### 左侧候选队列

职责：

```text
1. 展示候选标题、partition、tree node、risk level、source count、conflict status。
2. 支持搜索、分区、状态、冲突、来源可靠性、风险等级过滤。
3. 支持从知识树跳转携带 `tree_node_id` 后自动过滤。
4. 支持上千候选的分页或虚拟列表预留。
```

### 中间候选正文

职责：

```text
1. 展示候选 claim、evidence_summary、适用范围、不适用范围、假设、限制。
2. 展示来源证据列表，不隐藏 URL、publisher、source_type、reliability、score。
3. 展示冲突审计状态、checked_against、resolution_summary。
4. 展示 KnowledgeItem draft 预览，但只能标注为 draft preview。
```

### 右侧审核摘要

职责：

```text
1. 展示当前候选是否可进入 accepted_for_draft。
2. 展示 checklist pass/warning/fail。
3. 展示 missing_fields、blocking_issues 和 required_followups。
4. 提供 handoff JSON/Markdown 导出入口。
5. 提供复制 candidate_id、canonical_node_id 的辅助动作。
```

## CandidateReadableViewModel

Vue3 页面可以从 `IngestionCandidate` 派生阅读型 view model。派生层只服务展示和审核，不改变源数据语义。

```yaml
candidate_id: string
research_task_id: string
title: string
claim: string
summary: string
partition_id: string
domain: string
subdomain: string
tree_node_id: string
canonical_node_id: string
tree_path: string
candidate_status: candidate_ready | needs_more_evidence | blocked | accepted_for_draft | rejected
review_status: proposed | sanitized | sourced | classified | conflict_checked | reviewed | accepted | rejected
ingestion_decision: accepted_for_draft | needs_more_evidence | rejected | blocked
risk_level: low | medium | high | blocked
risk_reasons: string[]
source_count: number
source_quality_score: number
source_reliability: low | medium | high
conflict_status: none | potential | confirmed | resolved | unchecked
freshness: stable | time_sensitive | deprecated
applies_when: string[]
not_applicable_when: string[]
assumptions: string[]
limitations: string[]
missing_fields: string[]
blocking_issues: string[]
required_followups: string[]
conversion_preview:
  proposed_knowledge_id: string
  target_review_status: draft
  can_convert_to_draft: boolean
```

## Risk Level 派生规则

```text
blocked:
  - candidate_status = blocked
  - conflict_status = confirmed
  - conflict_status = unchecked
  - source_count = 0
  - freshness = deprecated

high:
  - candidate_status = needs_more_evidence
  - source_reliability = low
  - source_quality_score < 0.6
  - missing_fields 非空
  - blocking_issues 非空

medium:
  - conflict_status = potential
  - freshness = time_sensitive
  - assumptions 或 limitations 不完整

low:
  - 来源、边界、分类、冲突审计均满足最低要求
```

## CandidateAuditChecklist

每条候选必须生成 checklist：

```yaml
candidate_id: string
can_accept_for_draft: boolean
checks:
  - key: has_sources
    label: 有可追踪来源
    status: pass | warning | fail
    reason: string
  - key: source_quality
    label: 来源质量足够
    status: pass | warning | fail
    reason: string
  - key: conflict_checked
    label: 冲突已审计
    status: pass | warning | fail
    reason: string
  - key: scope_defined
    label: 适用和不适用边界完整
    status: pass | warning | fail
    reason: string
  - key: assumptions_defined
    label: 假设和限制已说明
    status: pass | warning | fail
    reason: string
  - key: tree_classified
    label: 已归类到知识树节点
    status: pass | warning | fail
    reason: string
  - key: draft_ready
    label: 可进入 draft 交接
    status: pass | warning | fail
    reason: string
```

## Handoff 输出契约

候选页导出的 handoff 面向 `CEK-TA-102`。它是交接材料，不是正式入库写入。

```yaml
handoff_id: string
phase: "29"
target_task_id: CEK-TA-102
generated_at: string
source_view:
  page: ingestion
  filters:
    query: string
    partition_id: string | all
    tree_node_id: string | null
    candidate_status: string | all
    conflict_status: string | all
    risk_level: string | all
candidates:
  - candidate_id: string
    decision: accepted_for_draft | needs_more_evidence | rejected | blocked
    decision_reason: string
    risk_level: low | medium | high | blocked
    missing_fields: string[]
    blocking_issues: string[]
    required_followups: string[]
    target_knowledge_preview:
      proposed_knowledge_id: string
      review_status: draft
      canonical_node_id: string
      tree_node_id: string
```

## FastAPI 只读候选读取契约

Phase 29 第一版可以继续使用 fixture。如果增加 FastAPI 候选读取接口，必须遵守只读契约。

### GET `/api/candidates`

查询参数：

```yaml
q: string | null
partition_id: string | null
tree_node_id: string | null
candidate_status: string | null
conflict_status: string | null
risk_level: string | null
limit: integer
offset: integer
```

响应：

```yaml
data:
  items: CandidateReadableViewModel[]
  total: integer
  limit: integer
  offset: integer
  source: api | fixture
  generated_at: string
```

### GET `/api/candidates/{candidate_id}`

响应：

```yaml
data:
  item: CandidateReadableViewModel
  sources: SourceRef[]
  checklist: CandidateAuditChecklist
  source: api | fixture
  generated_at: string
```

### 错误响应

```yaml
error:
  code: string
  message: string
  details: object
  retryable: boolean
```

错误码：

```text
CANDIDATE_INDEX_NOT_FOUND
CANDIDATE_NOT_FOUND
INVALID_CANDIDATE_FILTER
CANDIDATE_SCHEMA_INVALID
READ_ONLY_RUNTIME
INTERNAL_ERROR
```

## Vue3 组件契约

### IngestionReview.vue

职责：

```text
1. 管理候选页筛选、选中候选、分页和 handoff 导出。
2. 组合候选队列、候选正文、来源、冲突、治理、转换预览和审核摘要。
3. 支持 `route.query.tree_node_id` 过滤。
4. 不直接修改候选源文件或正式知识文件。
```

状态：

```text
loading: 加载候选数据
empty: 没有候选或过滤无结果
error: fixture/API 读取失败
ready: 正常展示
```

### CandidateAuditChecklistPanel.vue

建议新增组件。

props：

```yaml
candidate: IngestionCandidate | CandidateReadableViewModel
checklist: CandidateAuditChecklist
```

emits：

```yaml
copy-id: candidate_id | canonical_node_id
```

职责：

```text
1. 展示 pass/warning/fail。
2. 聚合 can_accept_for_draft。
3. 展示阻断原因和下一步动作。
```

## 视觉和阅读规则

```text
1. 风险颜色要克制，文字对比度必须清楚。
2. blocked/fail 使用边框、图标、短标签和说明，不依赖大面积红底。
3. 候选队列使用紧凑行或紧凑卡片，避免长 claim 撑高列表。
4. 中间正文优先显示 claim、summary、边界和证据，不把全部 metadata 堆在首屏。
5. 右侧摘要固定宽度，移动端折叠到 Tabs 或底部面板。
6. 上千候选场景必须预留分页、limit、offset 或虚拟列表实现点。
```

## 测试契约

文档：

```text
1. UTF-8 读取无乱码。
2. docs/index_tasks.md 文档入口包含本契约。
3. Phase 29 任务卡引用本契约。
```

Vue3：

```text
1. `npm run build` 通过。
2. `/ingestion` 能显示候选队列和详情。
3. `/ingestion?tree_node_id=...` 能过滤候选。
4. candidate 不显示为 approved。
5. blocked、unchecked conflict、无来源候选显示阻断提示。
6. 桌面端和移动端无重叠、无横向溢出。
7. handoff JSON/Markdown 按钮存在，且文案不表示直接入库。
```

API：

```text
1. API 只读，不提供 POST/PUT/DELETE 审核写接口。
2. limit/offset 边界参数可控。
3. 未找到候选返回 CANDIDATE_NOT_FOUND。
4. 候选索引缺失返回 CANDIDATE_INDEX_NOT_FOUND。
5. 错误响应符合统一错误结构。
```

## 回滚

```text
1. 前端回退到 Phase 24 的 IngestionReview。
2. 删除新增 CandidateAuditChecklistPanel 组件引用。
3. 如新增候选 API 出错，前端回退到 phase23Candidates fixture。
4. 保留 handoff 旧逻辑，不影响 CEK-TA-102。
5. 不修改候选源文件和正式知识目录。
```
