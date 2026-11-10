# Technical and GRC Write-Up: NIST CSF 2.0 Identify and Protect, and DNS Security

> **Scope:** Monday (National Institute of Standards and Technology (NIST) Cybersecurity Framework (CSF) 2.0 Identify), Wednesday (CSF 2.0 Protect), Friday (Domain Name System (DNS) security and Governance, Risk, and Compliance (GRC) mapping)
> **Method:** Studying the topics listed for each day, summarizing them in original wording, and connecting them to governance questions and evidence. No tools were run and no real environment was assessed.
> **Scenario:** TrailMint, a fictional online retailer. Assumptions A1 to A9 are in [BUSINESS-IMPACT.md](03-business-impact.md).
> **Companion files:** [README.md](01-README.md) -- [BUSINESS-IMPACT.md](03-business-impact.md) -- [RESOURCES.md](04-resources.md)

---

## Bottom Line Up Front

| Part | Key takeaway | Why it matters for GRC |
|---|---|---|
| **A. Identify** | Asset visibility, ownership, and risk assessment come before prioritization. A **vulnerability is not the same as a risk**. | An incomplete inventory hides systems, data, suppliers, and dependencies from risk assessment |
| **B. Protect** | The five Protect Categories turn requirements into responsibilities and operating practice. A policy or configuration alone does not show that a control works. | Reviewers need evidence that a control was designed, operated, and kept operating |
| **C to F. DNS** | DNS is a shared dependency for web, email, and application programming interfaces (APIs). Each threat and each control has a **distinct scope and limits**. | DNS Security Extensions (DNSSEC) do not encrypt queries, and locks or multi-factor authentication do not replace change control |
| **G to H. Evidence and scenarios** | One three-tier evidence model is applied to DNS controls, followed by three fictional exercises. | Turns concepts into concrete review questions |

## What This Write-Up Is and Is Not

| Activity | Status |
|---|---|
| Studied the CSF 2.0 Identify and Protect Categories listed for the week, at Category level | Conceptual study |
| Studied DNS architecture, record types, threats, and security mechanisms | Conceptual study |
| Practiced describing gaps, impacts, and evidence requests for a fictional organization | Written exercise |
| Ran DNS lookup, scanning, or testing tools, or configured DNS, DNSSEC, or registrar settings | **Not done** |
| Performed a vulnerability assessment, risk assessment, or audit of a real environment | **Not done** |
| Studied every Subcategory | **Not done** (a few Subcategory outcomes are cited as examples only) |

**Labels used:** **Study fact** (summarized from the sources in [RESOURCES.md](04-resources.md)), **Scenario assumption** (fictional), and **Proposed action** (not performed).

---

## Part A: NIST CSF 2.0 Identify (Monday)

### A.1 Purpose of ID.AM and ID.RA

| Category | Purpose (paraphrased from NIST) | Plain-language question |
|---|---|---|
| **ID.AM** Asset Management | Identify and manage the assets that enable the organization's business purposes, in line with their relative importance to its objectives and risk strategy | What do we rely on, who owns it, and how important is it? |
| **ID.RA** Risk Assessment | Understand the cybersecurity risk to the organization, its assets, and individuals | What could go wrong, how much would it matter, and what should come first? |

NIST's examples of assets include data, hardware, software, systems, facilities, services, and people. Identify also contains ID.IM (Improvement), which was not studied this week.

### A.2 Asset Categories

| Category | Examples | Why a gap matters |
|---|---|---|
| **Hardware** | Laptops, servers, network devices | Unlisted devices can miss patching and access review |
| **Software and systems** | Applications, operating systems, cloud workloads | Unknown software hides weaknesses |
| **Services** | Hosted platforms, managed DNS, email services | Business processes depend on them |
| **Data** | Customer records, order history, support correspondence | Determines confidentiality, retention, and handling needs |
| **Identities and accounts** | Staff, contractors, administrator and service accounts | Accounts often control other assets, such as a registrar or DNS provider |
| **Suppliers** | Registrar, DNS provider, cloud provider, e-commerce platform | Supplier-held assets and risks sit outside direct control |
| **Dependencies** | Domain registration, DNS delegation, shared services | Failure of one dependency can disrupt many services |

These are practical inventory groupings for this exercise, not a complete reproduction of NIST's asset examples or CSF Subcategories.

### A.3 Why an Inventory Needs Ownership, Context, and Maintenance

