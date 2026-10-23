# Business Impact and Risk Analysis: OrbitDesk (Fictional SaaS Startup)

> **Scope:** Business impact analysis supporting Governance, Risk, and Compliance (GRC) review, using one fictional startup
> **Scenario status:** OrbitDesk is entirely fictional. The gaps below are hypothetical, were not observed in any real system, and every recommendation is a **proposed action**, not completed work.
> **Method:** Qualitative analysis only. No numerical risk scores, likelihood percentages, or financial figures are used, because no scoring methodology was defined for this exercise.
> **Labels:** **Scenario assumption** (fictional detail) -- **Proposed action** (not performed) -- **Study fact** (summarized from the sources in [RESOURCES.md](04-resource.md))
> **Companion files:** [README.md](01-README.md) -- [WRITE-UP.md](02-write-up.md) -- [RESOURCES.md](04-resource.md)

---

## Bottom Line Up Front

| Impact area | Bottom line for OrbitDesk (fictional) |
|---|---|
| **Operational downtime** | The key downtime scenarios considered in this exercise are certificate expiry, an untested restore, and an unreviewed supplier dependency |
| **Customer-data exposure** | Broken tenant isolation or weak session handling could affect many customers at once, which differs in kind from a single transport gap |
| **Compliance uncertainty** | Obligations are unknown rather than absent; the first step is to establish which, if any, apply |
| **Customer trust** | Visible failures, such as browser warnings or an account takeover, are what customers notice first |
| **Reputation** | Follows from the other four areas and is not assessed on its own |

**Overall:** eight illustrative gaps (R1 to R8) cover all six Functions of the National Institute of Standards and Technology (NIST) Cybersecurity Framework (CSF) 2.0. The proposed first steps favor governance and visibility before technical review, because they set scope and ownership for everything else.

---

## 1. Scenario and Assumptions

| ID | Scenario assumption (fictional) |
|---|---|
| **A1** | OrbitDesk is a business-to-business (B2B) help-desk Software as a Service (SaaS) startup with 12 staff: a founder/CEO, a CTO, 5 engineers, a support lead, and 4 others in product, sales, and operations. The team is remote-first. |
| **A2** | The service is cloud-hosted with one public cloud provider (application servers, a managed database, and object storage). The provider is not named. |
| **A3** | Customers use a browser-based web application and a web Application Programming Interface (API) over Hypertext Transfer Protocol (HTTP) and, when encrypted with Transport Layer Security (TLS), HTTP over TLS (HTTPS). The service is multi-tenant: each customer organization is a tenant with two roles, Admin and Agent. |
| **A4** | Data held includes customer account details and authentication-related data (the exact password-storage design is unspecified), plus support tickets that may contain business information and some personal data about customers' own end users. |
| **A5** | Users log in with email and password, and the server then issues a session cookie. Multi-factor authentication (MFA) is available but not required. |
| **A6** | Third-party services include the cloud hosting provider, an email delivery service, and an error-monitoring service. |
| **A7** | There is no dedicated security role; the CTO holds informal responsibility for security. |
| **A8** | No legal, regulatory, or contractual obligation is assumed. Any that might apply would need verification with qualified advisers. |

---

## 2. Risk Mapping Table

