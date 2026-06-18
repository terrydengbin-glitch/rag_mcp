# KnowledgeTree FastAPI Runtime Plan

## 目标

本文定义 Phase 28 `CEK-TA-127` 的 FastAPI 服务位置、依赖策略、启动边界和 resolver 路径策略。

该文档承接 `docs/contracts/knowledge_tree_reading_api_contract.md`，为后续 `CEK-TA-128` 至 `CEK-TA-132` 的 Vue3、FastAPI adapter、契约测试和 Playwright 验收提供运行时约束。

## 结论

```text
FastAPI 服务目录：codex-expert-kit/api/
服务性质：CEK-TA 审计 UI 的只读本地数据服务
默认数据源：codex-expert-kit/rag/indexes/knowledge_items.json
路径解析：必须使用 codex-expert-kit/core/path_resolver.py
依赖策略：先文档锁定，后续实现任务中再新增 FastAPI / uvicorn / pytest 依赖
Vue3 策略：默认先 healthcheck，API 可用则使用 FastAPI adapter，不可用则 fixture fallback
MCP 关系：FastAPI 不替代 MCP，外部项目继续优先通过 MCP 查询知识库
```

## 为什么放在 codex-expert-kit/api/

`codex-expert-kit/api/` 更符合本项目作为支持层能力包的定位。

```text
1. 与 core、mcp、rag、templates 并列，表示它是 CEK-TA 能力包的一部分。
2. 后续外部项目把 codex-expert-kit 作为 submodule 或能力包复用时，可以一起携带 API runtime。
3. 避免根目录 api/ 被误解为单一业务应用后端。
4. 可以直接复用 codex-expert-kit/core/path_resolver.py。
5. 便于后续把 MCP、RAG index、Vue3 审计 UI 的契约统一归档。
```

## 目录契约

后续实现阶段建议目录：

```text
codex-expert-kit/api/
  __init__.py
  main.py
  config.py
  schemas.py
  errors.py
  services/
    __init__.py
    knowledge_index_loader.py
    knowledge_tree_service.py
    audit_summary_service.py
  routers/
    __init__.py
    health.py
    knowledge_tree.py
    knowledge_items.py
  tests/
    test_health_contract.py
    test_knowledge_tree_contract.py
    test_read_only_boundary.py
```

职责边界：

```text
main.py: FastAPI app 创建、router 注册、CORS 本地开发配置。
config.py: 环境变量读取、默认端口、索引路径解析配置。
schemas.py: Pydantic 输入输出 schema。
errors.py: 统一错误码和 envelope。
knowledge_index_loader.py: 只读加载 knowledge_items.json。
knowledge_tree_service.py: 节点、alias、children、knowledge 分页聚合。
audit_summary_service.py: 右侧审计摘要聚合。
routers/*: API endpoint，不直接读写文件。
tests/*: contract tests 和只读边界测试。
```

## 依赖策略

当前 `CEK-TA-127` 不安装依赖、不新增后端代码。

后续实现阶段可新增最小依赖：

```text
fastapi
uvicorn
pydantic
pytest
httpx
```

依赖落点待 `CEK-TA-132` 或实现任务确认：

```text
方案 A：codex-expert-kit/api/requirements.txt
方案 B：codex-expert-kit/pyproject.toml
方案 C：根目录 requirements-dev.txt 增加 api extra
```

当前推荐：

```text
codex-expert-kit/api/requirements.txt
```

原因：

```text
1. API runtime 是可选能力，不强迫 MCP 使用者安装 FastAPI。
2. 与现有文件化项目结构兼容。
3. 后续可在外部项目接入指南中说明按需安装。
```

## 启动策略

后续实现阶段建议启动命令：

```powershell
$env:CEK_TA_ROOT="E:\collector\rag"
python -m uvicorn codex_expert_kit_api.main:app --host 127.0.0.1 --port 8787
```

注意：由于当前目录名是 `codex-expert-kit`，Python import 不能直接使用连字符包名。实现时需要二选一：

```text
方案 A：在 codex-expert-kit/api/ 内提供可执行脚本，脚本用文件路径加载 main.py。
方案 B：创建合法 Python 包名 codex_expert_kit_api/，内部通过 resolver 访问 codex-expert-kit。
```

当前推荐：

```text
方案 B：创建 codex_expert_kit_api/ 作为 Python import 包。
```

原因：

```text
1. uvicorn 需要合法 import path。
2. 避免在运行时动态 import 带连字符目录。
3. 仍然可以把包目录放在 codex-expert-kit/api/codex_expert_kit_api/ 下。
```

推荐实现结构修订为：

```text
codex-expert-kit/api/
  requirements.txt
  codex_expert_kit_api/
    __init__.py
    main.py
    config.py
    schemas.py
    errors.py
    services/
    routers/
  tests/
```

启动命令：

```powershell
cd codex-expert-kit\api
$env:CEK_TA_ROOT="E:\collector\rag"
python -m uvicorn codex_expert_kit_api.main:app --host 127.0.0.1 --port 8787
```

文档中的本机路径只作为示例，运行时必须允许用任意 `CEK_TA_ROOT` 替换。

## 端口策略

```text
默认 API 端口：8787
默认 Host：127.0.0.1
用途：本地 Vue3 审计 UI 调用
禁止：默认暴露到 0.0.0.0
```

