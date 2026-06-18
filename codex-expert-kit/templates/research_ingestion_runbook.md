# CEK-TA Research Ingestion Runbook

本文件定义 Codex 执行专业知识采集任务时的标准运行流程。它连接 `research_task_card.md`、来源质量评分、冲突检测、知识树分类、候选知识入库包和 Vue3 审计工作台。

## 目标

```text
1. 把联网搜索变成可复核的研究任务。
2. 把资料阅读变成结构化 claim、source、scope、conflict。
3. 把候选知识先放入审计队列，而不是直接写入 approved 知识库。
4. 保证后续 RAG、MCP、Vue3、知识质量评测可以消费同一套字段。
```

## 输入契约

每次采集必须先创建或填写 `ResearchIngestionTask`：

```yaml
research_task_id: CEK-TA-RESEARCH-YYYYMMDD-001
status: draft | running | candidate_ready | blocked | reviewed
topic: ""
target_node_id: "kt.backtest.bias"
tree_path: "CEK-TA / Trading Engineering / Backtest / Bias"
partition_id: "KB_04_BACKTEST"
domain: "backtest"
subdomain: "bias"
question_set:
  - ""
source_policy:
  preferred_source_types:
    - official_doc
    - paper
    - framework_doc
  minimum_reliability: medium
freshness_requirement: stable | time_sensitive
must_include_sources: []
must_exclude_sources: []
conflict_check_scope:
  domain: ""
  subdomain: ""
  related_tree_nodes: []
reviewer: "human | mixed"
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
```

## 输出契约

采集任务只能输出 `IngestionCandidate`，不得直接输出 approved knowledge item。

```text
允许输出：
1. 候选知识包。
2. 来源记录。
3. 抽取 claim。
4. 冲突审计记录。
5. 人工审计问题。
6. 是否建议进入 RAG、Skill、两者或都不进入。

禁止输出：
1. 自动 approved 知识。
2. 无来源知识。
3. 未绑定知识树节点的候选知识。
4. 未写适用/不适用边界的规则。
5. 大段复制版权内容。
6. 未脱敏的项目私有经验。
7. 行情数据、K线数据或订单流原始数据。
```

## 采集流程

### 1. 问题收敛

先把宽泛主题改写成可验证问题：

```text
不好：K线怎么采集？
较好：ATR 在 1m/5m K 线止损距离估计中能支持什么专业交易知识，哪些结论必须避免？
```

必须明确：

```text
market
asset
timeframe
data_granularity
project_type
used_for
applies_when
not_applicable_when
assumptions
```

### 2. 知识树定位

每个任务必须绑定一个 primary `target_node_id`，并可列出 related nodes。

选择规则：

```text
1. 优先选择最具体的 level 3 节点。
2. 如果没有 level 3 节点，选择对应 level 2 节点并记录缺口。
3. 不把 market、asset、timeframe 当成树节点；它们属于 applicability。
4. 一个候选知识包只能有一个 primary tree_node_id。
```

### 3. 来源搜索

执行联网搜索时按来源优先级采集：

```text
P0: official_doc, exchange_rule, standard protocol, original paper, authoritative data source
P1: framework_doc, open-source project official docs, engineering whitepaper
P2: book, course, research_report, engineering_article
P3: blog, forum, experience post
```

规则：

```text
1. P3 只能发现边界和案例，不能单独支持 approved。
2. live execution、exchange rule、model/API/library 行为必须优先使用当前官方资料。
3. backtest methodology、bias、metrics 可以使用稳定论文、书籍、框架文档，但涉及框架行为时仍要检查版本。
4. performance claim 必须记录样本、成本、偏差控制和可复现条件；否则只能作为低置信候选。
```

### 4. 来源记录

每个来源必须转成 `SourceRef`：

```json
{
  "source_id": "src_001",
  "source_title": "string",
  "source_url": "string | null",
  "source_type": "official_doc | paper | exchange_rule | framework_doc | book | research_report | engineering_article | internal_report | task_card | code_doc | runbook",
  "publisher": "string | null",
  "published_at": "YYYY-MM-DD | null",
  "accessed_at": "YYYY-MM-DD",
  "version": "string | null",
  "reliability": "high | medium | low",
  "score": 0,
  "relevance": "high | medium | low",
  "freshness": "stable | time_sensitive | deprecated",
  "limitations": []
}
```

### 5. Claim 抽取

