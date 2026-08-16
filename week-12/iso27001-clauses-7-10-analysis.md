# ISO/IEC 27001:2022 — Clauses 7 Through 10: Practitioner Analysis

> **Standard:** ISO/IEC 27001:2022 (Third Edition)
> **Scope:** Clauses 7 (Support), 8 (Operation), 9 (Performance Evaluation), 10 (Improvement)
> **PDCA Context:** Clause 7 enables the Plan phase; Clauses 8–10 complete the Do–Check–Act cycle

---

## The PDCA Cycle and the 10 Clauses

ISO 27001 is built on the Plan–Do–Check–Act (PDCA) improvement model. Every clause maps to a specific phase:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   PLAN          DO           CHECK          ACT            │
│  ──────        ──────       ───────        ──────          │
│  Clauses       Clause       Clause         Clause          │
│  4, 5, 6         8            9              10            │
│                                                             │
│              ↑ Clause 7 (Support) runs across ALL phases ↑  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Clause 7 is crosscutting** — it provides the people, competencies, communication infrastructure, and documentation that every other clause depends on. You cannot Plan without documented procedures (7.5), cannot Do without competent people (7.2), cannot Check without a communication plan for findings (7.4), and cannot Act without trained staff who understand why nonconformities matter (7.3).

---

## Clause 7: Support

### 7.1 — Resources

**Requirement:** The organization shall determine and provide the resources needed for the establishment, implementation, maintenance and continual improvement of the ISMS.

**Interpretation:** "Resources" is deliberately broad — it covers budget, personnel, tools, time, and management attention. An ISMS that exists only in documentation, with no budget allocation, no staff assigned, and no management time devoted to it, fails this clause before any audit evidence is reviewed.

**Audit implication:** Evidence of resource allocation includes: budget line items for security, headcount with information security in job descriptions, approved tooling (SIEM, vulnerability scanner, etc.), and documented management review time.

**Common gap:** Treating security as a cost center that absorbs whatever budget remains after other priorities are met — which in practice means perpetually under-resourced ISMS activities and a Clause 7.1 finding at every audit.

---

### 7.2 — Competence

**Requirement:** The organization shall determine the necessary competence of person(s) doing work under its control that affects its information security performance; ensure those persons are competent; take actions to acquire competence where needed; retain documented information as evidence.

**Interpretation:** Competence is not the same as having attended a training session. A person is competent if they have the education, training, or experience to actually perform the information security work assigned to them. The clause requires documented evidence of that competence — not just completion certificates.

**Evidence expected at audit:**
- Competency matrix mapping roles to required skills
- Training records with completion dates
- Certificates, qualifications, or experience records
- Evidence of gap-closure actions where competence was insufficient

**Practical example:** Assigning internal audit responsibility to an IT Manager who has never been trained in ISO 27001 audit methodology does not satisfy 7.2. The clause requires the organization to recognize the gap and take action — whether through training, hiring, or engaging an external auditor.

---

### 7.3 — Awareness

**Requirement:** Persons doing work under the organization's control shall be aware of: the information security policy; their contribution to the effectiveness of the ISMS; the implications of not conforming to ISMS requirements.

**Interpretation:** This is the clause that bridges the gap between having a policy and having people who follow it. Awareness is not the same as training — it is ongoing communication that keeps security top of mind across the organization.

**Why this clause matters disproportionately to its length:**

Every technical control in the organization depends on the people using systems behaving in accordance with security requirements. A stateful firewall cannot block an employee who connects a personal mobile hotspot to a corporate laptop. A DLP solution cannot scan traffic that never passes through the corporate proxy. An endpoint protection platform cannot intercept data transferred on a personal USB drive.

These are all Clause 7.3 failures — not failures of the technical controls themselves, but failures of the people interacting with those controls to understand why the rules exist.

**Evidence expected at audit:**
- Security awareness training logs (dates, completion rates, content)
- Records of policy communication (email evidence, intranet publication dates)
- Phishing simulation results (if conducted)
- Acknowledgment records (employees signing that they have read and understood the policy)

**Metrics:**
- Percentage of staff completing annual security awareness training (target: 100%)
- Phishing simulation click rate (trending direction matters more than absolute value)
- Policy acknowledgment completion rate

---

### 7.4 — Communication

**Requirement:** The organization shall determine the need for internal and external communications relevant to the ISMS, including: what to communicate, when, to whom, and how.

