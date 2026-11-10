# Business Impact and Risk Analysis: TrailMint (Fictional Online Retailer)

> **Scope:** Business impact and risk reasoning for Governance, Risk, and Compliance (GRC) review, using one fictional organization and the Domain Name System (DNS) as the focus
> **Scenario status:** TrailMint is entirely fictional. The gaps are hypothetical, were not observed in any real system, and every recommendation is a **proposed action that has not been performed**.
> **Method:** Qualitative prioritization against defined criteria (Section 2). No numerical risk scores, likelihood percentages, financial losses, or corrective-action service levels are used.
> **Companion files:** [README.md](01-README.md) -- [WRITE-UP.md](02-write-up.md) -- [RESOURCES.md](04-resources.md)

---

## Bottom Line Up Front

| Question | Bottom line for TrailMint (fictional) |
|---|---|
| **What is at risk?** | TrailMint's ability to be found and reached. The web store, email, customer accounts, and application programming interface (API) all depend on DNS and on the accounts that control it. |
| **What matters most?** | Knowing what exists, **who can change DNS and registration**, and whether DNS stays available. Five of nine risks are prioritized **High** for these reasons. |
| **What is uncertain?** | Whether any gap can actually be exploited, which obligations apply, and what safeguards really operate. The scenario assumes no evidence for any of these. |
| **What is proposed?** | Governance and visibility first (inventory, ownership, access review), then DNS-specific safeguards and evidence requests. Nothing has been carried out. |

---

## 1. Scenario and Assumptions

| ID | Scenario assumption (fictional) |
|---|---|
| **A1** | TrailMint is an online retailer of outdoor gear with 25 staff: a chief executive officer (CEO) who founded the company, an operations manager, an information technology (IT) lead, 3 developers, a marketing lead with 3 marketing staff, a customer service lead with 4 agents, and 10 others in warehouse, logistics, and finance. |
| **A2** | Customers shop on a web store hosted by a third-party e-commerce platform. Customer accounts, order history, and an API run on one public cloud provider. All public hostnames sit under one primary domain, `trailmint.example` (an illustrative name). |
| **A3** | The primary domain is registered with one commercial registrar. Authoritative DNS is hosted by a **separate managed DNS provider** with no secondary service. DNS Security Extensions (DNSSEC) are **not enabled**, and a decision on enabling them is pending. |
| **A4** | Business email uses a hosted email provider (mail exchange records) and a marketing email service. Email policies, such as Sender Policy Framework (SPF), are published as text records. |
| **A5** | Two marketing subdomains, `promo` and `events`, are aliases to external landing-page and event-registration services. |
| **A6** | Data held includes customer account and authentication data, order history, and customer service correspondence. The design for storing authentication data is outside the scope of this scenario and is not assumed. Payment processing is also outside the scope. |
| **A7** | There is no dedicated security staff. The IT lead is the informal security owner, the operations manager administers the registrar account, and the marketing lead manages marketing subdomain content. |
| **A8** | Suppliers include the registrar, the managed DNS provider, the public cloud provider, the e-commerce platform, the hosted email provider, and the marketing and event services. |
| **A9** | No legal, regulatory, contractual, or service-level obligation is assumed. The online store is treated as revenue-critical to TrailMint. Any obligation that might apply would need verification. |

---

## 2. Risk Prioritization Framework

**Priority is the proposed order of governance attention.** It is a qualitative judgment against the criteria below, not a score, a likelihood, or a prediction. It reflects TrailMint's ability to act, not the general seriousness of a threat.

| ID | Criterion | Question asked |
|---|---|---|
| **C1** | Impact on confidentiality, integrity, and availability | What could be affected, and how widely? |
| **C2** | Business criticality of affected assets | Does it touch the revenue-critical store, email, or customer accounts? |
| **C3** | Exposure and plausible threat conditions | Do the scenario's conditions make the event plausible, or does it need further conditions that are not confirmed? |
| **C4** | Existing safeguards and evidence of their operation | Does the scenario include evidence that safeguards operate? |
| **C5** | Dependencies, commitments, and recovery needs | Do suppliers, commitments, or recovery needs raise the stakes? (No commitments are assumed; see A9.) |

