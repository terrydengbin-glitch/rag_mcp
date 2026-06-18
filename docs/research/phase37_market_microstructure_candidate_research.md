# Phase 37 Market Microstructure 候选知识采集记录

生成日期：2026-06-11

## 范围

本批覆盖 Phase 37 D 组 Market Microstructure 12 条 P0 候选知识。候选只做审计准备，不创建 formal reviewed，不进入 approved/default/hard gate。

## 来源原则

- 优先使用 CFA Institute、SEC/ESMA/ECB 等专业机构或监管来源、交易所/API 官方文档、数据供应商字段级文档和学术论文。
- 供应商、平台和教育资料只作为 supporting evidence，不单独证明交易优势。
- 微观结构特征必须声明数据源、交易所、市场、时间戳、粒度、执行和 regime 边界。

## 采集结果

- 候选数量：12
- 质量门禁：pass
- 最少来源数：4

### P37-D-M01 价差信号必须声明流动性上下文

- candidate_id: `cand_20260611_phase37_market_microstructure_spread_liquidity_context_required_001`
- normalized_claim: `microstructure.spread_liquidity_context_required.v1`
- tree_node_id: `kt.market_microstructure`
- 来源数：4
- statement: Bid-ask spread、盘口价差或价差收窄/扩大信号，必须同时声明市场、品种、交易时段、数据源、成交量和流动性状态；不得把单一价差变化解释为通用交易方向。

主要来源：
- Trading Costs and Electronic Markets：https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets
- Trade Strategy and Execution：https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution
- Gauging the interplay between market liquidity and funding liquidity：https://www.ecb.europa.eu/press/financial-stability-publications/fsr/special/html/ecb.fsrart202305_01~830184261b.en.html
- Nasdaq TotalView：https://www.nasdaq.com/solutions/data/equities/nasdaq-totalview

### P37-D-M02 盘口深度必须声明 L2/L3 和可见性边界

- candidate_id: `cand_20260611_phase37_market_microstructure_order_book_depth_boundary_001`
- normalized_claim: `microstructure.order_book_depth_boundary.v1`
- tree_node_id: `kt.market_microstructure`
- 来源数：4
- statement: Order book depth 只能描述可见订单簿的深度和变动，必须声明是 L2 aggregate depth、L3 market-by-order、top-of-book 还是完整深度；不得把可见深度等同于全部市场流动性。

主要来源：
- Market by order (MBO)：https://databento.com/docs/schemas-and-data-formats/mbo
- Market by price (MBP-10)：https://databento.com/docs/schemas-and-data-formats/mbp-10
- Nasdaq TotalView：https://www.nasdaq.com/solutions/data/equities/nasdaq-totalview
- Nasdaq TotalView-ITCH 5.0 specification：https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification.pdf

### P37-D-M03 逐笔成交 aggressor 方向必须保留数据源语义

- candidate_id: `cand_20260611_phase37_market_microstructure_trade_prints_aggressor_caveat_001`
- normalized_claim: `microstructure.trade_prints_aggressor_caveat.v1`
- tree_node_id: `kt.market_microstructure`
- 来源数：4
- statement: Trade prints 的买卖主动方、bid/ask hit 或 aggressor side 必须按数据源字段定义解释；缺失、推断或 venue 规则不一致时，不能把 trade side 当成确定订单流事实。

主要来源：
- Trades schema：https://databento.com/docs/schemas-and-data-formats/trades
- Nasdaq TotalView-ITCH 5.0 specification：https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification.pdf
- Market by order (MBO)：https://databento.com/docs/schemas-and-data-formats/mbo
- Trading Costs and Electronic Markets：https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets

### P37-D-M04 订单流代理指标不能替代真实订单簿事实

- candidate_id: `cand_20260611_phase37_market_microstructure_order_flow_proxy_boundary_001`
- normalized_claim: `microstructure.order_flow_proxy_boundary.v1`
- tree_node_id: `kt.market_microstructure.order_flow`
- 来源数：4
- statement: Order flow proxy、imbalance、signed volume 或 OFI 类指标必须声明输入数据、采样窗口、方向推断和归一化方式；代理指标不能替代真实订单、取消、修改和成交事件事实。

