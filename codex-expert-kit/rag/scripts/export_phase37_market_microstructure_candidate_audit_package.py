"""Export Phase 37 Market Microstructure candidate audit package."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-11"
PHASE = "37"
TASK_ID = "CEK-TA-403"
PARTITION = "KB_03_MARKET_MICROSTRUCTURE"

CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
AUDIT_PACKAGE = resolve_repo_path(
    "docs", "audit", "phase37_market_microstructure_candidate_audit_package_20260611.json", start_file=__file__
)
QUALITY_GATE = resolve_repo_path(
    "docs", "reports", "phase37_market_microstructure_candidate_audit_package_quality_gate.json", start_file=__file__
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_candidates() -> list[dict[str, Any]]:
    candidates = []
    for path in sorted(CAND_DIR.glob("cand_20260611_phase37_market_microstructure_*.json")):
        data = read_json(path)
        if data.get("workflow", {}).get("stage") == "candidate_ready":
            candidates.append(data)
    return candidates


def validate_package(candidates: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if len(candidates) != 12:
        errors.append(f"expected 12 candidate_ready candidates, got {len(candidates)}")
    for item in candidates:
        cid = item.get("candidate_id", "<missing>")
        if item.get("classification", {}).get("partition_id") != PARTITION:
            errors.append(f"{cid}: partition mismatch")
        if item.get("status", {}).get("ingestion_decision") != "candidate_ready":
            errors.append(f"{cid}: ingestion_decision must be candidate_ready")
        if len(item.get("source_refs", [])) < 3:
            errors.append(f"{cid}: source_refs < 3")
        machine_gate = item.get("machine_gate", {})
        if machine_gate.get("default_guidance") != "deny":
            errors.append(f"{cid}: default guidance must be denied")
        if machine_gate.get("approved_allowed") is not False:
            errors.append(f"{cid}: approved_allowed must be false")
        if machine_gate.get("hard_gate_allowed") is not False:
            errors.append(f"{cid}: hard_gate_allowed must be false")
    return errors


def main() -> None:
    candidates = load_candidates()
    errors = validate_package(candidates)
    package = {
        "schema_version": "1.0.0",
        "package_id": "phase37_market_microstructure_candidate_audit_package_20260611",
        "phase": PHASE,
        "task_id": TASK_ID,
        "created_at": TODAY,
        "purpose": "外部 AI/人工对 Phase 37 Market Microstructure 12 条候选进行严格审计，判断每条只能进入 accepted_for_draft、needs_more_evidence 或 rejected。",
        "hard_boundaries": {
            "candidate_is_not_formal_knowledge": True,
            "reviewed_allowed_in_this_package": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_instruction_allowed": False,
            "must_not_generate": ["买卖点", "仓位", "杠杆", "止损止盈参数", "实盘执行建议"],
        },
        "audit_instructions": [
            "必须搜索相关专业网站、论文、官方文档、监管资料、交易所/API 文档、案例和数据，对候选来源与 claim 进行严格审计。",
            "检查每条 claim 是否被来源充分支持，尤其是盘口深度、逐笔成交、aggressor side、CVD、funding/OI、流动性、滑点、延迟和市场影响成本。",
            "检查是否混入 AI Engineering、Backtest、Replay、Live Execution 或 Risk Management 本体；如混入，请给出拆分建议。",
            "检查供应商/平台文档是否被过度当作通用理论来源；字段级文档只能支撑数据语义，不能证明交易优势。",
            "检查是否存在中文乱码、mock/test 污染、项目私有参数、账户事实、密钥、交易所私有配置或实盘敏感信息。",
            "只允许输出 accepted_for_draft / needs_more_evidence / rejected；不得输出 reviewed、approved、default_guidance 或 hard_gate。",
            "若 needs_more_evidence，请列出缺少的具体来源类型、需要补强的 statement、边界和冲突处理。",
        ],
        "expected_output_schema": {
            "package_id": "string",
            "quality_gate": {"pass": "boolean", "reason": "string"},
            "results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected",
                    "confidence": "low | medium | medium_high | high",
                    "reviewed_allowed": False,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "patch_notes": {
                        "source": ["string"],
                        "content": ["string"],
                        "boundary": ["string"],
                        "conflict": ["string"],
                    },
                    "reason": "string",
                }
            ],
        },
        "scope_notes": [
            "本批归入 KB_03_MARKET_MICROSTRUCTURE / Trading Engineering / Market Microstructure。",
            "本批只做市场微观结构、订单簿、订单流、流动性、滑点、延迟和市场影响边界，不证明任何策略盈利。",
            "AI Engineering 只能通过 knowledge_refs 引用本批规则，不得复制改写 Trading Engineering 规则本体。",
        ],
        "candidate_count": len(candidates),
        "candidates": candidates,
    }
    quality = {
        "quality_gate": {"pass": not errors, "errors": errors},
        "phase": PHASE,
        "task_id": TASK_ID,
        "created_at": TODAY,
        "candidate_count": len(candidates),
        "candidate_ids": [item["candidate_id"] for item in candidates],
        "audit_package": str(AUDIT_PACKAGE),
    }
    write_json(AUDIT_PACKAGE, package)
    write_json(QUALITY_GATE, quality)
    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
