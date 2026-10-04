# Business Impact and Risk Analysis: Statement of Applicability, Cloud Misconfiguration, and Supplier Governance -- PayFast

> **Scope:** Business impact, cost-benefit justification, supplier governance, and multi-cloud ownership for findings identified across the SoA simulation and the AWS/Azure comparative assessment, all mapped to the simulated organization PayFast
> **Companion Files:** [Technical Write-Up](02-technical-write-up-a8-soa-aws-azure.md) -- [Resources and Evidence Matrix](04-resource-a8-soa-aws-azure.md)

---

## Bottom Line Up Front

| Area | Business Takeaway |
|---|---|
| **SoA cost-benefit** | Every "Yes" applicability decision for PayFast carries a cost-to-risk ratio that favors inclusion -- none of the 9 controls analyzed represent disproportionate implementation burden relative to the PCI/Fintech risk they close |
| **Misconfiguration impact** | A public storage bucket or missing MFA finding is not a technical footnote for a Fintech startup -- depending on the specific data exposed, it can create cardholder data exposure with potential PCI DSS and regulatory consequences |
| **Supplier governance** | PayFast's risk surface extends beyond its own AWS account into payment gateways, SaaS vendors, and (per the Azure comparison) any secondary cloud dependency |
| **Ownership model** | A RACI structure prevents the single most common multi-cloud failure mode: a control gap nobody owns because "cloud security" was assumed to be someone else's responsibility |

---

## Risk Register Methodology: Likelihood, Remediation SLA, and Ownership

Consistent with established portfolio convention, each finding below documents Severity, Likelihood, Remediation SLA, and Owner alongside the business impact narrative. **Likelihood and Remediation SLA reflect the general principle that response urgency should scale directly with severity**, adapted for PayFast's startup-scale operational tempo rather than a literal citation of a single published framework's exact day-counts.

| Severity | Likelihood | Remediation SLA |
|---|---|---|
| Critical | High | 24-48 hours |
| High | Medium-High to High | 7 days |
| Medium-High | Medium | 14-30 days |

**Ownership reflects PayFast's 20-person, 8-developer operating structure** rather than a dedicated enterprise security function: Engineering Lead / DevOps Lead owns code-level and SDLC findings; Cloud Infrastructure Team owns network, IAM, and cloud configuration findings across both AWS and Azure; GRC/Compliance Lead owns SoA documentation, supplier governance, and cross-framework evidence findings.

---

## Part 1 -- Statement of Applicability: Cost-Benefit and Business Justification

### 1.1 Cost-Benefit Analysis Table

