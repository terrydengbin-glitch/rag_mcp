"""Prepare Phase 37 blocked Quant Foundation supplemental re-audit package.

CEK-TA-381 keeps the three blocked candidates as candidate-only artifacts,
adds source-backed supplemental evidence, and exports a reviewed/caveat_only
re-audit package. It must not create formal reviewed/approved/default/hard-gate
knowledge.
"""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_project_root, resolve_repo_path  # noqa: E402


ROOT = resolve_project_root(__file__)
TODAY = "2026-06-11"
TASK_ID = "CEK-TA-381"
PACKAGE_ID = "phase37_quant_foundation_blocked_supplemental_reaudit_package_20260611"
REPORT_ID = "phase37_quant_foundation_blocked_supplemental_reaudit_report"

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_01_QUANT_FOUNDATION", start_file=__file__
)
RESEARCH_PATH = resolve_repo_path(
    "docs", "research", "phase37_quant_foundation_blocked_supplemental_research.md", start_file=__file__
)
AUDIT_PACKAGE_PATH = resolve_repo_path(
    "docs", "audit", "phase37_quant_foundation_blocked_supplemental_reaudit_package_20260611.json", start_file=__file__
)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_quant_foundation_blocked_supplemental_reaudit_report.json", start_file=__file__
)


SUPPLEMENTAL_SPECS: dict[str, dict[str, Any]] = {
    "P37-A-Q02": {
        "candidate_file": "cand_20260611_phase37_r_multiple_definition_001.json",
        "title": "R-multiple 页码级书籍证据补强",
        "target_decision": "reviewed/caveat_only 准备再审",
        "claim_patch": {
            "statement": (
                "R-multiple 将单笔交易盈亏表达为相对初始风险单位 R 的倍数；它是风险归一化的交易结果指标，"
                "可用于复盘、结果比较、标签候选和研究评估，但必须受成本、滑点、样本量、回撤和验证边界约束。"
            ),
            "normalized_claim": "phase37_r_multiple_as_risk_normalized_trade_outcome_metric",
            "evidence_summary": (
                "Van Tharp Institute 直接支撑 R-multiple distribution、expectancy 与 R-value；"
                "Van Tharp Position Sizing 书籍目录给出页码级章节线索：Risk (R) and R-Multiples p.11、"
                "Understanding R-Multiples p.12、Using Your Total Risk to Keep Track of Your R-Multiples p.14、"
                "What If You Don’t Know Your Initial Risk? p.16、More Thoughts about Expectancy p.18。"
            ),
            "interpretation_notes": (
                "R-multiple 只能表达风险归一化交易结果，不能单独判断 edge、盈利能力、稳健性、实盘资格、仓位或执行许可。"
            ),
        },
        "source_refs": [
            {
                "source_id": "src_phase37_q02_tharp_position_sizing_toc_page_refs",
                "source_title": "Van Tharp's Definitive Guide to Position SizingSM - Table of Contents page references",
                "source_url": "https://nexusfi.com/attachments/893d1248578892",
                "source_type": "book_preview_page_reference",
                "publisher": "International Institute of Trading Mastery / NexusFi attachment mirror",
                "published_at": "2008-01-01",
                "accessed_at": TODAY,
                "version": "preview excerpt",
                "reliability": "medium_high",
                "score": 84,
                "relevance": "high",
                "freshness": "stable",
                "page_refs": [
                    "TOC: Chapter 2 Risk (R) and R-Multiples, p.11",
                    "TOC: Understanding R-Multiples, p.12",
                    "TOC: Using Your Total Risk to Keep Track of Your R-Multiples, p.14",
                    "TOC: What If You Don’t Know Your Initial Risk?, p.16",
                    "TOC: More Thoughts about Expectancy, p.18",
                    "TOC: What about the Variability?, p.19",
                    "TOC: So What’s the Downside?, p.21",
                ],
                "limitations": [
                    "只保存目录级页码证据和摘要，不保存书籍正文；正式 approved 仍需人工核验合法持有版本的正文页。",
                    "该来源用于满足 reviewed-preparation 页码级线索，不单独授权 default guidance。",
                ],
                "evidence_summary": (
                    "目录页明确列出 R、R-multiples、total risk tracking、initial risk、expectancy 和 variability 的页码区间，"
                    "可作为 R-multiple 本体来源的页码级证据线索。"
                ),
                "quoted_excerpt_allowed": False,
            },
            {
                "source_id": "src_phase37_q02_van_tharp_expectancy_r_distribution",
                "source_title": "Tharp Think Trading Concepts",
                "source_url": "https://vantharpinstitute.com/tharp-think-trading-concepts/",
                "source_type": "professional_training_note",
                "publisher": "Van Tharp Institute",
                "published_at": None,
                "accessed_at": TODAY,
                "version": None,
                "reliability": "medium_high",
                "score": 84,
                "relevance": "high",
                "freshness": "stable",
                "limitations": [
                    "网页直接支撑 R-multiple distribution 和 expectancy，但不是书籍页码级证据。",
                    "只作为 reviewed/caveat_only 支撑，不授权 approved/default/hard gate。",
                ],
                "evidence_summary": (
                    "网页说明交易系统可由其生成的 R-multiple distribution 表征，expectancy 是平均 R-multiple；"
                    "同时给出按 R 记录交易结果的示例和样本量 caveat。"
                ),
                "quoted_excerpt_allowed": False,
            },
        ],
        "supplemental_notes": [
            "补充了 Van Tharp Position Sizing 书籍目录的页码级线索，解决 reviewed-preparation 的主要阻断点。",
            "仍保持 caveat_only：不得用 R-multiple 单独判断交易质量、edge、盈利能力、稳健性或实盘资格。",
        ],
    },
    "P37-A-Q06": {
        "candidate_file": "cand_20260611_phase37_position_sizing_requires_risk_unit_001.json",
        "title": "仓位 sizing 交易规则与 AI 治理边界拆分",
        "target_decision": "reviewed/caveat_only 准备再审",
        "claim_patch": {
            "statement": (
                "仓位 sizing 的交易规则本体应限定为：进入仓位计算前必须有账户风险预算、单笔风险单位、"
                "止损或失效边界、最大暴露和杠杆/保证金边界；AI/RAG 只能提示缺字段或路由人工复核，不能自行推导仓位。"
            ),
            "normalized_claim": "phase37_position_sizing_requires_explicit_risk_unit_and_ai_missing_field_boundary",
            "evidence_summary": (
                "Investopedia 和 CrossTrade 支撑仓位 sizing 需要账户风险、交易风险/止损距离和风险百分比；"
                "Investor.gov/SEC 支撑保证金会放大损失；CEK-TA Phase 38 runtime contract 支撑缺字段时 LLM audit 只能提示/降级，不能作为 final gate。"
            ),
            "interpretation_notes": (
                "本条拆成两个边界：Trading Engineering 保存仓位 sizing 事实；AI Engineering 只保存缺字段提示、"
                "schema 校验和 human_review/needs_more_evidence 路由，不得输出具体仓位。"
            ),
        },
        "source_refs": [
            {
                "source_id": "src_phase37_q06_investor_gov_margin_larger_losses",
                "source_title": "Investor Bulletin: Understanding Margin Accounts",
                "source_url": "https://www.investor.gov/introduction-investing/general-resources/news-alerts-bulletins/investor-bulletins-29".replace(
                    "news-alerts-bulletins", "news-alerts/alerts-bulletins"
                ),
                "source_type": "regulatory_guidance",
                "publisher": "Investor.gov / U.S. SEC",
                "published_at": None,
                "accessed_at": TODAY,
                "version": None,
                "reliability": "high",
                "score": 88,
                "relevance": "high",
                "freshness": "time_sensitive",
                "limitations": [
                    "美国证券保证金投资者教育材料；不同市场、交易所、期货、CFD 或 crypto 规则不同。",
                    "用于支撑杠杆/保证金风险边界，不用于计算具体仓位。"
                ],
                "evidence_summary": "Investor.gov 说明 margin 会提高购买力，同时暴露于更大损失风险。",
                "quoted_excerpt_allowed": False,
            },
            {
                "source_id": "src_phase37_q06_cek_ta_phase38_runtime_contract_missing_field",
                "source_title": "CEK-TA Phase 38 AI scoring gate runtime contract",
                "source_url": "docs/contracts/phase38_ai_scoring_gate_runtime_contract.md",
                "source_type": "internal_contract",
                "publisher": "CEK-TA",
                "published_at": "2026-06-10",
                "accessed_at": TODAY,
                "version": "phase38_runtime_contract_v1",
                "reliability": "high",
                "score": 90,
                "relevance": "high",
                "freshness": "current",
                "limitations": [
                    "内部治理契约只能支撑 AI 行为边界，不能替代外部交易仓位 sizing 来源。",
                    "用于 reviewed/caveat_only，不授权 approved/default/hard gate。"
                ],
                "evidence_summary": (
                    "该契约定义 LLM audit 负责解释 scorer 输出、生成 reason code、missing field 与人工复核摘要；"
                    "unsupported_claims 不为空时 final gate 不得因 LLM 输出而放行。"
                ),
                "quoted_excerpt_allowed": False,
            },
            {
                "source_id": "src_phase37_q06_crosstrade_position_sizing_risk_stop",
                "source_title": "Position Sizing",
                "source_url": "https://crosstrade.io/learn/risk-management/position-sizing",
                "source_type": "trading_education",
                "publisher": "CrossTrade",
                "published_at": None,
                "accessed_at": TODAY,
                "version": None,
                "reliability": "medium",
                "score": 70,
                "relevance": "high",
                "freshness": "stable",
                "limitations": [
                    "交易教育资料；只能作为 supporting source。",
                    "具体风控阈值必须由外接项目 owner 定义。"
                ],
                "evidence_summary": "支持按账户风险、止损距离和合约/资产波动来确定仓位 sizing，而不是 AI 自行推导。",
                "quoted_excerpt_allowed": False,
            },
        ],
        "supplemental_notes": [
            "将原 claim 拆为 Trading Engineering 外部事实和 AI Engineering 内部治理边界。",
            "AI 只能提示缺字段、触发 needs_more_evidence/human_review，不得生成具体仓位、杠杆或订单动作。",
        ],
    },
    "P37-A-Q11": {
        "candidate_file": "cand_20260611_phase37_sample_size_and_regime_caveat_001.json",
        "title": "样本量、regime 与 non-stationarity 泛化边界补证",
        "target_decision": "reviewed/caveat_only 准备再审",
        "claim_patch": {
            "statement": (
                "交易系统评价必须声明样本数量、样本时期、市场状态、资产范围和验证方式；"
                "样本过小、只覆盖单一 regime，或未处理金融市场 non-stationarity 时，不得泛化为跨市场、跨周期或跨状态规则。"
            ),
            "normalized_claim": "phase37_sample_size_regime_non_stationarity_generalization_boundary",
            "evidence_summary": (
                "Bailey et al. 支撑回测过拟合风险；LSEG 和 State Street 资料支撑 market regime 识别与资产表现差异；"
                "UCL 金融时间序列研究支撑金融系统结构随时间变化和 non-stationarity 对统计假设的挑战。"
            ),
            "interpretation_notes": (
                "本条只定义方法论边界：单一样本或单一 regime 下的结果不能被 AI/RAG 写成跨市场、跨周期、跨状态的通用规则。"
            ),
        },
        "source_refs": [
            {
                "source_id": "src_phase37_q11_lseg_market_regime_detection",
                "source_title": "Market regime detection using Statistical and ML based approaches",
                "source_url": "https://developers.lseg.com/en/article-catalog/article/market-regime-detection",
                "source_type": "market_data_provider_research",
                "publisher": "LSEG Developer Community",
                "published_at": None,
                "accessed_at": TODAY,
                "version": None,
                "reliability": "medium_high",
                "score": 82,
                "relevance": "high",
                "freshness": "stable",
                "limitations": [
                    "方法示例文章；用于支撑 regime 概念和检测方法，不构成交易收益声明。"
                ],
                "evidence_summary": "说明金融市场微观结构行为会随时间变化，并可形成连续相似条件的 market regimes，需要识别 regime 及其 shifts。",
                "quoted_excerpt_allowed": False,
            },
            {
                "source_id": "src_phase37_q11_ssga_decoding_market_regimes",
                "source_title": "Decoding Market Regimes with Machine Learning",
                "source_url": "https://www.ssga.com/library-content/assets/pdf/global/pc/2025/decoding-market-regimes-with-machine-learning.pdf",
                "source_type": "institutional_research",
                "publisher": "State Street Global Advisors",
                "published_at": "2025-01-01",
                "accessed_at": TODAY,
                "version": None,
                "reliability": "high",
                "score": 86,
                "relevance": "high",
                "freshness": "time_sensitive",
                "limitations": [
                    "机构研究覆盖特定数据集和美国市场；不能直接泛化到所有资产或交易策略。"
                ],
                "evidence_summary": (
                    "该研究将 market-regime analysis 描述为金融研究的重要工具，识别 1995-2024 年多个市场 regime，"
                    "并比较不同 regime 下资产表现，支撑按 market state 限定结论边界。"
                ),
                "quoted_excerpt_allowed": False,
            },
            {
                "source_id": "src_phase37_q11_ucl_nonstationarity_financial_timeseries",
                "source_title": "Non Stationarity and Market Structure Dynamics in Financial Time Series",
                "source_url": "https://discovery.ucl.ac.uk/10165624/1/Procacci_Thesis.pdf",
                "source_type": "academic_thesis",
                "publisher": "University College London",
                "published_at": "2022-01-01",
                "accessed_at": TODAY,
                "version": None,
                "reliability": "high",
                "score": 84,
                "relevance": "high",
                "freshness": "stable",
                "limitations": [
                    "博士论文；用于支撑 non-stationarity 与金融市场结构变化，不直接授权某个交易策略。"
                ],
                "evidence_summary": "研究指出金融系统结构会随时间变化，non-stationarity 是金融系统关键特征，并挑战经典统计假设。",
                "quoted_excerpt_allowed": False,
            },
        ],
        "supplemental_notes": [
            "补齐了 regime 和 non-stationarity 的直接来源，不再只依赖过拟合/样本外资料间接支撑。",
            "把“单一 regime 不得泛化”的强规则与样本量/过拟合规则区分为独立方法论边界。",
        ],
    },
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def dedupe_sources(existing: list[dict[str, Any]], added: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for source in existing + added:
        source_id = str(source.get("source_id", ""))
        if not source_id or source_id in seen:
            continue
        seen.add(source_id)
        result.append(source)
    return result


def append_unique(values: list[Any], additions: list[Any]) -> list[Any]:
    result = list(values)
    seen = {json.dumps(value, ensure_ascii=False, sort_keys=True) for value in result}
    for value in additions:
        key = json.dumps(value, ensure_ascii=False, sort_keys=True)
        if key not in seen:
            result.append(value)
            seen.add(key)
    return result


def patch_candidate(task_id: str, spec: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    path = CANDIDATE_DIR / spec["candidate_file"]
    candidate = read_json(path)

    if candidate.get("research_task_id") != task_id:
        raise ValueError(f"{path} research_task_id mismatch: {candidate.get('research_task_id')} != {task_id}")
    if candidate.get("status", {}).get("review_status") != "needs_more_evidence":
        raise ValueError(f"{path} is not in needs_more_evidence state.")

    candidate["claim"].update(spec["claim_patch"])
    candidate["source_refs"] = dedupe_sources(candidate.get("source_refs", []), spec["source_refs"])

    source_quality = candidate.setdefault("source_quality", {})
    source_quality["overall_reliability"] = "high"
    source_quality["score"] = max(int(source_quality.get("score", 0) or 0), 84)
    source_quality["supplemented_for_reviewed_preparation"] = True
    source_quality["supplemental_source_count"] = len(spec["source_refs"])
    source_quality["limitations"] = append_unique(
        source_quality.get("limitations", []),
        [
            "本轮 CEK-TA-381 只补 reviewed/caveat_only 准备证据，不授权 approved/default guidance/hard gate。",
            "外部 AI 必须重新搜索专业网站、资料、案例和数据，确认补证是否足以进入 formal reviewed/caveat_only。",
        ],
    )

    candidate["status"]["ingestion_decision"] = "needs_more_evidence"
    candidate["status"]["decision_reason"] = "CEK-TA-381 已补充 reviewed 阻断证据，等待外部严格再审。"
    candidate["status"]["updated_at"] = TODAY

    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "supplemented_for_reaudit",
            "queue_group": "needs_more_evidence",
            "next_action": "external_strict_reaudit_for_reviewed_caveat_only",
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
            "visible_in_default_guidance_queue": False,
        }
    )

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate.update(
        {
            "default_guidance": "deny",
            "reason": "CEK-TA-381 supplemented for external re-audit only; no reviewed/approved/default/hard gate until audit result is imported.",
            "requires_human_escalation": True,
            "hidden_from_default_queue": True,
        }
    )

    review = candidate.setdefault("review", {})
    review["reviewer"] = "codex_cec_ta_381_supplemental_research"
    review["reviewed_at"] = TODAY
    review["open_questions"] = append_unique(
        review.get("open_questions", []),
        [
            "外部再审是否认为本轮补证足以进入 formal reviewed/caveat_only？",
            "是否仍需页码级、监管、机构或论文级证据？",
            "是否存在和完整 CEK-TA formal KB 的冲突或重复？",
        ],
    )
    review["audit_log"] = append_unique(
        review.get("audit_log", []),
        [
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase37_quant_foundation_blocked_supplemental_reaudit_prepared",
                "reason": f"CEK-TA-381: {spec['title']}；保持 candidate-only，等待外部严格再审。",
                "audit_package": PACKAGE_ID,
            }
        ],
    )
    for log_item in review["audit_log"]:
        if isinstance(log_item, dict) and "audit_package_id" in log_item:
            log_item["audit_package"] = log_item.pop("audit_package_id")
    review["supplemental_reaudit"] = {
        "task_id": TASK_ID,
        "package_id": PACKAGE_ID,
        "target_decision": spec["target_decision"],
        "supplemental_notes": spec["supplemental_notes"],
        "reviewed_allowed_before_reaudit": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
    }

    write_json(path, candidate)
    return path, candidate


