# Technical Write-Up: ISO/IEC 27001 Annex A.7 Physical Controls Audit Simulation and AWS Cloud Security Assessment

> **Project 1:** ISO/IEC 27001:2022 Annex A.7 (Physical Controls) Audit Simulation -- all 14 controls
> **Project 2:** AWS Cloud Security and Shared Responsibility Model Assessment -- simulated FinTech startup engagement
> **Method:** Control-by-control evidence mapping, evidence quality analysis, and structured risk spotting against a simulated organizational scenario
> **Companion Files:** [Business Impact and Risk Analysis](business-impact-a7-and-aws-cloud-security.md) -- [Evidence Matrix](evidence-matrix-a7-and-aws-cloud-security.md) -- [Resource and Reference Library](resource-a7-and-aws-cloud-security.md)

---

# Part 1 -- ISO/IEC 27001:2022 Annex A.7: Physical Controls Audit Simulation

## Scope Disclaimer

This analysis covers Annex A.7 (Physical Controls) only -- 14 of ISO 27001:2022's 93 total Annex A controls. It does not represent a complete ISMS control review. A.5 (Organizational), A.6 (People), and A.8 (Technological) controls are addressed in separate portfolio entries. Where A.7 controls intersect with organizational governance (for example, A.7.2 and the Joiner-Mover-Leaver access lifecycle documented in the Week 13 entry on A.5.15), that intersection is noted, but the governance control families themselves are not re-assessed here.

## 1.1 Methodology

The simulation was structured as a control-by-control audit walkthrough rather than a policy review. For each of the 14 A.7 controls, the exercise followed a consistent four-step reasoning process:

```
1. STATE the control's intent (what risk is this control designed to reduce)
2. IDENTIFY the evidence type an auditor would request (Design, Operating, Effectiveness)
3. MAP that evidence to a concrete artifact (CCTV footage, badge log, visitor logbook)
4. STRESS-TEST the evidence for quality gaps (would this evidence actually hold up)
```

Steps 1-3 build the baseline Evidence Matrix (documented in full in the companion [Evidence Matrix](evidence-matrix-a7-and-aws-cloud-security.md) file). Step 4 is where this simulation's two flagged findings originated -- a retention gap in CCTV evidence and a set of workflow gaps in the visitor management process -- both detailed below.

## 1.2 The Three Evidence Types: Design, Operating, Effectiveness

Before any control-specific analysis, the simulation first established a shared definition for the three evidence categories an auditor uses at every control, because conflating them is the single most common error in a first-pass physical controls review:

| Evidence Type | Question It Answers | Example for A.7.2 (Physical Entry) |
|---|---|---|
| **Design** | Does a documented control exist on paper? | The Physical Access Control Policy defines badge issuance, visitor sign-in, and entry logging requirements |
| **Operating** | Is the control being followed in practice, right now? | A sample of this month's badge logs and visitor sign-in sheets shows entries consistent with policy |
| **Effectiveness** | Does the control actually achieve its intended outcome over time? | A quarterly access review shows no former employees retain active badge access, and no tailgating incidents were recorded in the last review period |

A control can pass Design evidence and still fail Operating evidence (a policy exists but nobody follows it), and it can pass both Design and Operating evidence while still failing Effectiveness (the policy is followed exactly as written, but the policy itself has a gap that lets an unauthorized event occur anyway). This three-way distinction is the reasoning tool applied to every one of the 14 controls in the matrix.

## 1.3 Evidence Quality Analysis: The Four Quality Attributes

Beyond simply identifying what evidence exists, the simulation evaluated each evidence artifact against four quality attributes drawn from standard audit evidence theory:

| Attribute | What It Tests | Failure Example |
|---|---|---|
| **Authenticity** | Is the evidence genuinely what it claims to be, with no tampering? | A visitor logbook with pages that can be removed and replaced provides weak authenticity assurance |
| **Timeliness** | Was the evidence captured close to the event it documents, and is it still available when needed? | CCTV footage retained for a shorter period than an incident investigation window requires |
| **Completeness** | Does the evidence cover the full population, or only a sample that may miss exceptions? | A badge log that only captures successful entries, with no record of denied-access attempts |
| **Traceability** | Can the evidence be linked back to a specific, identifiable individual or event? | A shared visitor badge with no name field associates entry with "a visitor" rather than a specific person |

