# Week 15: ISO/IEC 27001 Annex A.8 Technological Controls (A.8.1-A.8.20) and AWS Cloud Risk Assessment -- NovaStream SaaS

> **Format:** Two-part Annex A.8 control mapping analysis (A.8.1-A.8.10, then A.8.11-A.8.20) followed by an AWS Shared Responsibility Model and cloud risk assessment, all applied to a single simulated organization
> **Method:** Technical domain mapping, four-tier evidence taxonomy construction, structured threat scenario modeling, and auditor testing methodology
> **Simulated Organization:** NovaStream SaaS -- a high-growth B2B software startup, used continuously across all three analyses to create a cohesive simulation storyline

---

## Executive Summary

This week extended the Annex A.8 (Technological Controls) analysis across 20 of the theme's 34 total controls (A.8.1-A.8.20), then closed the entry with an AWS Shared Responsibility Model and cloud risk assessment applied to the same simulated organization's actual cloud footprint -- NovaStream SaaS, a high-growth B2B software startup used consistently across all three analyses in this entry.

The first control set (A.8.1-A.8.10) covered endpoint security, identity and access, source code protection, and configuration management, and introduced a four-tier evidence taxonomy (Design, Technical, Operating, Effectiveness) extending the three-tier model used in prior physical-controls work, specifically to account for the machine-readable configuration state that technological controls -- unlike physical or organizational ones -- can produce as its own distinct category of evidence. Two specific findings were surfaced this way: GitHub repositories lacking branch protection rules, permitting unreviewed code directly onto the production branch (A.8.4), and Mobile Device Management policies that were deployed but did not strictly enforce Full-Disk Encryption on remote developer endpoints (A.8.1).

The second control set (A.8.11-A.8.20) covered data security, resilience, visibility, and system administration, and surfaced two further findings that reinforced the same core lesson from an entirely different technical angle: automated backup jobs that consistently reported success in the console, while a live restore simulation failed due to an encryption key rotation mismatch rendering the backups unreadable (A.8.13); and inconsistent NTP configuration between on-premise and cloud environments producing a five-minute clock drift that breaks the chronological timeline required for incident response forensics (A.8.17).

The AWS Cloud Risk Assessment closed the entry by mapping NovaStream's actual AWS service footprint (EC2, S3, RDS, Lambda) against the Shared Responsibility Model, surfacing four risk categories -- unintended public S3 exposure, over-privileged IAM access without MFA, unrestricted EC2 network exposure, and untested RDS disaster recovery -- and connecting each directly back to the Annex A.8 controls analyzed earlier in the same entry, demonstrating that the control set is not an abstract checklist but translates into concrete, auditable configuration states within a real cloud architecture.

> **Scope note:** This entry addresses Annex A.8 controls A.8.1-A.8.20 only -- 20 of the theme's 34 total Technological Controls, and 20 of ISO 27001:2022's 93 total Annex A controls overall. The remaining A.8.21-A.8.34 controls (Network, Application, and Cryptographic controls) are planned for a future entry and are explicitly out of scope here. All findings, the NovaStream SaaS organization, and its architecture are entirely simulated for self-directed training purposes; no finding in this entry reflects an actual completed remediation, live production system, or real organization.

---

## Key Competencies Demonstrated

- Control-by-control technical domain mapping across 20 Annex A.8 controls, spanning Endpoint, Identity and Access, DevSecOps, Infrastructure, Data Management, Resilience, Visibility, and System Administration domains
- Construction and application of a four-tier evidence taxonomy (Design, Technical, Operating, Effectiveness) purpose-built to capture the machine-readable configuration state distinctive to technological controls
- Root-cause threat scenario analysis connecting a specific technical failure mode (encryption key rotation) to a specific, high-severity business risk (permanent backup unreadability)
- Cross-domain pattern recognition, identifying the same underlying lesson (policy presence without technical enforcement) recurring across four structurally unrelated technical domains
- AWS Shared Responsibility Model analysis applied to a defined four-service architecture (EC2, S3, RDS, Lambda), with per-service responsibility boundary mapping
- Direct integration of an AWS-specific risk register with the Annex A.8 control set analyzed earlier in the same entry, rather than treating cloud risk as a separate framework
- Startup-appropriate Minimum Viable Implementation (MVI) and Quick Win prioritization, distinguishing low-cost, high-impact remediation actions suitable for a resource-constrained engineering team from a comprehensive, enterprise-scale control rollout
- Auditor testing methodology (Interview, Document Review, Live Sampling) tailored specifically to technological controls, including live restore testing and direct cross-environment timestamp comparison as sampling techniques beyond routine document review

---

## Repository Directory Structure