主要来源：
- Market by order (MBO)：https://databento.com/docs/schemas-and-data-formats/mbo
- Market by price (MBP-10)：https://databento.com/docs/schemas-and-data-formats/mbp-10
- Trades schema：https://databento.com/docs/schemas-and-data-formats/trades
- Trading Costs and Electronic Markets：https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets

### P37-D-M05 CVD 只能作为订单流代理，不能单独定义趋势结论

- candidate_id: `cand_20260611_phase37_market_microstructure_cvd_interpretation_caveat_001`
- normalized_claim: `microstructure.cvd_interpretation_caveat.v1`
- tree_node_id: `kt.market_microstructure.order_flow`
- 来源数：4
- statement: Cumulative Volume Delta 或 Volume Delta 只能作为指定数据源和采样规则下的订单流代理；CVD 背离、上升或下降不得单独证明趋势、反转或交易优势。

主要来源：
- Volume Delta：https://www.overcharts.com/en/helpcenter/docs/volume-delta/
- Trades schema：https://databento.com/docs/schemas-and-data-formats/trades
- Market by order (MBO)：https://databento.com/docs/schemas-and-data-formats/mbo
- Trade Strategy and Execution：https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution

### P37-D-M06 资金费率和持仓量必须声明衍生品上下文

- candidate_id: `cand_20260611_phase37_market_microstructure_funding_open_interest_context_required_001`
- normalized_claim: `microstructure.funding_open_interest_context_required.v1`
- tree_node_id: `kt.market_microstructure`
- 来源数：4
- statement: Funding rate、open interest、合约持仓量和永续合约定位指标必须声明交易所、合约类型、时间戳、结算机制和样本范围；不得把单所资金费率或 OI 当成全市场方向事实。

主要来源：
- Get Funding Rate History：https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History
- Open Interest：https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Open-Interest
- Market Liquidity and Funding Liquidity：https://www.nber.org/system/files/working_papers/w12939/w12939.pdf
- Gauging the interplay between market liquidity and funding liquidity：https://www.ecb.europa.eu/press/financial-stability-publications/fsr/special/html/ecb.fsrart202305_01~830184261b.en.html

### P37-D-M07 流动性状态必须按 regime 标注

- candidate_id: `cand_20260611_phase37_market_microstructure_liquidity_regime_required_001`
- normalized_claim: `microstructure.liquidity_regime_required.v1`
- tree_node_id: `kt.market_microstructure`
- 来源数：4
- statement: Microstructure 特征必须区分 normal、thin、stressed、event-driven、rollover 或 session-specific liquidity regime；不得把正常时段的盘口特征直接外推到压力、休市前后或低流动性时段。

主要来源：
- Gauging the interplay between market liquidity and funding liquidity：https://www.ecb.europa.eu/press/financial-stability-publications/fsr/special/html/ecb.fsrart202305_01~830184261b.en.html
- Market Liquidity and Funding Liquidity：https://www.nber.org/system/files/working_papers/w12939/w12939.pdf
- Trade Strategy and Execution：https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution
- Trading Costs and Electronic Markets：https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets

### P37-D-M08 市场影响成本必须进入微观结构解释边界

- candidate_id: `cand_20260611_phase37_market_microstructure_market_impact_cost_required_001`
- normalized_claim: `microstructure.market_impact_cost_required.v1`
- tree_node_id: `kt.market_microstructure`
- 来源数：4
- statement: 使用盘口深度、订单流或短周期信号评估交易候选时，必须考虑订单规模、执行速度、流动性、临时/永久市场影响和机会成本；不得只看理论信号而忽略执行带来的价格冲击。

主要来源：
- Optimal Liquidation：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=53501
- Trading Costs and Electronic Markets：https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets
- Trade Strategy and Execution：https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution
- Gauging the interplay between market liquidity and funding liquidity：https://www.ecb.europa.eu/press/financial-stability-publications/fsr/special/html/ecb.fsrart202305_01~830184261b.en.html