| Control | Theme | Implementation Burden (Startup Context) | Risk Closed | Cost-Benefit Verdict |
|---|---|---|---|---|
| **A.5.23** -- Cloud services | A.5 | Low -- primarily a documented vendor risk assessment process layered onto an existing AWS relationship | Unmanaged third-party cloud and SaaS risk across PayFast's entire infrastructure footprint | Strongly favorable |
| **A.5.8** -- Project management | A.5 | Low-Medium -- a security gate added to existing sprint/release process | Unreviewed features reaching production without a security checkpoint | Favorable |
| **A.6.3** -- Awareness and training | A.6 | Low -- recurring training program, minimal tooling cost | Spear-phishing and social-engineering compromise of staff with payment-system access | Strongly favorable |
| **A.6.7** -- Remote working | A.6 | Low-Medium -- policy plus existing MDM/VPN tooling | Compromise of corporate assets accessed from uncontrolled public locations | Strongly favorable, given 100% hybrid/remote workforce |
| **A.7.4** -- Physical monitoring | A.7 | Low -- scoped to the specific co-working boundary PayFast controls, not a full office build-out | Unauthorized physical access in a shared, multi-tenant environment | Favorable |
| **A.7.7** -- Clear desk/screen | A.7 | Very Low -- policy and automatic screen-lock configuration | Visual data exposure (shoulder surfing) in public co-working space | Strongly favorable -- near-zero cost |
| **A.8.24** -- Cryptography | A.8 | Medium -- AWS KMS key management configuration for data at rest; TLS enforcement across services (PCI DSS floor: TLS 1.2; PayFast's own baseline: TLS 1.3) | Potential PCI DSS non-compliance exposure for cardholder data in transit/at rest if the TLS 1.2 floor is not met | Strongly favorable, and not meaningfully cost-discretionary given PayFast's cardholder-data obligations |
| **A.8.28** -- Secure coding | A.8 | Medium -- SAST/DAST tooling integration into existing CI/CD | Vulnerable code reaching production financial APIs | Strongly favorable |
| **A.8.31** -- Dev/Test/Prod separation | A.8 | Medium -- cloud environment and IAM boundary design | Untested code or bugs directly affecting live payment processing | Strongly favorable |

**Cost-benefit pattern:** every control in this sample returns a favorable-or-better verdict for PayFast specifically because the sample was drawn from controls the organization's own risk profile (cloud-native, PCI-sensitive, hybrid-remote, small engineering team) makes high-value by construction. This is not evidence that every Annex A control would score this favorably for PayFast -- a complete SoA cost-benefit exercise would also surface controls with a less favorable ratio for this organization's specific context (for example, a control oriented toward large-scale, multi-site physical security would carry disproportionate implementation burden relative to risk closed, for a 20-person, single-co-working-space organization), which the representative sample analyzed here did not include.

### 1.2 Business Justification: Why PCI-Sensitive Fintech Changes the Calculus

For a generic SaaS startup, several of the controls above might sit in genuinely discretionary territory. For PayFast specifically, two context factors remove that discretion:

**PCI DSS applicability is externally imposed, not internally chosen.** A.8.24 (cryptography) is not a control PayFast can deprioritize based on its own risk appetite -- cardholder data handling triggers PCI DSS requirements that exist independent of PayFast's internal risk tolerance, converting what would otherwise be a cost-benefit judgment call into a compliance floor.

**A small engineering team concentrates risk rather than diluting it.** An 8-developer team managing financial APIs means there is no large, bureaucratic layer between a single developer's code change and a live payment-processing system -- the controls that govern code quality and change discipline (A.8.28, A.8.31, A.8.32 from the companion write-up) carry higher per-developer impact than the same controls would in a large organization where a single engineer's change passes through multiple review layers before reaching production.

---

## Part 2 -- Cloud Misconfiguration: Business Impact

### 2.1 Finding: Public Storage Exposure (S3 / Azure Blob)

| Field | Detail |
|---|---|
| **Finding Classification** | Nonconformity candidate |
| **Severity** | Critical |
| **Likelihood** | High |
| **Remediation SLA** | 24-48 hours |
| **Owner** | Cloud Infrastructure Team |
| **Platform** | AWS (primary), Azure (comparative risk if adopted) |
| **Threat Scenario** | Direct, unauthenticated access to stored cardholder or transaction data |

**Business impact analysis:** This finding carries impact at three distinct levels, and the distinction matters for how the finding is communicated and prioritized.

*Technical/security impact:* a public storage misconfiguration is, at minimum, unauthorized exposure of whatever data category is stored in the affected bucket. For PayFast, the specific data categories plausibly stored in object storage -- transaction records, KYC documentation, or payment metadata -- make this a direct confidentiality exposure of sensitive, and potentially cardholder-related, data.

*Compliance impact:* whether this specific exposure constitutes PCI DSS noncompliance, and to what degree, depends on the affected data's classification, the bucket's role within PayFast's defined cardholder data environment, and which PCI DSS requirements apply to that specific storage location. An exposure involving data clearly in PCI scope would typically indicate noncompliance with relevant access-control requirements; an exposure involving adjacent but out-of-scope data (for example, general application logs with no cardholder data present) may not carry the same compliance weight, even though it remains a serious confidentiality finding in its own right.

*Downstream consequences:* breach-notification obligations, card-network reporting requirements, and potential contractual or regulatory consequences are not triggered uniformly by PCI DSS itself -- they typically arise from the specific contractual terms PayFast holds with its acquiring bank and the card networks, and from the jurisdiction-specific breach notification laws applicable to the affected data subjects. These obligations may apply here, but their applicability and scope depend on the circumstances of the specific incident, not on the existence of a public bucket alone. This conditionality does not reduce the severity of the finding -- it is the reason the finding is classified as Critical and treated as requiring immediate investigation to determine exactly which of these downstream obligations apply, rather than being assumed away as a low-urgency configuration item.

**Proposed remediation direction:** Recommended default-deny public access enforcement at the account level (S3 Block Public Access on AWS; equivalent container-level public access restriction on Azure), paired with continuous configuration evaluation (AWS Config rules or Azure Policy) rather than point-in-time manual review, given that misconfigurations of this type are frequently introduced by a later, unrelated change rather than present at initial setup.

### 2.2 Finding: Unenforced MFA on Privileged Identity

| Field | Detail |
|---|---|
| **Finding Classification** | Nonconformity candidate |
| **Severity** | High |
| **Likelihood** | Medium-High to High |
| **Remediation SLA** | 7 days |
| **Owner** | Cloud Infrastructure Team |
| **Platform** | AWS IAM (primary), Azure Entra ID (comparative) |
| **Threat Scenario** | Credential-based account takeover of a privileged cloud identity |

**Business impact analysis:** A privileged identity without MFA depends entirely on password secrecy -- for PayFast, a compromised privileged AWS or Azure identity has a direct path to systems governing payment processing, cardholder data storage, or production deployment, meaning the blast radius of a single credential compromise is disproportionately severe relative to the same compromise at an organization without PayFast's financial-data footprint.

**Proposed remediation direction:** Recommended account-wide MFA enforcement as a policy condition for any privileged action (an IAM policy condition on AWS; a Conditional Access policy on Azure), rather than a per-user, opt-in configuration that depends on individual compliance.

### 2.3 Finding: Unassigned OS Patching Responsibility (IaaS)

| Field | Detail |
|---|---|
| **Finding Classification** | Nonconformity candidate |
| **Severity** | Medium-High |
| **Likelihood** | Medium |
| **Remediation SLA** | 14-30 days |
| **Owner** | Cloud Infrastructure Team |
| **Platform** | AWS EC2 (primary), Azure VM (comparative) |
| **Threat Scenario** | Exploitation of a known vulnerability on an unpatched IaaS instance |

**Business impact analysis:** The shared responsibility model established in the companion write-up makes OS patching explicitly a customer obligation in IaaS deployments on both AWS and Azure -- when no individual or team is clearly assigned ownership of this obligation, the organization can mistakenly assume provider-managed patching coverage that does not exist at this service layer, leaving instances exposed for the full window between vulnerability disclosure and eventual, undirected remediation.

**Proposed remediation direction:** Recommended an explicit, named ownership assignment for IaaS patch management as part of the RACI structure in Section 3.2 below, paired with a recurring vulnerability scan cadence rather than an ad hoc patching practice.

---

## Part 3 -- Supplier Governance and Multi-Cloud Ownership

### 3.1 Supplier Risk Governance for PayFast

PayFast's A.5.23 applicability determination (Part 1) establishes that supplier and cloud vendor risk is a primary, not secondary, risk category for this organization. Three supplier categories carry distinct risk profiles:

| Supplier Category | Example | Primary Risk | Governance Mechanism |
|---|---|---|---|
| **Cloud infrastructure provider** | AWS (primary), potential Azure adoption | Infrastructure-level outage or breach outside PayFast's direct control | Provider assurance report review (AWS Artifact / Azure STP), SLA review |
| **Payment gateway / processor** | Third-party PCI-scope payment processor | Scope-reduction dependency -- PayFast's own PCI burden is partly transferred, not eliminated | Processor PCI DSS attestation review, contractual security clause verification |
| **Third-party SaaS vendors** | Business tooling with access to PayFast data | Data handling and access scope outside PayFast's infrastructure boundary | Vendor security questionnaire, data processing agreement review |

**The critical distinction for a payment gateway specifically:** routing card transaction processing through a PCI DSS-accredited third-party gateway narrows PayFast's own PCI DSS compliance scope for cardholder data handling. It does not eliminate PayFast's security governance obligation for that relationship -- PayFast remains accountable for verifying the gateway's own compliance posture and for any cardholder data that transits or is referenced within PayFast's own systems before reaching the gateway.

### 3.2 Multi-Cloud Ownership: A RACI Concept for PayFast

The AWS/Azure comparative analysis in the companion write-up surfaces a structural governance risk specific to any organization operating (or considering operating) more than one cloud platform: a control that is clearly owned when only one platform is in use can become an orphaned responsibility once a second platform enters the environment, because each team may reasonably assume the other team or the original single-platform process already covers it.

| Activity | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| AWS IAM / Azure Entra ID configuration | Cloud Infrastructure Team | Engineering Lead | GRC/Compliance Lead | All developers |
| Network security group configuration (AWS SG / Azure NSG) | Cloud Infrastructure Team | Engineering Lead | -- | GRC/Compliance Lead |
| Provider assurance report review (AWS Artifact / Azure STP) | GRC/Compliance Lead | Engineering Lead | Cloud Infrastructure Team | -- |
| SoA maintenance and control applicability review | GRC/Compliance Lead | Engineering Lead | Cloud Infrastructure Team | All staff |
| Patch management (EC2 / Azure VM) | Cloud Infrastructure Team | Engineering Lead | -- | GRC/Compliance Lead |
| Supplier security review (gateways, SaaS vendors) | GRC/Compliance Lead | Engineering Lead | Cloud Infrastructure Team | -- |

**Why this RACI structure specifically prevents the orphaned-control failure mode identified above:** every row names exactly one Accountable party regardless of which cloud platform the activity touches, so the question "who owns this if we add a second cloud provider" has a pre-answered response rather than requiring an ad hoc decision at the moment a gap is discovered -- typically during an incident or an audit, which is the worst time to be working out an ownership ambiguity for the first time.

---

## References

- ISO/IEC 27001:2022 Annex A.5.8, A.5.23, A.6.3, A.6.7, A.7.4, A.7.7, A.8.24, A.8.28, A.8.31 (SoA simulation controls)
- PCI DSS -- Payment Card Industry Data Security Standard (referenced for cardholder data handling context)
- AWS Shared Responsibility Model
- Microsoft Azure Shared Responsibility in the Cloud (Microsoft Learn)

---

*This analysis was developed as part of a self-directed cybersecurity portfolio project. PayFast is an entirely fictional organization created for educational purposes; all findings, architecture details, and scenarios in this entry are simulated.*

---

*Return to: [README](01-README.md)*
