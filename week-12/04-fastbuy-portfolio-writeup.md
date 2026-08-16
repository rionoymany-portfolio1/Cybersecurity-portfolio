# From Architecture Diagram to Board Decision: A GRC Case Study of FastBuy E-Commerce

*A simulated ISO/IEC 27001:2022 ISMS implementation and network security assessment, demonstrating how technical findings are translated into regulatory risk, business impact, and executive-ready recommendations.*

---

## 1. Executive Summary

This case study documents a simulated information security governance engagement for **FastBuy**, a mid-size, AWS-hosted e-commerce startup processing customer personally identifiable information (PII) and payment card data across a three-zone network architecture.

The engagement combined two complementary workstreams:

- **An ISMS Risk Register and Corrective Action Plan** — applying ISO/IEC 27001:2022 Clauses 6 and 8 to identify, score, and treat the organization's most significant information security risks
- **A Network Architecture Risk Assessment** — reviewing the firewall ruleset, network topology, and zone segmentation through a GRC lens, mapping each finding to a specific ISO 27001 Annex A control and a quantified business consequence

**Four risks were identified**, ranging from CRITICAL to HIGH severity. The most significant finding — a database server co-located with an internet-facing web server in the same network zone — left 500,000+ customer records one SQL injection away from a mandatory PDPA breach notification. The assessment concluded with a C-Level action plan presenting each remediation as a business decision, not a technical task.

---

## 2. The Challenge

### The Organization

FastBuy is an e-commerce startup with a fully cloud-based infrastructure (AWS). Its two primary data categories create overlapping compliance obligations:

| Data Type | Regulation | Obligation |
|-----------|-----------|-----------|
| Customer PII (name, address, email, order history) | PDPA (Thailand) — Section 37 | Implement appropriate security measures; notify PDPC within 72 hours of a breach |
| Payment card data | PCI DSS | Scoped to third-party gateway — FastBuy never stores raw card data |

### The Architecture

FastBuy's network followed a conventional three-zone design — Internet, DMZ, and Internal Zone — separated by a stateful firewall (`fw-main-01`). On paper, the architecture was sound. In practice, the firewall ruleset undermined it:

```
INTERNET
    ↓
EDGE ROUTER (no stateful inspection)
    ↓
STATEFUL FIREWALL (fw-main-01)
    ↓                    ↓
   DMZ               INTERNAL ZONE
  [Web Server]       [ERP, Finance, Workstations]
  [Database ←── also here, misconfigured]
```

**The critical misconfiguration was not in the firewall itself — it was in the architecture underneath it.** The customer database was deployed in the DMZ alongside the public-facing web server, rather than in the private internal zone. And the firewall's ruleset allowed all traffic from the DMZ to the Internal zone with no restriction (`PERMIT IP DMZ → INTERNAL ANY`), effectively eliminating the security value of the zone boundary.

These two issues together meant that a single web application vulnerability would cascade directly into a full database breach and an uncontrolled internal network compromise.

---

## 3. My Approach: The GRC Lens

A network engineer reviewing this environment would produce a list of configuration errors and fixes. That list is necessary, but it is not sufficient. The role of a GRC practitioner in a technical assessment is to answer a different set of questions:

- **Which ISO 27001 control does this gap violate?**
- **If this vulnerability is exploited, what regulatory obligation is triggered?**
- **How do we frame this for a CEO or CFO who needs to authorize the fix?**

My approach applied the following framework to each finding:

**Step 1 — Risk Identification (ISO 27001 Clause 6.1 / 8.2)**
For each identified weakness, I defined the asset, threat, and vulnerability, then scored risk using a qualitative Likelihood × Impact matrix (rated 1–3 on each dimension, producing scores of 1, 2, 3, 4, 6, or 9).

**Step 2 — Control Mapping (Annex A)**
Each risk was mapped to the most specific applicable Annex A control — not to a broad category, but to the precise control the gap violates.

**Step 3 — Business and Regulatory Translation**
Each technical finding was reframed in terms of: what regulatory obligation is triggered if this is exploited, what is the likely financial consequence, and what does the CISO need to tell the board?

**Step 4 — Treatment Decision (ISO 31000 / Clause 8.3)**
For each risk: Mitigate, Transfer, Avoid, or Accept — with documented rationale, owner, and target date.

---

## 4. Highlighted Findings

### Finding A: Database and Web Server in the Same Network Zone *(Risk Score: 9 — CRITICAL)*

**The Technical Flaw**

FastBuy's customer database — containing PII for 500,000+ registered users — was deployed in the DMZ alongside the public-facing web server. No network segmentation existed between the presentation tier and the data tier. Additionally, firewall Rule 3 (`PERMIT IP DMZ → INTERNAL ANY`) allowed all DMZ traffic to reach the internal zone without restriction.

