# Business Impact and Risk Analysis: ISO/IEC 27001 Annex A.8 (A.8.1-A.8.20) and AWS Cloud Risk Assessment -- NovaStream SaaS

> **Scope:** Business impact, risk classification, threat modeling, and proposed remediation direction for findings identified across Annex A.8 controls A.8.1-A.8.20 and the AWS cloud risk assessment, all mapped to the simulated organization NovaStream SaaS
> **Companion Files:** [Technical Write-Up](write-up-a8-and-aws-cloud-risk.md) -- [Resources and Reference Library](resource-a8-and-aws-cloud-risk.md)

---

## Risk Register Methodology: Likelihood, Remediation SLA, and Ownership

Each finding below is documented as a five-part risk register entry: Severity, Likelihood, Remediation SLA, Owner, and the underlying business impact narrative. Severity alone answers "how bad would this be if it materialized"; Likelihood, SLA, and Owner together answer the three questions a risk register exists to make actionable: how probable is this, how fast does it need to close, and who is accountable for closing it.

**Likelihood and Remediation SLA are modeled after common industry vulnerability management practice -- the general principle, reflected across guidance such as NIST SP 800-40 and widely-used enterprise vulnerability management SLA tiers, that response urgency should scale directly and tightly with severity -- adapted for a startup's agile operational tempo.** The specific day-ranges below are a startup-appropriate compression of that principle rather than a literal citation of any single framework's published timeframes, since published enterprise guidance (including NIST SP 800-40) is deliberately risk-based rather than prescriptive about exact day-counts, and typically assumes a larger organization's longer change-approval cycles than NovaStream's flatter engineering organization requires.

| Severity | Likelihood | Remediation SLA |
|---|---|---|
| Critical | High | 24-48 hours |
| High | Medium-High to High | 7 days |
| Medium-High | Medium | 14-30 days |

**Ownership is assigned to startup-appropriate operational roles rather than a dedicated security function**, reflecting NovaStream's current stage as a high-growth startup without a large, dedicated enterprise security team: Engineering Lead / DevOps Lead owns source code and endpoint-level findings; Data / Platform Team owns backup, key management, and database resilience findings; Cloud Infrastructure Team owns network, IAM, and cloud configuration findings.

---

## Part 1 -- A.8.1-A.8.10 Findings: Business Impact and Risk Analysis

### 1.1 Finding: A.8.4 -- Missing Branch Protection on Production Repositories

| Field | Detail |
|---|---|
| **Finding Classification** | Nonconformity candidate |
| **Severity** | High |
| **Likelihood** | Medium-High to High |
| **Remediation SLA** | 7 days |
| **Owner** | Engineering Lead / DevOps Lead |
| **Control Mapping** | A.8.4 (Access to source code) |
| **Threat Scenario** | Unauthorized or unreviewed source code modification reaching production |

**Business impact analysis:**

For a B2B SaaS company, the production codebase is the company's core product delivery mechanism, and an unreviewed change reaching it carries two distinct impact categories that compound each other. The first is availability and quality risk: a change that has not passed peer review has not benefited from a second set of eyes checking for logic errors, unintended side effects, or interactions with other parts of the system -- for a SaaS product serving paying B2B customers under some form of service-level expectation, a production incident traced back to a change nobody but its author ever reviewed is a materially harder incident to explain to an affected customer than one caused by a reviewed change that had an unforeseen edge case.

The second, more severe impact category is the insider-risk and supply-chain angle: without mandatory review, a single developer -- whether acting maliciously, having their credentials compromised, or simply making an unintentional but consequential change -- has an unobstructed path to modify production behavior with no independent verification step in between. For a SaaS company whose product itself is the thing every customer depends on, this is functionally equivalent to having no code-integrity control at all over the most critical asset the company operates.

There is also a forward-looking commercial dimension specific to a growth-stage B2B startup: as NovaStream pursues larger enterprise customers, security due diligence questionnaires and vendor risk assessments routinely and specifically ask whether code changes require peer review before reaching production. A finding of this kind, if surfaced during a prospective customer's security review rather than through NovaStream's own internal audit, risks stalling or losing a deal at a stage where the commercial cost of the finding is considerably higher than the cost of corrective action taken earlier.