| Element | What it adds | Example attribute |
|---|---|---|
| **Ownership** | A named, accountable role who decides, reviews, and answers questions | "Operations manager owns the registrar account" |
| **Business context** | Criticality, data held, and processes supported | "Supports checkout and email" |
| **Dependencies** | What the asset relies on and what relies on it | "Web store depends on the DNS provider" |
| **Maintenance** | A review cadence and triggers such as a new supplier, a departure, or a cancelled service | "Reviewed when a service is retired" |

An inventory without owners lists things but not responsibilities. An inventory without maintenance becomes out of date.

### A.4 From Visibility to Prioritization

```
Asset visibility -> Asset ownership -> Risk identification -> Risk prioritization
 (what exists)     (who is accountable) (what could go wrong)  (what comes first)
```

- **Visibility:** an asset missing from the inventory may be overlooked during subsequent risk assessment, control reviews, and ownership activities.
- **Ownership:** someone can answer questions, approve access, and accept or treat risk.
- **Identification:** threats, weaknesses, and impacts only make sense in the context of a known asset.
- **Prioritization:** the asset's importance, its exposure, and the safeguards around it decide what comes first.

### A.5 Vulnerability Assessment Versus Risk Assessment

| Aspect | Vulnerability assessment | Risk assessment |
|---|---|---|
| **Question** | What weaknesses exist in an asset or process? | What could the effect on the organization be, and what should be prioritized? |
| **Inputs** | Asset information, configuration, review or scan results | Assets and their importance, threats, weaknesses, exposure, likelihood, impact, and existing controls |
| **Output** | A list of weaknesses, often with a technical severity | Prioritized risks with reasoning for treatment decisions |
| **Perspective** | Technical | Business and governance |

Identifying a weakness alone does not establish business risk. The same type of weakness can carry very different risk depending on the affected asset, its exposure, how likely exploitation is, the impact, and the controls around it (**illustrative example**):

| Factor | Weakness on an internal test host | Same type of weakness on the internet-facing store |
|---|---|---|
| **Asset importance** | Low | High |
| **Exposure** | Limited to the internal network | Reachable from the internet |
| **Impact if exploited** | Limited | Could interrupt sales |
| **Existing controls** | Network restrictions (assumed) | None evidenced (assumed) |

The weakness is similar; the risk is not. NIST's Subcategories reflect this split: ID.RA-01 concerns identifying, validating, and recording vulnerabilities, while ID.RA-04 concerns identifying the potential impacts and likelihoods of threats exploiting them. These are cited only to show the distinction; Subcategories were not studied in full.

> **Note:** No vulnerability assessment or formal risk assessment was performed against a real environment.

### A.6 Conceptual Mapping to ISO/IEC 27001:2022

The International Organization for Standardization (ISO) and the International Electrotechnical Commission (IEC) publish ISO/IEC 27001:2022, a standard that specifies requirements for an information security management system. It is **not equivalent** to the NIST CSF. The mapping below is reasoned and illustrative.

| Concept | CSF 2.0 | ISO/IEC 27001:2022 | Why related |
|---|---|---|---|
| **Asset inventory and owners** | ID.AM | Annex A.5.9, Inventory of information and other associated assets | Published summaries state the inventory is expected to include owners, which matches the CSF emphasis on identified and managed assets |
| **Risk assessment** | ID.RA | Clause 6.1.2 (risk assessment process) and Clause 8.2 (performing it) | Both expect risks to be identified, analyzed, and evaluated; ISO frames this as a repeatable management-system process |
| **Accountability** | Govern (GV.RR) | Clause 5.3, Organizational roles, responsibilities and authorities | Ownership of an asset only has meaning if roles and authorities are defined |

### A.7 Illustrative Asset Inventory Gap

| Element | Illustration (fictional) |
|---|---|
| **1. Asset or dependency overlooked** | A marketing email service holding an exported customer contact list is absent from TrailMint's inventory |
| **2. Why the gap matters** | It has no owner, no data-type record, and no supplier review, so it falls outside access reviews and risk assessment scope |
| **3. Potential risk** | Customer contact data could be held, shared, or retained without oversight, and the service's user list could include people who have left |
| **4. Business impact** | Possible customer-data exposure, difficulty answering customer questionnaires, and uncertainty about obligations |
| **5. Responsible role** | Marketing lead as proposed asset owner; information technology (IT) lead as inventory owner |
| **6. Evidence an analyst could request** | Inventory entry with owner and data type; supplier register entry; the service's user list; a record of the data's purpose and retention decision |

*Illustrative only; not a finding about any real system.*

---

## Part B: NIST CSF 2.0 Protect (Wednesday)

### B.1 The Five Protect Categories