The combined effect: a single exploited web application vulnerability (SQL injection, remote code execution, or file upload bypass) provided an attacker with direct, unrestricted access to the full customer database and a foothold into the internal network.

**ISO 27001 Control Mapping**

| Control | Title | Gap |
|---------|-------|-----|
| **A.8.22** | Segregation in networks | Database and web server in same zone — no tier separation |
| **A.8.20** | Networks security | Firewall rule permits all DMZ→Internal traffic without restriction |

**Business and Regulatory Impact**

A full database exfiltration would trigger **mandatory PDPA breach notification to the PDPC within 72 hours** of the organization becoming aware of the incident. Under PDPA Section 82, administrative penalties reach up to **5 million THB**. Public disclosure is required. For an early-stage e-commerce business, the reputational consequence of a breach of this scale — particularly one that exploited a preventable architectural decision — would be severe, affecting customer retention, investor confidence, and the ability to pursue enterprise B2B clients who require ISO 27001 certification as a supplier prerequisite.

An ISO 27001 certification audit conducted while this gap is open would result in a **Major Nonconformity** against A.8.22 — a finding serious enough to prevent initial certification or cause suspension of an existing certificate.

**Corrective Action**

Move the database to a private AWS subnet with no direct inbound access from the DMZ. Web server communicates with the database only through a defined application API layer. Firewall rules replace Rule 3 with specific, justified permit rules for documented traffic flows only — all other DMZ→Internal traffic denied explicitly.

*Risk Score After Treatment: 2 (Medium) | Target: 14 days | Owner: Cloud Infrastructure Lead*

---

### Finding B: Shadow IT — Employee Mobile Hotspot Bypassing All Corporate Controls *(Risk Score: 6 — HIGH)*

**The Technical Flaw**

No Network Access Control (NAC) enforcement existed on corporate devices or network ports. Employees could — and in organizations without strong security awareness, routinely do — connect personal mobile hotspots to corporate laptops to bypass network speed or content restrictions. When this happens, the device routes corporate traffic over an unmonitored mobile data connection, completely outside the corporate network perimeter.

**ISO 27001 Control Mapping**

| Control | Title | Gap |
|---------|-------|-----|
| **A.8.20** | Networks security | No technical enforcement of approved connectivity paths |
| **A.8.21** | Security of network services | Traffic exits through uncontrolled, unapproved network service |
| **A.6.3** | Information security awareness | No documented awareness training on Shadow IT risk consequences |

**Business and Regulatory Impact**

When a corporate laptop routes traffic through a personal hotspot, **every DLP rule, proxy filter, and antivirus inspection the organization has invested in becomes irrelevant for that session.** Customer PII transmitted over an unmonitored mobile data connection is not subject to any of FastBuy's security controls.

PDPA Section 37(1) requires that a data controller implements *appropriate* security measures to protect personal data. Transmitting PII over an unmonitored, uncontrolled network path is inconsistent with that obligation — regardless of which network the employee chose to use. **The organization's PDPA liability does not diminish because the breach path ran through a personal SIM card rather than the corporate firewall.**

From an ISO 27001 perspective, this represents a gap in both technical controls (A.8.20) and people controls (A.6.3) — two different Annex A themes requiring two different remediation tracks.

**Corrective Action**

*Technical:* Deploy 802.1X Network Access Control on all switch ports — devices must authenticate before receiving network access. Implement endpoint DNS enforcement so corporate devices always route through corporate DNS regardless of physical connectivity.

*Organizational:* Mandatory security awareness training session specifically addressing Shadow IT risk, with signed employee acknowledgment. Update acceptable use policy to explicitly prohibit alternate connectivity without IT approval.

*Risk Score After Treatment: 2 (Medium) | Target: 30 days | Owner: IT Manager / CISO*

---

### Finding C: DMZ-to-Internal Firewall Rule Allows All Traffic *(CRITICAL)*

**The Technical Flaw**

Firewall Rule 3 — `PERMIT IP DMZ → INTERNAL ANY` — allows all IP traffic from the DMZ to the Internal Zone on any port. This rule was originally added as a temporary troubleshooting measure and was never removed after the connectivity issue was resolved. No change management process tracked its existence or required its review.

**ISO 27001 Control Mapping**

| Control | Title | Gap |
|---------|-------|-----|
| **A.8.20** | Networks security | Network not managed to protect information assets |
| **A.8.22** | Segregation in networks | Zone boundary rendered ineffective by unrestricted traversal rule |

**Business and Regulatory Impact**

