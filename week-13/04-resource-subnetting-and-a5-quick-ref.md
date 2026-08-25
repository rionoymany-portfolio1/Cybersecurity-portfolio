# Resource: Quick Reference — IPv4 Subnetting & ISO 27001 Annex A.5 Audit Checklist

> **Purpose:** Fast-lookup reference sheet for use during live subnetting calculations and A.5 audit checks
> **Companion Files:** [Technical Write-Up](technical-write-up-annex-a5-and-subnetting.md) · [Business Impact & Risk Analysis](business-impact-audit-finding-firewall-subnetting.md)

---

## Part 1 — IPv4 Subnetting Cheat Sheet

### 1.1 — Full-Octet CIDR Reference (Class-Boundary Level)

| CIDR | Subnet Mask | Total Addresses | Common Use |
|:----:|:-----------:|:----------------:|-----------|
| /8 | `255.0.0.0` | 16,777,216 | Class A default |
| /16 | `255.255.0.0` | 65,536 | Class B default |
| /24 | `255.255.255.0` | 256 | Class C default |
| /32 | `255.255.255.255` | 1 | Single host route |

### 1.2 — Interesting-Octet Reference (Sub-Class Subnetting)

The single most-used table for manual subnetting — covers every non-full-octet mask value.

| Binary (1 octet) | Decimal | CIDR bits added | Block Size |
|:-----------------:|:-------:|:----------------:|:----------:|
| `0000 0000` | 0 | +0 | 256 |
| `1000 0000` | 128 | +1 | 128 |
| `1100 0000` | 192 | +2 | 64 |
| `1110 0000` | 224 | +3 | 32 |
| `1111 0000` | 240 | +4 | 16 |
| `1111 1000` | 248 | +5 | 8 |
| `1111 1100` | 252 | +6 | 4 |
| `1111 1110` | 254 | +7 | 2 |
| `1111 1111` | 255 | +8 | 1 |

> **Block Size formula:** `256 − (interesting octet decimal value)` — this is the "Inverting Mask" shortcut in one step.

### 1.3 — Full CIDR-to-Mask Table (/1 – /32)

| CIDR | Mask | CIDR | Mask | CIDR | Mask | CIDR | Mask |
|:----:|------|:----:|------|:----:|------|:----:|------|
| /1 | 128.0.0.0 | /9 | 255.128.0.0 | /17 | 255.255.128.0 | /25 | 255.255.255.128 |
| /2 | 192.0.0.0 | /10 | 255.192.0.0 | /18 | 255.255.192.0 | /26 | 255.255.255.192 |
| /3 | 224.0.0.0 | /11 | 255.224.0.0 | /19 | 255.255.224.0 | /27 | 255.255.255.224 |
| /4 | 240.0.0.0 | /12 | 255.240.0.0 | /20 | 255.255.240.0 | /28 | 255.255.255.240 |
| /5 | 248.0.0.0 | /13 | 255.248.0.0 | /21 | 255.255.248.0 | /29 | 255.255.255.248 |
| /6 | 252.0.0.0 | /14 | 255.252.0.0 | /22 | 255.255.252.0 | /30 | 255.255.255.252 |
| /7 | 254.0.0.0 | /15 | 255.254.0.0 | /23 | 255.255.254.0 | /31 | 255.255.255.254 |
| /8 | 255.0.0.0 | /16 | 255.255.0.0 | /24 | 255.255.255.0 | /32 | 255.255.255.255 |

### 1.4 — Host Bits to Usable Hosts Quick Lookup

| Host Bits | Formula | Usable Hosts |
|:---------:|:-------:|:-------------:|
| 2 | 2² − 2 | 2 |
| 3 | 2³ − 2 | 6 |
| 4 | 2⁴ − 2 | 14 |
| 5 | 2⁵ − 2 | 30 |
| 6 | 2⁶ − 2 | 62 |
| 7 | 2⁷ − 2 | 126 |
| 8 | 2⁸ − 2 | 254 |
| 9 | 2⁹ − 2 | 510 |
| 10 | 2¹⁰ − 2 | 1,022 |
| 12 | 2¹² − 2 | 4,094 |

### 1.5 — Four-Step Manual Calculation Process

