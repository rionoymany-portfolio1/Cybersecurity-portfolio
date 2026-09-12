# Resources: ISO/IEC 27001 Annex A.8 (A.8.1-A.8.20) and AWS Cloud Risk Assessment

> **Scope:** Reference materials, frameworks, key lessons, and study backlog for the Annex A.8 Technological Controls analysis and the AWS Cloud Risk Assessment, both mapped to the simulated organization NovaStream SaaS
> **Companion Files:** [Technical Write-Up](02-write-up-a8-and-aws-cloud-risk.md) -- [Business Impact and Risk Analysis](03-business-impact-a8-and-aws-cloud-risk.md)

---

## ISO/IEC 27001:2022 Standard and Supporting Documents

| Resource | Detail |
|---|---|
| ISO/IEC 27001:2022 (official) | Third edition -- Annex A, Theme 8 (Technological Controls), covering A.8.1-A.8.20 of the 34 total controls analyzed this week |
| ISO/IEC 27002:2022 | Implementation guidance for Annex A controls, including detailed guidance text for each of the 20 A.8 controls analyzed |

**Key A.8 structural facts (verified):**
- Annex A.8 (Technological Controls) contains 34 controls total, numbered A.8.1 through A.8.34. This entry covers A.8.1-A.8.20 (20 of 34).
- A.8.9 (Configuration management), A.8.10 (Information deletion), A.8.11 (Data masking), A.8.12 (Data leakage prevention), and A.8.16 (Monitoring activities) are among the 11 entirely new controls introduced in the 2022 revision, with no direct equivalent in the 2013 edition.
- A.8.4 (Access to source code) corresponds to a merged and expanded scope from the 2013 edition's more narrowly framed access control provisions.

---

## GitHub and DevSecOps References

| Resource | Relevance |
|---|---|
| GitHub Documentation -- About protected branches | Primary source for the branch protection mechanism referenced in the A.8.4 source code protection finding |
| GitHub Documentation -- Managing a branch protection rule | Configuration reference for required pull request reviews and administrator enforcement |

---

## Backup, Encryption, and Key Management References

| Resource | Relevance |
|---|---|
| Vendor documentation on encrypted backup key lifecycle (general key management principle) | Basis for the A.8.13 finding -- confirms that a backup encrypted under a since-rotated key cannot be restored without retaining the original key, independent of vendor or platform |
| AWS Backup and AWS Key Management Service (KMS) documentation | Reference for key rotation and retention practices applicable to the proposed remediation direction |

---

## Network Time and Forensics References

| Resource | Relevance |
|---|---|
| NTP (Network Time Protocol) standard references | Basis for the A.8.17 clock synchronization finding and the proposed remediation of unifying on-premise and cloud time sources |

---

## AWS Cloud Security and Shared Responsibility Model

| Resource | Relevance |
|---|---|
| AWS Shared Responsibility Model (official AWS documentation) | Primary source for the Security OF the Cloud vs. Security IN the Cloud distinction applied to NovaStream's EC2, S3, RDS, and Lambda footprint |
| AWS Config documentation | Reference for continuous configuration evaluation, proposed as the remediation direction for the S3 public exposure and account-wide monitoring findings |
| AWS Identity and Access Management (IAM) documentation | Reference for MFA enforcement and privileged access management remediation directions |

---

## Related Portfolio Entries

| Entry | Connection |
|---|---|
| Week 14 -- ISO/IEC 27001 Annex A.7 Physical Controls and AWS Cloud Security (FinTrust Startup) | Established the four-way Design/Operating/Effectiveness evidence model later extended to a four-tier model (adding Technical) in this entry to account for machine-readable configuration evidence specific to technological controls |
| Week 13 -- ISO/IEC 27001 Annex A.5 Deep-Dive and IPv4 Subnetting | Established the pattern of pairing a governance framework analysis with a hands-on technical exercise, continued in this entry's pairing of Annex A.8 control analysis with the AWS cloud risk assessment |

---

## Key Lessons Learned (Summary)

- Technical policy existence does not equal operational effectiveness; automated technical enforcement (branch protection, MDM compliance reporting) is what closes the gap between a documented requirement and an actually-enforced outcome.
- Backup logs reporting success do not guarantee restore capability; only a live restore test can verify that a backup is actually usable, particularly across an encryption key rotation event.
- Policy presence does not equate to technical enforcement, a pattern that recurred across unrelated technical domains (source code management, endpoint encryption, backup key management, clock synchronization) rather than being isolated to a single control area.
- AWS Assurance Reports validate AWS's own infrastructure only; they provide no evidence about customer-side configuration, which requires independent, direct evaluation.
- Audit evidence for a technological control must demonstrate both Design and Operating Effectiveness sustained over time, not a single point-in-time configuration snapshot.

---

## Study Backlog and Next Steps

- Extend Annex A.8 coverage to the remaining controls, A.8.21-A.8.34, focusing on Network Security (A.8.21-A.8.23), Cryptography (A.8.24), and the Secure Development Life Cycle controls (A.8.25-A.8.34).
- Deepen technical familiarity with AWS Key Management Service (KMS) key rotation mechanics specifically, following directly from the A.8.13 finding in this entry, to better analyze key retention policy design in future work.
- Explore SIEM-level time synchronization validation techniques as a follow-on from the A.8.17 finding, to analyze how a SIEM platform itself can detect and flag clock drift between ingested log sources rather than relying on manual comparison.

---

## References

- ISO/IEC 27001:2022 (Third Edition), Annex A, Theme 8 -- Technological Controls
- ISO/IEC 27002:2022 -- Implementation guidance for Annex A controls
- GitHub Documentation
- AWS Shared Responsibility Model

---

*Return to: [README](01-README.md)*
