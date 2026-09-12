# Technical Write-Up: ISO/IEC 27001 Annex A.8 Technological Controls (A.8.1-A.8.20) and AWS Cloud Risk Assessment -- NovaStream SaaS

> **Scope:** ISO/IEC 27001:2022 Annex A.8 Technological Controls A.8.1-A.8.20 (20 of 34 total A.8 controls), plus an AWS Shared Responsibility Model and cloud risk assessment
> **Simulated Organization:** NovaStream SaaS -- a high-growth B2B software startup, used consistently as the case study subject across all three analyses in this entry
> **Method:** Control-by-control technical domain mapping, evidence taxonomy construction, structured threat scenario modeling, and auditor testing methodology
> **Companion Files:** [Business Impact and Risk Analysis](business-impact-a8-and-aws-cloud-risk.md) -- [Resources and Reference Library](resource-a8-and-aws-cloud-risk.md)

---

# Part 1 -- Annex A.8 Technological Controls (A.8.1-A.8.10): Technical Security and GRC Mapping Analysis

## Scope Disclaimer

This analysis covers Annex A.8 controls A.8.1 through A.8.10 only -- 10 of ISO 27001:2022's 34 total Technological Controls, and 10 of 93 total Annex A controls overall. It does not represent a complete Annex A.8 review. The remaining A.8.11-A.8.34 controls are addressed in Part 2 of this write-up (A.8.11-A.8.20) and in a planned future entry (A.8.21-A.8.34, covering Network, Application, and Cryptographic controls). A.5 (Organizational), A.6 (People), and A.7 (Physical) controls are addressed in separate prior portfolio entries.

## 1.1 Methodology

The analysis followed a structured domain-mapping approach: each of the 10 controls was assigned to a technical architecture domain (Endpoint, Identity and Access, DevSecOps, Infrastructure, Data Management), then evaluated against a purpose-built evidence taxonomy distinguishing four evidence tiers rather than the three-tier model (Design, Operating, Effectiveness) used in prior physical-controls analysis. The fourth tier -- Technical -- was added specifically for A.8, because technological controls, unlike physical or organizational ones, can produce a distinct category of evidence that a policy or observation cannot: a raw, machine-generated configuration state.

### 1.1.1 -- The Four-Tier Evidence Taxonomy

| Evidence Tier | Question It Answers | Example for A.8.4 (Access to source code) |
|---|---|---|
| **Design** | Does a documented control or standard exist? | A documented Secure Development Policy requiring code review before merge to production branches |
| **Technical** | What does the raw system configuration actually show, independent of any process around it? | The GitHub repository's branch protection ruleset configuration (JSON export), which either does or does not have `required_pull_request_reviews` enabled on the default branch |
| **Operating** | Is the control being followed in day-to-day practice? | A sample of the last 20 merge events to the production branch, checked for an associated approved pull request |
| **Effectiveness** | Does the control demonstrably prevent the outcome it exists to prevent, over time? | Zero incidents of unreviewed code reaching production over a defined review period, cross-referenced against the technical configuration remaining continuously enabled (not toggled off and back on around a specific merge) |

**Why Technical is distinct from Operating, and why A.8 specifically needs this distinction:** For a physical control (a locked door) or an organizational control (a signed policy), "is the control configured correctly" and "is the control being followed" are close to the same question -- a door is either locked or it isn't, and that state is directly observable. For a technological control, this is not true: an IAM policy document can exist, be technically well-formed, and be completely disconnected from what actually happens at runtime if, for example, a separate emergency-access mechanism bypasses it. The Technical tier isolates the raw configuration state as its own piece of evidence, deliberately kept separate from Operating evidence (samples of what actually happened), because a control can score well on one tier and poorly on the other -- and the gap between them is frequently where the most consequential findings live, as demonstrated directly in the branch protection finding below.

## 1.2 Technical Domain Mapping

