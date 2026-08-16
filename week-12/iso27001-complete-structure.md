# ISO/IEC 27001:2022 — Complete Structure: All 10 Clauses + Annex A

> **Purpose:** Consolidated reference and self-assessment after completing all main body clauses
> **Basis:** ISO/IEC 27001:2022 (Third Edition) read in full across Weeks 10–11

---

## The Complete Clause Map

```
ISO/IEC 27001:2022 — Main Body Structure

CLAUSES 1–3 (Scope, Normative References, Terms)
  └── Foundational — not auditable requirements, but define the standard's scope and vocabulary

CLAUSE 4 — Context of the Organization          [PLAN]
  4.1  Understanding the organization and its context
  4.2  Understanding needs and expectations of interested parties
  4.3  Determining the scope of the ISMS
  4.4  Information security management system

CLAUSE 5 — Leadership                            [PLAN]
  5.1  Leadership and commitment
  5.2  Policy
  5.3  Organizational roles, responsibilities and authorities

CLAUSE 6 — Planning                              [PLAN]
  6.1  Actions to address risks and opportunities
  6.2  Information security objectives and planning to achieve them
  6.3  Planning of changes  ← NEW IN 2022

CLAUSE 7 — Support                               [PLAN — enabling infrastructure]
  7.1  Resources
  7.2  Competence
  7.3  Awareness
  7.4  Communication
  7.5  Documented information

CLAUSE 8 — Operation                             [DO]
  8.1  Operational planning and control
  8.2  Information security risk assessment
  8.3  Information security risk treatment

CLAUSE 9 — Performance Evaluation               [CHECK]
  9.1  Monitoring, measurement, analysis and evaluation
  9.2  Internal audit
  9.3  Management review

CLAUSE 10 — Improvement                          [ACT]
  10.1 Continual improvement
  10.2 Nonconformity and corrective action

ANNEX A — Information Security Controls Reference
  A.5  Organizational controls  (37 controls)
  A.6  People controls           (8 controls)
  A.7  Physical controls        (14 controls)
  A.8  Technological controls   (34 controls)
  Total: 93 controls
```

---

## Clause-by-Clause Self-Assessment

**Rating scale:** 1–10 where 10 = can explain clearly, apply in a simulation, and identify gaps in real implementation

| Clause | Title | Self-Rating | Strongest point | Residual gap |
|--------|-------|-------------|-----------------|--------------|
| 4.1 | Context | 8.5/10 | SWOT/PESTLE for external/internal issues | Applying to highly complex, regulated industries (banking, healthcare) |
| 4.2 | Interested parties | 8/10 | Stakeholder requirement mapping | Handling conflicting stakeholder requirements |
| 4.3 | Scope | 9/10 | Cloud shared responsibility scope decisions | Multi-jurisdictional scope across regulatory frameworks |
| 4.4 | ISMS as a system | 8/10 | Understands process-based approach | Evidencing ISMS integration with business processes |
| 5.1 | Leadership | 8.5/10 | Three Lines Model application | Assessing whether leadership commitment is genuine vs. performative |
| 5.2 | Policy | 8.5/10 | Policy content requirements + communication evidence | Measuring policy effectiveness |
| 5.3 | Roles + authorities | 8/10 | RACI matrix construction, CISO accountability | Gap analysis for organizations with informal security governance |
| 6.1 | Risk and opportunities | 8.5/10 | Likelihood × Impact scoring, risk register | Quantitative risk modeling (FAIR methodology) |
| 6.2 | Objectives | 8/10 | SMART objective structuring | Cascading ISMS objectives to department level |
| 6.3 | Planning of changes | 8.5/10 | Change management gate requirement (new in 2022) | Integrating with existing ITIL/change management frameworks |
| 7.1 | Resources | 8/10 | Resource requirement documentation | Budget justification for security investment |
| 7.2 | Competence | 8/10 | Competency matrix and gap closure | Assessing competence vs. credentials (different things) |
| **7.3** | **Awareness** | **9/10** | **Human bypass of technical controls (Shadow IT)** | Measuring actual behavioral change vs. training completion |
| 7.4 | Communication | 7.5/10 | Communication plan structure | External communication obligations (regulatory, clients) |
| 7.5 | Documented information | 8/10 | Document vs. record distinction | Version control at scale across large organizations |
| 8.1 | Operational control | 8/10 | Clause 6 vs 8 distinction | Third-party / outsourced process control |
| 8.2 | Risk assessment (Do) | 8.5/10 | Executing risk assessment with evidence | Annual vs. event-triggered cadence decisions |
| 8.3 | Risk treatment (Do) | 8.5/10 | Treatment decisions + SoA evidence | Residual risk acceptance documentation |
| 9.1 | Monitoring + measurement | 8/10 | KPI construction (MTTD, patch compliance, etc.) | Metric selection for non-technical ISMS processes |
| 9.2 | Internal audit | 8/10 | Audit finding classification (Major/Minor/OFI) | Auditor independence in small organizations |
| 9.3 | Management review | 8/10 | Required review inputs and evidence | Ensuring management review drives action, not just documentation |
| 10.1 | Continual improvement | 8/10 | PDCA cycle as a living process | Distinguishing improvement from reactive firefighting |
| 10.2 | Nonconformity + CAP | 9/10 | Root cause vs symptom analysis | Effectiveness review (verifying the fix actually worked) |

