# Phase 1 任务卡：Codex Expert Kit 骨架

## 基本信息

| 字段 | 内容 |
| --- | --- |
| Phase | Phase 1 |
| 名称 | Codex Expert Kit 骨架 |
| 当前状态 | done |
| 主目标 | 创建 `codex-expert-kit/` 基础骨架，让后续全局规则、领域包、Skills、模板、RAG、MCP 和安装脚本有稳定承载目录 |
| 上游 Phase | Phase 0 项目管理与规范入口 |
| 下游 Phase | Phase 2 RAGFlow、Phase 2.5 知识审计、Phase 3 MCP、Phase 4 交易接口、Phase 8/9 接入与倒灌 |

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-001 | P0 | done | 创建 `codex-expert-kit/` 基础目录 | `codex-expert-kit/` |
| CEK-TA-002 | P0 | done | 编写全局 `AGENTS.md` | `codex-expert-kit/core/AGENTS.md` |
| CEK-TA-003 | P0 | done | 编写项目接入模板 | `codex-expert-kit/templates/project_AGENTS.md` |
| CEK-TA-004 | P1 | done | 创建首批领域包 | `codex-expert-kit/domains/*` |
| CEK-TA-005 | P1 | done | 创建首批 Skill | `codex-expert-kit/skills/*/SKILL.md` |

## 上游输入

| 输入 | 来源 | 用途 |
| --- | --- | --- |
| Phase 0 管理契约 | `docs/tasks/phase0_project_management.md` | 约束任务状态、路径、DoD、测试 |
| 总体目录设计 | `docs/需求框架.md` 第 3、16 节 | 定义 CEK-TA 推荐目录结构 |
| 任务拆分 | `docs/index_tasks.md`、`docs/任务需求清单.md` | 定义 CEK-TA-001 到 CEK-TA-005 |
| 项目级开发规范 | `AGENTS.md` | 约束 UTF-8、任务卡、上下游、契约、DoD |

## 下游输出

| 输出 | 消费方 | 用途 |
| --- | --- | --- |
| `codex-expert-kit/core/` | CEK-TA-002 | 承载全局 Codex 规则 |
| `codex-expert-kit/domains/` | CEK-TA-004、后续领域包 | 承载 quant、kline、backtest 等领域 |
| `codex-expert-kit/skills/` | CEK-TA-005、后续 Skill | 承载可复用 Codex Skills |
| `codex-expert-kit/templates/` | CEK-TA-003、Phase 4/5/6/8/9 | 承载 AGENTS、接口、报告、倒灌任务卡模板 |
| `codex-expert-kit/rag/` | Phase 2、Phase 2.5、Phase 9 | 承载 KB 分区、metadata、schema、冲突规则 |
| `codex-expert-kit/mcp/` | Phase 3 | 承载 Knowledge MCP server 和工具 |
| `codex-expert-kit/install/` | 后续安装流程 | 承载安装、链接、bootstrap 脚本 |

## 输入契约

CEK-TA-001 不接受业务项目事实作为输入，只接受本项目文档中的目录规范。

输入约束：

```text
1. 目录结构以 `docs/需求框架.md` 第 16 节为准。
2. 路径必须相对项目根目录。
3. 不引入具体知识条目。
4. 不创建具体领域内容。
5. 不创建真实 MCP 实现。
```

CEK-TA-002 输入约束：

```text
1. 只使用 CEK-TA 总体框架和支持层定位。
2. 不写入当前仓库绝对路径。
3. 不写入任何业务项目私有字段或配置。
4. 不写入未经来源支撑的具体市场规则。
5. 输出必须可作为跨项目全局 Codex guidance 使用。
```

CEK-TA-003 输入约束：

```text
1. 模板只描述业务项目如何引用 CEK-TA。
2. 模板不绑定具体业务项目。
3. 模板必须要求项目事实留在业务项目。
4. 模板必须要求专业结论有来源、CEK-TA 知识或显式假设。
```

