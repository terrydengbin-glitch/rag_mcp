# Phase 38 G04-R1 上下文预算补证采集记录

## 目标

为 G04-R1 `context_budget_field_trimming` 补充更直接的上下文预算、字段白名单、top-k、token budget 和显式展开策略证据，并导出三审包。该补证不代表 reviewed、approved 或 default guidance。

## 补证后 claim

交易 scoring/gating 的 RAG 知识包必须按字段白名单、top-k 和 token_budget 裁剪上下文；默认只返回最小必要字段，详细审计内容必须显式请求。

## 补充来源

- `src_langchain_contextual_compression`：Improving Document Retrieval with Contextual Compression
  - URL：https://www.langchain.com/blog/improving-document-retrieval-with-contextual-compression
  - 用途：LangChain contextual compression describes compressing retrieved documents using the query context so that only relevant information is returned, including shrinking individual documents and filtering documents wholesale.
- `src_llamaindex_response_modes_compact`：Response Modes - LlamaIndex
  - URL：https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/response_modes/
  - 用途：LlamaIndex response modes document refine and compact strategies for processing retrieved chunks, including compacting chunks to fit prompt size before refinement.
- `src_llamaindex_compact_and_refine`：Compact and refine - LlamaIndex
  - URL：https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/compact_and_refine/
  - 用途：LlamaIndex compact/refine documentation supports combining text chunks into larger consolidated chunks that fit the context window, then refining across them.
- `src_openai_prompt_engineering`：Prompt engineering - OpenAI API
  - URL：https://developers.openai.com/api/docs/guides/prompt-engineering
  - 用途：OpenAI prompt engineering guidance supports providing relevant reference text, splitting complex tasks, and using tools systematically instead of overloading prompts with unrelated context.
- `src_anthropic_context_engineering_agents`：Effective context engineering for AI agents
  - URL：https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  - 用途：Anthropic context engineering discusses curating and managing context as a finite resource for AI agents.

## 三审边界

```text
1. 只审 G04-R1 是否可进入 formal draft queue。
2. 不允许直接 reviewed、approved、default guidance 或 hard gate。
3. G04-R1 只治理 CEK-TA RAG 知识包上下文预算，不沉淀交易规则本体。
4. 字段白名单、top_k、token_budget 和 detail_expansion_policy 是 CEK-TA 内部契约字段。
```
