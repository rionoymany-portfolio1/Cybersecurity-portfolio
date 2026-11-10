# Resources: References, Terminology, and Study Notes

> **Purpose:** Source index with official URLs and verification notes, a glossary, interview-preparation questions, and optional further practice
> **Verification window:** 25 October to 1 November 2026, based on system timestamps at the start and end of the work. Individual checks were not date-stamped separately. This window describes the overall research period; it does not mean every source was independently re-verified on a specific date.
> **Abbreviations:** NIST = National Institute of Standards and Technology; CSF = Cybersecurity Framework; ISO = International Organization for Standardization; IEC = International Electrotechnical Commission; IETF = Internet Engineering Task Force; RFC = Request for Comments; BCP = Best Current Practice; STD = Internet Standard; HTTP = Hypertext Transfer Protocol; TLS = Transport Layer Security; HTTPS = HTTP over TLS; DNS = Domain Name System; DNSSEC = DNS Security Extensions; DoT = DNS over TLS; DoH = DNS over HTTPS; EPP = Extensible Provisioning Protocol; TTL = Time to Live; MFA = multi-factor authentication; ICT = information and communication technology; GRC = Governance, Risk, and Compliance
> **Companion files:** [README.md](README.md) -- [WRITE-UP.md](WRITE-UP.md) -- [BUSINESS-IMPACT.md](BUSINESS-IMPACT.md)

---

## Bottom Line Up Front

| Item | Result |
|---|---|
| **Sources listed** | 15 foundational (used to support claims) and 3 supplementary (recommended for further reading) |
| **Currency finding 1** | The DNSSEC core documents (RFC 4033, 4034, 4035) are **updated by later RFCs**, not obsoleted. RFC 6840 and RFC 9364 help read them together. |
| **Currency finding 2** | RFC 1034 and RFC 1035 remain Internet Standards (STD 13) but are updated by many later RFCs. |
| **Currency finding 3** | NIST SP 800-81 Revision 3 (March 2026) supersedes SP 800-81-2 (2013). |
| **Limitation** | The ISO catalogue page could not be opened directly (access blocked), and the ISO/IEC 27001 and 27002 texts are paid and were not accessed. |

---

## Topics Studied Versus Optional Further Reading

| Day | Topics studied this week | Optional further reading |
|---|---|---|
| **Monday** | ID.AM and ID.RA; asset categories and the purpose of an inventory; vulnerability assessment versus risk assessment; ownership and ISO/IEC 27001 concepts | The full Identify section of CSWP 29; the ID.IM Category; ISO/IEC 27002 guidance on asset inventory |
| **Wednesday** | PR.AA, PR.AT, PR.DS, PR.PS, and PR.IR at Category level | Subcategory outcomes under each Category |
| **Friday** | DNS architecture and resolution; caching; five common record types covering addresses, aliases, mail routing, and text data; DNS threats; DNS security mechanisms; GRC mapping | NIST SP 800-81 Rev. 3; RFC 9364; RFC 6840; Cloudflare DNS security overview; encrypted DNS specifications |

---

## Foundational Sources

