# Trading Engineering 与 AI Engineering 跨分支引用契约

## 目标

本契约用于 Phase 37，定义 Trading Engineering 与 AI Engineering 的知识边界、引用方式、字段契约和审计门禁，避免交易专业规则本体被复制到 AI Engineering，也避免 AI 训练、RAG、MCP 或模型部署规则污染 Trading Engineering。

## 核心原则

```text
1. Trading Engineering 是交易专业规则本体的 owner。
2. AI Engineering 只能通过 knowledge_refs / retrieved_knowledge / reason_codes 引用 Trading Engineering。
3. 交易规则修订后，AI Engineering 的训练、评测、rubric、gate、memory 和 runtime contract 必须重新验证。
4. 任何跨分支引用都不得绕过 candidate -> reviewed/caveat_only -> human approved 的治理链路。
5. reviewed 不等于 approved，不自动进入 default guidance。
```

## Trading Engineering 拥有的内容

```text
1. 量化基础、期望值、R/R、成本、仓位和交易决策流。
2. 市场数据工程、时间对齐、缺失重复、时区、数据版本和合约归一。
3. K 线结构、指标边界、多周期、入场、止损和止盈。
4. 市场微观结构、盘口、流动性、订单流、滑点和冲击成本。
5. 回测可信度、数据泄漏、过拟合、样本外、成本模型和可复现。
6. 回放模拟、fill model、同根 K TP/SL、partial fill、延迟和 paper/live gap。
7. 实盘执行、订单状态机、仓位同步、kill switch 和事故恢复。
8. 风险管理、单笔风险、日亏损、组合暴露和风控闸门。
9. 交易复盘、坏例 taxonomy、R/R 分解、MAE/MFE 和交易质量归因。
```

## AI Engineering 只能拥有的内容

```text
1. 如何检索 Trading Engineering 知识。
2. 如何把 Trading Engineering 知识转成训练样本字段、标签、rubric 或 eval case。
3. 如何让 LLM 审计助手引用 Trading Engineering 来源和 reason code。
4. 如何做 scorer、calibrator、threshold、final gate、shadow/paper/OPE 和模型发布治理。
5. 如何控制上下文预算、RAG 引用、MCP tool contract、memory contract 和安全治理。
```

## 禁止跨分支复制

AI Engineering 不得复制或改写 Trading Engineering 的规则本体。例如：

```text
禁止：在 AI Engineering 写“同根 K TP/SL 应如何排序”的规则本体。
允许：在 AI Engineering 写“LLM 审计时必须引用 kt.trading_engineering.replay_simulation.fill_model 中的同根 K TP/SL 知识”。

禁止：在 AI Engineering 写“单笔风险不得超过 X%”这类交易规则本体。
允许：在 AI Engineering 写“scorer/final gate 必须读取 Trading Engineering 的 risk_management.single_trade_risk_limit_required 知识引用”。
```

## 引用字段契约

AI Engineering、外部项目和候选知识如果引用 Trading Engineering，必须使用：

```json
{
  "knowledge_refs": [
    {
      "knowledge_id": "string",
      "canonical_node_id": "kt.trading_engineering.<partition>.<topic>",
      "review_status": "candidate | reviewed | approved",
      "usage": "training_schema | eval_case | llm_audit | final_gate_reason | search_context",
      "required": true,
      "allowed_as_default_guidance": false,
      "citation_required": true
    }
  ]
}
```

## 候选知识分类契约

Trading Engineering 候选必须包含：

```text
primary_branch = Trading Engineering
primary_partition = KB_01_QUANT_FOUNDATION / KB_02_DATA_ENGINEERING / ...
canonical_node_id = kt.trading_engineering.<partition>.<topic>
claim_type = boundary_rule | definition | audit_checklist | runtime_constraint | risk_control_rule
source_evidence >= 2
applicability
not_applicable_when
assumptions
conflict_audit
llm_usage_policy
machine_gate
related_ai_engineering_nodes
```

## AI 使用边界

Trading Engineering 知识可以被 AI 用于：

```text
1. 解释交易工程边界。
2. 审计策略、回测、模拟盘、实盘执行和交易复盘方案。
3. 给外部 AI IDE 提供代码设计约束。
4. 给 LLM scoring/gating 项目提供字段、标签、eval case 和 reason code 的引用依据。
```

不得用于：

```text
1. 生成具体买卖点。
2. 生成仓位、杠杆、止损止盈或实盘执行命令。
3. 替代交易所、券商、监管、风控或人工审批。
4. 在未获 approved 的情况下进入默认指导队列。
```

## 修订联动

```text
1. Trading Engineering 知识修订时，引用它的 AI Engineering 知识必须记录 impacted_by。
2. 如果交易规则从 reviewed 升级为 approved，AI Engineering 仍需单独审计是否可进入 default guidance。
3. 如果交易规则降级为 conflict/expired，AI Engineering 相关训练样本、eval case、rubric 和 gate 必须重新检查。
```

## 下游消费方

```text
docs/research/phase37_trading_engineering_research_task_queue.md
codex-expert-kit/rag/candidates/
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/indexes/knowledge_items.json
ui/src/data/formalKnowledgeItems.ts
MCP/SearchLab/FastAPI/Vue3
外部 LLM gating/scoring 项目
```

## 审计门禁

```text
1. source_refs 为空则不得进入 candidate_ready。
2. conflict_status unresolved 则不得进入 reviewed。
3. candidate / accepted_for_draft / reviewed 均不得自动 approved。
4. 如果内容描述 AI 训练、RAG、MCP、部署或 memory，而不是交易规则本体，应移出 Trading Engineering。
5. 如果内容包含项目私有策略参数、账户事实、密钥或实盘配置，应拒绝或脱敏后重做。
```
