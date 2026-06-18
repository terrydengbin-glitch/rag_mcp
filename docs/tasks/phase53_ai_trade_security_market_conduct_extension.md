# Phase 53: AI/Trading 安全、市场行为与运行治理知识扩展

## 任务目标

承接 Phase 52 的权威资料缺口复审结果，针对 AI Engineering 与 Trading Engineering 两条主线补齐高价值治理型知识：

```text
1. Trading AI Agent Threat Model
2. AI SBOM / Model SBOM
3. Market Conduct Surveillance
4. Market Access / DEA / Reg NMS Boundary
5. Time Synchronization Audit
```

本 Phase 的目标是生成有来源、有边界、有审计追踪的候选知识，并在外部 AI/人工严格审计后沉淀为 formal reviewed/caveat_only。默认不得创建 approved、default guidance 或 hard gate。

## 上游输入

```text
docs/reports/phase52_ai_trade_authoritative_gap_audit_report.md
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/knowledge_tree.md
docs/tasks/phase52_ai_trade_authoritative_gap_audit.md
```

权威来源种子：

```text
NIST AI RMF
OWASP Top 10 for LLM Applications
MITRE ATLAS
CISA SBOM / AI SBOM guidance
SEC Rule 15c3-5 Market Access
FINRA Manipulative Trading
CFTC Disruptive Trading Practices
ESMA MiFID II Article 17
FIXatdl / FIX Trading Community
OpenTelemetry
```

## 下游输出

```text
docs/research/phase53_ai_trade_security_market_conduct_scope.md
docs/research/phase53_research_task_queue.md
docs/research/phase53_source_seed.md
docs/audit/phase53_knowledge_scope_for_audit.json
codex-expert-kit/rag/candidates/
docs/audit/phase53_candidate_audit_package_*.json
docs/reports/phase53_*_report.*
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/indexes/knowledge_items.json
ui/public/data/
```

## 输入契约

### Knowledge Gap 输入

每条缺口必须具备：

```text
gap_id
target_branch
target_l2
target_l3
claim_boundary
source_seed
expected_candidate_count
priority
out_of_scope
```

### Source 输入

来源必须标注：

```text
source_id
source_type
publisher
url
retrieved_at
authority_level
jurisdiction_or_scope
supports_claim
does_not_support
```

## 输出契约

### 候选知识输出

候选知识必须包含：

```text
candidate_id
research_task_id
proposed_knowledge_id
canonical_node_id
tree_node_id
claim_type
content.statement
applies_when
not_applicable_when
source_evidence
source_quality
conflict_audit
review
llm_usage_policy
machine_gate
workflow
```

### 审计包输出

审计包必须明确：

```text
1. candidate 不是正式知识。
2. accepted_for_draft 不等于 reviewed。
3. reviewed 不等于 approved。
4. 本 Phase 默认禁止 approved/default guidance/hard gate。
5. 审计方必须搜索相关专业网站、官方资料、案例和数据进行严格审计。
6. 审计输出必须给出 decision、confidence、patch_notes、required_followups。
```

## 边界范围

范围内：

```text
1. AI/LLM/Agent 安全治理知识。
2. AI SBOM / Model SBOM / 数据集和依赖供应链清单知识。
3. 市场行为监控 taxonomy，包括 spoofing、layering、wash/self-trade、momentum ignition 等风险识别边界。
4. Market Access / DEA / sponsored access / Reg NMS / MiFID II Algorithmic Trading 的监管边界知识。
5. 交易事件时间同步、clock source、timestamp precision、drift policy、审计日志时间序知识。
```

范围外：

```text
1. 不输出法律意见。
2. 不输出交易信号。
3. 不输出买卖点、仓位、杠杆、止损止盈。
4. 不输出风控阈值、信用额度或保证金比例。
5. 不把任何监管条款泛化为所有市场通用规则。
6. 不直接创建 approved/default guidance/hard gate。
7. 不绑定单一安全、监控、可观测或交易平台。
```

