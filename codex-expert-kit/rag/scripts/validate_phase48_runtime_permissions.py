"""Validate Phase 48 reviewed/caveat_only runtime permission boundaries."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


INDEX_PATH = resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase48_runtime_permission_validation_report.json", start_file=__file__)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def main() -> int:
    payload = json.loads(INDEX_PATH.read_text(encoding="utf-8-sig"))
    items = payload.get("items", payload if isinstance(payload, list) else [])
    if not isinstance(items, list):
        raise ValueError("knowledge_items.json must be a list or {items: [...]} object.")

    unsafe: list[dict[str, Any]] = []
    reviewed = 0
    approved = 0
    for item in items:
        knowledge_id = str(item.get("knowledge_id", ""))
        review_status = deep_get(item, ("review", "review_status"), "")
        if review_status == "approved":
            approved += 1
        if review_status != "reviewed":
            continue
        reviewed += 1
        bad_fields = []
        if deep_get(item, ("review", "approved_allowed")) is True:
            bad_fields.append("review.approved_allowed")
        if deep_get(item, ("review", "default_guidance_allowed")) is True:
            bad_fields.append("review.default_guidance_allowed")
        if deep_get(item, ("review", "hard_gate_allowed")) is True:
            bad_fields.append("review.hard_gate_allowed")
        if deep_get(item, ("machine_gate", "default_guidance")) != "caveat_only":
            bad_fields.append("machine_gate.default_guidance")
        if bad_fields:
            unsafe.append({"knowledge_id": knowledge_id, "bad_fields": bad_fields})

    report = {
        "report_id": "phase48_runtime_permission_validation",
        "generated_at": utc_now(),
        "task_id": "CEK-TA-492",
        "input_file": str(INDEX_PATH),
        "summary": {
            "item_count": len(items),
            "reviewed_count": reviewed,
            "approved_count": approved,
            "unsafe_reviewed_count": len(unsafe),
        },
        "checks": {"unsafe_reviewed_items": unsafe},
        "status": "pass" if not unsafe else "fail",
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"] | {"status": report["status"]}, ensure_ascii=False, indent=2))
    return 0 if not unsafe else 1


if __name__ == "__main__":
    raise SystemExit(main())
