# CEK-TA

CEK-TA 是一个交易与 AI 项目的支持层，用来给外部项目提供：

```text
1. 专业交易 / AI Engineering / RAG / MCP 知识库。
2. Codex 专家工作流和项目接入规范。
3. 只读 MCP 知识检索能力。
4. Vue3 知识审计工作台。
5. 候选知识审计、正式知识沉淀和知识倒灌流程。
```

本项目不保存外部业务项目的私有策略、账户、密钥或实盘事实。外部项目只提供项目事实，CEK-TA 提供可复用的专业知识、来源、边界和审计规则。

## 一分钟接入

外部项目只想先验证能否调用知识库时，按下面顺序做：

```powershell
$env:CEK_TA_ROOT = "替换为你的 CEK-TA 根目录"
cd $env:CEK_TA_ROOT
python codex-expert-kit/mcp/server.py --info
python codex-expert-kit/mcp/server.py --list-tools
python codex-expert-kit/mcp/server.py --call search_expert_knowledge --request-json "{\"query\":\"lookahead bias\",\"top_k\":3}"
```

如果需要指定正式知识索引：

```powershell
$env:CEK_TA_KNOWLEDGE_ITEMS_PATH = "$env:CEK_TA_ROOT\codex-expert-kit\rag\indexes\knowledge_items.json"
python codex-expert-kit/mcp/server.py --info
```

健康检查通过后，再把模板复制到业务项目的 Codex MCP 配置中：

```text
codex-expert-kit/templates/codex_config_mcp.toml
```

默认模板使用 `enabled = false`。只有当 `--info`、`--list-tools` 和一次查询 smoke test 通过后，业务项目才应改为 `enabled = true`。

完整接入手册：

- [外部项目 MCP 快速接入手册](./docs/external_mcp_quickstart.md)
- [其他项目接入指南](./docs/其他项目接入指南.md)
- [MCP server 规格](./codex-expert-kit/mcp/mcp_server_spec.md)
- [正式知识索引说明](./codex-expert-kit/rag/indexes/README.md)

## MCP 调用边界

CEK-TA MCP 是只读知识检索层：

```text
允许：搜索正式知识、读取来源、读取冲突状态、浏览知识树。
禁止：下单、读取账户、读取密钥、写知识、批准知识、把候选知识当默认指导。
```

使用结果时必须关注：

```text
source / citation
confidence
review_status
conflict_status
machine_gate
default_guidance_allowed
approved_allowed
hard_gate_allowed
```

`reviewed` 或 `caveat_only` 代表可用于审计和检索，不等于 `approved`，也不会自动成为默认指导或 hard gate。

## 项目管理入口

[docs/index_tasks.md](./docs/index_tasks.md)

## 开发规范入口

[AGENTS.md](./AGENTS.md)

## 核心文档

- [docs/需求框架.md](./docs/需求框架.md)
- [docs/任务需求清单.md](./docs/任务需求清单.md)
- [docs/知识库采集与审计规范.md](./docs/知识库采集与审计规范.md)
- [docs/Vue3知识审计界面需求.md](./docs/Vue3知识审计界面需求.md)
- [docs/其他项目接入指南.md](./docs/其他项目接入指南.md)
- [docs/知识倒灌与反哺规范.md](./docs/知识倒灌与反哺规范.md)
- [docs/knowledge_research_backlog.md](./docs/knowledge_research_backlog.md)
- [docs/knowledge_tree_v2_integration_plan.md](./docs/knowledge_tree_v2_integration_plan.md)
- [codex-expert-kit/rag/quality_metrics.md](./codex-expert-kit/rag/quality_metrics.md)
- [codex-expert-kit/rag/eval_sets/README.md](./codex-expert-kit/rag/eval_sets/README.md)
- [codex-expert-kit/templates/knowledge_quality_report.md](./codex-expert-kit/templates/knowledge_quality_report.md)
- [docs/seed_knowledge_assets_plan.md](./docs/seed_knowledge_assets_plan.md)
- [docs/reports/seed_knowledge_quality_report.md](./docs/reports/seed_knowledge_quality_report.md)
- [docs/tasks/phase19_seed_runtime_validation.md](./docs/tasks/phase19_seed_runtime_validation.md)
- [docs/tasks/phase20_searchlab_mcp_runtime_quality.md](./docs/tasks/phase20_searchlab_mcp_runtime_quality.md)
- [docs/seed_runtime_validation_plan.md](./docs/seed_runtime_validation_plan.md)
- [docs/reports/seed_runtime_validation_report.md](./docs/reports/seed_runtime_validation_report.md)
- [docs/searchlab_mcp_runtime_contract.md](./docs/searchlab_mcp_runtime_contract.md)
- [codex-expert-kit/rag/eval_sets/runtime_ranking_eval_cases.json](./codex-expert-kit/rag/eval_sets/runtime_ranking_eval_cases.json)
- [docs/reports/runtime_ranking_quality_report.md](./docs/reports/runtime_ranking_quality_report.md)
- [docs/reports/searchlab_mcp_runtime_quality_report.md](./docs/reports/searchlab_mcp_runtime_quality_report.md)
- [docs/tasks/phase21_formal_mcp_knowledge_index.md](./docs/tasks/phase21_formal_mcp_knowledge_index.md)
- [codex-expert-kit/rag/scripts/build_knowledge_items_index.py](./codex-expert-kit/rag/scripts/build_knowledge_items_index.py)
- [codex-expert-kit/rag/indexes/knowledge_items.json](./codex-expert-kit/rag/indexes/knowledge_items.json)
- [docs/reports/formal_mcp_knowledge_index_report.md](./docs/reports/formal_mcp_knowledge_index_report.md)
- [docs/tasks/phase22_path_resolver_foundation.md](./docs/tasks/phase22_path_resolver_foundation.md)
- [codex-expert-kit/core/path_resolver.py](./codex-expert-kit/core/path_resolver.py)
- [codex-expert-kit/rag/knowledge/KB_10_PROJECT_RUNBOOKS/kb_10_project_runbooks.path_resolver.portable_paths.v1.json](./codex-expert-kit/rag/knowledge/KB_10_PROJECT_RUNBOOKS/kb_10_project_runbooks.path_resolver.portable_paths.v1.json)
- [docs/reports/path_resolver_foundation_report.md](./docs/reports/path_resolver_foundation_report.md)
- [docs/tasks/phase23_partition_wide_research_ingestion.md](./docs/tasks/phase23_partition_wide_research_ingestion.md)
- [docs/research/phase23_partition_collection_plan.md](./docs/research/phase23_partition_collection_plan.md)
- [docs/research/phase23_source_seed_catalog.md](./docs/research/phase23_source_seed_catalog.md)
- [docs/research/phase23_research_task_queue.md](./docs/research/phase23_research_task_queue.md)

## 项目技能

- [.agents/skills/cek-ta-development-workflow/SKILL.md](./.agents/skills/cek-ta-development-workflow/SKILL.md)

## Vue3 知识审计界面

- [ui/](./ui/)

本地启动：

```text
cd ui
npm install
npm run dev
```

## 知识倒灌队列

- [contributions/](./contributions/)

倒灌必须走：

```text
proposed -> sanitized -> sourced -> classified -> conflict_checked -> reviewed -> accepted
```
