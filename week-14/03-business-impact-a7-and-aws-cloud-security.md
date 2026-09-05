# Business Impact and Risk Analysis: ISO/IEC 27001 Annex A.7 Physical Controls and AWS Cloud Security Assessment

> **Scope:** Business impact, risk classification, and proposed remediation direction for findings identified across the Annex A.7 Physical Controls simulation and the FinTrust Startup AWS Cloud Security assessment
> **Companion Files:** [Technical Write-Up](write-up-a7-and-aws-cloud-security.md) -- [Evidence Matrix](evidence-matrix-a7-and-aws-cloud-security.md) -- [Resource and Reference Library](resource-a7-and-aws-cloud-security.md)

---

## Part 1 -- Physical Controls: Business Impact and Risk Analysis

### 1.1 Finding: CCTV Retention Gap (30-Day Actual vs. 90-Day Policy Requirement)

| Field | Detail |
|---|---|
| **Finding Classification** | Nonconformity candidate -- Operating evidence does not conform to Design evidence |
| **Severity** | Medium-High |
| **Control Mapping** | A.7.4 (Physical security monitoring) -- primary |
| **Evidence Type Affected** | Operating (Design evidence, the policy itself, was satisfactory) |

**Business impact analysis:**

The direct business consequence of this gap is an **evidentiary blind spot for any incident investigation window exceeding 30 days.** For a physical security incident to fall within this gap, it does not need to be a slow-moving investigation -- it only needs to be *discovered* more than 30 days after it occurred, which is a common pattern for physical security events specifically: an asset going missing is often first noticed during a periodic inventory check, not at the moment of removal; an unauthorized access pattern is often first flagged during a quarterly access review, not in real time.

For an organization handling any regulated or contractually sensitive information in the affected secure areas, this gap has a secondary compliance dimension: a documented 90-day retention *policy* implies a corresponding compliance or contractual obligation was the basis for setting that specific number, and a 30-day actual retention window means the organization cannot demonstrate it is meeting whatever obligation drove the 90-day requirement in the first place -- the policy exists to satisfy something, and the something is not being satisfied.

**Proposed remediation direction:** Align the CCTV storage system's configured retention window to the documented 90-day policy requirement, and add a periodic verification step (for example, a quarterly check comparing configured retention against policy) to the organization's internal audit calendar, so that a Design-versus-Operating mismatch of this kind is caught through a scheduled control rather than relying on it surfacing incidentally during an unrelated review.

### 1.2 Finding: Tailgating Into the Server Room

| Field | Detail |
|---|---|
| **Finding Classification** | Nonconformity candidate |
| **Severity** | High |
| **Control Mapping** | A.7.2 (Physical entry) -- primary; A.7.3 (Securing offices, rooms and facilities) -- secondary |
| **Evidence Type Affected** | Effectiveness (badge log Operating evidence appeared complete; the actual security outcome was not achieved) |

**Business impact analysis:**

A server room is, by definition, the physical location holding the organization's highest-concentration information assets in one place. Unauthorized physical entry to this specific location -- as opposed to a general office area -- carries a materially higher impact ceiling: direct physical access to server hardware can enable data exfiltration via physical media, hardware tampering, or outright theft of equipment containing sensitive data, none of which require defeating any logical (network or application-layer) control at all. This finding is therefore evaluated at High severity specifically because of *where* the gap occurs, not merely that the gap exists in general.

The business impact is compounded by the detection gap documented in the companion write-up: because badge logs cannot, by their design, record entry that occurs without a badge swipe, an organization relying solely on badge log review has no visibility into whether this risk has already been exploited in the past. The absence of anomalies in a badge log is not evidence of absence of tailgating; it is an artifact of the evidence source's blind spot.

**Proposed remediation direction:** Recommended a combination of a physical access control mechanism that structurally resists tailgating (for example, a mantrap-style single-person entry vestibule at the server room door specifically, rather than relying on staff vigilance or signage), combined with positioning CCTV coverage (A.7.4) directly at this entry point as a compensating detective control that can surface tailgating events a badge log cannot.

### 1.3 Finding: Unreturned and Unrevoked Visitor Badges

| Field | Detail |
|---|---|
| **Finding Classification** | Nonconformity candidate |
| **Severity** | Medium |
| **Control Mapping** | A.7.2 (Physical entry) |
| **Evidence Type Affected** | Operating (the badge return step in the documented process was not being consistently followed) |

**Business impact analysis:**

The business risk here scales with the number of outstanding unreturned badges over time rather than being a single, one-time exposure -- each visit that ends without a badge return adds one more live, valid credential to a growing population of unaccounted-for access devices. A visitor badge that is never returned and never programmatically expires functions, from a risk perspective, identically to an unauthorized access credential: it grants building access to whoever physically possesses it, with no ongoing verification that the original visitor (rather than someone who later obtained the badge) is the person using it.

The compounding factor identified in the underlying process design is that the *only* mechanism ensuring access revocation is a manual physical return step -- meaning the security outcome depends entirely on human follow-through with no structural backstop if that follow-through fails, which is precisely the condition that produced the accumulating gap in the first place.