| Level | Meaning |
|---|---|
| **High** | Potential impact is broad (many hostnames, services, or customers) or touches a revenue-critical asset, plausible conditions exist in the scenario, and the scenario shows no evidence that safeguards operate. Proposed for early attention. |
| **Medium** | Potential impact is significant but narrower, or depends on further conditions that are not confirmed, or safeguards are partly in place. Proposed for planned attention. |
| **Low** | TrailMint has limited ability to change the exposure directly, or the impact is narrow, or the relevant safeguards sit largely outside its control. Proposed for monitoring and periodic review. |

---

## 3. Risk Mapping

The National Institute of Standards and Technology (NIST) Cybersecurity Framework (CSF) 2.0 and the International Organization for Standardization (ISO) and International Electrotechnical Commission (IEC) standard ISO/IEC 27001:2022 are **not equivalent**. The mappings below are reasoned and illustrative, with the reason for each given.

### 3.1 Risk Context and Framework Mapping

| Risk ID | Scenario or security gap | Affected asset or service | Potential technical impact | Potential business impact | NIST CSF 2.0 Category (illustrative) | ISO/IEC 27001:2022 concept or control (illustrative, with reason) |
|---|---|---|---|---|---|---|
| **R1** | **Incomplete or outdated asset inventory:** no entries for the registrar account, the managed DNS provider account, the marketing email service, or the external services behind the `promo` and `events` subdomains | Inventory and risk assessment scope | Unknown dependencies and accounts fall outside access reviews, monitoring, and supplier review | Surprise outages or exposure; no accountable owner; slower answers to customer questions | ID.AM; supports ID.RA | A.5.9 Inventory of information and other associated assets (assets and owners are known); Clause 6.1.2 (risk assessment depends on knowing the assets) |
| **R2** | **Weak access management or unremoved access:** a former contractor's account and a former role's DNS edit rights remain active, and no periodic review is documented | DNS provider and marketing service accounts | An account that is no longer needed can change records, or be misused if its credentials are exposed | Misdirected traffic or email; disruption; loss of confidence | PR.AA | A.5.16 Identity management; A.5.18 Access rights (provision, review, modify, remove); A.8.2 Privileged access rights (accounts that change DNS are privileged) |
| **R3** | **DNS (domain) hijacking:** unauthorized control over the domain registration or delegation, for example through the registrar account, whose multi-factor authentication (MFA) and lock status are not documented | Domain registration and delegation | Changed delegation or records; redirected web traffic and email | Interrupted sales and email; customers sent to unauthorized destinations; effort to regain control | PR.AA; GV.SC | A.8.5 Secure authentication (registrar login); A.5.19 and A.5.22 (the registrar is a supplier whose service is reviewed) |
| **R4** | **DNS cache poisoning:** incorrect data accepted into a resolver's cache. This sits mostly outside TrailMint's control, and DNSSEC is not enabled (A3) | Resolvers used by customers and staff | Wrong answers for TrailMint's names until cached entries expire | Customers misdirected; hard to see from TrailMint's side | PR.DS (integrity of data); PR.IR | A.8.21 Security of network services (DNS is a network service); A.8.24 Use of cryptography (DNSSEC relies on digital signatures) |
| **R5** | **DNS tunneling:** a compromised internal device could carry unauthorized communication in DNS messages, and DNS logs are not reviewed | Internal network and outbound DNS | A covert channel; data transferred without notice | Possible data loss and delayed detection | DE.CM | A.8.15 Logging; A.8.16 Monitoring activities; A.8.20 Networks security |
| **R6** | **Subdomain takeover:** the `promo` alias points to an external service that is no longer used, and whether the external name can be claimed is unconfirmed | Marketing subdomains and zone records | Unauthorized content under a trusted hostname, if the required conditions apply | Brand misuse; phishing under a trusted name; customer confusion | ID.AM; PR.PS | A.5.9 (external services tied to hostnames are assets and dependencies); A.8.9 Configuration management (records are configuration) |
| **R7** | **DNSSEC deployment errors:** if DNSSEC is enabled (decision pending, A3), mismatched delegation data, expired signatures, or mishandled key changes could make lookups fail at validating resolvers | DNS zone configuration and delegation | Legitimate names fail validation | Store and email unreachable for affected users | PR.PS; PR.IR | A.8.32 Change management; A.8.9 Configuration management; A.8.24 Use of cryptography (key management) |
| **R8** | **DNS service outage:** a single managed DNS provider with no secondary service, untested recovery, and untracked renewal dates | Authoritative DNS and domain registration | Name lookups fail although servers may be running | Interrupted sales, email, and support; recovery effort | PR.IR; RC.RP | A.8.14 Redundancy of information processing facilities; A.5.30 ICT (information and communication technology) readiness for business continuity; A.5.22 (monitoring supplier services) |
| **R9** | **Unauthorized DNS record changes:** no documented approval or review for changes within the managed DNS service | DNS records and managed DNS provider account | Records altered without approval; changes not traceable | Disruption or redirection; difficulty investigating | PR.AA; PR.PS; DE.CM | A.8.32 Change management; A.8.9 Configuration management; A.8.15 Logging |