## 涉及组件

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase53_ai_trade_security_market_conduct_extension.md
docs/research/
docs/audit/
docs/reports/
codex-expert-kit/rag/candidates/
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/indexes/
codex-expert-kit/rag/scripts/
ui/public/data/
```

## 涉及数据结构

```text
KnowledgeItem
CandidateKnowledgeItem
ResearchIngestionTask
SourceEvidence
ConflictAudit
MachineGate
LLMUsagePolicy
AuditPackage
RuntimeLinkageReport
```

## 涉及数据库/存储

本 Phase 不引入新数据库。正式知识仍使用文件化 JSON + 聚合索引。

如果后续将 SBOM、市场行为监控事件或时间同步审计日志落到数据库，必须另建 Phase 定义表结构、索引、迁移和回滚。

## 实施步骤

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-518 | P0 | done | 定义 Phase 53 知识范围、L2/L3 节点和跨分支边界 | `docs/research/phase53_ai_trade_security_market_conduct_scope.md` | CEK-TA-517 |
| CEK-TA-519 | P0 | done | 创建 Phase 53 来源种子库和 ResearchIngestionTask 队列 | `docs/research/phase53_source_seed.md`、`docs/research/phase53_research_task_queue.md` | CEK-TA-518 |
| CEK-TA-520 | P0 | done | 生成 Phase 53 知识范围审计 JSON | `docs/audit/phase53_knowledge_scope_for_audit.json` | CEK-TA-519 |
| CEK-TA-521 | P1 | done | 联网采集 5 条 P0 候选知识并运行来源/冲突/乱码门禁 | `codex-expert-kit/rag/candidates/`、`docs/reports/phase53_candidate_generation_report.md` | CEK-TA-520 |
| CEK-TA-522 | P1 | done | 导出 Phase 53 候选 AI 审计包 | `docs/audit/phase53_candidate_audit_package_20260613.json`、`docs/reports/phase53_candidate_quality_gate.json` | CEK-TA-521 |
| CEK-TA-523 | P1 | done | 导入审计结果，按 patch notes 补证、重建或阻断候选 | `docs/reports/phase53_audit_import_report.json`、`ui/public/data/` | CEK-TA-522 |
| CEK-TA-524 | P1 | done | 将通过 reviewed-preparation 的候选沉淀为 formal reviewed/caveat_only 并重建索引；对剩余 AI Security/SBOM 候选导出补证二审包 | `codex-expert-kit/rag/knowledge/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`docs/audit/phase53_ai_security_sbom_supplemental_reaudit_package_20260613.json`、`docs/reports/phase53_ai_security_sbom_supplemental_reaudit_import_report.json` | CEK-TA-523 |
| CEK-TA-525 | P1 | done | 验证 MCP/SearchLab/KnowledgeTree/Vue3 能命中、引用、阻断和正确展示 Phase 53 知识 | `docs/reports/phase53_runtime_linkage_validation_report.json` | CEK-TA-524 |
| CEK-TA-526 | P1 | done | 生成 Phase 53 验收报告并更新任务索引 | `docs/reports/phase53_ai_trade_security_market_conduct_extension_report.md` | CEK-TA-525 |

## 建议 P0 知识点

| gap_id | canonical_node_id 建议 | 知识点 | 优先级 | 初始来源 |
| --- | --- | --- | --- | --- |
| GAP-AI-01 | `kt.ai_engineering.security_governance.agent_threat_model` | Trading AI Agent Threat Model 必须覆盖 prompt injection、tool misuse、memory poisoning、excessive agency、overreliance | P0 | OWASP, MITRE ATLAS, NIST AI RMF |
| GAP-AI-02 | `kt.ai_engineering.supply_chain_governance.ai_sbom` | AI SBOM / Model SBOM 必须记录模型、adapter、数据集、依赖、容器、许可证和推理服务 | P0 | CISA SBOM, OWASP Supply Chain, NIST AI RMF |
| GAP-TR-01 | `kt.trading_engineering.market_conduct.surveillance_taxonomy` | 市场行为监控必须区分 spoofing、layering、wash/self-trade、momentum ignition 等风险 | P0 | FINRA, CFTC |
| GAP-TR-02 | `kt.trading_engineering.market_access.regulatory_boundary` | Market Access / DEA / sponsored access 需要金融、监管、信用和错误订单控制证据 | P0 | SEC Rule 15c3-5, ESMA MiFID II Article 17 |
| GAP-TR-03 | `kt.trading_engineering.audit_trace.time_synchronization` | 订单、行情、成交、风控和审计日志必须声明 clock source、sync status、timestamp precision 和 drift policy | P0 | OpenTelemetry, venue audit guidance, time sync standards |

## Definition of Done

```text
1. Phase 53 已登记到 docs/index_tasks.md。
2. Phase 53 已登记到 docs/tasks/README.md。
3. Phase 53 任务卡包含上下游、契约、边界、DoD 和测试。
4. 每个候选知识都有权威来源和明确适用边界。
5. 候选、reviewed、approved 状态不混淆。
6. MCP/SearchLab/KnowledgeTree/Vue3 联动验证通过后才能标记 done。
7. UTF-8 与中文乱码检查通过。
```

## 测试与验收

```text
1. 文档存在性检查。
2. UTF-8 读取检查。
3. mojibake 检查。
4. 候选质量门禁：来源、冲突、边界、review_status、machine_gate。
5. MCP/SearchLab 查询验证：能命中、能返回来源、能阻断 default guidance 误用。
6. Vue3 展示验证：知识树节点统计正确，用户可见文案为中文。
```

## 风险与回滚

风险：

```text
1. 监管资料具有地域边界，不能泛化为所有市场。
2. 市场行为监控知识容易被误读成法律结论。
3. AI 安全知识容易被误读成阻断交易的 hard gate。
4. 时间同步知识容易被误读成高频策略建议。
```

回滚：

```text
1. 删除 Phase 53 新增候选、报告和审计包。
2. 从 docs/index_tasks.md 和 docs/tasks/README.md 移除 Phase 53 入口。
3. 如已生成 formal reviewed，必须通过单独治理任务回滚索引和前端 fixture。
```

## 需要开发者确认的问题

```text
1. Phase 53 是否先只做 5 条 P0，还是同时扩展 P1。
2. Market Access / Reg NMS 是否限定美国证券市场，还是同时覆盖 EU MiFID II 与 crypto venue。
3. AI SBOM 是否只做知识契约，还是后续要为外接项目生成实际 SBOM 模板。
```