| Control | Title | Technical Domain | Representative Technology |
|---|---|---|---|
| A.8.1 | User endpoint devices | Endpoint | MDM (Mobile Device Management), EDR (Endpoint Detection and Response) |
| A.8.2 | Privileged access rights | Identity and Access Management | Identity Provider (IdP), Privileged Access Management (PAM) tooling |
| A.8.3 | Information access restriction | Identity and Access Management | Role-based access control within IdP and application-layer permissions |
| A.8.4 | Access to source code | DevSecOps | GitHub Branch Protection, repository access controls |
| A.8.5 | Secure authentication | Identity and Access Management | Multi-Factor Authentication (MFA) enforcement policy |
| A.8.6 | Capacity management | Infrastructure | AWS CloudWatch metrics, auto-scaling configuration |
| A.8.7 | Protection against malware | Endpoint | EDR/antivirus tooling, email and web gateway filtering |
| A.8.8 | Management of technical vulnerabilities | Infrastructure | Vulnerability scanning tooling, patch management cadence |
| A.8.9 | Configuration management | Infrastructure | Infrastructure as Code (IaC, e.g., Terraform), AWS Config |
| A.8.10 | Information deletion | Data Management | Data retention and deletion tooling, database-level purge jobs |

## 1.3 Specific Finding One: A.8.4 (Access to Source Code) -- Missing Branch Protection

**The simulated finding:** NovaStream SaaS's GitHub repositories were found to lack branch protection rules on the default production branch, allowing developers to push unreviewed and unapproved code directly to main.

**Why this is a Technical-tier finding, and why it would not be visible from Design evidence alone:** NovaStream had a documented Secure Development Policy stating that all production code changes require peer review -- Design evidence, on its own, looks satisfactory. The gap surfaces entirely at the Technical tier: the repository's actual branch protection configuration had no `required_pull_request_reviews` rule enabled on the default branch, meaning nothing in the platform itself enforced the policy's requirement. Any developer with write access could commit directly to main, bypassing the review process the policy describes, with no technical mechanism stopping them.

**Why GitHub's branch protection mechanism is the correct technical control for this gap:** GitHub branch protection rules can require that all changes to a designated branch be submitted via a pull request and approved by a specified number of reviewers before merging, and can further require that this applies even to repository administrators. Without this configuration active, a policy requiring code review exists only as a social expectation the platform does nothing to enforce -- any developer under time pressure, or any developer simply unaware of the policy, has an unobstructed technical path to bypass it entirely.

**The core lesson this finding produces:** policy existence and technical enforcement are two independent variables, and a documented requirement with no corresponding platform-level control is not evidence that the requirement is being met -- it is only evidence that the requirement was written down. This finding, and the parallel one below, are the basis for this week's central lesson, developed further in Section 1.5.

## 1.4 Specific Finding Two: A.8.1 (User Endpoint Devices) -- Incomplete MDM Encryption Enforcement

**The simulated finding:** NovaStream SaaS had deployed Mobile Device Management (MDM) policies across its remote developer fleet, but these policies failed to strictly enforce Full-Disk Encryption (FDE, via BitLocker on Windows or FileVault on macOS) on all enrolled endpoints, exposing data in the event of device loss or theft.

**Why "MDM is deployed" is Design/Technical-tier evidence, not Effectiveness-tier evidence:** The presence of an MDM platform managing a fleet of devices confirms that a technical control *exists* and is *operating* at some level -- devices are enrolled, checking in, and receiving some configuration. It does not, on its own, confirm that the specific configuration profile requiring FDE is both correctly defined at the Technical tier and consistently *enforced* rather than merely *recommended* or *available as an option* the end user could decline or the profile could silently fail to apply to.

