{
  "report_id": "phase37_trade_analysis_candidate_generation",
  "generated_at": "2026-06-12",
  "task_id": "CEK-TA-442",
  "partition_id": "KB_07_TRADE_ANALYSIS",
  "candidate_count": 12,
  "candidate_dir": "E:\\collector\\rag\\codex-expert-kit\\rag\\candidates\\KB_07_TRADE_ANALYSIS",
  "quality_gate": {
    "gate_id": "phase37_trade_analysis_candidate_quality_gate",
    "checked_at": "2026-06-12",
    "phase": "37",
    "task_id": "CEK-TA-442",
    "candidate_count": 12,
    "expected_count": 12,
    "gate_status": "pass",
    "failures": [],
    "warnings": [
      "本批只是 Trade Analysis candidate，不得直接创建 reviewed、approved、default guidance 或 hard gate。",
      "Vendor journal sources 只能作为复盘工作流示例，不能单独支撑 reviewed 级字段本体。",
      "复盘发现只能进入 research hypothesis 或 label/eval 设计，不能直接变成实盘交易规则。"
    ]
  },
  "candidate_ids": [
    "cand_20260612_phase37_trade_analysis_planned_vs_realized_r_required_001",
    "cand_20260612_phase37_trade_analysis_mae_mfe_for_post_trade_only_001",
    "cand_20260612_phase37_trade_analysis_bad_trade_taxonomy_required_001",
    "cand_20260612_phase37_trade_analysis_good_loss_bad_win_distinction_001",
    "cand_20260612_phase37_trade_analysis_entry_quality_review_required_001",
    "cand_20260612_phase37_trade_analysis_exit_quality_review_required_001",
    "cand_20260612_phase37_trade_analysis_risk_quality_review_required_001",
    "cand_20260612_phase37_trade_analysis_execution_quality_review_required_001",
    "cand_20260612_phase37_trade_analysis_rule_compliance_review_required_001",
    "cand_20260612_phase37_trade_analysis_regime_fit_review_required_001",
    "cand_20260612_phase37_trade_analysis_reason_code_required_001",
    "cand_20260612_phase37_trade_analysis_research_hypothesis_requires_validation_001"
  ],
  "formal_knowledge_created": 0,
  "approved_created": 0,
  "default_guidance_enabled": 0,
  "hard_gate_enabled": 0,
  "next_action": "CEK-TA-443 export Trade Analysis candidate AI audit package."
}