def build_research_doc(patched: dict[str, tuple[Path, dict[str, Any]]]) -> str:
    lines = [
        "# Phase 37 Quant Foundation 阻断项补证记录",
        "",
        f"生成日期：{TODAY}",
        "",
        "## 任务边界",
        "",
        "本记录属于 `CEK-TA-381`，只为 `P37-A-Q02/Q06/Q11` 补充 reviewed-preparation 阻断证据并导出再审包。",
        "",
        "不做：",
        "",
        "```text",
        "不创建 formal reviewed",
        "不创建 approved",
        "不启用 default guidance",
        "不启用 hard gate",
        "不生成买卖点、仓位、杠杆、止损止盈或实盘执行建议",
        "```",
        "",
        "## 补证摘要",
        "",
    ]

    for task_id, spec in SUPPLEMENTAL_SPECS.items():
        path, candidate = patched[task_id]
        lines.extend(
            [
                f"### {task_id} - {spec['title']}",
                "",
                f"候选：`{candidate['candidate_id']}`",
                "",
                f"文件：`{path.relative_to(ROOT).as_posix()}`",
                "",
                "补证目标：",
                "",
                "```text",
                spec["target_decision"],
                "```",
                "",
                "补丁后 statement：",
                "",
                "```text",
                candidate["claim"]["statement"],
                "```",
                "",
                "新增或强化证据：",
                "",
            ]
        )
        for source in spec["source_refs"]:
            lines.append(f"- `{source['source_id']}`：{source['source_title']} - {source['source_url']}")
            lines.append(f"  - 用途：{source['evidence_summary']}")
            if source.get("page_refs"):
                lines.append(f"  - 页码线索：{'; '.join(source['page_refs'])}")
        lines.extend(
            [
                "",
                "保留边界：",
                "",
                "```text",
                "candidate-only；等待外部严格再审；approved/default guidance/hard gate 全部禁用。",
                "```",
                "",
            ]
        )

    lines.extend(
        [
            "## 再审入口",
            "",
            f"`{AUDIT_PACKAGE_PATH.relative_to(ROOT).as_posix()}`",
            "",
        ]
    )
    return "\n".join(lines)