**Why this specific gap is high-consequence for a remote-first B2B SaaS startup:** A high-growth B2B startup with a distributed, remote workforce has a materially larger population of devices operating outside any physical office perimeter, at any given time, than a traditional on-premises organization -- meaning device loss or theft (in transit, at a co-working space, in a personal vehicle) is a routine and expected risk category rather than an edge case. Without FDE strictly enforced, a lost or stolen laptop is not merely a hardware replacement cost; the device's local storage, potentially containing cached credentials, source code, or customer data synced for offline access, is directly readable by anyone with physical possession of the drive, since the device's own login screen provides no protection against the disk being removed and read on separate hardware.

**Why this parallels the A.8.4 finding structurally:** both findings share the same underlying shape -- a control that exists at the Design and partial-Technical tier (a policy exists, a platform is deployed) but fails at full Technical-tier verification (the specific enforcement setting is not actually locked in) and therefore cannot be relied upon at the Effectiveness tier. This structural parallel across two unrelated technical domains (source code management and endpoint management) is what elevates it from a single finding to the section-wide lesson below.

## 1.5 Startup/SME Case Study: Minimum Viable Implementation (MVI) for NovaStream SaaS

A recurring consideration in analyzing a high-growth startup environment like NovaStream is that a security control roadmap appropriate for a mature enterprise with a dedicated security team is frequently impractical for a startup with a small, engineering-heavy headcount and no dedicated security function. The MVI approach defines the smallest set of technical controls that closes the highest-consequence gaps first, rather than pursuing comprehensive coverage across all 10 controls simultaneously.

**MVI priorities identified for the two specific findings above:**

- For A.8.4: enabling branch protection with a required pull request review is a configuration change achievable in minutes, at no additional tooling cost, and closes the entire finding immediately -- making it a first-priority MVI action specifically because the cost-to-impact ratio is exceptionally favorable for a resource-constrained team.
- For A.8.1: rather than pursuing a fully custom MDM policy framework, the MVI approach is to audit the existing MDM platform's built-in compliance reporting (most major MDM platforms can report per-device FDE status directly) and address only the specific non-compliant devices identified, rather than re-architecting the entire endpoint management approach.

## 1.6 Auditor Testing Approach (A.8.1-A.8.10)

| Testing Approach | Example Applied to NovaStream |
|---|---|
| **Interview** | Ask a developer directly how they would push an urgent hotfix -- this is the specific interview question that would surface a direct-to-main push habit if branch protection is not enforced |
| **Document Review** | Review the Secure Development Policy text and the MDM platform's configuration profile export |
| **Live Sampling** | Sample the last 20 commits to the production branch and check each for an associated, approved pull request; separately sample a subset of enrolled endpoints and check each device's actual FDE status against the MDM console's reported compliance status |

## 1.7 Section Takeaways: A.8.1-A.8.10

- **Technological controls introduce a fourth evidence tier -- Technical -- that physical and organizational controls do not require in the same way**, because a system's raw configuration state can be captured and checked directly, independent of any policy or observed behavior around it, and that state can diverge from both.
- **Confirmed that technical policy existence does not equal operational effectiveness.** Both flagged findings (A.8.4, A.8.1) involved a documented policy and a deployed platform that nonetheless failed to enforce the specific outcome the policy described, at the Technical-tier configuration level.
- **Automated technical enforcement is what closes the gap between policy and outcome.** A policy that depends on individual developer discipline (do not push directly to main; do enable full-disk encryption) is only as reliable as the least-disciplined or most rushed person with access -- a platform-level technical control removes that dependency entirely.

---
---

# Part 2 -- Annex A.8 Technological Controls (A.8.11-A.8.20): Technical Security and GRC Mapping Analysis

## Scope Disclaimer

This analysis covers Annex A.8 controls A.8.11 through A.8.20 only -- 10 further of ISO 27001:2022's 34 total Technological Controls, bringing the cumulative A.8 coverage in this portfolio to 20 of 34 controls. Remaining A.8.21-A.8.34 controls (Network, Application, and Cryptographic controls) are planned for a future entry.

## 2.1 Methodology

The same four-tier evidence taxonomy (Design, Technical, Operating, Effectiveness) established in Part 1 was applied to this second control set, extended across a different set of technical domains: Data Security, Resilience, Visibility, System Administration, and Network-adjacent Infrastructure.

