"""Build a compact Phase 54 precheck report from existing quality gates."""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


SCRIPT_DIR = resolve_repo_path("codex-expert-kit", "rag", "scripts", start_file=__file__)
SCHEMA_REPORT = resolve_repo_path("docs", "reports", "phase34_schema_v1_1_validation_report.json", start_file=__file__)
WORKFLOW_REPORT = resolve_repo_path("docs", "reports", "phase32_candidate_to_reviewed_quality_gate.json", start_file=__file__)
OUTPUT_PATH = resolve_repo_path("docs", "reports", "phase54_backfill_precheck_report.json", start_file=__file__)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def run_gate(script_name: str) -> int:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / script_name)],
        cwd=resolve_repo_path(start_file=__file__),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.returncode


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    return payload if isinstance(payload, dict) else {}


def schema_failure_reasons(report: dict[str, Any]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for entry in report.get("failures", []):
        if not isinstance(entry, str) or ": " not in entry:
            counter["unknown"] += 1
            continue
        counter[entry.rsplit(": ", 1)[-1]] += 1
    return dict(sorted(counter.items()))


def workflow_failure_reasons(report: dict[str, Any]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for entry in report.get("failures", []):
        if isinstance(entry, dict):
            counter[str(entry.get("reason", "unknown"))] += 1
    return dict(sorted(counter.items()))


def main() -> int:
    schema_exit = run_gate("validate_knowledge_item_schema_v1_1.py")
    workflow_exit = run_gate("validate_candidate_to_reviewed_workflow.py")
    schema_report = load_json(SCHEMA_REPORT)
    workflow_report = load_json(WORKFLOW_REPORT)

    report = {
        "report_id": "phase54_backfill_precheck_report",
        "generated_at": utc_now(),
        "task_id": "CEK-TA-528",
        "inputs": {
            "schema_report": SCHEMA_REPORT.relative_to(resolve_repo_path(start_file=__file__)).as_posix(),
            "workflow_report": WORKFLOW_REPORT.relative_to(resolve_repo_path(start_file=__file__)).as_posix(),
        },
        "gate_exit_codes": {
            "validate_knowledge_item_schema_v1_1": schema_exit,
            "validate_candidate_to_reviewed_workflow": workflow_exit,
        },
        "schema": {
            "gate_status": schema_report.get("gate_status"),
            "item_count": schema_report.get("item_count"),
            "failure_count": schema_report.get("failure_count"),
            "failure_reasons": schema_failure_reasons(schema_report),
        },
        "workflow": {
            "gate_status": workflow_report.get("gate_status"),
            "candidate_count": workflow_report.get("candidate_count"),
            "knowledge_count": workflow_report.get("knowledge_count"),
            "failure_count": workflow_report.get("failure_count"),
            "warning_count": workflow_report.get("warning_count"),
            "failure_reasons": workflow_failure_reasons(workflow_report),
        },
        "boundary": {
            "claim_content_change_allowed": False,
            "approved_upgrade_allowed": False,
            "default_guidance_enable_allowed": False,
            "hard_gate_enable_allowed": False,
        },
        "status": "needs_backfill"
        if schema_report.get("failure_count") or workflow_report.get("failure_count")
        else "pass",
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
