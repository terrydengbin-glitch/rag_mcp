# SearchLab MCP Runtime Quality Report

## Report Identity

```text
report_id: cek_ta_searchlab_mcp_runtime_quality_20260608
phase: Phase 20
tested_at: 2026-06-08
scope: SearchLab MCP 同构运行时、canonical filter、ranking quality、blocked result audit
```

## Completed Tasks

| Task | Result | Deliverable |
| --- | --- | --- |
| CEK-TA-080 | done | `docs/searchlab_mcp_runtime_contract.md` |
| CEK-TA-081 | done | `codex-expert-kit/mcp/common.py`、`codex-expert-kit/mcp/search_expert_knowledge.py`、`codex-expert-kit/mcp/tests/test_phase20_runtime_quality.py` |
| CEK-TA-082 | done | `codex-expert-kit/rag/eval_sets/runtime_ranking_eval_cases.json`、`docs/reports/runtime_ranking_quality_report.md` |
| CEK-TA-083 | done | `ui/src/data/runtimeSearchData.ts`、`ui/src/stores/auditStore.ts`、`ui/src/views/SearchLab.vue` |
| CEK-TA-084 | done | `ui/src/types.ts`、`ui/src/views/SearchLab.vue`、`ui/src/data/runtimeSearchData.ts` |
| CEK-TA-085 | done | `docs/reports/searchlab_mcp_runtime_quality_report.md` |

## Runtime Contract

SearchLab runtime 契约已经定义：

```text
request_id
query
task_type
top_k
filters.tree_node_id
filters.canonical_node_id
filters.tree_path_prefix
filters.canonical_tree_path_prefix
include.sources
include.conflicts
include.blocked
include.ranking_debug
```

MCP response 保持旧字段兼容，并新增：

```text
results[].canonical_node_id
results[].canonical_tree_path
results[].why_matched.reasons
blocked_results[]
blocked_results[].blocked_reason
blocked_results[].recommended_fix
```

## MCP Runtime Results

```text
pytest codex-expert-kit/mcp/tests
18 passed
```

新增覆盖：

```text
canonical_node_id 过滤
v1 alias 迁移期兼容
canonical_tree_path_prefix 过滤
blocked_results 返回阻断原因和修复建议
```

## Ranking Quality

```text
eval_case_count: 10
top_k: 5
target_in_top5_rate: 1.0
target_rank1_rate: 1.0
unsafe_default_guidance_rate: 0.0
```

排序修正：

```text
查询相关性优先于 source_quality high。
source_quality high 作为同分加权。
tokenizer 拆分下划线 ID。
item_text 纳入来源标题、证据摘要、procedure、examples、assumptions。
```

## SearchLab Runtime Display

SearchLab 已从 Phase 19 的 seed mock 展示升级为 Phase 20 MCP 同构 runtime fixture。

当前展示：

```text
request_id
runtime_status
query
task_type
tree_node_id
canonical_node_id
audit.blocked_count
warnings
matches
canonical_tree_path
score
why_matched.reasons
source_count
blocked_results
blocked_reason
recommended_fix
```

代表用例：

```text
phase20_runtime_ohlc_same_bar: 正常命中并展示 canonical path。
phase20_runtime_kill_switch_warning: time_sensitive live_trading warning。
phase20_runtime_unsourced_blocked: 无来源知识被阻断并展示 recommended_fix。
```

## Boundaries

```text
未引入数据库。
未引入后端框架。
未接入外部 RAGFlow 或向量数据库。
未改变 MCP tool 权限。
未新增写入型 MCP tool。
未联网采集新知识。
未采集行情、K线、订单流或账户数据。
Vue3 主信息架构未改变。
```

## Tests

```text
pytest codex-expert-kit/mcp/tests
18 passed

npm --prefix ui run build
pass

runtime_ranking_eval_cases.json
JSON parse passed
```

## Open Gaps

```text
1. SearchLab 仍使用 MCP 同构 runtime fixture，不直接调用 MCP server。
2. 尚未引入 HTTP bridge；如需要必须单独建 Phase 并确认后端边界。
3. 当前 ranking 是轻量词法增强，不是向量检索或 reranker。
4. 评测集当前只覆盖 10 条 seed 知识，后续规模化入库前需要扩展。
```

## DoD Checklist

```text
Phase 20 任务卡存在并已被索引: pass
SearchLab MCP runtime 契约文档存在: pass
MCP 支持 canonical_node_id / alias / tree_path 过滤: pass
10 条 seed ranking eval cases 存在: pass
目标知识 top_k=5 命中率有报告: pass
SearchLab 能展示 runtime 查询结果、来源、边界、阻断原因和 audit summary: pass
阻断无来源、冲突、过期、draft/rejected 的测试继续通过: pass
不改变 MCP 权限: pass
不引入数据库、后端框架或外部服务: pass
pytest 通过: pass
Vue3 build 通过: pass
中文文档 UTF-8 无乱码: pass
```