**Proposed remediation direction:** Analyzed that enabling a GitHub branch protection ruleset on the default production branch, requiring at least one approving review before merge and applying the rule to repository administrators as well as standard contributors, would close this specific gap at the platform-configuration level rather than relying on a documented expectation alone. Recommended this as a first-priority action given the low effort required to apply it relative to its risk reduction.

### 1.2 Finding: A.8.1 -- Incomplete MDM Full-Disk Encryption Enforcement

| Field | Detail |
|---|---|
| **Finding Classification** | Nonconformity candidate |
| **Severity** | Medium-High |
| **Likelihood** | Medium |
| **Remediation SLA** | 14-30 days |
| **Owner** | Engineering Lead / DevOps Lead |
| **Control Mapping** | A.8.1 (User endpoint devices) |
| **Threat Scenario** | Unencrypted endpoint loss exposing data at rest |

**Business impact analysis:**

The business risk scales directly with NovaStream's specific operating model: a distributed, remote-first B2B software startup has, by the nature of that structure, a continuously larger population of laptops in transit, in co-working spaces, and in employees' homes than a traditional office-based organization would -- meaning the base rate of device loss or theft that any organization must plan for is proportionally elevated for a company built this way. Without Full-Disk Encryption strictly and verifiably enforced, each of those devices represents a standing exposure: a lost or stolen laptop's storage can be read directly by removing the drive and mounting it on separate hardware, entirely bypassing any login screen, credential, or session timeout the device's operating system presents.

The specific data categories at risk on a developer endpoint compound the severity: cached source code (connecting this finding directly to the A.8.4 source-code-integrity concern above, since a device with unreviewed local commit history and no disk encryption is a single point of exposure for both source code confidentiality and integrity), locally cached authentication tokens or session credentials that could provide a path into production systems, and potentially customer data pulled locally for debugging or support purposes.

**Proposed remediation direction:** Recommended an audit of the existing MDM platform's built-in per-device compliance reporting to identify specifically which enrolled endpoints do not currently show FDE as active, followed by a remediation push scoped only to those specific non-compliant devices rather than a full platform reconfiguration. Proposed adding FDE compliance as a recurring, scheduled check rather than a one-time verification, since new devices are continuously being provisioned for a growing team.

---

## Part 2 -- A.8.11-A.8.20 Findings: Business Impact and Risk Analysis

### 2.1 Finding: A.8.13 -- Backup Restore Failure from Encryption Key Rotation Mismatch

| Field | Detail |
|---|---|
| **Finding Classification** | Nonconformity candidate |
| **Severity** | Critical |
| **Likelihood** | High |
| **Remediation SLA** | 24-48 hours |
| **Owner** | Data / Platform Team |
| **Control Mapping** | A.8.13 (Information backup) |
| **Threat Scenario** | Permanent data loss from unverified backups |

**Business impact analysis:**

This finding is evaluated at the highest severity level in this entry because of a specific structural property: it produces zero warning signal before the moment it is needed, and at the moment it is needed, the failure is total and permanent. Every operational signal an organization would normally rely on -- job completion status, absence of error alerts, backup file existing at the expected size -- reports as entirely healthy right up until an actual restore is attempted, at which point the backup is discovered to be permanently unreadable rather than merely delayed or partially degraded. There is no partial-recovery path available once the encrypting key required to decrypt a specific backup generation is no longer accessible; encryption is functioning exactly as designed, and that design property becomes a liability rather than a protection at the precise moment recovery is needed.

For NovaStream specifically, the business consequence of this gap materializing during an actual incident (a database corruption event, a ransomware event, or accidental data deletion) would be the loss of all data since the last backup generation encrypted under a key that remains accessible -- and depending on how far back the key rotation event occurred relative to the incident, this could represent a substantial, unrecoverable gap in customer data, transaction history, or product state, with direct consequences for customer trust, contractual data-retention obligations, and potentially regulatory exposure depending on the data categories involved.

The fact that this finding was only surfaced through a live restore simulation, rather than through routine monitoring, is itself the most important part of the business case for remediation: it demonstrates that NovaStream's existing operational monitoring provides false assurance on this specific risk, and that the same false assurance would have persisted indefinitely without a deliberate test.