| # | Resource | Publisher or author | Identifier and date | Official URL | Supports | Verification note |
|---|---|---|---|---|---|---|
| F1 | The NIST Cybersecurity Framework (CSF) 2.0 | NIST | CSWP 29, February 2024 | https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-csf-20/final | Names and purposes of ID.AM, ID.RA, PR.AA, PR.AT, PR.DS, PR.PS, PR.IR; Subcategory examples ID.RA-01 and ID.RA-04 | Category wording checked against excerpts of NIST's published Core text and a mirror of it. The CSWP 29 page was not re-opened for this entry. |
| F2 | Secure Domain Name System (DNS) Deployment Guide (NIST SP 800-81 Rev. 3) | S. Rose (NIST), C. Liu and R. Gibson (Infoblox) | Final, March 2026 | https://csrc.nist.gov/pubs/sp/800/81/r3/final | Context for DNS deployment security, including protective DNS, logging, DNSSEC, and encrypted DNS | Page opened. Supersedes SP 800-81-2 (2013). The page shows a planning note dated 10 July 2026 about potential updates (errata). Cited as the latest revision verified during the research period. |
| F3 | ISO/IEC 27001:2022, Information security management systems -- Requirements | ISO and IEC | Edition 3, 2022; Amendment 1:2024 listed | https://www.iso.org/standard/27001 and https://www.iso.org/standard/88435.html | ISMS requirements; Annex A structure; the control titles in the table below | Catalogue page could not be opened directly (access blocked). Edition and amendment details come from excerpts of ISO catalogue pages. The amendment (climate action changes) was **not studied** and is listed only as a catalogue observation. |
| F4 | RFC 1034: Domain Names - Concepts and Facilities | IETF (P. Mockapetris) | STD 13, November 1987 | https://www.rfc-editor.org/info/rfc1034/ | DNS hierarchy, zones, delegation, resolvers, caching | Internet Standard. Updated by many later RFCs; RFC Editor and Datatracker lists include, for example, RFC 2181, RFC 2308, and RFC 8767. Status read from RFC Editor and Datatracker excerpts. |
| F5 | RFC 1035: Domain Names - Implementation and Specification | IETF (P. Mockapetris) | STD 13, November 1987 | https://www.rfc-editor.org/info/rfc1035/ | Record types covering addresses, aliases, mail routing, and text data | Internet Standard. Updated by many later RFCs; lists include, for example, RFC 7766 and RFC 8767. Status read from excerpts. |
| F6 | RFC 4033: DNS Security Introduction and Requirements | IETF (R. Arends and others) | Proposed Standard, March 2005 | https://www.rfc-editor.org/info/rfc4033/ | What DNSSEC provides and does not provide; no confidentiality; limits and operational risk | Info page opened. Updated by RFC 6014 and RFC 6840. |
| F7 | RFC 4034: Resource Records for the DNS Security Extensions | IETF (R. Arends and others) | Proposed Standard, March 2005 | https://www.rfc-editor.org/info/rfc4034/ | DNSSEC record types, including the delegation signer record | RFC Editor header excerpt: updated by RFC 4470, 6014, 6840, 6944, 9077, 9824, and 9905; errata exist. |
| F8 | RFC 4035: Protocol Modifications for the DNS Security Extensions | IETF (R. Arends and others) | Proposed Standard, March 2005 | https://www.rfc-editor.org/rfc/rfc4035 | How validating resolvers use DNSSEC data | RFC Editor header excerpt: updated by RFC 4470, 6014, 6840, 8198, 9077, 9520, and 9824; errata exist. Older third-party copies show shorter lists. |
| F9 | RFC 5452: Measures for Making DNS More Resilient against Forged Answers | IETF (A. Hubert, R. van Mook) | Proposed Standard, January 2009 | https://www.rfc-editor.org/info/rfc5452/ | Measures that make forged DNS answers harder to accept; cache poisoning safeguards | RFC Editor page excerpt; it updates RFC 2181. Not checked for later updates beyond the excerpt. |
| F10 | RFC 7858: Specification for DNS over Transport Layer Security (TLS) | IETF (Z. Hu and others) | Proposed Standard, May 2016 | https://rfc-editor.org/rfc/rfc7858 | DoT protects queries in transit | RFC Editor header excerpt. Not checked for later updates beyond the excerpt. |
| F11 | RFC 8484: DNS Queries over HTTPS (DoH) | IETF (P. Hoffman, P. McManus) | Proposed Standard, October 2018 | https://www.rfc-editor.org/info/rfc8484/ | DoH protects queries in transit | RFC Editor page excerpt. Not checked for later updates beyond the excerpt. |
| F12 | EPP Status Codes | ICANN | Web resource | https://www.icann.org/resources/pages/epp-status-codes-2014-06-16-en | Client statuses set by registrars, server statuses set by registries (with precedence), and lock statuses for transfer, update, and delete | Official ICANN page, read through a search-result excerpt. The URL carries a 2014 date, so current registrar practice should be confirmed with the registrar. |
| F13 | Cloudflare Learning Center: What is DNS, DNS server types, DNS records, How does DNSSEC work | Cloudflare | Web resources | https://www.cloudflare.com/learning/dns/what-is-dns/ ; https://www.cloudflare.com/learning/dns/dns-server-types/ ; https://www.cloudflare.com/learning/dns/dns-records/ ; https://www.cloudflare.com/learning/dns/dnssec/how-dnssec-works/ | Plain-language explanations of resolution, server types, record types, and the DNSSEC chain | Vendor educational material, not a standards body. Read through search-result excerpts of the official site. |
| F14 | OWASP Web Security Testing Guide: Subdomain Takeover | OWASP Foundation | Living document | https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management/10-Subdomain_Takeover/ | Definition of a dangling DNS record and the preventive concept | Official project page, read through a search-result excerpt. Only the definition and prevention are used; no testing procedure is used or reproduced. |
| F15 | MITRE ATT&CK: Application Layer Protocol: DNS (T1071.004) | MITRE | Technique page | https://attack.mitre.org/techniques/T1071/004/ | Adversary use of DNS as a communication channel, including tunneling | Official page, read through a search-result excerpt. Used only for the defensive description. |

