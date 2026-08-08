# ISO/IEC 27001:2022 — Clauses 4 Through 6: Practitioner Analysis

> **Standard:** ISO/IEC 27001:2022 (Third Edition, replacing 2013/2017 revision)
> **Scope of this document:** Clauses 4 (Context), 5 (Leadership), and 6 (Planning)
> **Approach:** Clause text → practical interpretation → audit implications

---

## Preliminary: What Changed from 2013 to 2022

Understanding the revision is itself an audit skill — an organization certified under ISO 27001:2013 that has not transitioned must have done so by October 31, 2025 (the deadline set by IAF).

**Key structural changes in 2022:**
- Annex A restructured from **114 controls in 14 domains** (A.5–A.18) to **93 controls in 4 themes** (A.5 Organizational, A.6 People, A.7 Physical, A.8 Technological)
- **11 new controls** added, including A.5.7 (Threat intelligence), A.5.23 (Cloud security), A.8.11 (Data masking)
- **Clause 6.3 added** (Planning of changes) — no equivalent in 2013
- Control numbering changed entirely — mapping tables required for transition audits

---

## Clause 4: Context of the Organization

### 4.1 — Understanding the Organization and Its Context

**Requirement (what the standard says):**
> The organization shall determine external and internal issues that are relevant to its purpose and that affect its ability to achieve the intended outcome(s) of its information security management system.

**Interpretation:**
Before an organization decides what to protect, it must understand what it is — its purpose, its operating environment, and the pressures acting on it. This is not a one-time activity; it informs every other clause.

**Internal issues to identify:**
- Organizational structure, governance model, culture
- IT architecture and existing controls
- Contractual and legal obligations already in place
- Existing risk appetite and management practices

**External issues to identify:**
- Regulatory environment (PDPA, GDPR, PCI DSS, sector-specific regulation)
- Threat landscape (industry-relevant threat actors and TTPs)
- Technology dependencies (cloud providers, third-party vendors)
- Economic, political, and competitive factors that affect security investment

**Audit implication:** An auditor would expect to see documented evidence that this analysis was conducted — typically in the form of a SWOT analysis, PESTLE analysis, or a structured context review. The absence of this documentation is a nonconformity.

---

### 4.2 — Understanding the Needs and Expectations of Interested Parties

**Requirement:**
> The organization shall determine: (a) interested parties that are relevant to the ISMS; (b) the relevant requirements of these interested parties; (c) which of these requirements will be addressed through the ISMS.

**Interpretation:**
"Interested parties" (stakeholders) include anyone whose requirements affect the ISMS — customers, regulators, shareholders, employees, suppliers, and certification bodies.

**Practical example — identifying relevant requirements:**

| Interested Party | Requirement | ISMS Implication |
|-----------------|-------------|------------------|
| Enterprise clients | ISO 27001 certification required for supplier onboarding | ISMS scope must include systems processing client data |
| Thai regulators | PDPA compliance (data subject rights, security of personal data) | Processing activities must be documented; security measures must be appropriate |
| Cloud provider (AWS/Azure) | Shared Responsibility Model — security *of* the cloud is their responsibility; security *in* the cloud is ours | Scope statement must explicitly address cloud deployment security responsibilities |

**Audit implication:** A stakeholder register or equivalent document is expected. Crucially, the requirement to address a stakeholder's needs does not mean the ISMS must satisfy every request — it means the organization has *considered* each requirement and made a documented decision about which to incorporate.

---

### 4.3 — Determining the Scope of the ISMS

**Requirement:**
> The organization shall determine the boundaries and applicability of the ISMS to establish its scope.

**Interpretation:**
Scope is the most consequential single decision in an ISMS implementation. A scope statement defines exactly which assets, processes, locations, and business units are inside the ISMS boundary — and implicitly, what is outside it.

**Scope statement structure (what auditors look for):**
- Physical locations included
- Organizational units included
- Information assets within scope
- Key business processes covered
- Explicit exclusions, with justification
- Connection points to out-of-scope systems

**Common scope failures:**

1. **Artificial exclusion of critical assets:** An organization scopes its ISMS to cover only "the data center" while the application layer deployed on AWS remains out of scope. If that application processes customer personal data, the exclusion is indefensible.