**Proposed remediation direction:** Recommended establishing an explicit encryption key retention policy directly tied to the backup retention period -- any key used to encrypt a backup generation must remain available and accessible for at least as long as that specific backup generation is retained, even after the key is rotated for future use. Proposed scheduling recurring live restore tests (not merely reviewing backup job status) as a standing verification practice, given that this is the only method that actually surfaced the gap in this simulation.

### 2.2 Finding: A.8.17 -- NTP Drift Breaking Incident Response Forensic Timelines

| Field | Detail |
|---|---|
| **Finding Classification** | Nonconformity candidate |
| **Severity** | Medium-High |
| **Likelihood** | Medium |
| **Remediation SLA** | 14-30 days |
| **Owner** | Cloud Infrastructure Team |
| **Control Mapping** | A.8.17 (Clock synchronization) |
| **Threat Scenario** | Log tampering and forensic timeline corruption during incident response |

**Business impact analysis:**

The business risk here is latent rather than immediate: under normal operating conditions, a five-minute clock drift between on-premise and cloud environments has no observable operational consequence at all -- systems continue functioning, transactions continue processing, and no dashboard or alert would surface the drift as a problem. The risk materializes specifically and only during the one scenario where log timestamp accuracy becomes mission-critical: an active security incident requiring forensic reconstruction of what happened, in what order, and where an attacker's activity moved between environments.

For NovaStream, this creates a specific and severe form of risk concentration: the exact moment this gap matters most (during a live incident, when decisions about scope, containment, and disclosure obligations are being made under time pressure) is also the exact moment the gap is most likely to actively mislead the investigating team, rather than merely fail to help them. An investigator reconstructing an attack chain from logs that appear precisely timestamped, but are silently offset by five minutes between environments, risks drawing an incorrect conclusion about which system was compromised first or how an attacker moved laterally -- a wrong causal conclusion during incident response can lead to an incomplete containment action, leaving an actual point of compromise unaddressed while effort is misdirected toward a system that was actually a secondary, not primary, point of entry.

There is also a downstream credibility dimension: if NovaStream's incident timeline is later required for a customer notification, a regulatory report, or a cyber-insurance claim, a forensic reconstruction later found to be inaccurate due to an uncorrected clock drift undermines confidence in the entire incident response process, independent of how well the actual containment and remediation work was performed.

**Proposed remediation direction:** Recommended configuring both on-premise and cloud environments to synchronize against the same authoritative NTP source (or a small, deliberately synchronized set of sources), closing the drift at its root cause rather than attempting to reconcile timestamps after the fact during a future investigation. Identified this as a low-cost, configuration-level change appropriate for immediate action given the disproportionately high forensic-integrity value it provides relative to the effort required to apply it.

---

## Part 3 -- AWS Cloud Risk Assessment Findings: Business Impact and Risk Analysis

### 3.1 Risk: Unintended Public Storage Exposure (S3)

| Field | Detail |
|---|---|
| **Risk Classification** | High-severity access control risk |
| **Likelihood** | Medium-High to High |
| **Remediation SLA** | 7 days |
| **Owner** | Cloud Infrastructure Team |
| **Shared Responsibility Mapping** | Customer responsibility (Security IN the cloud) |
| **CIA Triad Property Affected** | Confidentiality |

**Business impact analysis:** A publicly-accessible S3 bucket converts whatever data category NovaStream stores there into a directly retrievable resource for anyone aware of the bucket's existence, with no authentication barrier at all -- for a B2B SaaS company, this could plausibly include customer-uploaded files, application logs containing sensitive operational detail, or backup artifacts, any of which becoming publicly discoverable would represent a direct, foreseeable data exposure to NovaStream's own customers rather than a hypothetical or abstract risk category.

**Proposed remediation direction:** Recommended enforcing S3 Block Public Access at the account level as a default-deny baseline across all buckets, combined with AWS Config rules configured to continuously evaluate bucket public-access status rather than relying on a one-time manual check.

### 3.2 Risk: Over-Privileged Access and Missing MFA (IAM)

