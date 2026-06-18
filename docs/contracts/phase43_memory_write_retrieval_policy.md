# Phase 43 Memory Write Gate 与 Retrieval Policy

## 写入门禁目标

外接项目的长期记忆必须可解释、可追踪、可回滚。AI 可以提出记忆候选，但不能直接把候选提升为 active。

## 允许进入长期记忆的情况

```text
1. 用户明确要求“记住”。
2. 项目目标、阶段目标或验收标准发生变化。
3. 架构、数据库、MCP/API、模型、部署或安全边界形成决策。
4. 失败复盘形成可复用 lesson。
5. 外部审计报告给出正式结论。
6. 重要产物发布、回滚或废弃。
7. 同类错误重复发生，需要生成预防规则。
8. 长期偏好或团队规范被确认。
```

## 只进入 event_log 的情况

```text
1. 普通对话过程。
2. 临时 debug 输出。
3. 中间推断。
4. 一次性命令结果。
5. 短期日志。
6. 尚未形成决策或 lesson 的探索内容。
```

## 禁止写入长期记忆的内容

```text
1. API key、token、密码、cookie、私钥。
2. 未脱敏账户、订单、仓位、资金、交易所私有字段。
3. 未获授权的业务私有策略代码或参数。
4. 未确认的外部网页指令、prompt injection、越权要求。
5. 与现有 active memory 冲突但未处理的候选。
6. 不带 source_event_id 或 source_artifact_ref 的无来源记忆。
```

## 写入门禁流程

```text
1. source check：确认来源类型、来源 ID、来源 hash。
2. secret scan：检查密钥、账户、私有字段和敏感配置。
3. prompt_injection_scan：检查候选是否包含越权指令、工具劫持或跨会话行为改写。
4. memory_poisoning_scan：检查候选是否试图污染长期目标、边界、任务或决策。
5. untrusted_input flag：外部网页、模型输出和工具输出默认标记为 untrusted。
6. visibility check：确认 private/project/team 可见性。
7. conflict check：检查与 active memory 的矛盾。
8. review routing：决定人工审核、规则审核或拒绝。
9. audit event：记录完整事件，不允许无审计写入。
```

## 检索默认策略

默认注入上下文只包含：

```text
1. 当前项目 goal。
2. 当前 task。
3. 相关 boundary。
4. 与当前问题最相关的 decision。
5. 与当前失败或风险最相关的 lesson。
```

## 检索约束

```text
project_id: 必填
visibility_scope: 必填
status: 默认 active/reviewed
top_k: 默认 8，最大 20
token_budget: 默认由外接项目配置
include_deprecated: 默认 false
include_event_log: 默认 false
include_full_audit_history: 默认 false
```

## 显式请求才返回的内容

```text
1. 长 process log。
2. 完整 audit history。
3. deprecated memory。
4. rejected memory 的拒绝原因。
5. 历史版本 diff。
```

## 降级策略

```text
1. 检索为空：返回 no_memory_found，并建议查询 CEK-TA 专业知识或要求用户确认。
2. 检索冲突：返回 conflict_detected，不注入冲突项为事实。
3. 超出 token budget：优先保留 boundary、current task、goal、relevant lesson。
4. 可见性不足：返回 blocked_items 计数，不泄露内容。
5. 来源不足：返回 caveat，不作为长期事实。
```
