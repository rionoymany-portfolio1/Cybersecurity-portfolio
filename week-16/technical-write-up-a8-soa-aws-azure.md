# Technical Write-Up: ISO/IEC 27001 Annex A.8 (A.8.21-A.8.34), Statement of Applicability Simulation, and AWS/Azure Shared Responsibility -- PayFast

> **Scope:** Annex A.8 Technological Controls A.8.21-A.8.34 (14 of 34 controls), a Statement of Applicability (SoA) decision simulation spanning all four Annex A themes, and a comparative AWS/Azure shared responsibility and risk assessment
> **Simulated Organization:** PayFast -- a 20-person hybrid/remote Fintech startup, 100% AWS-hosted, processing PCI-DSS-sensitive cardholder data
> **Companion Files:** [Business Impact and Risk Analysis](business-impact-a8-soa-aws-azure.md) -- [Resources and Evidence Matrix](resource-a8-soa-aws-azure.md)

---

## Bottom Line Up Front

| Area | Finding |
|---|---|
| **A.8.21-A.8.34 coverage** | 14 technological controls analyzed across Network and Cryptography, Secure Development, Development Testing and Outsourcing, and Change/Test Data/Audit Protection domains |
| **SoA simulation** | 9 representative controls across all four Annex A themes evaluated for PayFast; all 9 assessed as **Applicable** given PayFast's cloud-native, PCI-sensitive, hybrid-workforce profile |
| **AWS vs. Azure comparison** | Same underlying principle (**Security OF vs. IN the cloud**), different native tooling -- NSG vs. Security Groups, Activity Log vs. CloudTrail, STP vs. Artifact |
| **Primary cross-cutting risk** | Misconfiguration (public storage, missing MFA, unmonitored audit logs, unassigned OS patching ownership) is platform-agnostic -- the control gap, not the cloud provider, drives the risk |

---

# Part 1 -- Annex A.8 Technological Controls (A.8.21-A.8.34)

## Scope Disclaimer

This analysis covers Annex A.8 controls A.8.21 through A.8.34 only -- the final 14 of ISO 27001:2022's 34 total Technological Controls. Combined with A.8.1-A.8.20 analyzed in a prior portfolio entry, this completes full coverage of Theme A.8 (34 of 34 controls). A.5 (Organizational), A.6 (People), and A.7 (Physical) controls are addressed in prior entries, with select cross-domain controls revisited in the SoA simulation in Part 2 of this write-up.

## 1.1 Methodology

Each control was grouped into one of four functional domains, then evaluated for its practical risk-reduction purpose, the technology or mechanism that typically enforces it, and the evidence an auditor would expect to see.

| Domain | Controls | Focus |
|---|---|---|
| **Network and Cryptography** | A.8.21-A.8.24 | Network service security, segmentation, web filtering, cryptographic lifecycle |
| **Secure Development Foundation** | A.8.25-A.8.28 | SDLC, application security requirements, architecture principles, secure coding |
| **Development Testing and Outsourcing** | A.8.29-A.8.31 | Security testing, third-party development governance, environment separation |
| **Change, Test Data, and Audit Protection** | A.8.32-A.8.34 | Change management, test data handling, protection of systems during audit |

## 1.2 Control-by-Control Summary