| Category and plain-language purpose | Example risk | Illustrative TrailMint example | Governance or management consideration | Example evidence to request | Limitation or review consideration |
|---|---|---|---|---|---|
| **PR.AA** Identity Management, Authentication, and Access Control: limit access to physical and logical assets to authorized users, services, and hardware, in line with assessed risk | Excessive or unremoved access; weak authentication | A former contractor still has an account at the managed DNS provider | Access policy; named owners who approve access; a joiner, mover, and leaver process; periodic review | Account lists reconciled to staff and contractor records; approval records; review records; multi-factor authentication (MFA) settings | A list at one date does not show that reviews happen consistently; shared and service accounts need particular attention |
| **PR.AT** Awareness and Training: give personnel the cybersecurity awareness and training they need for their tasks | Staff misled by phishing or by social engineering aimed at account recovery | The operations manager receives a convincing message claiming to come from the registrar | Role-based training content; completion tracking; refresh cadence; extra focus for holders of critical supplier accounts | Training materials; completion records; results of any exercises | Completion shows attendance, not changed behavior |
| **PR.DS** Data Security: manage data in line with the risk strategy to protect confidentiality, integrity, and availability | Customer data exposed, altered, or lost | Order exports kept in an unmanaged shared folder | Data classification; handling and retention rules; encryption and backup standards; named data owners | Classification scheme; data location records; encryption and backup settings; restore test records | Encryption settings do not address who is authorized; classification helps only if applied |
| **PR.PS** Platform Security: manage hardware, software, and services of physical and virtual platforms in line with the risk strategy | Misconfigured or unmaintained platforms; unreviewed changes | A DNS or application setting is changed without review | Configuration baselines; change management; named owners for maintenance | Baseline documents; change tickets with approvals; maintenance records | A baseline document does not show that systems still match it; drift needs detection |
| **PR.IR** Technology Infrastructure Resilience: manage security architectures and infrastructure to protect assets and support resilience | Single points of failure; infrastructure outages | A single managed DNS provider with no secondary service and untested recovery | Architecture standards; resilience requirements; recovery expectations; provider expectations | Architecture diagrams; redundancy design; availability reports; failover or recovery test records | A diagram shows design, not behavior during a failure; tests need realistic scenarios |

### B.2 The Identity Lifecycle (PR.AA)

| Stage | Control question | Example evidence |
|---|---|---|
| **Grant** | Who approves access, and on what basis (role and need)? | Access requests and approval records |
| **Change** | When a role changes, is access that is no longer needed removed? | Role-change records; before and after access lists |
| **Review** | Does an accountable owner review access periodically? | Review schedule; completed reviews; exceptions and follow-up actions |
| **Revoke** | Is access removed when no longer required, including contractor and supplier accounts? | Leaver checklist; account removal records; reconciliation to staff and contractor lists |

In ISO/IEC 27001:2022 terms, this lifecycle relates to Annex A.5.16 (Identity management) and A.5.18 (Access rights), which published summaries describe as covering the full identity life cycle and the provisioning, review, modification, and removal of access.

### B.3 From Requirement to Review

| Link | Meaning | Example (registrar account MFA) | Evidence tier |
|---|---|---|---|
| **Requirement** | A security requirement is stated | Policy: administrator accounts for critical suppliers require MFA | Design |
| **Responsibility** | A role is accountable | Operations manager owns the registrar account; IT lead owns the policy | Design |
| **Put into practice** | The control is configured | Configuration record showing MFA is enabled for the registrar account | Implementation evidence; supports implementation but is not a separate tier in the three-tier model |
| **Operational practice** | The control is performed in day-to-day work | Authentication records showing MFA challenges were applied to relevant sign-in events | Operating |
| **Review** | A periodic check of whether the control works across the intended scope and period | Periodic review of authentication coverage, exceptions, bypasses, and account changes over the review period | Operating Effectiveness |

> **A documented policy or configuration does not automatically show that a control operates consistently or achieves its intended objective.** It shows what was intended or what was set at one moment.

---

## Part C: DNS Fundamentals (Friday)

### C.1 Purpose and Components

DNS translates names that people use into data that systems need, such as addresses and mail destinations. It is organized as a hierarchy with delegated authority.

| Component | Role |
|---|---|
| **Client (stub resolver)** | The operating system or application component that asks its configured resolver for an answer |
| **Recursive resolver** | A server that finds answers on behalf of clients by querying the DNS hierarchy, and caches what it learns |
| **Root nameservers** | The top of the hierarchy; they answer with referral information that points to the relevant top-level domain (TLD) nameservers |
| **TLD nameservers** | Know which nameservers are authoritative for domains under a TLD such as .com |
| **Authoritative nameservers** | Hold the zone data for a domain and give the definitive answers for it |

