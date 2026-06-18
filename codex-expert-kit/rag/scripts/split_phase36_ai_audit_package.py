"""Split the Phase 36 AI Engineering audit package into smaller batches."""

from __future__ import annotations

import json
import sys
from pathlib import Path


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


SOURCE_PACKAGE = resolve_repo_path(
    "docs", "audit", "phase36_ai_engineering_candidate_audit_package_20260609.json", start_file=__file__
)
OUTPUT_DIR = resolve_repo_path("docs", "audit", "phase36_ai_engineering_batches", start_file=__file__)
MANIFEST_PATH = OUTPUT_DIR / "phase36_ai_engineering_audit_batches_manifest.json"
BATCH_COUNT = 10


def chunk_sizes(total: int, batch_count: int) -> list[int]:
    base = total // batch_count
    remainder = total % batch_count
    return [base + (1 if idx < remainder else 0) for idx in range(batch_count)]


def main() -> int:
    package = json.loads(SOURCE_PACKAGE.read_text(encoding="utf-8-sig"))
    candidates = package.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise ValueError("source package must contain non-empty candidates list")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sizes = chunk_sizes(len(candidates), BATCH_COUNT)
    offset = 0
    manifest_batches = []

    for index, size in enumerate(sizes, start=1):
        batch_candidates = candidates[offset : offset + size]
        offset += size
        batch_id = f"phase36_ai_engineering_candidate_audit_batch_{index:02d}_of_{BATCH_COUNT}_20260609"
        batch_path = OUTPUT_DIR / f"{batch_id}.json"
        batch_package = {
            **{k: v for k, v in package.items() if k != "candidates"},
            "package_id": batch_id,
            "package_type": "candidate_ai_audit_package_batch",
            "source_package_id": package.get("package_id"),
            "batch_index": index,
            "batch_count": BATCH_COUNT,
            "candidate_count": len(batch_candidates),
            "candidate_range": {
                "start_index_1_based": sum(sizes[: index - 1]) + 1,
                "end_index_1_based": sum(sizes[:index]),
            },
            "batch_audit_instruction": {
                "说明": "本文件是 Phase 36 总审计包的一个分批文件。请只审计本批 candidates，并按 required_output_schema 输出 JSON 审计结果。",
                "输出要求": [
                    "audit_result_id 必须包含 batch 编号，方便回写。",
                    "source_package_id 使用本 batch 的 package_id。",
                    "每个 candidate_id 必须输出一条 decision。",
                    "decision 只能是 accepted_for_draft、needs_more_evidence 或 rejected。",
                    "accepted_for_draft 不等于 approved，只表示可交给 CEK-TA 转 draft/reviewed。",
                ],
            },
            "candidates": batch_candidates,
        }
        batch_path.write_text(json.dumps(batch_package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest_batches.append(
            {
                "batch_id": batch_id,
                "path": batch_path.as_posix(),
                "candidate_count": len(batch_candidates),
                "candidate_ids": [item.get("candidate_id") for item in batch_candidates],
            }
        )

    manifest = {
        "manifest_id": "phase36_ai_engineering_audit_batches_manifest_20260609",
        "source_package_id": package.get("package_id"),
        "batch_count": BATCH_COUNT,
        "candidate_count": len(candidates),
        "generated_at": package.get("generated_at"),
        "purpose": "把 113 条 Phase 36 AI Engineering 候选知识拆成 10 份小审计包，降低单次审计负担。",
        "return_instruction": "审计完成后，把 10 份审计结果 JSON 放回 docs/audit/，CEK-TA 将按 candidate_id 和 source_package_id 回写优化。",
        "batches": manifest_batches,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "source_package_id": package.get("package_id"),
                "candidate_count": len(candidates),
                "batch_count": BATCH_COUNT,
                "batch_sizes": sizes,
                "output_dir": OUTPUT_DIR.as_posix(),
                "manifest": MANIFEST_PATH.as_posix(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
