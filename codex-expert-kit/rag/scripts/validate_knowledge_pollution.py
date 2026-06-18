"""Detect mock/demo/test pollution in the formal CEK-TA knowledge base."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase33_knowledge_pollution_scan_report.json", start_file=__file__)

POLLUTION_TERMS = {
    "mock",
    "demo",
    "fixture",
    "sample",
    "test-only",
    "placeholder",
    "fake",
    "synthetic",
    "playwright",
    "pytest",
}

INTERNAL_SOURCE_TYPES = {"internal_report", "task_card", "runbook", "code_doc"}
EXTERNAL_SOURCE_TYPES = {
    "official_doc",
    "paper",
    "academic_paper",
    "exchange_rule",
    "framework_doc",
    "book",
    "research_report",
    "professional_curriculum",
    "engineering_article",
    "standard_or_risk_framework",
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return payload


def text_blob(item: dict[str, Any]) -> str:
    chunks: list[str] = []
    for key in ("knowledge_id", "title"):
        value = item.get(key)
        if isinstance(value, str):
            chunks.append(value)
    content = item.get("content")
    if isinstance(content, dict):
        for key in ("statement", "rationale", "citation_notes"):
            value = content.get(key)
            if isinstance(value, str):
                chunks.append(value)
    for source in item.get("source_evidence", []):
        if isinstance(source, dict):
            chunks.extend(str(source.get(key, "")) for key in ("source_id", "source_title", "source_type", "publisher"))
    return " ".join(chunks).lower()


def source_types(item: dict[str, Any]) -> set[str]:
    return {
        str(source.get("source_type"))
        for source in item.get("source_evidence", [])
        if isinstance(source, dict) and source.get("source_type")
    }


def publishers(item: dict[str, Any]) -> set[str]:
    return {
        str(source.get("publisher"))
        for source in item.get("source_evidence", [])
        if isinstance(source, dict) and source.get("publisher")
    }


def has_external_source(item: dict[str, Any]) -> bool:
    return bool(source_types(item) & EXTERNAL_SOURCE_TYPES)


def is_project_governance(item: dict[str, Any]) -> bool:
    metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
    domain = str(metadata.get("domain", ""))
    return domain in {
        "knowledge_governance",
        "project_integration",
        "project_runbooks",
        "rag_engineering",
        "mcp_engineering",
        "llm_training",
    }


def is_professional_training_schema_usage(item: dict[str, Any], term: str) -> bool:
    """Allow ML/trading training schema terms with external evidence.

    The pollution gate uses "sample" to catch mock/demo/test artifacts entering
    formal knowledge. In AI Engineering, "training sample" and "trade sample
    schema" are domain terms, so they should not fail when the item has
    professional external sources and belongs to the LLM training domain.
    "synthetic" is also allowed only when used as a source_mode enum for
    training data provenance, not as a fake/mock source.
    """
    metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
    domain = str(metadata.get("domain", ""))
    if domain != "llm_training" or not has_external_source(item):
        return False
    blob = text_blob(item)
    if term == "sample":
        professional_phrases = (
            "training sample",
            "trade sample",
            "data sample",
            "trade data sample",
            "sample schema",
            "training_data.trade_sample_schema_required",
        )
        return "source_mode" in blob or any(phrase in blob for phrase in professional_phrases)
    if term == "synthetic":
        professional_phrases = (
            "source_mode",
            "synthetic",
            "trade data sample",
            "allowed_use",
            "prohibited_use",
        )
        return all(phrase in blob for phrase in ("source_mode", "synthetic")) or any(
            phrase in blob for phrase in professional_phrases
        )
    return False


def is_professional_ai_governance_usage(item: dict[str, Any], term: str) -> bool:
    """Allow AI governance terms that contain sample/sampling as method words."""
    metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
    domain = str(metadata.get("domain", ""))
    if domain != "ai_governance" or not has_external_source(item):
        return False
    blob = text_blob(item)
    if term == "sample":
        professional_phrases = (
            "tail sampling",
            "long_tail_feedback_sampling",
            "low-sample tail",
            "control samples",
            "random/stratified control samples",
            "sample coverage",
        )
        return any(phrase in blob for phrase in professional_phrases)
    return False


def is_professional_numeric_scoring_usage(item: dict[str, Any], term: str) -> bool:
    """Allow numeric scorer terms such as sample_weight/class_weight.

    These are ML API and modeling terms, not mock/demo/test fixture markers.
    They should pass only when the item is in the numeric scoring branch and
    has external evidence.
    """
    metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
    node_id = str(metadata.get("canonical_node_id") or metadata.get("tree_node_id") or "")
    if not node_id.startswith("kt.ai_engineering.numeric_scoring") or not has_external_source(item):
        return False
    blob = text_blob(item)
    if term == "sample":
        professional_phrases = (
            "sample_weight",
            "class_weight",
            "sample weight",
            "cost-sensitive",
            "false allow",
            "false block",
        )
        return any(phrase in blob for phrase in professional_phrases)
    return False


def is_professional_trading_research_usage(item: dict[str, Any], term: str) -> bool:
    """Allow sample/sample-size terms in trading research and backtest rules.

    In Trading Engineering, "sample", "out-of-sample", "sample coverage" and
    "sample size" are methodological terms. They are not mock/demo/test
    pollution when the item has professional external evidence and belongs to a
    trading research/backtest/quant branch.
    """
    metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
    domain = str(metadata.get("domain", ""))
    node_id = str(metadata.get("canonical_node_id") or metadata.get("tree_node_id") or "")
    if term != "sample" or not has_external_source(item):
        return False
    if not (
        domain in {"backtest", "quant_foundation", "trade_analysis", "strategy_engineering"}
        or node_id.startswith("kt.trading_engineering")
        or node_id.startswith("kt.quant_foundation")
        or node_id.startswith("kt.trade_analysis")
    ):
        return False
    blob = text_blob(item)
    professional_phrases = (
        "out-of-sample",
        "out of sample",
        "sample size",
        "sample-size",
        "sample coverage",
        "sample selection",
        "in-sample",
        "holdout sample",
        "validation sample",
        "sample period",
    )
    return any(phrase in blob for phrase in professional_phrases)


def pollution_term_present(blob: str, term: str) -> bool:
    """Match pollution terms as tokens, not substrings inside professional words."""
    escaped = re.escape(term)
    return re.search(rf"(?<![a-z0-9_]){escaped}(?![a-z0-9_])", blob) is not None


def pollution_reasons(item: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    blob = text_blob(item)
    matched_terms = sorted(
        term
        for term in POLLUTION_TERMS
        if pollution_term_present(blob, term)
        and not is_professional_training_schema_usage(item, term)
        and not is_professional_ai_governance_usage(item, term)
        and not is_professional_numeric_scoring_usage(item, term)
        and not is_professional_trading_research_usage(item, term)
    )
    if matched_terms:
        reasons.append(f"pollution_terms:{','.join(matched_terms)}")

    st = source_types(item)
    review = item.get("review") if isinstance(item.get("review"), dict) else {}
    review_status = str(review.get("review_status", ""))
    source_evidence = item.get("source_evidence", [])
    pub = publishers(item)
    internal_only = bool(st) and st.issubset(INTERNAL_SOURCE_TYPES)
    cek_only = bool(pub) and pub.issubset({"CEK-TA", "cek-ta"})

    if not source_evidence:
        reasons.append("missing_source_evidence")
    if internal_only and not is_project_governance(item):
        reasons.append("internal_only_non_governance")
    if cek_only and not is_project_governance(item):
        reasons.append("cek_only_non_governance")
    if review_status == "approved" and not has_external_source(item) and not is_project_governance(item):
        reasons.append("approved_without_external_professional_source")
    return reasons


def scan() -> dict[str, Any]:
    polluted_items: list[dict[str, Any]] = []
    kept_internal_items: list[dict[str, Any]] = []
    scanned_count = 0

    for path in sorted(KNOWLEDGE_ROOT.glob("**/*.json")):
        item = read_json(path)
        scanned_count += 1
        reasons = pollution_reasons(item)
        knowledge_id = str(item.get("knowledge_id", path.stem))
        rel_path = path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()
        if reasons:
            polluted_items.append(
                {
                    "knowledge_id": knowledge_id,
                    "path": rel_path,
                    "reasons": reasons,
                    "action": "remove_from_formal_knowledge",
                }
            )
        elif source_types(item) & INTERNAL_SOURCE_TYPES:
            kept_internal_items.append(
                {
                    "knowledge_id": knowledge_id,
                    "path": rel_path,
                    "reasons": ["has_external_source_or_project_governance_scope"],
                }
            )

    return {
        "report_id": "phase33_knowledge_pollution_scan",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "scanned_count": scanned_count,
        "polluted_count": len(polluted_items),
        "polluted_items": polluted_items,
        "kept_internal_items": kept_internal_items,
        "gate_status": "pass" if not polluted_items else "fail",
    }


def main() -> int:
    report = scan()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["gate_status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
