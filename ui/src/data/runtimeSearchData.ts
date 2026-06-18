import type { SearchTestCase } from '../types'

export const runtimeSearchCases: SearchTestCase[] = [
  {
    test_id: 'phase20_runtime_ohlc_same_bar',
    request_id: 'seed_runtime_002',
    query: 'OHLC same bar take profit stop loss fill model',
    task_type: 'backtest_review',
    filters: {
      domain: 'backtest',
      tree_node_id: 'kt.backtest.bias',
      canonical_node_id: 'kt.trading_engineering.backtest.fill_assumption',
      canonical_tree_path_prefix: 'CEK-TA / Trading Engineering / Backtest'
    },
    status: 'pass',
    runtime_status: 'ok',
    warnings: [],
    audit: {
      retrieval_policy_version: '0.1.0',
      result_count: 5,
      blocked_count: 0,
      returned_review_statuses: ['approved'],
      returned_conflict_statuses: ['none']
    },
    matches: [
      {
        item_id: 'kb_04_backtest.fill_model.ohlc_same_bar_path_ambiguity.v1',
        title: '只用 OHLC K线不能确定同一根 bar 内止盈止损的真实先后顺序',
        claim: '当仅有 OHLC K线数据时，如果同一根 bar 同时触及止盈和止损，回测系统不能声称知道真实先后顺序。',
        tree_node_id: 'kt.backtest.bias',
        tree_path: 'CEK-TA / Trading Engineering / Backtest / Bias',
        canonical_node_id: 'kt.trading_engineering.backtest.fill_assumption',
        canonical_tree_path: 'CEK-TA / Trading Engineering / Backtest / Fill Assumption',
        domain: 'backtest',
        source_count: 2,
        confidence: 'high',
        freshness: 'stable',
        review_status: 'approved',
        conflict_status: 'none',
        score: 0.7,
        recommended_next_action: 'use_as_guidance',
        why_matched: {
          score: 0.7,
          reasons: ['lexical_token_overlap', 'metadata_scope_boost_available']
        }
      }
    ],
    blocked_results: []
  },
  {
    test_id: 'phase20_runtime_kill_switch_warning',
    request_id: 'seed_runtime_004',
    query: 'live trading kill switch no new orders',
    task_type: 'live_trading',
    filters: {
      domain: 'live_trading',
      tree_node_id: 'kt.live_execution.risk_control',
      canonical_node_id: 'kt.trading_engineering.risk_management.kill_switch'
    },
    status: 'warning',
    runtime_status: 'warning',
    warnings: ['kb_06_live_execution.risk_control.kill_switch_no_new_orders.v1 is time_sensitive for live_trading.'],
    audit: {
      retrieval_policy_version: '0.1.0',
      result_count: 5,
      blocked_count: 0,
      returned_review_statuses: ['approved'],
      returned_conflict_statuses: ['none']
    },
    matches: [
      {
        item_id: 'kb_06_live_execution.risk_control.kill_switch_no_new_orders.v1',
        title: '实盘 kill switch 触发后默认禁止新开仓',
        claim: '实盘 kill switch 触发后，系统默认必须禁止新开仓，并进入保护状态。',
        tree_node_id: 'kt.live_execution.risk_control',
        tree_path: 'CEK-TA / Trading Engineering / Live Execution / Risk Control',
        canonical_node_id: 'kt.trading_engineering.risk_management.kill_switch',
        canonical_tree_path: 'CEK-TA / Trading Engineering / Risk Management / Kill Switch',
        domain: 'live_trading',
        source_count: 2,
        confidence: 'high',
        freshness: 'time_sensitive',
        review_status: 'approved',
        conflict_status: 'none',
        score: 0.8333,
        recommended_next_action: 'use_as_guidance',
        why_matched: {
          score: 0.8333,
          reasons: ['lexical_token_overlap', 'metadata_scope_boost_available']
        }
      }
    ],
    blocked_results: []
  },
  {
    test_id: 'phase20_runtime_unsourced_blocked',
    request_id: 'phase20_blocked_results',
    query: 'phase20 unsourced blocking fixture',
    task_type: 'rag_engineering',
    filters: {
      domain: 'rag_engineering',
      canonical_node_id: 'kt.ai_engineering.rag_engineering.source_quality'
    },
    status: 'pass',
    runtime_status: 'ok',
    warnings: [],
    audit: {
      retrieval_policy_version: '0.1.0',
      result_count: 0,
      blocked_count: 1,
      returned_review_statuses: [],
      returned_conflict_statuses: []
    },
    matches: [],
    blocked_results: [
      {
        item_id: 'kb_test.phase20.unsourced.v1',
        knowledge_id: 'kb_test.phase20.unsourced.v1',
        title: 'Phase 20 unsourced blocking fixture',
        blocked_reason: 'missing_source_evidence',
        review_status: 'approved',
        conflict_status: 'none',
        freshness: 'stable',
        has_source_refs: false,
        tree_node_id: 'kt.rag_engineering.source_quality',
        canonical_node_id: 'kt.ai_engineering.rag_engineering.source_quality',
        recommended_fix: 'add_source_evidence_before_default_guidance'
      }
    ]
  }
]
