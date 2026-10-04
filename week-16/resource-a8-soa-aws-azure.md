# Resources and Evidence Matrix: ISO/IEC 27001 Annex A.8, SoA Simulation, and AWS/Azure Cloud Audit Readiness

> **Scope:** Portfolio-wide evidence mapping across all analyzed Annex A controls to date, the Provider Assurance vs. Customer-side evidence distinction, the Design/Operating/Operating Effectiveness evidence taxonomy, and the reference library supporting this entry
> **Companion Files:** [Technical Write-Up](technical-write-up-a8-soa-aws-azure.md) -- [Business Impact and Risk Analysis](business-impact-a8-soa-aws-azure.md)

---

## Bottom Line Up Front

| Area | Summary |
|---|---|
| **Evidence coverage** | Consolidated mapping spans A.8.1-A.8.34 (complete Technological Controls theme) plus cross-domain A.5/A.6/A.7 controls from the SoA simulation |
| **Provider vs. Customer evidence** | A provider assurance report proves the platform *can* be operated securely; by itself, it does not demonstrate that the customer *is* operating it securely -- the two evidence categories address different questions and do not substitute for one another |
| **Evidence taxonomy** | Three tiers -- Design, Operating, Operating Effectiveness -- distinguish "a control exists on paper" from "the control is followed" from "the control demonstrably works over time" |

---

## Part 1 -- Consolidated Evidence Mapping Matrix

This table consolidates evidence mapping across all Annex A controls analyzed in this entry and referenced from prior portfolio work, organized by theme.

### 1.1 -- A.8 Technological Controls (Full Theme, A.8.1-A.8.34)

| Control Range | Domain | Representative Evidence |
|---|---|---|
| A.8.1-A.8.10 | Endpoint, IAM, source code, vulnerability management, data deletion | MDM compliance reports, IAM policy exports, branch protection configuration, vulnerability scan results |
| A.8.11-A.8.20 | Data masking/DLP, backup/redundancy, logging/monitoring/clock sync, privileged utilities, network security | Data masking tooling logs, backup restore test records, SIEM log exports, NTP configuration, firewall rule base |
| **A.8.21-A.8.24** | Network services, segregation, web filtering, cryptography | Network service inventory, VPC/subnet architecture diagrams, DNS filter policy configuration, KMS key rotation policy |
| **A.8.25-A.8.29** | SDLC, application security requirements, architecture principles, secure coding, security testing | Secure Development Policy, application security requirements register, CI/CD SAST/DAST scan logs, UAT sign-off documentation |
| **A.8.30-A.8.31** | Outsourced development, environment separation | Vendor development contracts, environment architecture diagrams with IAM boundaries |
| **A.8.32-A.8.34** | Change management, test data, audit protection | GitHub PR approval logs, change ticket records, data masking/anonymization policy, audit test plans |

### 1.2 -- Cross-Domain Controls Referenced in the SoA Simulation

| Control | Theme | Representative Evidence |
|---|---|---|
| A.5.8 | Organizational | Project delivery methodology documentation showing embedded security gate |
| A.5.23 | Organizational | Cloud vendor risk assessment records, AWS/Azure provider agreement review |
| A.6.3 | People | Security awareness training completion records, phishing simulation results |
| A.6.7 | People | Remote working policy, MDM enrollment and compliance reporting |
| A.7.4 | Physical | CCTV/monitoring coverage records for the specific co-working boundary controlled |
| A.7.7 | Physical | Clear desk walk-through spot-check records, automatic screen-lock configuration |

---

## Part 2 -- Provider Assurance Reports vs. Customer-Side Evidence

### 2.1 The Core Distinction

| Evidence Type | What It Proves | What It Does Not Prove |
|---|---|---|
| **Provider Assurance Report** (AWS Artifact / Azure STP) | The cloud provider's own infrastructure, physical security, and platform operations meet the stated compliance standard (SOC 2 Type II, ISO 27001) | Anything about how the customer has configured their own account, identities, network rules, or data within that infrastructure |
| **Customer-Side Evidence** (IAM logs, NSG/Security Group configuration, CloudTrail/Activity Logs) | The customer's own configuration decisions and ongoing operational behavior within the provider's infrastructure | Nothing about the provider's own infrastructure-level control environment -- that scope is outside what customer-side telemetry can observe |

### 2.2 Platform-Specific Mapping

| Evidence Need | AWS Source | Azure Source |
|---|---|---|
| Provider SOC 2 Type II / ISO 27001 attestation | AWS Artifact | Azure Service Trust Portal (STP) |
| Customer IAM configuration and MFA enforcement | IAM Credential Report | Entra ID Conditional Access policy export |
| Customer network rule configuration | Security Group / NACL export | NSG configuration export, NSG Flow Logs |
| Customer audit trail | CloudTrail | Azure Activity Log, Azure Monitor diagnostic logs |

### 2.3 Why This Distinction Is the Single Most Common Audit-Readiness Gap

An organization that treats a downloaded AWS Artifact or Azure STP report as sufficient evidence of its own security posture has not actually produced any evidence about itself -- it has produced evidence about its provider, which an auditor already has independent access to verify. A genuinely audit-ready evidence package pairs provider assurance (establishing the platform's own baseline is sound) with customer-side evidence (establishing the specific organization's own configuration and operational practice on top of that baseline) -- neither category substitutes for the other, and an auditor evaluating a cloud-hosted organization will expect to see both.

---

## Part 3 -- Evidence Taxonomy: Design, Operating, and Operating Effectiveness

### 3.1 The Three-Tier Distinction

