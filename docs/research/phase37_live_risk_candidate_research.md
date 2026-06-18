# Phase 37 Live Execution / Risk Management Candidate Research

- generated_at: 2026-06-12
- task_id: CEK-TA-435
- candidate_count: 12
- live_execution_count: 6
- risk_management_count: 6
- gate_status: pass

## 来源种子

- `nist_least_privilege`: Least Privilege - NIST CSRC Glossary (NIST CSRC) - https://csrc.nist.gov/glossary/term/least_privilege
- `ibkr_api`: TWS API Documentation (Interactive Brokers) - https://www.interactivebrokers.com/campus/ibkr-api-page/trader-workstation-api/
- `ibkr_positions`: TWS API Positions (Interactive Brokers) - https://interactivebrokers.github.io/tws-api/positions.html
- `ibkr_orders`: Placing Orders using TWS Python API (Interactive Brokers) - https://www.interactivebrokers.com/campus/trading-lessons/python-placing-orders/
- `fix_execution_report`: Execution Report <8> message - FIX 4.4 (OnixS FIX Dictionary) - https://www.onixs.biz/fix-dictionary/4.4/msgtype_8_8.html
- `fix_ordstatus`: OrdStatus <39> field - FIX 4.4 (OnixS FIX Dictionary) - https://www.onixs.biz/fix-dictionary/4.4/tagnum_39.html
- `binance_filters`: Filters (Binance Open Platform) - https://developers.binance.com/docs/binance-spot-api-docs/filters
- `sec_market_access`: Rule 15c3-5 Risk Management Controls for Brokers or Dealers with Market Access (SEC) - https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm
- `cftc_risk_program`: 17 CFR 1.11 Risk Management Program (eCFR / CFTC) - https://www.ecfr.gov/current/title-17/chapter-I/part-1/subject-group-ECFR812208927193be3/section-1.11
- `cme_pretrade`: Pre-Trade Risk Management (CME Group) - https://www.cmegroup.com/solutions/market-access/globex/trade-on-globex/pre-trade-risk-management.html
- `cme_kill_switch`: Enforcing Kill Switch (CME Group) - https://www.cmegroup.com/tools-information/webhelp/globex-credit-controls/Content/KS_Detail.html
- `cme_audit_trail`: Audit Trail - CME Group Risk Management (CME Group) - https://www.cmegroup.com/tools-information/webhelp/brokertec-risk-management/Content/audit-trail.html
- `fia_risk_controls`: Best Practices for Automated Trading Risk Controls and System Safeguards (FIA) - https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf
- `quantconnect_risk`: Risk Management - Key Concepts (QuantConnect) - https://www.quantconnect.com/docs/v2/writing-algorithms/algorithm-framework/risk-management/key-concepts

## 候选知识点

- `P37-G-L01` / `live_trading.least_privilege_api_required.v1`: 实盘 API key、broker session 和交易权限必须按最小权限配置；只读、下单、撤单、资金划转、账户管理和管理端权限必须分离，不能用全权限密钥运行交易机器人。
- `P37-G-L02` / `live_trading.order_state_machine_required.v1`: 实盘执行必须维护订单状态机，覆盖 submitted、accepted、partially_filled、filled、cancel_pending、canceled、rejected、expired、unknown 和 reconciliation_required 等状态及合法迁移。
- `P37-G-L03` / `live_trading.position_reconciliation_required.v1`: 实盘系统必须把本地订单/成交/仓位与 broker、exchange、account statement 或 clearing source 对账；发现差异时必须进入 reconciliation_required，而不是继续按本地状态下单。
- `P37-G-L04` / `live_trading.kill_switch_required.v1`: 实盘系统必须定义 kill switch、order-entry block、cancel working orders、manual override 和恢复流程；kill switch 触发不能等同于策略判断，只能作为执行安全控制。
- `P37-G-L05` / `live_trading.exchange_adapter_error_contract_required.v1`: 交易所或 broker adapter 必须把网络错误、认证错误、限频、风控拒单、参数非法、状态未知、成交回报缺失和服务降级映射为结构化错误，不能用字符串异常驱动实盘决策。
- `P37-G-L06` / `live_trading.order_fill_trade_log_required.v1`: 实盘执行必须保存订单请求、broker 回报、成交、拒单、撤单、费用、滑点、状态迁移、风险触发和人工操作日志，并能回放到每个交易决策和执行事件。
- `P37-G-L07` / `risk_management.single_trade_risk_limit_required.v1`: 交易系统必须在下单前检查单笔风险、订单名义金额、最大数量、价格偏离和账户可承受损失；超过策略或账户限额的订单不能进入执行适配器。
- `P37-G-L08` / `risk_management.daily_loss_limit_required.v1`: 交易系统必须定义日内 realized/unrealized loss 口径、重置时区、触发阈值、冻结动作和人工恢复流程；达到日亏损限制后不能继续按普通信号自动下单。
- `P37-G-L09` / `risk_management.max_open_positions_required.v1`: 交易系统必须检查最大持仓数、未完成订单数、同向/反向重复订单和账户级未结风险；超过限额时必须阻止新的自动开仓请求。
- `P37-G-L10` / `risk_management.portfolio_exposure_limit_required.v1`: 风险管理必须定义账户、策略、品种、相关资产、行业或方向暴露上限；组合暴露检查应在下单前执行，且不能被单个信号或 AI scoring 绕过。
- `P37-G-L11` / `risk_management.consecutive_loss_stop_required.v1`: 交易系统若使用连续亏损停止规则，必须定义亏损事件口径、时间窗口、重置条件、冻结动作和人工复核流程；该规则不能替代单笔风险、日亏损或组合暴露限制。
- `P37-G-L12` / `risk_management.hard_risk_gate_precedes_execution.v1`: 任何 AI scoring、策略信号或人工队列都不能绕过 deterministic hard risk gate；最终下单前必须经过权限、订单约束、风险限额、账户状态、市场状态和 kill-switch 状态检查。

## 边界

- 本批候选只处理实盘执行和风控规则本体，不处理回测、回放、AI 训练、RAG/MCP 或项目私有策略参数。
- 候选不得直接进入 reviewed、approved、default guidance 或 hard gate。
- 风险阈值、账户配置、交易所配置和密钥权限必须由外接项目 owner 自行定义并审计。
