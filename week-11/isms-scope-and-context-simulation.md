# ISMS Scope & Context Simulation: Practical Application of Clauses 4–6

> **Format:** Simulated organization case study — designed to demonstrate practical application of Clauses 4.1–4.4 and 6.1, not a real audit engagement
> **Organization:** RetailCo (fictional Thai e-commerce company, ~500 employees)

---

## Simulated Organization Profile

**RetailCo** operates an e-commerce platform serving customers across Thailand and neighboring ASEAN markets. Key characteristics relevant to ISMS scoping:

- Customer-facing web application (AWS-hosted, Singapore region)
- Back-office ERP system (on-premise, Bangkok data center)
- 12 branch offices connected via site-to-site VPN
- Payment processing via third-party PCI DSS-certified gateway
- ~500,000 registered customers; personal data processed = PDPA obligations triggered
- Currently pursuing ISO 27001:2022 certification for competitive differentiation

---

## Step 1: Context Analysis (Clause 4.1 + 4.2)

### External Issues Identified

| Category | Issue | ISMS Relevance |
|----------|-------|----------------|
| Regulatory | PDPA compliance mandatory (personal data of Thai residents) | Processing activities must be documented; security measures required under Section 37 |
| Regulatory | PCI DSS applies to cardholder data environment (even via third-party) | Scope must address CDE boundary clearly |
| Threat landscape | E-commerce sector is a primary target for Magecart-style JS injection | A.8.24 (cryptography), A.8.20 (network security), WAF controls |
| Third-party dependency | AWS shared responsibility model | Application-layer security is RetailCo's responsibility |
| Competition | Enterprise B2B clients require supplier ISO 27001 certification | Certification is a business requirement, not optional |

### Internal Issues Identified

| Category | Issue | ISMS Relevance |
|----------|-------|----------------|
| IT architecture | Hybrid environment (cloud + on-premise) complicates boundary definition | Scope statement must clearly map both environments |
| Organizational | No dedicated CISO; security managed by IT Manager | Clause 5.3 gap — information security accountability not formally assigned |
| Culture | Security viewed as "IT's problem" by business units | Clause 5.1 gap — leadership commitment not demonstrated |
| Process | Change management process exists but security review not integrated | Clause 6.3 gap — planned changes not evaluated for security impact |

### Stakeholder Requirements (Clause 4.2)

| Stakeholder | Requirement | Addressed in ISMS? |
|-------------|-------------|-------------------|
| B2B clients | ISO 27001 certification required | Yes — certification objective |
| PDPC (Thai regulator) | Appropriate security measures for personal data (PDPA s.37) | Yes — Annex A.8.24, A.5.15 |
| AWS (cloud provider) | Customer responsible for security in the cloud | Yes — reflected in scope statement |
| Employees | Clear information security policies and role expectations | Yes — Clause 5.2, 5.3 |
| Payment gateway | Data minimization; no storage of raw card data | Yes — out-of-scope cardholder data environment |

---

## Step 2: Scope Statement (Clause 4.3)

**Proposed ISMS Scope Statement:**

> The ISMS covers the information security management of RetailCo's e-commerce platform, customer data processing operations, and supporting technology infrastructure, including:
>
> - The customer-facing web application and API layer deployed on AWS (ap-southeast-1)
> - Customer personal data (account data, order history, delivery addresses) as processed and stored within the AWS environment
> - The Bangkok headquarters back-office ERP system
> - The network connectivity infrastructure connecting headquarters to 12 branch offices
> - All RetailCo-controlled identity and access management for the above systems
>
> **Exclusions:**
> - The payment processing cardholder data environment (managed by third-party PCI DSS-certified gateway; interface is the only scope boundary)
> - AWS physical infrastructure (in scope for AWS; governed by AWS SOC 2 reports and the Shared Responsibility Model)
> - Branch office physical security (covered under separate physical security policy)
>
> **Justification for exclusions:** Payment processing is fully delegated to a certified third party under contract; RetailCo never holds raw cardholder data. AWS physical security is AWS's contractual responsibility.

---

## Step 3: Risk Register (Clause 6.1)

The following risk register applies the organization's chosen risk assessment methodology: **Likelihood × Impact qualitative matrix**, scored 1–3 on each dimension.

**Risk scoring:**

| Likelihood | Definition |
|-----------|------------|
| 3 — High | Likely to occur within 12 months; threat is active and target is exposed |
| 2 — Medium | Possible within 12 months; some controls in place |
| 1 — Low | Unlikely; strong controls and low threat activity |

| Impact | Definition |
|--------|------------|
| 3 — High | Significant financial loss, regulatory penalty, or reputational damage; business disruption |
| 2 — Medium | Moderate operational impact; recoverable within days |
| 1 — Low | Minor disruption; no significant external impact |

**Risk Level = Likelihood × Impact:** 1–2 = Low, 3–4 = Medium, 6–9 = High/Critical

---

### Risk Register — Selected Entries

**Risk 001: Default Credentials on Branch Office Routers**