The DMZ exists precisely to limit the blast radius of a compromised internet-facing service. Rule 3 eliminates that limitation entirely. A compromised web server becomes an unrestricted pivot point into the internal network — ERP systems, finance workstations, file servers, and internal admin interfaces are all directly reachable. The scope of a single web application breach expands from "the customer database" to "every internal system."

For FastBuy's PDPA obligations, this transforms a contained data-tier breach into an organization-wide data incident. For ISO 27001, a temporary troubleshooting rule that permanently eliminates zone segmentation is a Major Nonconformity against A.8.22.

**Root Cause (and the GRC lesson):** This finding illustrates a class of risk that technical vulnerability scanners rarely catch — not a software vulnerability, but a process failure. The rule passed syntax validation. The firewall functioned correctly. The gap was the absence of a change management process requiring justification and expiry dates for every firewall rule.

**Corrective Action**

Remove Rule 3 immediately. Replace with explicit, documented permit rules for each justified DMZ→Internal traffic flow. Implement quarterly firewall rule review — any rule without a documented justification and review date is flagged for removal.

*Owner: Network Security Engineer | Timeline: Immediate*

---

## 5. Executive Communication: The C-Level Action Plan

Each finding was translated into a business decision format for presentation to the FastBuy executive team. The structure for each item was: **what the risk is (one sentence), what we are asking for (effort estimate), and cost of action versus cost of inaction**.

> **Risk 001 — Network Re-Segmentation (CRITICAL — 14 days)**
> *What the risk is:* If the website is hacked, the database is hacked — they are on the same network.
> *What we are asking for:* 2 engineering days and a 4-hour deployment window to move the database to a private subnet.
> *Cost of action vs. inaction:* ~2 engineering days vs. mandatory PDPA public disclosure, penalties up to 5M THB, and reputational damage that ends early-stage e-commerce businesses.

> **Risk 002 — Shadow IT Controls (HIGH — 30 days)**
> *What the risk is:* Employees can route company data around all security controls using a personal phone. No technical control prevents this.
> *What we are asking for:* 3 days of IT time and a 1-hour staff training session.
> *Cost of action vs. inaction:* Minor tooling cost vs. a PDPA breach that does not become less severe because the data traveled over a personal SIM card.

> **Risk 004 — PDPA Compliance Clarification (HIGH — 30 days)**
> *What the risk is:* The organization may believe the payment gateway covers all compliance obligations. PDPA applies to all customer personal data, not only payment data.
> *What we are asking for:* Legal review and a Data Protection Impact Assessment for the checkout flow.
> *Cost of action vs. inaction:* Legal review hours vs. operating under a compliance misunderstanding that creates unquantified regulatory exposure.

The framing in every case was deliberate: the executive does not need to understand firewall rules. They need to understand what the risk costs if it materializes, and what it costs to fix it. That ratio — not the technical severity score — is what drives a budget decision.

---

## 6. Key Takeaways and Lessons Learned

**Network architecture assessment is a translation exercise, not a technical exercise.** The highest-value output of reviewing a firewall ruleset is not a list of misconfigurations. It is a document that tells a non-technical decision-maker: this rule means your 500,000-record customer database is reachable from the public internet via a single web application vulnerability, and here is what regulatory obligation that triggers. The technical finding and the business finding are different documents, and both are necessary.

**Risk Transfer does not extinguish regulatory liability.** FastBuy's decision to route payment processing through a PCI DSS-certified third-party gateway was correct — it removed the most burdensome compliance scope from the organization. But it did not transfer FastBuy's PDPA obligations for the customer PII collected before and alongside the payment step. Risk Transfer relocates financial and operational responsibility; it does not end the controller's accountability to regulators. Confusing the two is a governance risk in its own right, and it surfaced as a distinct finding in this assessment.

**The most dangerous findings are often process failures, not technical ones.** Rule 3 (`PERMIT IP DMZ → INTERNAL ANY`) did not exist because the firewall was broken. It existed because no process required its removal after a troubleshooting session. A technical control that cannot survive a routine change is not a control — it is a liability waiting for an engineer to have a bad day.

**A GRC practitioner's job is to make the cost of inaction visible.** Every finding in this assessment had a known, achievable fix. The obstacle was not knowledge — it was prioritization. Framing each fix in terms of regulatory consequence, financial exposure, and effort required is not spin — it is the information a decision-maker needs to allocate resources correctly. That translation, from technical severity to business consequence, is the core function of a GRC role.

---

*This case study was developed as part of a self-directed cybersecurity portfolio project. All organizations, systems, and data referenced are entirely fictional and created for educational purposes. Standard references: ISO/IEC 27001:2022; PDPA Thailand (B.E. 2562); OWASP Top 10 2021; ISO 31000:2018.*
