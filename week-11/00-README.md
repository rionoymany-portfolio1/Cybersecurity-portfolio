# Week 11: ISO/IEC 27001:2022 Foundations & Network Security Fundamentals

> **First GRC Week — Learning to Read a Standard, Not Just Follow It**

---

## Context: Why This Week Marks a Shift

From this week onward, the portfolio reflects a blended track: approximately **70% GRC / 30% technical**, with content weighted toward governance, risk, and compliance work. The technical weeks that came before this one are not abandoned — they are the foundation that makes GRC work credible. A GRC analyst who cannot explain why FTP on port 21 violates a cryptography control, or what a network segmentation gap looks like in a firewall rulebook, cannot audit those controls effectively. This week makes that connection explicit.

---

## Topics Covered This Week

### ISO/IEC 27001:2022 — Clauses 4 through 6
Read directly from the official standard document. Focus on understanding the *intent* behind each clause, not just its words.

| Clause | Title | What It Governs |
|--------|-------|-----------------|
| 4.1 | Understanding the organization and its context | Internal and external factors affecting the ISMS |
| 4.2 | Understanding the needs and expectations of interested parties | Stakeholder requirements |
| 4.3 | Determining the scope of the ISMS | What is — and is not — inside the ISMS boundary |
| 4.4 | Information security management system | The ISMS itself as a system |
| 5.1 | Leadership and commitment | Top management's active role |
| 5.2 | Policy | Information security policy requirements |
| 5.3 | Organizational roles, responsibilities and authorities | Who is accountable for what |
| 6.1 | Actions to address risks and opportunities | Risk assessment and treatment |
| 6.2 | Information security objectives | How objectives are set and measured |
| **6.3** | **Planning of changes** | **New in 2022 — planned ISMS changes must be evaluated** |

### Networking Fundamentals
OSI 7-Layer Model and TCP/IP Model, studied through a GRC lens: not "how to configure a router" but "how to audit a network control."

### Applied GRC Simulation
Fifteen case-study scenarios blending ISO 27001 clause requirements against simulated organizational findings, practiced through architectural analysis and log review.

---

## Key Learnings This Week

- **Reading a standard is a skill, not just reading comprehension.** Clause 4.1 says "the organization shall determine external and internal issues relevant to its purpose." That sentence is doing a lot of work — it is asking an organization to define what *its* context is before deciding what to protect. Not every organization scopes its ISMS the same way, and the standard is deliberately flexible. Learning to interpret that flexibility is what separates a practitioner from someone who just memorizes clause numbers.
- **Scope (Clause 4.3) is the most consequential decision in any ISMS implementation.** A scope that is too broad makes certification impractical; a scope that is too narrow creates a false sense of coverage. The Cloud shared-responsibility model is a direct example: a company using AWS cannot scope out its own application layer just because the infrastructure sits on Amazon's servers — and a scope statement that implies otherwise will not survive audit scrutiny.
- **Clause 6.3 exists because organizations routinely broke their ISMS by changing things without re-evaluating risks first.** A cloud migration, a network re-architecture, an acquisition — any planned change to the ISMS itself must now be managed with the same rigor as an initial risk assessment. The 2022 revision added this clause precisely because the 2013 version was silent on it and organizations were treating ISMS documentation as static.
- **The Three Lines Model is a mental map for understanding accountability, not a rigid org-chart.** First line (operations — the people who build and run systems) owns the risks day-to-day. Second line (risk management and compliance functions, including information security teams) provides oversight, policy, and monitoring without being operationally responsible for the outcome. Third line (internal audit) provides independent assurance to the board and senior management. The model matters for GRC because it clarifies who a finding is directed at: a firewall misconfiguration is a first-line failure; a missing policy is a second-line failure; missing audit coverage is a third-line failure.
- **Network knowledge is not optional for a GRC analyst.** ISO 27001 Annex A.8.20 (Network Security) requires controls on network segmentation, monitoring, and service restriction. Auditing whether those controls exist requires knowing what VLAN separation actually means in a firewall ACL, what "least privilege" looks like in a routing rule, and why FTP on port 21 violates A.8.24 (Use of Cryptography) while SFTP on port 22 satisfies it. Without that foundation, a GRC analyst can only verify that a policy exists — not whether it is actually implemented.
- **The OSI model is a diagnostic tool for identifying where a security control operates.** A WAF is a Layer 7 (Application) control. A firewall ACL enforces rules at Layer 3 (Network) and Layer 4 (Transport). Physical access controls operate at or below Layer 1. When a non-technical stakeholder proposes a CCTV camera as a mitigation for a database intrusion risk, the OSI layer distinction is what allows a GRC analyst to explain precisely why that control addresses a different threat at a different layer — and what Layer 3–7 controls are actually needed.

---

## Framework for GRC Weeks

GRC content is structured differently from technical weeks. Each GRC-focused file uses the following analytical lens where applicable:

1. **Requirement** — what the standard, law, or framework actually says
2. **Interpretation** — what it means in practice, translated out of standards language
3. **Organizational Application** — how a real organization implements this, with a simulated or illustrative case
4. **Evidence / Artifacts** — what documentation an auditor would expect to see
5. **Common Gaps** — where organizations most frequently fall short
6. **Related Controls** — connections to Annex A controls, other frameworks (NIST, PDPA, etc.), or other clauses

This framework replaces the pentest 6-part structure (Vulnerability → Exploitation → Business Impact → Technical Fix → Policy Fix → Detection) for GRC-dominant weeks. Some weeks will blend both, depending on content.

---

## Files This Week

```
week-11/
├── 00-README.md                                    (this file)
├── 01-iso27001-clauses-4-6-analysis.md             (clause-by-clause breakdown with GRC framework)
├── 02-isms-scope-and-context-simulation.md         (practical scoping exercise + risk register draft)
├── 03-network-fundamentals-for-grc.md              (OSI + TCP/IP through an audit lens)
├── 04-network-security-audit-writeup.md.md         (15-scenario simulation: log analysis, topology, ACL review)
└── 05-resources.md                                 (references: ISO standard, PDPA, OWASP, IIA Three Lines)
```

