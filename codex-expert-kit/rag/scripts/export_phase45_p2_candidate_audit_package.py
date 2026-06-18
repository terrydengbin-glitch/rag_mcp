"""Export Phase 45 P2 candidates for strict external audit."""

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


TODAY = "2026-06-12"
PHASE = "45"
TASK_ID = "CEK-TA-471"
PACKAGE_ID = "phase45_p2_candidate_audit_package_20260612"
PATTERNS = {
    "KB_02_DATA_ENGINEERING": "cand_20260612_phase45_reference_data_entitlement_*.json",
    "KB_03_MARKET_MICROSTRUCTURE": "cand_20260612_phase45_crypto_perp_*.json",
    "KB_07_RISK_MANAGEMENT": "cand_20260612_phase45_crypto_perp_*.json",
}

AUDIT_PACKAGE = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
PACKAGE_GATE = resolve_repo_path("docs", "reports", "phase45_p2_candidate_audit_package_quality_gate.json", start_file=__file__)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_candidates() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for partition, pattern in PATTERNS.items():
        cand_dir = resolve_repo_path("codex-expert-kit", "rag", "candidates", partition, start_file=__file__)
        for path in sorted(cand_dir.glob(pattern)):
            data = read_json(path)
            if data.get("status", {}).get("ingestion_decision") == "candidate_ready" and data.get("workflow", {}).get("stage") == "pending_external_audit":
                candidates.append(data)
    return sorted(candidates, key=lambda item: str(item.get("research_task_id")))


def package_quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    expected = {f"P45-G-DATA{idx:02d}" for idx in range(1, 7)} | {f"P45-H-CRYPTO{idx:02d}" for idx in range(1, 6)}
    actual = {str(item.get("research_task_id")) for item in candidates}
    if len(candidates) != 11:
        failures.append(f"expected 11 P2 candidate_ready candidates, got {len(candidates)}")
    if actual != expected:
        failures.append(f"unexpected research_task_id set: {sorted(actual ^ expected)}")
    ids = [item.get("candidate_id") for item in candidates]
    if len(ids) != len(set(ids)):
        failures.append("duplicate candidate_id detected")
    for item in candidates:
        cid = item.get("candidate_id", "<unknown>")
        task_id = str(item.get("research_task_id"))
        partition = item.get("classification", {}).get("partition_id")
        if task_id.startswith("P45-G") and partition != "KB_02_DATA_ENGINEERING":
            failures.append(f"{cid}: P45-G partition must be KB_02_DATA_ENGINEERING")
        if task_id.startswith("P45-H") and partition not in {"KB_03_MARKET_MICROSTRUCTURE", "KB_07_RISK_MANAGEMENT"}:
            failures.append(f"{cid}: P45-H partition mismatch")
        if item.get("status", {}).get("review_status") != "candidate_ready":
            failures.append(f"{cid}: review_status is not candidate_ready")
        if item.get("workflow", {}).get("stage") != "pending_external_audit":
            failures.append(f"{cid}: workflow.stage is not pending_external_audit")
        if len(item.get("source_refs", [])) < 3:
            failures.append(f"{cid}: source_refs < 3")
        if item.get("source_quality", {}).get("primary_source_count", 0) < 3:
            failures.append(f"{cid}: primary_source_count < 3")
        gate = item.get("machine_gate", {})
        if gate.get("default_guidance") != "deny":
            failures.append(f"{cid}: default guidance must be deny")
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "risk_threshold_advice_allowed", "trade_execution_advice_allowed"):
            if gate.get(field) is not False:
                failures.append(f"{cid}: {field} must be false")
        blob = json.dumps(item, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake detected")
        if re.search(r"\b(api_key|secret|private_key|password)\b", blob, flags=re.IGNORECASE):
            failures.append(f"{cid}: possible secret/private field detected")
    return {
        "gate_id": "phase45_p2_candidate_audit_package_quality_gate",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "package_id": PACKAGE_ID,
        "candidate_count": len(candidates),
        "expected_count": 11,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本包只审计 candidate；不得直接创建 reviewed、approved、default guidance 或 hard gate。",
            "P45-G 只能用于市场数据授权、reference data、point-in-time 元数据和 vendor schema 边界，不输出法律授权结论或交易信号。",
            "P45-H 只能用于 crypto perpetual 特有价格、funding、清算、ADL/insurance fund 和 outage/clawback 风险边界，不输出仓位、杠杆、清算规避或实盘许可。",
        ],
    }


