# Phase 37 Backtest 候选知识研究记录

生成日期：2026-06-11

## 范围

本批只覆盖 Trading Engineering / Backtest P0 的 12 条候选知识。所有条目均为候选，不是正式 reviewed，不是 approved，不进入默认指导，也不形成 hard gate。

## 来源矩阵

### cfa_backtesting

- 标题：Backtesting & Simulation
- 链接：https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/backtesting-and-simulation
- 类型：professional_curriculum
- 发布方：CFA Institute
- 证据作用：CFA Institute frames backtesting as approximating the real-life investment process, including rolling-window processes, rules, portfolio formation, rebalancing, performance and risk profiles.
- 使用边界：Professional curriculum source; use for process and boundary, not for a specific trading edge.

### cfa_trade_strategy

- 标题：Trade Strategy and Execution
- 链接：https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution
- 类型：professional_curriculum
- 发布方：CFA Institute
- 证据作用：CFA Institute frames execution around liquidity needs, market conditions, execution risk, opportunity cost, market impact and trade cost analysis.
- 使用边界：Supports cost and execution boundary; not a backtest platform contract.

### white_reality_check

- 标题：A Reality Check for Data Snooping
- 链接：https://www.ssc.wisc.edu/~bhansen/718/White2000.pdf
- 类型：academic_paper
- 发布方：Econometrica
- 证据作用：White formalizes data snooping risk when data is reused for inference or model selection, where apparently good results may arise by chance.
- 使用边界：Academic inference source; does not provide a platform implementation.

### sullivan_white

- 标题：Data-Snooping, Technical Trading Rule Performance, and the Bootstrap
- 链接：https://www.jstor.org/stable/222451
- 类型：academic_paper
- 发布方：Journal of Finance
- 证据作用：Sullivan, Timmermann and White apply bootstrap methods to technical trading rules and data-snooping bias.
- 使用边界：JSTOR landing page/source metadata; page-level access may require subscription.

### bailey_dsr

- 标题：The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality
- 链接：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551
- 类型：academic_paper
- 发布方：SSRN / Journal of Portfolio Management
- 证据作用：The Deflated Sharpe Ratio corrects for selection bias under multiple testing and non-normal returns, addressing inflated backtest performance.
- 使用边界：Supports overfitting/selection-bias metrics; not a standalone approval rule.

### bailey_pbo

- 标题：The Probability of Backtest Overfitting
- 链接：https://www.davidhbailey.com/dhbpapers/backtest-overfitting.pdf
- 类型：academic_paper
- 发布方：SSRN / Journal of Computational Finance
- 证据作用：Bailey et al. propose Probability of Backtest Overfitting and cross-validation methods for strategy selection risk.
- 使用边界：Academic metric source; not an execution or production readiness rule.

### quantconnect_fills

- 标题：Trade Fills - Key Concepts
- 链接：https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts
- 类型：platform_doc
- 发布方：QuantConnect
- 证据作用：QuantConnect explains fill models, spread costs and interaction with slippage models for backtest order fills.
- 使用边界：Platform-specific semantics; external projects must map their own fill model.

### quantconnect_slippage

- 标题：Slippage Models - Key Concepts
- 链接：https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/slippage/key-concepts
- 类型：platform_doc
- 发布方：QuantConnect
- 证据作用：QuantConnect defines slippage as the difference between expected and actual fill price and models it for more realistic backtests.
- 使用边界：Platform-specific; supports slippage concept and modeling boundary.

### quantconnect_fees

- 标题：Transaction Fees - Key Concepts
- 链接：https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/transaction-fees/key-concepts
- 类型：platform_doc
- 发布方：QuantConnect
- 证据作用：QuantConnect fee models simulate brokerage transaction fees to make backtest results more realistic.
- 使用边界：Platform-specific; external projects must map actual brokerage/exchange fees.

### quantconnect_report

- 标题：Backtesting Report
- 链接：https://www.quantconnect.com/docs/v2/cloud-platform/backtesting/report
- 类型：platform_doc
- 发布方：QuantConnect
- 证据作用：QuantConnect backtest reports show return distributions, cumulative returns, summary and risk information.
- 使用边界：Report fields are platform-specific; use as example of metric context, not universal schema.

### mlflow_tracking

- 标题：MLflow Tracking
- 链接：https://mlflow.org/docs/latest/tracking.html
- 类型：framework_doc
- 发布方：MLflow
- 证据作用：MLflow Tracking records parameters, metrics, artifacts and source/version metadata for reproducible experiments.
- 使用边界：Framework implementation example; not mandatory for CEK-TA.

### dvc_pipelines

- 标题：DVC Pipelines
- 链接：https://dvc.org/doc/user-guide/pipelines
- 类型：framework_doc
- 发布方：DVC
- 证据作用：DVC pipelines define stages, dependencies, outputs and reproducible data workflows.
- 使用边界：Framework implementation example; not mandatory for CEK-TA.

## 候选清单

- `P37-E-B01` / `backtest.lookahead_bias_block.v1`：Lookahead bias 必须阻断
- `P37-E-B02` / `backtest.data_leakage_block.v1`：数据泄漏必须阻断
- `P37-E-B03` / `backtest.survivorship_selection_bias_check.v1`：必须检查幸存者偏差和选择偏差
- `P37-E-B04` / `backtest.parameter_search_separate_from_final_eval.v1`：参数搜索必须与最终评估分离
- `P37-E-B05` / `backtest.walk_forward_validation_required.v1`：Walk-forward 验证必须声明窗口和重训练规则
- `P37-E-B06` / `backtest.out_of_sample_required.v1`：样本外评估必须存在
- `P37-E-B07` / `backtest.cost_model_required.v1`：回测必须显式声明成本模型
- `P37-E-B08` / `backtest.slippage_fee_spread_required.v1`：滑点、手续费和价差必须纳入或声明缺失
- `P37-E-B09` / `backtest.metric_interpretation_boundary.v1`：回测指标必须带解释边界
- `P37-E-B10` / `backtest.profit_factor_drawdown_context_required.v1`：Profit factor 必须结合回撤和样本语境
- `P37-E-B11` / `backtest.reproducibility_package_required.v1`：回测必须具备可复现实验包
- `P37-E-B12` / `backtest.strategy_version_and_data_version_required.v1`：策略版本和数据版本必须绑定