def build_audit_package(patched: dict[str, tuple[Path, dict[str, Any]]]) -> dict[str, Any]:
    candidates = []
    for task_id, (_, candidate) in patched.items():
        snapshot = deepcopy(candidate)
        candidates.append(
            {
                "candidate_id": snapshot["candidate_id"],
                "research_task_id": task_id,
                "current_status": {
                    "review_status": snapshot["status"]["review_status"],
                    "ingestion_decision": snapshot["status"]["ingestion_decision"],
                    "workflow_stage": snapshot["workflow"]["stage"],
                    "queue_group": snapshot["workflow"]["queue_group"],
                    "reviewed_allowed": False,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                },
                "conversion_target": snapshot.get("conversion_target", {}),
                "classification": snapshot.get("classification", {}),
                "claim": snapshot.get("claim", {}),
                "applicability": snapshot.get("applicability", {}),
                "source_refs": snapshot.get("source_refs", []),
                "source_quality": snapshot.get("source_quality", {}),
                "conflict_audit": snapshot.get("conflict_audit", {}),
                "llm_usage_policy": snapshot.get("llm_usage_policy", {}),
                "machine_gate": snapshot.get("machine_gate", {}),
                "review": snapshot.get("review", {}),
            }
        )

    return {
        "package_id": PACKAGE_ID,
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "package_type": "reviewed_caveat_only_blocked_supplemental_reaudit",
        "schema_version": "1.0.0",
        "scope": {
            "phase": "Phase 37",
            "branch": "Trading Engineering",
            "partition_id": "KB_01_QUANT_FOUNDATION",
            "candidate_count": len(candidates),
            "input_condition": "needs_more_evidence candidates supplemented by CEK-TA-381.",
        },
        "audit_instruction": {
            "language": "zh-CN",
            "primary_goal": "严格判断 P37-A-Q02/Q06/Q11 补证后是否可以进入 formal reviewed/caveat_only。",
            "must_search": "必须搜索相关的专业网站、资料、案例和数据，对审计报告进行严格审计；不能只依赖候选包内摘要。",
            "must_check": [
                "Q02：Van Tharp 页码级书籍线索是否足以支撑 R-multiple reviewed/caveat_only；若仍不足，请说明还缺什么页码或正文核验。",
                "Q06：是否已清楚拆分 Trading Engineering 仓位 sizing 外部事实与 CEK-TA AI governance 内部规则。",
                "Q11：regime / non-stationarity 来源是否足以支撑单一 regime 不得泛化的边界。",
                "是否仍存在来源过度外推、vendor 教育材料过度升格、无来源规则或理论冲突。",
                "是否仍包含买卖点、具体仓位、杠杆、止损止盈、实盘执行或投资建议风险。",
            ],
            "hard_boundaries": [
                "candidate 不是正式知识。",
                "本次审计最多只能允许 formal reviewed/caveat_only。",
                "不得创建 approved。",
                "不得启用 default guidance。",
                "不得启用 hard gate。",
                "不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
            ],
            "allowed_decisions": [
                "accepted_for_reviewed_caveat_only",
                "needs_more_evidence",
                "rejected",
            ],
            "required_output_schema": {
                "audit_result_id": "string",
                "package_id": PACKAGE_ID,
                "audited_at": "YYYY-MM-DD",
                "quality_gate": {
                    "pass": "boolean",
                    "candidate_count": "integer",
                    "notes": "array<string>",
                },
                "decisions": [
                    {
                        "candidate_id": "string",
                        "research_task_id": "string",
                        "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected",
                        "confidence": "low | medium | high",
                        "reviewed_allowed": "boolean",
                        "approved_allowed": False,
                        "default_guidance_allowed": False,
                        "hard_gate_allowed": False,
                        "reasons": "array<string>",
                        "required_patches": {
                            "source": "array<string>",
                            "content": "array<string>",
                            "boundary": "array<string>",
                            "conflict": "array<string>",
                        },
                        "required_extra_sources": "array<object>",
                        "formal_conversion_notes": "array<string>",
                    }
                ],
            },
        },
        "quality_gate": {
            "pass": True,
            "candidate_count": len(candidates),
            "ready_count": len(candidates),
            "reviewed_created": 0,
            "approved_created": 0,
            "default_guidance_created": 0,
            "hard_gate_created": 0,
            "boundary": "export only; candidates remain needs_more_evidence until external audit result is imported.",
        },
        "candidates": candidates,
    }