---

## Supplementary Sources for Further Reading

| # | Resource | Publisher or author | Identifier and date | Official URL | Supports | Verification note |
|---|---|---|---|---|---|---|
| S1 | RFC 9364: DNS Security Extensions (DNSSEC) | IETF | BCP 237 | https://www.rfc-editor.org/rfc/rfc9364.html | An overview of the DNSSEC document set | Title and BCP number from RFC Editor excerpt; page not opened in full. |
| S2 | RFC 6840: Clarifications and Implementation Notes for DNS Security (DNSSEC) | IETF | Standards Track, February 2013 | https://www.rfc-editor.org/rfc/rfc6840.txt | Clarifications that update RFC 4033, 4034, and 4035 | Update relationship read from RFC Editor excerpts. |
| S3 | Cloudflare Learning Center: What is DNS security, What is recursive DNS | Cloudflare | Web resources | https://www.cloudflare.com/en-gb/learning/dns/dns-security/ ; https://www.cloudflare.com/learning/dns/what-is-recursive-dns/ | Overlapping DNS defenses; how recursive resolution works | Vendor educational material; search-result excerpts only. |

---

## Updated, Superseded, and Pending Relationships

| Item | Relationship found | Handling in this repository |
|---|---|---|
| **RFC 1034 and RFC 1035 (STD 13)** | Remain Internet Standards; updated by many later RFCs; not obsoleted | Cited as base references; later updates exist and should be read with them |
| **RFC 4033, 4034, 4035** | Proposed Standards, each updated by later RFCs (see F6 to F8); RFC 6840 clarifies them and RFC 9364 gives an overview | Cited for DNSSEC concepts. "Updated by" is not "obsoleted by". |
| **NIST SP 800-81 Rev. 3** | Supersedes SP 800-81-2 (2013); a planning note mentions potential errata | Cited as the current revision |
| **ISO/IEC 27001:2022** | Amendment 1:2024 exists | Mentioned as a catalogue observation only |
| **RFC 5452** | Proposed Standard; updates RFC 2181 | Cited for forged-answer resilience measures |

---

## Source Map

| Topic | Sources | Used in |
|---|---|---|
| Identify and Protect Categories | F1 | WRITE-UP Parts A and B |
| ISO/IEC 27001 concepts and control titles | F3 and the Annex A table below | WRITE-UP A.6 and B.2; BUSINESS-IMPACT Section 3 |
| DNS architecture, caching, and record types | F4, F5, F13 | WRITE-UP Parts C and D |
| DNSSEC scope and limits | F6, F7, F8, F13; S1, S2 | WRITE-UP Part F |
| Cache poisoning measures | F9 | WRITE-UP E.2 |
| Encrypted DNS | F10, F11 | WRITE-UP F.3 |
| Domain locks and registrar statuses | F12 | WRITE-UP F.4 |
| DNS tunneling and subdomain takeover | F15, F14 | WRITE-UP E.3 and E.4 |
| DNS deployment security context | F2 | WRITE-UP Parts E and F |

---

## ISO/IEC 27001:2022 Annex A Controls Referenced

Titles were checked against published summaries from independent catalogues, not against the paid standard text. The mappings that use them are reasoned and illustrative.

| Control | Title | Used for |
|---|---|---|
| A.5.9 | Inventory of information and other associated assets | Asset inventory and owners |
| A.5.16 | Identity management | Identity lifecycle |
| A.5.18 | Access rights | Provision, review, modification, removal of access |
| A.5.19 | Information security in supplier relationships | Registrar and provider as suppliers |
| A.5.22 | Monitoring, review and change management of supplier services | Supplier service oversight |
| A.5.30 | ICT readiness for business continuity | DNS availability and recovery |
| A.8.2 | Privileged access rights | Accounts that can change DNS |
| A.8.5 | Secure authentication | Registrar login and MFA |
| A.8.9 | Configuration management | DNS records as configuration |
| A.8.14 | Redundancy of information processing facilities | DNS redundancy |
| A.8.15 | Logging | DNS and change logs |
| A.8.16 | Monitoring activities | Monitoring for unusual DNS activity |
| A.8.20 | Networks security | Outbound DNS rules |
| A.8.21 | Security of network services | DNS as a network service |
| A.8.24 | Use of cryptography | DNSSEC signatures and key management |
| A.8.32 | Change management | DNS change approvals |