原因：

```text
1. 避免占用 Vue3 常见端口 5173/5174。
2. API 是本地审计服务，不需要默认对公网开放。
3. 与用户此前“不要搞错端口、不要误删其他进程”的要求一致。
```

## 环境变量

| 变量 | 默认值 | 用途 |
| --- | --- | --- |
| `CEK_TA_ROOT` | resolver 自动向上查找 | 指定 CEK-TA 根目录 |
| `CEK_TA_KNOWLEDGE_ITEMS_PATH` | `codex-expert-kit/rag/indexes/knowledge_items.json` | 覆盖正式知识索引路径 |
| `CEK_TA_API_HOST` | `127.0.0.1` | API host |
| `CEK_TA_API_PORT` | `8787` | API port |
| `CEK_TA_API_READ_ONLY` | `true` | 只读保护开关，必须默认为 true |

硬规则：

```text
1. CEK_TA_API_READ_ONLY 不得默认为 false。
2. 如果 READ_ONLY=false，服务也不得自动开放写接口；写能力必须另开 Phase。
3. CEK_TA_ROOT 无效时必须返回 INDEX_NOT_FOUND 或 SERVICE_DEGRADED，不得猜测路径。
```

## Resolver 使用策略

后续 Python 服务必须这样定位数据：

```text
1. import 或动态加载 codex-expert-kit/core/path_resolver.py。
2. 优先读取 CEK_TA_KNOWLEDGE_ITEMS_PATH。
3. 未配置时调用 resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json")。
4. 所有测试使用临时 CEK_TA_ROOT 或临时 CEK_TA_KNOWLEDGE_ITEMS_PATH。
5. 禁止使用 Path.cwd() 作为默认数据根。
```

## Vue3 接入策略

```text
1. Vue3 启动 KnowledgeTreeView 时先请求 GET /api/health。
2. health 成功且 read_only=true 时启用 FastAPI adapter。
3. health 失败时启用 fixture fallback。
4. fallback 状态必须在页面显示为 degraded fixture fallback。
5. FastAPI base URL 由 Vite env 控制，例如 VITE_CEK_TA_API_BASE_URL=http://127.0.0.1:8787。
6. Vue3 不直接假设 API 端口，避免端口冲突。
```

## 与 MCP 的关系

```text
1. MCP 仍然是外部项目调用 CEK-TA 知识库的默认入口。
2. FastAPI 只服务 Vue3 审计 UI。
3. FastAPI 不修改 MCP tool 参数、权限、返回结构。
4. FastAPI 可以复用 MCP/RAG 的知识索引，但不能绕过知识治理规则。
5. 如果 API 与 MCP 检索语义冲突，以 MCP 和 RAG governance 文档为准。
```

## 只读边界

FastAPI 实现时不得出现以下 endpoint：

```text
POST /api/knowledge-items
PUT /api/knowledge-items/{id}
PATCH /api/knowledge-items/{id}
DELETE /api/knowledge-items/{id}
POST /api/knowledge-tree/nodes/{node_id}/approve
POST /api/contributions
POST /api/trading/*
```

只允许：

```text
GET /api/health
GET /api/knowledge-tree/roots
GET /api/knowledge-tree/nodes/{node_id}
GET /api/knowledge-tree/nodes/{node_id}/children
GET /api/knowledge-tree/nodes/{node_id}/knowledge
GET /api/knowledge-items/{knowledge_id}
GET /api/knowledge-tree/nodes/{node_id}/audit-summary
```

## 测试策略

后续实现阶段至少包含：

```text
1. pytest codex-expert-kit/api/tests
2. /api/health 返回 read_only=true。
3. 未配置索引路径时通过 resolver 读取默认 knowledge_items.json。
4. 配置 CEK_TA_KNOWLEDGE_ITEMS_PATH 时读取覆盖路径。
5. page_size 超过 100 返回 INVALID_QUERY。
6. 未知 node_id 返回 NODE_NOT_FOUND。
7. 未知 knowledge_id 返回 ITEM_NOT_FOUND。
8. 扫描 routes，确认不存在 POST/PUT/PATCH/DELETE 写接口。
```

## 风险与回滚

```text
1. FastAPI 是新增后端运行面；若依赖安装或运行不稳定，Vue3 必须保留 fixture fallback。
2. 目录名 codex-expert-kit 带连字符，不能直接作为 Python 包 import；实现时使用 codex_expert_kit_api 子包解决。
3. 若端口 8787 被占用，不杀进程，改用 CEK_TA_API_PORT 指定新端口。
4. 若 API 数据映射不足，不修改正式知识 schema，先在 service mapper 中补默认值。
5. 若 API 被误用于外部项目调用，外部接入指南必须继续推荐 MCP。
```

## CEK-TA-127 DoD

```text
1. 本文档存在。
2. Phase 28 任务卡 CEK-TA-127 标记为 done。
3. docs/index_tasks.md 中 CEK-TA-127 标记为 done。
4. 文档明确服务目录、import 包策略、依赖策略、端口策略、环境变量、resolver 策略。
5. 文档明确 FastAPI 与 MCP、Vue3、fixture fallback 的边界。
6. 未安装依赖，未新增后端代码。
7. 中文文档 UTF-8 读取正常。
```