**Interpretation:** Information security events, policy updates, nonconformity findings, and audit results all need defined communication channels. Who tells the board about a major security incident? Who notifies staff about a policy change? Who communicates corrective action requirements to process owners?

**Communication plan elements:**
- Internal: Management review outputs to relevant staff; audit findings to process owners; incident notifications to affected teams
- External: Breach notification to PDPC (PDPA requirement); communications to certification bodies; supplier security requirement updates

---

### 7.5 — Documented Information

**Requirement:** The ISMS shall include documented information required by the standard and determined by the organization as necessary for effectiveness. The organization shall control documented information for suitability, adequacy, and availability.

**Interpretation:** ISO 27001:2022 uses "documented information" as a single term covering what was previously split into "documents" (procedures, policies) and "records" (evidence of actions taken). The distinction still matters operationally — a policy is a document (defines what should happen); an audit finding report is a record (proves something did happen).

**Minimum documented information required by the standard:**

| Document/Record | Clause |
|-----------------|--------|
| ISMS scope | 4.3 |
| Information security policy | 5.2 |
| Risk assessment process and results | 6.1, 8.2 |
| Risk treatment plan | 6.1, 8.3 |
| Statement of Applicability | 6.1.3 |
| Information security objectives | 6.2 |
| Evidence of competence | 7.2 |
| Internal audit results | 9.2 |
| Management review results | 9.3 |
| Nonconformities and corrective actions | 10.2 |

**Document control requirement:** Every document must have a version, approval status, and defined review cycle. A policy last reviewed in 2018 with no update history is a document control failure.

---

## Clause 8: Operation

### The Critical Distinction: Clause 6 vs Clause 8

This distinction is worth stating explicitly because confusion between them is one of the most common ISMS implementation errors:

| | Clause 6 (Planning) | Clause 8 (Operation) |
|-|---------------------|----------------------|
| **ISO language** | "The organization shall determine…" | "The organization shall implement and control…" |
| **What it produces** | The methodology, the framework, the plan | Records of the methodology being executed |
| **Auditor looks for** | Documents describing how risk assessment will be done | Evidence that it was actually done |
| **PDCA phase** | Plan | Do |

An organization can have perfect Clause 6 documentation — a beautifully written risk assessment methodology, a well-structured risk treatment plan, clearly defined objectives — and have zero Clause 8 compliance if none of it was ever executed and recorded. Conversely, running risk assessments without a documented methodology (Clause 6 gap) means the results are not reproducible or comparable over time.

---

### 8.1 — Operational Planning and Control

**Requirement:** The organization shall plan, implement, control, monitor and review the processes needed to meet requirements for the provision of information security.

**Interpretation:** This clause requires that the ISMS processes defined in planning phases are actually managed and controlled during execution — including managing changes and ensuring outsourced processes meet ISMS requirements.

**Outsourcing implication:** If a critical process (e.g., cloud hosting, software development, HR data processing) is outsourced, the organization retains responsibility for ensuring the supplier meets ISMS requirements. Clause 8.1 is where third-party security requirements originate.

---

### 8.2 — Information Security Risk Assessment

**Requirement:** The organization shall perform information security risk assessments at planned intervals or when significant changes are proposed or occur.

**Key word: "perform."** Clause 6 defines how. Clause 8 requires doing it — and keeping records that prove it was done.

**Triggers for risk assessment:**
- Planned intervals (annual is typical, quarterly for high-risk environments)
- New system deployments
- Significant architectural changes (cloud migration, new business line)
- Security incidents (retrospective risk assessment)
- Changes in threat landscape (new CVE class, new regulation)

**Evidence required:** Completed risk assessment records, dated and signed by the risk owner. Not a template — a completed, specific assessment for this organization's actual assets and threats.

---

### 8.3 — Information Security Risk Treatment

**Requirement:** The organization shall implement the information security risk treatment plan.

**Interpretation:** The risk treatment plan produced under Clause 6 must be executed. Controls selected in the Statement of Applicability must be implemented. Residual risk must be accepted by appropriate authority (typically the risk owner or CISO, escalated to board for high residual risk).

**Evidence required:**
- Records of control implementation (change tickets, configuration records)
- Updated risk register showing current risk status vs. pre-treatment level
- Formal risk acceptance decisions for residual risks above appetite
- Statement of Applicability showing implementation status for each control

---

## Clause 9: Performance Evaluation

### 9.1 — Monitoring, Measurement, Analysis and Evaluation