def build_package(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": PACKAGE_ID,
        "created_at": TODAY,
        "created_by": "codex",
        "phase": PHASE,
        "task_id": TASK_ID,
        "scope": {
            "branch": "Trading Engineering / P2",
            "batches": [
                "P45-G Market Data Entitlement / Reference Data",
                "P45-H Crypto Perpetual",
            ],
            "candidate_count": len(candidates),
            "target": "审计 Phase 45 P2 11 条候选，包括市场数据授权、reference data、point-in-time 元数据、vendor schema、crypto perpetual mark/index/last price、funding、liquidation、ADL/insurance fund 和 outage/clawback 边界。",
        },
        "hard_boundaries": {
            "candidate_not_formal": True,
            "accepted_for_draft_not_reviewed": True,
            "reviewed_not_approved": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "legal_license_conclusion_allowed": False,
            "must_not_create_formal_knowledge": True,
            "must_not_generate": [
                "买卖点",
                "仓位",
                "杠杆",
                "止损止盈参数",
                "清算规避建议",
                "实盘执行建议",
                "法律授权结论",
                "数据再分发许可",
                "训练授权结论",
                "hard gate",
            ],
        },
        "audit_instructions": [
            "必须搜索相关的专业网站、官方文档、监管资料、交易所/供应商/crypto venue/API 文档、案例和数据，对本审计包进行严格审计。",
            "逐条检查来源是否足以支撑 claim；NYSE、Nasdaq、CME、Databento、Binance、Bybit、OKX 等来源不得被过度泛化。",
            "检查 P45-G 是否正确归入 Data Engineering / Reference Data Entitlement，并保持与 AI Engineering 训练数据、Market Microstructure 和 Strategy Feature Engineering 的 owner 边界。",
            "检查 P45-H 是否正确归入 Market Microstructure / Risk Management，不得混入交易策略 alpha、仓位建议、杠杆建议或清算规避建议。",
            "检查每条候选是否清楚声明适用范围、不适用场景、假设、限制、来源质量和 AI 使用边界。",
            "检查是否有中文乱码、mock/test 污染、项目私有策略参数、账户事实、密钥、真实订单、真实费率、真实阈值、真实授权状态或实盘敏感信息。",
            "输出只能是 accepted_for_draft、needs_more_evidence、rejected 或 blocked；不得输出 reviewed、approved、default guidance 或 hard gate。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "auditor": "string",
            "audited_at": "YYYY-MM-DD",
            "package_id": PACKAGE_ID,
            "summary": {"total": 11, "accepted_for_draft": 0, "needs_more_evidence": 0, "rejected": 0, "blocked": 0},
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | high",
                    "reviewed_allowed": False,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "risk_threshold_advice_allowed": False,
                    "trade_execution_advice_allowed": False,
                    "legal_license_conclusion_allowed": False,
                    "reasons": ["string"],
                    "required_followups": ["string"],
                    "patch_notes": {"source": ["string"], "content": ["string"], "boundary": ["string"], "conflict": ["string"]},
                    "source_assessment": {
                        "source_count": 0,
                        "missing_sources": ["string"],
                        "weak_sources": ["string"],
                        "recommended_extra_sources": ["string"],
                    },
                    "classification_assessment": {
                        "is_correct_branch": True,
                        "expected_branch": "Trading Engineering / P2",
                        "misplaced_topics": ["string"],
                    },
                }
            ],
        },
        "quality_gate": gate,
        "candidates": candidates,
    }


def main() -> int:
    candidates = load_candidates()
    gate = package_quality_gate(candidates)
    write_json(PACKAGE_GATE, gate)
    write_json(AUDIT_PACKAGE, build_package(candidates, gate))
    print(json.dumps({"status": gate["gate_status"], "candidate_count": len(candidates), "audit_package": str(AUDIT_PACKAGE)}, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
