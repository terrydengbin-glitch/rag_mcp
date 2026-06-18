# Phase 0 任务卡：项目管理与规范入口

## 基本信息

| 字段 | 内容 |
| --- | --- |
| Phase | Phase 0 |
| 名称 | 项目管理与规范入口 |
| 任务 ID | CEK-TA-000 |
| 优先级 | P0 |
| 当前状态 | done |
| 主交付物 | `docs/index_tasks.md` |
| 辅助交付物 | `AGENTS.md`、`docs/tasks/README.md`、`docs/tasks/phase0_project_management.md`、`.agents/skills/cek-ta-development-workflow/SKILL.md` |
| 目标读者 | Codex、项目维护者、接入 CEK-TA 的其他项目 |

## Phase 目标

建立 CEK-TA 的项目管理入口，使后续所有 Phase 都有统一的任务索引、状态定义、优先级、依赖关系、交付物路径、验收规则和任务卡目录。

Phase 0 不实现知识库、MCP、Skill、Vue3 UI 或交易接口本身，它只负责建立项目治理契约。

## 背景与问题

CEK-TA 是一个支持层项目，后续会同时包含：

```text
1. 专业知识库
2. 知识采集与冲突审计规则
3. Codex Skills
4. MCP/RAG 检索层
5. 交易研发统一接口
6. Vue3 知识审计界面
7. 其他项目接入与知识倒灌机制
```

如果没有统一任务索引，后续会出现：

```text
任务散落在多个文档里
Phase 边界不清楚
P0/P1/P2 优先级混乱
交付物路径不一致
完成状态无法追踪
其他项目不知道如何接入或反哺
```

Phase 0 的职责是先把管理骨架立住。

## 上游输入

| 输入 | 来源 | 用途 |
| --- | --- | --- |
| 总体方案 | `docs/需求框架.md` | 提供愿景、架构、Phase 方向 |
| 任务需求 | `docs/任务需求清单.md` | 提供任务 ID、优先级、交付物和验收标准 |
| 支持层定位 | `docs/需求框架.md`、`docs/知识库采集与审计规范.md` | 明确本项目不是业务项目，而是专业知识支持层 |
| Vue3 审计需求 | `docs/Vue3知识审计界面需求.md` | 确保任务索引覆盖 UI 工作台 |
| 外部项目接入需求 | `docs/其他项目接入指南.md` | 确保任务索引覆盖调用方 |
| 知识倒灌需求 | `docs/知识倒灌与反哺规范.md` | 确保任务索引覆盖反哺流 |

## 下游输出

| 输出 | 消费方 | 用途 |
| --- | --- | --- |
| `docs/index_tasks.md` | 所有后续 Phase | 项目总索引、任务状态、依赖和验收入口 |
| `docs/tasks/README.md` | 任务卡维护者 | 管理每个 Phase 的详细任务卡 |
| `docs/tasks/phase0_project_management.md` | Codex、维护者 | Phase 0 的详细执行与验收依据 |
| `AGENTS.md` | Codex | 项目级开发规范和持久规则 |
| `.agents/skills/cek-ta-development-workflow/SKILL.md` | Codex | 可复用开发流程 Skill |
| 状态定义 | 所有任务卡 | 统一使用 `todo/doing/blocked/review/done/deprecated` |
| 优先级定义 | 所有任务卡 | 统一使用 `P0/P1/P2` |

## 范围内

```text
1. 创建项目管理总入口。
2. 定义 Phase 总览。
3. 定义任务状态。
4. 定义优先级。
5. 定义每个任务的交付物路径。
6. 定义首轮 P0 执行顺序。
7. 创建任务卡目录。
8. 创建 Phase 0 任务卡。
9. 建立任务卡与 index_tasks.md 的引用关系。
10. 创建项目级 `AGENTS.md`。
11. 创建仓库级开发流程 Skill。
```

## 范围外

```text
1. 不创建 codex-expert-kit 实体目录。
2. 不实现 Skills。
3. 不实现 MCP server。
4. 不搭建 RAGFlow/Qdrant。
5. 不创建 Vue3 工程。
6. 不采集具体专业知识。
7. 不接入真实业务项目。
8. 不接受业务项目倒灌内容入库。
```

这些内容分别属于 Phase 1 到 Phase 9。

## 核心契约

### 1. 文档入口契约

项目根目录必须有 `README.md` 指向：

```text
docs/index_tasks.md
```

`docs/index_tasks.md` 必须作为项目管理总入口。

### 2. Phase 索引契约

`docs/index_tasks.md` 必须包含：

```text
Phase 编号
Phase 名称
Phase 目标
Phase 状态
任务 ID
任务优先级
任务状态
任务交付物
任务依赖
```

### 3. 任务卡目录契约

所有详细任务卡必须放在：

```text
docs/tasks/
```

禁止把详细任务卡散落在根目录或其他目录。

### 4. 任务 ID 契约

任务 ID 使用：

```text
CEK-TA-000
CEK-TA-001
...
```

新增任务不能复用已有 ID。废弃任务必须保留 ID，并标记 `deprecated`。

### 5. 状态契约

任务状态只能使用：

```text
todo
doing
blocked
review
done
deprecated
```

不能使用 `pending`、`finished`、`complete`、`wip` 等其他状态，以免后续自动化解析混乱。

### 6. 路径契约

所有交付物路径必须相对项目根目录书写。

正确示例：

```text
docs/index_tasks.md
codex-expert-kit/core/AGENTS.md
ui/src/views/KnowledgeList.vue
```

