# Business Impact & Risk Analysis: Audit Finding — Over-Permissive Firewall Rule via Subnet Calculation

> **Format:** Simulated audit finding — technical subnet analysis conducted as part of a GRC firewall rule review
> **Organization Type:** Financial Institution (simulated)
> **Companion Files:** [Technical Write-Up](technical-write-up-annex-a5-and-subnetting.md) · [Resources & Quick Reference](resource-subnetting-and-a5-quick-ref.md)

---

## 1. Scenario Background

**Organization Profile:** A simulated regional financial institution processing customer account data, transaction records, and financial PII within a segmented internal network. As a financial services organization, the entity operates under heightened regulatory scrutiny — data confidentiality and access control failures carry direct financial regulatory exposure in addition to standard data protection obligations, which materially raises the business impact of any access control finding relative to a lower-sensitivity industry.

**Audit Context:** During a routine internal firewall rule review — the kind of exercise required to produce evidence for **ISO 27001 Clause 9.2 (Internal Audit)** — the following rule was identified permitting access into the Database Zone hosting the core financial database:

```
# Firewall ruleset excerpt — reviewed rule
# Zone: Internal-Application -> DB-Zone

Rule 14:  PERMIT TCP 10.0.0.0/20 -> DB-Zone:5432   [Finding — scope review required]
```

**Initial Observation:** Port 5432 is the default port for PostgreSQL — the rule is intentionally permitting database traffic, not a stray misconfiguration. The finding is not that database access exists; it is that the **source scope permitted to reach the database (`10.0.0.0/20`) is defined at a network block far larger than any documented business justification supports.**

---

## 2. Technical Subnet Breakdown

### 2.1 — What `/20` Actually Authorizes

| Property | Value |
|----------|-------|
| CIDR notation | `/20` |
| Subnet mask | `255.255.240.0` |
| Block size (3rd octet) | 16 |
| Network address | `10.0.0.0` |
| Broadcast address | `10.0.15.255` |
| **Total addresses in block** | **2³² ⁻ ²⁰ = 2¹² = 4,096** |
| Usable host addresses | 4,094 |

### 2.2 — The Scope in Plain Terms

```
Rule as written: PERMIT TCP 10.0.0.0/20 -> DB-Zone:5432

Address range authorized:  10.0.0.0  through  10.0.15.255
                            └──────── 4,096 total IP addresses ────────┘

Any single one of these 4,096 addresses is currently permitted
to open a TCP connection directly to the financial database.
```

For context on what a `/20` block represents in a typical network design: it is large enough to encompass an **entire building's worth of workstations, printers, IoT devices, guest network equipment, and any other host that happens to receive a DHCP lease within that address range** — not merely the specific application servers that have a legitimate, documented need to query the database.

### 2.3 — The Governance Question a Subnet Calculation Answers

A firewall rule syntax check confirms the rule is technically valid — port 5432 is correctly specified, the CIDR notation is correctly formed, the rule will function exactly as written. **Syntactic validity and security adequacy are two entirely different questions, and only the second one is the GRC practitioner's concern.** Calculating that `/20` equals 4,096 addresses is what converts "this rule looks fine" into "this rule authorizes four thousand times more access than a single application server requires" — a finding a syntax-only review would never surface.

---

## 3. GRC Audit Finding & Risk Mapping

**Finding Classification:** Major Nonconformity (candidate) — pending confirmation of documented business justification

**Severity:** HIGH

| Field | Detail |
|-------|--------|
| **Observation** | Firewall rule permits TCP/5432 (database) access from a `/20` source block (4,096 addresses) into the financial database zone, with no evidence the full scope reflects an intentional, documented access requirement |
| **Root Cause (hypothesis)** | Rule likely configured at the containing network block level for administrative convenience during initial setup, rather than scoped to the specific application server(s) requiring database connectivity — a pattern consistent with rules that are never revisited after initial deployment |
| **ISO 27001 Control Mapping** | **A.5.15** (Access Control) — primary; **A.5.18** (Access Rights) — secondary |

### 3.1 — Control Mapping Detail

| Control | Title | Gap Identified |
|---------|-------|-----------------|
| **A.5.15** | Access control | The access control policy requirement — that rules be established "based on business and information security requirements" — is not evidenced by this rule. A `/20` scope has no apparent connection to a specific, documented business need; it reads as a default or convenience configuration rather than a deliberate access decision. |
| **A.5.18** | Access rights | Access rights provisioning (which hosts *should* reach the database) has not been kept aligned with access rights as actually implemented (which hosts *can* reach the database per this rule). The gap between intended and implemented scope is the specific failure mode A.5.18 periodic access review exists to catch. |

### 3.2 — Business and Regulatory Impact

For a financial institution, the database in scope holds customer account and transaction data — the exact data category subject to the highest regulatory sensitivity in the organization's risk profile. The business impact of this finding operates on two levels:

**Attack surface:** Any of the 4,096 addresses within `10.0.0.0/20` — including hosts that were never intended to have database connectivity, and including any device that is later compromised, misconfigured, or connected to that address range without the security team's awareness — has a direct network path to the financial database on its service port. The rule does not require an attacker to compromise a specific, known application server; it requires only that the attacker obtain *any* foothold within a very large address range.