R9 focuses on unauthorized DNS record changes within the managed DNS service, rather than changes to domain registration or delegation covered by R3.

### 3.2 Proposed Treatment, Evidence, Ownership, and Priority

| Risk ID | Proposed risk treatment (not performed) | Evidence to request | Accountable role | Priority |
|---|---|---|---|---|
| **R1** | Build and maintain an inventory with owners, data types, and renewal dates, covering accounts, suppliers, and subdomains | Inventory export; owner assignments; DNS zone export reconciled to the inventory | IT lead, with asset owners | **High** |
| **R2** | Reconcile account lists to current staff and contractors; remove access no longer needed; define roles; require MFA; schedule periodic review | Before and after account lists; review records; provider audit trail | IT lead; operations manager | **High** |
| **R3** | Require MFA and documented recovery contacts on the registrar account; apply appropriate transfer and update locks that the registrar offers; track renewals; treat the registrar as a critical supplier | MFA setting; lock status shown by the registrar; renewal and contact records; supplier register entry | Operations manager | **High** |
| **R4** | Document a decision on DNSSEC signing; keep any corporate resolvers maintained; accept that customers' resolvers are outside TrailMint's control | DNSSEC decision record; resolver patch and configuration records | IT lead | **Low** |
| **R5** | Define DNS logging and a review routine; restrict outbound DNS to approved resolvers; consider DNS filtering | Log source list; retention settings; alert rules; review records | IT lead | **Medium** |
| **R6** | Add DNS cleanup to the service decommissioning checklist; review subdomain records against the inventory; remove records that point to unused external resources, after approval | Zone export; decommissioning records; review records | IT lead, with the marketing lead | **Medium** |
| **R7** | If DNSSEC is enabled: a written deployment and key-management procedure; staged changes with review and a rollback plan; validation monitoring | Procedure; change approvals; validation monitoring records | IT lead; DNS provider | **Medium** |
| **R8** | Review redundancy options, including a secondary provider; track expiry dates; test recovery steps. Any secondary DNS arrangement should be tested for configuration consistency, failover behavior, and recovery readiness before being relied upon. | Architecture description; provider availability reports; expiry tracker; recovery test record; evidence of configuration consistency and failover testing | IT lead; operations manager | **High** |
| **R9** | A written DNS change procedure with approval; review of the provider audit trail against approvals; alerts on changes | Procedure; change tickets with approvals; reconciliation records | IT lead | **High** |

---

## 4. Why Each Risk Is Prioritized

| Risk ID | Priority | Reasoning against the criteria |
|---|---|---|
| **R1** | **High** | An incomplete inventory does not directly cause an incident, but it increases the chance that important assets, dependencies, and security responsibilities will be missed during subsequent reviews. The missing entries relate to revenue-critical services (C2), and the scenario shows no inventory evidence for them (C4). |
| **R2** | **High** | Accounts that can change DNS or registration affect integrity and availability widely (C1, C2). The scenario includes unremoved access and no review evidence (C4). |
| **R3** | **High** | Control of registration affects every hostname, including the store and email (C2). Registrar security is not documented (C4), and plausible conditions depend on account security and recovery processes (C3). |
| **R4** | **Low** | The exposure sits mainly with resolvers operated by others, so TrailMint's ability to act is limited (C3). DNSSEC deployment and validation risks are addressed separately under R7. **Low reflects TrailMint's ability to act, not the general seriousness of the threat.** |
| **R5** | **Medium** | Relevant mainly after a device is already compromised, so it depends on a further event (C3). Impact could include data loss (C1), and no DNS monitoring evidence exists (C4). |
| **R6** | **Medium** | A stale alias exists (C3), but takeover depends on conditions that are not confirmed. Impact is limited to marketing subdomains unless trust or cookie scope reaches further (C1, C2). |
| **R7** | **Medium** | Impact on validating users could be broad (C1, C2), but it arises only if DNSSEC is enabled, which is a pending decision (C3). Change management reduces the exposure. |
| **R8** | **High** | A single provider with no secondary service and no recovery evidence (C4); the store and email depend on DNS (C2); provider incidents, errors, and expiry are plausible conditions (C3). |
| **R9** | **High** | DNS records affect all hostnames (C2), and the scenario has no approval or traceability evidence (C4). |

