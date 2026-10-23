# Week 17: NIST CSF 2.0 Foundations and Web Security Fundamentals

> **Type:** Self-directed learning record (Monday, Wednesday, Friday)
> **Topics:** National Institute of Standards and Technology (NIST) Cybersecurity Framework (CSF) 2.0 Functions and Govern Categories; Hypertext Transfer Protocol (HTTP), Transport Layer Security (TLS), HTTP over TLS (HTTPS), and session-cookie fundamentals
> **Scenario:** One fictional Software as a Service (SaaS) startup, OrbitDesk, used for practice analysis only
> **Nature of the work:** Conceptual study and written analysis. No system was configured, built, tested, or assessed.

---

## Bottom Line Up Front

| Question | Answer |
|---|---|
| **What was studied?** | How CSF 2.0 organizes cybersecurity risk management into six Functions, with **Govern** as the cross-cutting one, and the web protocol basics (HTTP, HTTPS, TLS, cookies) that many technical control reviews rely on |
| **Why does it matter for Governance, Risk, and Compliance (GRC) work?** | Governance decisions such as policy, ownership, and supplier expectations are reviewable when supported by documented requirements, assigned responsibilities, approval records, and appropriate operational evidence. For technical controls, this may include observable system behavior, configuration records, logs, and test results |
| **What can be shown?** | Written explanations, comparison tables, and a fictional-scenario analysis that separates **technical impact**, **business impact**, and **possible regulatory or contractual consequences** |
| **What is not claimed?** | No professional assessment, production work, penetration test, or control deployment; no real organization; no legal conclusions |

---

## Executive Summary

This week combined two threads. The first (Monday and Wednesday) studied the six CSF 2.0 Functions and then the six Categories of the Govern Function, with a conceptual comparison to ISO/IEC 27001:2022, a standard published by the International Organization for Standardization (ISO) and the International Electrotechnical Commission (IEC). The second (Friday) reviewed how web applications communicate: HTTP methods, four status codes, the risks of unencrypted transport, what HTTPS and the TLS handshake provide and do not provide, and the introductory role of session cookies.

Both threads were connected through OrbitDesk, a fictional startup used to practice describing gaps, potential consequences, ownership, and initial actions.

---

## Study Overview

| Day | Topic | What was studied | Read more |
|---|---|---|---|
| **Monday** | CSF 2.0 overview and scenario practice | Six Functions; conceptual comparison with ISO/IEC 27001:2022; analysis of a fictional SaaS scenario | [WRITE-UP: Monday](02-write-up.md), [BUSINESS-IMPACT.md](03-business-impact.md) |
| **Wednesday** | CSF 2.0 Govern (GV) | Six Categories (GV.OC, GV.RM, GV.RR, GV.PO, GV.OV, GV.SC) and how Govern guides the other five Functions | [WRITE-UP: Wednesday](02-write-up.md) |
| **Friday** | HTTP and TLS fundamentals | Request-response model; six methods; status codes 401, 403, 404, 422; plaintext risks; HTTPS properties; TLS handshake; session cookies | [WRITE-UP: Friday](02-write-up.md), [Concept-to-GRC table](03-business-impact.md) |

---

## Repository Map

| File | Contents |
|---|---|
| **README.md** | This page: summary, study overview, takeaways, scope |
| [WRITE-UP.md](02-write-up.md) | Learning narrative for Monday, Wednesday, and Friday, with tables for Functions, Categories, methods, status codes, and TLS |
| [BUSINESS-IMPACT.md](03-business-impact.md) | Fictional scenario and assumptions, risk mapping table, impact areas, governance roles, proposed first actions, and the Concept-to-GRC table |
| [RESOURCES.md](03-resource.md) | Source index with official URLs, supporting concepts, and the result of a status check |

---

## How to Read This Repository

| Label | Meaning |
|---|---|
| **Study fact** | A concept summarized from the sources listed in [RESOURCES.md](04-resource.md) |
| **Scenario assumption** | A fictional detail about OrbitDesk, created for illustration |
| **Proposed action** | A recommendation written for analysis; not performed anywhere |

---

## Key Concepts and Takeaways

- **Govern is the cross-cutting Function.** It sets direction, accountability, policy, risk priorities, oversight, and supplier expectations that the other five Functions depend on.
- **CSF 2.0 and ISO/IEC 27001:2022 are related but not equivalent.** The CSF is a voluntary framework of outcomes; ISO/IEC 27001 specifies requirements for an information security management system and supports independent assessment.
- **401 and 403 answer different questions.** 401 concerns authentication (who are you); 403 concerns authorization (what may you do).
- **HTTPS protects data in transit, not application logic.** Broken access control and injection flaws remain possible over a valid TLS connection.
- **TLS version context matters.** TLS 1.0 and 1.1 are deprecated, TLS 1.2 and 1.3 differ in handshake mechanics, and Request for Comments (RFC) 9846 is now the current TLS 1.3 specification (it obsoletes RFC 8446).
- **A status code is a signal, not a verdict.** One response from one request is not conclusive evidence of a vulnerability.

---

## GRC and Foundational Web Security

| GRC activity | Web fundamental it depends on | Example review question |
|---|---|---|
| **Policy (GV.PO)** | Transport and session settings that a policy can state | Does policy define a minimum TLS version and session cookie settings? |
| **Roles (GV.RR)** | Ownership of certificate renewal and session configuration | Who renews TLS certificates, and who approves changes? |
| **Supplier risk (GV.SC)** | Third parties that terminate TLS or process requests | Which suppliers handle customer traffic or data in transit? |
| **Oversight (GV.OV)** | Observable artifacts such as response headers, TLS scan output, and logs | What evidence shows the stated control is operating? |

---

## Scope and Disclaimer

- **Self-directed educational work.** This repository records personal study. It is not professional advice and does not describe professional security work.
- **Fictional scenario.** OrbitDesk and all of its assumptions, gaps, and roles are invented for illustration. They are not a transcript of the original Monday exercise and do not describe any real organization.
- **Conceptual, not hands-on.** No server was configured, no application was built, no penetration test was performed, and no control was deployed.
- **No legal conclusions.** Any regulatory or contractual obligation mentioned is a potential obligation that would require verification.
- **Source status.** Selected source-status entries were rechecked on 23 October 2026; earlier checks and any remaining verification limits are noted in [RESOURCES.md](04-resource.md).

---

*This portfolio entry is part of a self-directed cybersecurity and GRC learning program.*
