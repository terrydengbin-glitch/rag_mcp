# Phase 50 Vue3 大 Fixture 拆包与懒加载验收报告

## 结论

Phase 50 已完成。Vue3 审计工作台不再由 `auditStore` 直接 import 候选、正式知识和知识树的大型 TS fixture，而是通过静态 JSON 数据 client 异步加载。

本次没有改变知识治理状态，没有把 reviewed 升级为 approved，没有启用 default guidance 或 hard gate，也没有改变 MCP 权限。

## 交付物

```text
docs/contracts/phase50_vue3_data_loading_contract.md
ui/src/services/knowledgeDataClient.ts
ui/public/data/phase23Candidates.json
ui/public/data/formalKnowledgeItems.json
ui/public/data/knowledgeTreeNodes.json
ui/tests/e2e/fixture-lazy-loading.spec.ts
docs/reports/phase50_vue3_lazy_loading_validation_report.json
```

## 实现摘要

```text
1. 三个生成脚本继续保留原子写入，并额外输出 phase50.static_fixture.v1 JSON envelope。
2. Vue3 新增 knowledgeDataClient，统一读取 /data/*.json。
3. auditStore 改为异步加载静态 JSON，并提供 dataState。
4. 候选页、知识树页、SearchLab 页增加中文加载/错误/成功状态条。
5. Playwright 增加静态 JSON 请求、刷新不白屏、分页和详情展示验收。
```

## 首包体积结果

```text
Phase 49 主 JS 基线：约 7,299 KB
Phase 50 主 JS：约 232 KB
gzip 后：约 73 KB
```

大型数据已经移动到静态 JSON：

```text
phase23Candidates.json：483 条，约 5.9 MB
formalKnowledgeItems.json：479 条，约 3.3 MB
knowledgeTreeNodes.json：121 个节点，约 0.1 MB
```

## 验收

```text
python -m py_compile ...                       pass
JSON envelope validation                       pass
npm --prefix ui run build                      pass
npm --prefix ui run test:e2e                   26 passed
python codex-expert-kit/rag/scripts/validate_no_mojibake.py  pass
```

## 边界

```text
1. 不引入数据库。
2. 不引入 FastAPI 新接口。
3. 不改变候选、reviewed、approved 状态语义。
4. 不改变 MCP tool 权限。
5. SearchLab 小型 runtimeSearchData 暂不拆分。
```

## 后续建议

```text
1. 知识量继续增长后，可把 phase23Candidates.json 和 formalKnowledgeItems.json 再拆成 index + page/detail JSON。
2. 如果部署到普通静态服务器，仍需确认 SPA fallback 或 hash router 策略。
3. 后续可补前端所有历史英文筛选 aria-label 的中文化清理任务。
```
