# Week 18: NIST CSF 2.0 Identify and Protect, and DNS Security -- A GRC Learning Record

> **Purpose:** A self-directed learning record showing how governance concepts connect to Domain Name System (DNS) security, written for review by hiring managers
> **Topics:** National Institute of Standards and Technology (NIST) Cybersecurity Framework (CSF) 2.0 Identify and Protect Categories; DNS architecture, threats, and security mechanisms; Governance, Risk, and Compliance (GRC) mapping and evidence; concepts from the International Organization for Standardization (ISO) and International Electrotechnical Commission (IEC) standard ISO/IEC 27001:2022
> **Scenario:** One fictional online retailer, TrailMint, used for practice analysis only
> **Nature of the work:** Conceptual study and written analysis. No tools were run, no real environment was assessed, and no recommendation was carried out.

---

## Bottom Line Up Front

| Question | Answer |
|---|---|
| **What was studied?** | CSF 2.0 Identify (ID.AM, ID.RA) and Protect (PR.AA, PR.AT, PR.DS, PR.PS, PR.IR), plus how DNS works, how it is threatened, and which mechanisms address those threats |
| **Why does it matter?** | DNS is a shared dependency for web, email, and application programming interfaces (APIs). Protecting it depends on governance basics: knowing what exists, who owns it, who can change it, and what evidence shows controls operate. |
| **What can be shown?** | Conceptual explanations, a **defined qualitative prioritization** of nine fictional risks, a **three-tier evidence model** applied to DNS controls, and three fictional exercises |
| **What is not claimed?** | No professional assessment, audit, or live finding; no tool execution; no completed corrective action. TrailMint is fictional. |

---

## Executive Summary

Monday and Wednesday covered the NIST CSF 2.0 Functions that sit before and around an incident. **Identify** (ID.AM and ID.RA) explained why asset visibility, ownership, and risk assessment come first, and why a vulnerability is not the same as a business risk. **Protect** (five Categories) connected security requirements to responsibilities, operating practice, and review, including the identity lifecycle.

Friday applied those ideas to DNS. The study covered resolution pathways, caching, five record types, five threats (domain hijacking, cache poisoning, tunneling, subdomain takeover, and outages), and the mechanisms that address them. Each mechanism was described with its **purpose, limits, owner, and evidence**, so that no single control is mistaken for a complete answer.

---

## Study Overview