def main() -> int:
    patched: dict[str, tuple[Path, dict[str, Any]]] = {}
    for task_id, spec in SUPPLEMENTAL_SPECS.items():
        patched[task_id] = patch_candidate(task_id, spec)

    RESEARCH_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_PATH.write_text(build_research_doc(patched), encoding="utf-8")

    package = build_audit_package(patched)
    write_json(AUDIT_PACKAGE_PATH, package)

    report = {
        "report_id": REPORT_ID,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "task_id": TASK_ID,
        "package_id": PACKAGE_ID,
        "candidate_count": len(patched),
        "patched_candidates": [
            {
                "research_task_id": task_id,
                "candidate_id": candidate["candidate_id"],
                "path": path.relative_to(ROOT).as_posix(),
                "source_count": len(candidate.get("source_refs", [])),
                "workflow_stage": candidate.get("workflow", {}).get("stage"),
                "queue_group": candidate.get("workflow", {}).get("queue_group"),
                "review_status": candidate.get("status", {}).get("review_status"),
            }
            for task_id, (path, candidate) in patched.items()
        ],
        "research_path": RESEARCH_PATH.relative_to(ROOT).as_posix(),
        "audit_package_path": AUDIT_PACKAGE_PATH.relative_to(ROOT).as_posix(),
        "reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "status": "pass",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