Clauses referenced: 5.3 (roles, responsibilities and authorities), 6.1.2 (risk assessment), and 8.2 (performing risk assessments).

---

## Glossary

| Term | Meaning |
|---|---|
| **DNS** | The Domain Name System, which translates names into data such as addresses and mail destinations |
| **Recursive resolver** | A server that finds answers on behalf of clients by querying the DNS hierarchy and caches the results |
| **Authoritative nameserver** | A server that holds a zone's data and gives the definitive answers for it |
| **TTL** | Time to Live: how long, in seconds, a resolver may reuse a cached answer |
| **DNSSEC** | DNS Security Extensions: cryptographic signatures that let validating resolvers check the origin and integrity of DNS data; it does not encrypt queries |
| **DNS filtering** | Blocking or flagging names classified as harmful by policy, also called Protective DNS |
| **Registrar** | The company through which a domain registration is managed |
| **Domain locking** | Registrar or registry statuses that ask the registry to reject specified operations, such as transfer, update, or deletion; the effect depends on the exact status |
| **Cache poisoning** | Introducing incorrect data into a resolver's cache so that it returns wrong answers |
| **DNS tunneling** | Using DNS messages to carry unauthorized communication or data |
| **Subdomain takeover** | An unauthorized party gaining control of content at a subdomain, typically through a dangling reference to an external resource that can be claimed |
| **Asset inventory** | A maintained record of assets with owners, context, and dependencies |
| **Risk assessment** | Understanding risk by combining assets, threats, weaknesses, exposure, likelihood, impact, and existing controls |
| **Design Evidence** | Shows a control is specified and appropriately designed |
| **Operating Evidence** | Shows a control was performed in practice for specific activities or samples |
| **Operating Effectiveness Evidence** | Supports the conclusion that a control operated consistently across the intended scope and period, including review of exceptions |

---

## Interview Preparation

The answer outlines below are study aids, not prescribed answers. They should be adapted to the evidence and context of each scenario.

| # | Question | Model-answer outline |
|---|---|---|
| 1 | A reviewer notices a stale alias that points to a cancelled external service. How do you decide whether it is a risk, and what do you propose? | Do not assume takeover; ask whether the external name can be claimed, by asking the provider; identify the owner and the subdomain's trust context; weigh impact and conditions; propose removal after approval and a decommissioning step; list the evidence you would ask for |
| 2 | Why does a policy that requires MFA on the registrar account not show, by itself, that the control works? | Policy is Design Evidence; settings at one date are Operating Evidence; effectiveness needs periodic reviews across the period; check scope (all administrators), recovery paths, and exceptions |
| 3 | A manager says, "We enabled DNSSEC, so our domain is protected from hijacking." How do you respond? | DNSSEC gives origin authentication and integrity for signed data; it does not encrypt queries or stop a compromised account from making valid changes; ask about registrar MFA, locks, and change control; note that errors can break resolution |
| 4 | How would you explain a vulnerability assessment versus a risk assessment to a business owner? | A weakness is not the same as business risk; risk adds asset importance, exposure, likelihood, impact, and existing controls; use the internal test host versus the store example |
| 5 | The business depends on a single managed DNS provider. How would you approach it? | Add it to the inventory with an owner; review available assurance material, data handling, and contract terms (conditionally); discuss redundancy options and trade-offs; request recovery test evidence; do not assume service levels |

---

## Suggested Further Practice

**None of the items below was performed during the week.** They are optional ideas for continued study.

- Run read-only DNS lookups with a command-line tool (for example, `dig` or `nslookup`) against a domain you own or a lab zone, to observe record types and TTLs.
- Reconcile a sample zone export against a sample inventory in a spreadsheet.
- Draft a one-page DNS change procedure and an access review checklist.
- Study DNSSEC validation behavior in a lab environment.

---

## Notes on Use and Verification

- **Reading claim.** Listing a source means it supports the concepts in this repository. It is **not** a claim that every page or standard was read in full or practiced.
- **How status was checked.** Entries marked "opened" were read directly. Entries marked "excerpt" were checked through excerpts from the official site, and should be re-opened before being cited elsewhere.
- **Dates.** The verification window comes from system timestamps. Re-open key pages and record your own date before publishing.
- **Paid standards.** ISO/IEC 27001 and 27002 are paid standards. Their text was not accessed or reproduced.
- **No quotations.** Source content is paraphrased in original wording. No quotations, page numbers, or publication details are included beyond what was checked.

---

*Return to: [README.md](README.md)*
