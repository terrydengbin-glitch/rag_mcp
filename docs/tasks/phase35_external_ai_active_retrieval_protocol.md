# Phase 35: 外部项目 AI 主动检索协议

## Phase 目标

让接入 CEK-TA 的外部项目 AI 在处理交易、回测、模拟盘、实盘、RAG、MCP、LLM 训练和知识治理任务时，能够主动调用 CEK-TA MCP/RAG，而不是只依赖模型记忆或把知识库全文塞进上下文。

本 Phase 输出“什么时候必须搜、怎么搜、怎么引用、没搜到怎么办”的接入模板和测试。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-173 | P0 | done | 定义外部项目 AI 主动检索协议 | `docs/contracts/external_ai_active_retrieval_protocol.md` | CEK-TA-172 |
| CEK-TA-174 | P0 | done | 创建外部项目 AGENTS 主动检索模板 | `codex-expert-kit/templates/external_project_active_retrieval_AGENTS.md` | CEK-TA-173 |
| CEK-TA-175 | P0 | done | 更新外部项目 AGENTS 模板引用主动检索协议 | `codex-expert-kit/templates/external_project_AGENTS.md` | CEK-TA-174 |
| CEK-TA-176 | P1 | done | 创建主动检索测试计划 | `codex-expert-kit/templates/external_project_active_retrieval_test_plan.md` | CEK-TA-174 |
| CEK-TA-177 | P1 | done | 增加主动检索协议 pytest 验证 | `codex-expert-kit/mcp/tests/test_external_ai_active_retrieval_protocol.py` | CEK-TA-176 |
| CEK-TA-178 | P1 | done | 更新任务索引并完成验收 | `docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-177 |
| CEK-TA-262 | P1 | done | 调整 MCP 默认检索信用语义：正式入库 reviewed 知识默认作为 accepted_reference 返回，approved/allow 仍作为高置信默认指导 | `codex-expert-kit/mcp/common.py`、`docs/contracts/external_ai_active_retrieval_protocol.md`、`codex-expert-kit/templates/external_project_active_retrieval_AGENTS.md`、`codex-expert-kit/mcp/tests/` | CEK-TA-178 |

## 上游输入

```text
1. Phase 21 正式 knowledge_items.json 聚合索引。
2. Phase 22 path_resolver 和 CEK_TA_ROOT 接入方式。
3. Phase 34 machine_gate/default_guidance 安全门控。
4. MCP search_expert_knowledge、get_knowledge_item、browse_knowledge_tree。
5. codex-expert-kit/templates/external_project_AGENTS.md。
```

## 下游输出

```text
1. 外部项目 AGENTS.md 可复制的主动检索规则。
2. AI 知道什么任务必须先搜 CEK-TA。
3. AI 知道如何构造 search_expert_knowledge 请求。
4. AI 知道如何引用 knowledge_id、source 和 machine_gate。
5. AI 知道无命中时创建缺口/采集/回灌任务，而不是编造规则。
6. 测试可以验证模板包含强制检索、引用和无命中处理规则。
```

## 输入契约

外部项目必须提供项目事实：

```text
project_name
project_type
market
asset/symbol
timeframe
environment
task_type
affected_modules
```

CEK-TA MCP 必须可用：

```text
search_expert_knowledge
get_knowledge_item
browse_knowledge_tree
```

## 输出契约

AI 在专业任务中必须输出：

```text
1. retrieval_required: true/false
2. retrieval_queries: 使用过的 MCP 查询
3. knowledge_used: knowledge_id 列表
4. machine_gate: allow/caveat_only/deny
5. acceptance_level: approved_guidance/accepted_reference/blocked_reference
6. source_refs: 来源或 source_count
7. applicability_check: 适用/不适用边界
8. no_hit_action: none/create_gap/create_research_task/ask_human
```

## 必须主动检索的任务

```text
1. 策略设计、策略审计、信号解释、指标边界。
2. K 线结构、周期、形态、技术指标、信号泛化。
3. 回测可信度、数据泄漏、过拟合、成本、滑点、fill model。
4. 回放、模拟盘、paper trading、撮合语义。
5. 实盘执行、订单状态机、仓位同步、安全停机。
6. 风控、仓位、风险预算、组合暴露、日亏损。
7. 交易分析、坏例归因、R/R 分解、复盘标签。
8. RAG、MCP、知识治理、来源评分、冲突阻断。
9. LLM 训练、数据集、评测、泄漏控制、RAG vs fine-tune。
10. 外部项目回灌 CEK-TA 的知识贡献。
```

## 搜索策略

```text
1. 先根据 task_type 选择 domain 或 tree_node_id。
2. top_k 默认 5，最大不超过 20。
3. 默认 include.reviewed = true，include.default_guidance_only = false，返回正式入库的 reviewed/approved 知识。
4. reviewed/caveat_only 是 accepted_reference，可用于 AI IDE 开发、审计和规范对齐，但不是 approved 默认交易指导。
5. 如果需要只取高置信默认指导，可显式设置 include.default_guidance_only = true，此时只返回 machine_gate.default_guidance = allow。
6. 不允许把 blocked_results 当成默认指导。
```

## 引用规则

AI 引用 CEK-TA 知识时必须至少写：

```text
knowledge_id
title
machine_gate.default_guidance
review_status
conflict_status
source_count 或 source_refs
适用边界
```

推荐格式：

```text
依据 CEK-TA: kb_04_backtest.bias.multiple_testing_overfit.v1
gate: allow
scope: backtest_review / general market / general timeframe
source: 2 refs
```

## 无命中处理

如果没有命中 allow 知识：

```text
1. 不得编造专业规则。
2. 如果有 caveat_only，说明只能作为审计线索，不能默认指导。
3. 如果只有 blocked_results，说明阻断原因。
4. 如果完全无结果，创建 knowledge gap 或 research ingestion task。
5. 高风险任务必须 ask_human。
```

## 边界范围

### 本 Phase 做

```text
1. 定义外部项目主动检索协议。
2. 提供 AGENTS.md 模板。
3. 提供测试计划。
4. 增加模板与 MCP 检索行为测试。
```

### 本 Phase 不做

```text
1. 不改变 MCP tool 权限。
2. 不引入外部服务。
3. 不引入数据库。
4. 不让 AI 自动 approved 知识。
5. 不让外部项目直接写 CEK-TA 正式知识。
```

## 涉及组件

```text
docs/contracts/external_ai_active_retrieval_protocol.md
codex-expert-kit/templates/external_project_active_retrieval_AGENTS.md
codex-expert-kit/templates/external_project_AGENTS.md
codex-expert-kit/templates/external_project_active_retrieval_test_plan.md
codex-expert-kit/mcp/tests/test_external_ai_active_retrieval_protocol.py
```

## 测试与验收

```text
python -m pytest codex-expert-kit/mcp/tests/test_external_ai_active_retrieval_protocol.py
```

测试必须覆盖：

```text
1. 模板包含 must search / search_expert_knowledge / machine_gate。
2. 模板包含 how to cite / no hit action。
3. 默认 MCP 检索能返回 formal knowledge，包括 reviewed/caveat_only accepted_reference。
4. reviewed/caveat_only 不会被提升为 approved/default guidance。
```

## Definition of Done

```text
1. Phase 35 任务卡已创建。
2. 主动检索协议文档存在。
3. 外部项目 AGENTS 主动检索模板存在。
4. 原外部项目 AGENTS 模板已引用主动检索模板。
5. 测试计划存在。
6. pytest 验证通过。
7. docs/index_tasks.md 和 docs/tasks/README.md 已更新。
```

## 风险与回滚

```text
风险：外部项目 AI 过度检索，影响速度。
缓解：使用 task_type/domain/tree_node_id/top_k/default_guidance_only 控制范围。

风险：AI 把 caveat_only 当默认指导。
缓解：模板和测试强制 machine_gate 引用。

回滚：移除 Phase 35 模板引用，外部项目仍可按 Phase 8/10 的旧接入方式使用 CEK-TA。
```
