# Phase 53 来源种子库

创建日期：2026-06-13

## 来源优先级

```text
A1: 官方监管、政府、标准组织、交易所、行业协议组织。
A2: 官方开源项目文档、研究机构、同行评议或广泛引用论文。
B1: 交易平台、broker、数据供应商官方文档。
B2: vendor 白皮书、行业博客、案例文章，仅作为 supporting source。
```

本 Phase 候选知识至少需要 2 个 A1/A2 来源；如果使用 B1/B2，必须标明只支持具体平台或实现示例。

## AI Engineering 来源

| source_id | source_type | authority | publisher | url | scope | supports | does_not_support |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P53-SRC-AI-001 | official_framework | A1 | NIST | https://www.nist.gov/itl/ai-risk-management-framework | AI 风险管理、GenAI 风险 profile | AI 生命周期风险治理、trustworthiness、设计/开发/使用/评估治理 | 不提供交易系统具体实现 |
| P53-SRC-AI-002 | security_standard | A2 | OWASP | https://owasp.org/www-project-top-10-for-large-language-model-applications/ | LLM 应用安全 | prompt injection、training data poisoning、supply chain、excessive agency、overreliance | 不提供交易领域监管结论 |
| P53-SRC-AI-003 | threat_knowledge_base | A2 | MITRE | https://atlas.mitre.org/ | AI 对抗技术和真实攻击观察 | adversarial AI threat taxonomy、攻击面建模 | 不定义 CEK-TA agent 权限 |
| P53-SRC-AI-004 | official_guidance | A1 | CISA | https://www.cisa.gov/topics/information-communications-technology-supply-chain-security/sbom | SBOM 基础 | 软件供应链透明度、依赖清单、风险归因 | 不直接覆盖模型权重和训练数据 |
| P53-SRC-AI-005 | official_guidance | A1 | CISA | https://www.cisa.gov/resources-tools/resources/software-bill-materials-ai-minimum-elements | AI SBOM | AI 系统组件、依赖、透明度和供应链记录 | 不证明某模型安全 |
| P53-SRC-AI-006 | research | A2 | Google Research | https://research.google/pubs/model-cards-for-model-reporting/ | 模型透明度 | intended use、limitations、evaluation conditions | 不替代 SBOM |
| P53-SRC-AI-007 | official_docs | A2 | OpenTelemetry | https://opentelemetry.io/docs/concepts/observability-primer/ | 可观测性 | logs、metrics、traces、系统外部可观测 | 不定义交易事件时钟合规 |

## Trading Engineering 来源

| source_id | source_type | authority | publisher | url | scope | supports | does_not_support |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P53-SRC-TR-001 | regulation | A1 | SEC | https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm | Market Access Rule | broker/dealer market access risk controls、naked access 风险 | 不适用于所有国家/资产 |
| P53-SRC-TR-002 | regulatory_guidance | A1 | SEC | https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions/divisionsmarketregfaq-0 | Rule 15c3-5 FAQ | 控制权、定期 review、风险管理程序 | 不给具体阈值 |
| P53-SRC-TR-003 | regulatory_report | A1 | FINRA | https://www.finra.org/rules-guidance/guidance/reports/2026-finra-annual-regulatory-oversight-report/manipulative-trading | Manipulative Trading | manipulative trading 监管关注、监控和合规 program | 不给法律裁决 |
| P53-SRC-TR-004 | rule | A1 | FINRA | https://www.finra.org/rules-guidance/rulebooks/finra-rules/6820 | CAT clock synchronization | business clocks、NIST atomic clock、drift、daily sync | 不适用于所有市场 |
| P53-SRC-TR-005 | regulation | A1 | ESMA | https://www.esma.europa.eu/publications-and-data/interactive-single-rulebook/mifid-ii/article-17-algorithmic-trading | MiFID II algorithmic trading | algorithmic trading controls、DEA、records、risk controls | 不替代美国 SEC/FINRA |
| P53-SRC-TR-006 | regulation | A1 | European Commission | https://ec.europa.eu/finance/securities/docs/isd/mifid/rts/160607-rts-25_en.pdf | RTS 25 clock synchronization | UTC、timestamp accuracy、clock sync requirements | 不覆盖美国 CAT 细节 |
| P53-SRC-TR-007 | official_guidance | A1 | CFTC | https://www.cftc.gov/LawRegulation/DoddFrankAct/Rulemakings/DF_24_DisruptiveTrading/index.htm | Disruptive Trading Practices | spoofing/disruptive practices regulatory context | 不替代 FINRA equity surveillance |
| P53-SRC-TR-008 | industry_standard | A2 | FIX Trading Community | https://fixtrading.org/standards/fix-algorithmic-trading-definition-language/ | FIXatdl | algo order interface、parameter semantics | 不证明 strategy alpha |
| P53-SRC-TR-009 | industry_guidance | A2 | FIA | https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf | Automated Trading Risk Controls | pre-trade controls、real-time monitoring、post-trade reporting | 不定义 CEK-TA 字段契约 |
| P53-SRC-TR-010 | official_plan | A1 | CAT NMS Plan | https://www.catnmsplan.com/guidance/clock-synchronization | CAT Clock Synchronization | clock certification、CAT clock requirements | 不覆盖 EU RTS 25 |
| P53-SRC-TR-011 | regulatory_report | A1 | FINRA | https://www.finra.org/rules-guidance/guidance/reports/2024-finra-annual-regulatory-oversight-report/manipulative-trading | Manipulative Trading / Momentum Ignition | 直接支撑 Momentum Ignition Trading 作为监控项目和 surveillance program 语境 | 不给法律裁决，不允许自动 hard gate |

## 来源使用边界

```text
1. SEC/FINRA 只直接支撑美国证券市场语境。
2. CFTC 只直接支撑 futures/swaps/commodities disruptive practice 语境。
3. ESMA/MiFID II 只直接支撑 EU investment firms、venues、DEA 和 algorithmic trading 语境。
4. CISA SBOM/AI SBOM 只支撑供应链透明度和清单契约，不证明组件安全。
5. OWASP/MITRE/NIST 只支撑 AI 安全威胁与治理，不证明交易策略有效。
6. OpenTelemetry 只支撑可观测性模型，不替代金融监管时间同步规则。
```
