# LLM Training Domain Rules

Use this domain when curating datasets, writing dataset cards, planning SFT, designing evals, analyzing regressions, or deciding whether a CEK-TA capability belongs in RAG, Skill, SFT, preference data, or eval.

## Decision Boundary

```text
RAG:
  current facts, source-backed knowledge, exchange rules, model/API behavior, project facts

Skill:
  stable workflow Codex should execute step by step

SFT:
  stable behavior or output format the model repeatedly fails to follow

Preference optimization:
  judgment where better/worse outputs are clear and reviewed

Eval:
  proof that a capability improved or did not regress
```

## Hard Rules

```text
1. Do not train on raw private trades.
2. Do not train on secrets, account data, or project-private config.
3. Do not train latest market facts or time-sensitive exchange/API rules into weights.
4. Every sample needs source_ref, sanitization_status, label_quality, split, and review_status.
5. Train/eval leakage blocks release.
6. No model update is useful unless an eval report shows improvement without unacceptable regressions.
```

## Output Requirements

```text
dataset_card
eval_report
source mix
sanitization status
label quality
leakage check
target capability
release decision
open risks
```