2. **Cloud shared responsibility misunderstood:** Scoping out "the infrastructure" because it is on AWS does not scope out the organization's own application-layer security responsibilities. AWS controls the physical server; the organization controls its own IAM policies, encryption keys, application code, and data.

3. **Scope creep in the other direction:** Scoping the entire organization for a first certification creates an unmanageable implementation. Certification bodies accept a defined subset — a specific product line, a single business unit, a defined service.

**Evidence expected at audit:** A written scope statement, typically a single document, reviewed and approved by top management.

---

### 4.4 — Information Security Management System

**Requirement:**
> The organization shall establish, implement, maintain and continually improve an information security management system, including the processes needed and their interactions.

**Interpretation:**
This is the foundational clause that frames everything else: the ISMS is a *system of processes*, not a collection of documents. The word "continually" is deliberate — certification is not a destination, it is a state of ongoing operation.

---

## Clause 5: Leadership

### 5.1 — Leadership and Commitment

**Requirement:**
> Top management shall demonstrate leadership and commitment with respect to the information security management system.

**Interpretation:**
This clause exists because ISMS implementations fail most often at the top, not the bottom. Without visible, active commitment from senior leadership, security policies are ignored, resources are not allocated, and the ISMS degrades into documentation that exists on paper only.

**What "demonstrated" commitment looks like:**
- Information security policy approved and signed by C-level
- ISMS roles formally assigned with documented accountability
- Adequate resources (budget, personnel, tools) allocated to ISMS activities
- Management review meetings conducted (Clause 9.3) with documented outcomes
- Information security integrated into business planning, not treated as a separate IT function

**Audit approach:** Review management review meeting minutes, resource allocation decisions, and whether the CISO (or equivalent) has direct access to the board. A CISO who reports only to the CTO, with no independent board visibility, is a governance gap.

**Three Lines Model application:**
- **First line** (operations — IT, development, business units): owns risk day-to-day; implements controls
- **Second line** (information security, risk management, compliance): provides policy, oversight, monitoring, and expertise without operational ownership
- **Third line** (internal audit): provides independent assurance to the board and audit committee

An auditor notes that the second line and third line must be genuinely independent of each other. A security team that both sets policy and assesses its own compliance has a conflict of interest that is itself a control weakness.

---

### 5.2 — Policy

**Requirement:**
> Top management shall establish an information security policy.

**What the policy must include:**
- Appropriate to the organization's purpose
- Includes objectives or provides a framework for setting them
- Includes commitment to satisfying applicable requirements
- Includes commitment to continual improvement
- Communicated within the organization
- Available to interested parties as appropriate

**Common gap:** A policy that is well-written but not communicated. If staff are unaware the policy exists, the control is ineffective regardless of document quality. Evidence of communication (training records, acknowledgment logs, intranet publication dates) is part of the audit.

---

### 5.3 — Organizational Roles, Responsibilities and Authorities

**Requirement:**
> Top management shall ensure that the responsibilities and authorities for roles relevant to information security are assigned and communicated.

**Interpretation:**
Specifically requires that responsibility for:
- Ensuring the ISMS conforms to the standard's requirements
- Reporting on ISMS performance to top management

...is formally assigned to a named person or function.

**Practical application:** A RACI matrix or equivalent that maps ISMS responsibilities to specific roles. The absence of a named CISO or equivalent — or a CISO whose information security responsibilities are not formally documented — is a finding.

---

## Clause 6: Planning

### 6.1 — Actions to Address Risks and Opportunities

**Requirement:**
> When planning for the ISMS, the organization shall consider the issues referred to in 4.1 and the requirements referred to in 4.2 and determine the risks and opportunities that need to be addressed.

**Interpretation:**
Clause 6.1 is where strategic context (Clause 4) is translated into concrete risk management action. It requires:
1. A defined risk assessment process (criteria, methodology, ownership)
2. Execution of that process to identify information security risks
3. Risk treatment decisions for each identified risk
4. A documented risk treatment plan