| Field | Detail |
|---|---|
| **Risk Classification** | High-severity access control risk |
| **Likelihood** | Medium-High to High |
| **Remediation SLA** | 7 days |
| **Owner** | Cloud Infrastructure Team |
| **Shared Responsibility Mapping** | Customer responsibility (Security IN the cloud) |
| **CIA Triad Property Affected** | Confidentiality, Integrity |

**Business impact analysis:** A privileged IAM identity without MFA enforced depends entirely on password secrecy as its only defense -- if that password is exposed through any of the routine channels credentials leak through (a phishing message, a reused password from a separate breach, an accidentally committed configuration file), an attacker gains the full scope of that identity's privileged access with no second factor to stop them, directly connecting this AWS-layer finding to the A.8.5 (Secure authentication) control analyzed in Part 1 of the companion write-up.

**Proposed remediation direction:** Recommended enforcing MFA account-wide as an IAM policy condition for any privileged action, rather than a per-user, opt-in setting, given that a startup-scale team benefits more from one consistently enforced baseline than from individually configured exceptions that are easy to miss one of.

### 3.3 Risk: Unrestricted Network Exposure (EC2/Security Groups)

| Field | Detail |
|---|---|
| **Risk Classification** | High-severity network exposure risk |
| **Likelihood** | Medium-High to High |
| **Remediation SLA** | 7 days |
| **Owner** | Cloud Infrastructure Team |
| **Shared Responsibility Mapping** | Customer responsibility (Security IN the cloud) |
| **CIA Triad Property Affected** | Confidentiality, Integrity, Availability |

**Business impact analysis:** A security group rule permitting inbound access from an unrestricted source range on an administrative port (for example, SSH or RDP) exposes that instance to automated internet-wide scanning traffic that specifically and continuously probes for exactly this kind of misconfiguration -- this is not a theoretical risk contingent on a targeted attacker discovering NovaStream specifically, but an ambient, ongoing exposure to opportunistic, automated compromise attempts from the moment the rule is created.

**Proposed remediation direction:** Recommended restricting administrative access rules to specific, known source IP ranges (for example, a corporate VPN egress range) rather than an unrestricted range, and evaluated a Bastion host or Systems Manager Session Manager approach as a longer-term direction that removes the need for any directly internet-exposed administrative port at all.

### 3.4 Risk: Untested Disaster Recovery (RDS)

| Field | Detail |
|---|---|
| **Risk Classification** | Critical-severity resilience risk |
| **Likelihood** | High |
| **Remediation SLA** | 24-48 hours |
| **Owner** | Data / Platform Team |
| **Shared Responsibility Mapping** | Customer responsibility (Security IN the cloud) |
| **CIA Triad Property Affected** | Availability |

**Business impact analysis:** As established in the companion write-up, this finding describes the condition of NovaStream's RDS recovery capability being genuinely unverified rather than known to function -- a distinct and, from a risk-management standpoint, arguably more concerning state than a recovery process that has been tested and found to have a specific, addressable flaw (as demonstrated in the A.8.13 finding in Part 2), because an untested process could fail for any number of undiagnosed reasons, none of which have been identified or planned for.

**Proposed remediation direction:** Recommended scheduling a live RDS restoration exercise into an isolated test environment as a recurring practice, treating a successful past backup job as the start of the verification process rather than its conclusion, directly informed by the A.8.13 finding in Part 2 demonstrating one specific, concrete way an apparently healthy backup process can still fail to produce a usable restore.

---

## References

- ISO/IEC 27001:2022 Annex A, Theme 8 -- Technological Controls (A.8.1, A.8.4, A.8.5, A.8.8, A.8.12, A.8.13, A.8.17 referenced directly in this analysis)
- NIST SP 800-40 Rev. 4 -- Guide to Enterprise Patch Management Planning (referenced as an example of risk-based severity-to-response-urgency framework logic underlying the Likelihood and Remediation SLA fields)
- AWS Shared Responsibility Model
- GitHub Documentation -- About protected branches

---

*This analysis was developed as part of a self-directed cybersecurity portfolio project. NovaStream SaaS is an entirely fictional organization created for educational purposes; all findings, architecture details, and scenarios in this entry are simulated.*

---

*Return to: [Week 15 README](week15-readme.md)*