```
week-15/
|-- 01-README.md                                        (this file -- weekly dashboard)
|-- 02-write-up-a8-and-aws-cloud-risk.md                (Methodology and step-by-step reasoning, all three analyses)
|-- 03-business-impact-a8-and-aws-cloud-risk.md         (Risk classification and remediation direction, all findings)
|-- 04-resource-a8-and-aws-cloud-risk.md                (Reference library, key lessons, and study backlog)
```

---

## Key Metrics and Outcomes

| Metric | Result |
|---|---|
| Annex A.8 controls analyzed this entry | 20 / 34 (A.8.1-A.8.20) |
| Cumulative A.8 coverage across portfolio | 20 / 34 |
| Technical domain-mapped controls | 20 (across 8 technical domains) |
| Evidence taxonomy tiers applied | 4 (Design, Technical, Operating, Effectiveness) |
| A.8-level findings identified | 4 (A.8.4 branch protection, A.8.1 endpoint encryption, A.8.13 backup restore failure, A.8.17 clock drift) |
| AWS cloud risk findings identified | 4 (S3 public exposure, IAM missing MFA, EC2 network exposure, RDS untested DR) |
| AWS services mapped against Shared Responsibility Model | 4 (EC2, S3, RDS, Lambda) |
| Cross-referenced control connections between A.8 analysis and AWS assessment | 3 (A.8.5, A.8.8, A.8.12 directly mapped to specific AWS risk findings) |

---

## Links to Sub-Modules

### [Technical Write-Up: Annex A.8 (A.8.1-A.8.20) and AWS Cloud Risk Assessment](02-write-up-a8-and-aws-cloud-risk.md)
Full methodology and step-by-step reasoning across all three analyses. Covers the four-tier evidence taxonomy, technical domain mapping for all 20 controls, the branch protection and MDM encryption findings (A.8.4, A.8.1), the backup key rotation and NTP drift findings (A.8.13, A.8.17), the AWS Shared Responsibility Model applied to NovaStream's EC2/S3/RDS/Lambda footprint, and the four AWS cloud risk findings with their connection back to the Annex A.8 control set.

### [Business Impact and Risk Analysis](03-business-impact-a8-and-aws-cloud-risk.md)
Risk classification, severity, threat scenario framing, and proposed remediation direction for every finding identified across all three analyses, framed for business impact and startup-appropriate prioritization.

### [Resources and Reference Library](04-resource-a8-and-aws-cloud-risk.md)
Reference materials, framework citations, a consolidated summary of key lessons learned, and the study backlog identifying next steps (A.8.21-A.8.34 and related technical deep-dives).

---

## Key Takeaways

- **A four-tier evidence model (Design, Technical, Operating, Effectiveness) is necessary for technological controls specifically**, because a system's raw, machine-readable configuration state is a distinct category of evidence that physical and organizational controls do not produce in the same directly-verifiable way -- and the gap between Technical-tier configuration and Design-tier policy is where this week's most consequential findings were found.
- **The same core lesson -- policy presence does not equal technical enforcement -- recurred across four structurally unrelated domains**: source code management (A.8.4), endpoint encryption (A.8.1), backup key management (A.8.13), and time synchronization (A.8.17). A pattern recurring this consistently across unrelated technical areas is a stronger signal of a systemic gap than any single finding on its own.
- **A backup process reporting success and a backup process that has been proven to restore are two different claims**, and only a live restore test closes the gap between them -- a lesson demonstrated twice in this entry, once at the specific root-cause level (A.8.13's key rotation mismatch) and once at the broader risk-register level (the AWS assessment's untested RDS disaster recovery finding).
- **An AWS-specific cloud risk register is not a separate framework from Annex A.8 -- it is the same control set applied to a concrete architecture.** Directly mapping AWS risk findings back to A.8.5, A.8.8, and A.8.12 demonstrates that technological controls translate into specific, auditable cloud configuration states rather than remaining abstract.
- **Startup-appropriate remediation prioritizes cost-to-impact ratio, not comprehensive coverage.** Several of this week's proposed remediation directions (branch protection, NTP source alignment) were identified specifically because they are low-cost, configuration-level changes with outsized risk reduction -- the right sequencing for a resource-constrained engineering team, distinct from a mature enterprise's more comprehensive rollout timeline.

---

## References

- ISO/IEC 27001:2022 (Third Edition), Annex A, Theme 8 -- Technological Controls
- ISO/IEC 27002:2022 -- Implementation guidance for Annex A controls
- GitHub Documentation -- About protected branches
- AWS Shared Responsibility Model

---

*This portfolio entry was developed as part of a self-directed cybersecurity and GRC learning program. NovaStream SaaS is an entirely fictional organization created for educational purposes; all findings, architecture details, and scenarios in this entry are simulated.*