| Tier | Question Answered | Example (A.8.32 Change Management) |
|---|---|---|
| **Design Evidence** | Does a documented control or standard exist? | A documented Change Management Policy requiring approval before production deployment |
| **Operating Evidence** | Is the control being followed in day-to-day practice? | A sample of recent production deployments, each checked for an associated approval record |
| **Operating Effectiveness Evidence** | Does the control demonstrably achieve its intended outcome, sustained over a review period? | Zero unauthorized production changes identified across a full audit period -- supported by confirmation that the approval mechanism was continuously active throughout (not temporarily enabled around a specific audit window), that the sample reviewed covered the full population of production deployments rather than a convenient subset, and that any exceptions, bypasses, or emergency changes during the period went through a documented and appropriately approved exception path |

### 3.2 Why Operating Effectiveness Is Distinct from Operating Evidence

A single sample of recent deployments showing proper approval records (Operating Evidence) confirms the control was followed for that specific sample window. It does not confirm the control has been consistently applied across the full period an auditor needs assurance over -- a control that was correctly followed for the three weeks before an audit review, after being bypassed for the preceding months, would pass an Operating Evidence spot-check while failing Operating Effectiveness entirely. This distinction is why audit evidence collection should be planned as an ongoing practice rather than a pre-audit preparation exercise: Operating Effectiveness evidence cannot be retroactively manufactured in the way a single Operating Evidence sample can be staged.

---

## Part 4 -- Reference Library

### 4.1 ISO/IEC 27001:2022 Standard and Supporting Documents

| Resource | Detail |
|---|---|
| ISO/IEC 27001:2022 (official) | Third edition -- Annex A, Theme 8 (A.8.21-A.8.34 analyzed this entry, completing full A.8.1-A.8.34 coverage) |
| ISO/IEC 27002:2022 | Implementation guidance for Annex A controls, including A.8.21-A.8.34 and the cross-domain A.5/A.6/A.7 controls referenced in the SoA simulation |

### 4.2 AWS and Azure Platform Documentation

| Resource | Relevance |
|---|---|
| AWS Shared Responsibility Model | Primary source for AWS-side responsibility boundary mapping |
| Microsoft Azure Shared Responsibility in the Cloud (Microsoft Learn) | Primary source for Azure-side responsibility boundary mapping, confirming the same IaaS/PaaS/SaaS gradient logic as AWS |
| AWS Artifact documentation | Reference for provider assurance report access on AWS |
| Microsoft Service Trust Portal documentation | Reference for provider assurance report access on Azure (SOC 2, ISO/IEC 27001 audit documentation) |
| Azure Network Security Groups documentation | Reference for NSG configuration and the common-misconfiguration pattern (unrestricted inbound rules) |

### 4.3 PCI DSS and Fintech-Specific Context

| Resource | Relevance |
|---|---|
| PCI Security Standards Council | Reference for cardholder data handling requirements driving PayFast's SoA applicability decisions |

### 4.4 Related Portfolio Entries

| Entry | Connection |
|---|---|
| Prior entry -- Annex A.8 Technological Controls A.8.1-A.8.20 | Establishes a four-tier evidence model (Design, Technical, Operating, Effectiveness), where Technical tier isolated a control's raw, machine-generated configuration state as its own evidence category. This entry's three-tier taxonomy (Design, Operating, Operating Effectiveness) consolidates that Technical artifact as supporting evidence *within* Design or Operating -- whichever a specific configuration export or scan result is being used to demonstrate in context -- rather than introducing a separate evidence model. The consolidation reflects this entry's broader scope (spanning cross-domain SoA controls and two cloud platforms, not only A.8 configuration state), where a single additional tier specific to technical artifacts would not generalize cleanly to organizational or physical controls in the same matrix |
| Prior entry -- Annex A.7 Physical Controls and AWS Shared Responsibility | Establishes the original AWS shared responsibility and evidence mapping pattern this entry extends to a second cloud platform |

---

## Key Lessons Learned

- A Statement of Applicability decision is never made control-by-control in isolation -- a single organizational profile (PayFast's cloud-native, PCI-sensitive, hybrid-workforce characteristics) drives applicability determinations consistently across all four Annex A themes simultaneously.
- The Shared Responsibility Model's underlying principle transfers across cloud providers even when the specific native tooling does not -- a GRC analyst's working knowledge of the AWS model is directly applicable to an Azure environment, with the primary adjustment being vocabulary (NSG vs. Security Groups) rather than conceptual relearning.
- Provider assurance reports do not, by themselves, demonstrate customer-side control operation, on any cloud platform -- this distinction is the most common audit-readiness gap identified across this entry's analysis.
- Operating Effectiveness evidence cannot be retroactively staged in the way a single Operating Evidence sample can be -- evidence collection planning needs to treat Operating Effectiveness as an ongoing practice, not a pre-audit activity.

---

## Study Backlog and Next Steps

- Deepen hands-on evaluation of A.8.30 (Outsourced development) against a simulated vendor development contract, building on the conceptual-level analysis in this entry's companion write-up.
- Evaluate a specific data masking or anonymization tool against A.8.33 (Test information) requirements, moving from control-intent mapping to hands-on technique evaluation.
- Extend the AWS/Azure comparative model to Google Cloud Platform (GCP) to test whether the platform-agnostic Shared Responsibility principle identified in this entry holds across a third major provider.
- Build a complete (not representative-sample) SoA exercise covering all 93 Annex A controls for PayFast, including controls expected to be assessed as Not Applicable with documented exclusion justification.

---

## References

- ISO/IEC 27001:2022 (Third Edition), Annex A, Theme 8 -- Technological Controls
- ISO/IEC 27002:2022 -- Implementation guidance for Annex A controls
- AWS Shared Responsibility Model
- Microsoft Azure Shared Responsibility in the Cloud (Microsoft Learn)
- PCI Security Standards Council

---

*Return to: [Week 16 README](week16-readme.md)*