**Requirement:** The organization shall determine what needs to be monitored and measured, including information security processes and controls; the methods for monitoring, measurement, analysis and evaluation; when monitoring and measurement shall be performed; who shall monitor and measure.

**Practical KPI examples:**

| KPI | Measurement Method | Target |
|-----|-------------------|--------|
| Security incidents per month | SIEM incident count | Trending downward |
| Mean Time to Detect (MTTD) | Incident log timestamps | < 24 hours (High/Critical) |
| Patch compliance rate (critical patches within SLA) | Vulnerability scanner | ≥ 95% |
| Internal audit nonconformity closure rate | Audit tracker | 100% within agreed deadline |
| Security awareness training completion | LMS / training log | 100% of staff annually |
| Phishing simulation click rate | Phishing platform | Trending downward over 12 months |

---

### 9.2 — Internal Audit

**Requirement:** The organization shall conduct internal audits at planned intervals to provide information on whether the ISMS conforms to the organization's own requirements and to the requirements of ISO 27001, and is effectively implemented and maintained.

**Internal audit is not self-assessment.** The standard requires that the audit program maintain objectivity and impartiality — auditors cannot audit their own work. A CISO auditing the ISMS they are responsible for maintaining has a conflict of interest. Typical solutions: rotate audit responsibility, use a different team within the organization, or engage an external internal auditor.

**Audit program elements:**
- Planned audit schedule covering the full scope of the ISMS over a defined cycle
- Audit criteria (what is being checked against)
- Auditor selection ensuring independence
- Documented audit findings and results
- Reports to management

**Audit finding classification:**
- **Major Nonconformity:** A clause requirement is absent or completely fails to achieve its intent
- **Minor Nonconformity:** A requirement is partially met, or evidence is incomplete
- **Observation/Opportunity for Improvement:** Not a nonconformity, but a weakness that could develop into one

---

### 9.3 — Management Review

**Requirement:** Top management shall review the organization's ISMS at planned intervals to ensure its continuing suitability, adequacy and effectiveness.

**What the management review must consider:**
- Status of actions from previous reviews
- Changes in external/internal issues relevant to the ISMS
- Feedback on ISMS performance (audit results, incidents, KPIs)
- Interested party feedback
- Risk assessment results and risk treatment plan status
- Continual improvement opportunities

**Evidence required:** Management review meeting minutes, dated and signed. The absence of documented management review outputs is a major nonconformity — "we discussed it verbally" does not satisfy the clause.

---

## Clause 10: Improvement

### 10.1 — Continual Improvement

**Requirement:** The organization shall continually improve the suitability, adequacy and effectiveness of the ISMS.

**Interpretation:** Continual improvement is not a separate activity — it is the output of the entire Check (Clause 9) → Act (Clause 10) cycle working correctly. Every internal audit, management review, incident analysis, and KPI review should generate inputs to the improvement process.

---

### 10.2 — Nonconformity and Corrective Action

**Requirement:** When a nonconformity occurs, the organization shall: react; evaluate the need for action; implement corrective action; review effectiveness; update risks and documented information if necessary; retain documented information as evidence.

**The corrective action cycle:**

```
Nonconformity identified (Clause 9)
         ↓
Contain the immediate issue
         ↓
Root cause analysis (why did this happen?)
         ↓
Corrective action (fix the root cause, not just the symptom)
         ↓
Implementation with target date and owner
         ↓
Effectiveness check (did it work? did the problem recur?)
         ↓
Close or escalate
         ↓
Update risk register and documented information
```

**Root cause vs symptom example:**

| Nonconformity | Symptom Fix | Root Cause Fix |
|---------------|-------------|----------------|
| Firewall rule "PERMIT ANY ANY" found in DMZ→Internal | Remove the rule | Implement firewall change management process requiring security review before any rule change |
| Staff member clicked phishing link | Warn the individual | Investigate why awareness training failed; update training content; run targeted simulation for high-risk roles |
| Patch missing on critical server for 45 days | Apply patch | Review and fix patch management SLA process; implement exception tracking |

A corrective action that fixes the symptom without addressing the root cause will produce a repeat finding at the next audit.

---

## References

- ISO/IEC 27001:2022 (Third Edition) — official standard document
- ISO/IEC 27002:2022 — information security controls guidance
- ISO/IEC 27000:2018 — ISMS vocabulary and definitions
- ISO 31000:2018 — Risk management guidelines (risk treatment terminology)
