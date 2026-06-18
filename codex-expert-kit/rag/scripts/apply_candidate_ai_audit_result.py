"""Apply external AI audit results to CEK-TA candidate and draft knowledge files."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 9).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return data


def write_json(path: Path, payload: dict[str, Any], *, dry_run: bool) -> None:
    if dry_run:
        return
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def list_json_files(root: Path) -> list[Path]:
    return sorted(root.glob("**/*.json"))


def index_by_field(paths: list[Path], field: str) -> dict[str, Path]:
    indexed: dict[str, Path] = {}
    for path in paths:
        payload = read_json(path)
        value = payload.get(field)
        if isinstance(value, str):
            indexed[value] = path
    return indexed


def index_knowledge_by_id(paths: list[Path]) -> dict[str, Path]:
    return index_by_field(paths, "knowledge_id")


def append_unique(log: list[Any], entry: dict[str, Any], key_fields: tuple[str, ...]) -> None:
    for existing in log:
        if not isinstance(existing, dict):
            continue
        if all(existing.get(key) == entry.get(key) for key in key_fields):
            return
    log.append(entry)


def audit_payload(audit: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    return {
        "audit_result_id": audit["audit_result_id"],
        "package_id": audit["package_id"],
        "auditor": audit["auditor"],
        "audited_at": audit["audited_at"],
        "decision": result["decision"],
        "confidence": result["confidence"],
        "reasons": result.get("reasons", []),
        "required_followups": result.get("required_followups", []),
        "patch_notes": result.get("patch_notes", []),
        "boundary": "accepted_for_draft/reviewed is not approved; approved requires a later human governance task.",
    }


def workflow_payload(audit: dict[str, Any], result: dict[str, Any], knowledge_id: str) -> dict[str, Any]:
    decision = result["decision"]
    audit_result_id = audit["audit_result_id"]
    if decision == "accepted_for_draft":
        return {
            "stage": "formalized_reviewed",
            "queue_group": "formalized",
            "formal_knowledge_id": knowledge_id,
            "formal_review_status": "reviewed",
            "ai_audit_result_id": audit_result_id,
            "hidden_from_default_queue": True,
            "next_action": "request_human_approval",
        }
    if decision == "needs_more_evidence":
        return {
            "stage": "needs_more_evidence",
            "queue_group": "needs_more_evidence",
            "formal_knowledge_id": knowledge_id or None,
            "formal_review_status": None,
            "ai_audit_result_id": audit_result_id,
            "hidden_from_default_queue": False,
            "next_action": "export_ai_audit",
        }
    return {
        "stage": "rejected",
        "queue_group": "rejected",
        "formal_knowledge_id": knowledge_id or None,
        "formal_review_status": None,
        "ai_audit_result_id": audit_result_id,
        "hidden_from_default_queue": True,
        "next_action": "none",
    }


def update_candidate(candidate: dict[str, Any], audit: dict[str, Any], result: dict[str, Any]) -> None:
    status = candidate.setdefault("status", {})
    review = candidate.setdefault("review", {})
    audit_log = review.setdefault("audit_log", [])
    if not isinstance(audit_log, list):
        audit_log = []
        review["audit_log"] = audit_log

    decision = result["decision"]
    if decision == "accepted_for_draft":
        status["review_status"] = "accepted"
        status["ingestion_decision"] = status.get("ingestion_decision") or "convert_to_knowledge_item"
    else:
        status["review_status"] = decision
    status["updated_at"] = TODAY
    status["decision_reason"] = (
        f"AI 审计结果为 {decision}；本状态只表示候选通过审计并可作为 draft/reviewed 来源，"
        "不代表 approved 或默认指导。"
    )

    review["ai_audit"] = audit_payload(audit, result)
    review["reviewed_at"] = TODAY
    review["reviewer"] = "external_ai_and_codex_alignment"
    candidate["workflow"] = workflow_payload(audit, result, str(result.get("proposed_knowledge_id") or ""))
    append_unique(
        audit_log,
        {
            "at": TODAY,
            "actor": audit["auditor"],
            "action": "ai_audit_result_received",
            "reason": f"{result['decision']} / confidence={result['confidence']}",
            "audit_result_id": audit["audit_result_id"],
        },
        ("action", "audit_result_id"),
    )
    append_unique(
        audit_log,
        {
            "at": TODAY,
            "actor": "codex",
            "action": "candidate_marked_accepted_after_ai_audit",
            "reason": "根据用户提供的 AI 审计结果和 CEK-TA 边界，将候选设为 accepted_for_draft；不得视为 approved。",
            "audit_result_id": audit["audit_result_id"],
        },
        ("action", "audit_result_id"),
    )


def extend_unique(values: list[Any], additions: list[str]) -> list[Any]:
    existing = {str(value) for value in values}
    for addition in additions:
        if addition not in existing:
            values.append(addition)
            existing.add(addition)
    return values


def apply_domain_patch(knowledge: dict[str, Any], result: dict[str, Any]) -> None:
    knowledge_id = knowledge.get("knowledge_id", "")
    content = knowledge.setdefault("content", {})
    applicability = knowledge.setdefault("applicability", {})
    source_evidence = knowledge.setdefault("source_evidence", [])

    if "kb_11_mcp_engineering" in knowledge_id:
        content["statement"] = (
            "Knowledge MCP 工具在对外暴露前必须声明稳定的 name、purpose、input_schema、output_schema、"
            "error_schema、permission boundary、rate/size limits、audit fields 和测试用例；CEK-TA 默认 MCP 工具必须只读，"
            "且只读必须由服务端权限层强制，不得只依赖 ToolAnnotations.readOnlyHint。"
        )
        risk_notes = content.setdefault("risk_notes", [])
        if isinstance(risk_notes, list):
            extend_unique(
                risk_notes,
                [
                    "MCP 2025-11-25 schema 明确 readOnlyHint 是 ToolAnnotations hint，不能作为不可信服务器的安全证明。",
                    "CEK-TA 只读 MCP 必须同时具备服务端权限控制、工具契约声明、错误结构和无写副作用测试。"
                ],
            )
        anti_patterns = content.setdefault("anti_patterns", [])
        if isinstance(anti_patterns, list):
            extend_unique(
                anti_patterns,
                [
                    "只在 MCP ToolAnnotations 中写 readOnlyHint，却没有服务端权限层和测试来阻断写操作。"
                ],
            )
        for source in source_evidence:
            if not isinstance(source, dict):
                continue
            title = str(source.get("source_title", ""))
            if title == "Model Context Protocol Specification":
                source["source_url"] = "https://modelcontextprotocol.io/specification/2025-11-25"
                source["version"] = "2025-11-25 specification (latest verified 2026-06-09)"
                source["accessed_at"] = TODAY
                source["evidence_summary"] = "MCP 官方规范 2025-11-25 版本定义协议、tools、JSON-RPC、安全信任原则和最新 schema，是 CEK-TA MCP tool contract 的主来源。"
            if title == "MCP Basic Protocol":
                source["source_url"] = "https://modelcontextprotocol.io/specification/2025-11-25"
                source["version"] = "2025-11-25"
                source["accessed_at"] = TODAY
            if title == "MCP Security Best Practices":
                source["source_url"] = "https://modelcontextprotocol.io/specification/2025-11-25"
                source["version"] = "2025-11-25"
                source["accessed_at"] = TODAY

    if "kb_10_rag_engineering" in knowledge_id:
        risk_notes = content.setdefault("risk_notes", [])
        if isinstance(risk_notes, list):
            extend_unique(
                risk_notes,
                [
                    "conflict_status、review_status 和 freshness gate 是 CEK-TA 专业知识库的组合治理规则，不是 OpenAI、Qdrant、LangChain 或 LlamaIndex 单个框架直接规定的标准。",
                    "外部来源支撑 metadata filtering、citation、retrieval evaluation；默认指导阻断由 CEK-TA 内部检索契约和治理规则共同支撑。"
                ],
            )
        for source in source_evidence:
            if isinstance(source, dict) and source.get("source_title") == "OpenAI File Search":
                source["accessed_at"] = TODAY
                source["version"] = "File Search docs verified 2026-06-09"
                source["evidence_summary"] = "官方文档支持 file_search_call.results 返回检索结果，并支持基于文件 metadata/attributes 过滤检索结果。"

    if "kb_06_live_execution" in knowledge_id:
        risk_notes = content.setdefault("risk_notes", [])
        if isinstance(risk_notes, list):
            extend_unique(
                risk_notes,
                [
                    "本知识只覆盖 Binance USDⓈ-M Futures 边界；其他交易所的状态枚举、断线恢复、成交字段和仓位语义必须重新映射和审计。"
                ],
            )
        not_applicable = applicability.setdefault("not_applicable_when", [])
        if isinstance(not_applicable, list):
            extend_unique(
                not_applicable,
                [
                    "直接迁移到非 Binance USDⓈ-M Futures 交易所且未重新映射订单事件、REST 查询、仓位字段和断线恢复语义"
                ],
            )

    if "kb_07_risk_management" in knowledge_id:
        not_applicable = applicability.setdefault("not_applicable_when", [])
        if isinstance(not_applicable, list):
            extend_unique(
                not_applicable,
                [
                    "需要具体杠杆倍数、仓位大小、止损比例或策略参数建议时，本知识只能作为工程风控闸门，不提供交易参数。"
                ],
            )
        risk_notes = content.setdefault("risk_notes", [])
        if isinstance(risk_notes, list):
            extend_unique(
                risk_notes,
                [
                    "SEC/CFTC/CME 来源支撑 pre-trade controls 和自动化交易风险控制，不支撑具体策略收益或仓位参数。"
                ],
            )

    if "kb_13_knowledge_governance" in knowledge_id:
        risk_notes = content.setdefault("risk_notes", [])
        if isinstance(risk_notes, list):
            extend_unique(
                risk_notes,
                [
                    "NIST AI RMF 支撑风险治理框架；CEK-TA proposed/candidate/draft/reviewed/approved/deprecated 状态机是本项目内部治理规则，不是 NIST 直接规定。"
                ],
            )

    if "kb_05_replay_simulation" in knowledge_id:
        risk_notes = content.setdefault("risk_notes", [])
        if isinstance(risk_notes, list):
            extend_unique(
                risk_notes,
                [
                    "OHLC-only 规则只说明同根路径不可观测；若有可信 tick/path replay 或交易所成交事件，应按更低粒度事件链重新判断。"
                ],
            )

    if "kb_04_backtest.bias.leakage_overfit" in knowledge_id:
        risk_notes = content.setdefault("risk_notes", [])
        if isinstance(risk_notes, list):
            extend_unique(
                risk_notes,
                [
                    "数据泄漏、测试集调参、多重试验选择和 PBO 可后续拆分为多个知识条目；本条先作为回测偏差审计总门。"
                ],
            )

    patch_notes = content.setdefault("audit_patch_notes", [])
    if isinstance(patch_notes, list):
        extend_unique(patch_notes, result.get("patch_notes", []))


def update_knowledge(knowledge: dict[str, Any], audit: dict[str, Any], result: dict[str, Any]) -> None:
    review = knowledge.setdefault("review", {})
    decision_log = review.setdefault("decision_log", [])
    if not isinstance(decision_log, list):
        decision_log = []
        review["decision_log"] = decision_log

    if result["decision"] == "accepted_for_draft":
        review["review_status"] = "reviewed"
    review["reviewed_at"] = TODAY
    review["updated_at"] = TODAY
    review["reviewer"] = "codex"
    review["ai_audit"] = audit_payload(audit, result)
    review["source_candidate_id"] = result["candidate_id"]
    review["ai_audit_result_id"] = audit["audit_result_id"]
    review["approval_status"] = review.get("approval_status") or "not_requested"
    review["default_guidance_allowed"] = bool(
        review.get("review_status") == "approved" and review.get("approval_status") == "approved"
    )
    apply_domain_patch(knowledge, result)

    append_unique(
        decision_log,
        {
            "at": TODAY,
            "actor": audit["auditor"],
            "decision": "ai_audit_accepted_for_draft",
            "reason": f"外部 AI 审计结论：{result['decision']} / confidence={result['confidence']}。",
            "audit_result_id": audit["audit_result_id"],
        },
        ("decision", "audit_result_id"),
    )
    append_unique(
        decision_log,
        {
            "at": TODAY,
            "actor": "codex",
            "decision": "review_status_updated_to_reviewed",
            "reason": "按用户提供的审计结果和 CEK-TA 回写契约修正知识；reviewed 不等于 approved。",
            "audit_result_id": audit["audit_result_id"],
        },
        ("decision", "audit_result_id"),
    )


def run(audit_path: Path, *, dry_run: bool) -> dict[str, Any]:
    candidate_root = resolve_repo_path("codex-expert-kit", "rag", "candidates", start_file=__file__)
    knowledge_root = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
    audit = read_json(audit_path)
    candidate_paths = index_by_field(list_json_files(candidate_root), "candidate_id")
    knowledge_paths = index_knowledge_by_id(list_json_files(knowledge_root))

    updated_candidates: list[str] = []
    updated_knowledge: list[str] = []
    skipped: list[str] = []
    decisions: dict[str, int] = {}

    for result in audit.get("candidate_results", []):
        if not isinstance(result, dict):
            continue
        candidate_id = result.get("candidate_id")
        knowledge_id = result.get("proposed_knowledge_id")
        if not isinstance(candidate_id, str) or not isinstance(knowledge_id, str):
            skipped.append(str(result))
            continue

        candidate_path = candidate_paths.get(candidate_id)
        knowledge_path = knowledge_paths.get(knowledge_id)
        if candidate_path is None or knowledge_path is None:
            skipped.append(candidate_id)
            continue

        candidate = read_json(candidate_path)
        knowledge = read_json(knowledge_path)
        update_candidate(candidate, audit, result)
        update_knowledge(knowledge, audit, result)
        write_json(candidate_path, candidate, dry_run=dry_run)
        write_json(knowledge_path, knowledge, dry_run=dry_run)
        updated_candidates.append(str(candidate_path))
        updated_knowledge.append(str(knowledge_path))
        decision = str(result.get("decision"))
        decisions[decision] = decisions.get(decision, 0) + 1

    return {
        "audit_result_id": audit.get("audit_result_id"),
        "package_id": audit.get("package_id"),
        "auditor": audit.get("auditor"),
        "audited_at": audit.get("audited_at"),
        "dry_run": dry_run,
        "candidate_result_count": len(audit.get("candidate_results", [])),
        "decision_counts": decisions,
        "updated_candidates": updated_candidates,
        "updated_knowledge": updated_knowledge,
        "skipped": skipped,
        "boundary": "reviewed is not approved; Phase 32 import does not create approved/default guidance.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "audit_result",
        nargs="?",
        default="docs/audit/phase31_candidate_ai_audit_result_20260609.json",
        help="Path to candidate AI audit result JSON, relative to CEK-TA root unless absolute.",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--report-path",
        default="docs/reports/latest_candidate_ai_audit_backwrite_report.json",
        help="Machine-readable backwrite report path, relative to CEK-TA root unless absolute.",
    )
    args = parser.parse_args()

    audit_path = Path(args.audit_result)
    if not audit_path.is_absolute():
        audit_path = resolve_repo_path(*audit_path.parts, start_file=__file__)
    report = run(audit_path, dry_run=args.dry_run)
    report_path = Path(args.report_path)
    if not report_path.is_absolute():
        report_path = resolve_repo_path(*report_path.parts, start_file=__file__)
    if not args.dry_run:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        report["report_path"] = str(report_path)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["skipped"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
