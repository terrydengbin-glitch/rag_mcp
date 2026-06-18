# Phase 45 Trading Engineering P1/P2 运行时与跨分支契约

## 目标

本契约定义 Phase 45 交易工程 P1/P2 知识的分类、候选生成、审计、formal reviewed/caveat_only 沉淀、MCP/SearchLab/Vue3 展示和外接项目引用边界。

Phase 45 的知识用于帮助外接交易项目 AI IDE 理解机构级交易工程约束，但不直接给出交易动作。

## 上游输入

```text
docs/research/phase45_trading_engineering_p1_knowledge_scope.md
docs/research/phase45_trading_engineering_p1_research_task_queue.md
docs/reports/phase37_trading_engineering_post_completion_gap_audit_report.md
codex-expert-kit/rag/knowledge_tree.md
docs/contracts/knowledge_item_schema_v1_1_contract.md
```

## 下游输出

```text
CandidateKnowledgeItem
formal reviewed/caveat_only knowledge item
knowledge_items.json
Vue3 knowledgeTreeNodes fixture
MCP/SearchLab 只读检索结果
外接项目 AI IDE 的引用型上下文
```

## 分支 owner 契约

| 主题 | 主 owner | 可引用 owner | 不允许越界 |
| --- | --- | --- | --- |
| Execution TCA | Live Execution、Trade Analysis | Data Engineering、AI Engineering | 不得把执行算法或 TCA 指标写成策略 edge、买卖点或实盘许可 |
| Audit Trail / Clock Sync | Data Engineering、Live Execution | Database/Storage | 不得把时间同步、事件追踪或 retention 写成策略信号 |
| Layered Risk / Credit / Margin | Risk Management | Live Execution、AI Engineering | 不得给风险阈值数值，不得替外接项目启用 hard gate |
| Resilience / Incident / Log | Live Execution、Database/Storage | Risk Management | 不得把 incident label 自动解释成停机、拒单或撤单动作 |
| Stress Testing / Scenario Risk | Risk Management | Trade Analysis、AI Engineering | 不得把 stress result 当作仓位建议或交易放行 |
| Order Type / TIF / Venue Semantics | Live Execution、Replay/Simulation | Market Microstructure | 不得把某个交易所语义泛化为所有市场 |
| Reference Data / Entitlement | Data Engineering | Market Microstructure、Database/Storage | 不得把 reference data 当作 feature signal 或策略条件 |
| Crypto Perpetual | Market Microstructure、Risk Management | Live Execution、Data Engineering | 不得把 crypto perpetual 特有规则泛化到股票、期货或外汇 |

## CandidateKnowledgeItem 输入契约

每条候选必须包含：

```json
{
  "research_task_id": "P45-A-TCA01",
  "knowledge_slug": "execution_tca.implementation_shortfall_required.v1",
  "classification": {
    "primary_partition": "KB_07_TRADE_ANALYSIS",
    "canonical_node_id": "kt.trade_analysis.execution_tca_review",
    "domain": "trade_analysis",
    "subdomain": "execution_tca_review"
  },
  "source_refs": [],
  "source_quality": {
    "minimum_source_count": 2,
    "required_source_types": ["regulatory_doc", "official_doc", "professional_research", "standard_doc"]
  },
  "content": {
    "statement": "",
    "applies_when": [],
    "not_applicable_when": [],
    "assumptions": [],
    "anti_patterns": [],
    "validation": []
  },
  "conflict_audit": {
    "status": "unchecked",
    "checked_against": ["Phase 37 formal KB", "Phase 42 storage", "Phase 43 memory", "Phase 41 AI scoring"]
  },
  "review": {
    "review_status": "candidate",
    "approved_allowed": false,
    "default_guidance_allowed": false,
    "hard_gate_allowed": false,
    "risk_threshold_advice_allowed": false
  },
  "machine_gate": {
    "default_guidance": "deny",
    "review_visibility": "candidate_only",
    "hidden_from_default_queue": true
  }
}
```

## Formal reviewed 输出契约

审计通过并正式沉淀后，最多只能进入：

```json
{
  "review": {
    "review_status": "reviewed",
    "approved_allowed": false,
    "default_guidance_allowed": false,
    "hard_gate_allowed": false,
    "risk_threshold_advice_allowed": false
  },
  "machine_gate": {
    "default_guidance": "caveat_only",
    "review_visibility": "reviewed_caveat_only",
    "hidden_from_default_queue": true,
    "visible_in_default_guidance_queue": false
  }
}
```

`reviewed/caveat_only` 表示可被外接项目 AI IDE 用作带边界的审计上下文、设计提醒、reason code 或检索引用；不表示可作为默认指导、硬风控、交易许可、买卖点或仓位建议。

## MCP/SearchLab 契约

MCP/SearchLab 对 Phase 45 知识只读检索：

```text
1. 返回必须包含 source/citation/confidence/review_status/machine_gate。
2. 候选知识不得进入默认检索结果。
3. reviewed/caveat_only 可以返回，但必须显示 caveat。
4. approved/default guidance/hard gate 字段必须保持 false。
5. 无来源、冲突未处理、过期、乱码、mock/test 污染条目必须阻断。
```

## Vue3 展示契约

Vue3 知识树和知识详情页必须：

```text
1. 使用中文展示用户可见文案。
2. L1/L2/L3 节点从 knowledge_tree.md 和 fixture 生成。
3. 统计数量来自 formal knowledge index 和 candidates，不手写。
4. Phase 45 新 L3 节点可展示 0 条知识，但必须能显示为待补齐范围。
5. 状态标签需区分 candidate、accepted_for_draft、reviewed、approved、needs_more_evidence。
```

## 硬边界

```text
1. 不创建 approved。
2. 不启用 default guidance。
3. 不启用 hard gate。
4. 不给风险阈值数值。
5. 不生成买卖点、仓位、杠杆、止损止盈、实盘执行建议。
6. 不把 broker、交易所、监管辖区、数据商或 vendor 文档泛化为所有市场。
7. 不把 AI Engineering 变成交易执行 owner。
8. 不把 Database/Storage 变成交易策略 owner。
```

## Definition of Done

```text
1. Phase 45 范围文档、来源种子库、审计 JSON 和知识树节点已存在。
2. 每个新增 L3 节点都有明确 owner、下游和边界。
3. 后续候选生成必须按本契约写入 classification、review 和 machine_gate。
4. Vue3 fixture 重建后能显示新增节点。
5. UTF-8 无乱码。
```
