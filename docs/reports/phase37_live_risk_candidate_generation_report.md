{
  "report_id": "phase37_live_risk_candidate_generation",
  "generated_at": "2026-06-12",
  "task_id": "CEK-TA-435",
  "candidate_count": 12,
  "candidate_dirs": [
    "E:\\collector\\rag\\codex-expert-kit\\rag\\candidates\\KB_06_LIVE_EXECUTION",
    "E:\\collector\\rag\\codex-expert-kit\\rag\\candidates\\KB_07_RISK_MANAGEMENT"
  ],
  "quality_gate": {
    "gate_id": "phase37_live_risk_candidate_quality_gate",
    "checked_at": "2026-06-12",
    "phase": "37",
    "task_id": "CEK-TA-435",
    "candidate_count": 12,
    "expected_count": 12,
    "live_execution_count": 6,
    "risk_management_count": 6,
    "gate_status": "pass",
    "failures": [],
    "warnings": [
      "本批只是 Live Execution / Risk Management candidate，不得直接创建 reviewed、approved、default guidance 或 hard gate。",
      "风险阈值必须由外接项目 owner 按账户、市场、品种、策略和监管环境设定，本知识库不提供阈值数值建议。"
    ]
  },
  "candidate_ids": [
    "cand_20260612_phase37_live_risk_least_privilege_api_required_001",
    "cand_20260612_phase37_live_risk_order_state_machine_required_001",
    "cand_20260612_phase37_live_risk_position_reconciliation_required_001",
    "cand_20260612_phase37_live_risk_kill_switch_required_001",
    "cand_20260612_phase37_live_risk_exchange_adapter_error_contract_required_001",
    "cand_20260612_phase37_live_risk_order_fill_trade_log_required_001",
    "cand_20260612_phase37_live_risk_single_trade_risk_limit_required_001",
    "cand_20260612_phase37_live_risk_daily_loss_limit_required_001",
    "cand_20260612_phase37_live_risk_max_open_positions_required_001",
    "cand_20260612_phase37_live_risk_portfolio_exposure_limit_required_001",
    "cand_20260612_phase37_live_risk_consecutive_loss_stop_required_001",
    "cand_20260612_phase37_live_risk_hard_risk_gate_precedes_execution_001"
  ],
  "formal_knowledge_created": 0,
  "approved_created": 0,
  "default_guidance_enabled": 0,
  "hard_gate_enabled": 0,
  "next_action": "CEK-TA-436 export Live Execution / Risk Management candidate AI audit package."
}