| Security gap or scenario | Affected asset or process | Potential technical impact | Potential business impact | GRC review or control consideration | Suggested action or evidence to request |
|---|---|---|---|---|---|
| **R1 (Govern)** No written security policy and no named security owner; responsibility is informal (A7) | Governance and decision-making; all later control work | Controls applied inconsistently; no agreed baseline, such as a minimum TLS version or session settings | Slow or inconsistent decisions; unclear accountability if a customer asks who is responsible | GV.PO, GV.RR: are policy and ownership documented, approved, and communicated? | **Action:** name a security owner and a deputy; draft a short baseline policy.<br>**Evidence:** policy document, role assignments, approval record |
| **R2 (Govern)** Reliance on a cloud host, an email delivery service, and an error-monitoring service with no documented review of their security expectations (A6) | Supplier relationships | Availability and confidentiality depend on parties outside direct control, for example where error reports that may contain customer data are sent | An outage or exposure at a supplier can still affect OrbitDesk's customers; customers may ask how suppliers are governed | GV.SC: is there a supplier list, a review of each provider's assurance material, and a review of contract terms? | **Action:** create a supplier register; review each provider's published assurance material and contract terms.<br>**Evidence:** supplier register, review notes, contracts |
| **R3 (Identify)** No maintained inventory of hostnames, certificates, data types, and third-party services | Knowledge of assets and data | Forgotten or unmanaged endpoints and certificates; unclear where customer data is stored or sent | Surprise outages, such as an expired certificate; difficulty prioritizing work | ID.AM: is there a current inventory with named owners? | **Action:** build a lightweight inventory (a shared spreadsheet is enough to start).<br>**Evidence:** inventory showing owner, data type, and renewal date |
| **R4 (Protect)** TLS coverage has not been checked systematically: an older hostname is reachable over plain HTTP without a redirect, and certificate renewal is manual and unmonitored | Customer-facing and internal web endpoints; TLS certificates | Traffic on the plain-HTTP path could be read or altered in transit; an expired certificate would cause browser warnings or failed connections | Service interruption, reduced customer trust, and extra support load | PR.DS, GV.RR: is encrypted transport defined in policy, and who owns certificate renewal? | **Action:** review every hostname for HTTP and HTTPS behavior and TLS settings; assign a renewal owner and expiry reminders.<br>**Evidence:** TLS scan output, hostname list, redirect check results, renewal records |
| **R5 (Protect)** Session handling and access control have not been formally reviewed: cookie attributes, session lifetime, cross-tenant authorization checks, and optional MFA for administrators (A5) | Login, sessions, and tenant isolation | Session theft or reuse; broken access control that exposes one tenant's data to another | Customer-data exposure, account takeover, and loss of customer confidence | PR.AA: are authentication, session, and authorization rules defined and tested? | **Action:** review Set-Cookie attributes and the session lifecycle; write authorization test cases for cross-tenant access; consider requiring MFA for administrators.<br>**Evidence:** sample response headers, test results, role and permission matrix |
| **R6 (Detect)** Logs exist per component but are not reviewed together, so unusual patterns, such as bursts of 401 or 403 responses, might not be noticed promptly | Logging and monitoring | Delayed awareness of credential attacks or misconfiguration | Longer exposure window and harder investigation | DE.CM: which logs are collected, retained, and reviewed? Status-code patterns are signals, not proof | **Action:** define minimum log sources and a simple review routine; consider basic alert thresholds.<br>**Evidence:** log source list, retention settings, a sample review record |
| **R7 (Respond)** No documented incident response plan or decision authority | Incident handling and communication | Inconsistent containment and evidence handling | Slower response; confusion over who informs customers and when; possible obligations unclear (A8) | RS.MA, GV.RR: is there a plan with roles, contacts, and decision authority? | **Action:** write a one-page plan with roles and contacts; hold a short tabletop discussion.<br>**Evidence:** the plan, contact list, tabletop notes |
| **R8 (Recover)** Database backups are configured, but no restore has been tested | Production data and service availability | Backups may be unusable or incomplete when needed | Extended downtime or data loss after an incident or failure | RC.RP: has recovery been exercised, and are recovery priorities defined? | **Action:** schedule a restore test into a separate environment and record the time and result.<br>**Evidence:** restore test record, backup configuration |

*The CSF Category mapping is illustrative and chosen for study purposes. Confirm Category wording against NIST CSWP 29 ([RESOURCES.md](04-resource.md)).*

---

## 3. Impact Areas: Technical, Business, and Possible Regulatory or Contractual Consequences

| Impact area | Technical impact | Business impact | Possible regulatory or contractual consequence (verification required) |
|---|---|---|---|
| **Operational downtime** | An expired certificate, a failed restore, or an unavailable supplier prevents users from reaching or using the service | Lost working time for customers' support teams; higher support workload | Service-level terms in customer agreements might apply if such terms exist (none assumed in A8) |
| **Customer-data exposure** | Cross-tenant access, intercepted traffic, or a stolen session could expose ticket or account data | Customer concern, investigation effort, and possible loss of contracts | Data-protection or breach-notification obligations may apply depending on the data involved, customer locations, and agreements; requires verification with qualified advisers |
| **Compliance uncertainty** | No policy, inventory, or evidence trail to show what is in place | Difficulty answering customer security questionnaires; slower sales cycles | It is unknown which requirements apply; establishing which obligations exist is a first step |
| **Customer trust** | Visible browser warnings, inconsistent behavior, or account takeover | Customers question reliability and care | Any security commitments made in contracts could be tested |
| **Reputation** | Public discussion of an outage or incident | Harder to win new customers | Not a regulatory matter by itself; interacts with the other four areas |

