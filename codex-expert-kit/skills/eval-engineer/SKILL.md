---
name: eval-engineer
description: Design and review CEK-TA evals for RAG, Skills, prompts, SFT candidates, trade-quality labels, task-card quality, source grounding, boundary preservation, safety, and regression gates.
---

# Eval Engineer

## Use When

Use this skill when creating or reviewing:

```text
eval reports
holdout sets
regression suites
RAG answer evals
Skill behavior evals
SFT candidate evals
trade-quality label evals
task-card quality evals
```

## Workflow

1. Define target capability and output contract.
2. Select eval set with normal, edge, bad-case, ambiguous, and safety cases.
3. Confirm eval set has no train leakage.
4. Define metrics and rubric.
5. Compare baseline vs candidate.
6. Inspect failure cases before trusting aggregate metrics.
7. Apply regression gates.
8. Write release decision in `eval_report.md`.

## Hard Rules

```text
No eval, no release.
Safety failures block release.
Leakage blocks release.
Aggregate pass rate cannot hide critical label failures.
Candidate must preserve CEK-TA boundaries and source grounding.
```

## Output

```json
{
  "eval_id": "",
  "target_capability": "",
  "metrics": {},
  "regressions": [],
  "safety_failures": [],
  "failure_cases": [],
  "release_decision": "pass | fail | needs_review",
  "required_followups": []
}
```