| Day | Topic | What was studied | Read more |
|---|---|---|---|
| **Monday** | CSF 2.0 Identify | ID.AM and ID.RA; asset categories and inventory purpose; ownership and ISO/IEC 27001 concepts; vulnerability assessment versus risk assessment | [WRITE-UP: Part A](WRITE-UP.md#part-a-nist-csf-20-identify-monday) |
| **Wednesday** | CSF 2.0 Protect | PR.AA, PR.AT, PR.DS, PR.PS, and PR.IR; the identity lifecycle; the path from requirement to review | [WRITE-UP: Part B](WRITE-UP.md#part-b-nist-csf-20-protect-wednesday) |
| **Friday** | DNS security and GRC mapping | Resolution and caching; five common record types covering addresses, aliases, mail routing, and text data; five threats; security mechanisms; evidence mapping | [Part C](WRITE-UP.md#part-c-dns-fundamentals-friday), [Part E](WRITE-UP.md#part-e-dns-threat-analysis-friday), [Part F](WRITE-UP.md#part-f-dns-security-controls-friday), [Part G](WRITE-UP.md#part-g-evidence-mapping) |

---

## Repository Map

| File | Contents |
|---|---|
| **README.md** | This page: summary, overview, frameworks, mechanisms, competencies, scope |
| [WRITE-UP.md](WRITE-UP.md) | The principal learning document: Parts A to H covering Identify, Protect, DNS fundamentals, record types, threats, controls, evidence mapping, and three fictional exercises |
| [BUSINESS-IMPACT.md](BUSINESS-IMPACT.md) | Fictional scenario and assumptions, a [prioritization framework](BUSINESS-IMPACT.md#2-risk-prioritization-framework), a [risk mapping](BUSINESS-IMPACT.md#3-risk-mapping) of nine risks, governance roles, and an [executive communication example](BUSINESS-IMPACT.md#7-executive-communication-example) |
| [RESOURCES.md](RESOURCES.md) | Source index with verification notes, glossary, interview-preparation questions, and optional further practice |

---

## Frameworks and Concepts Covered

| Framework or concept | How it is used |
|---|---|
| **NIST CSF 2.0** | Describes cybersecurity outcomes, risk activities, and governance responsibilities, through the Identify and Protect Categories |
| **ISO/IEC 27001:2022** | Reference for information security management system requirements and Annex A controls. Mappings are illustrative, and the standard is **not equivalent** to the CSF. |
| **Three-tier evidence model** | Design Evidence, Operating Evidence, and Operating Effectiveness Evidence, applied consistently to DNS controls |
| **Qualitative risk prioritization** | Defined criteria and High, Medium, and Low levels, with reasoning per risk and no numerical scores |
| **Supporting concepts** | Asset inventory and ownership, vulnerability versus risk, identity lifecycle, supplier governance |

---

## Security Mechanisms Reviewed

These were studied conceptually. No mechanism was configured or tested.

| Mechanism | What it addresses | Key limit noted |
|---|---|---|
| **DNSSEC** (DNS Security Extensions) | Authenticity and integrity of signed DNS data | Does not encrypt queries or stop a compromised account from making valid changes; errors can break resolution |
| **DNS filtering (Protective DNS)** | Access to destinations classified as harmful | Does not stop every threat and depends on classification quality |
| **Registrar account multi-factor authentication (MFA)** | Unauthorized login to the account that controls registration | Does not govern records at a separate DNS provider |
| **Domain and transfer locking** | Specified registry operations such as transfer, update, and deletion | Effect depends on the registrar and the exact lock type |
| **DNS change control** | Unauthorized or erroneous record changes | Does not stop a compromised approver |
| **DNS logging and monitoring** | Visibility for detection and investigation | Detects rather than prevents; logs must be retained and reviewed |
| **Availability and recovery** | Effect of a DNS failure | Does not address integrity or unauthorized changes |

---

## Competencies Demonstrated Through This Portfolio

| Competency | Where it is shown |
|---|---|
| **Explaining technical concepts in business terms** | [WRITE-UP: Parts C to F](WRITE-UP.md#part-c-dns-fundamentals-friday); [BUSINESS-IMPACT: executive example](BUSINESS-IMPACT.md#7-executive-communication-example) |
| **Risk-based reasoning with transparent criteria** | [BUSINESS-IMPACT: Sections 2 to 4](BUSINESS-IMPACT.md#2-risk-prioritization-framework) |
| **Governance awareness** (ownership, lifecycle, suppliers) | [WRITE-UP: Part B](WRITE-UP.md#part-b-nist-csf-20-protect-wednesday); [BUSINESS-IMPACT: Section 6](BUSINESS-IMPACT.md#6-governance-responsibilities) |
| **Evidence literacy** (what to request and what it does not show) | [WRITE-UP: Part G](WRITE-UP.md#part-g-evidence-mapping) |
| **Accuracy about control limits** | [WRITE-UP: Part F](WRITE-UP.md#part-f-dns-security-controls-friday) |
| **Source checking and honesty about uncertainty** | [RESOURCES.md](RESOURCES.md) |

---

## Key Takeaways

- **Visibility comes before risk assessment.** An asset missing from the inventory may be overlooked during subsequent risk assessment, control reviews, and ownership activities. A vulnerability alone does not establish business risk.
- **A policy or configuration does not show that a control works.** The three evidence tiers separate what was designed, what was done, and what held over time.
- **Registrar security, domain locks, DNSSEC, and change control address different risks.** None replaces the others.
- **DNSSEC does not encrypt queries.** It also does not stop a compromised but authorized account from making valid changes.
- **A stale-looking DNS record does not establish a subdomain takeover.** The risk needs specific conditions, so the right response is to gather evidence before concluding.
- **Source status matters.** The DNSSEC core documents are updated by later Requests for Comments (RFCs), and NIST SP 800-81 Revision 3 is the current DNS deployment guide.

---

## Scope, Limitations, and Disclaimer

- **Self-directed educational work.** This repository records personal study. It is not professional advice and does not describe professional security work.
- **Fictional scenario.** TrailMint, its hostnames, and all of its assumptions, gaps, and roles are invented for illustration. They do not describe any real organization.
- **Conceptual, not hands-on.** No DNS lookup, scanning, or testing tool was run, and no DNS, DNSSEC, or registrar setting was configured.
- **No audit or live findings.** No audit, formal assessment, verified vulnerability, real incident, or completed corrective action is claimed.
- **Mappings are illustrative.** NIST and ISO mappings are reasoned, not established by an official source.
- **No legal conclusions.** Any regulatory, contractual, or service-level obligation mentioned is potential and would require verification.
- **Source verification.** Source statuses and their limits are in [RESOURCES.md](RESOURCES.md). The paid ISO standards were not accessed.

---

*This portfolio entry is part of a self-directed cybersecurity and GRC learning program.*