### C.2 A Typical Uncached Lookup

1. The client asks its configured recursive resolver for the address of `www.example.com`.
2. If the resolver has no cached answer, it uses root referral information to find the TLD nameservers for `.com`.
3. The TLD nameservers refer the resolver to the authoritative nameservers for `example.com`.
4. The authoritative nameserver returns the answer.
5. The resolver returns the answer to the client and may cache it according to applicable DNS rules and the record's Time to Live (TTL).

```
Client -> Recursive resolver -> Root nameserver          (referral to TLD)
                             -> TLD nameserver           (referral to authoritative)
                             -> Authoritative nameserver (answer)
Recursive resolver -> Client                             (answer, cached per TTL)
```

**A real query does not necessarily traverse the entire hierarchy every time.** The resolver may already hold the final answer, or it may already know the TLD or authoritative nameservers from earlier lookups. Operating systems and applications can also cache answers.

### C.3 Recursive Resolver Versus Authoritative Nameserver

| Aspect | Recursive resolver | Authoritative nameserver |
|---|---|---|
| **Question it answers** | "What is the answer for this name?" on behalf of a client | "What does this zone say?" for names it is responsible for |
| **Holds** | Cached copies of answers it has obtained | The zone data for its domains |
| **Typical operator** | An internet provider, an employer, or a public resolver service | The domain owner or the DNS provider they use |
| **Relevance to governance** | Determines which answers users receive; largely outside the domain owner's control | Determines what the domain publishes; under the domain owner's control through the provider |

### C.4 Zones and Delegation

A **zone** is a portion of the DNS namespace managed as a unit. **Delegation** passes responsibility for part of the namespace to other nameservers, using NS (nameserver) records in the parent zone. A parent zone can delegate a domain to its nameservers, and a domain owner can delegate a subdomain to another party. For governance, delegation decides **who controls the answers**. When DNSSEC is used, a delegation signer (DS) record published in the parent zone also links the parent to the child's signing keys.

### C.5 Caching and TTL

Each DNS record carries a **TTL**: how long, in seconds, a resolver may reuse the answer before asking again.

| TTL setting | Benefit | Consideration |
|---|---|---|
| **Shorter** | Changes take effect sooner, and a wrong answer expires sooner | More queries reach authoritative servers, and resolvers depend more on their availability |
| **Longer** | Fewer queries; cached answers may remain usable during a brief authoritative outage | Changes, including corrections, spread more slowly, and a wrong answer can persist longer. This benefit depends on resolver behavior and the availability of the cached data; it is not a guarantee of continued resolution during every outage. |

### C.6 Why DNS Matters to the Business

- **Availability:** if names cannot be looked up, websites, email, and application programming interfaces (APIs) can be unreachable even when the servers behind them are running.
- **Trustworthy answers:** an incorrect answer can send customers or staff to the wrong destination, or send mail to the wrong server.
- **Shared dependency:** one DNS provider or registrar account can sit underneath every public hostname the business uses.

---

## Part D: DNS Record Types (Friday)

| Record | Purpose | Generic example (fictional values) | Review consideration |
|---|---|---|---|
| **A** (address) | Maps a hostname to an Internet Protocol version 4 (IPv4) address | `shop.example.com. IN A 192.0.2.10` | Wrong or stale addresses misdirect traffic |
| **AAAA** (address) | Maps a hostname to an Internet Protocol version 6 (IPv6) address | `shop.example.com. IN AAAA 2001:db8::10` | Both A and AAAA need to be reviewed together |
| **CNAME** (canonical name) | Defines an alias from one name to another name | `promo.example.com. IN CNAME pages.vendor.example.net.` | An alias that outlives the service it points to can become a dangling reference |
| **MX** (mail exchange) | Identifies the mail-exchange hostnames for a domain, with a preference value (lower is preferred) | `example.com. IN MX 10 mail.example.com.` | Controls where inbound email goes, so changes need approval |
| **TXT** (text) | Stores text data used for various purposes, including domain verification and certain email-related policies | `example.com. IN TXT "v=spf1 include:mailer.example.net -all"` | Old verification and policy entries can remain after a service ends |

The example values use names and address ranges set aside for documentation and are not records of any real organization.

**Notes:**

- **TXT is a general-purpose record type.** The Sender Policy Framework (SPF) is a policy convention commonly published using TXT records. It is not a separate DNS record type in the ordinary DNS record-type sense.
- **No single record type protects a domain on its own.** Record types carry data; whether that data is accurate, approved, and protected depends on the controls around them.

