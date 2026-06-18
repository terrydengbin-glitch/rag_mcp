"""Export Phase 53 reviewed/caveat_only preparation audit package.

All five Phase 53 P0 candidates are accepted_for_draft. This script prepares
the next external audit package to decide whether each candidate may become
formal reviewed/caveat_only knowledge.

It does not create formal knowledge, approved knowledge, default guidance, hard
gates, legal opinions, manipulation findings, risk thresholds, or trading
execution advice.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-13"
PHASE = 53
TASK_ID = "CEK-TA-524"
PACKAGE_ID = "phase53_reviewed_preparation_audit_package_20260613"

CANDIDATE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "candidates", start_file=__file__)
AUDIT_PACKAGE_PATH = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
QUALITY_GATE_PATH = resolve_repo_path(
    "docs", "reports", "phase53_reviewed_preparation_quality_gate.json", start_file=__file__
)
EXPORT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase53_reviewed_preparation_export_report.md", start_file=__file__
)

EXPECTED_TASK_IDS = {
    "P53-AI-SEC01",
    "P53-AI-SBOM01",
    "P53-TR-MC01",
    "P53-TR-MA01",
    "P53-TR-TS01",
}


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def dump_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def dump_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def load_phase53_candidates() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for path in sorted(CANDIDATE_ROOT.glob("**/*phase53*.json")):
        item = load_json(path)
        if item.get("research_task_id") in EXPECTED_TASK_IDS:
            item["_source_path"] = path.relative_to(resolve_repo_path(".", start_file=__file__)).as_posix()
            candidates.append(item)
    return sorted(candidates, key=lambda item: str(item.get("research_task_id")))


def candidate_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    actual_task_ids = {str(item.get("research_task_id")) for item in candidates}
    if actual_task_ids != EXPECTED_TASK_IDS:
        failures.append(f"unexpected Phase 53 task ids: missing={sorted(EXPECTED_TASK_IDS - actual_task_ids)}, extra={sorted(actual_task_ids - EXPECTED_TASK_IDS)}")
    if len(candidates) != 5:
        failures.append(f"expected 5 Phase 53 candidates, got {len(candidates)}")

    ids = [str(item.get("candidate_id")) for item in candidates]
    if len(ids) != len(set(ids)):
        failures.append("duplicate candidate_id detected")

    for item in candidates:
        cid = str(item.get("candidate_id"))
        status = item.get("status", {})
        workflow = item.get("workflow", {})
        review = item.get("review", {})
        machine_gate = item.get("machine_gate", {})
        classification = item.get("classification", {})
        source_refs = item.get("source_refs", [])
        blob = json.dumps(item, ensure_ascii=False)

        if status.get("ingestion_decision") != "accepted_for_draft":
            failures.append(f"{cid}: ingestion_decision is not accepted_for_draft")
        if workflow.get("stage") != "accepted_for_draft":
            failures.append(f"{cid}: workflow.stage is not accepted_for_draft")
        if review.get("approved_allowed") is not False:
            failures.append(f"{cid}: approved_allowed must be false")
        if review.get("default_guidance_allowed") is not False:
            failures.append(f"{cid}: default_guidance_allowed must be false")
        if review.get("hard_gate_allowed") is not False:
            failures.append(f"{cid}: hard_gate_allowed must be false")
        if machine_gate.get("default_guidance") != "deny":
            failures.append(f"{cid}: machine_gate.default_guidance must be deny")
        if machine_gate.get("visible_in_default_guidance_queue") is not False:
            failures.append(f"{cid}: visible_in_default_guidance_queue must be false")
        if not classification.get("canonical_node_id"):
            failures.append(f"{cid}: missing canonical_node_id")
        if len(source_refs) < 3:
            failures.append(f"{cid}: source_refs < 3")
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake detected")
        if re.search(r"\b(api_key|secret|private_key|password|access_token)\b", blob, flags=re.IGNORECASE):
            failures.append(f"{cid}: possible secret-like field detected")

        task_id = str(item.get("research_task_id"))
        if task_id == "P53-AI-SEC01":
            warnings.append("P53-AI-SEC01 reviewed 前需重点审计 memory poisoning / MCP tool governance 是否需要内部 contract extract。")
        if task_id == "P53-AI-SBOM01":
            warnings.append("P53-AI-SBOM01 reviewed 前需确认 CycloneDX/SPDX AI BOM 或等价 schema 是否必须补入。")
        if task_id == "P53-TR-MC01":
            warnings.append("P53-TR-MC01 reviewed 前必须保留 FINRA/CFTC jurisdiction caveat，不能写成 manipulation finding。")
        if task_id == "P53-TR-TS01":
            warnings.append("P53-TR-TS01 reviewed 前需确认 audit_time_sync_context schema extract 是否足够。")

    return {
        "gate_id": "phase53_reviewed_preparation_quality_gate",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "package_id": PACKAGE_ID,
        "candidate_count": len(candidates),
        "expected_count": 5,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": sorted(set(warnings)),
        "boundary": "This gate only checks export readiness. It does not authorize formal reviewed/approved/default/hard gate.",
    }


def build_package(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": PACKAGE_ID,
        "created_at": TODAY,
        "created_by": "codex",
        "phase": PHASE,
        "task_id": TASK_ID,
        "scope": {
            "branch": "AI Engineering / Trading Engineering",
            "batch": "Phase 53 P0 reviewed/caveat_only preparation",
            "candidate_count": len(candidates),
            "target": "审计 5 条 Phase 53 accepted_for_draft 候选是否可转 formal reviewed/caveat_only。",
        },
        "hard_boundaries": {
            "candidate_not_formal": True,
            "accepted_for_draft_not_reviewed": True,
            "reviewed_not_approved": True,
            "max_allowed_decision": "accepted_for_reviewed_caveat_only",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "legal_opinion_allowed": False,
            "manipulation_finding_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "must_not_create_formal_knowledge": True,
            "must_not_generate": [
                "法律意见",
                "操纵定性",
                "合规满足声明",
                "买卖点",
                "仓位",
                "杠杆",
                "止损止盈",
                "风险阈值",
                "交易许可",
                "hard gate",
            ],
        },
        "audit_instructions": [
            "必须搜索相关专业网站、官方资料、监管资料、标准、案例和数据，对 reviewed/caveat_only 准备进行严格审计。",
            "逐条判断是否可进入 formal reviewed/caveat_only；不得输出 approved、default guidance 或 hard gate。",
            "重点检查 source_refs 是否直接支撑 claim，不得把 NIST/OWASP/MITRE/CISA/FINRA/CFTC/SEC/ESMA/OpenTelemetry 过度泛化。",
            "重点检查 AI Agent Threat Model 是否需要补 memory poisoning / MCP tool governance 内部 contract extract。",
            "重点检查 AI SBOM / Model SBOM 是否需要补 CycloneDX ML-BOM、SPDX AI BOM 或等价 schema。",
            "重点检查 Market Conduct taxonomy 是否只作为 surveillance labels / reason codes / manual escalation context，不得写成 manipulation finding。",
            "重点检查 Market Access / DEA 是否按 US SEC、EU MiFID、FIA source group 拆分 jurisdiction caveat。",
            "重点检查 Time Synchronization 是否补足 audit_time_sync_context 字段并区分 FINRA/CAT、RTS 25、OpenTelemetry 语境。",
            "检查是否有中文乱码、mock/test 污染、密钥、账户事实、项目私有策略参数、真实阈值或实盘敏感信息。",
        ],
        "allowed_decisions": [
            "accepted_for_reviewed_caveat_only",
            "needs_more_evidence",
            "rejected",
            "blocked",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "auditor": "string",
            "audited_at": "YYYY-MM-DD",
            "package_id": PACKAGE_ID,
            "summary": {
                "total": 5,
                "accepted_for_reviewed_caveat_only": 0,
                "needs_more_evidence": 0,
                "rejected": 0,
                "blocked": 0,
            },
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | high",
                    "reviewed_allowed": "boolean",
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "legal_opinion_allowed": False,
                    "trade_execution_advice_allowed": False,
                    "risk_threshold_advice_allowed": False,
                    "reasons": ["string"],
                    "required_followups": ["string"],
                    "patch_notes": {
                        "source": ["string"],
                        "content": ["string"],
                        "boundary": ["string"],
                        "conflict": ["string"],
                    },
                    "source_assessment": {
                        "source_count": 0,
                        "missing_sources": ["string"],
                        "weak_sources": ["string"],
                        "recommended_extra_sources": ["string"],
                    },
                    "classification_assessment": {
                        "is_correct_branch": True,
                        "expected_branch": "AI Engineering 或 Trading Engineering 对应子分支",
                        "misplaced_topics": ["string"],
                    },
                }
            ],
        },
        "quality_gate": gate,
        "candidates": candidates,
    }


def build_report(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> str:
    rows = [
        "| research_task_id | candidate_id | canonical_node_id | source_count |",
        "| --- | --- | --- | --- |",
    ]
    for item in candidates:
        rows.append(
            "| {task} | `{cid}` | `{node}` | {count} |".format(
                task=item.get("research_task_id"),
                cid=item.get("candidate_id"),
                node=item.get("classification", {}).get("canonical_node_id"),
                count=len(item.get("source_refs", [])),
            )
        )
    return "\n".join(
        [
            "# Phase 53 reviewed-preparation 审计包导出报告",
            "",
            f"创建日期：{TODAY}",
            "",
            "## 结论",
            "",
            f"- 审计包：`docs/audit/{PACKAGE_ID}.json`",
            f"- 质量门禁：`{gate['gate_status']}`",
            f"- 候选数量：{len(candidates)} / 5",
            "- 本步骤不创建 formal reviewed、approved、default guidance 或 hard gate。",
            "",
            "## 候选清单",
            "",
            *rows,
            "",
            "## 下一步",
            "",
            "将 `docs/audit/phase53_reviewed_preparation_audit_package_20260613.json` 交给外部 AI/人工严格审计。只有审计明确返回 `accepted_for_reviewed_caveat_only` 的条目，后续才允许在单独任务中 materialize 为 formal reviewed/caveat_only。",
            "",
        ]
    )


def main() -> None:
    candidates = load_phase53_candidates()
    gate = candidate_gate(candidates)
    dump_json(QUALITY_GATE_PATH, gate)
    if gate["gate_status"] != "pass":
        dump_json(AUDIT_PACKAGE_PATH, build_package(candidates, gate))
        raise SystemExit(f"quality gate failed: {gate['failures']}")
    package = build_package(candidates, gate)
    dump_json(AUDIT_PACKAGE_PATH, package)
    dump_text(EXPORT_REPORT_PATH, build_report(candidates, gate))
    print(json.dumps({"package": str(AUDIT_PACKAGE_PATH), "candidate_count": len(candidates), "gate": gate["gate_status"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