---

## 4. Governance Responsibilities

| Role (assumed) | Responsibility in this scenario | CSF link (illustrative) |
|---|---|---|
| **Founder / CEO** | Approves risk priorities and resourcing; accepts or declines residual risk | GV.RM, GV.RR |
| **CTO (informal security owner, A7)** | Maintains the baseline policy, coordinates reviews, and reports to the CEO | GV.PO, GV.OV |
| **Engineering team (5)** | Follows policy in code and configuration; writes authorization test cases; renews certificates under an assigned owner | PR.AA, PR.DS, ID.AM |
| **Support lead** | Handles customer communication during incidents; holds the supplier contact list | RS.CO, GV.SC |

---

## 5. Initial Action Items (Proposed, Not Performed)

The sequence is a proposed order of work, **not a risk score**.

| Sequence | Proposed action | Why in this order | Related gaps |
|---|---|---|---|
| 1 | Name a security owner and a deputy; document roles | Accountability has to exist before other work can be assigned | R1, R7 |
| 2 | Draft a short baseline policy covering access, transport encryption, sessions, and supplier use | Gives later reviews a stated standard to test against | R1 |
| 3 | Build a lightweight inventory of hostnames, certificates, data types, and suppliers; identify which suppliers require closer review of security assurance material, data handling, and relevant contractual terms | Defines the scope of later reviews and identifies supplier relationships requiring follow-up | R2, R3 |
| 4 | Review transport and certificate coverage; assign a certificate renewal owner | Addresses a visible availability and trust exposure | R4 |
| 5 | Review session settings and cross-tenant authorization | Targets a potentially high-impact path for unauthorized cross-tenant data exposure | R5 |
| 6 | Define a minimal log review routine, a one-page response plan, and a restore test | Establishes detection, response, and recovery basics | R6, R7, R8 |

---

## 6. Concept-to-GRC Mapping Table

| Concept | Business risk if weak or unreviewed | Control-review consideration | Evidence an analyst may request |
|---|---|---|---|
| **HTTP (unencrypted)** | Traffic can be read or altered in transit; credentials and session identifiers can be exposed | Is any credential-bearing or customer-data traffic allowed over plain HTTP? | List of hostnames with observed HTTP and HTTPS behavior; redirect test results |
| **HTTPS / TLS** | A weak or outdated configuration reduces protection; treating HTTPS as proof that the application is safe creates false assurance | Is a minimum TLS version defined by the organization and applied consistently? Is HTTPS treated as one control rather than proof of application security? | TLS configuration scan output; policy statement of the minimum version |
| **TLS certificates** | Expiry causes outages and browser warnings; exposure of a private key undermines server authentication | Who owns renewal? Is expiry monitored? Is access to private keys limited? | Certificate inventory; renewal records; expiry alert settings |
| **Session cookies** | A stolen or reusable session identifier can allow account takeover without knowing the password | Are Secure, HttpOnly, and SameSite set deliberately? Is the session identifier renewed at login and ended on logout or timeout? | Sample Set-Cookie headers; session management standard; timeout settings |
| **Authentication** | Weak or missing MFA on privileged accounts increases account takeover exposure | Which accounts require MFA? How are repeated failed logins handled? | Authentication standard; MFA enforcement list; description of failed-login handling |
| **Authorization** | In a multi-tenant application, broken access control can expose one customer's data to another | Are roles defined? Is tenant isolation tested at the object level? | Role and permission matrix; authorization test cases and results; code review records |
| **HTTP status-code behavior** | Inconsistent or overly detailed responses can leak information or hide problems, and patterns can signal issues | Are 401, 403, 404, and 422 used consistently? Are trends in 401 and 403 reviewed? A status code is a signal, not proof of a vulnerability | Sample API responses; log extracts showing status-code trends; error-handling guideline |

---

## Limits of This Analysis

- **No scoring.** No numerical risk scores, likelihood percentages, or financial losses are used or implied.
- **HTTPS is not proof of a safe application.** It protects data in transit between TLS endpoints and does not address application logic, access control, or injection flaws.
- **Status codes are signals.** One code from one request is not conclusive evidence of a vulnerability.
- **Fictional and conditional.** OrbitDesk, its gaps, and its assumptions are invented for study. Recommendations are proposals, and any regulatory or contractual obligations would require verification.

---

## References

Sources, official URLs, and status checks are listed in [RESOURCES.md](04-resource.md).

---

*Return to: [README.md](01-README.md)*