---

## Part E: DNS Threat Analysis (Friday)

The scenarios below focus on understanding, risk identification, prevention, detection, and corrective action. They do not describe exploit procedures.

### E.0 How the Five Threats Differ

| Threat | What goes wrong | Where it occurs | Typical control focus |
|---|---|---|---|
| **Domain hijacking** | Unauthorized control over a domain or its configuration | Registrar or DNS provider accounts; registration data | Account security, locks, supplier management, change control |
| **DNS cache poisoning** | Incorrect data enters a resolver's cache | Recursive resolvers | Resolver hardening, DNSSEC validation, patching (mostly by the resolver operator) |
| **DNS tunneling** | DNS messages carry unauthorized communication or data | Internal devices to external resolvers and nameservers | Logging, monitoring, filtering, outbound DNS rules |
| **Subdomain takeover** | A dangling reference lets an unauthorized party claim an external resource behind a subdomain | Zone records that point to external services | Inventory, decommissioning, periodic record review |
| **DNS outage** | Name lookups fail, or answers are unavailable | Authoritative DNS, registration, or provider services | Redundancy, change control, monitoring, tested recovery |

### E.1 Domain Hijacking

| Element | Description |
|---|---|
| **Definition** | Unauthorized control over a domain or its configuration, for example through the registrar account or the DNS provider account |
| **How the risk may arise** | Weak or exposed account credentials; account recovery processes that can be misused; social engineering of provider support; out-of-date contact details; access left active for former staff or contractors; a lapsed registration |
| **Potential technical impact** | Changed delegation or records; redirected web traffic and email; impersonation under the real domain name |
| **Potential business impact** | Interrupted sales and email; customers sent to unauthorized destinations; lost confidence; effort to regain control |
| **Relevant safeguards** | MFA and sound recovery processes on registrar and DNS provider accounts; limited and reviewed account access; appropriate domain and transfer locks; renewal management; alerts on changes; documented change control |
| **Governance or ownership** | A named domain owner and deputy; the registrar treated as a critical supplier; documented recovery contacts; periodic review |
| **Evidence a reviewer may request** | Account user list; MFA settings; lock status shown by the registrar; renewal and contact records; change notifications and logs |

### E.2 DNS Cache Poisoning

| Element | Description |
|---|---|
| **Definition** | Introducing incorrect DNS data into a resolver's cache, so the resolver returns the wrong answer to its clients until the entry expires or is removed |
| **How the risk may arise** | At a high level, weaknesses that let a resolver accept forged or unvalidated responses. Exposure rests mainly with resolver software and configuration, which an internet provider, employer, or public service operates |
| **Potential technical impact** | Clients directed to wrong addresses or mail servers for as long as the cached entry lasts, which TTL influences |
| **Potential business impact** | Customers or staff misdirected away from legitimate services; potential impersonation; difficult to see from the domain owner's side |
| **Relevant safeguards** | Maintained and patched resolvers; measures that make forged answers harder to accept (standardized in Request for Comments (RFC) 5452); DNSSEC signing by the domain owner and validation by resolvers; monitoring at resolvers the organization operates |
| **Governance or ownership** | Resolver operators are responsible for resolver hardening. A domain owner controls its own resolvers (if any) and its decision on DNSSEC signing |
| **Evidence a reviewer may request** | Resolver patch and configuration records; DNSSEC validation settings on operated resolvers; supplier statements about resolver protection; the DNSSEC decision record |

### E.3 DNS Tunneling

| Element | Description |
|---|---|
| **Definition** | Using DNS queries and responses to carry unauthorized communication or data, taking advantage of the fact that DNS traffic is commonly allowed |
| **How the risk may arise** | A device or tool inside the network that is already compromised sends data encoded within DNS messages to infrastructure controlled by an unauthorized party |
| **Potential technical impact** | A covert command channel; data leaving the network unnoticed |
| **Potential business impact** | Possible loss of customer or business data; delayed detection; investigation effort |
| **Relevant safeguards** | DNS logging and monitoring for unusual patterns, such as high query volume or unusually long, encoded names; restricting outbound DNS to approved resolvers; DNS filtering or Protective DNS; endpoint protection |
| **Governance or ownership** | Monitoring requirements owned by the IT lead; decisions on log retention and review cadence; exception handling |
| **Evidence a reviewer may request** | Log sources and retention settings; alert rules and review records; outbound DNS rules; records of exceptions |

### E.4 Subdomain Takeover

