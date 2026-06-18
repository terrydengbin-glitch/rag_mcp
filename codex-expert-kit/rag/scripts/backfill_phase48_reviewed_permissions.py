"""Backfill explicit reviewed permission fields without upgrading knowledge."""

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


KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase48_reviewed_schema_backfill_report.json", start_file=__file__)

PERMISSION_FIELDS = ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return payload


def is_reviewed_caveat_only(item: dict[str, Any]) -> bool:
    review = item.get("review") if isinstance(item.get("review"), dict) else {}
    machine_gate = item.get("machine_gate") if isinstance(item.get("machine_gate"), dict) else {}
    return review.get("review_status") == "reviewed" and machine_gate.get("default_guidance") == "caveat_only"


def main() -> int:
    changed: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    unsafe: list[dict[str, Any]] = []
    scanned = 0
    reviewed_caveat_only = 0

    for path in sorted(KNOWLEDGE_ROOT.glob("**/*.json")):
        scanned += 1
        item = load_json(path)
        knowledge_id = str(item.get("knowledge_id", path.stem))
        review = item.get("review")
        if not isinstance(review, dict):
            skipped.append({"knowledge_id": knowledge_id, "path": str(path), "reason": "missing_review_object"})
            continue
        if not is_reviewed_caveat_only(item):
            skipped.append(
                {
                    "knowledge_id": knowledge_id,
                    "path": str(path),
                    "reason": "not_reviewed_caveat_only",
                    "review_status": review.get("review_status"),
                    "machine_gate": (item.get("machine_gate") or {}).get("default_guidance")
                    if isinstance(item.get("machine_gate"), dict)
                    else None,
                }
            )
            continue

        reviewed_caveat_only += 1
        true_fields = [field for field in PERMISSION_FIELDS if review.get(field) is True]
        if true_fields:
            unsafe.append({"knowledge_id": knowledge_id, "path": str(path), "true_fields": true_fields})
            continue

        missing_fields = [field for field in PERMISSION_FIELDS if field not in review]
        if not missing_fields:
            continue

        for field in missing_fields:
            review[field] = False
        path.write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed.append({"knowledge_id": knowledge_id, "path": str(path), "backfilled_fields": missing_fields})

    report = {
        "report_id": "phase48_reviewed_schema_backfill_report",
        "generated_at": utc_now(),
        "task_id": "CEK-TA-491",
        "scope": "Only review permission fields for reviewed/caveat_only formal knowledge.",
        "summary": {
            "scanned_file_count": scanned,
            "reviewed_caveat_only_count": reviewed_caveat_only,
            "changed_file_count": len(changed),
            "unsafe_file_count": len(unsafe),
            "skipped_file_count": len(skipped),
        },
        "checks": {
            "changed": changed,
            "unsafe": unsafe,
            "skipped_sample": skipped[:200],
        },
        "boundary": {
            "knowledge_claim_changed": False,
            "source_evidence_changed": False,
            "review_status_changed": False,
            "approved_or_default_or_hard_gate_enabled": False,
        },
        "status": "pass" if not unsafe else "fail",
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"] | {"status": report["status"]}, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
