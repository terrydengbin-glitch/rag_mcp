# LLM Training Domain

This domain contains reusable rules for CEK-TA LLM data curation, SFT planning, preference data, evaluation design, regression gates, and training release decisions.

Use RAG for current facts and source-backed knowledge retrieval. Use SFT when Codex fails to follow stable workflows or output contracts. Use preference optimization only when preferred judgment is well-defined. Use evals to prove whether a capability improved.

Do not fine-tune latest market facts, current exchange rules, secrets, private prompts, raw private trades, or current project configuration.