| Element | Description |
|---|---|
| **Definition** | An unauthorized party gains control over content served at a subdomain of a legitimate domain. It typically requires a **dangling DNS reference** to an external service or resource that can be claimed |
| **How the risk may arise** | A record, often an alias, keeps pointing to an external resource after the service was cancelled or deprovisioned, and the external provider's rules allow another party to claim that name. **An unclaimed-looking record alone does not establish that takeover is possible** |
| **Potential technical impact** | Unauthorized content under a trusted name; possible interaction with cookies or trust relationships scoped to the parent domain |
| **Potential business impact** | Brand misuse; phishing under a trusted hostname; customer confusion; investigation effort |
| **Relevant safeguards** | An inventory that links external services to hostnames; a decommissioning checklist that removes DNS entries when a service is retired; periodic review of records against the inventory; change approvals |
| **Governance or ownership** | Every subdomain has an owner; marketing and IT share a decommissioning step |
| **Evidence a reviewer may request** | Zone export reconciled to the inventory; decommissioning records; periodic review records; the exception list |

### E.5 DNS Outages and Availability Failures

| Element | Description |
|---|---|
| **Definition** | Loss of the ability to obtain DNS answers for a domain, or answers that are wrong or unavailable |
| **How the risk may arise** | Attacks on DNS infrastructure; configuration errors; provider incidents; expired registrations or other dependencies; DNSSEC problems; other availability failures |
| **Potential technical impact** | Name lookups fail although servers may be running; web, email, and API access are interrupted |
| **Potential business impact** | Interrupted sales, email, and support; recovery effort. Any service-level consequence depends on agreements that this scenario does not assume |
| **Relevant safeguards** | Redundant authoritative service (a secondary provider where justified); change control and review; monitoring of DNS availability and expiry dates; renewal management; tested recovery steps; documented provider contacts |
| **Governance or ownership** | A named owner; provider expectations reviewed; recovery needs set by the business |
| **Evidence a reviewer may request** | Architecture showing redundancy; provider availability reports; monitoring and alert records; renewal records; recovery test records |

---

## Part F: DNS Security Controls (Friday)

### F.1 Control Summary

| Control | Intended purpose | Risks it reduces | Limits and risks outside its scope | Typical owner | Example evidence |
|---|---|---|---|---|---|
| **DNSSEC** | Lets validating resolvers check that DNS data comes from the signing zone and was not altered | Forged or altered answers, including cache poisoning, for clients behind validating resolvers | Does not encrypt queries; does not address domain hijacking, registrar-account compromise, outages, or changes made by a compromised authorized account; protects only where validation is performed; mistakes can break resolution | IT lead with the DNS provider | Signing and delegation records; validation results; key-management procedure and rollover records |
| **DNS filtering or Protective DNS** | Blocks or flags names classified as harmful by policy | Access to known-malicious destinations; some command channels and phishing destinations | Does not stop every threat; cannot see activity that bypasses the filtering resolver; depends on classification quality | IT lead | Filtering policy; resolver configuration; block logs; exception records |
| **Registrar account MFA** | Reduces unauthorized login to the account that controls registration | Domain hijacking through stolen credentials | Does not govern records at a separate DNS provider; does not replace locks; weak recovery paths or shared accounts can undermine it | Operations manager; IT lead | MFA setting; account user list; recovery contacts |
| **Domain and transfer locking** | Asks the registry to reject specified operations such as transfer, update, or deletion | Unauthorized transfer; some unauthorized registration changes, depending on the lock | Protection depends on the registrar and the exact lock type; client-set locks are managed through the registrar account; does not govern edits to zone records at a DNS provider | Operations manager | Lock status shown by the registrar; records of lock decisions; periodic checks |
| **DNS record change control** | Provides a defined path for changes to be requested, approved, performed, and traced | Unauthorized or erroneous record changes; stale records; some outage causes | Does not stop a compromised approver or provider account; needs evidence that the process is followed | IT lead; record owners | Change procedure; approvals; provider audit trail; periodic reconciliation |
| **DNS logging and monitoring** | Gives visibility into queries and changes for detection and investigation | Delays in noticing tunneling, unauthorized changes, or unusual patterns | Does not prevent events; logs must be retained and reviewed; volume and privacy need consideration | IT lead | Log source list; retention settings; alert rules; review records |
| **Availability and recovery** | Reduces the effect of a DNS failure | Outages from provider incidents, errors, and expiry | Does not address integrity or unauthorized changes; redundancy adds complexity | IT lead; operations manager | Redundancy design; provider reports; expiry tracking; recovery tests |