CEK-TA-004 输入约束：

```text
1. 只创建首批领域包骨架。
2. 不采集具体知识内容。
3. 每个领域包必须包含 AGENTS.domain.md。
4. 每个领域包必须包含 knowledge、templates、checklists 目录。
```

CEK-TA-005 输入约束：

```text
1. 只创建首批可用 Skill。
2. 每个 Skill 必须有有效 frontmatter。
3. 每个 Skill 必须包含 Workflow 和 Output。
4. Skill 不依赖外部服务或数据库。
```

## 输出契约

CEK-TA-001 完成后，项目根目录必须存在：

```text
codex-expert-kit/
├── core/
├── domains/
├── skills/
├── knowledge/
├── adapters/
├── templates/
├── rag/
├── mcp/
└── install/
```

为了保证空目录可见，每个一级目录允许放置 `.gitkeep`。

允许新增：

```text
codex-expert-kit/README.md
```

用于说明该目录是 CEK-TA 能力包根目录。

CEK-TA-002 完成后必须存在：

```text
codex-expert-kit/core/AGENTS.md
```

该文件必须覆盖：

```text
项目事实优先于通用知识
任务路由
交易系统改动契约
策略审计规则
回测/回放/模拟盘规则
实盘安全规则
知识来源与冲突规则
知识倒灌规则
RAG/SFT/DPO/Eval 分工
输出要求
UTF-8 要求
```

CEK-TA-003 完成后必须存在：

```text
codex-expert-kit/templates/project_AGENTS.md
```

CEK-TA-004 完成后必须存在：

```text
codex-expert-kit/domains/quant_trading/AGENTS.domain.md
codex-expert-kit/domains/kline_strategy/AGENTS.domain.md
codex-expert-kit/domains/backtest_replay_simulation/AGENTS.domain.md
```

每个领域包至少包含：

```text
AGENTS.domain.md
README.md
knowledge/
templates/
checklists/
```

CEK-TA-005 完成后必须存在：

```text
codex-expert-kit/skills/strategy-auditor/SKILL.md
codex-expert-kit/skills/kline-strategy-engineer/SKILL.md
codex-expert-kit/skills/backtest-reviewer/SKILL.md
```

## 边界

### CEK-TA-001 范围内

```text
1. 创建 `codex-expert-kit/` 根目录。
2. 创建一级能力目录。
3. 创建必要 `.gitkeep` 占位文件。
4. 创建简短 `codex-expert-kit/README.md`。
5. 更新 `docs/index_tasks.md`。
6. 更新 `docs/tasks/README.md`。
7. 更新本任务卡状态。
```

### CEK-TA-002 范围内

```text
1. 编写 `codex-expert-kit/core/AGENTS.md` 的全局指导。
2. 明确项目事实优先于通用知识。
3. 明确交易系统改动契约。
4. 明确策略、回测、实盘、知识、LLM/RAG 的核心规则。
5. 明确 UTF-8 要求。
6. 更新 `docs/index_tasks.md` 和本任务卡状态。
```

### CEK-TA-003 范围内

```text
1. 创建业务项目 `AGENTS.md` 模板。
2. 明确 CEK-TA 引用方式。
3. 明确 Project Type、Enabled Domains、Project Facts、Hard Rules。
4. 明确验证要求。
```

### CEK-TA-004 范围内

```text
1. 创建 quant_trading 领域包。
2. 创建 kline_strategy 领域包。
3. 创建 backtest_replay_simulation 领域包。
4. 每个领域包写入 AGENTS.domain.md。
5. 每个领域包创建 knowledge/templates/checklists 目录。
```

### CEK-TA-005 范围内

```text
1. 创建 strategy-auditor Skill。
2. 创建 kline-strategy-engineer Skill。
3. 创建 backtest-reviewer Skill。
4. 每个 Skill 写清 description、Workflow、Output。
5. 使用 skill validator 校验。
```

