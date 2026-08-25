# Week 13: ISO 27001 Annex A.5 Deep-Dive & IPv4 Subnetting Mastery

> **Period:** August 17–22, 2026
> **Format:** Self-directed study (ISO 27001 Annex A.5) + hands-on calculation practice (IPv4 subnetting) + applied GRC case study synthesis
> **Method:** AI-assisted concept discussion for A.5 controls; manually-solved subnetting problem set, cross-verified programmatically
> **Approach:** Governance framework study -> technical calculation drilling -> real-world audit finding synthesis connecting the two

---

## Executive Summary

This week combined two distinct but deliberately connected disciplines: a deep study of **ISO/IEC 27001:2022 Annex A.5 (Organizational Controls)** — all 37 controls, with focused analysis on three that recur most often in real GRC practice — and a **20-problem IPv4 subnetting drill** aimed at building calculation speed and accuracy.

The connective work of the week was demonstrating that these two disciplines are not parallel tracks but a single skill: **a firewall rule with an oversized subnet scope is not merely a technical misconfiguration — it is a potential Annex A.5.15 (Access Control) nonconformity.** The [Business Impact & Risk Analysis](business-impact-audit-finding-firewall-subnetting.md) file applies subnet arithmetic directly to a simulated financial-institution audit finding, translating a raw CIDR calculation (`/20` = 4,096 addresses) into a quantified, regulator-facing risk finding with a scoped remediation.

> **Scope note:** The governance analysis this week is limited to **Annex A.5 (Organizational Controls) only** — 37 of ISO 27001:2022's 93 total Annex A controls. It does not represent a complete ISMS or Annex A review. A.6 (People), A.7 (Physical), and A.8 (Technological) controls are addressed separately in other portfolio entries and are explicitly out of scope for this week's work.

---

## Repository Directory Structure

```
week-13/
├── week13-readme.md                                          (this file — weekly dashboard)
├── technical-write-up-annex-a5-and-subnetting.md              (Deep-dive: 37 A.5 controls + 20-problem subnetting log)
├── business-impact-audit-finding-firewall-subnetting.md       (Applied case: subnet calc to audit finding)
└── resource-subnetting-and-a5-quick-ref.md                    (Fast-lookup reference: both disciplines)
```

---

## Key Metrics & Outcomes

| Metric | Result |
|--------|:------:|
| Annex A.5 controls reviewed | **37 / 37** (100% of theme) |
| Controls examined in depth | 5 (A.5.1, A.5.2, A.5.7, A.5.15, A.5.19/20) |
| Subnetting problems solved | **20 / 20** |
| Subnetting answers independently verified | **20 / 20 correct** (Python `ipaddress`, RFC 4632) |
| Real-world audit case studies produced | 1 (financial institution, over-permissive `/20` DB rule) |
| ISO 27001 controls mapped in case study | A.5.15, A.5.18 |
| Firewall rule scope reduction demonstrated | 4,096 addresses to 8 or 1 (**99.8%+ reduction**) |

---

## Links to Sub-Modules

### [Technical Write-up: Annex A.5 & Subnetting](technical-write-up-annex-a5-and-subnetting.md)
Full review of all 37 A.5 controls, with in-depth analysis of **A.5.15** (Access Control — Joiner-Mover-Leaver lifecycle), **A.5.19/A.5.20** (Supplier Relationships — the process/instrument pairing), and **A.5.7** (Threat Intelligence — the contextualization requirement), plus **A.5.1/A.5.2** examined as the foundational dependency for the other 35 controls. Followed by the full 20-problem IPv4 subnetting practice log — calculation shortcuts, a root-cause human-error analysis, and a complete verification table.

### [Business Impact & Risk Analysis: Audit Finding Case Study](business-impact-audit-finding-firewall-subnetting.md)
Applied synthesis connecting both disciplines from the write-up: a simulated financial-institution audit finding on a `PERMIT TCP 10.0.0.0/20 -> DB-Zone:5432` rule. Full subnet breakdown (4,096 addresses authorized), A.5.15/A.5.18 control mapping, and a remediation recommendation grounded in Least Privilege and Zero Trust principles.

### [Resource: Quick Reference — Subnetting & A.5 Audit Checklist](resource-subnetting-and-a5-quick-ref.md)
Condensed, fast-lookup cheat sheet — full CIDR-to-mask conversion table, host-bit calculations, and a checklist-style A.5 audit quick-reference organized by control grouping.

---

## Key Takeaways

- **Technical skill and governance skill are not separate tracks — this week's structure was designed to prove that directly.** A subnet calculation error and a firewall rule audit finding are the same failure mode observed at two different stages: one caught during practice, one caught during audit.
- **Annex A.5's 37 controls are process governance, not device configuration.** They exist to ensure technical controls (the A.8 theme) stay correctly configured and accountable over time, rather than correct only at the moment they were first set up — a distinction made concrete in this week's case study, where a syntactically perfect firewall rule was still a governance finding.
- **A misconfigured network scope does not fail loudly.** Both the subnetting error analysis and the audit finding case study converge on the same underlying lesson: an oversized `/20` block and a miscalculated subnet boundary both produce a result that looks structurally correct. Neither error type announces itself — both require a deliberate, systematic verification step to catch, whether that step is re-checking a homework answer or auditing a production firewall rule.
- **This week's governance scope was intentionally narrow (A.5 only) to allow depth over breadth.** Five controls (A.5.1, A.5.2, A.5.7, A.5.15, A.5.19/20) were studied to a level where the underlying *why* — not just the control text — could be explained and applied to a novel scenario (the case study). That depth-first approach is the target model for future weeks covering A.6, A.7, and A.8.

---

## References

- ISO/IEC 27001:2022 (Third Edition), Annex A, Theme 5 — Organizational Controls
- ISO/IEC 27002:2022 — Implementation guidance for Annex A controls
- RFC 4632 — Classless Inter-Domain Routing (CIDR)
- PDPA Thailand (B.E. 2562), Section 37: https://www.pdpc.or.th/
- NIST SP 800-207 — Zero Trust Architecture: https://csrc.nist.gov/publications/detail/sp/800-207/final

---

*This portfolio entry was developed as part of a self-directed cybersecurity and GRC learning program. All organizations, systems, and data referenced in case studies are entirely fictional and created for educational purposes.*