```
1. IDENTIFY the interesting octet (first octet in mask that isn't 255 or 0)
2. FIND the block size -> 256 − (interesting octet value)
3. LOCATE the subnet boundary -> floor(target octet ÷ block size) × block size
4. DERIVE broadcast/last host -> next boundary − 1 (broadcast) or − 2 (last host)
```

> **Common error trap:** Confusing adjacent CIDR/mask pairs (e.g., `/19` and `/20`, corresponding to block sizes 32 vs. 16) produces a wrong-but-plausible subnet boundary — always re-verify against Table 1.2 before finalizing an answer. Full analysis: [Technical Write-Up §2.2](technical-write-up-annex-a5-and-subnetting.md#22-root-cause-error-analysis-when-mental-shortcuts-fail).

---

## Part 2 — ISO 27001 Annex A.5 Quick Audit Checklist

Condensed checklist for a rapid A.5 (Organizational Controls) spot-check. Full control-by-control detail: [Technical Write-Up](technical-write-up-annex-a5-and-subnetting.md).

### 2.1 — Governance Foundation (A.5.1 – A.5.6)

- [ ] Information security policy exists, is management-approved, and has a defined review date (A.5.1)
- [ ] Security roles/responsibilities are documented with no accountability gaps (A.5.2)
- [ ] Conflicting duties (request vs. approve) are assigned to different individuals (A.5.3)
- [ ] Defined contact points exist for regulators/law enforcement (A.5.5)

### 2.2 — Risk & Project Inputs (A.5.7 – A.5.8)

- [ ] Threat intelligence is *analyzed against the asset inventory*, not just collected (A.5.7)
- [ ] Security requirements are embedded at project initiation, not added pre-launch (A.5.8)

### 2.3 — Asset & Information Handling (A.5.9 – A.5.14)

- [ ] Asset inventory is current and complete (A.5.9)
- [ ] Acceptable Use Policy exists and has an enforcement mechanism (A.5.10)
- [ ] Offboarding includes verified asset return (A.5.11)
- [ ] Classification scheme is defined AND consistently applied/labelled (A.5.12, A.5.13)

### 2.4 — Access Governance (A.5.15 – A.5.18) — Priority Focus

- [ ] Access control policy exists and rules trace to documented business need (A.5.15)
- [ ] **Joiner-Mover-Leaver lifecycle is enforced — specifically check "Mover" transitions for access accumulation** (A.5.15)
- [ ] No shared/generic accounts without a compensating control (A.5.16)
- [ ] MFA/credential standards are defined and enforced (A.5.17)
- [ ] Periodic access rights recertification is evidenced, not assumed (A.5.18)

### 2.5 — Supplier & Cloud Relationships (A.5.19 – A.5.23) — Priority Focus

- [ ] Supplier risk assessment occurs **before** onboarding, not after (A.5.19)
- [ ] Contracts contain explicit security clauses: audit rights, incident notification window, data handling terms (A.5.20)
- [ ] Sub-processor/sub-contractor visibility is required and disclosed (A.5.21)
- [ ] Supplier security posture is re-reviewed on service change, not one-time only (A.5.22)
- [ ] Cloud shared-responsibility boundary is documented (A.5.23)

### 2.6 — Incident Management (A.5.24 – A.5.28)

- [ ] Incident response plan is current and has assigned roles (A.5.24)
- [ ] Event-to-incident escalation criteria are defined (A.5.25)
- [ ] Post-incident review produces documented lessons learned (A.5.27)
- [ ] Evidence handling meets chain-of-custody standards (A.5.28)

### 2.7 — Continuity & Compliance (A.5.29 – A.5.37)

- [ ] BCP/DR technical recovery is tested against defined RTO/RPO (A.5.30)
- [ ] Compliance register maps applicable law (e.g., PDPA) to specific controls (A.5.31)
- [ ] Records retention schedule is defined and enforced (A.5.33)
- [ ] Independent review (internal audit) occurs at planned intervals with reviewer independence (A.5.35)
- [ ] Operating procedures are documented and accessible to those who need them (A.5.37)

---

## References

- ISO/IEC 27001:2022 Annex A, Theme 5 — Organizational Controls
- RFC 4632 — Classless Inter-Domain Routing (CIDR)

---

*Return to: [Week 13 README](week13-readme.md)*
