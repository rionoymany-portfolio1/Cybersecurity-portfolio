# Cybersecurity Portfolio

A self-directed, continuously documented cybersecurity portfolio — built to demonstrate that technical and GRC skills can coexist, and that a first-time candidate can think like a consultant before they have the job title.

---

## What This Portfolio Is For

Most junior cybersecurity portfolios are a list of certifications and a few CTF writeups. A recruiter reading one learns that the person can pass an exam and follow a guided lab. They do not learn whether that person can read a firewall ACL and connect it to a PDPA compliance gap, or explain to a client why a CVSS 10.0 vulnerability in their SAP system is a business-interruption risk, not just a patch ticket.

This portfolio is built to answer three questions a hiring manager actually has:

**1. Can they do the work?**
Technical content covers exploitation, reconnaissance, and vulnerability research — demonstrated through PortSwigger labs, TryHackMe rooms, DVWA practice, and custom Python tooling. GRC content covers ISO 27001:2022 clause analysis, risk registers, audit findings, and corrective action plans — applied to simulated organizational scenarios, not just read and summarized.

**2. Do they understand what the work means to a business?**
Every significant finding in this portfolio is translated into business consequence — financial exposure, regulatory liability (PDPA, GDPR), and impact on ISO 27001 certification. Figures are cited to primary sources, not invented. The goal is a finding report a CISO can hand to a board, not a technical document only another engineer can read.

**3. Can they sustain this without being told to?**
The commit history answers that. This is ongoing, self-directed work started at age 14, with no academic program, employer, or deadline requiring it.

---

## Track Structure

This portfolio covers two complementary tracks, roughly in a **70% GRC / 30% technical** split going forward — reflecting the target role of Cybersecurity Consultant (entry level) and the adjacent GRC Analyst path.

### GRC Track
- ISO/IEC 27001:2022 clause analysis and practical application
- Risk assessment methodology: risk registers, treatment plans, corrective action reports
- Network security auditing: firewall ACL review, topology analysis, log anomaly detection
- Control mapping across ISO 27001 Annex A, PDPA, OWASP, and NIST frameworks
- Simulated audit findings written in the format of a real engagement deliverable

### Technical Track
- Web application vulnerabilities: SQL injection, XSS (Reflected/Stored/DOM), file upload bypass, race conditions, IDOR
- Network reconnaissance: Nmap, passive recon, active recon, banner grabbing
- Custom tooling: Python port scanner, banner-grabbing scanner
- Real CVE case studies grounding every technique in documented, production-software incidents
- PortSwigger Web Security Academy labs: Apprentice through Expert difficulty

---

## How the Content Is Structured

Each week's folder is self-contained. The content structure adapts to the topic:

**For technical weeks**, each write-up follows a six-angle framework: Vulnerability → Exploitation → Business Impact → Technical Fix → Policy Fix → Detection Rule. Supporting files cover the lab walkthrough, CVE case studies, bypass technique reference, and business impact analysis with cited sources.

**For GRC weeks**, content uses a different framework suited to compliance work: Requirement → Interpretation → Organizational Application → Evidence/Artifacts → Common Gaps → Related Controls. Deliverables include annotated clause analysis, simulated risk registers, audit findings, and corrective action plans.

File names describe their content. There is no rigid template imposing the same six files on every week regardless of what that week's material actually needs.

---

## What "Blended" Actually Means

The combination of GRC and technical is not a hedge — it is the specific skill set that makes a consultant useful rather than just a specialist.

A GRC analyst who cannot read a firewall ACL cannot audit network segmentation controls. They can verify that a policy document exists. An analyst who understands both can identify that a "PERMIT IP ANY ANY" rule between the DMZ and the internal zone renders the entire network segmentation architecture ineffective — and write the finding in language a non-technical CFO can act on.

A technical practitioner who cannot connect a CVSS score to a business consequence cannot advise a client on remediation prioritization. They can identify a vulnerability. A practitioner who understands both can explain why a CVSS 9.8 flaw in an internet-facing SAP system is a manufacturing-downtime risk worth modeling at $500K–$1M per hour, and why that changes which fix gets funded first.

That is the work this portfolio is built to demonstrate.

---

## Analytical Standards

Business impact figures in this portfolio are sourced and cited, not estimated. Technical claims are verified before being written. Where a source cannot be confirmed, the claim is either removed or explicitly labeled as an estimate with its reasoning shown.

This standard exists because the same discipline applies in a real consulting engagement: a finding report that overstates severity loses credibility, and a finding report that cites a number the client cannot verify will be questioned in the room.

---

## Target Roles

- **Cybersecurity Consultant (Junior / Entry Level)** — blended GRC and technical, client-facing deliverables
- **GRC Analyst (Entry Level)** — ISO 27001 / risk management / compliance focus

Both roles are being pursued simultaneously. The portfolio is structured to be relevant to either conversation.

---

## Repository

**GitHub:** [Cybersecurity-portfolio](https://github.com/rionoymany-portfolio1/Cybersecurity-portfolio)
**Started:** 2025, age 14
**Status:** Active — updated weekly

---

## Reference Frameworks

- ISO/IEC 27001:2022 — https://www.iso.org/standard/27001
- OWASP Top 10 — https://owasp.org/Top10/
- NVD (National Vulnerability Database) — https://nvd.nist.gov/
- CWE (Common Weakness Enumeration) — https://cwe.mitre.org/
- PDPA Thailand — https://www.pdpc.or.th/
- NIST Cybersecurity Framework — https://www.nist.gov/cyberframework
- PortSwigger Web Security Academy — https://portswigger.net/web-security
- TryHackMe — https://tryhackme.com/