**Overall assessment:** Confident working understanding of the full standard. Residual gaps are concentrated in advanced quantitative risk modeling, multi-jurisdictional scope, and complex stakeholder environments — appropriate depth for an entry-level GRC practitioner.

---

## Annex A: Complete Structure

### The Restructuring from 2013 to 2022

ISO 27001:2013 Annex A contained **114 controls across 14 domains** (A.5 through A.18). ISO 27001:2022 restructured this to **93 controls across 4 themes** (A.5 through A.8). The reduction from 114 to 93 reflects consolidation, not removal of requirements — some controls were merged, and 11 entirely new controls were added.

**Mapping tables are required for transition audits** — an organization certified under 2013 needs to demonstrate that every 2013 control is covered in the new structure.

---

### A.5 — Organizational Controls (37 controls)

Covers governance, policy, legal compliance, information classification, supplier relationships, and incident management at the organizational level.

**Controls used most frequently in simulation work:**

| Control | Title | Applied in |
|---------|-------|-----------|
| A.5.10 | Acceptable use of information and other associated assets | Shadow IT risk, policy enforcement |
| A.5.15 | Access control | Authentication failures, default credentials |
| A.5.19 | Information security in supplier relationships | Third-party gateway risk transfer |
| A.5.23 | Information security for use of cloud services | AWS-hosted FastBuy architecture |
| A.5.24 | Information security incident management planning | Incident response gap findings |
| A.5.30 | ICT readiness for business continuity | BCP/DRP integration — gap area |

**Residual gap — A.5.30:** ICT readiness for business continuity requires integration with the organization's Business Continuity Plan and Disaster Recovery Plan. This control is context-dependent to a specific organization's RTO/RPO requirements and infrastructure — difficult to assess meaningfully in a simulation without a defined business continuity strategy as the baseline.

---

### A.6 — People Controls (8 controls)

Covers human resource security: pre-employment screening, terms of employment, security awareness, disciplinary process, offboarding, and remote working.

**Key controls for GRC practice:**

| Control | Title | Notes |
|---------|-------|-------|
| A.6.1 | Screening | Background verification requirements |
| A.6.3 | Information security awareness, education and training | Directly supports Clause 7.3 |
| A.6.4 | Disciplinary process | Enforcement mechanism for policy violations |
| A.6.6 | Confidentiality or non-disclosure agreements | Supplier and employee obligations |

**Practical note on A.6.4:** A disciplinary process for policy violations does not mean immediate termination for every breach. It means having a defined, proportionate, and documented process — so that when Shadow IT behavior is discovered, there is a consistent and defensible response rather than ad hoc manager discretion.

---

### A.7 — Physical Controls (14 controls)

Covers physical security perimeters, entry controls, desk policy, equipment protection, and secure disposal.

**Key controls for GRC practice:**

| Control | Title | Notes |
|---------|-------|-------|
| A.7.1 | Physical security perimeters | Server room, data center access zones |
| A.7.2 | Physical entry | Access control mechanisms (badge, biometric) |
| A.7.9 | Security of assets off-premises | Laptop/device policies for remote workers |
| A.7.10 | Storage media | Secure disposal, encryption requirements |