### F.2 DNSSEC: What It Does and Does Not Do

- **What it provides:** data-origin authentication and integrity validation of DNS data, using cryptographic signatures and validation by resolvers.
- **What it does not provide:** DNSSEC **does not encrypt ordinary DNS queries**. The core specification states that confidentiality is not part of the service.
- **Not a complete solution:** DNSSEC does not stop domain hijacking, registrar-account compromise, DNS outages, or malicious changes made by an authorized but compromised account. If an unauthorized party can change signed data through a legitimate account, the changed data can still be validly signed.
- **Only where validated:** the protection applies to clients whose resolvers perform validation.
- **Unsigned data:** information that is not signed, such as delegation data held in the parent zone, is not protected by the signatures.
- **Operational risk:** incorrect deployment or delegation can cause **legitimate** names to fail lookups through validating resolvers. Examples include delegation data that does not match the zone's keys, expired signatures, or mishandled key changes. Deployment and key-management changes therefore need careful review.

### F.3 DNSSEC Compared With Encrypted DNS

Encrypted DNS includes DNS over Transport Layer Security (DoT) and DNS over HTTPS (DoH), where HTTPS is the Hypertext Transfer Protocol carried over TLS.

| Mechanism | Protects | Does not protect |
|---|---|---|
| **DNSSEC** | The authenticity and integrity of signed DNS data | The privacy of queries; availability; account security |
| **DoT and DoH** | The confidentiality and integrity of queries and responses **in transit** between a client and a resolver | The origin of the DNS data itself (DNSSEC's role); registrar or provider account security; availability of authoritative services |

The two address different security properties and can be used together. Encrypted DNS can also change where an organization can observe DNS activity, which matters for the monitoring discussed in Part E.

### F.4 Registrar Security, Locks, and Change Control Are Different Layers

| Layer | What it governs | What it does not govern |
|---|---|---|
| **Registrar account security** (login, MFA, recovery, user access) | Who can act inside the registrar account | What the registry accepts for a locked domain; zone content at a separate DNS provider |
| **Transfer, update, and delete locks** (statuses set through the registrar or registry) | Whether specified operations on the registration are accepted | Account login security; edits to zone records at a DNS provider |
| **DNS record change control** (at the DNS provider) | Who may change zone records, and how changes are approved and traced | Registration and transfer status; the registrar account |

- **Lock protections depend on the registrar and the exact lock type.** Registrars set client statuses, registries set server statuses, and the statuses cover different operations such as transfer, update, and deletion.
- **A product called a "domain lock" may not block every unauthorized modification.** Its exact effect should be confirmed with the registrar.
- **Registrar controls are not substitutes** for DNSSEC or for DNS change control, because each addresses a different risk.

---

## Part G: Evidence Mapping

### G.1 The Three-Tier Evidence Model

| Evidence tier | Meaning |
|---|---|
| **Design Evidence** | Shows that a control is specified and appropriately designed through relevant policies, standards, approved configurations, architecture, or assigned responsibilities |
| **Operating Evidence** | Shows that the control was performed in practice for specific activities or samples, such as DNS change records, account reviews, or filtering events |
| **Operating Effectiveness Evidence** | Supports the conclusion that the control operated consistently across the intended scope and relevant review period, including review of exceptions, bypasses, and failures where applicable |

### G.2 Applying the Model to DNS Controls

| Control | Design Evidence | Operating Evidence | Operating Effectiveness Evidence | Not sufficient by itself |
|---|---|---|---|---|
| **Registrar MFA and domain lock** | Access standard requiring MFA for critical supplier accounts; an assigned account owner | MFA setting and lock status shown for the account at a point in time; recorded recovery contacts | Periodic reviews showing MFA and lock status stayed in place, the user list matched current staff, and exceptions were followed up | A single screenshot of settings |
| **DNSSEC** | Decision record; signing and key-management standard | Configuration showing the zone is signed and the parent holds matching delegation data; validation results for specific dates | Validation monitoring across the period; records of key and signature events completed without resolution failures; exceptions reviewed | One successful validation test |
| **DNS filtering** | Filtering policy and categories; named owner | Resolver configuration; a sample of block events and approved exceptions | Logs across the period showing consistent enforcement on the intended scope, with bypasses and false positives reviewed | A policy document or a screenshot of an enabled setting |
| **DNS change approvals** | Approved DNS change procedure | A sample of change tickets with approvals matched to provider audit trail entries | Reconciliation across the period showing that changes in the audit trail had approvals, and that emergency changes were reviewed | A sample chosen by the person who made the changes |
| **DNS logging and monitoring** | Logging standard and retention requirement | Log configuration; a sample of alerts and reviews | Evidence that logs were collected without gaps across the period, alerts were triaged, and incidents and exceptions were recorded | A dashboard screenshot |
| **Availability and recovery** | Availability requirement; recovery procedure; architecture | A provider availability report for a period; a recovery test record | Repeated tests or incident reviews across the period, with follow-up actions completed | A diagram alone |

### G.3 Evidence Cautions

- A screenshot or a one-time configuration export shows state at one moment. **By itself it does not establish sustained Operating Effectiveness.**
- Sampling should cover the intended scope and the review period, not only convenient examples.
- This repository contains **no real evidence**. The tables list what an analyst could request; no logs, approvals, test results, or records of corrective action are claimed.

---

## Part H: Practical Scenario Walkthroughs

*All three exercises are fictional. None states that a vulnerability was discovered, exploited, or addressed in a real environment.*

### Scenario 1: Asset Inventory Gap Analysis

| Element | Description |
|---|---|
| **Setting** | TrailMint's inventory lists servers and software-as-a-service tools. It does not list the managed DNS provider account, the registrar account, or the external services behind the `promo` and `events` subdomains |
| **Missing dependency** | The managed DNS provider, which controls the answers given for every TrailMint hostname |
| **Effect on risk assessment** | Risks involving DNS, registration, and subdomains cannot be identified or prioritized if the dependencies are not known, so the risk register is incomplete |
| **Effect on accountability** | With no owner recorded, no one is responsible for reviewing who has access, who the supplier is, or when registration renews |
| **Proposed initial actions** | Compare an export of the DNS zone with the inventory; add the registrar, DNS provider, and external services; assign owners and renewal dates |
| **Evidence to request** | Inventory with owners; a zone export reconciled to the inventory; user lists for the registrar and DNS provider; supplier register entries |

### Scenario 2: Access Control Lifecycle

| Lifecycle stage | Hypothetical gap | Proposed action | Evidence |
|---|---|---|---|
| **Revoke** | A marketing contractor's engagement has ended, but the contractor's account at the DNS provider is still active | Remove the account after confirming with the account owner | Account removal record; updated user list |
| **Change** | A staff member moved from marketing to operations and kept DNS edit rights from the previous role | Reassign permissions to match the new role | Role-change record; before and after permissions |
| **Review** | No periodic access review is documented | Introduce a scheduled review with a named reviewer | Review schedule; completed review records |
| **Grant** | DNS provider access was granted informally | Require approval by the account owner | Access request and approval records |

**Risk trace:** unremoved or excessive access -> an account that can change DNS records stays with someone who no longer needs it -> an accidental or unauthorized change becomes possible, or exposed credentials give an unauthorized party that ability -> misdirected traffic or email, or an outage -> interrupted sales, lost confidence, and investigation effort.

**Connection to PR.AA:** the scenario links the Category to **ownership** (who owns the provider account), **periodic reviews** (who checks, how often), **evidence** (what shows the review happened), and **corrective actions** (what happens to exceptions).

### Scenario 3: Subdomain Takeover and Registrar Security

| Element | Description |
|---|---|
| **Setting** | `promo.trailmint.example` is an alias to an external landing-page service that marketing stopped using. The alias remains in the zone. Whether the external name can be claimed by another party is **unconfirmed** |
| **Conditions that could make it risky** | The alias still exists; the external provider's rules allow another customer to claim the name; customers or systems trust the subdomain; no one reviews subdomain dependencies |
| **Preventive measures** | A decommissioning checklist that removes DNS entries; an inventory linking external services to hostnames; DNS change approvals; registrar account MFA; appropriate domain locking |
| **Detective measures** | Periodic review of subdomain dependencies against the inventory; alerts on DNS changes; monitoring of provider notifications |
| **Corrective measures** | Verify the external provider's resource status and whether the referenced name can actually be claimed before classifying the issue as a confirmed takeover exposure; if the service is no longer needed, remove the stale alias after approval; review any content or trust relationships tied to the subdomain |
| **Evidence to request before concluding** | Zone export; the inventory entry; the decommissioning record; the provider's confirmation of the external name's status; registrar MFA and lock status; DNS change approvals and audit trail; periodic review records; the exception list |

An analyst would not conclude that the risk is adequately addressed until the evidence shows both that the stale reference was handled and that the preventive and detective measures operate over time.

---

## References

Sources, official URLs, and verification notes are in [RESOURCES.md](04-resources.md).

---

*Return to: [README.md](01-README.md)*