错误示例：

```text
E:\collector\rag\docs\index_tasks.md
./../somewhere/file.md
```

绝对路径只允许出现在外部项目接入示例中。

## 数据/文档结构契约

Phase 0 交付后的最小结构：

```text
rag/
├── README.md
└── docs/
    ├── index_tasks.md
    ├── 需求框架.md
    ├── 任务需求清单.md
    ├── 知识库采集与审计规范.md
    ├── Vue3知识审计界面需求.md
    ├── 其他项目接入指南.md
    ├── 知识倒灌与反哺规范.md
    └── tasks/
        ├── README.md
        └── phase0_project_management.md
├── AGENTS.md
└── .agents/
    └── skills/
        └── cek-ta-development-workflow/
            ├── SKILL.md
            └── agents/
                └── openai.yaml
```

## 实施步骤

1. 创建 `docs/tasks/` 目录。
2. 创建 `docs/tasks/README.md`，列出所有 Phase 的任务卡规划。
3. 创建 `docs/tasks/phase0_project_management.md`。
4. 在 `docs/index_tasks.md` 中补充任务卡目录入口。
5. 在 Phase 0 表格中补充 Phase 0 任务卡路径。
6. 检查根目录 `README.md` 是否仍指向 `docs/index_tasks.md`。
7. 检查 Markdown 相对链接是否可读。

## Definition of Done

Phase 0 只有同时满足以下条件，才能保持 `done` 状态：

```text
1. `docs/index_tasks.md` 存在。
2. `docs/tasks/README.md` 存在。
3. `docs/tasks/phase0_project_management.md` 存在。
4. `docs/index_tasks.md` 包含 Phase 0 到 Phase 9 的总览。
5. `docs/index_tasks.md` 包含 CEK-TA-000 任务。
6. CEK-TA-000 状态为 done。
7. Phase 0 任务卡写清楚上游、下游、契约、边界、DoD、测试与验收。
8. 根目录 `README.md` 可以引导用户进入 `docs/index_tasks.md`。
9. 所有 Phase 的详细任务卡后续都必须放入 `docs/tasks/`。
10. `AGENTS.md` 存在，并包含任务管理、上下游、契约、边界、DoD、测试和重大决策提问规则。
11. `.agents/skills/cek-ta-development-workflow/SKILL.md` 存在，并通过 Skill 校验。
12. `AGENTS.md` 包含 UTF-8 编码规范，防止中文文档乱码。
```

## 测试与验收

### 静态文件测试

运行以下检查：

```powershell
Test-Path .\docs\index_tasks.md
Test-Path .\docs\tasks\README.md
Test-Path .\docs\tasks\phase0_project_management.md
Test-Path .\AGENTS.md
Test-Path .\.agents\skills\cek-ta-development-workflow\SKILL.md
```

预期结果：

```text
True
True
True
True
True
```

### Skill 校验

运行：

```powershell
python C:\Users\dove\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\.agents\skills\cek-ta-development-workflow
```

预期结果：

```text
Skill is valid!
```

### 内容完整性测试

检查 `phase0_project_management.md` 是否包含关键章节：

```text
上游输入
下游输出
核心契约
范围内
范围外
Definition of Done
测试与验收
风险与回滚
```

检查 `AGENTS.md` 是否包含编码规则：

```text
UTF-8 编码规范
Get-Content -Encoding UTF8
encoding="utf-8"
```

### 索引引用测试

检查 `docs/index_tasks.md` 是否包含：

```text
docs/tasks/README.md
docs/tasks/phase0_project_management.md
CEK-TA-000
Phase 0
```

### 人工验收

人工打开以下文件：

```text
README.md
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase0_project_management.md
```

确认从根目录能一路找到 Phase 0 任务卡，并能理解后续 Phase 的任务卡应该放在哪里。

## 风险

| 风险 | 影响 | 缓解 |
| --- | --- | --- |
| 任务卡过度散乱 | 后续 Phase 难以追踪 | 强制所有任务卡放入 `docs/tasks/` |
| 状态字段不统一 | 无法自动化解析 | 只允许使用约定状态 |
| 交付物路径写成绝对路径 | 跨机器不可复用 | 项目内部路径全部使用相对路径 |
| Phase 0 混入实现任务 | 破坏阶段边界 | Phase 0 只做治理和索引 |

## 回滚方案

如果 Phase 0 任务卡结构不合适：

```text
1. 保留 `docs/index_tasks.md`。
2. 修改 `docs/tasks/README.md` 的命名规则。
3. 调整 `docs/tasks/phase0_project_management.md` 的章节结构。
4. 同步更新 `docs/index_tasks.md` 中的任务卡入口。
```

禁止直接删除 `CEK-TA-000`，因为它是后续任务依赖的根任务。

## 状态更新要求

完成本任务后必须同步更新：

```text
docs/index_tasks.md
docs/tasks/README.md
```

如果后续新增 Phase 任务卡，也必须同步更新：

```text
docs/tasks/README.md
docs/index_tasks.md
```

## 关联文档

| 文档 | 关系 |
| --- | --- |
| `../index_tasks.md` | 项目管理总索引 |
| `../任务需求清单.md` | 任务来源 |
| `../需求框架.md` | 总体愿景 |
| `../知识库采集与审计规范.md` | 后续知识治理依据 |
| `../其他项目接入指南.md` | 后续外部项目调用依据 |
| `../知识倒灌与反哺规范.md` | 后续外部项目反哺依据 |