| Control | Title | Mechanism Analyzed | Representative Evidence |
|---|---|---|---|
| A.8.21 | Security of network services | Service-level security requirements identified for in-house and outsourced network services | Network service inventory, SLA security clauses |
| A.8.22 | Segregation of networks | VPC subnet design, security groups preventing lateral movement between zones | Network architecture diagram, firewall rule base |
| A.8.23 | Web filtering | DNS-based filtering identified as a lightweight, startup-appropriate alternative to a full Secure Web Gateway (SWG) deployment | DNS filter policy configuration, blocked-category logs |
| A.8.24 | Use of cryptography | Policy-driven key management via AWS KMS (with CloudHSM as a dedicated-hardware option) for data at rest; PayFast's own internal security baseline sets TLS 1.3 for data in transit, a standard exceeding the TLS 1.2 floor PCI DSS mandates | KMS key rotation policy, TLS configuration benchmark, cryptographic standard documentation |
| A.8.25 | Secure development life cycle | Security requirements embedded in SDLC phases from planning through maintenance | Secure Development Policy, SDLC phase gate documentation |
| A.8.26 | Application security requirements | Input validation, authentication, and data encryption requirements specified pre-development | Application security requirements register |
| A.8.27 | Secure system architecture and engineering principles | Documented, applied engineering principles for secure-by-design system builds | Architecture review records, design standard documentation |
| A.8.28 | Secure coding | SAST/DAST tooling integrated into CI/CD pipelines, aligned to OWASP Top 10 | CI/CD scan configuration, SAST/DAST scan logs |
| A.8.29 | Security testing in development and acceptance | Automated SAST/DAST testing balanced against agile delivery speed, pre-deployment gate | CI/CD pipeline test results, UAT sign-off documentation |
| A.8.30 | Outsourced development | Direction, monitoring, and review of third-party development activity | Vendor development contract, code review records for outsourced work |
| A.8.31 | Separation of development, test, and production environments | Cloud environment segregation preventing unvetted code from reaching production | Environment architecture diagram, IAM boundary per environment |
| A.8.32 | Change management | Pull request review and branch protection rules enforced for production changes | GitHub PR approval logs, change ticket records |
| A.8.33 | Test information | Appropriate selection and protection of test data, particularly when derived from production | Data masking/anonymization policy, test dataset provenance log |
| A.8.34 | Protection of information systems during audit testing | Audit and assurance activities planned and agreed to avoid disrupting operational systems | Audit test plan, read-only access scoping for audit activities |

## 1.3 Risk Mapping: Three Controls in Practical Context

### 1.3.1 -- A.8.23 (Web Filtering): Lightweight Control for a Resource-Constrained Startup

**The risk mapped:** Phishing and drive-by malware delivered through uncontrolled web access are a disproportionately high risk for a small, hybrid-workforce Fintech where every employee's browser session is a potential entry point to systems handling cardholder data.

**Why DNS-based filtering was identified as the fit for this stage:** A full Secure Web Gateway with deep packet inspection is both a cost and an operational-overhead commitment that does not match a 20-person organization's current scale. DNS-based filtering intercepts and blocks resolution requests to known-malicious domains at the network layer, requiring no endpoint agent deployment and minimal ongoing tuning -- a control that closes a meaningful fraction of the phishing/malware risk surface at a cost and complexity level appropriate to the organization's size, rather than a partial implementation of enterprise-grade web security tooling.

### 1.3.2 -- A.8.29 (Security Testing): Balancing Agile Velocity Against Risk

**The risk mapped:** A startup's competitive position depends on shipping features quickly; a security testing regime modeled on a slower-moving enterprise release cycle would create friction that the business cannot absorb, while skipping security testing entirely leaves vulnerabilities to reach production unchecked.

**The resolution identified:** automated SAST/DAST integrated directly into the CI/CD pipeline rather than a separate, manually-gated security review stage. Static analysis runs against every commit with no added wait time for the developer; dynamic analysis runs against the build artifact as part of the existing pipeline. This converts security testing from an additional sequential step that slows releases into a parallel, automated check that developers experience as part of the normal pipeline -- preserving agile velocity while still gating deployment on the absence of newly-introduced high-severity findings.

### 1.3.3 -- A.8.32 (Change Management): Linking Unauthorized Modification to Business Risk

**The risk mapped:** An unauthorized or unreviewed production modification is not merely a technical quality issue -- for a Fintech processing financial transactions, an unreviewed change reaching the payment flow carries direct business and stakeholder risk: a logic error in transaction processing has immediate financial consequences, and a change that bypasses review has, by definition, had no independent verification that it does not introduce exactly that kind of error.

