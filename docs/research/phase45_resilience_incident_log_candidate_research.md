# Phase 45 Resilience / Incident / Log 候选知识采集记录

## 范围

本批次对应 CEK-TA-463 / P45-D，目标是采集 6 条系统韧性、事故响应、恢复/replay 和日志治理 P1 候选知识。

本批次只生成候选和审计包，不创建 reviewed、approved、default guidance 或 hard gate。

## 来源记录

| source_key | 来源 | 类型 | URL | 用途 |
| --- | --- | --- | --- | --- |
| `ecfr_reg_sci` | 17 CFR Part 242 Regulation SCI | `regulatory_rule` | https://www.ecfr.gov/current/title-17/chapter-II/part-242/subpart-ECFRe106e84e67e2bc9 | Regulation SCI covers policies and procedures for SCI systems capacity, integrity, resiliency, availability and security, including SCI events, notification, corrective action and records. |
| `finra_4370` | FINRA Rule 4370: Business Continuity Plans and Emergency Contact Information | `regulatory_rule` | https://www.finra.org/rules-guidance/rulebooks/finra-rules/4370 | FINRA Rule 4370 requires member firms to create and maintain written business continuity plans for emergencies or significant business disruptions. |
| `nist_800_34` | NIST SP 800-34 Rev. 1: Contingency Planning Guide for Federal Information Systems | `standard_doc` | https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final | NIST SP 800-34 supports contingency planning, business impact analysis, recovery strategies, plan development, testing, training and maintenance. |
| `nist_800_61_r3` | NIST SP 800-61 Rev. 3: Incident Response Recommendations and Considerations | `standard_doc` | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf | NIST SP 800-61 Rev. 3 provides incident response considerations across preparation, detection, analysis, response, recovery and improvement activities. |
| `nist_800_92` | NIST SP 800-92: Guide to Computer Security Log Management | `standard_doc` | https://csrc.nist.gov/pubs/sp/800/92/final | NIST SP 800-92 supports log-management policies, infrastructure, analysis, retention, protection and operational processes. |
| `aws_reliability` | AWS Well-Architected Reliability Pillar | `cloud_architecture_doc` | https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html | AWS Reliability Pillar provides cloud reliability design and recovery practices for workloads. |
| `aws_dr` | AWS Reliability Pillar: Plan for Disaster Recovery | `cloud_architecture_doc` | https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/plan-for-disaster-recovery-dr.html | AWS DR guidance discusses backups, redundant components and RTO/RPO as restoration objectives set by business needs. |
| `google_sre_postmortem` | Google SRE Book: Postmortem Culture | `engineering_practice` | https://sre.google/sre-book/postmortem-culture/ | Google SRE postmortem guidance supports documenting incidents, understanding contributing causes and defining preventive actions in a blameless learning process. |
| `otel_docs` | OpenTelemetry Documentation | `framework_doc` | https://opentelemetry.io/docs/ | OpenTelemetry is a vendor-neutral observability framework for generating, collecting and exporting telemetry such as traces, metrics and logs. |

## 候选列表

| ID | title | partition | source_count | 状态 |
| --- | --- | --- | ---: | --- |
| P45-D-OPS01 | 交易系统必须声明 BC/DR 和关键系统恢复边界 | `KB_06_LIVE_EXECUTION` | 4 | candidate_ready |
| P45-D-OPS02 | 降级模式和只读模式必须有明确操作边界 | `KB_06_LIVE_EXECUTION` | 4 | candidate_ready |
| P45-D-OPS03 | failover、恢复和 replay 必须区分证据与动作 | `KB_06_LIVE_EXECUTION` | 4 | candidate_ready |
| P45-D-OPS04 | 交易事故 taxonomy 必须区分技术、市场、数据和风控影响 | `KB_06_LIVE_EXECUTION` | 4 | candidate_ready |
| P45-D-OPS05 | 事故后复盘必须输出可验证修复项 | `KB_06_LIVE_EXECUTION` | 4 | candidate_ready |
| P45-D-OPS06 | 运行时日志必须声明 retention、完整性和关联 ID | `KB_AI_26_DATABASE_STORAGE` | 4 | candidate_ready |

## 边界

```text
1. 不输出买卖点、仓位、杠杆、止损止盈、风险阈值、停机阈值或实盘执行建议。
2. Reg SCI / FINRA / NIST / AWS / Google SRE / OpenTelemetry 来源必须保留监管、平台、云服务、市场和系统边界。
3. replay、recovery、failover 不能被写成自动重发真实订单或绕过 Risk/Live Execution owner 的动作。
4. 候选知识必须等待外部严格审计，不得直接进入 formal reviewed。
```