**Proposed remediation direction:** Recommended a shift from "access valid until physically returned" to "access valid until end-of-day, automatically" as the default state for all visitor credentials -- for example, time-bound electronic visitor badges that automatically deactivate at close of business regardless of physical return status, making badge return a housekeeping convenience rather than the sole security control.

### 1.4 Finding: GDPR Violation -- Sequential Exposure of Prior Visitors' Data (Confidentiality and Integrity)

| Field | Detail |
|---|---|
| **Finding Classification** | Compliance violation |
| **Severity** | Medium |
| **Regulatory Mapping** | GDPR -- Confidentiality principle (Article 5(1)(f)); secondary Integrity consideration |
| **Control Mapping** | A.7.2 (Physical entry) -- the visitor sign-in artifact itself |

**Business impact analysis:**

The core business risk is regulatory exposure from a data protection violation that is structural rather than incident-driven -- this is not a single breach event but an ongoing, continuous disclosure occurring at every single visitor sign-in, for as long as the shared paper logbook remains in use. This distinction matters for how the risk is communicated internally: it is not a "what if this happens" risk, but a "this is currently happening, every day" finding, which materially changes the urgency framing for remediation prioritization.

There is a secondary reputational dimension specific to a visitor-facing artifact: unlike most data protection gaps, which are invisible to the data subjects affected by them, this particular gap is directly visible to the very people it affects -- any visitor who has ever glanced at the logbook while signing in has personally witnessed the previous visitor's exposed information, and can reasonably infer their own entry will be equally visible to the next visitor. This creates a direct, visible trust signal to external visitors (which may include clients, auditors, or partners) about the organization's data handling practices, independent of whether the organization has any other, more serious data protection gaps elsewhere.

**Proposed remediation direction:** Recommended replacing the shared paper logbook with either an individual sign-in slip system (one form per visitor, collected and stored separately rather than left on a shared page) or a digital visitor management system where each visitor's entry is only visible to authorized staff, not to subsequent visitors.

### 1.5 Finding: GDPR Violation -- Full National ID Number Collection Without Retention Policy (Data Minimization and Storage Limitation)

| Field | Detail |
|---|---|
| **Finding Classification** | Compliance violation |
| **Severity** | Medium-High |
| **Regulatory Mapping** | GDPR Article 5(1)(c) Data Minimization; GDPR Article 5(1)(e) Storage Limitation |
| **Control Mapping** | A.7.2 (Physical entry) -- the visitor identity verification step |

**Business impact analysis:**

This finding is evaluated as two separate, compounding risk vectors rather than one, in direct correspondence with the two GDPR principles it violates. The Data Minimization violation creates an ongoing collection risk: every new visitor's National ID number recorded going forward adds to a growing store of highly sensitive personal identifiers that were never necessary to collect for the stated visitor-management purpose, meaning the organization is continuously accumulating unnecessary exposure with each new entry, not carrying an unchanging, historical risk. The Storage Limitation violation separately creates a retention risk on data already collected: with no defined disposal trigger, historical logbooks containing years of visitor National ID numbers may exist somewhere in the organization's records with no mechanism ensuring their eventual destruction, representing a large, static pool of highly sensitive data with no reducing force acting on it over time.

The combined business impact is disproportionate to the apparent administrative simplicity of the artifact causing it: a paper visitor logbook is typically treated as a low-priority, low-visibility administrative item, yet in this case it is the source of two independent GDPR principle violations involving one of the most sensitive personal identifier categories that exists. This is a useful illustration for a portfolio audience of why a full information asset inventory (mapped to A.5.9 in Annex A.5) needs to extend to physical, non-digital artifacts and not only digital systems -- a paper logbook at a reception desk is as much an information asset requiring a documented retention policy as any database table.

**Proposed remediation direction:** Two independent corrective actions, addressing each violated principle separately. For Data Minimization: discontinue recording full National ID numbers in the visitor log; replace with a visual ID check at the desk (confirming the visitor's identity against their presented ID) without transcribing the ID number itself, since a name and host contact fully satisfy the stated visitor-management purpose. For Storage Limitation: define and document a retention period for visitor log records going forward (informed by the organization's actual legitimate need, likely a matter of months rather than indefinite retention), and separately address the disposal of historical logbook records already on file that were collected under the prior, non-compliant process.

---

## Part 2 -- AWS Cloud Security: FinTrust Startup Business Impact and Risk Analysis

### 2.1 Risk Finding: S3 Public Exposure of KYC Documents

| Field | Detail |
|---|---|
| **Risk Classification** | High-severity access control risk |
| **Affected Asset** | S3 bucket storing KYC identity documents (ID card images) |
| **Shared Responsibility Mapping** | Customer responsibility (Security IN the cloud) -- bucket policy and access configuration |
| **CIA Triad Property Affected** | Confidentiality |

**Business impact analysis:**