**The control proposed:** a lightweight peer-review workflow -- pull request review with branch protection rules on the default production branch -- scoped to be proportionate to an 8-developer engineering team rather than a multi-stage enterprise change advisory board. The mechanism (mandatory review before merge) is the same core principle a larger organization would apply; the process weight around it is calibrated to the team size.

## 1.4 Annex A Cross-Domain Integration

A.8.21-A.8.34 does not operate in isolation from the other three Annex A themes -- each A.8 control depends on, or directly enforces, a decision made at the organizational, people, or physical layer:

- **A.5 (Organizational)** sets the governance policies and risk assessment methodology that determine, for example, which cryptographic standards A.8.24 must enforce, or what risk threshold triggers a change under A.8.32.
- **A.6 (People)** is what makes A.8.23's web filtering control meaningful in practice -- a filtering policy without corresponding security awareness training (A.6.3) addresses the technical vector but not the social-engineering vector that often accompanies it.
- **A.7 (Physical)** protects the facilities and hardware A.8 controls ultimately protect data on -- a flawlessly segregated network (A.8.22) still depends on the physical security of the endpoints connecting to it.
- **A.8 (Technological)** is the layer that converts A.5's policy decisions into enforced technical safeguards across networks, code, and cloud infrastructure -- the mechanism, not the source, of the organization's security requirements.