## 2.2 Technical Domain Mapping

| Control | Title | Technical Domain | Representative Technology |
|---|---|---|---|
| A.8.11 | Data masking | Data Security | Data masking/tokenization tooling for staging and development environments |
| A.8.12 | Data leakage prevention | Data Security | DLP tooling, egress monitoring |
| A.8.13 | Information backup | Resilience | AWS Backup, database-native backup jobs, encryption key management |
| A.8.14 | Redundancy of information processing facilities | Resilience | Multi-AZ deployment, failover infrastructure |
| A.8.15 | Logging | Visibility | Centralized log aggregation (e.g., CloudWatch Logs, SIEM ingestion) |
| A.8.16 | Monitoring activities | Visibility | SIEM/SOC alerting and anomaly detection |
| A.8.17 | Clock synchronization | Visibility | NTP (Network Time Protocol) configuration across on-premise and cloud systems |
| A.8.18 | Use of privileged utility programs | System Administration | Restricted administrative tooling and utility access controls |
| A.8.19 | Installation of software on operational systems | System Administration | Change-controlled software deployment pipelines |
| A.8.20 | Networks security | Infrastructure | Network segmentation, firewall and security group configuration |

## 2.3 Specific Finding One: A.8.13 (Information Backup) -- Restore Failure Despite Successful Backup Logs

**The simulated finding:** NovaStream SaaS's automated backup jobs consistently reported as "Successful" in the backup console, but a live restore simulation failed: the restored backup files could not be decrypted, due to a mismatch between the encryption key used to originally encrypt the backup and the encryption key currently active in the key management system, following an encryption key rotation event.

**Why the backup job's own "Successful" status is Technical/Operating-tier evidence, and why it is insufficient on its own:** A backup job reporting success confirms that the job executed, wrote output, and did not throw an execution error -- this is genuine, valid Technical-tier evidence that the backup *process* ran. It says nothing about whether that output is actually *usable*, which is a separate property this evidence tier cannot capture on its own. Encryption at rest for a backup is applied using a specific key active at the time of the backup job; if that key is later rotated (a routine, recommended key management practice) and the *previous* key is not retained in a form the restore process can still access, backups encrypted under the retired key become cryptographically unreadable -- not corrupted, not missing, simply permanently inaccessible without the specific key that encrypted them, since encryption is designed precisely to make data unreadable without the correct key, with no legitimate technical shortcut around that guarantee.

**Why this specific failure mode is easy to miss without a live restore test:** every signal an operations team would normally monitor -- job completion status, backup file size, backup job duration, absence of error alerts -- reports as entirely normal in this scenario. The backup genuinely completed successfully at the time it ran, under the key that was active at that time. The failure is latent and only manifests at the moment of restore, which for most organizations (including, in this simulation, NovaStream) is a rare event compared to the routine cadence of the backup job itself -- meaning a real incident requiring restoration is often the very first time this specific gap would be discovered, at the worst possible moment to discover it.

**Why key rotation is the specific root cause, not backup tooling malfunction:** the backup files themselves are structurally intact; the failure is entirely a key-availability problem, not a data-integrity problem. This distinction is directly relevant to the remediation direction in the companion Business Impact file, because it points toward key lifecycle management (retaining prior keys for exactly as long as backups encrypted under them remain within the retention window) as the corrective direction, rather than toward re-architecting the backup process itself.

## 2.4 Specific Finding Two: A.8.17 (Clock Synchronization) -- NTP Drift Breaking Forensic Timelines

**The simulated finding:** Inconsistent NTP (Network Time Protocol) server configurations across NovaStream's on-premise and cloud environments produced a five-minute time drift between the two environments' system clocks, which in turn caused SIEM-ingested logs from both environments to carry inconsistent timestamps -- breaking the chronological timeline required for incident response forensics.