**GRC audit note:** Physical controls are frequently under-evidenced. Having a locked server room door is not sufficient — evidence of access logs, regular review of access permissions, and testing that controls work (e.g., tailgating tests) is what an auditor looks for.

---

### A.8 — Technological Controls (34 controls)

The largest theme. Covers endpoint security, network security, identity management, encryption, vulnerability management, secure development, and monitoring.

**Controls used most frequently across Weeks 10–11:**

| Control | Title | Applied in |
|---------|-------|-----------|
| A.8.8 | Management of technical vulnerabilities | Unpatched server findings |
| A.8.15 | Logging | Log retention requirements |
| A.8.16 | Monitoring activities | SIEM, geo-velocity anomaly detection |
| A.8.20 | Networks security | Firewall ACL review, Shadow IT |
| A.8.21 | Security of network services | Any-Any firewall rule finding |
| A.8.22 | Segregation in networks | DMZ/Internal zone separation |
| A.8.23 | Web filtering | Content filtering policies |
| A.8.24 | Use of cryptography | TLS requirements, FTP replacement |

**Residual gap — A.8 cryptography depth:** Controls A.8.24 (Use of Cryptography) and A.8.26 (Application security requirements) involve detailed requirements around key management, cipher suite selection, and cryptographic protocol lifecycle that require deeper technical cryptography knowledge than currently developed. The practical application of these controls (identifying weak cipher suites, reviewing TLS configurations) is understood; the underlying cryptographic mathematics is a gap area for future development.

---

### New Controls in 2022 (Not in 2013)

All 11 new controls, with GRC relevance rating:

| Control | Title | GRC Relevance |
|---------|-------|---------------|
| A.5.7 | Threat intelligence | HIGH — informs risk assessment inputs |
| A.5.23 | Cloud security | HIGH — critical for any cloud-hosted ISMS |
| A.5.30 | ICT readiness for business continuity | HIGH — BCP integration |
| A.7.4 | Physical security monitoring | MEDIUM — CCTV/monitoring policy |
| A.8.9 | Configuration management | HIGH — hardening standards |
| A.8.10 | Information deletion | HIGH — data retention + PDPA |
| A.8.11 | Data masking | MEDIUM — development/test environments |
| A.8.12 | Data leakage prevention | HIGH — DLP policy and tooling |
| A.8.16 | Monitoring activities | HIGH — SIEM, anomaly detection |
| A.8.23 | Web filtering | MEDIUM — acceptable use enforcement |
| A.8.28 | Secure coding | HIGH — application security in SDLC |

---

## The Statement of Applicability

The Statement of Applicability (SoA) is the document that declares which of the 93 Annex A controls the organization has selected, whether each is implemented, and why any control has been excluded (with justification).

**Why every control must be considered, even if excluded:**
ISO 27001 does not require implementing all 93 controls. It requires that the organization *consider* each control and either implement it or document a justified exclusion. An organization that excludes A.7.1 (Physical security perimeters) because they are entirely cloud-hosted with no physical premises has a defensible exclusion. An organization that excludes A.8.20 (Network security) without justification has a major nonconformity.

**SoA structure:**

| Control | Title | Applicable? | Implemented? | Justification |
|---------|-------|-------------|--------------|---------------|
| A.8.20 | Networks security | Yes | Yes | Network infrastructure present; controls defined in Network Security Policy |
| A.7.1 | Physical security perimeters | Partial | Yes | One data center operated; cloud environments covered by provider SOC 2 |

---

## Summary Assessment: Readiness for ISO 27001 Audit Engagement

**Areas of confidence:**
- Risk assessment methodology and risk register construction
- Audit finding classification and corrective action planning
- Annex A control mapping from technical findings
- Clause 6 vs Clause 8 operational distinction
- Document/record evidence requirements per clause

**Areas for continued development:**
- Quantitative risk modeling (FAIR, OCTAVE-S)
- Business continuity integration (A.5.30)
- Advanced cryptography controls (A.8.24, A.8.26)
- Multi-jurisdictional scope and cross-border data transfer requirements
- Internal audit methodology (practical auditing, not just conceptual)

---

## References

- ISO/IEC 27001:2022 (Third Edition) — official standard
- ISO/IEC 27002:2022 — guidance on controls
- ISO/IEC 27000:2018 — ISMS vocabulary
- ISO 31000:2018 — Risk management
