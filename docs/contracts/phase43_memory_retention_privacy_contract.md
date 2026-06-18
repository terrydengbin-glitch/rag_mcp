# Phase 43 Memory Retention Privacy Contract

## 目标

外接项目记忆会跨会话长期影响 AI IDE / Agent 行为，不能无限期保存所有内容。每个外接项目必须显式定义 retention、deletion、export、privacy minimization 和 tombstone 规则。

## 保留策略

```text
1. goal、boundary、decision 默认可长期保留，但必须支持 supersede 和 deprecate。
2. task 完成后应进入 closed / archived 状态，默认不再注入上下文。
3. artifact 只保存引用、摘要、版本和 hash，不保存大型原始内容。
4. lesson 可长期保留，但必须记录适用范围和过期条件。
5. event_log 应有保留周期，不能无限期保存全部对话过程。
```

## 删除与 tombstone

```text
1. 不建议物理删除 active memory，优先 tombstone + audit event。
2. 涉及敏感数据或合规要求时，允许物理删除内容，但保留不可逆脱敏 tombstone。
3. tombstone 至少记录 memory_id、删除原因、执行者、时间和影响范围。
4. 删除不得破坏审计链和引用完整性。
```

## 导出策略

```text
1. export_memory 必须按 project_id 和 visibility_scope 授权。
2. 导出内容必须包含 MemoryItem、MemoryEvent、MemoryLink 和 schema version。
3. 导出前必须执行 secret scan。
4. 导出包必须记录 export_hash、exported_by、exported_at 和用途。
```

## 隐私最小化

```text
1. 长期记忆只保留完成任务所需的最小信息。
2. 私有账户、资金、订单和密钥字段不得进入长期记忆。
3. 外部项目私有策略参数默认只保留摘要和引用，不保留原始值。
4. 任何跨项目记忆复用都必须先脱敏并经过人工确认。
```

## 失效与复核

```text
1. MemoryItem 应支持 valid_to 或 review_after。
2. 过期后默认不注入上下文。
3. 目标、架构、权限、依赖发生重大变化时，应触发 memory freshness review。
4. stale memory test 必须覆盖目标过期、任务完成、决策废弃和权限变化。
```
