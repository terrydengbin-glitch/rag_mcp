from __future__ import annotations

import json
import re
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[3]

SCAN_PATHS = [
    ROOT / "codex-expert-kit" / "rag" / "candidates",
    ROOT / "codex-expert-kit" / "rag" / "knowledge",
    ROOT / "codex-expert-kit" / "rag" / "indexes",
    ROOT / "docs" / "audit",
    ROOT / "docs" / "reports",
    ROOT / "docs" / "research",
    ROOT / "ui" / "src" / "data",
]

TEXT_SUFFIXES = {".json", ".ts", ".md"}
BAD_CODEPOINT_MARKERS = {
    "replacement_character": chr(0xFFFD),
    "mojibake_c3": chr(0x00C3),
    "mojibake_c2": chr(0x00C2),
    "mojibake_kun": chr(0x951F),
}
QUESTION_PLACEHOLDER_RE = re.compile(r"\?{2,}")


def scan_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    findings: list[str] = []
    if QUESTION_PLACEHOLDER_RE.search(text):
        findings.append("consecutive_question_placeholder")
    for name, marker in BAD_CODEPOINT_MARKERS.items():
        if marker in text:
            findings.append(name)
    return findings


def main() -> int:
    failures = []
    scanned_count = 0
    for root in SCAN_PATHS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
                continue
            scanned_count += 1
            markers = scan_file(path)
            if markers:
                failures.append(
                    {
                        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                        "markers": sorted(set(markers)),
                    }
                )

    report = {
        "report_id": "cek_ta_no_mojibake_gate",
        "scanned_count": scanned_count,
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "policy": "Chinese/user-visible Markdown, JSON, TS fixtures must be UTF-8 and must not contain mojibake markers.",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
