# Week 16: ISO/IEC 27001 Annex A.8 Completion, Statement of Applicability Simulation, and AWS/Azure Comparative Cloud Security -- PayFast

> **Format:** Final Annex A.8 control cluster (A.8.21-A.8.34), a cross-domain Statement of Applicability simulation, and a comparative AWS/Azure shared responsibility and risk assessment
> **Simulated Organization:** PayFast -- a 20-person hybrid/remote Fintech startup, 100% AWS-hosted, processing PCI-DSS-sensitive cardholder data

---

## Executive Summary

This entry closes out full coverage of ISO/IEC 27001:2022 Annex A.8 (Technological Controls) by analyzing the final 14 controls, A.8.21-A.8.34, spanning network and cryptographic controls, the secure development lifecycle, development testing and outsourcing governance, and change/test-data/audit protection controls. Combined with prior portfolio work on A.8.1-A.8.20, this represents **complete analysis of all 34 Technological Controls** in Annex A.8.

The entry then shifts from single-theme analysis to **cross-domain integration**, simulating a Statement of Applicability (SoA) decision framework for a cloud-native Fintech startup, **PayFast**. Nine representative controls spanning all four Annex A themes (Organizational, People, Physical, Technological) were evaluated against PayFast's specific operating context -- 100% AWS-hosted, PCI-DSS-sensitive, hybrid/remote workforce -- demonstrating that a defensible SoA applicability decision is driven by organizational risk context, not generic control text.

The entry closes with a **comparative AWS and Microsoft Azure shared responsibility assessment**, extending the Shared Responsibility Model analysis from a single-platform to a multi-platform GRC skill: the same provider/customer boundary logic, the same four customer-misconfiguration risk categories (public storage, missing MFA, unmonitored audit logs, unassigned OS patching ownership), and the same Provider Assurance vs. Customer-Side evidence distinction all hold across both platforms, with the primary difference being platform-native tooling and terminology rather than the underlying governance principle.

> **Scope note:** This entry addresses Annex A.8 controls A.8.21-A.8.34 (completing the 34-control theme), a representative 9-control SoA sample spanning all four Annex A themes (not an exhaustive 93-control SoA), and a comparative AWS/Azure assessment scoped to the shared responsibility principle and common misconfiguration categories (not a comprehensive platform-by-platform service audit). All findings, PayFast, and its architecture are entirely simulated for self-directed training purposes; no finding in this entry reflects an actual completed remediation, live production system, or real organization.

---

## Table of Contents

