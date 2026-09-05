# Week 14: ISO/IEC 27001 Annex A.7 Physical Controls Audit Simulation and AWS Cloud Security Assessment

> **Format:** Control-by-control audit simulation (ISO 27001 Annex A.7) plus a scenario-driven cloud security assessment (AWS Shared Responsibility Model) against a simulated FinTech startup
> **Method:** Evidence mapping across Design, Operating, and Effectiveness categories; evidence quality analysis; structured risk spotting; auditor testing methodology
> **Approach:** Physical controls audit walkthrough, followed by a cloud architecture risk assessment applying the same evidence-based reasoning to a cloud-native context

---

## Executive Summary

This week combined two audit-simulation exercises applying the same evidence-based reasoning discipline to two different security domains: the physical world (ISO/IEC 27001 Annex A.7) and the cloud (AWS Shared Responsibility Model).

**Project 1** simulated a full control-by-control audit of all 14 Annex A.7 Physical Controls, concentrating on CCTV, access badges, and visitor logs as the primary evidence artifacts. The exercise surfaced two specific findings through evidence quality analysis rather than a surface-level policy check: a CCTV retention configuration set to 30 days against a documented 90-day policy requirement, and a pair of physical access workflow gaps (tailgating into a secure server room, and visitor badges that were not consistently returned or automatically revoked). A separate compliance analysis identified two distinct GDPR violations embedded in a simple, easily overlooked artifact -- a shared paper visitor logbook -- covering both a confidentiality exposure and a data minimization and storage limitation gap from recording full National ID numbers with no retention policy.

**Project 2** applied the AWS Shared Responsibility Model to a simulated FinTech organization, "FinTrust Startup," analyzing its EC2, VPC, S3, RDS, Lambda, and WorkSpaces architecture. The assessment classified each service against the IaaS/PaaS/SaaS model, then conducted risk spotting that surfaced two high-severity findings: potential public exposure of KYC identity documents stored in S3, and a developer practice of sharing the RDS PostgreSQL Master User password, which eliminates individual accountability for database actions. Both findings were developed into evidence matrices, mapped to the four standard auditor testing approaches (Interview, Document Review, Observation, Sampling), and paired with remediation directions designed specifically for a startup-scale engineering team rather than a large-enterprise security program.

> **Scope note:** This entry addresses Annex A.7 (Physical Controls) only -- 14 of ISO 27001:2022's 93 total Annex A controls -- and a scenario-specific subset of AWS services (EC2, VPC, S3, RDS, Lambda, WorkSpaces) rather than the full AWS service catalog. It does not represent a complete ISMS review or a comprehensive cloud security audit. Both projects are self-directed training simulations; no finding in this entry reflects an actual completed remediation, live production system, or real organization.

---

## Key Competencies Demonstrated

- Control-by-control evidence mapping across Design, Operating, and Effectiveness evidence categories for a full Annex A theme (14 controls)
- Evidence quality analysis using the Authenticity, Timeliness, Completeness, and Traceability framework, applied to identify a real evidentiary gap (CCTV retention) rather than only confirming a policy exists
- GDPR compliance analysis applied to a physical (non-digital) artifact, identifying two distinct violated principles (Data Minimization, Storage Limitation) plus a separate Confidentiality exposure
- AWS cloud service model classification (IaaS/PaaS/SaaS) and Shared Responsibility Model analysis applied to a defined six-service architecture
- Risk spotting for cloud misconfiguration (S3 public exposure) and access governance failure (shared database credentials), each mapped to a specific, individually-accountable remediation direction
- Auditor testing methodology (Interview, Document Review, Observation, Sampling) applied and differentiated by service, with reasoning for why cloud evidence-gathering leans more heavily on Document Review than physical control testing does
- Startup-appropriate remediation design (account-wide MFA, Just-In-Time access, centralized secrets management) as a deliberately different design target from an equivalent large-enterprise security program, not a scaled-down version of one

---

## Repository Directory Structure

