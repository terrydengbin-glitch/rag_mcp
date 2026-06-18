# Phase 49: Vue3 前端白屏与 Dev Server 稳定性修复

## Phase 目标

定位并修复 Vue3 审计工作台刷新后白屏的问题，重点解决 Vite dev server 在大体量生成 fixture 重写期间缓存空模块或半写模块，导致浏览器刷新后 Vue 入口导入失败的问题。

本 Phase 不新增知识、不改变知识治理状态、不改变 Vue3 信息架构、不改变 MCP/API 权限。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-495 | P0 | done | 复现 Vue3 刷新白屏并记录根因 | `docs/reports/phase49_vue3_white_screen_root_cause_report.json` |
| CEK-TA-496 | P0 | done | 将 Vue3 大 fixture 生成改为原子写入 | `codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py`、`codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py`、`codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py` |
| CEK-TA-497 | P0 | done | 调整 Vite watcher 等待写入稳定，降低半写模块被缓存风险 | `ui/vite.config.ts` |
| CEK-TA-498 | P1 | done | 运行 build、fixture 生成、浏览器刷新验证 | `docs/reports/phase49_vue3_dev_server_stability_report.json` |

## 上游输入

```text
1. Phase 25 Vue3 Playwright 实机验收规则。
2. Phase 28 Vue3/FastAPI 只读与 fixture fallback 契约。
3. Phase 32 候选 fixture 生成脚本。
4. Phase 47/48 知识树和正式知识 fixture 重建流程。
5. 当前运行中的 Vite dev server。
```

## 下游输出

```text
1. Vue3 dev server 刷新白屏原因报告。
2. 原子写入后的大 fixture 生成脚本。
3. Vite watcher 写入稳定等待配置。
4. 前端 build 和关键路由刷新验证结果。
```

## 输入契约

前端生成 fixture 输入：

```text
codex-expert-kit/rag/candidates/**/*.json
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/knowledge_tree.md
```

前端运行输入：

```text
ui/src/data/phase23Candidates.ts
ui/src/data/formalKnowledgeItems.ts
ui/src/data/knowledgeTreeNodes.ts
```

## 输出契约

生成脚本必须保证：

```text
1. 先完整写入同目录临时文件。
2. 再使用原子 replace 覆盖目标文件。
3. 不让 Vite watcher 观察到空目标文件或半写目标文件。
4. 输出文件保持 UTF-8。
5. 不改变导出的变量名和前端类型契约。
```

Vite 配置必须保证：

```text
1. 继续使用本地开发服务器。
2. 通过 watcher awaitWriteFinish 降低大文件半写触发 HMR 的概率。
3. 不改变路由信息架构。
```

## 边界范围

范围内：

```text
1. 调查 Vue3 白屏原因。
2. 修复 fixture 生成写入方式。
3. 调整 Vite dev server watcher。
4. 验证关键页面刷新后不白屏。
```

范围外：

```text
1. 不新增专业知识。
2. 不修改候选/正式知识语义。
3. 不把 reviewed 升级为 approved。
4. 不启用 default guidance 或 hard gate。
5. 不改变 Vue3 页面信息架构。
6. 不引入数据库或新后端框架。
7. 不关闭其他项目端口或进程。
```

## 涉及组件

```text
codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py
codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py
codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py
ui/vite.config.ts
ui/src/data/*.ts
```

## 涉及数据结构

```text
IngestionCandidate
KnowledgeItem
KnowledgeTreeNode
```

## 涉及数据库/存储

不引入数据库。只涉及本地文件化 Vue3 fixture。

## 实施步骤

```text
1. 用 Playwright 访问当前 dev server，抓取 body、#app 和 pageerror。
2. 对比磁盘 fixture 与 dev server 实际返回模块。
3. 确认白屏根因为 Vite 缓存空 fixture 模块。
4. 将三个 fixture 生成脚本改为原子写入。
5. 增加 Vite watcher awaitWriteFinish。
6. 重新生成 fixture。
7. 执行 Vue3 build。
8. 启动或复用本项目 dev server，刷新关键路由验证无白屏。
9. 生成报告并更新索引。
```

## Definition of Done

```text
1. 任务卡存在并写入索引。
2. 根因报告存在。
3. 三个 fixture 生成脚本已改为原子写入。
4. Vite watcher 已配置写入稳定等待。
5. 重新生成 fixture 成功。
6. Vue3 build 通过。
7. 关键路由刷新后 body 非空，#app 已挂载。
8. 不误关其他项目端口。
9. UTF-8 乱码检查通过。
```

## 测试与验收

必须执行：

```text
python codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py
python codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py
python codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py
npm --prefix ui run build
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
```

实机验收：

```text
1. 访问 /、/dashboard、/knowledge-tree、/ingestion、/search-lab。
2. 刷新后 body 文本非空。
3. 刷新后 #app innerHTML 非空。
4. 控制台不再出现 “does not provide an export named phase23CandidateFixtureGeneratedAt”。
```

## 风险与回滚

风险：

```text
1. 当前已运行的 Vite 进程如果已经缓存空模块，需要重启本项目 dev server 才能恢复。
2. 首包仍然偏大，后续应另开 Phase 做数据懒加载或 API 分页。
3. createWebHistory 在非 SPA fallback 静态服务器上仍可能刷新 404，后续若部署到普通静态服务需另行处理。
```

回滚：

```text
1. 回滚三个生成脚本的 atomic write 修改。
2. 回滚 ui/vite.config.ts watcher 配置。
3. 重新运行 build 验证。
```

## 需要开发者确认的问题

```text
1. 是否后续把大 fixture 从首包拆出，改成 JSON/API 懒加载。
2. 是否后续把 router 从 createWebHistory 改为 createWebHashHistory，以兼容任意静态服务器刷新。
```