**Why clock synchronization, a control that looks purely operational, is a direct enabler of every other logging and monitoring control:** A.8.15 (Logging) and A.8.16 (Monitoring activities) both depend entirely on an implicit assumption: that a timestamp recorded by one system can be meaningfully compared to a timestamp recorded by another system, in order to reconstruct the sequence of events during an incident. A.8.17 is the control that makes that assumption actually true. Without synchronized clocks, two log entries that occurred at genuinely the same real-world moment can appear five minutes apart, and two events that occurred five minutes apart in reality can appear to have happened simultaneously -- in either direction, the sequencing an investigator relies on to answer "what happened first, and what did it cause" becomes unreliable exactly when that sequencing matters most.

**Why a five-minute drift is materially significant rather than a rounding error:** many attack chains -- initial access, privilege escalation, lateral movement, data exfiltration -- can unfold within a window considerably shorter than five minutes. A drift of this size is large enough to plausibly reorder the apparent sequence of steps in a fast-moving incident, which can lead an investigator to draw an incorrect conclusion about causation (for example, misattributing which system was compromised first) based on log timestamps that appear authoritative but are not actually comparable across the two environments.

**Why this finding is a Technical-tier gap specifically, not a Design gap:** it is very likely that NovaStream had some form of documented expectation that logs would be time-accurate (Design evidence, if it existed, would look unremarkable). The failure is entirely in the underlying Technical-tier configuration: on-premise systems and cloud systems each pointed at different, unsynchronized time sources, with no shared reference clock ensuring the two environments' clocks tracked together -- a gap invisible to anyone reviewing a logging policy document, and only discoverable by directly comparing NTP configuration across environments or by noticing a timestamp inconsistency during an actual investigation.

## 2.5 Startup/SME Case Study: Minimum Viable Implementation and Quick Wins for NovaStream SaaS

- For A.8.13: the MVI-appropriate action is not building custom backup infrastructure, but establishing a key retention policy tied explicitly to the backup retention period (any encryption key used for a backup must remain available for at least as long as that backup is retained) and scheduling a periodic live restore test as a standing verification step, since the finding demonstrates that backup success monitoring alone cannot catch this failure mode.
- For A.8.17: the Quick Win here is close to the lowest-cost technical remediation across the entire A.8.1-A.8.20 set analyzed this week -- pointing all on-premise and cloud systems at the same authoritative NTP source (or a small number of synchronized sources) is a configuration-level change with no new tooling cost, making it disproportionately high-impact relative to the effort required to apply it for a startup with limited security engineering capacity.

## 2.6 Auditor Testing Approach (A.8.11-A.8.20)