**Regulatory posture:** A financial services regulator (or an ISO 27001 certification auditor) reviewing this rule during an examination would reasonably ask: *"What is the specific business justification for authorizing 4,096 addresses to reach a database containing customer financial data?"* In the likely scenario that no such justification exists — because the rule was configured at the block level for convenience rather than derived from a documented access requirement — the finding would be classified as a **Major Nonconformity against A.5.15**, sufficient on its own to block certification or trigger suspension of an existing one. This is a materially worse audit outcome than a narrowly-scoped rule with a clear one-line justification on file.

---

## 4. Remediation Recommendation

### 4.1 — Recommended Scope Reduction

| Option | Scope | Addresses Authorized | When Appropriate |
|--------|-------|----------------------|-------------------|
| **Preferred: Host-specific** | `/32` per application server | 1 (each) | When the exact, finite set of application servers requiring database access is known and stable |
| **Acceptable: Narrow subnet** | `/29` | 8 (6 usable) | When a small, defined application tier (e.g., a load-balanced cluster of app servers) requires database access and host-level rules are impractical to maintain |

**Primary recommendation:** Replace the single `/20` rule with **explicit `/32` host rules for each specific application server** with a documented, legitimate need to query the database. Where the application tier is a small, defined cluster rather than fixed individual hosts, a `/29` covering only that cluster's address range is an acceptable middle ground — but the reduction from 4,096 addresses to 8 addresses (a **99.8% scope reduction**) still represents the actionable target regardless of which option is selected.

```
BEFORE:  PERMIT TCP 10.0.0.0/20  -> DB-Zone:5432   (4,096 addresses)

AFTER (preferred):
         PERMIT TCP 10.0.8.15/32 -> DB-Zone:5432   (App Server 1 — 1 address)
         PERMIT TCP 10.0.8.16/32 -> DB-Zone:5432   (App Server 2 — 1 address)
         DENY    TCP 10.0.0.0/20 -> DB-Zone:5432   (explicit deny — all other sources)

AFTER (acceptable, if cluster is dynamic):
         PERMIT TCP 10.0.8.8/29  -> DB-Zone:5432   (App tier cluster — 8 addresses)
         DENY    TCP 10.0.0.0/20 -> DB-Zone:5432   (explicit deny — all other sources)
```

### 4.2 — Business Justification for Remediation

**Principle of Least Privilege:** Access should be granted only to the minimum scope required to perform a legitimate function — nothing about the database's operational requirements changes based on which of the 4,096 addresses in `10.0.0.0/20` happens to make the connection. The rule should reflect exactly which hosts have that legitimate function, not the convenient containing block they happen to sit within.

**Zero Trust Alignment:** A Zero Trust posture treats network location as providing no inherent trust — a host is not implicitly trusted to reach the database merely because it resides somewhere within the internal `10.0.0.0/20` range. Scoping the rule to specific, known, and continuously-justified hosts (or a tightly-bound cluster) is the network-layer expression of that principle: trust is granted per-host based on verified need, not inherited from broad network placement.

**Attack Surface Reduction:** Reducing the authorized source scope from 4,096 addresses to 8 (or 1 per host) removes 99.8%+ of the addresses that currently have a viable network path to the financial database — directly shrinking the population of hosts an attacker could compromise and use as a pivot point into the database tier.

**Regulatory Compliance Alignment:** A narrowly-scoped, individually-justified rule set directly satisfies the A.5.15 requirement that access be established based on documented business need, and gives the organization a defensible, evidence-backed answer if a regulator or certification auditor asks why each specific host has database access.

*Owner: Network Security Engineer (implementation) / GRC Analyst (evidence and closure verification) | Timeline: 14 days | Priority: HIGH*

---

## 5. Key Takeaways

- **A `/20` rule and a `/32` rule can both be syntactically perfect and functionally correct — the difference between them is a governance decision, not a technical one.** A firewall will enforce either rule flawlessly; only a GRC-informed review asks whether the scope matches a documented need.
- **The specific number matters for communicating severity.** "The rule is too broad" is a vague technical observation. "This rule authorizes 4,096 addresses to reach the financial database, and only 2 servers actually need that access" is a quantified finding that makes the remediation priority self-evident to a non-technical stakeholder.
- **Subnet calculation is not a standalone technical skill in this context — it is the evidence-generation step of an access control audit finding.** See the companion [Technical Write-Up](technical-write-up-annex-a5-and-subnetting.md) for the calculation discipline (and the specific error class) that this finding depends on being executed correctly.

---

## References

- ISO/IEC 27001:2022 Annex A.5.15 (Access control), A.5.18 (Access rights)
- RFC 4632 — Classless Inter-Domain Routing (CIDR)
- NIST SP 800-207 — Zero Trust Architecture: https://csrc.nist.gov/publications/detail/sp/800-207/final
- IANA Port Number Registry (Port 5432 — PostgreSQL): https://www.iana.org/assignments/service-names-port-numbers/

---

*This case study was developed as part of a self-directed cybersecurity portfolio project. All organizations, systems, and data referenced are entirely fictional and created for educational purposes.*

---

*Return to: [Week 13 README](week13-readme.md)*