```
week-14/
|-- week14-readme.md                                     (this file -- weekly dashboard)
|-- write-up-a7-and-aws-cloud-security.md                 (Methodology and step-by-step reasoning, both projects)
|-- business-impact-a7-and-aws-cloud-security.md           (Risk classification and remediation direction, both projects)
|-- evidence-matrix-a7-and-aws-cloud-security.md            (14-control and 6-service evidence tables, auditor testing approach)
`-- resource-a7-and-aws-cloud-security.md                  (Reference library and frameworks)
```

---

## Key Metrics and Outcomes

| Metric | Result |
|---|---|
| Annex A.7 controls reviewed | 14 / 14 (100% of theme) |
| Physical control findings identified | 3 (CCTV retention gap, tailgating gap, visitor badge revocation gap) |
| GDPR principle violations identified | 2 distinct (Confidentiality exposure; Data Minimization and Storage Limitation) |
| AWS services classified against IaaS/PaaS/SaaS model | 6 (EC2, VPC, S3, RDS, Lambda, WorkSpaces) |
| Cloud risk findings identified | 2 high-severity (S3 public exposure of KYC documents; RDS Master credential sharing) |
| Auditor testing approaches mapped per service | 4 (Interview, Document Review, Observation, Sampling) |
| Startup-appropriate remediation directions proposed | 3 (account-wide MFA, Just-In-Time access, centralized secrets management via IAM Database Authentication and Secrets Manager) |

---

## Links to Sub-Modules

### [Technical Write-Up: Annex A.7 and AWS Cloud Security](write-up-a7-and-aws-cloud-security.md)
Full methodology and step-by-step reasoning for both projects. Covers the three evidence types and four evidence quality attributes applied across all 14 A.7 controls, the CCTV retention and access workflow findings, the two-part GDPR visitor logbook analysis, the FinTrust Startup architecture and IaaS/PaaS/SaaS classification, the Shared Responsibility Model applied to each service, and the reasoning behind both cloud risk findings and their proposed remediation direction.

### [Business Impact and Risk Analysis](business-impact-a7-and-aws-cloud-security.md)
Risk classification, severity, and proposed remediation direction for every finding identified in both projects, framed for business and regulatory impact rather than technical detail alone.

### [Evidence Matrix: Annex A.7 and AWS Cloud Security](evidence-matrix-a7-and-aws-cloud-security.md)
Clean, control-by-control and service-by-service tables mapping Design, Operating, and Effectiveness evidence for all 14 Annex A.7 controls and all six referenced AWS services, plus the full Interview / Document Review / Observation / Sampling auditor testing matrix with priority focus on S3, RDS, and WorkSpaces.

### [Resource and Reference Library](resource-a7-and-aws-cloud-security.md)
Reference materials, regulatory citations, and frameworks used to build both simulations.

---

## Key Takeaways

- **Evidence quality analysis surfaces gaps that a policy-only review cannot.** The CCTV retention finding existed entirely within the gap between Design evidence (an approved policy) and Operating evidence (the actual system configuration) -- confirming a policy exists is necessary but insufficient audit work.
- **An evidence source can be complete for its own definition while structurally blind to the specific risk under investigation.** Badge logs fully capture every badge swipe and, by that same design, cannot capture entry that occurs without one -- which is exactly what tailgating is.
- **A physical, non-digital artifact can be a GDPR compliance risk on its own**, independent of any system or database. A shared paper visitor logbook produced two distinct principle violations through its physical design alone.
- **High availability and durability are not the same property as confidentiality.** This was the central lesson connecting the AWS shared responsibility analysis to the S3 exposure finding -- AWS's infrastructure-level guarantees for a service say nothing about whether that service's access configuration is appropriately controlled.
- **Individual accountability and credential secrecy are separate security properties**, and a solution designed for one (issuing separate passwords per developer) can leave the other only partially addressed, or introduce new credential-management burden. IAM Database Authentication was the proposed direction specifically because it addresses both simultaneously by removing the long-lived credential entirely.
- **Startup-appropriate remediation is a genuinely different design target, not a smaller version of an enterprise program.** The proposed direction for FinTrust (account-wide MFA, Just-In-Time access, centralized secrets management) reflects what fits a small engineering team's actual operating constraints, rather than a scaled-down enterprise security architecture.

---

## References

- ISO/IEC 27001:2022 (Third Edition), Annex A, Theme 7 -- Physical Controls
- ISO/IEC 27002:2022 -- Implementation guidance for Annex A controls
- Regulation (EU) 2016/679 (GDPR)
- AWS Shared Responsibility Model
- NIST SP 800-145 -- The NIST Definition of Cloud Computing

---

*This portfolio entry was developed as part of a self-directed cybersecurity and GRC learning program. FinTrust Startup is an entirely fictional organization created for educational purposes; all findings, architecture details, and scenarios in this entry are simulated.*