### Phase 1 当前范围外

```text
1. 不创建具体 domain pack。
2. 不创建具体 Skill。
3. 不实现 RAG 检索。
4. 不实现 MCP server。
5. 不创建 Vue3 UI。
6. 不采集任何专业知识。
7. 不把项目级开发规范 `AGENTS.md` 原样复制进 `core/AGENTS.md`。
8. 不写具体业务项目适配层。
```

## 涉及组件

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase1_expert_kit_skeleton.md
codex-expert-kit/
```

## 涉及数据结构

本任务只创建目录结构，不定义业务数据 schema。

## 涉及数据库/存储

本任务不引入数据库，不引入外部存储，不创建迁移。

## 实施步骤

1. 创建 Phase 1 任务卡。
2. 创建 `codex-expert-kit/` 根目录。
3. 创建一级目录：`core`、`domains`、`skills`、`knowledge`、`adapters`、`templates`、`rag`、`mcp`、`install`。
4. 为一级目录添加 `.gitkeep` 占位。
5. 创建 `codex-expert-kit/README.md`。
6. 更新 `docs/index_tasks.md`：Phase 1 状态和 CEK-TA-001 状态。
7. 更新 `docs/tasks/README.md`：Phase 1 任务卡状态。
8. 运行文件存在性检查和 UTF-8 检查。
9. 编写 `codex-expert-kit/core/AGENTS.md`。
10. 更新 CEK-TA-002 状态。
11. 创建 `codex-expert-kit/templates/project_AGENTS.md`。
12. 创建首批三个领域包。
13. 创建首批三个 Skill。
14. 运行 Skill 校验、文件存在性检查和 UTF-8 检查。
15. 更新 Phase 1 状态为 done。

## Definition of Done

CEK-TA-001 只有满足以下条件才能标记 `done`：

```text
1. `codex-expert-kit/` 存在。
2. 9 个一级目录全部存在。
3. 每个一级目录有 `.gitkeep` 或实际交付物。
4. `codex-expert-kit/README.md` 存在。
5. `docs/tasks/phase1_expert_kit_skeleton.md` 存在。
6. `docs/index_tasks.md` 中 CEK-TA-001 状态为 done。
7. `docs/tasks/README.md` 中 Phase 1 任务卡状态不是 todo。
8. 本任务卡中 CEK-TA-001 状态为 done。
9. 未越界创建 Phase 2/3/4/7 的实现内容。
10. 中文文档 UTF-8 读取无乱码。
```

CEK-TA-002 只有满足以下条件才能标记 `done`：

```text
1. `codex-expert-kit/core/AGENTS.md` 存在。
2. 文件是跨项目全局 guidance，不包含当前仓库绝对路径。
3. 文件明确项目事实优先于通用知识。
4. 文件包含交易系统改动契约。
5. 文件包含策略、回测、实盘、知识、LLM/RAG 的核心规则。
6. 文件包含 UTF-8 要求。
7. `docs/index_tasks.md` 中 CEK-TA-002 状态为 done。
8. 本任务卡中 CEK-TA-002 状态为 done。
```

CEK-TA-003 只有满足以下条件才能标记 `done`：

```text
1. `codex-expert-kit/templates/project_AGENTS.md` 存在。
2. 模板包含 CEK-TA Reference、Project Type、Enabled Domains、Project Facts、Hard Rules。
3. 模板要求项目事实留在业务项目。
4. 模板要求验证和来源约束。
```

CEK-TA-004 只有满足以下条件才能标记 `done`：

```text
1. 三个首批领域包目录存在。
2. 每个领域包包含 `AGENTS.domain.md`。
3. 每个领域包包含 `knowledge/`、`templates/`、`checklists/`。
4. 领域包不包含未经来源审计的具体专业知识。
```

CEK-TA-005 只有满足以下条件才能标记 `done`：

```text
1. 三个首批 Skill 目录存在。
2. 每个 Skill 包含 `SKILL.md`。
3. 每个 Skill frontmatter 有 name 和 description。
4. 每个 Skill 包含 Workflow 和 Output。
5. 三个 Skill 均通过 validator。
```

Phase 1 只有满足以下条件才能标记 `done`：

```text
1. CEK-TA-001 到 CEK-TA-005 均为 done。
2. `docs/index_tasks.md` 中 Phase 1 状态为 done。
3. `docs/tasks/README.md` 中 Phase 1 状态为 done。
4. 本任务卡当前状态为 done。
```

## 测试与验收

### 文件存在性测试

```powershell
Test-Path .\codex-expert-kit
Test-Path .\codex-expert-kit\core
Test-Path .\codex-expert-kit\domains
Test-Path .\codex-expert-kit\skills
Test-Path .\codex-expert-kit\knowledge
Test-Path .\codex-expert-kit\adapters
Test-Path .\codex-expert-kit\templates
Test-Path .\codex-expert-kit\rag
Test-Path .\codex-expert-kit\mcp
Test-Path .\codex-expert-kit\install
Test-Path .\codex-expert-kit\README.md
Test-Path .\codex-expert-kit\core\AGENTS.md
Test-Path .\codex-expert-kit\templates\project_AGENTS.md
Test-Path .\codex-expert-kit\domains\quant_trading\AGENTS.domain.md
Test-Path .\codex-expert-kit\domains\kline_strategy\AGENTS.domain.md
Test-Path .\codex-expert-kit\domains\backtest_replay_simulation\AGENTS.domain.md
Test-Path .\codex-expert-kit\skills\strategy-auditor\SKILL.md
Test-Path .\codex-expert-kit\skills\kline-strategy-engineer\SKILL.md
Test-Path .\codex-expert-kit\skills\backtest-reviewer\SKILL.md
```

预期全部为：

```text
True
```

### 索引一致性测试

检查：

```text
docs/index_tasks.md 包含 CEK-TA-001 和 done
docs/tasks/README.md 包含 phase1_expert_kit_skeleton.md
docs/tasks/phase1_expert_kit_skeleton.md 包含上下游、契约、边界、DoD、测试
```

### UTF-8 测试

使用：

```powershell
Get-Content -LiteralPath .\docs\tasks\phase1_expert_kit_skeleton.md -Encoding UTF8
Get-Content -LiteralPath .\codex-expert-kit\README.md -Encoding UTF8
Get-Content -LiteralPath .\codex-expert-kit\core\AGENTS.md -Encoding UTF8
Get-Content -LiteralPath .\codex-expert-kit\templates\project_AGENTS.md -Encoding UTF8
```

### Skill 校验

```powershell
python C:\Users\dove\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\codex-expert-kit\skills\strategy-auditor
python C:\Users\dove\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\codex-expert-kit\skills\kline-strategy-engineer
python C:\Users\dove\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\codex-expert-kit\skills\backtest-reviewer
```

确认中文显示正常，无乱码。

## 风险与回滚

| 风险 | 影响 | 缓解 |
| --- | --- | --- |
| 目录结构过早细化 | 把后续 Phase 的实现提前混入 | 本任务只创建一级目录和占位 |
| 空目录后续不可追踪 | 版本管理时目录丢失 | 使用 `.gitkeep` |
| 路径与文档不一致 | 后续任务找不到交付物 | 更新 `docs/index_tasks.md` 和任务卡目录 |

回滚方式：

```text
1. 删除本任务新增的空目录或占位文件。
2. 保留任务卡，并把 CEK-TA-001 状态改回 todo。
3. 同步回滚 `docs/index_tasks.md` 和 `docs/tasks/README.md` 状态。
```

## 需要开发者确认的问题

当前无阻塞问题。目录结构来自既有需求框架，不涉及新增数据库、后端框架、外部服务或不可逆迁移。

## 状态更新要求

完成 Phase 1 后必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase1_expert_kit_skeleton.md
```