从来源中抽取 claim 时，必须把原始证据、Codex 解释和候选规则分开：

```yaml
claim_id: claim_001
statement: ""
source_ids:
  - src_001
evidence_summary: ""
interpretation: ""
scope:
  market: general
  timeframe: general
  data_granularity: general
assumptions: []
limitations: []
```

不要把多个不同 scope 的结论合成一个通用规则。遇到 scope 不同，拆成多个候选。

### 6. 来源评分

按 `source_quality_rules.md` 的 8 个维度评分：

```text
Authority
Specificity
Applicability
Freshness
Reproducibility
Primary Evidence
Conflict History
License / Reuse Safety
```

分数转 reliability：

```text
85-100: high
60-84: medium
0-59: low
```

强制降级条件仍然优先于分数。

### 7. 冲突检测

候选必须按 `conflict_detection_rules.md` 检查：

```text
1. 同 domain/subdomain。
2. 同 rule_type 或 used_for 重叠。
3. 同 market/timeframe/granularity 但结论不同。
4. 同 source family 不同版本。
5. 标题、statement、evidence_summary 指向同一专业概念。
```

冲突结果必须写入候选包：

```text
none
potential
confirmed
resolved
deprecated_by_conflict
```

存在 blocking conflict 时，候选不能进入 accepted。

### 8. 候选包生成

生成 `IngestionCandidate` 时必须满足：

```text
1. candidate_id 唯一。
2. research_task_id 可追踪。
3. tree_node_id 存在于 knowledge_tree.md。
4. source_refs 非空。
5. applicable_scope 和 not_applicable_scope 非空。
6. conflict_audit 已执行。
7. review_status 只能是 proposed、sourced、classified、conflict_checked、reviewed、accepted、rejected、needs_more_evidence。
```

### 9. 人工审计

人工审计必须回答：

```text
1. 来源是否足够支持 claim？
2. 适用边界是否足够窄？
3. 是否存在未解决冲突？
4. 是否可以转换成 KnowledgeItem？
5. 是否更适合进入 Skill、runbook 或 eval case？
6. 是否存在版权、隐私或项目私有化问题？
```

### 10. 转换为正式知识

只有满足以下条件时，候选才能被转换成 `knowledge_item_schema.md`：

```text
1. review_status = accepted。
2. ingestion_decision = convert_to_knowledge_item 或 convert_to_skill_and_knowledge。
3. source_quality.overall_reliability = high 或 medium。
4. conflict_status = none 或 resolved。
5. reviewer 为 human 或 mixed。
6. candidate audit_log 记录接受理由。
```

转换后的正式知识仍必须从 `draft -> reviewed -> approved`，禁止直接 approved。

## 状态流

```text
draft
  -> running
  -> candidate_ready
  -> reviewed

draft
  -> running
  -> blocked

candidate_ready
  -> needs_more_evidence
  -> candidate_ready
```

候选知识状态：

```text
proposed
  -> sourced
  -> classified
  -> conflict_checked
  -> reviewed
  -> accepted

reviewed
  -> rejected

conflict_checked
  -> needs_more_evidence
```

## 版权与引用边界

```text
1. 只保存短引用、摘要和来源链接。
2. 不保存大段原文。
3. 不复制付费资料正文。
4. 对论文、官方文档、框架文档使用概括和字段化证据。
5. quoted_excerpt_allowed 默认 false，除非审计确认许可。
```

## 纸面验收样例

主题：

```text
1m OHLC 回测中，同一根 K 线同时触发 TP 和 SL 时如何处理？
```

正确输出应该是：

```text
1. 绑定 kt.replay_simulation.fill_model。
2. 记录至少一个框架文档或方法论来源。
3. claim 明确 OHLC 无法提供真实先后顺序。
4. 候选规则写出 conservative、optimistic、ambiguous 三类模型边界。
5. 冲突检查指出与 tick/order_book 级回放不同。
6. 候选状态停在 conflict_checked 或 reviewed，等待人工审计。
```

## DoD

```text
1. 研究任务输入完整。
2. 来源记录完整且有 accessed_at。
3. claim 与解释分离。
4. 来源评分完成。
5. 知识树节点绑定完成。
6. 适用和不适用范围明确。
7. 冲突检测完成。
8. 候选包不自动进入 approved。
9. 人工审计问题已列出。
10. UTF-8 中文可读。
```