Count by level: **High 5** (R1, R2, R3, R8, R9), **Medium 3** (R5, R6, R7), **Low 1** (R4).

---

## 5. Possible Regulatory, Contractual, and Service-Level Considerations

None of these is assumed (A9). They indicate where verification would be needed.

- **Availability commitments:** if TrailMint made availability commitments in customer, marketplace, or supplier agreements, a DNS outage might affect them. Whether such commitments exist is unknown.
- **Data protection:** if misdirection or exposure involved personal data, obligations might apply depending on jurisdiction, data types, and agreements. This would need review by qualified advisers.
- **Supplier terms:** registrar and DNS provider terms may limit the provider's responsibility. Reviewing them is part of the supplier action in R2 and R3.
- **No violation or loss is established.** No finding here shows a legal violation, a contractual breach, or a financial loss.

---

## 6. Governance Responsibilities

| Role (assumed) | Responsibility in this scenario | NIST CSF 2.0 link (illustrative) |
|---|---|---|
| **CEO** | Decides risk priorities and resourcing; accepts or declines residual risk | GV.RM, GV.RR |
| **IT lead** (informal security owner, A7) | Owns the inventory, the DNS change procedure, and monitoring requirements; coordinates reviews | GV.PO, ID.AM, PR.PS |
| **Operations manager** (registrar account administrator, A7) | Owns the registrar relationship, renewals, and locks; contact for critical suppliers | GV.SC, PR.AA |
| **Marketing lead** (subdomain content owner, A7) | Owns marketing subdomains and external marketing services; completes the decommissioning step | ID.AM |
| **Developers** (3) | Follow DNS and access procedures when changes affect applications | PR.PS |

---

## 7. Executive Communication Example

A fictional, proposed message about the `promo` alias (R6), structured the way a GRC analyst might brief management:

| Element | Message |
|---|---|
| **1. What is at risk** | Customer trust in the `promo.trailmint.example` hostname, and indirectly in TrailMint's domain |
| **2. What could happen** | If the external service name can be claimed by another party, unauthorized content could appear under a TrailMint hostname. This is **not confirmed**. |
| **3. Why it matters to the business** | Customers trust TrailMint hostnames, so unauthorized content could support phishing or confuse customers |
| **4. Proposed action** | Ask the marketing lead whether the service is still needed; if not, remove the alias after approval; add DNS cleanup to the decommissioning checklist; review the other subdomains |
| **5. Who should own the decision or action** | The IT lead for the DNS change; the marketing lead for the subdomain; the CEO informed |
| **6. Evidence needed to verify the result** | Zone export before and after; the change approval; the decommissioning record; the external provider's confirmation of the name's status; a periodic review record |
| **7. Residual risk or uncertainty** | Whether the name was ever claimable remains unconfirmed. Other undocumented aliases may exist until the inventory is reconciled. No assessment has been performed. |

---

## Limits of This Analysis

- **No scoring.** No numerical risk scores, likelihood percentages, financial losses, or corrective-action service levels are used or implied.
- **Priority is not prediction.** High, Medium, and Low describe the proposed order of governance attention under stated criteria.
- **Fictional and conditional.** TrailMint, its gaps, and its assumptions are invented for study. Recommendations are proposals, and any regulatory or contractual obligation would require verification.

---

## References

Sources, official URLs, and verification notes are in [RESOURCES.md](04-resources.md). Concepts and definitions are in [WRITE-UP.md](02-write-up.md).

---

*Return to: [README.md](01-README.md)*