| Field | Detail |
|-------|--------|
| Asset | Branch network routers (×12) — gateways to corporate WAN |
| Threat | Unauthorized access via exploitation of known default credentials |
| Vulnerability | No credential change policy enforced at device deployment |
| Likelihood | 3 — High (default credentials publicly documented; actively exploited in the wild) |
| Impact | 3 — High (branch router compromise = lateral movement to corporate ERP and AWS VPN endpoint) |
| **Risk Level** | **9 — CRITICAL** |
| OWASP | A07:2021 — Identification and Authentication Failures |
| ISO 27001 Controls | A.8.20 (Network Security), A.5.15 (Access Control) |
| Treatment | Mitigate — immediate credential rotation; device hardening standard; quarterly credential audit |
| Residual Risk | 2 — Low-Medium (after treatment) |
| Owner | IT Infrastructure Manager |
| Target Date | Within 30 days |

---

**Risk 002: Plaintext Transmission of Credentials via HTTP**

| Field | Detail |
|-------|--------|
| Asset | Back-office ERP login interface |
| Threat | Credential interception via man-in-the-middle attack on internal network |
| Vulnerability | ERP login page served over HTTP (Port 80) — credentials transmitted in cleartext |
| Likelihood | 2 — Medium (requires network access; internal threat or compromised device) |
| Impact | 3 — High (ERP contains personal data of all customers and employees; PDPA Section 37(1) violation if credential compromise leads to data breach) |
| **Risk Level** | **6 — HIGH** |
| PDPA Reference | Section 37(1) — controller must implement appropriate security measures to protect personal data |
| ISO 27001 Controls | A.8.24 (Use of Cryptography) |
| Treatment | Mitigate — enforce HTTPS (TLS 1.2 minimum) on all authentication pages; deprecate HTTP |
| Corrective Action | Redirect HTTP to HTTPS via web server configuration; disable HTTP listener after migration |
| Residual Risk | 1 — Low |
| Owner | Application Development Lead |
| Target Date | Within 14 days |

---

**Risk 003: Inadequate VLAN Segmentation — Guest Wi-Fi to Internal Network**

| Field | Detail |
|-------|--------|
| Asset | Internal network segment (ERP, file servers) |
| Threat | Lateral movement from compromised guest device to internal systems |
| Vulnerability | Firewall ACL review found guest VLAN traffic to Internal Zone not fully restricted — ICMP and certain TCP ports permitted |
| Likelihood | 2 — Medium (guest network is physically accessible to visitors and contractors) |
| Impact | 3 — High (internal network access = potential ERP data exposure) |
| **Risk Level** | **6 — HIGH** |
| ISO 27001 Controls | A.8.20 (Network Security) — requirement for network segmentation |
| Treatment | Mitigate — update firewall ACL to implement explicit deny-all between Guest VLAN and Internal Zone; permit only whitelisted traffic (DNS, DHCP) |
| Residual Risk | 1 — Low |
| Owner | Network Security Engineer |
| Target Date | Within 7 days |

---

**Risk 004: Planned Cloud Migration Without Security Re-evaluation**

| Field | Detail |
|-------|--------|
| Asset | ISMS itself (scope, controls, risk treatment plan) |
| Threat | Material change to infrastructure renders existing risk assessment inaccurate |
| Vulnerability | Planned migration of on-premise ERP to AWS has no security impact assessment in the change management record |
| Likelihood | 3 — High (migration is scheduled; no process currently requires security review for ISMS changes) |
| Impact | 3 — High (ISMS becomes non-conformant; new cloud risks not addressed; PDPA exposure for data in transit during migration) |
| **Risk Level** | **9 — CRITICAL** |
| ISO 27001 Clause | 6.3 — Planning of changes |
| ISO 27001 Controls | A.5.23 (Information security for use of cloud services) |
| Treatment | Mitigate — implement change management gate requiring security impact assessment for any change affecting ISMS scope; complete cloud-specific risk assessment before migration proceeds |
| Residual Risk | 2 — Medium (migration risk remains; managed through assessed controls) |
| Owner | CISO (to be appointed) / IT Manager (interim) |
| Target Date | Before migration begins |

---

## Simulated Audit Finding Report

**Finding ID:** AF-2025-003
**Clause:** 6.3 — Planning of changes / 5.3 — Organizational roles, responsibilities and authorities
**Severity:** Major Nonconformity

**Observation:**
During review of change management records, the auditor noted that a planned migration of the on-premise ERP system to AWS (documented in the project registry as "ERP Cloud Migration — Q3 2025") has no associated information security impact assessment. Clause 6.3 of ISO 27001:2022 requires that changes to the ISMS be carried out in a planned manner. A migration of this scope — which would move all customer personal data covered by the PDPA into a new processing environment — represents a material change to the ISMS. No evidence was found that a risk assessment was performed or that Annex A.5.23 controls were considered.

Additionally, the CISO role referenced in the ISMS documentation is currently vacant, and no interim responsibility assignment is documented (Clause 5.3 gap).

**Root Cause:**
Change management procedure does not include an information security review gate. ISMS ownership is undefined during CISO vacancy.

**Corrective Action Required:**
1. Update change management procedure to require information security impact assessment for any planned change affecting ISMS scope or controls (Clause 6.3)
2. Formally document interim information security responsibility assignment until CISO appointment (Clause 5.3)
3. Complete cloud security risk assessment (Annex A.5.23) and update risk treatment plan before ERP migration proceeds

**Deadline:** 90 days

---

## References

- ISO/IEC 27001:2022 (official standard) — Clauses 4.1–4.4, 5.1–5.3, 6.1–6.3
- PDPA Thailand Section 37(1): https://www.pdpc.or.th/
- OWASP Top 10 2021 A07: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
