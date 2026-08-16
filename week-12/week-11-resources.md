# Resources: Week 11 — ISO/IEC 27001:2022 Clauses 7–10, Risk Simulation & Network Assessment

---

## ISO/IEC 27001:2022 Standard & Supporting Documents

| Resource | Detail |
|----------|--------|
| **ISO/IEC 27001:2022 (official)** | Third edition — main body Clauses 1–10 + Annex A |
| **ISO/IEC 27002:2022** | Implementation guidance for Annex A controls |
| **ISO/IEC 27000:2018** | ISMS vocabulary and definitions — freely available from ISO |
| **ISO 31000:2018** | Risk management — defines Avoid / Mitigate / Transfer / Accept terminology used in this portfolio |

**Key 2022 structural facts (verified):**
- 93 controls across 4 themes (A.5 Organizational, A.6 People, A.7 Physical, A.8 Technological)
- 11 new controls vs 2013 edition
- Clause 6.3 (Planning of changes) is new in 2022 — no equivalent in 2013
- Transition deadline from 2013 to 2022 certification: October 31, 2025 (IAF resolution)

---

## GRC Frameworks Referenced

| Resource | URL |
|----------|-----|
| **IIA Three Lines Model (2020)** | https://www.theiia.org/globalassets/documents/resources/the-iias-three-lines-model-an-update-of-the-three-lines-of-defense-july-2020/three-lines-model-updated.pdf |
| **NIST Cybersecurity Framework 2.0** | https://www.nist.gov/cyberframework |
| **NIST SP 800-30 Rev 1 (Risk Assessment)** | https://csrc.nist.gov/publications/detail/sp/800-30/rev-1/final |
| **ISO 31000:2018 (Risk Management)** | https://www.iso.org/standard/65694.html |

---

## Thai Regulatory Framework

| Resource | URL |
|----------|-----|
| **PDPA (Personal Data Protection Act B.E. 2562)** | https://www.pdpc.or.th/ |
| **PDPA Section 37** | Security obligations of controller — appropriate security measures for personal data |
| **PDPA Section 82** | Administrative penalties — up to 5M THB for non-compliance |

---

## Vulnerability & Weakness References

| Resource | URL |
|----------|-----|
| **OWASP Top 10 2021** | https://owasp.org/Top10/ |
| **OWASP A01:2021 — Broken Access Control** | https://owasp.org/Top10/A01_2021-Broken_Access_Control/ |
| **OWASP A03:2021 — Injection** | https://owasp.org/Top10/A03_2021-Injection/ |
| **CWE-284 (Improper Access Control)** | https://cwe.mitre.org/data/definitions/284.html |

---

## Network Security References

| Resource | URL |
|----------|-----|
| **IANA Port Number Registry** | https://www.iana.org/assignments/service-names-port-numbers/ |
| **NIST SP 800-41 Rev 1 (Firewall Guidelines)** | https://csrc.nist.gov/publications/detail/sp/800-41/rev-1/final |
| **Cisco 802.1X Overview** | https://www.cisco.com/c/en/us/td/docs/ios/12_2sx/configuration/guide/12_2sx_cg/sec_8021x.html |

---

## Annex A Controls Referenced This Week

| Control | Title | File Used In |
|---------|-------|-------------|
| A.5.10 | Acceptable use of information and other associated assets | FastBuy simulation |
| A.5.15 | Access control | Network assessment, FastBuy |
| A.5.19 | Information security in supplier relationships | FastBuy (gateway risk) |
| A.5.23 | Information security for use of cloud services | FastBuy (AWS scope) |
| A.5.30 | ICT readiness for business continuity | Self-assessment gap area |
| A.6.3 | Information security awareness, education and training | Shadow IT risk |
| A.6.4 | Disciplinary process | Policy enforcement |
| A.7.1 | Physical security perimeters | Network assessment |
| A.8.16 | Monitoring activities | Network assessment |
| A.8.20 | Networks security | FastBuy, network assessment |
| A.8.21 | Security of network services | FastBuy, network assessment |
| A.8.22 | Segregation in networks | FastBuy, network assessment |
| A.8.24 | Use of cryptography | Referenced in structure overview |

---

## Clause 9: Performance Evaluation — KPI Reference

KPIs cited in this week's clause analysis:

| KPI | Measurement | Target |
|-----|-------------|--------|
| Security incidents per month | SIEM incident count | Trending downward |
| Mean Time to Detect (MTTD) | Incident log timestamps | < 24h (Critical/High) |
| Patch compliance rate | Vulnerability scanner | ≥ 95% within SLA |
| Internal audit nonconformity closure rate | Audit tracker | 100% within agreed deadline |
| Security awareness training completion | LMS / training log | 100% annually |
| Phishing simulation click rate | Phishing platform | Trending downward |

---

## Risk Treatment Terminology (ISO 31000:2018)

| Option | Definition | Example This Week |
|--------|-----------|------------------|
| **Mitigate** | Apply controls to reduce likelihood or impact | Network segmentation for DMZ/DB separation |
| **Transfer** | Shift financial/operational responsibility | Payment routing through PCI DSS gateway |
| **Avoid** | Eliminate the activity that creates the risk | Shutting down unused switch ports |
| **Accept** | Acknowledge and document without treatment | Finance VLAN gap accepted with documented residual risk |

**Important clarification on Risk Transfer:**
Routing payment processing through a certified third-party gateway transfers PCI DSS compliance scope for card data. It does **not** transfer PDPA obligations for customer PII collected in the same checkout flow. Risk Transfer relocates financial and operational liability; it does not extinguish regulatory accountability to the PDPC under Thai law.

---

## PCI DSS Reference

| Resource | URL |
|----------|-----|
| **PCI Security Standards Council** | https://www.pcisecuritystandards.org/ |
| **PCI DSS v4.0** | https://www.pcisecuritystandards.org/document_library/ |
| **Shared Responsibility — Third Party Processors** | Covered under PCI DSS Requirement 12.8 |

---

## Weekly Study Schedule

| Day | Activity |
|-----|----------|
| **Mon–Tue** | ISO 27001:2022 — read Clause 7 (Support) from official standard |
| **Wed** | ISO 27001:2022 — read Clauses 8–10 (Operation, Evaluation, Improvement) |
| **Thu** | Complete 10-clause structure review + Annex A self-assessment |
| **Fri** | FastBuy risk simulation — risk register construction |
| **Sat** | FastBuy — corrective action plan (C-Level format) + Network architecture assessment |
| **Sun** | Write documentation; commit to repository |

---

**Status:** Week 11 Resources | ISO 27001:2022 Complete (All Clauses) | FastBuy Simulation | Network GRC Assessment