**Risk assessment methodology:**
ISO 27001 does not prescribe a specific methodology — it requires that the chosen methodology produce "consistent, valid and comparable results." Common approaches:
- Likelihood × Impact matrix (qualitative)
- NIST SP 800-30 (quantitative elements)
- OCTAVE (asset-based)

**Simulated finding — default credentials:**

```
Finding: Default admin credentials on branch office router (admin/admin)

Risk Assessment:
  Asset: Branch network router (gateway to corporate WAN)
  Threat: Unauthorized network access
  Vulnerability: No credential change policy enforced on deployment
  Likelihood: High (default credentials are publicly documented for every device)
  Impact: High (compromise of branch router = lateral movement to corporate WAN)
  Risk Level: CRITICAL (High × High)

Risk Treatment Decision: Mitigate
Treatment: Immediate credential rotation; implementation of configuration
           management procedure for all network device deployments;
           monthly audit of device credential status

Residual Risk: Medium (after treatment, credentials still require periodic
               rotation — ongoing monitoring required)

OWASP Mapping: A07:2021 — Identification and Authentication Failures
ISO 27001 Control: A.8.20 (Network Security), A.5.15 (Access Control)
```

---

### 6.2 — Information Security Objectives and Planning to Achieve Them

**Requirement:**
> The organization shall establish information security objectives at relevant functions and levels.

**What makes an objective compliant:**
- Consistent with the information security policy
- Measurable (or at least assessable)
- Takes into account applicable requirements and risk assessment results
- Monitored, communicated, updated as appropriate

**Non-compliant objective example:** "Improve security" — no measurement, no timeline, no accountability.

**Compliant objective example:** "Reduce the mean time to detect (MTTD) critical security events from 72 hours to 8 hours by Q4 2025, measured monthly via SIEM dashboard, owned by the SOC Manager."

---

### 6.3 — Planning of Changes *(New in 2022)*

**Requirement:**
> When the organization determines the need to change the information security management system, the changes shall be carried out in a planned manner.

**Why this clause was added:**
ISO 27001:2013 was silent on what happens when an organization changes its ISMS — a gap that allowed organizations to make significant changes (cloud migrations, acquisitions, network re-architectures) without re-evaluating the risk posture of the ISMS itself. The 2022 revision addresses this by requiring that planned changes to the ISMS be managed deliberately.

**What "planned manner" means in practice:**
- Changes to scope, policy, risk treatment, or organizational structure must be evaluated for security impact before implementation
- The ISMS must not be left in a degraded state during transition
- Risk assessment must be re-performed or updated when the change is material

**Examples of changes requiring Clause 6.3 treatment:**

| Change | ISMS Impact |
|--------|------------|
| Migrating from on-premise to AWS | New assets, new controls required, shared responsibility must be re-documented |
| Acquiring a subsidiary | Subsidiary's systems may fall inside scope; their risks inherit |
| Changing CISO or security team | Clause 5.3 responsibilities must be re-assigned; competency requirements reassessed |
| Deploying a new SaaS platform that processes personal data | New processing activity; PDPA obligations triggered; Annex A.5.23 (cloud) applies |

**Audit implication:** Change management records (change request, risk impact assessment, approval) are the evidence. An organization that cannot show it assessed security impact before a major architectural change has a gap against Clause 6.3.

---

## Annex A Controls Referenced This Week

| Control | Title | Clause Connection |
|---------|-------|-------------------|
| A.5.15 | Access Control | 6.1 — Risk treatment for authentication failures |
| A.5.23 | Information security for use of cloud services | 4.3 — Scope; 6.3 — planned change (cloud migration) |
| A.8.20 | Networks security | 6.1 — Risk treatment for network exposure |
| A.8.24 | Use of cryptography | 6.1 — Risk treatment for plaintext transmission |

---

## References

- ISO/IEC 27001:2022 (Third Edition) — official standard document
- ISO/IEC 27000:2018 — ISMS vocabulary and definitions
- IIA Three Lines Model (2020): https://www.theiia.org/globalassets/documents/resources/the-iias-three-lines-model-an-update-of-the-three-lines-of-defense-july-2020/three-lines-model-updated.pdf
- PDPA (Thailand) Personal Data Protection Act B.E. 2562: https://www.pdpc.or.th/