### P37-D-M09 高频微观结构信号必须声明延迟和时钟同步边界

- candidate_id: `cand_20260611_phase37_market_microstructure_high_frequency_signal_latency_boundary_001`
- normalized_claim: `microstructure.high_frequency_signal_latency_boundary.v1`
- tree_node_id: `kt.market_microstructure`
- 来源数：4
- statement: 高频盘口、成交、订单流和微观结构信号必须声明数据延迟、处理延迟、时钟同步、事件顺序和可执行窗口；无法证明时间一致性时，不能用于声称实时交易优势。

主要来源：
- Commission Delegated Regulation RTS 25 clock synchronisation：https://ec.europa.eu/finance/securities/docs/isd/mifid/rts/160607-rts-25_en.pdf
- Trading Costs and Electronic Markets：https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets
- Market by order (MBO)：https://databento.com/docs/schemas-and-data-formats/mbo
- Nasdaq TotalView-ITCH 5.0 specification：https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification.pdf

### P37-D-M10 滑点必须按流动性和执行 regime 建模

- candidate_id: `cand_20260611_phase37_market_microstructure_slippage_regime_caveat_001`
- normalized_claim: `microstructure.slippage_regime_caveat.v1`
- tree_node_id: `kt.market_microstructure`
- 来源数：4
- statement: Slippage 不应使用固定常数覆盖所有品种、时段和订单类型；微观结构相关滑点必须按流动性、价差、深度、订单规模、波动、延迟和执行方式分层建模或审计。

主要来源：
- Trading Costs and Electronic Markets：https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets
- Trade Strategy and Execution：https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution
- Optimal Liquidation：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=53501
- Gauging the interplay between market liquidity and funding liquidity：https://www.ecb.europa.eu/press/financial-stability-publications/fsr/special/html/ecb.fsrart202305_01~830184261b.en.html

### P37-D-M11 薄市场执行风险必须显式阻断或降级

- candidate_id: `cand_20260611_phase37_market_microstructure_thin_market_execution_risk_001`
- normalized_claim: `microstructure.thin_market_execution_risk.v1`
- tree_node_id: `kt.market_microstructure`
- 来源数：4
- statement: 在薄市场、低深度、宽价差、事件冲击或流动性枯竭场景下，微观结构信号必须降级为风险提示或要求人工/风控复核；不能把正常市场假设沿用到 thin market 执行。

主要来源：
- Gauging the interplay between market liquidity and funding liquidity：https://www.ecb.europa.eu/press/financial-stability-publications/fsr/special/html/ecb.fsrart202305_01~830184261b.en.html
- Market Liquidity and Funding Liquidity：https://www.nber.org/system/files/working_papers/w12939/w12939.pdf
- Trade Strategy and Execution：https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution
- Responses to Frequently Asked Questions Concerning Risk Management Controls for Brokers or Dealers with Market Access：https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions/divisionsmarketregfaq-0

### P37-D-M12 微观结构特征不得跨市场无条件泛化

- candidate_id: `cand_20260611_phase37_market_microstructure_microstructure_feature_not_universal_001`
- normalized_claim: `microstructure.microstructure_feature_not_universal.v1`
- tree_node_id: `kt.market_microstructure`
- 来源数：5
- statement: 盘口、订单流、CVD、funding、OI、深度、滑点和市场影响特征不能跨资产、交易所、数据源、交易时段和 market regime 无条件泛化；每个特征必须声明适用市场、数据契约和验证范围。

主要来源：
- Market by order (MBO)：https://databento.com/docs/schemas-and-data-formats/mbo
- Get Funding Rate History：https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History
- Trading Costs and Electronic Markets：https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets
- Optimal Liquidation：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=53501
- Commission Delegated Regulation RTS 25 clock synchronisation：https://ec.europa.eu/finance/securities/docs/isd/mifid/rts/160607-rts-25_en.pdf