These four attributes are the analytical lens applied directly to the two flagged findings below.

## 1.4 Finding One: CCTV Retention Gap (Timeliness Failure)

**The simulated finding:** Corporate policy specifies a 90-day CCTV retention requirement for server room and secure area monitoring. On review, the storage system's actual configured retention period was found to be 30 days.

**Why this is a Timeliness failure, not a Design failure:** The Design evidence passes -- a documented 90-day retention policy exists and is approved. The Operating evidence is where the gap surfaces: the CCTV storage system's *actual* retention configuration does not match the policy's stated requirement. This is a Design-versus-Operating mismatch, which is a distinct and often more serious finding category than a missing policy, because it indicates the control was defined correctly but never verified in its running state.

**Why the gap matters for A.7.4 (Physical Security Monitoring) specifically:** A.7.4 exists to support two functions -- real-time detection of unauthorized physical access, and after-the-fact investigation when an incident is reported. A 30-day retention window satisfies the first function (footage is available to review this week's alerts) but critically undermines the second: any incident reported, discovered, or escalated more than 30 days after it occurred -- which is common, since physical security incidents are frequently noticed well after the fact (a missing asset discovered during a quarterly inventory, a suspicious access pattern flagged during a periodic access review) -- has no corresponding footage to review. The evidence exists in policy, but is not preserved long enough to be useful for the exact class of incident it is most needed for.

**Framing this as a Design-Operating gap for audit reporting:** The correct audit language distinguishes what was reviewed from what was found. The reviewer confirmed the retention policy was documented and approved (Design: satisfactory), then discovered the storage system's retention window was configured to 30 days against a 90-day requirement (Operating: does not conform). This framing matters because it directs the corrective action precisely -- the policy itself does not need rewriting; the storage configuration needs to be brought into alignment with the already-approved policy.

## 1.5 Finding Two: Physical Access Workflow Gaps

Two distinct workflow gaps were identified during the simulated walkthrough of the physical access process, each mapping to a different control and a different underlying weakness:

### 1.5.1 -- Tailgating into the Server Room (A.7.2, A.7.3)

**The gap:** The simulated scenario identified a workflow condition where an individual could follow an authorized badge-holder through a secure entry point (the server room door) without independently presenting credentials -- the well-documented "tailgating" pattern.

**Why badge logs alone cannot detect this:** A badge access log is a Completeness-limited evidence source for tailgating specifically. The log faithfully records every legitimate badge swipe, but by design it has no mechanism to record a person who entered *without* swiping. An auditor reviewing badge logs alone would see a fully populated, well-formatted log with no anomalies -- and would be looking at evidence that is complete for its own definition (all badge swipes) while being structurally incapable of surfacing the exact risk in question (entry without a swipe). This is why A.7.4 (Physical Security Monitoring, via CCTV) functions as a compensating evidence source for A.7.2 -- video evidence can show two people passing through a door on one badge swipe in a way a badge log cannot.

**Control mapping:** A.7.2 (Physical entry) is the primary control whose intent is undermined; A.7.3 (Securing offices, rooms and facilities) is secondary, since the server room qualifies as a defined secure area under this control, and tailgating into it is a direct instance of the control's threat model in the specific context of a *secure area* rather than a general premises entry point.

### 1.5.2 -- Unreturned and Unrevoked Visitor Badges (A.7.2)

**The gap:** The simulation identified that visitor badges issued for daytime access were not consistently returned at end-of-visit, and that badge access was not being programmatically revoked at end-of-day for badges that were not physically returned.

**Why this is a two-part failure, not one:** The first half (badge not returned) is a process compliance gap -- a person did not follow the checkout procedure. The second half (access not revoked regardless) is the more serious structural gap, because it means the control's effectiveness depends entirely on the first half succeeding. A well-designed visitor access control should not have valid, live access credentials outstanding overnight as its default state whenever a visitor forgets to check out; it should have same-day automatic expiration as the default, with badge return being a convenience rather than a security dependency. This finding directly informed the remediation direction of moving toward time-bound access credentials rather than relying on a manual return step (detailed in the [Business Impact and Risk Analysis](business-impact-a7-and-aws-cloud-security.md)).

## 1.6 GDPR Compliance Analysis: The Physical Visitor Logbook

The simulation identified two distinct GDPR violations in a common, easily overlooked artifact: a paper visitor logbook used at the front reception desk.

### 1.6.1 -- Confidentiality and Integrity: Sequential Exposure of Prior Visitors' Data

**The mechanism:** A physical, bound logbook where each visitor signs in on the next available line means every subsequent visitor can see the name, company, time of arrival, and host contact of every visitor who signed in before them on the same page.

**Why this is a Confidentiality violation and not merely a design inconvenience:** GDPR's confidentiality principle requires that personal data is processed in a manner that ensures appropriate security, including protection against unauthorized disclosure. A shared, sequentially-visible logbook actively discloses one data subject's personal data to another data subject with no legitimate basis for that second person to see it -- the second visitor has no business need to know who visited before them. This is a structural disclosure built into the artifact's physical design, occurring regardless of how well-intentioned or careful the front-desk staff are; no amount of staff training corrects a design flaw where the paper itself is the exposure mechanism.

**Why this also touches Integrity:** Because prior entries remain physically visible and editable (a pen-and-paper log has no access control on the page itself), any visitor with sign-in access could, in principle, alter or annotate a previous entry. This is a lower-likelihood but still relevant integrity concern layered on top of the primary confidentiality issue.

### 1.6.2 -- Data Minimization and Storage Limitation: Full National ID Number Collection

**The mechanism:** The simulated visitor logbook process recorded full National ID numbers from every visitor, with no documented retention period or disposal procedure once the logbook page was full or archived.

**Why this violates Data Minimization (GDPR Article 5(1)(c)):** Data minimization requires that personal data collected be adequate, relevant, and limited to what is necessary for the stated purpose. The stated purpose of a visitor log is to establish who was on premises, at what time, and who they visited -- a purpose fully satisfied by a name and a host contact. A full National ID number is a significantly more sensitive data category than the stated purpose requires; visitor identity verification (confirming the person is who they claim to be) can be satisfied by visually checking an ID card at the desk without transcribing the ID number itself into a retained log.

**Why this violates Storage Limitation (GDPR Article 5(1)(e)):** Storage limitation requires that personal data be kept no longer than necessary for the purposes for which it is processed, with a defined retention period. A logbook with no defined retention or disposal procedure means visitor National ID numbers persist indefinitely by default -- the absence of a deletion trigger is itself the violation, independent of how long the data has actually been sitting in a drawer at any given point in time.

**Why these are two separate GDPR principle violations, not one:** Data Minimization concerns what was collected in the first place (the ID number should never have been recorded at all); Storage Limitation concerns how long collected data is retained (even data legitimately collected still needs a deletion trigger). A remediation that only addresses retention (add a shredding schedule) but keeps recording ID numbers still violates Data Minimization; a remediation that stops collecting ID numbers but does not address the retention of the historical logbook data already on file still leaves a Storage Limitation gap on existing records. Both are addressed independently in the [Business Impact and Risk Analysis](business-impact-a7-and-aws-cloud-security.md).

## 1.7 Section Takeaways: Physical Controls Simulation

- **Physical controls are frequently evaluated on Design evidence alone, when Operating and Effectiveness evidence is where the real gaps live.** The CCTV retention finding would not have surfaced from a policy review; it required checking the actual system configuration against the policy.
- **An evidence source can be internally complete while being externally blind to the exact risk being investigated.** Badge logs are a complete record of badge swipes and a structurally incomplete record of tailgating, because tailgating is defined by the absence of a swipe.
- **A physical artifact's design can itself be the source of a data protection violation**, independent of staff behavior or training. A shared visitor logbook exposes prior visitors' data by its physical structure, not because any individual acted carelessly.

---
---

# Part 2 -- AWS Cloud Security and Shared Responsibility Model Assessment: FinTrust Startup

## 2.1 Methodology

Project 2 was structured around a single simulated organization -- "FinTrust Startup," a FinTech company with a defined AWS architecture -- to ground the cloud service model analysis, shared responsibility mapping, and risk spotting exercise in a consistent, evolving scenario rather than a series of disconnected service reviews.

### 2.1.1 -- FinTrust Startup: Simulated Architecture

| Component | AWS Service(s) | Function |
|---|---|---|
| Web and API layer | EC2, VPC | Customer-facing web application and API gateway |
| Transaction database | RDS (PostgreSQL) | Stores financial transaction records |
| KYC document storage | S3 | Stores uploaded identity documents (ID cards) for Know Your Customer verification |
| Developer remote access | AWS WorkSpaces | Virtual desktop environment for developer access to internal systems |
| (Referenced, not primary finding scope) | Lambda | Serverless functions referenced in the broader service model analysis |

### 2.1.2 -- Cloud Service Model Classification (IaaS / PaaS / SaaS)

The simulation classified each FinTrust service against the standard IaaS/PaaS/SaaS model to establish where the shared responsibility line falls for each:

| Service | Classification | Reasoning |
|---|---|---|
| EC2 | IaaS | AWS provides the virtualized compute layer; the customer manages the guest operating system, patching, and all software installed on top of it |
| VPC | IaaS (networking) | AWS provides the underlying network fabric; the customer defines and manages subnets, route tables, and security group rules |
| S3 | PaaS-like (AWS documentation classifies as a fully managed storage platform) | AWS manages the storage infrastructure, redundancy, and durability entirely; the customer's responsibility is scoped to what is stored, how it is encrypted, and who can access it |
| RDS | PaaS | AWS manages the underlying database engine installation, patching, and infrastructure; the customer manages schema, data, user accounts, and query-level access control |
| Lambda | PaaS/Serverless | AWS manages the entire execution environment; the customer is responsible only for the function code and its permissions |
| WorkSpaces | SaaS-like (Desktop-as-a-Service) | AWS manages the full virtual desktop stack; the customer manages user provisioning, MFA enforcement, and data handled within the workspace |

**The pattern this classification reveals:** as a service moves from IaaS toward SaaS, the *volume* of the customer's security responsibility decreases, but the *stakes* of what remains do not decrease at the same rate. This is the direct lead-in to the shared responsibility analysis below.

## 2.2 Shared Responsibility Model: Security OF the Cloud vs. Security IN the Cloud

AWS's shared responsibility model divides accountability into two categories: AWS is responsible for **security of the cloud** -- the physical infrastructure, hardware, and the underlying software that runs AWS's own services -- while the customer is responsible for **security in the cloud** -- what the customer builds, configures, stores, and controls access to on top of that infrastructure.

**Applying this to the FinTrust architecture directly:**

| Service | AWS Responsibility (Security OF) | FinTrust Responsibility (Security IN) |
|---|---|---|
| EC2 | Physical hosts, hypervisor, host OS patching | Guest OS patching, security group rules, application-level access control |
| S3 | Storage infrastructure, durability, physical redundancy | Bucket policies, public access settings, encryption configuration, IAM permissions on objects |
| RDS | Database engine patching, underlying infrastructure, automated backups (infrastructure level) | Database user accounts, credential management, schema-level access, network access rules to the DB |
| WorkSpaces | Virtual desktop infrastructure, hypervisor | User provisioning, MFA enforcement, data handled inside the desktop session |

**The critical lesson this exercise surfaced -- durability and availability are not confidentiality:** AWS's responsibility for S3 includes extremely high data durability guarantees at the infrastructure level. It is a common and consequential misreading of the shared responsibility model to interpret "AWS guarantees my data won't be lost" as "AWS guarantees my data is protected from unauthorized access." These are two entirely separate properties of data security -- durability concerns whether the data continues to exist and remains retrievable; confidentiality concerns who is permitted to retrieve it. AWS's infrastructure-level durability guarantee for S3 says nothing about whether a bucket is publicly readable, because bucket-level access configuration sits unambiguously on the customer's side of the responsibility line. This distinction is the direct analytical basis for Risk Finding One below.

## 2.3 Risk Finding One: S3 Public Exposure of KYC Documents

**The simulated risk:** FinTrust stores KYC identity documents (ID card images) in S3. The risk-spotting exercise focused on the possibility that a bucket holding these documents could be configured with public read access -- whether through an overly permissive bucket policy, a misconfigured Access Control List, or the "Block Public Access" account-level setting being disabled.

**Why this specific risk was prioritized over other S3 misconfigurations:** KYC documents are a uniquely high-sensitivity data category for a FinTech organization -- they typically include a government-issued ID image, a full name, a date of birth, and often a document number, which together constitute a near-complete identity theft toolkit if exposed. Unlike a generic file storage misconfiguration, an exposed KYC bucket does not just risk internal data loss; it risks direct financial fraud enablement against FinTrust's own customers using documents customers were legally required to submit as part of onboarding.

**Why "S3 is highly durable" does not address this risk:** As established in Section 2.2, S3's infrastructure-level durability guarantee is orthogonal to bucket-level access configuration. A KYC document bucket can simultaneously have effectively zero risk of accidental data loss (extremely high durability, AWS's responsibility) and a critical risk of unauthorized public exposure (bucket policy misconfiguration, FinTrust's responsibility). Evaluating whether KYC storage is adequately access-controlled by checking only durability metrics would produce a false sense of assurance while leaving the actual access-control risk completely unassessed.

**Relevant recommended direction (detailed fully in Business Impact file):** Enforcing S3 Block Public Access at the account level as a default-deny baseline, combined with least-privilege IAM policies scoped to only the specific application roles that require KYC bucket access, and server-side encryption using a customer-managed KMS key rather than relying solely on default encryption.

## 2.4 Risk Finding Two: RDS Master Credential Sharing (Individual Accountability Gap)

**The simulated risk:** FinTrust developers were found to be sharing the RDS PostgreSQL "Master User" password among the development team as a common practice for troubleshooting and directly addressing defects in the production database.

**Why this is fundamentally an accountability problem, not merely a password hygiene problem:** The immediate-seeming issue is that a shared secret is inherently harder to keep confidential than an individually-held one. But the deeper and more consequential issue is what happens *after* a shared credential is used: every query, schema change, or data access performed under the shared Master User account is attributed to "the Master User" in database logs, with no way to determine *which specific developer* performed *which specific action*. If a data integrity incident occurs -- a bad UPDATE statement corrupts financial transaction records, or a query inadvertently exposes data it should not have -- the audit trail leads to a dead end: the logs confirm *that* the Master User performed the action, but cannot answer *who* was at the keyboard.

**Why this matters more for a FinTech organization specifically:** Financial services organizations face materially higher scrutiny around data integrity and access accountability than most other sectors, precisely because the data in question (financial transaction records) has direct monetary consequences if altered incorrectly, and regulators and auditors in this space specifically expect individual-level accountability for any privileged access to financial data stores -- "our Master User account did it" is not an acceptable answer to a regulator asking who modified a customer's transaction history.

**Why the default alternative (individual database passwords per developer) is an incomplete solution:** A straightforward alternative -- create a separate database user account with a separate password for each developer -- addresses the attribution problem but reintroduces the original password-hygiene problem at a larger scale: now there are multiple long-lived database passwords to store, rotate, and protect instead of one, multiplying the credential-management burden rather than eliminating it.

**Why AWS IAM Database Authentication is the better-fit direction for this specific gap:** RDS for PostgreSQL supports IAM database authentication, which allows each developer to authenticate to the database using their own individual AWS IAM identity and a short-lived, automatically generated authentication token (each token valid for approximately 15 minutes) rather than a static password. This achieves both goals simultaneously that a shared password and a set of individual passwords each only achieve one of: authentication is tied to an individually identifiable IAM principal (solving the accountability gap), and there is no long-lived password for any individual to manage, share, or leak (solving the credential-hygiene problem, and eliminating the underlying incentive that led to password-sharing as a "convenient" workaround in the first place). This direction, along with AWS Secrets Manager and Just-In-Time access as complementary measures for cases where IAM-native authentication is not available, is developed fully in the [Business Impact and Risk Analysis](business-impact-a7-and-aws-cloud-security.md).

## 2.5 Auditor Testing Approaches for Cloud Evidence

A distinct methodological question the simulation addressed: given that AWS resources are configuration states rather than physical objects, what does "testing" a control even mean for a cloud service, and how does an auditor gather evidence for it? Four standard testing approaches were mapped against the FinTrust architecture (full detail in the companion [Evidence Matrix](evidence-matrix-a7-and-aws-cloud-security.md)):

| Testing Approach | What It Involves | Example Applied to FinTrust |
|---|---|---|
| **Interview** | Asking personnel to describe how a control operates in practice | Asking a developer to describe how they currently connect to the production RDS instance, surfacing the shared Master User practice |
| **Document Review** | Reviewing written policies, configuration exports, or IAM policy JSON | Reviewing the S3 bucket policy JSON and IAM policy documents attached to application roles accessing the KYC bucket |
| **Observation** | Directly observing a control being exercised, live | Observing a developer's WorkSpaces login process to confirm MFA is actually prompted, rather than only confirming MFA is enabled in policy |
| **Sampling** | Reviewing a subset of a larger population to draw a conclusion about the whole | Sampling a set of RDS query logs across a date range to check for entries attributable to the shared Master User account versus individually identifiable users |

**Why cloud auditing leans more heavily on Document Review than traditional physical auditing does:** Unlike a physical control (where an auditor can walk the floor and directly observe a locked door), a cloud configuration state is not directly observable without either console access or an exported configuration artifact. This makes Document Review -- reviewing IAM policy JSON, S3 bucket policy documents, security group rule sets -- the primary evidence-gathering method for most cloud controls, with Observation reserved for behavior that a static configuration export cannot fully capture, such as confirming an MFA prompt actually appears during a live login rather than only confirming an MFA requirement is set in policy.

## 2.6 Startup-Appropriate Remediation Design Philosophy

A recurring consideration throughout Project 2 was that GRC remediation approaches suitable for a large, mature enterprise are frequently impractical for an early-stage startup with a small engineering team and limited dedicated security headcount. Three specific design choices reflect this:

- **MFA enforcement** was proposed as an account-wide IAM policy requirement rather than a per-service configuration, because a startup-scale engineering team benefits more from one consistently-enforced baseline than from service-by-service MFA policies that are individually simple but collectively easy to miss one of.
- **Just-In-Time (JIT) access** was proposed over standing privileged access specifically for the WorkSpaces developer environment, because a startup's small team means privileged access requests are infrequent enough that a time-bound approval workflow adds minimal friction, while removing the much larger risk surface of privileged credentials that remain valid indefinitely.
- **AWS Secrets Manager** was proposed as the credential-management approach for any service or scenario where IAM-native authentication is not available (for example, third-party API keys FinTrust's application code needs to call external services), specifically because it centralizes credential rotation and access logging without requiring the startup to build or maintain any custom secrets infrastructure of its own.

## 2.7 Section Takeaways: AWS Cloud Security Assessment

- **High availability and durability are not the same property as confidentiality.** AWS's infrastructure-level guarantees for a service like S3 say nothing about whether that service's access configuration is appropriately controlled -- these are separate axes of the CIA triad, governed by separate parts of the shared responsibility line.
- **Individual accountability in database access is a distinct security property from credential secrecy**, and a solution optimized only for the latter (more passwords) can make the former worse by increasing the number of long-lived secrets in circulation. IAM Database Authentication addresses both simultaneously because it removes the long-lived credential rather than merely multiplying it.
- **Cloud control testing relies more heavily on Document Review than physical control testing does**, because most cloud controls exist as configuration state rather than directly observable physical conditions -- a fact that shapes which of the four testing approaches (Interview, Document Review, Observation, Sampling) an auditor reaches for first at each control.
- **Remediation design for a startup is not simply "the enterprise solution, but smaller."** The right-sized answer for a five-person engineering team (account-wide MFA, JIT access, centralized secrets management) is a genuinely different design choice from the equivalent enterprise answer, not merely a scaled-down version of it.

---

## References

- ISO/IEC 27001:2022 (Third Edition), Annex A, Theme 7 -- Physical Controls
- ISO/IEC 27002:2022 -- Implementation guidance for Annex A controls
- Regulation (EU) 2016/679 (GDPR), Article 5(1)(c) Data Minimization and Article 5(1)(e) Storage Limitation
- AWS Shared Responsibility Model
- AWS Documentation -- IAM Database Authentication for MariaDB, MySQL, and PostgreSQL

---

*Return to: [Week 14 README](week14-readme.md)*