This interplay is the direct motivation for the SoA simulation in Part 2: a Statement of Applicability cannot be built theme-by-theme in isolation, because a single organizational context (PayFast's cloud-native, PCI-sensitive, hybrid-workforce profile) drives applicability decisions across all four themes simultaneously.

## 1.5 Limitations and Knowledge Gaps

This review focused on architectural overview, control purpose, and evidence mapping rather than deep-dive, hands-on lab configuration of each control. Two specific gap areas were identified for continued study: **A.8.30 (Outsourced development)** -- the contractual and governance mechanics of directing and reviewing third-party development work were analyzed at a conceptual level only, without a simulated vendor contract to evaluate against; and **A.8.33 (Test information)** -- data masking and anonymization techniques for test datasets derived from production were mapped at the control-intent level, without hands-on evaluation of a specific masking tool or technique.

---

# Part 2 -- Statement of Applicability (SoA) Simulation: PayFast

## 2.1 Objective and Organizational Context

This simulation builds a Statement of Applicability decision framework for **PayFast**, a cloud-native Fintech startup, applying a risk-based justification to each control's inclusion rather than a default "apply everything" approach. The SoA is the document that declares, for every Annex A control, whether it is applicable to the organization and why -- it is the artifact that demonstrates the organization has *considered* every control, not that it has applied all 93.

**PayFast's profile, which drives every justification below:**

| Attribute | Detail |
|---|---|
| Team size | 20 people, hybrid/remote |
| Cloud footprint | 100% AWS-hosted |
| Data sensitivity | PCI-DSS-relevant cardholder data; financial transaction data |
| Workforce model | Hybrid/remote; co-working space usage |
| Engineering team | 8 developers managing financial APIs |

## 2.2 SoA Decision Logic by Control

The following 9 controls were evaluated as representative examples spanning all four Annex A themes. Each entry below states the business context driving the applicability decision, not merely the control's generic definition.

### A.5 Organizational Theme

**A.5.23 -- Information security for use of cloud services.** PayFast's entire infrastructure dependency sits with AWS, payment gateway providers, and third-party SaaS vendors -- a cloud-native organization with no on-premises infrastructure has its primary attack surface and primary vendor-risk surface concentrated almost entirely in its cloud and SaaS relationships, making this control's applicability self-evident rather than a judgment call.

**A.5.8 -- Information security in project management.** PayFast's competitive position depends on high-velocity feature releases; without a mandatory security gate built into the project delivery process itself, security review becomes an optional step teams can skip under delivery pressure -- embedding the requirement into project management is what makes the gate structurally unavoidable rather than dependent on individual diligence.

### A.6 People Theme

**A.6.3 -- Information security awareness and training.** The human factor is the most consistently exploited vulnerability class in financial-sector attacks specifically; spear-phishing targeting Fintech employees (who routinely have access to payment systems or customer financial data) is a foreseeable, high-likelihood threat vector that technical controls alone cannot close.

**A.6.7 -- Remote working.** PayFast's workforce is 100% hybrid/remote, meaning every employee routinely accesses corporate systems from outside any controlled office perimeter -- the exception case this control is designed for (an employee occasionally working remotely) is PayFast's *default* operating condition, making the control non-negotiable rather than a nice-to-have.

### A.7 Physical Theme

**A.7.4 -- Physical security monitoring.** PayFast operates from shared co-working environments rather than a dedicated, wholly-controlled office -- a shared space means PayFast cannot rely on a single, organization-controlled perimeter and instead needs active monitoring of the specific boundary and access points it does control.

**A.7.7 -- Clear desk and clear screen.** The same shared co-working context that drives A.7.4 directly drives this control: a desk or screen left unattended in a space shared with unrelated third parties creates a direct shoulder-surfing and visual-eavesdropping risk that would not exist in the same form inside a dedicated, access-controlled office.

### A.8 Technological Theme

**A.8.24 -- Use of cryptography.**
- *Why applicable:* PayFast processes cardholder data -- a data category with an explicit, non-discretionary protection requirement under PCI DSS for both data in transit and data at rest, making this control mandatory on regulatory grounds independent of PayFast's own internal risk appetite.
- *How enforced:* PCI DSS Requirement 4.2.1 sets the regulatory floor -- strong cryptography, with TLS 1.2 or higher for data in transit. PayFast's own security baseline goes beyond that floor, standardizing on TLS 1.3 as an internal hardening decision rather than a PCI-mandated version. Data at rest is protected via AWS KMS-managed encryption keys, with CloudHSM available as a dedicated hardware-backed option for key material requiring single-tenant HSM control.
- *Evidence:* KMS key rotation policy, TLS configuration benchmark confirming the enforced minimum version, cryptographic standard documentation distinguishing the regulatory floor from PayFast's internal baseline.

**A.8.28 -- Secure coding.**
- *Why applicable:* An 8-developer team building and maintaining financial APIs directly handling payment data means insecure coding practices -- unvalidated input, improperly handled secrets, injection flaws -- have a direct, undiluted path to a cardholder-data-handling production system, with no intermediate layer or legacy system to absorb the risk.
- *How enforced:* A defined secure coding standard aligned to OWASP Top 10, paired with SAST/DAST scanning in the CI/CD pipeline (A.8.28's direct link to A.8.29, analyzed in Part 1) and code review before merge.
- *Evidence:* Secure coding standard documentation, CI/CD SAST/DAST scan logs, pull request review records.

**A.8.31 -- Separation of development, test, and production environments.** Cloud environment segregation is what prevents an unvetted change or an undiscovered bug in a test environment from ever having the opportunity to affect production financial transaction processing -- for an organization where production directly handles live payments, this separation is the structural backstop behind every other code-quality or testing control.

## 2.3 Simulated Statement of Applicability (SoA) Summary Table

| Control ID | Control Name | Theme | Applicable? | Primary Risk / Business Justification |
|---|---|---|---|---|
| **A.5.23** | Information security for use of cloud services | A.5 Organizational | **Yes** | 100% reliance on AWS, payment gateways, and third-party SaaS vendors |
| **A.5.8** | Information security in project management | A.5 Organizational | **Yes** | High-velocity feature releases require mandatory security gates before deployment |
| **A.6.3** | Information security awareness and training | A.6 People | **Yes** | Human factor vulnerability; addresses spear-phishing targeting Fintech employees |
| **A.6.7** | Remote working | A.6 People | **Yes** | 100% hybrid/remote workforce accessing corporate assets from public locations |
| **A.7.4** | Physical security monitoring | A.7 Physical | **Yes** | Shared co-working office environment requiring boundary access control |
| **A.7.7** | Clear desk and clear screen | A.7 Physical | **Yes** | Prevents visual eavesdropping and shoulder surfing in public working spaces |
| **A.8.24** | Use of cryptography | A.8 Technological | **Yes** | Mandatory protection of cardholder data and financial transactions in transit and at rest |
| **A.8.28** | Secure coding | A.8 Technological | **Yes** | Financial API codebase handling cardholder data requires defined secure coding standards (input validation, secrets handling, OWASP-aligned practices) to prevent common coding vulnerabilities from reaching production |
| **A.8.31** | Separation of development, test, and production | A.8 Technological | **Yes** | Cloud environment segregation; prevents unvetted code or bugs from affecting production |

**On the uniform "Yes" result:** this 9-control sample was selected as representative examples relevant to PayFast's specific profile, not as a random or exhaustive sample of the full 93-control set -- the consistent applicability result reflects that these specific controls were deliberately chosen because they map directly onto PayFast's cloud-native, PCI-sensitive, hybrid-workforce characteristics, not a general claim that every Annex A control is universally applicable to every organization. A complete SoA exercise would also surface controls assessed as not applicable with a documented exclusion justification (for example, a control addressing on-premises data center physical perimeters would likely be excluded for a 100% cloud-hosted organization), a case this representative sample did not include.

---

# Part 3 -- AWS and Microsoft Azure Shared Responsibility Model: Comparative Cloud Risk and Evidence Mapping

## 3.1 Objective and Scope

This entry extends the shared responsibility and cloud risk analysis established in prior portfolio work to a second cloud platform, Microsoft Azure, evaluated alongside AWS -- the platform PayFast's own infrastructure runs on. The objective is to demonstrate that the underlying GRC principle (a consistent provider/customer responsibility boundary that shifts by service model) holds across providers, while the specific native tooling an auditor or GRC analyst needs to reference differs by platform.

## 3.2 Control Boundaries: Provider vs. Customer, Both Platforms

| Responsibility Layer | AWS | Azure | Owner |
|---|---|---|---|
| Physical data centers, global infrastructure | AWS data centers | Azure data centers | Provider |
| Hypervisor and host virtualization | AWS-managed | Microsoft-managed | Provider |
| Network controls above the hypervisor | Security Groups, NACLs | Network Security Groups (NSGs) | Customer |
| Identity and Access Management | IAM | Microsoft Entra ID (Azure AD) | Customer |
| OS patching | Required in IaaS (EC2) | Required in IaaS (Azure VM) | Customer (IaaS only) |
| Application code security | Customer-owned | Customer-owned | Customer |
| Data classification and encryption configuration | Customer-owned | Customer-owned | Customer |

**The service-model gradient holds on both platforms:** in an IaaS deployment (EC2 or Azure VM), the customer holds the largest share of "security IN the cloud" responsibility, including OS-level patching. As the service model moves toward PaaS and SaaS, Microsoft's own shared responsibility guidance documents the same narrowing of customer responsibility that AWS's model describes -- network controls shift from fully customer-owned in IaaS to shared in PaaS to provider-owned in SaaS, following the identical underlying logic documented for AWS in prior portfolio analysis. This is the core finding of the comparison: the shared responsibility *principle* is platform-agnostic; only the specific native service names enforcing it differ.

## 3.3 Customer Misconfiguration Risks: Platform-Agnostic Risk Categories

Four misconfiguration categories recur across both platforms, because they stem from the same customer-side responsibility gap regardless of which provider's console the configuration lives in:

| Risk Category | AWS Manifestation | Azure Manifestation |
|---|---|---|
| Unenforced MFA | IAM users without MFA enforced | Entra ID accounts without MFA enforced |
| Public storage exposure | Public S3 bucket | Public Azure Blob Storage container |
| Unmonitored audit logs | CloudTrail not enabled or not centrally reviewed | Azure Activity Log / Diagnostic Logs not enabled or not centrally reviewed |
| Unassigned OS patching responsibility | Unpatched EC2 instance, ownership unclear | Unpatched Azure VM, ownership unclear |

**Why this pattern recurs identically on both platforms:** each of these four risks exists precisely because the relevant control sits on the customer side of the responsibility boundary established in Section 3.2 -- Azure NSGs are explicitly documented as customer-configured, with Microsoft's own guidance noting that an NSG permitting unrestricted inbound access on an administrative port is "an extremely common finding in Azure security reviews," the direct Azure-platform analog of the unrestricted AWS Security Group risk category analyzed in prior portfolio work. The provider's infrastructure-level security posture does not change whether the customer has correctly configured a network rule, enabled MFA, or restricted a storage container's access scope -- that responsibility, and that risk, is identical in kind on both platforms.

## 3.4 Evidence and Compliance Mapping: Provider vs. Customer Evidence

| Evidence Category | AWS Source | Azure Source |
|---|---|---|
| **Provider assurance (SOC 2 Type II, ISO 27001)** | AWS Artifact | Azure Service Trust Portal (STP) |
| **Customer-side access control evidence** | IAM Credential Report, MFA enforcement policy | Entra ID Conditional Access policy, MFA enforcement report |
| **Customer-side network evidence** | Security Group / NACL configuration export | NSG configuration export, NSG Flow Logs |
| **Customer-side audit trail evidence** | CloudTrail logs | Azure Activity Log, Azure Monitor diagnostic logs |
| **Change management evidence** | Change ticket records, infrastructure-as-code commit history | Change ticket records, infrastructure-as-code commit history |

**Why provider assurance reports cannot substitute for customer-side evidence, on either platform:** an AWS Artifact SOC 2 report attests to AWS's own control environment; an Azure STP SOC 2 report attests to Microsoft's. Neither report contains any information about whether a specific customer's IAM policies are least-privilege, whether a specific customer's storage containers are public, or whether a specific customer's audit logs are actually being reviewed -- these are customer-side configuration states that exist entirely outside the scope of what a provider's own third-party audit evaluates. This is the direct justification for the Design/Operating/Operating Effectiveness evidence taxonomy applied to this evidence set in the companion [Resources and Evidence Matrix](resource-a8-soa-aws-azure.md) file: provider assurance reports establish that the underlying platform *can* be operated securely; customer-side evidence is what demonstrates the organization actually *is* operating it securely.

## 3.5 Section Takeaways: AWS and Azure Comparative Analysis

- **The Shared Responsibility Model is a provider-agnostic GRC principle, not an AWS-specific concept.** The provider/customer boundary, and how it shifts across IaaS, PaaS, and SaaS, holds identically on Azure -- a GRC analyst's understanding of the model transfers directly across cloud platforms, even though the specific native tool names (NSG vs. Security Groups) do not.
- **Customer misconfiguration risk categories are platform-agnostic.** Public storage exposure, missing MFA, unmonitored audit logs, and unassigned OS patching ownership are not AWS-specific or Azure-specific failure modes -- they are failure modes of the customer-side responsibility layer itself, and will recur on any cloud platform where that layer exists.
- **Provider assurance reports and customer-side evidence answer two different audit questions, on both platforms.** An auditor evaluating a cloud-hosted organization's security posture needs both AWS Artifact/Azure STP (does the provider's infrastructure meet its stated standard) and IAM/NSG/CloudTrail/Activity Log evidence (has the customer correctly configured what it controls) -- one type of evidence does not substitute for the other.

---

## References

- ISO/IEC 27001:2022 Annex A, Theme 8 -- Technological Controls (A.8.21-A.8.34 analyzed in this entry; completes full A.8.1-A.8.34 coverage across portfolio entries)
- ISO/IEC 27002:2022 -- Implementation guidance for Annex A controls
- ISO/IEC 27001:2022 Annex A.5.8, A.5.23, A.6.3, A.6.7, A.7.4, A.7.7 (cross-domain controls referenced in the SoA simulation)
- AWS Shared Responsibility Model
- Microsoft Azure Shared Responsibility in the Cloud (Microsoft Learn)
- Microsoft Azure Service Trust Portal documentation

---

*Return to: [Week 16 README](week16-readme.md)*