- [Key Skills Demonstrated](#key-skills-demonstrated)
- [Resume Bullet Points](#resume-bullet-points)
- [Repository Structure](#repository-structure)
- [Key Metrics and Outcomes](#key-metrics-and-outcomes)
- [Technical Write-Up](02-technical-write-up-a8-soa-aws-azure.md) -- A.8.21-A.8.34 analysis, SoA simulation, AWS/Azure comparison
- [Business Impact and Risk Analysis](03-business-impact-a8-soa-aws-azure.md) -- Cost-benefit justification, misconfiguration impact, supplier governance, RACI
- [Resources and Evidence Matrix](04-resource-a8-soa-aws-azure.md) -- Consolidated evidence mapping, provider vs. customer evidence, reference library

---

##Key Skills Demonstrated

| Domain | Specific Capability Demonstrated |
|---|---|
| **ISO/IEC 27001:2022 Annex A.8** | Complete 34-control coverage (A.8.1-A.8.34) across endpoint, IAM, network, cryptography, secure development, and change management domains |
| **Statement of Applicability (SoA)** | Risk-based control applicability justification driven by organizational context, spanning all four Annex A themes |
| **Cross-Domain Integration** | Mapping the interplay between Organizational, People, Physical, and Technological controls rather than analyzing each theme in isolation |
| **AWS Shared Responsibility Model** | Provider/customer boundary mapping across IaaS, PaaS, and Serverless service models |
| **Microsoft Azure Shared Responsibility Model** | Comparative boundary mapping (NSG, Entra ID, Activity Log) demonstrating platform-transferable GRC skill |
| **Cloud Misconfiguration Risk Assessment** | Public storage exposure, unenforced MFA, unmonitored audit logs, and unassigned OS patching ownership, evaluated across both AWS and Azure |
| **Evidence Taxonomy** | Design / Operating / Operating Effectiveness evidence distinction, plus Provider Assurance vs. Customer-Side evidence separation |
| **Supplier and Vendor Governance** | Payment gateway and SaaS vendor risk evaluation, including PCI DSS scope-transfer reasoning |
| **Multi-Cloud Ownership Design** | RACI-based accountability structure for cloud security activities spanning more than one provider |

---

## Resume Bullet Points

*Drawn exclusively from this entry's scope (A.8.21-A.8.34, the PayFast SoA simulation, and the AWS/Azure comparative assessment). Action-oriented and ready for direct use.*

### Junior GRC Analyst

- **Analyzed** the complete ISO/IEC 27001:2022 Annex A.8 Technological Controls theme (all 34 controls, A.8.1-A.8.34), mapping each control to technical mechanism, representative evidence, and audit testing approach.
- **Simulated** a Statement of Applicability (SoA) decision framework for a cloud-native Fintech startup, evaluating 9 representative controls across all four Annex A themes (Organizational, People, Physical, Technological) with documented, risk-based business justification for each applicability determination.
- **Developed** a cost-benefit analysis methodology for SoA control inclusion, pairing implementation burden against risk closed for a PCI-DSS-relevant, startup-scale operating context.
- **Constructed** a three-tier evidence taxonomy (Design, Operating, Operating Effectiveness) distinguishing documented policy from day-to-day practice from sustained, auditable outcome -- applied consistently across cross-domain Annex A controls.
- **Evaluated** supplier and third-party risk governance for payment gateway and SaaS vendor relationships, including PCI DSS compliance-scope transfer reasoning distinct from security governance accountability.
- **Mapped** compliance evidence requirements distinguishing Provider Assurance reports (AWS Artifact, Azure Service Trust Portal) from Customer-Side evidence (IAM configuration, network security rules, audit logs), identifying this distinction as a common audit-readiness gap.

### Junior Cybersecurity Consultant

- **Analyzed** AWS and Microsoft Azure Shared Responsibility Models in parallel, demonstrating platform-transferable understanding of the provider/customer security boundary across IaaS, PaaS, and SaaS service models.
- **Identified** recurring customer-side cloud misconfiguration risk categories -- public storage exposure, unenforced multi-factor authentication, unmonitored audit logging, and unassigned OS patching ownership -- evaluated consistently across both AWS and Azure environments.
- **Assessed** network security control configuration (AWS Security Groups and NACLs; Azure Network Security Groups) for common misconfiguration patterns, including unrestricted inbound administrative access rules.
- **Reviewed** Infrastructure-as-a-Service (IaaS) operating system patch management responsibility boundaries across both cloud platforms, identifying unassigned ownership as a recurring architecture-review finding.
- **Designed** a RACI-based ownership model for multi-cloud security operations, addressing the orphaned-control risk that arises when a security activity's ownership is assumed rather than explicitly assigned across more than one cloud platform.
- **Mapped** secure development lifecycle controls (A.8.25-A.8.29) to CI/CD pipeline enforcement points, balancing automated SAST/DAST security testing against agile delivery velocity for a small engineering team.

---

## Repository Structure

```
week-16/
|-- 01-readme.md                                  (this file -- main portfolio index)
|-- 02-technical-write-up-a8-soa-aws-azure.md              (A.8.21-A.8.34, SoA simulation, AWS/Azure comparison)
|-- 03-business-impact-a8-soa-aws-azure.md                  (Cost-benefit, misconfiguration impact, supplier governance, RACI)
`-- 04-resource-a8-soa-aws-azure.md                        (Evidence matrix, provider vs. customer evidence, reference library)
```

---

## Key Metrics and Outcomes

| Metric | Result |
|---|---|
| Annex A.8 controls analyzed this entry | 14 / 34 (A.8.21-A.8.34) |
| Cumulative A.8 theme coverage | **34 / 34 (100% complete)** |
| SoA controls evaluated | 9, spanning all 4 Annex A themes |
| SoA applicability determinations | 9 / 9 assessed Applicable (representative sample; not an exhaustive 93-control SoA) |
| Cloud platforms compared | 2 (AWS, Microsoft Azure) |
| Platform-agnostic misconfiguration risk categories identified | 4 (public storage, missing MFA, unmonitored audit logs, unassigned OS patch ownership) |
| Evidence taxonomy tiers applied | 3 (Design, Operating, Operating Effectiveness) |
| Cross-domain controls referenced in SoA | 6 (A.5.8, A.5.23, A.6.3, A.6.7, A.7.4, A.7.7) |

---

## Key Takeaways

- **Reaching full A.8 theme coverage (34/34) demonstrates depth, not just breadth** -- the final 14 controls (A.8.21-A.8.34) close the secure development, change management, and audit protection gaps that the earlier A.8.1-A.8.20 analysis did not cover, producing a complete technological-controls picture rather than a partial one.
- **A Statement of Applicability is a cross-domain exercise by nature.** PayFast's single organizational profile drove consistent applicability logic across Organizational, People, Physical, and Technological controls simultaneously -- an SoA built theme-by-theme in isolation would miss this connective reasoning.
- **The Shared Responsibility Model is a transferable GRC skill, not an AWS-specific one.** Extending the same analytical framework to Azure surfaced an identical underlying principle with different native tooling -- directly relevant to a consultant role that may need to assess any cloud platform, not only the one most familiar from prior training.
- **Provider assurance reports and customer-side evidence are never interchangeable**, a distinction that recurred as the single most consequential audit-readiness insight across both the AWS and Azure evidence analysis.

---

## References

- ISO/IEC 27001:2022 (Third Edition), Annex A, Theme 8 -- Technological Controls
- ISO/IEC 27002:2022 -- Implementation guidance for Annex A controls
- AWS Shared Responsibility Model
- Microsoft Azure Shared Responsibility in the Cloud (Microsoft Learn)
- PCI Security Standards Council

---

*This portfolio entry was developed as part of a self-directed cybersecurity and GRC learning program. PayFast is an entirely fictional organization created for educational purposes; all findings, architecture details, and scenarios in this entry are simulated.*