| Testing Approach | Example Applied to NovaStream |
|---|---|
| **Interview** | Ask the infrastructure lead directly when the backup encryption key was last rotated, and whether a live restore has ever been performed following that rotation -- this is the specific question that surfaces the A.8.13 gap before an actual incident does |
| **Document Review** | Review the backup job configuration, the key management system's key rotation history, and the NTP configuration files or equivalent settings across both on-premise and cloud environments |
| **Live Sampling** | Perform an actual restore simulation of a sampled recent backup (not merely reviewing the job's reported status); separately sample timestamped log entries from both environments for the same real-world event and directly compare their recorded times |

## 2.7 Section Takeaways: A.8.11-A.8.20

- **Reaffirmed that backup logs do not guarantee restore capability.** A "Successful" status is Technical-tier evidence that a process executed; it is not Effectiveness-tier evidence that the output is usable, and only an actual restore test can close that gap.
- **Policy presence does not equate to technical enforcement**, reinforcing the same core lesson from Part 1 across an entirely different technical domain (backup and time infrastructure rather than source code and endpoints) -- the recurrence of this pattern across unrelated domains is itself the most important finding of this week's combined analysis.
- **Network and data security controls require automated evidence validation rather than status-monitoring alone.** Both findings in this section were invisible to routine operational monitoring (backup job status, standard log review) and were only surfaced by directly testing the underlying mechanism (an actual restore, a direct timestamp comparison across environments).

---
---

# Part 3 -- AWS Shared Responsibility Model and Cloud Risk Assessment: NovaStream SaaS Cloud Infrastructure Audit

## 3.1 Methodology and Continuity with Parts 1 and 2

This entry represents the cloud infrastructure audit of NovaStream SaaS -- the same simulated organization analyzed in Parts 1 and 2 -- extending the technological controls analysis specifically into the AWS environment NovaStream's production infrastructure runs on. Where Parts 1 and 2 examined technical controls in domain-general terms (endpoint, source code, backup, logging), this entry maps those same underlying risk categories onto NovaStream's actual AWS service footprint: Amazon EC2, Amazon S3, Amazon RDS, and AWS Lambda.

## 3.2 Shared Responsibility Analysis

AWS's Shared Responsibility Model divides accountability between AWS's responsibility for **security "OF" the cloud** and the customer's responsibility for **security "IN" the cloud**.

| Responsibility | Owner | Applied to NovaStream's Architecture |
|---|---|---|
| Physical security of data centers, hardware maintenance, network infrastructure | AWS | Applies uniformly across EC2, S3, RDS, and Lambda -- outside NovaStream's control or audit scope |
| Host virtualization (Hypervisor) and core infrastructure availability | AWS | Applies uniformly across all four services |
| Customer data protection | NovaStream | What is stored in S3 and RDS, and how it is classified and encrypted |
| Identity and Access Management (IAM) | NovaStream | Every credential, role, and permission granted across all four services |
| Network firewall configurations (Security Groups/NACLs) | NovaStream | Specifically relevant to EC2 network exposure |
| Operating system patching (IaaS) | NovaStream | Specifically relevant to EC2, since Lambda and the managed portions of RDS abstract the OS layer away from the customer |
| Application code security | NovaStream | Relevant to any custom application logic running on EC2 or within Lambda functions |
| Encryption settings | NovaStream | Relevant to S3 bucket encryption configuration and RDS encryption-at-rest settings |

**The pattern this reveals across NovaStream's specific service mix:** EC2 sits furthest toward the IaaS end of the model, giving NovaStream the largest slice of "security IN the cloud" responsibility (including OS-level patching) of any of the four services in scope; Lambda sits furthest toward the serverless end, where AWS manages the execution environment entirely and NovaStream's responsibility narrows to function code and its assigned permissions. This range across a single organization's service footprint is precisely why a shared responsibility assessment cannot be a single blanket statement -- the responsibility boundary shifts service by service, and each of NovaStream's four services needs its own specific mapping.

## 3.3 Customer Cloud Security Risks and Evidence Mapping

| # | Risk | Affected Service | Risk Description | Evidence |
|---|---|---|---|---|
| 1 | Unintended Public Storage | S3 | Data leakage risk from a bucket policy or account setting permitting public read access to stored objects | S3 Bucket Policy JSON, AWS Config Rules (specifically rules evaluating public access block status) |
| 2 | Over-privileged Access and Missing MFA | IAM | Credential theft risk amplified by broad permission grants and the absence of a second authentication factor on privileged accounts | IAM Credential Report, CloudTrail Logs |
| 3 | Unrestricted Network Exposure | EC2 / Security Groups | Unauthorized remote access risk from security group rules permitting inbound access from an unrestricted source range | Security Group configuration export |
| 4 | Untested Disaster Recovery | RDS | Permanent data loss risk from a backup and recovery configuration that has never been validated through an actual restoration exercise | Backup configuration log, Restoration Test reports |

**Why Risk 4 (Untested Disaster Recovery on RDS) is a distinct finding from the A.8.13 backup finding in Part 2, not a duplicate of it:** the Part 2 finding (encryption key rotation breaking backup readability) is a specific, root-caused failure mode discovered through an actual restore attempt -- the restore was performed, and it failed for an identified reason. This AWS-layer finding is broader and precedes that level of diagnosis: it describes the condition of *never having attempted a restore at all*, meaning NovaStream's actual recovery capability for the RDS-hosted transactional data is genuinely unknown rather than known-and-broken. The two findings are complementary rather than duplicative: this entry identifies the absence of a Disaster Recovery test as a standalone gap in its own right, while Part 2 shows one specific, concrete way such an untested recovery process can fail once a live test is finally attempted -- reinforcing, from an independent angle, exactly why testing a recovery process before it is needed matters.

## 3.4 SaaS Startup Case Study Simulation: NovaStream Cloud Risk Assessment

Applying the risk register above directly to NovaStream's simulated AWS environment surfaced three critical misconfigurations as the highest-priority items for a startup-appropriate response: a publicly-accessible S3 bucket, an EC2 instance running an unpatched operating system, and IAM users with privileged access but no MFA enforced. Each was mapped to the specific ISO/IEC 27001 controls it corresponds to for documentation and audit-trail purposes: the S3 exposure maps to A.5.23 (cloud services) and the data-handling intent behind A.8.12 (data leakage prevention); the missing MFA maps directly to A.8.5 (secure authentication) from Part 1 of this write-up; and the unpatched EC2 instance maps to A.8.8 (management of technical vulnerabilities), also from Part 1 -- demonstrating that the AWS-specific risk register in this entry is not a separate framework from the Annex A.8 controls analyzed in Parts 1 and 2, but a direct, service-specific application of the same underlying control set to NovaStream's actual cloud footprint.

## 3.5 Limitations and Lessons Learned

**AWS Assurance Reports validate AWS infrastructure only; they do not prove customer-side compliance.** A report demonstrating that AWS's own data centers, hypervisor, and physical security meet a given standard says nothing about whether NovaStream's own S3 bucket policies, IAM configurations, or EC2 patch levels are correctly configured -- these sit entirely on the customer side of the responsibility line established in Section 3.2, and no assurance report from AWS can substitute for NovaStream directly auditing its own configuration.

**Audit evidence must prove both Control Design and Operating Effectiveness over time.** A single point-in-time configuration snapshot showing an S3 bucket is currently not public, or an IAM user currently has MFA enabled, demonstrates the control was correctly configured at the moment of the snapshot -- it does not demonstrate the control has remained correctly configured across the full period an auditor needs assurance over, since cloud configurations can change at any time through a console action, an API call, or an infrastructure-as-code deployment, with no inherent guarantee that a correct state persists.

## 3.6 Section Takeaways: AWS Shared Responsibility and Cloud Risk Assessment

- **The shared responsibility boundary is service-specific, not organization-wide.** NovaStream's own responsibility differs materially between its most IaaS-like service (EC2, including OS patching) and its most serverless service (Lambda, execution-environment-abstracted) -- a single blanket assessment of "our AWS security posture" obscures this necessary granularity.
- **An untested recovery capability and a recovery capability that has been tested and found broken are different risk states, both worth documenting.** The RDS disaster recovery finding in this entry and the encryption-key-driven restore failure in Part 2 are complementary evidence of the same underlying principle from two independent angles: a backup that has not been proven to restore should be treated as unproven, not as functional by default.
- **This entry closes the loop between the domain-general A.8 analysis (Parts 1 and 2) and a concrete cloud environment**, directly mapping the same controls (A.8.5, A.8.8, A.8.12) onto NovaStream's actual AWS service footprint, demonstrating that Annex A.8 controls are not an abstract checklist but a framework that translates into specific, auditable configuration states within a real cloud architecture.

---

## References

- ISO/IEC 27001:2022 (Third Edition), Annex A, Theme 8 -- Technological Controls (A.8.1-A.8.20 of 34 total)
- ISO/IEC 27002:2022 -- Implementation guidance for Annex A controls
- GitHub Documentation -- About protected branches
- AWS Shared Responsibility Model

---

*Return to: [Week 15 README](week15-readme.md)*
