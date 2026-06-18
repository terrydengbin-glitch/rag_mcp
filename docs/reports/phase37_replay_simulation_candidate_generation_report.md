{
  "report_id": "phase37_replay_simulation_candidate_generation",
  "generated_at": "2026-06-11",
  "task_id": "CEK-TA-424",
  "partition_id": "KB_05_REPLAY_SIMULATION",
  "candidate_count": 12,
  "candidate_dir": "E:\\collector\\rag\\codex-expert-kit\\rag\\candidates\\KB_05_REPLAY_SIMULATION",
  "quality_gate": {
    "gate_id": "phase37_replay_simulation_candidate_quality_gate",
    "checked_at": "2026-06-11",
    "phase": "37",
    "task_id": "CEK-TA-424",
    "candidate_count": 12,
    "expected_count": 12,
    "gate_status": "pass",
    "failures": [],
    "warnings": [
      "本批只是 Replay / Simulation candidate，不得直接创建 reviewed、approved、default guidance 或 hard gate。",
      "成交模型、延迟模型和交易所规则必须按市场/交易所/品种映射，不得泛化为统一实盘真理。"
    ]
  },
  "candidate_ids": [
    "cand_20260611_phase37_replay_simulation_event_clock_required_001",
    "cand_20260611_phase37_replay_simulation_ohlc_same_bar_tp_sl_ordering_required_001",
    "cand_20260611_phase37_replay_simulation_fill_model_assumption_required_001",
    "cand_20260611_phase37_replay_simulation_partial_fill_policy_required_001",
    "cand_20260611_phase37_replay_simulation_latency_model_required_001",
    "cand_20260611_phase37_replay_simulation_paper_trading_not_equal_live_001",
    "cand_20260611_phase37_replay_simulation_exchange_rule_simulation_required_001",
    "cand_20260611_phase37_replay_simulation_minimum_order_size_required_001",
    "cand_20260611_phase37_replay_simulation_order_reject_and_cancel_policy_required_001",
    "cand_20260611_phase37_replay_simulation_simulation_live_gap_report_required_001",
    "cand_20260611_phase37_replay_simulation_tick_replay_vs_ohlc_boundary_001",
    "cand_20260611_phase37_replay_simulation_execution_cost_consistency_required_001"
  ]
}