For a FinTech organization specifically, KYC documents occupy a uniquely high-consequence position in the data sensitivity hierarchy: they are, by regulatory design, the exact category of document that verifies a customer's real-world identity, meaning their exposure does not merely risk generic data loss but risks direct enablement of identity theft and financial fraud against FinTrust's own customer base, using documents those customers were legally required to submit to open an account. This shifts the impact analysis from "data breach" in the generic sense to a specific, foreseeable harm to identifiable third parties (FinTrust's customers), which is a materially more severe framing for both regulatory exposure and customer trust impact.

There is a direct connection here to the shared responsibility model analysis in the companion write-up: because S3's infrastructure-level durability guarantee is entirely orthogonal to bucket-level access configuration, an organization that monitors only availability and durability metrics for its KYC storage (both of which AWS guarantees at a very high standard) could have full confidence in those metrics while a public-read bucket policy misconfiguration sits completely unmonitored and undetected -- the metrics an organization is most likely to check by default are not the metrics that would reveal this specific risk.

**Proposed remediation direction:**
- Enforce S3 Block Public Access at the account level as a default-deny baseline for all buckets, not only the KYC bucket specifically, so that a similar misconfiguration on any future bucket is prevented by default rather than requiring per-bucket vigilance.
- Scope IAM policies for any application role accessing the KYC bucket to the minimum required actions (for example, read access for a document-verification service, without broader list or delete permissions unless specifically justified).
- Apply server-side encryption using a customer-managed AWS KMS key rather than relying solely on default encryption, so that key access itself becomes an additional access-control layer independently auditable from the bucket policy.
- Recommended a recurring, scheduled configuration review (rather than a one-time check) specifically for any bucket holding KYC or other high-sensitivity customer documents, given that access misconfigurations are a common cause of exposure precisely because they can be introduced by a later, unrelated change long after the bucket's access controls were originally configured correctly.

### 2.2 Risk Finding: RDS Master Credential Sharing (Individual Accountability Gap)

| Field | Detail |
|---|---|
| **Risk Classification** | High-severity access control and accountability risk |
| **Affected Asset** | RDS PostgreSQL instance storing financial transaction records |
| **Shared Responsibility Mapping** | Customer responsibility (Security IN the cloud) -- database user account management |
| **CIA Triad Property Affected** | Integrity (primary); Confidentiality (secondary) |

**Business impact analysis:**

The immediate operational risk of shared Master User credentials is the loss of individual accountability documented in the companion write-up, but the business impact analysis extends further: for a financial services organization, the database in question stores financial transaction records, meaning any data integrity incident here -- an incorrect update, an accidental deletion, an unauthorized modification -- has a direct financial consequence to real customer account balances or transaction histories, not merely an internal data quality issue. When an incident of this kind occurs against a shared-credential account, FinTrust faces a compounding problem beyond the incident itself: it cannot answer the specific accountability question a regulator, an affected customer, or an internal post-incident review would reasonably ask, which is precisely which individual performed the action that caused it.

This finding also carries forward-looking business risk beyond any single incident: as FinTrust seeks funding, banking partnerships, or eventual regulatory licensing appropriate to a financial services company, due diligence reviews from investors, banking partners, or regulators routinely examine privileged access controls over financial data systems as a standard checkpoint. A shared Master User credential practice, if discovered during such a review, is the kind of finding that can materially affect a funding round or partnership negotiation, independent of whether any actual incident has occurred using that shared access -- the absence of individual accountability is itself the finding, not merely a risk factor for some other, separate finding.

**Proposed remediation direction:**
- Enable and enforce IAM Database Authentication for RDS PostgreSQL, allowing each developer to authenticate using their own individual IAM identity via short-lived, automatically generated authentication tokens rather than a static, shared password -- directly closing the accountability gap while simultaneously removing the long-lived credential that created the incentive for password-sharing in the first place.
- For any access pattern where IAM-native authentication is not immediately available or practical (for example, third-party tools requiring traditional connection strings), recommended AWS Secrets Manager as an interim credential-management layer, providing centralized rotation and access logging even for password-based connections, as a materially better position than an unmanaged shared password with no rotation or centralized audit trail.
- Recommended Just-In-Time (JIT) access as the target access model for any privileged production database action, so that even individually-attributed access is time-bound and requires an explicit approval step, rather than standing individual credentials that remain valid indefinitely once issued.
- Recommended explicitly retiring direct use of the Master User account for day-to-day developer troubleshooting, reserving it strictly for emergency break-glass scenarios with its own separate approval and logging process.

---

## References

- ISO/IEC 27001:2022 Annex A.7.2 (Physical entry), A.7.3 (Securing offices, rooms and facilities), A.7.4 (Physical security monitoring)
- Regulation (EU) 2016/679 (GDPR), Article 5(1)(c) Data Minimization, Article 5(1)(e) Storage Limitation, Article 5(1)(f) Confidentiality
- AWS Shared Responsibility Model
- AWS Documentation -- IAM Database Authentication for MariaDB, MySQL, and PostgreSQL

---

*This analysis was developed as part of a self-directed cybersecurity portfolio project. FinTrust Startup is an entirely fictional organization created for educational purposes; all findings and architecture details are simulated.*

---

*Return to: [Week 14 README](week14-readme.md)*
