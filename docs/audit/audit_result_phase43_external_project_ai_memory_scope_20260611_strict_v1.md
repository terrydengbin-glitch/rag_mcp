# Phase 43 External Project AI Memory Layer 范围严格审计结果

## 审计结论

```text
decision: accept_with_patch
reviewed_allowed: false
approved_allowed: false
default_guidance_allowed: false
hard_gate_allowed: false
```

Phase 43 可以成立，并应挂在：

```text
kt.ai_engineering.external_project_memory
```

但必须先完成结构和优先级 patch 后，才能进入候选知识采集。

## 允许推进

```text
1. 创建 Phase 43: External Project AI Memory Layer。
2. 挂在 AI Engineering 下。
3. 生成候选知识点。
4. 定义 Memory Contract / MemoryItem schema / Project Memory MCP / adapter selection。
```

## 禁止事项

```text
1. 不允许直接 formal reviewed。
2. 不允许直接 approved。
3. 不允许直接 default guidance。
4. 不允许直接 hard gate。
5. CEK-TA 不保存外接项目私有记忆。
6. 不自动把所有聊天写入长期记忆。
7. AI 不直接写 active memory。
8. 第三方 memory engine 不能作为 CEK-TA 核心契约。
```

## 必须 patch

```text
1. 新增 L3: memory_mcp_api_contract。
2. 新增 L3: memory_retention_privacy。
3. P43-P0E-004 memory poisoning / prompt injection 上调为 P0。
4. P43-P0E-005 rollback / integrity 上调为 P0。
5. P43-P1-003 memory quality regression 上调为 P0E。
6. 拆分 P43-P1-002:
   - PostgreSQL JSONB canonical store -> P0。
   - pgvector optional semantic index -> P1。
7. 增强 P43-P0-013:
   - prompt_injection_scan。
   - memory_poisoning_scan。
   - untrusted_input flag。
8. 新增知识点:
   - Project Memory MCP/API minimal permission contract。
   - Memory retention / deletion / export policy。
   - Memory conflict resolution contract。
   - Adapter portability test。
```

## 执行结果

```text
1. 已新增 memory_mcp_api_contract 和 memory_retention_privacy 两个 L3。
2. 知识点范围已从 24 条调整为 29 条。
3. 采集优先级调整为 P0-Core 22 / P0-Extended 4 / P1 3。
4. MemoryItem schema 已补充 source_trust、write_policy、secret_scan_status、integrity。
5. Project Memory MCP/API 契约已补充最小权限工具集和 admin 工具边界。
6. 已新增 retention/privacy 契约。
7. 修订版审计包已输出到 `docs/audit/phase43_external_project_ai_memory_scope_for_audit.json`。
```
